# Proposal: split `ai` into `ai` + `aisafety`

**Status:** awaiting approval. Nothing in `tex-files/` has changed except the header website link, which was approved.

## Review files
- `build/preview/resume-ai-proposed.pdf`: applied AI / forward-deployed / infra variant (1 page)
- `build/preview/resume-aisafety-proposed.pdf`: safety / interpretability variant (1 page)
- `build/preview/ai-split.patch`: the full change set. Once approved, apply with `git apply build/preview/ai-split.patch`

## The two variants

| Tag | Targets | Emphasis | Section order |
|---|---|---|---|
| `ai` | Goodfire FDE / Platform, Anthropic Fellows (ML Systems), Baseten, Fireworks, Modal, Cognition, LangChain, Applied Intuition, Sierra, … | Shipping, customers, systems, AI tooling | Experience, Education, Skills, Projects (ARENA), AI Safety (compact) |
| `aisafety` | Anthropic Fellows (Safety), Goodfire Research Fellow, MATS, FAR.AI, Pivotal, Apollo, Transluce, AE Studio, Simplex | Mission, research, interpretability, community | Experience, **AI Safety (incl. ARENA)**, Education, Skills |

## Changes

### Applies to every role (the facts are new; recommended for all variants)
- ICE: "...volatility surface construction **across 4M+ instruments** using C++17"
- ICE: "Led AI best practices documentation for Curve Engine C++ development team to improve derivatives pricing software" becomes "Led AI-assisted development best practices (Claude Code, Copilot) for Curve Engine C++ derivatives pricing team"

### Both `ai` and `aisafety`
- New `tex-files/ai-safety.tex` section, `\input` from `main.tex` at a role-specific position
- 7 Chord: "Configured AI coding agent workflows (CLAUDE.md, rules, skills) and documented pipeline architecture for the CEO"
- UChicago: the coursework line is replaced by the "Concentrations: ... Machine Learning and AI" line. The Econ of TAI bullet moves into the new section.
- Dev tools line: "Claude Code, GitHub Copilot, git, CI/CD (GitHub Actions), Linux, bash/zsh, tmux"
- Dropped: C++ primer, Flask tool, CMake/GHA bullet, NAND2Tetris, ICE SDLC/QA bullet, Manteio project-management bullet, Minerva "Course projects:" label

### `ai` only
- Eve: "Unlocked $350M+ in signed sales **across 10+ multi-year customer campaigns** via Monte Carlo and sensitivity analyses"
- Keeps: ICE functional-tests bullet, Docker/Java bullet
- ARENA kept under Projects
- AI Safety section (2 lines): one XLab entry covering both fellowships (with cohort sizes) and the working group
- Dropped: Certifications, Minerva NER capstone

### `aisafety` only
- AI Safety section: XLab entry (two fellowship bullets), working group entry, ARENA entry
- Dropped: Certifications, ICE functional-tests bullet, Docker/Java bullet, Minerva NER capstone

### Build plumbing
- `Makefile` `ROLES` and the script's default `--roles` gain `aisafety`
- Several lines that used to be untagged are now wrapped in `\rolecontent{qr,qd,tech,soleng,de,ds}{...}`. Builds for `qr qd tech soleng de ds` were diffed before and after: the only text change is the two ICE bullets above.

## Please confirm
1. **Working group details:** title "Stipended Member", location "Chicago, IL" and start "Autumn 2026" are placeholders. Is it under XLab?
2. **$350M + 10+ customers (`ai`):** this bullet joins the two facts. Only keep it if the $350M came from those campaigns.
3. **"after completing the spring cohort":** this assumes Spring 2026.
4. **Left out for space:** the reading group (20+ members) and the blog-writing group (10+ members). Add them back when you present a paper or a post is published.

## Revisit when
- You present in the reading group: add a bullet to `aisafety`.
- The first State of AI Safety post or report is published (expected ~Nov 2026): add a link and an outcome.
- An interpretability project from `goodfire/PROJECT_IDEAS.md` has a repo: add a Projects entry and consider moving it above ARENA.
- The fellowships finish (end of Autumn 2026): add outcomes such as completion rate or fellows moving on to further programs.
- Fellowship/working-group content is reviewed against the Eve **Data Science Intern** block (NER, K-means), which is currently off both AI variants. Decide which is more relevant for `ai` as the fellowship content grows.
