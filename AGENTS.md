# AGENTS.md 
This project will include 2 projects covering the areas from data engineering to data science. 

## General Working Rules
- When prompted to create script use simple, readable Python.
- Build on existing working code rather than replacing it unnecessarily.
- Avoid unnecessary functions, classes, abstractions, or production-style
programming structures.
- Do not perform analyses, diagnostics, transformations, or checks that were not
requested.

## Data instructions
- Never modify the raw data.

When creating a skill for this project, create only .agents/skills/<skill-name>/SKILL.md; do not create agents/openai.yaml or any other supporting files.

## Knowledge Generate Instructions
- Always generate knowledge in a precise and accurate manner, presented compactly — no filler, no repetition.
- Notes are for a student to actually learn from: they must be neat, intuitive, and readable in **one direction, top to bottom** — a learner should never have to jump back and forth to make sense of it.

### Note structure (follow this order)
1. **Title** — the topic name as a heading.
2. **Technical Definition** — precise, formal definition/information about the topic.
3. **In Simple Words** — an intuitive, plain-language explanation of the same idea.
4. **How It Works / Steps** — only when the topic involves a process, procedure, formula application, or algorithm. Use numbered steps, in the order they're actually performed.
5. **Diagram** — only when a visual would make the concept click faster than text (a process flow, a comparison, the shape of a distribution, a decision tree, etc.). Skip it when the topic is simple enough that a diagram would add clutter instead of clarity.
6. **Worked Example** — one concrete example applying the definition/steps.
7. **Key Takeaways** — optional, only for dense or multi-part topics: a short bullet summary at the end.

### Formatting rules
- Give every section its own heading — never run sections together as unbroken paragraphs.
- Use proper spacing between sections and between list items; avoid cramped walls of text.
- Numbered lists for sequential steps; bullet lists for non-sequential facts or properties.
- Bold key terms the first time they're introduced.
- The note should be skimmable start to finish without re-reading anything.

## Source File Notes Instructions
- Whenever I hand you a source file — a **PPT/PPTX**, **PDF**, or **DOC/DOCX** — treat it as raw source material to learn from, not something to copy or lightly reformat. These are typically dense, jargon-heavy, or confusingly worded (e.g., MS in CS coursework slides), so the job is to actually understand the content and rewrite it as a proper note.
- Read the whole source file before writing anything — don't generate notes from a partial skim.
- Regenerate the content fully following the **Knowledge Generate Instructions** above: same note structure (Title → Technical Definition → In Simple Words → Steps if applicable → Diagram if applicable → Worked Example → Key Takeaways) and the same formatting rules — regardless of how the source file itself is structured or worded.
- If the source covers multiple distinct topics, split them into separate notes rather than one long combined file, and track each one individually in `Knowledge-Map.md`.
- Example: when I give you PPTs for my **Natural Language Processing** coursework, put them in a `Natural Language Processing` folder and produce one clean, precise, student-readable note per topic, following the rules above — not a rehash of the slide text.
- After generating, follow the existing **Folder Generate**, **Skill Generation**, and **Memory Tracking** instructions as usual (permission before creating folders, `Topic-Name-Notes.docx` naming, run `update-memory`).

## Folder Generate Instructions
- You always have to generate folders categorizing the topics. Below is an example of it. 
- Always take permission before creating this folder. If approved, then only generate the foler.
    <Discussion/Chat about Area>/Topic/Topic-Name-Notes.docx