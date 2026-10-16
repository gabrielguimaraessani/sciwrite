#!/usr/bin/env python3
"""Validate this repository's restricted metadata schemas and editorial coverage.

Standard library only. This is structural validation, not an LLM evaluator or a
general YAML parser. The separate skill-creator validator can parse full YAML.
"""
import argparse
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

MODES = ('full-review', 'section-review', 'targeted', 'interactive',
         'structural-review', 'planning')
PRINCIPLES = {f'P{i:02d}' for i in range(1, 45)}
MODULES = ('principles', 'evidence-and-integrity', 'structure-and-sections',
           'tables-and-figures', 'review-articles', 'reviewer-responses',
           'other-genres', 'broader-audiences', 'grants-and-recommendations')
LICENSE_BLOB = 'c527d5c8603248c21a4ab2ab37d5846efd04d3d3'


def slug(text):
    return re.sub(r'[^\w -]', '', text.lower()).replace(' ', '-')


def validate(root):
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    required = ['SKILL.md', 'README.md', 'HOW-TO-USE.md', 'LICENSE',
                'agents/openai.yaml', 'docs/coverage.md', 'docs/provenance.md',
                'docs/evaluation-results.md', 'evals/cases.json', 'evals/cases.md']
    required += [f'references/{name}.md' for name in MODULES]
    for name in required:
        require((root / name).is_file(), f'Missing required file: {name}')
    if errors:
        return errors

    skill = (root / 'SKILL.md').read_text(encoding='utf-8')
    # Deliberately accept only this project's two-key, folded-description schema.
    front = re.match(r'\A---\nname: ([a-z0-9]+(?:-[a-z0-9]+)*)\n'
                     r'description: >\n((?:  [^\n]+\n)+)---\n', skill)
    require(front is not None, 'Invalid restricted SKILL frontmatter schema')
    if front:
        require(front[1] == 'manuscript-writing-review', 'Legacy skill name changed')
        description = ' '.join(line.strip() for line in front[2].splitlines())
        require(0 < len(description) <= 1024, 'Description length invalid')
    require(len(skill.splitlines()) < 500, 'SKILL.md exceeds the 500-line guide')
    for mode in MODES:
        require(f'`{mode}`' in skill, f'Missing mode: {mode}')
    for i in range(1, 6):
        require(f'### Pass {i}:' in skill, f'Missing legacy audit: Pass {i}')
    for module in MODULES:
        require(f'(references/{module}.md)' in skill, f'Unrouted module: {module}')

    principles = (root / 'references/principles.md').read_text(encoding='utf-8')
    ids = re.findall(r'^### (P\d{2}) — .+$', principles, re.M)
    require(ids == [f'P{i:02d}' for i in range(1, 45)],
            'Canonical principles must be unique and ordered P01–P44')

    coverage = (root / 'docs/coverage.md').read_text(encoding='utf-8')
    coverage_ids = re.findall(r'^\| (P\d{2}) \|', coverage, re.M)
    require(coverage_ids == [f'P{i:02d}' for i in range(1, 45)],
            'Coverage must have one ordered row for each principle')
    try:
        cases = json.loads((root / 'evals/cases.json').read_text(encoding='utf-8'))
        require(isinstance(cases, list) and bool(cases), 'Cases must be a nonempty array')
        if not isinstance(cases, list):
            return errors
        case_ids = []
        evaluated = set()
        for case in cases:
            require(isinstance(case, dict), 'Each case must be an object')
            if not isinstance(case, dict):
                continue
            case_ids.append(case.get('id'))
            for key in ('id', 'request', 'input', 'expected', 'forbidden'):
                require(isinstance(case.get(key), str) and bool(case[key].strip()),
                        f'Case {case.get("id")} missing {key}')
            pids = case.get('principles')
            require(isinstance(pids, list) and bool(pids),
                    f'Case {case.get("id")} needs principle IDs')
            if isinstance(pids, list):
                require(all(isinstance(p, str) and p in PRINCIPLES for p in pids),
                        f'Unknown principle in {case.get("id")}')
                evaluated.update(p for p in pids if isinstance(p, str))
        require(case_ids == [f'E{i:02d}' for i in range(1, len(cases) + 1)],
                'Case IDs must be unique, sequential, and ordered')
        require(PRINCIPLES <= evaluated,
                f'Principles without a scenario: {sorted(PRINCIPLES - evaluated)}')
        known_cases = set(case_ids)
        for line in coverage.splitlines():
            if re.match(r'^\| P\d{2} \|', line):
                pid = line.split('|')[1].strip()
                mapped = re.findall(r'\bE\d{2}\b', line)
                require(bool(mapped), f'Coverage row has no scenario: {pid}')
                require(all(cid in known_cases for cid in mapped),
                        f'Coverage references unknown scenario: {pid}')
                require(all(any(c.get('id') == cid and pid in c.get('principles', [])
                                for c in cases) for cid in mapped),
                        f'Coverage scenario does not exercise {pid}')
        readable = (root / 'evals/cases.md').read_text(encoding='utf-8')
        require(re.findall(r'^## (E\d{2}) —', readable, re.M) == case_ids,
                'Readable scenario catalogue diverges from JSON IDs')
    except (ValueError, TypeError, KeyError) as exc:
        errors.append(f'Invalid fixture structure: {exc}')

    metadata = (root / 'agents/openai.yaml').read_text(encoding='utf-8')
    require(metadata.startswith('interface:\n'), 'Metadata must declare interface')
    values = {}
    for line in metadata.splitlines()[1:]:
        match = re.fullmatch(r'  ([a-z_]+): (".*")', line)
        require(match is not None, 'Metadata uses unsupported schema/unquoted value')
        if match:
            try:
                values[match[1]] = json.loads(match[2])
            except ValueError:
                errors.append('Invalid metadata quoted scalar')
    require(set(values) == {'display_name', 'short_description', 'default_prompt'},
            'Unexpected or missing interface fields')
    require(25 <= len(values.get('short_description', '')) <= 64,
            'Interface short description must have 25–64 characters')
    require('$manuscript-writing-review' in values.get('default_prompt', ''),
            'Default prompt must mention the skill')

    for path in root.rglob('*.md'):
        if '.git' in path.parts:
            continue
        text = path.read_text(encoding='utf-8')
        require(text.count('```') % 2 == 0, f'Unbalanced code fence: {path.name}')
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            relative = unquote(parsed.path)
            dest = (root / relative.lstrip('/') if relative.startswith('/')
                    else path.parent / relative) if relative else path
            dest = dest.resolve()
            require(dest.is_relative_to(root.resolve()), f'Link escapes repository: {target}')
            require(dest.is_file(), f'Broken link in {path.name}: {target}')
            if dest.is_file() and parsed.fragment and dest.suffix == '.md':
                headings = re.findall(r'^#{1,6} (.+)$', dest.read_text(encoding='utf-8'), re.M)
                require(unquote(parsed.fragment) in {slug(h) for h in headings},
                        f'Unknown anchor in {path.name}: {target}')

    license_bytes = (root / 'LICENSE').read_bytes()
    blob = hashlib.sha1(f'blob {len(license_bytes)}\0'.encode() + license_bytes).hexdigest()
    require(blob == LICENSE_BLOB, 'Upstream license changed unexpectedly')
    return errors


