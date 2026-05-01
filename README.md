# Guruji Knowledge Master

**The authoritative knowledge base for Guruji Mahendra Trivedi's teachings, scientific research, and Divine Connection content — structured as a high-quality training dataset for AI agents and a working source of truth for human content creators.**

Merged from three repositories on 2026-04-24:
- `guruji-knowledge/` (local scaffold, built 2026-04-23)
- `guruji-science/` (GitHub: kiranmagic7/guruji-science)
- `divine-content/` (GitHub: kiranmagic7/divine-content)

---

## What This Repo Is

A single, machine-readable knowledge base that contains:
- **Primary teachings** — Guruji's own words, blessed material
- **Official content** — Alice/Dahryn-approved interviews, website, publications
- **Scientific research** — 10 domains, 676+ publications, paper analyses, critique playbook
- **Physiology reports** — Documentation of Guruji's extraordinary physiology
- **Website content** — Full Divine Connection website in markdown form
- **Blog posts, interviews, testimonials, religious text references**

Every file has YAML frontmatter (`content_type`, `authority_level`, `source`, `tags`), so any agent or pipeline can read, filter, embed, or retrieve it without guesswork.

---

## Who This Repo Serves

**AI agents** training on Guruji's corpus or retrieving it at runtime:
- Read `STANDING-RULES.md` before processing content
- Navigate via `INDEX.md` (root) and `_indexes/MASTER-INDEX.md`
- Use `_indexes/LAYMAN-EXAMPLES-INDEX.md` for analogies
- Every file is uniformly structured (frontmatter + clean markdown)

**Human content creators** (Kiran, Suhani, Shreyash, approved collaborators):
- Use `_templates/` for new content scaffolds
- Follow `CONTRIBUTING.md` for the add-content workflow
- All website copy lives under `website/` — never re-source from divineconnection.org

---

## Structure

```
guruji-knowledge-master/
├── INDEX.md                  # Root navigation (start here)
├── STANDING-RULES.md         # Language rules, authority, anti-hallucination
├── CONTRIBUTING.md           # How to add content
├── CHANGELOG.md              # Repo change history
├── README.md                 # This file
│
├── research/                 # All scientific research
│   ├── life-sciences/        # Agriculture, plant genetics, clinical trials
│   └── materials-science/    # Metals, ceramics, polymers, vitamins
├── domains/                  # 10 domain summaries
├── papers/                   # Paper analyses (MKT-193 through MKT-207)
│   ├── analyses/             # Individual paper analyses
│   └── dt-papers/            # DT paper analyses
├── physiology/               # Guruji's physiology research & reports
├── critique-playbook/        # How to critique/review scientific claims
│
├── website/                  # Divine Connection website (docx + markdown)
│   ├── about/                # About pages
│   ├── benefits/             # Benefits pages
│   ├── blog/                 # Blog posts (source collection)
│   ├── faq/                  # FAQ
│   ├── home/                 # Homepage
│   ├── meta/                 # Meta content, change logs
│   └── science/              # Science pages
│
├── articles/                 # Derivative layman explainers and integrated drafts
├── blogs/                    # Published blog posts (BLOG-1..15)
├── religious-texts/          # Scriptures, sacred writings
├── testimonials/             # Participant testimonials
├── talks-transcripts/        # Talks, interview Q&As
├── website-content/          # Legacy DC webpages as markdown
├── social-media/             # Social media content
│
├── _templates/               # YAML frontmatter templates (one per content type)
├── _indexes/                 # Cross-repo indexes
│   ├── MASTER-INDEX.md       # Concepts, themes, terminology
│   ├── LAYMAN-EXAMPLES-INDEX.md  # 95 analogies
│   └── science-index.md      # Scientific domain overview
└── _scripts/                 # Ingestion pipeline (ingest.py, watch.py)
```

---

## How to Use This Repo

### As an AI agent
1. Read `STANDING-RULES.md` (load once per session).
2. Start navigation at `INDEX.md`.
3. For concept / term lookups → `_indexes/MASTER-INDEX.md`.
4. For analogies when simplifying → `_indexes/LAYMAN-EXAMPLES-INDEX.md`.
5. For scientific claims → always trace back to the source paper in `papers/` or `research/`.
6. Respect authority hierarchy: `primary` > `official` > `derivative` > `draft`.

### As a human content creator
1. Find the most relevant template in `_templates/`.
2. Write the file with frontmatter + content.
3. Place it under the correct directory (see `CONTRIBUTING.md`).
4. Update indexes where applicable.
5. Commit and push.

---

## Authority Hierarchy (NON-NEGOTIABLE)

| Level | `authority_level` | Source |
|-------|------------------|--------|
| 1 | `primary` | Guruji direct (spoken, written, blessed) |
| 2 | `official` | Alice Ma'am / approved organization output |
| 3 | `derivative` | Papers, blogs, Grokipedia derived from 1/2 |
| 4 | `draft` | Work-in-progress, not yet approved |

Never let a `derivative` override a `primary`.

---

## Standing Rules (Quick Reference)

- **NO WEBSITE SOURCING**: Content comes from Guruji direct, Alice, or this repo. Never divineconnection.org.
- **MKT-164 MANGO**: No DNA polymorphism detected. Never claim genetic change for mango.
- **Guruji = "a being"** (never "a man").
- **"Science of Consciousness"** (never "Biofield Science").
- **6,000+ experiments**, **676 publications** (verify current count before citing).
- **The Trivedi Effect®** — use ® on first mention per file.

Full rules in `STANDING-RULES.md`.

---

## Ingestion Pipeline

```bash
# one-shot ingest to SQLite-vec
python3 _scripts/ingest.py

# watch mode (auto-ingest on file save)
python3 _scripts/watch.py
```

---

## Agents That Use This Repo

| Agent | Purpose |
|-------|---------|
| Kiran | Knowledge retrieval, paper analysis, content generation |
| Suhani | Paper summaries, PPTs, Grokipedia articles |

---

## Key Files to Know

| File | Purpose |
|------|---------|
| [`INDEX.md`](INDEX.md) | Root navigation |
| [`STANDING-RULES.md`](STANDING-RULES.md) | Non-negotiable rules |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to add content |
| [`CHANGELOG.md`](CHANGELOG.md) | Change history |
| [`_indexes/MASTER-INDEX.md`](_indexes/MASTER-INDEX.md) | Concept map |
| [`_indexes/LAYMAN-EXAMPLES-INDEX.md`](_indexes/LAYMAN-EXAMPLES-INDEX.md) | Analogies library |
| [`_indexes/science-index.md`](_indexes/science-index.md) | Science domain overview |

---

*This repo supersedes `guruji-science` and `divine-content` on GitHub.*
