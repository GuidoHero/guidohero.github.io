# guidohero.github.io

Personal website of Guido A. Herrera-R, published at <https://guidohero.github.io>.
Any change pushed to the `gh-pages` branch goes live within a few minutes.

## Where things live

| What | Where | Notes |
|---|---|---|
| Publications | `_data/publications.yml` | One entry per paper, newest first; new papers are added automatically from ORCID (see below) |
| Publication PDFs | `papers/` | File name must match the entry's `pdf:` value |
| Photos | `images/` | Profile photo is `images/profile.jpg` |
| CV | `CV_GuidoA._Herrera-R.pdf` | Replace the file, keep the name |
| Appointment, education | `index.md` | Plain Markdown |
| Sidebar (interests, links) | `_layouts/default.html` | |
| Site title, tagline | `_config.yml` | |

## Adding a publication

Copy an entry in `_data/publications.yml`, paste it at the top, and edit it:

```yaml
- title: "Paper title (use *asterisks* for italics, e.g. species names)"
  authors: "Smith, J., Herrera-R, G.A., & Doe, A."
  year: 2026
  journal: "Journal Name"
  volume: "12"        # optional
  issue: "3"          # optional
  pages: "45–67"      # optional (or article number)
  doi: "10.xxxx/xxxxx" # optional, without https://doi.org/
  pdf: "Smith2026_JournalName.pdf"  # optional
```

`Herrera-R, G.A.` is bolded automatically (set by `scholar_name` in `_config.yml`).
Keep the quotes around text values.

## Adding a PDF

Upload the file to `papers/` with the exact name in the entry's `pdf:` field.
A **[PDF]** link appears next to that paper once the file is there; papers
without a file show no link.

Check the journal's self-archiving policy first: many publishers allow posting
the accepted manuscript but not the final typeset PDF. Open-access (CC BY)
articles can be posted freely.

## Changing the profile photo

Replace `images/profile.jpg`. Square-ish, about 400 px wide, keeps the page fast.

## Automatic updates from ORCID

Set your ORCID iD in `_config.yml` (`orcid: "0000-0000-0000-0000"`). Every
Monday the **Sync publications from ORCID** GitHub Action
(`.github/workflows/sync-publications.yml`) looks up the journal articles on
your ORCID record, fetches their details from Crossref, and adds any paper
that is not yet in `_data/publications.yml`. Run it any time from the
repository's **Actions** tab → *Sync publications from ORCID* → *Run workflow*.

- Existing entries are never changed, so edits you make by hand are kept.
- Papers without a DOI are skipped; add those by hand.
- Keep ORCID current by letting Crossref update it automatically:
  ORCID → *Works* → *Add* → *Search & link* → *Crossref Metadata Search*, and
  allow Crossref to auto-update your record.
- The sync script is `scripts/sync_orcid.py`
  (`python scripts/sync_orcid.py --dry-run` previews without saving).