def self_test(root):
    mutations = {
        'broken reference': lambda p: (p / 'references/tables-and-figures.md').unlink(),
        'duplicate principle': lambda p: (p / 'references/principles.md').write_text(
            (p / 'references/principles.md').read_text() + '\n### P01 — Duplicate\n'),
        'unknown case principle': lambda p: (p / 'evals/cases.json').write_text(
            (p / 'evals/cases.json').read_text().replace('"P01"', '"P99"', 1)),
        'missing legacy mode': lambda p: (p / 'SKILL.md').write_text(
            (p / 'SKILL.md').read_text().replace('`interactive`', '`removed`')),
    }
    for label, mutate in mutations.items():
        with tempfile.TemporaryDirectory(prefix='sciwrite-validation-') as directory:
            copy = Path(directory) / 'skill'
            shutil.copytree(root, copy, ignore=shutil.ignore_patterns('.git', '__pycache__'))
            mutate(copy)
            if not validate(copy):
                raise RuntimeError(f'Validator missed mutation: {label}')
    print(f'Negative validation checks passed: {len(mutations)}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        for error in errors:
            print(f'ERROR: {error}')
        return 1
    print('Static validation passed: 44 principles, linked coverage, modes, modules, fixtures, metadata, license.')
    if args.self_test:
        self_test(args.root)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
