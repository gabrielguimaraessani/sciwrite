# SciWrite — scientific clarity and evidence fidelity

A modular extension of [Lorena A. Barba's SciWrite](https://github.com/labarba/sciwrite),
based on the scientific-writing methodology associated with Kristin Sainani's
[Writing in the Sciences](https://www.coursera.org/learn/sciwrite) course.

Review scientific writing from argument to sentence while preserving data,
uncertainty, terminology, authorship, and the author's voice. This fork organizes
44 principles into actionable checks, retaining SciWrite's five audit passes
and four original review modes.

## What changes in this fork

- Review message, structure, paragraphs, and section functions before wording.
- Separate work mode from genre so an editorial is not treated as an empirical study.
- Add structural review and planning while preserving `full-review`, `section-review`,
  `targeted`, and `interactive` requests.
- Track support for substantial claims and distinguish verified evidence from
  unavailable sources or author decisions.
- Review supplied tables/figures with captions, notes, and surrounding prose;
  disclose text-only or inaccessible visual material.
- Add optional modules for review articles, reviewer responses, public communication,
  personal statements, grants, and academic recommendations.
- Replace mechanical style thresholds with contextual checks and protect necessary
  negatives, estimates, legitimate acronyms, and uncertainty.
- Document principle coverage and adversarial evaluation cases separately from
  observed behavioral results.

## Installation

Install the **whole folder**, not just `SKILL.md`: instructions load files from
`references/`. Keep the internal directory structure intact.

For a Codex environment that discovers local skills in `~/.codex/skills`, clone
this repository under the skill's name:

```bash
git clone https://github.com/gabrielguimaraessani/sciwrite.git ~/.codex/skills/manuscript-writing-review
```

For project-scoped Claude Code use, copy the folder into
`.claude/skills/manuscript-writing-review/` in the project. In another assistant,
use its supported instruction/reference mechanism and provide **all referenced
modules**. Do not assume a platform automatically loads sibling files from a
single pasted instruction. See [the usage guide](HOW-TO-USE.md).

## Example requests

```text
Use $manuscript-writing-review to review this Introduction for context,
knowledge gap, objective, and paragraph flow.
```

```text
Run a structural review before editing individual sentences.
```

```text
Review my Results without changing estimates, uncertainty, or causal meaning.
Check the supplied tables and captions against the prose.
```

```text
Help me outline this narrative review using only the notes and sources supplied.
```

```text
Prepare proposed point-by-point reviewer responses. Distinguish changes already
made from changes still planned.
```

## Review modes and legacy audits

| Mode | Use |
| --- | --- |
| `full-review` | Every applicable dimension of supplied material in one batch |
| `section-review` | One section and its purpose |
| `targeted` | A specified pass or editorial focus |
| `interactive` | One paragraph at a time, awaiting the user's response |
| `structural-review` | Argument, sections, and paragraph order before wording |
| `planning` | Supported outline and manageable writing steps |

The five legacy passes remain available by their names/numbers:
1. Clutter Extraction
2. Active Voice and Verb Vitality
3. Sentence Architecture
4. Keyword Consistency and Terminology
5. Numerical Consistency and Citation Integrity

Each substantive finding includes an identifiable location, original passage or
structural issue, concrete revision, rationale, and severity. Optional stylistic
preferences are not critical errors. A narrow request receives a proportionate answer.

## Scope and limitations

This is an editorial workflow, not automatic scientific validation, a plagiarism
detector, reference manager, or statistical analysis service. It can flag apparent
inconsistencies and missing reporting without deciding unsupported technical facts.
Citation support is verified only when a source is actually accessible and read.
Visual review requires accessible images and vision capabilities. Missing figures
do not prevent useful review of available prose.

Preserve warranted uncertainty and actual agency. Do not turn association into
causation, nonsignificance into equivalence, or proposed work into completed work.
Do not invent sources, approvals, analyses, personal stories, or letter endorsements.
Use the manuscript's language; English-specific conventions are not universal rules.

## Repository map and validation

- [SKILL.md](SKILL.md): concise operating protocol and routing.
- [Principles](references/principles.md): canonical P01–P44.
- [Coverage](docs/coverage.md): operational destinations and evaluation mapping.
- [Cases](evals/cases.md): readable scenario catalogue; [JSON](evals/cases.json)
  is the machine-readable source.
- [Evaluation results](docs/evaluation-results.md): checks actually run and limits.
- [Provenance](docs/provenance.md): upstream, influences, and changes.

Run structural validation with Python 3, without third-party dependencies:

```bash
python3 scripts/validate.py
```

This checks links, IDs, routing, metadata structure, coverage, and fixture integrity.
It does **not** prove a model will obey the skill. Evaluate behavior using raw tasks
without expected-answer leakage and retain outputs. Do not call the full suite
passed when only static validation or selected scenarios were run.

## Attribution and license

Original SciWrite: © 2026 Lorena A. Barba. This fork's extensions were prepared
for Gabriel Magalhães Nunes Guimarães, 2026. Preserve the upstream
[CC BY 4.0 license](LICENSE) and attribution. Changes include modular organization,
expanded editorial checks, contextual safeguards, and evaluation materials.

The modular workflow also draws conceptual inspiration from
[jingkarqi/writing-in-the-sciences-skill](https://github.com/jingkarqi/writing-in-the-sciences-skill).
No mirrored course notes or image collection from that project are bundled here.
See the provenance note for what was inspected and adapted. Neither project nor
this fork is an official Stanford/Coursera product or endorsement.
