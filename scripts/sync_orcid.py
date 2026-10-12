"""Keep the publication data files up to date.

1. _data/submitted.yml (preprints, papers in review or accepted): any entry
   that has a `doi:` but no `title:` is filled in from Crossref, so adding a
   preprint only takes its DOI.
2. _data/publications.yml: new papers on the ORCID record are added.

Reads the ORCID iD from _config.yml (`orcid:`), lists the works on that
ORCID record, and fills in authors, volume and pages from Crossref.
Only papers whose DOI (or title) is not already in the data file are
added; existing entries are never changed, so manual edits are safe.
ORCID works without a DOI are skipped (they have no reliable author list).

Usage: python scripts/sync_orcid.py [--dry-run]
"""

import html
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "_config.yml"
DATA = ROOT / "_data" / "publications.yml"
SUBMITTED = ROOT / "_data" / "submitted.yml"

# ORCID work types to import. Add "preprint" etc. to include more.
INCLUDE_TYPES = {"journal-article"}
MAX_AUTHORS = 20  # longer author lists are cut to the first 19 + "et al."
USER_AGENT = "guidohero.github.io publication sync (mailto:gah234@cornell.edu)"
SMALL_WORDS = {"of", "and", "the", "in", "for", "on", "a", "an", "&", "to"}


def get_json(url, accept="application/json"):
    req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_orcid_works(orcid):
    """Return [{doi, title, year, journal}] for the ORCID record."""
    data = get_json(f"https://pub.orcid.org/v3.0/{orcid}/works")
    works = []
    for group in data.get("group", []):
        summary = group["work-summary"][0]  # ORCID's preferred version
        if summary.get("type") not in INCLUDE_TYPES:
            continue
        doi = None
        for ext in (summary.get("external-ids") or {}).get("external-id", []):
            if ext.get("external-id-type") == "doi":
                doi = normalize_doi(ext.get("external-id-value", ""))
                break
        date = summary.get("publication-date") or {}
        works.append({
            "doi": doi,
            "title": ((summary.get("title") or {}).get("title") or {}).get("value"),
            "year": int((date.get("year") or {}).get("value") or 0) or None,
            "journal": (summary.get("journal-title") or {}).get("value"),
        })
    return works


def fetch_crossref(doi):
    try:
        return get_json("https://api.crossref.org/works/" + urllib.parse.quote(doi))["message"]
    except Exception as exc:  # network error or DOI not in Crossref
        print(f"  Crossref lookup failed for {doi}: {exc}", file=sys.stderr)
        return None


def normalize_doi(doi):
    doi = doi.strip().lower()
    return re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", doi)


def normalize_title(title):
    title = re.sub(r"<[^>]+>|\*", "", title or "")
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def clean_title(title):
    """Crossref titles may contain HTML: keep italics as Markdown, drop the rest."""
    title = re.sub(r"</?(i|em)>", "*", title)
    title = re.sub(r"<[^>]+>", "", title)
    title = html.unescape(re.sub(r"\s+", " ", title)).strip()
    return title.rstrip(".")


def initials(given):
    parts = re.split(r"[\s.]+", given.strip())
    out = []
    for part in filter(None, parts):
        # Keep hyphenated initials, e.g. Jean-Claude -> J.-C.
        out.append("-".join(p[0].upper() + "." for p in part.split("-") if p))
    return "".join(out)


def format_author(author, me):
    family = (author.get("family") or author.get("name") or "").replace("‐", "-").strip()
    given = author.get("given") or ""
    name = f"{family}, {initials(given)}" if given else family
    # Show this site's owner exactly as written in _config.yml so it gets bolded.
    me_family = me.split(",")[0].strip()
    if family.lower() in {me_family.lower(), "herrera-rodriguez", "herrera rodríguez", "herrera-rodríguez"} \
            and given[:1].upper() == me.split(",")[1].strip()[:1].upper():
        return me
    return name


def format_authors(authors, me):
    names = [format_author(a, me) for a in authors if a.get("family") or a.get("name")]
    if len(names) > MAX_AUTHORS:
        names = names[:MAX_AUTHORS - 1]
        if me not in names:
            names.append(me)
        return ", ".join(names) + ", et al."
    if len(names) > 1:
        return ", ".join(names[:-1]) + ", & " + names[-1]
    return names[0] if names else ""


def pdf_name(authors_text, year, journal):
    first = re.sub(r"[^A-Za-z]", "", authors_text.split(",")[0]) or "Paper"
    words = [w for w in re.findall(r"[A-Za-z]+", journal or "") if w.lower() not in SMALL_WORDS]
    abbrev = "".join(w[:4].capitalize() for w in words)[:30] or "Article"
    return f"{first}{year or ''}_{abbrev}.pdf"


