#!/usr/bin/env python3
"""Import a Medium post into data/content.json as a blog article."""

from __future__ import annotations

import argparse
import json
import re
import ssl
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "data" / "content.json"
DATA_DIR = ROOT / "data"
IMAGES_ROOT = ROOT / "public" / "images" / "blog"


def slugify_filename(medium_id: str) -> str:
    base = re.sub(r"[^A-Za-z0-9._-]+", "-", medium_id).strip("-")
    if "." not in base:
        base += ".png"
    return base.lower()


def fetch_medium_json(url: str, cache_path: Path) -> dict:
    if "?format=json" not in url:
        url = url.rstrip("/") + "?format=json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
            raw = resp.read().decode("utf-8")
        raw = re.sub(r"^\]\)\}while\(1\);\s*", "", raw)
        payload = json.loads(raw)
        cache_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return payload["payload"]["value"]
    except Exception:
        for candidate in (cache_path, cache_path.with_name(
            re.sub(r"-[a-f0-9]{6,}$", "", cache_path.stem) + ".json"
        )):
            if candidate.exists():
                return json.loads(candidate.read_text(encoding="utf-8"))["payload"]["value"]
        raise


def build_image_map(post: dict, slug: str) -> dict[str, tuple[str, int, int]]:
    image_map: dict[str, tuple[str, int, int]] = {}
    for p in post["content"]["bodyModel"]["paragraphs"]:
        if p.get("type") != 4:
            continue
        meta = p.get("metadata", {})
        img_id = meta.get("id")
        if not img_id or img_id in image_map:
            continue
        filename = slugify_filename(img_id)
        image_map[img_id] = (
            f"/images/blog/{slug}/{filename}",
            int(meta.get("originalWidth") or 1400),
            int(meta.get("originalHeight") or 900),
        )
    return image_map


def download_images(image_map: dict[str, tuple[str, int, int]], slug: str) -> None:
    out_dir = IMAGES_ROOT / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    ctx = ssl.create_default_context()
    for medium_id, (src, _w, _h) in image_map.items():
        filename = Path(src).name
        dest = out_dir / filename
        if dest.exists() and dest.stat().st_size > 1000:
            continue
        enc = urllib.parse.quote(medium_id, safe="")
        url = f"https://miro.medium.com/max/1400/{enc}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
            dest.write_bytes(resp.read())


NUMBERED_TITLE_RE = re.compile(r"^([\u200b\s]*)(\d+\.\s+)([^\n]+)(\n?)")


def markups_for_range(markups: list, start: int, end: int) -> list:
    adjusted = []
    for m in markups:
        if m["start"] >= end or m["end"] <= start:
            continue
        adjusted.append({
            **m,
            "start": max(0, m["start"] - start),
            "end": min(end, m["end"]) - start,
        })
    return adjusted


def apply_markups(text: str, markups: list) -> str:
    if not markups:
        return text
    parts: list[tuple[int, int, str, str]] = []
    for m in sorted(markups, key=lambda x: x["start"]):
        start, end = m["start"], m["end"]
        if m["type"] == 1:
            parts.append((start, end, "strong", ""))
        elif m["type"] == 2:
            parts.append((start, end, "em", ""))
        elif m["type"] == 3:
            href = m.get("href", "")
            parts.append((start, end, "a", href))
    out = []
    pos = 0
    for start, end, tag, href in parts:
        out.append(text[pos:start])
        chunk = text[start:end]
        if tag == "a":
            out.append(f'<a href="{href}">{chunk}</a>')
        else:
            out.append(f"<{tag}>{chunk}</{tag}>")
        pos = end
    out.append(text[pos:])
    return "".join(out)


def image_block(src: str, width: int, height: int, alt: str = "", caption: str = "") -> str:
    ratio = (height / width) * 100 if width else 56.25
    cap = ""
    if caption:
        cap = (
            '<figcaption data-sqsp-image-classic-block-caption-container '
            'class="image-caption-wrapper"><div class="image-caption">'
            f'<p class="">{caption}</p></div></figcaption>'
        )
    return f"""
<div class="sqs-block image-block sqs-block-image" data-block-type="5" data-sqsp-block="image-classic">
  <div class="sqs-block-content">
    <div class="image-block-outer-wrapper layout-caption-below design-layout-inline">
      <figure class="sqs-block-image-figure intrinsic" style="max-width:{width}px;">
        <div class="image-block-wrapper" data-animation-role="image">
          <div class="sqs-image-shape-container-element has-aspect-ratio"
            style="position:relative;padding-bottom:{ratio:.5f}%;overflow:hidden;">
            <img src="{src}" alt="{alt}" width="{width}" height="{height}" loading="lazy" decoding="async"
              sizes="(max-width: 640px) 100vw, (max-width: 767px) 100vw, 100vw"
              style="display:block;object-fit:cover;width:100%;height:100%;object-position:50% 50%" />
          </div>
        </div>
        {cap}
      </figure>
    </div>
  </div>
</div>"""


