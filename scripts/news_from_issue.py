"""Turn a "Post news" issue (see .github/ISSUE_TEMPLATE/news.yml) into a news item.

Reads the issue body from the ISSUE_BODY environment variable, downloads and
resizes the photo (if any) into images/news/, and adds the item to the top of
_data/news.yml. Run by .github/workflows/news-from-issue.yml.
"""

import datetime
import io
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

import yaml
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
NEWS = ROOT / "_data" / "news.yml"
IMAGES = ROOT / "images" / "news"
MAX_SIZE = (1200, 1200)
NO_RESPONSE = "_No response_"


def parse_sections(body):
    """Issue forms render as '### Label' headings followed by the answer."""
    sections, current = {}, None
    for line in body.replace("\r\n", "\n").split("\n"):
        heading = re.match(r"^###\s+(.*)$", line)
        if heading:
            current = heading.group(1).strip()
            sections[current] = []
        elif current:
            sections[current].append(line)
    out = {}
    for label, lines in sections.items():
        value = "\n".join(lines).strip()
        out[label] = "" if value == NO_RESPONSE else value
    return out


def one_line(text):
    return re.sub(r"\s*\n\s*", " ", text).strip()


def slugify(text, length=40):
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # keep link text only
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:length].rstrip("-") or "news"


def download_photo(field, token, stem):
    match = re.search(r"https://[^\s)\"'>]+", field or "")
    if not match:
        return None
    req = urllib.request.Request(match.group(0), headers={"User-Agent": "news-from-issue"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    img = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB")
    img.thumbnail(MAX_SIZE)
    IMAGES.mkdir(parents=True, exist_ok=True)
    path = IMAGES / f"{stem}.jpg"
    n = 2
    while path.exists():
        path = IMAGES / f"{stem}-{n}.jpg"
        n += 1
    img.save(path, "JPEG", quality=82, optimize=True, progressive=True)
    return path.relative_to(ROOT).as_posix()


def main():
    fields = parse_sections(os.environ["ISSUE_BODY"])
    text = one_line(fields.get("News (English)", ""))
    if not text:
        sys.exit("The English news text is empty.")
    date = fields.get("Date", "").strip() or datetime.date.today().strftime("%Y-%m")
    if not re.fullmatch(r"\d{4}(-\d{2}){0,2}", date):
        sys.exit(f"Date must look like 2026-10 (got {date!r}).")

    item = {"date": date[:7], "text": text}
    text_es = one_line(fields.get("News (Spanish, optional)", ""))
    if text_es:
        item["text_es"] = text_es
    photo = download_photo(fields.get("Photo (optional)", ""), os.environ.get("GITHUB_TOKEN"),
                           f"{date[:7]}-{slugify(text)}")
    if photo:
        item["image"] = photo
        alt = one_line(fields.get("Photo description (optional)", ""))
        if alt:
            item["image_alt"] = alt

    block = "\n".join(
        ("- " if i == 0 else "  ") + f"{k}: {json.dumps(v, ensure_ascii=False)}"
        for i, (k, v) in enumerate(item.items())
    ) + "\n\n"
    current = NEWS.read_text()
    first = re.search(r"^- ", current, re.M)
    pos = first.start() if first else len(current)
    output = current[:pos] + block + current[pos:]
    yaml.safe_load(output)  # refuse to write a broken file
    NEWS.write_text(output)
    print(f"Added news item dated {item['date']}" + (f" with photo {photo}" if photo else ""))


if __name__ == "__main__":
    main()
