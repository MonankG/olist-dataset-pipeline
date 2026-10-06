---
name: update-knowledge-base
description: Use this whenever a new tool, technology, or concept is introduced, explained, or used for the first time on the olist-dataset-pipeline project, or when the user hands over a source file (PPT/PDF/DOC) to learn from. Generates/updates a proper student note under notes/ and keeps Knowledge-Map.md current.
---

# Update Knowledge Base

Run this whenever a new concept/tool is explained or used for the first time in
this project, or when the user hands over a source file to turn into notes.

## Steps

1. **Check for an existing note.** Look in `notes/Knowledge-Map.md` for the topic.
   If it already exists, extend the existing `.docx` note instead of creating a
   duplicate.

2. **Determine Area/Topic placement.**
   - For a concept introduced organically while building the pipeline, pick the
     Area folder that fits (e.g. `Data Engineering`, `AWS`, `dbt`, `Airflow`).
   - For a handed-over source file (PPT/PDF/DOC), read the **whole** file first —
     never generate from a partial skim. If it covers multiple distinct topics,
     split into separate notes, one per topic, all under the same Area folder
     named after the source's subject (e.g. `Natural Language Processing`).

3. **Ask permission before creating any new folder** under `notes/` (a new Area or
   Topic folder) — per AGENTS.md, never create one silently. Confirm folder path
   before writing the note into it.

4. **Write the note**, following AGENTS.md's Knowledge Generate Instructions
   exactly, regardless of how source material was structured:
   - **Title** — the topic name as a heading.
   - **Technical Definition** — precise, formal definition.
   - **In Simple Words** — intuitive, plain-language version of the same idea.
   - **How It Works / Steps** — only if the topic is a process/procedure/algorithm;
     numbered, in actual execution order.
   - **Diagram** — only if a visual would genuinely speed up understanding; skip
     for simple topics.
   - **Worked Example** — one concrete example applying the definition/steps.
   - **Key Takeaways** — optional, only for dense/multi-part topics.
   - Formatting: separate heading per section (never run sections together), proper
     spacing, numbered lists for sequential steps / bullets for non-sequential
     facts, bold key terms on first use, skimmable top-to-bottom without
     backtracking.
   - Tie the explanation back to this project specifically where it applies (e.g.
     not generic "what is a star schema" but why `fact_orders` + the dim tables
     are shaped that way here).
   - Generate the file via the `docx` skill as `Topic-Name-Notes.docx` at
     `notes/<Area>/<Topic>/`.

5. **Update `notes/Knowledge-Map.md`** — add/update the row for this note (Area,
   Topic, file link, date).

6. **Run the `update-memory` skill** afterward to log that this note was created,
   per this project's existing workflow.

7. Do not create any other supporting files beyond the note `.docx` and the
   `Knowledge-Map.md` update — no extra scaffolding, per this project's AGENTS.md
   rule on skills and minimal structure.