def text_block(html: str) -> str:
    return f"""
<div class="sqs-block html-block sqs-block-html" data-block-type="2" data-sqsp-block="text">
  <div class="sqs-block-content">
    <div class="sqs-html-content" data-sqsp-text-block-content>{html}</div>
  </div>
</div>"""


def blockquote_inline(p: dict) -> str:
    inner = apply_markups(p.get("text", ""), p.get("markups", []))
    return f'<blockquote><p class="" style="white-space:pre-wrap;">{inner}</p></blockquote>'


def list_item_inline(p: dict) -> str:
    inner = apply_markups(p.get("text", ""), p.get("markups", []))
    return f'<li><p class="" style="white-space:pre-wrap;">{inner}</p></li>'


def paragraph_inline(p: dict) -> str:
    text = p.get("text", "")
    markups = p.get("markups", [])
    match = NUMBERED_TITLE_RE.match(text)
    if match:
        title_text = match.group(1) + match.group(2) + match.group(3)
        title_len = len(title_text)
        newline = match.group(4)
        body_start = match.end()
        body_text = text[body_start:]
        title_html = (
            f"<strong>{apply_markups(title_text, markups_for_range(markups, 0, title_len))}</strong>"
        )
        body_html = apply_markups(body_text, markups_for_range(markups, body_start, len(text)))
        inner = f"{title_html}{newline}{body_html}"
    else:
        inner = apply_markups(text, markups)
    return f'<p class="" style="white-space:pre-wrap;">{inner}</p>'


def subtitle_html(text: str) -> str:
    return f'<p class="post-subtitle" style="white-space:pre-wrap;"><strong>{text}</strong></p>'


def is_post_subtitle(text: str, post_subtitle: str) -> bool:
    if not post_subtitle:
        return False
    normalized = lambda value: value.strip().rstrip(".")
    return normalized(text) == normalized(post_subtitle)


def heading_html(ptype: int, text: str) -> str:
    """Map Medium headings to Squarespace h1/h2 hierarchy."""
    if ptype == 13 or (ptype == 3 and re.match(r"^\d+\.\s", text.strip())):
        tag = "h2"
    else:
        tag = "h1"
    return f'<{tag} style="white-space:pre-wrap;"><strong>{text}</strong></{tag}>'


def should_skip_paragraph(p: dict, post_title: str, hero_id: str) -> bool:
    if p["type"] == 3 and p.get("text") == post_title:
        return True
    if p["type"] == 4 and p.get("metadata", {}).get("id") == hero_id:
        return True
    return False


def paragraph_html(
    p: dict,
    image_map: dict[str, tuple[str, int, int]],
    post_subtitle: str = "",
) -> str | None:
    ptype = p["type"]
    text = p.get("text", "")

    if ptype == 4:
        meta = p.get("metadata", {})
        img_id = meta.get("id", "")
        if img_id not in image_map:
            return None
        src, w, h = image_map[img_id]
        return image_block(src, w, h, caption=text)
    if ptype == 13 and is_post_subtitle(text, post_subtitle):
        return text_block(subtitle_html(text))
    if ptype in (3, 13):
        return text_block(heading_html(ptype, text))
    if ptype in (6, 7):
        return text_block(blockquote_inline(p))
    if ptype == 9:
        return text_block(f'<ul data-rte-list="default">{list_item_inline(p)}</ul>')
    if ptype == 10:
        return text_block(f'<ol data-rte-list="default">{list_item_inline(p)}</ol>')
    if ptype == 1:
        return text_block(paragraph_inline(p))
    return None


