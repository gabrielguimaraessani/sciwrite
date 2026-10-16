# Evaluation results — 2026-10-16

## What was exercised

Three fresh-context agents performed realistic tasks using SKILL.md and its
relevant references. They received only the raw task and artifact paths, without
expected answers, suspected bugs, or the implementation conversation. After
responding, they archived their exact outputs. The parent agent compared the
outputs with the specified safeguards. This is a small synthetic forward check,
not an independent benchmark or a statistical estimate of reliability.

| Task | Raw input | Observed output | Checked observations |
| --- | --- | --- | --- |
| Targeted scientific wording | [Input](../evals/observations/wording-input.txt) | [Output](../evals/observations/wording-output.md) | Retained may, estimated status, nonsignificance, and association; preserved external/unknown actors; accepted singular they; fixed parallelism and empty phrasing. |
| Batch manuscript excerpt review | [Input](../evals/observations/manuscript-input.txt) | [Output](../evals/observations/manuscript-output.md) | Detected causal overclaiming, missing objective, undefined group label, and citation/access limits; distinguished enrollment, inclusion, and subgroup denominators; gave concrete structural proposals in one batch. |
| Proposed reviewer response | [Input](../evals/observations/reviewer-input.txt) | [Output](../evals/observations/reviewer-output.md) | Labeled responses proposed; did not claim an unperformed sensitivity analysis or completed edits; left page/line locations unresolved rather than inventing them. |

No failure of the listed safeguards was observed in these outputs. The manuscript
task appropriately treated 120 enrolled versus 102 included as a reconciliation
question, not an automatic numerical error, and did not add a subgroup N=50 to
the cohort total. It did not claim to inspect the unavailable figure or source.

## What was not exercised behaviorally

The full catalogue of 59 individual scenarios was not run as an automated suite.
The three composite tasks exercise a subset of its concerns; they do not establish
behavioral coverage of all 44 principles. Interactive turn boundaries, visual
inspection of actual images, historical-note instruction conflicts, grants,
recommendation letters, and broad-audience numerical explanation were not all
independently forward-tested. No real literature search, statistical analysis,
clinical evaluation, or plagiarism assessment was performed.

## Static checks

The repository validator checks the restricted metadata schemas, routed modules,
44 unique principle IDs, 44 coverage rows, mapped case references, sequential
fixture IDs, local Markdown links/anchors, balanced code fences, and the unchanged
upstream license. Its self-test checks detection of broken references, duplicate
principles, invalid fixture mappings, and a removed legacy mode. These are
structural checks only. The skill-creator quick validator separately checks YAML
frontmatter and the skill name/description. See execution status below.

Execution status: `python3 scripts/validate.py --self-test` completed successfully
on 2026-10-16, including all four negative mutation checks. The skill-creator
`quick_validate.py` also reported `Skill is valid!`. These results do not imply
that the 59 behavioral scenarios were run or all model behaviors were validated.
