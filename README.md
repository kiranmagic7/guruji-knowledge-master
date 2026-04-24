# Guruji Knowledge Master

**Single source of truth for everything touching Guruji's mission.**

Merged from three repositories on 2026-04-24:
- `guruji-knowledge/` (local scaffold, built 2026-04-23)
- `guruji-science/` (GitHub: kiranmagic7/guruji-science)
- `divine-content/` (GitHub: kiranmagic7/divine-content)

---

## Structure

```
guruji-knowledge-master/
├── research/                 # All scientific research
│   ├── life-sciences/        # Agriculture, plant genetics, clinical trials, etc.
│   └── materials-science/    # Metals, ceramics, polymers, vitamins, etc.
├── domains/                  # Domain summaries (consciousness, genetics, etc.)
├── papers/                   # Paper analyses (MKT-193 through MKT-207)
│   ├── analyses/             # Individual paper analyses
│   └── dt-papers/            # DT paper analyses
├── physiology/               # Guruji's physiology research & reports
├── critique-playbook/        # How to critique/review scientific claims
├── website/                  # Divine Connection website content (docx/markdown)
├── blogs/                    # Blog posts
├── religious-texts/          # Scriptures, sacred writings
├── testimonials/             # 4,481+ testimonials
├── talks-transcripts/        # Guruji's talks, video/audio transcripts
├── website-content/          # DC webpages as markdown
├── social-media/             # Social media content
├── _templates/               # YAML frontmatter templates (6 content types)
├── _indexes/                 # Auto-generated per-topic index pages
├── _scripts/                 # Ingestion pipeline (ingest.py, watch.py)
└── science-index.md          # Original guruji-science index
```

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

## Standing Rules

- **NO WEBSITE SOURCING**: Content comes from Guruji direct, Alice, or this repo. Never divineconnection.org.
- **MKT-164 MANGO**: No DNA polymorphism detected. Never claim genetic change for mango.
- **Guruji = "a being"** (never "a man").
- **"Science of Consciousness"** (never "Biofield Science").
- **6,000+ experiments**, **676 publications**.

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

*This repo supersedes `guruji-science` and `divine-content` on GitHub.*
