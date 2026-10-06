---
name: knowledge-base
description: Interview-prep note system for the olist-dataset-pipeline project. Points to where topic notes live and how they're organized. Read this to find or review a topic before an interview.
---

# Knowledge Base

Since this project is built learn-as-you-go, every new tool/technology/concept
encountered gets written up as a proper student note for later interview review.
This file is the map to that system; the `update-knowledge-base` skill is what
actually generates/updates notes, following the format and rules defined in this
project's `AGENTS.md` (see **Knowledge Generate Instructions**, **Source File Notes
Instructions**, and **Folder Generate Instructions**).

## Where notes live
All notes live under `notes/` at the project root, organized as:

```
notes/
  Knowledge-Map.md          <- index of every note, kept up to date
  <Area>/
    <Topic>/
      <Topic-Name>-Notes.docx
```

- `<Area>` is the broader subject/context the topic came from (e.g. `Data
  Engineering`, `AWS`, `dbt`, or a coursework subject name like `Natural Language
  Processing` when notes come from a handed-in source file).
- `<Topic>` is the specific concept (e.g. `Star Schema`, `IAM Policies`, `DAGs`).
- The note itself is a `.docx` file named `Topic-Name-Notes.docx`, generated via the
  docx skill, following the note structure in AGENTS.md (Title, Technical Definition,
  In Simple Words, How It Works/Steps if applicable, Diagram if applicable, Worked
  Example, Key Takeaways if dense).

## Knowledge-Map.md
`notes/Knowledge-Map.md` is the index — one row per note, with Area, Topic, file
link, and date added. Always check it first to see whether a topic already has a
note before creating a new one.

## Creating new folders
Per AGENTS.md, always ask permission before creating a new `<Area>` or `<Topic>`
folder under `notes/`. Never create one silently.
