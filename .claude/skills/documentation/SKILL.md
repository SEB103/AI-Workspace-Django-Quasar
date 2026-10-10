---
name: documentation
description: Write concise product and workspace docs based on verified implementation
---

# documentation

1. Identify audience and owning Git repo. Backend/API/install/deploy/release docs go under `project/docs` and project README; general Claude tools rules go in Workspace Git.
2. AI notes, prompts, transient screenshots and session summaries go to ignored `generated/reports/` **only when asked**.
3. Never document a planned or untested release as operational; show prerequisites and real commands from files.
4. Use meaningful headings, short clear Russian internal guides and English identifiers; end-user site content can be German.
5. For requested PDF/DOCX artifacts use the separately provided document production requirements and validate resulting files; don't silently convert an internal Markdown draft into a formal PDF.
