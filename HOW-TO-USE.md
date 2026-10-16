# Using SciWrite

## Supply useful context, then proceed

Provide text or notes, genre, intended audience, target message, and known length
or journal requirements. Attach relevant tables, figures, captions, and sources.
Optional missing context should not block useful review. The assistant should
state assumptions and distinguish inaccessible material from reviewed material.

## Install the complete skill

Keep `SKILL.md`, `references/`, and `agents/` together. Use the installation in
[README.md](README.md). For a project installation, copy the folder to
`.claude/skills/manuscript-writing-review/` or the relevant environment's supported
skills location. Do not copy only `SKILL.md` or paste only its body into an
assistant that cannot retrieve its references. If using a project knowledge system,
upload the referenced modules too and ensure they can actually be read.

## Choose work mode independently of genre

Examples:

```text
Review the writing in my manuscript. Use full-review and give the results in one batch.
```

```text
Review only this Discussion: answer to the question, interpretation, limitations,
and supported implications.
```

```text
Run targeted Pass 2 on these paragraphs. Preserve external actors and necessary passives.
```

```text
Walk me through my Introduction paragraph by paragraph in interactive mode.
```

```text
Use structural-review for this narrative review. Propose a thematic organization.
```

```text
Use planning to organize my supplied study facts into an outline. List evidence gaps
separately; do not invent preliminary results.
```

A narrative review is a genre, not a work mode. A request can combine that genre
with targeted, structural, full, or interactive work. Protocols use planned-action
language; editorials do not need empirical Methods and Results.

## Understand the output

Broad reviews begin with scope and the identified message, then useful findings.
Each finding gives a real location, original text or specific structural issue,
concrete proposal, explanation, severity, and unresolved dependency where relevant.
Line numbers appear only when known. Identifying quoted openings can locate pasted
paragraphs. Unavailable sources and images are reported as unverified/not assessed.

Before applying an edit, verify it preserves your meaning. Tell the assistant when
a flagged technical noun or purposeful construction is appropriate. No revision
quota applies: a clear sentence may remain unchanged.

## Applying changes and reviewer replies

Ask explicitly to apply revisions to files if desired. A report alone should not
overwrite your manuscript. Structural changes can move or combine supplied text;
they must not manufacture data or fill scientific gaps with plausible facts.

For reviewer responses, supply comments and the revised manuscript or a clear list
of completed changes. If nothing has been changed, request proposed wording.
The assistant should not claim an analysis or edit has been completed merely
because a response sounds polished. Verify pagination before inserting locations.

## Other academic genres

Use optional modules for lay summaries, essays, personal statements, grants, and
recommendation letters. Supply actual evidence and examples. The skill must not
invent personal experiences, rank, program fit, approvals, or preliminary data.
Requested templates can have labeled fields; a purported final draft should put
missing inputs in a separate note rather than fake citations or unresolved markers.

## What is outside the automatic promise

- Technical peer review of scientific validity or statistical suitability.
- New analyses or independent systematic literature searches.
- Certification of originality, research ethics compliance, or image authenticity.
- Automatic bibliography-format compliance.
- Actual visual inspection when images or vision tools are unavailable.

These may require separate tasks, evidence, and tools. Editorial completeness
checks can still flag relevant questions without claiming those tasks were done.
