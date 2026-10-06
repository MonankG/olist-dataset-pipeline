---
name: update-memory
description: Use this after finishing any task on the olist-dataset-pipeline project (a script written, a setup step completed, a bug fixed, a decision made) to record it in the memory skill. Keeps .agents/skills/memory/SKILL.md an accurate, up-to-date record of project progress.
---

# Update Memory

Run this immediately after completing a task on this project, before ending the turn.

## Steps
1. Open `.agents/skills/memory/SKILL.md`.
2. Add a new entry at the top of the **Progress log** section (newest first) with:
   - Date (use the actual current date)
   - One or two sentences on what was done
   - Files created/modified
   - Anything discovered or decided that changes prior assumptions (e.g. a step
     previously marked done turned out to be broken, or a plan changed)
3. If the task completed an item in **What's NOT done yet**, move it out of that list
   (or mark it done) and make sure the list still reflects the correct next step at
   the top.
4. If the task changed the **Environment setup status** (e.g. a new account, table,
   or bucket was created), update that section directly rather than only logging it.
5. Keep entries short — this file is a status record, not a full transcript. Don't
   paste code into it; reference file paths instead.
6. Do not create any other files for this update — only edit
   `.agents/skills/memory/SKILL.md`, per this project's AGENTS.md rule.