def build_content(
    post: dict,
    slug: str,
    full_slug: str,
    image_map: dict[str, tuple[str, int, int]],
) -> str:
    paragraphs = post["content"]["bodyModel"]["paragraphs"]
    title = post["title"]
    post_subtitle = post.get("content", {}).get("subtitle", "")
    hero = next((p for p in paragraphs if p.get("type") == 4), paragraphs[0])
    hero_id = hero.get("metadata", {}).get("id", "")
    hero_src, hero_w, hero_h = image_map[hero_id]
    hero_ratio = (hero_h / hero_w) * 100 if hero_w else 56.25

    body_blocks = []
    i = 0
    while i < len(paragraphs):
        p = paragraphs[i]
        if should_skip_paragraph(p, title, hero_id):
            i += 1
            continue

        if p["type"] == 1:
            paras = []
            while i < len(paragraphs) and paragraphs[i]["type"] == 1:
                if should_skip_paragraph(paragraphs[i], title, hero_id):
                    break
                paras.append(paragraph_inline(paragraphs[i]))
                i += 1
            if paras:
                body_blocks.append(text_block("".join(paras)).strip())
            continue

        if p["type"] in (6, 7):
            quotes = []
            while i < len(paragraphs) and paragraphs[i]["type"] in (6, 7):
                if should_skip_paragraph(paragraphs[i], title, hero_id):
                    break
                quotes.append(blockquote_inline(paragraphs[i]))
                i += 1
            body_blocks.append(text_block("".join(quotes)).strip())
            continue

        if p["type"] == 9:
            items = []
            while i < len(paragraphs) and paragraphs[i]["type"] == 9:
                if should_skip_paragraph(paragraphs[i], title, hero_id):
                    break
                items.append(list_item_inline(paragraphs[i]))
                i += 1
            body_blocks.append(
                text_block(f'<ul data-rte-list="default">{"".join(items)}</ul>').strip()
            )
            continue

        if p["type"] == 10:
            items = []
            while i < len(paragraphs) and paragraphs[i]["type"] == 10:
                if should_skip_paragraph(paragraphs[i], title, hero_id):
                    break
                items.append(list_item_inline(paragraphs[i]))
                i += 1
            body_blocks.append(
                text_block(f'<ol data-rte-list="default">{"".join(items)}</ol>').strip()
            )
            continue

        block = paragraph_html(p, image_map, post_subtitle)
        if block:
            body_blocks.append(block.strip())
        i += 1

    published_ms = post.get("latestPublishedAt") or post.get("firstPublishedAt")
    published = datetime.fromtimestamp(published_ms / 1000, tz=timezone.utc)
    date_iso = published.strftime("%Y-%m-%d")
    date_display = published.strftime("%B %d, %Y")
    body = "\n".join(body_blocks)

    return f"""<!--SPECIAL CONTENT-->

  
    <div class="special-content"><div class="sqs-layout sqs-grid-12 columns-12" data-layout-label="Promoted Block" data-type="promoted-block"><div class="row sqs-row"><div class="col sqs-col-12 span-12">
<div class="sqs-block image-block sqs-block-image" data-block-type="5" data-sqsp-block="image-classic"><div class="sqs-block-content">
<div class="image-block-outer-wrapper layout-caption-below design-layout-inline">
<figure class="sqs-block-image-figure intrinsic" style="max-width:{hero_w}px;">
<div class="image-block-wrapper" data-animation-role="image">
<div class="sqs-image-shape-container-element has-aspect-ratio" style="position:relative;padding-bottom:{hero_ratio:.5f}%;overflow:hidden;">
<img src="{hero_src}" alt="" width="{hero_w}" height="{hero_h}" loading="lazy" decoding="async"
  sizes="(max-width: 640px) 100vw, (max-width: 767px) 100vw, 100vw"
  style="display:block;object-fit:cover;width:100%;height:100%;object-position:50% 50%" />
</div></div></figure></div></div></div>
</div></div></div></div>

  <!--POST HEADER-->

  <header>
		<h1 class="entry-title">
      
        <a href="/{full_slug}" data-content-field="title">{title}</a>
      
    </h1>
    <div class="meta">
      <span class="date"><time class="published" datetime="{date_iso}">{date_display}</time></span>
    </div>
  </header>

  <!--POST BODY-->


  <div class="body entry-content"><div class="sqs-layout sqs-grid-12 columns-12" data-layout-label="Post Body" data-type="item"><div class="row sqs-row"><div class="col sqs-col-12 span-12">
{body}
</div></div></div></div>"""


def import_post(url: str) -> dict:
    slug_match = re.search(r"medium\.com/[^/]+/([^?]+)", url)
    if not slug_match:
        raise ValueError(f"Could not parse slug from URL: {url}")
    slug = slug_match.group(1)
    full_slug = f"blog/{slug}"
    cache_path = DATA_DIR / f"medium-{slug}.json"

    post = fetch_medium_json(url, cache_path)
    if post.get("slug"):
        slug = post["slug"]
        full_slug = f"blog/{slug}"

    image_map = build_image_map(post, slug)
    download_images(image_map, slug)

    entry = {
        "slug": slug,
        "fullSlug": full_slug,
        "title": f'{post["title"]} &mdash; Ke Lyu',
        "date": datetime.fromtimestamp(
            (post.get("latestPublishedAt") or post.get("firstPublishedAt")) / 1000,
            tz=timezone.utc,
        ).strftime("%Y-%m-%d"),
        "content": build_content(post, slug, full_slug, image_map),
    }

    with CONTENT.open(encoding="utf-8") as f:
        data = json.load(f)

    posts = [p for p in data["blog"] if p.get("slug") != slug]
    posts.append(entry)
    posts.sort(key=lambda p: p["date"], reverse=True)
    data["blog"] = posts

    with CONTENT.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    return entry


def main() -> None:
    parser = argparse.ArgumentParser(description="Import a Medium post into the blog.")
    parser.add_argument(
        "url",
        nargs="?",
        default="https://medium.com/@lukelyu/design-thinking-in-ai-product-best-practice-84bf8fd3e130",
        help="Medium article URL",
    )
    args = parser.parse_args()
    entry = import_post(args.url)
    print(f"Imported: {entry['title']} ({entry['date']})")


if __name__ == "__main__":
    main()