def crossref_fields(msg, me):
    """Citation fields from a Crossref record (journal article or preprint)."""
    parts = (msg.get("issued") or msg.get("published") or {}).get("date-parts", [[None]])[0]
    venue = ((msg.get("container-title") or [None])[0]
             or ((msg.get("institution") or [{}])[0]).get("name")
             or msg.get("group-title") or msg.get("publisher") or "")
    entry = {
        "title": clean_title((msg.get("title") or [""])[0]),
        "authors": format_authors(msg.get("author", []), me),
        "year": parts[0],
        "journal": html.unescape(venue),
    }
    for key, value in (("volume", msg.get("volume")), ("issue", msg.get("issue")),
                       ("pages", msg.get("page") or msg.get("article-number"))):
        if value:
            entry[key] = str(value).replace("-", "–")
    return entry


def build_entry(work, me):
    """Build a data-file entry from Crossref, or None if Crossref has no record."""
    msg = fetch_crossref(work["doi"])
    if not msg:
        return None
    entry = crossref_fields(msg, me)
    entry["title"] = entry["title"] or clean_title(work["title"] or "")
    entry["year"] = entry["year"] or work["year"]
    entry["journal"] = entry["journal"] or work["journal"] or ""
    entry["doi"] = work["doi"]
    entry["pdf"] = pdf_name(entry["authors"], entry["year"], entry["journal"])
    return entry


def fill_submitted(me, dry_run):
    """Fill in entries of _data/submitted.yml that only have a DOI."""
    if not SUBMITTED.exists():
        return
    header, blocks = split_entries(SUBMITTED.read_text())
    changed = 0
    for i, block in enumerate(blocks):
        given = yaml.safe_load(block)[0]
        if given.get("title") or not given.get("doi"):
            continue
        doi = normalize_doi(given["doi"])
        msg = fetch_crossref(doi)
        if not msg:
            print(f"Submitted: {doi} not found in Crossref, will retry next run")
            continue
        entry = crossref_fields(msg, me)
        if msg.get("type") == "posted-content":
            entry["status"] = "Preprint"
        entry.update({k: v for k, v in given.items() if v not in (None, "")})  # your values win
        entry["doi"] = doi
        blocks[i] = entry_to_yaml(entry) + "\n"
        changed += 1
        print(f"Submitted: filled in {entry['title']} ({doi})")
    if changed:
        output = header + "".join(blocks)
        yaml.safe_load(output)
        print(output) if dry_run else SUBMITTED.write_text(output)


def entry_to_yaml(entry):
    lines = []
    for i, (key, value) in enumerate(entry.items()):
        prefix = "- " if i == 0 else "  "
        if key == "year" and value:
            lines.append(f"{prefix}{key}: {value}")
        else:
            lines.append(f"{prefix}{key}: {json.dumps(str(value), ensure_ascii=False)}")
    return "\n".join(lines) + "\n"


def split_entries(text):
    """Split the data file into (header, [entry_text, ...]) without reformatting it."""
    starts = [m.start() for m in re.finditer(r"^- ", text, re.M)]
    if not starts:
        return text, []
    header = text[:starts[0]]
    bounds = starts + [len(text)]
    return header, [text[bounds[i]:bounds[i + 1]] for i in range(len(starts))]


def main(argv):
    dry_run = "--dry-run" in argv
    config = yaml.safe_load(CONFIG.read_text())
    me = config.get("scholar_name") or "Herrera-R, G.A."
    fill_submitted(me, dry_run)

    orcid = (config.get("orcid") or "").strip()
    if not re.fullmatch(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]", orcid):
        print("No valid `orcid:` set in _config.yml; skipping ORCID.")
        return 0

    text = DATA.read_text()
    header, blocks = split_entries(text)
    existing = [yaml.safe_load(b)[0] for b in blocks]
    known_dois = {normalize_doi(e.get("doi") or "") for e in existing} - {""}
    known_titles = {normalize_title(e.get("title")) for e in existing}

    new = []
    for work in fetch_orcid_works(orcid):
        if work["doi"] in known_dois or normalize_title(work["title"]) in known_titles:
            continue
        if not work["doi"]:
            # Without a DOI there is no reliable author list; add these by hand.
            print(f"Skipped (no DOI): {work['title']}")
            continue
        entry = build_entry(work, me)
        if entry is None:
            print(f"Skipped (not found in Crossref, will retry next run): {work['title']}")
            continue
        if normalize_title(entry["title"]) in known_titles:
            continue
        print(f"New: {entry['title']} ({entry['doi']})")
        known_titles.add(normalize_title(entry["title"]))
        known_dois.add(work["doi"])
        new.append(entry)

    if not new:
        print("Publication list is up to date.")
        return 0

    # Insert each new paper above the first existing paper from the same or an earlier year.
    for entry in sorted(new, key=lambda e: e["year"] or 0):
        pos = next((i for i, e in enumerate(existing) if (e.get("year") or 0) <= (entry["year"] or 0)),
                   len(existing))
        blocks.insert(pos, entry_to_yaml(entry) + "\n")
        existing.insert(pos, entry)
    if blocks and not blocks[-1].endswith("\n"):
        blocks[-1] += "\n"

    output = header + "".join(blocks)
    yaml.safe_load(output)  # refuse to write a file that no longer parses
    if dry_run:
        print(output)
    else:
        DATA.write_text(output)
    print(f"Added {len(new)} publication(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
