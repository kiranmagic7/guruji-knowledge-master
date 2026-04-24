# Contributing to Guruji Knowledge Master

## How to Add Content

### Step 1: Convert to Markdown
If source is .docx: `pandoc "file.docx" -t markdown --wrap=none -o "file.md"`

### Step 2: Add Frontmatter
Every .md file MUST start with YAML frontmatter. See STANDING-RULES.md for template.

### Step 3: Place in Correct Directory
- Blog posts → `blogs/`
- Interview transcripts → `talks-transcripts/`
- Website content → `website/[section]/`
- Research papers → `research/[domain]/[subdomain]/`
- Paper analyses → `papers/analyses/` or `papers/dt-papers/analysis/`
- Domain summaries → `domains/`
- Physiology reports → `physiology/reports/[report-name]/`

### Step 4: Update Indexes
After adding content, update:
- `_indexes/MASTER-INDEX.md` — add new concepts, cross-references
- `INDEX.md` — if new directory or major addition

### Step 5: Commit & Push
```bash
git add -A
git commit -m "[type]: [brief description]"
git push
```

## File Naming Conventions
- Blogs: `BLOG-[number]_[Title]_[YYYYMMDD].md`
- Interviews: `[Speaker]-[Q-count]-Interview-QA-[YYYYMMDD].md`
- Papers: `MKT-[number]-[brief-name].md`
- Analyses: `MKT-[number]-analysis.md`

## Quality Standards
- Verbatim quotes must be in blockquotes (>)
- Cross-reference related files
- Tag consistently
- No duplicate content
