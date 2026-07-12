#!/usr/bin/env python3
"""Generate static HTML pages from scraped kelyu.com content."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "content.json").read_text())
DIST = ROOT / "dist"

WORK_THUMBS = [
    ("cloud-music-player-landscape-mode", "Cloud Music Player Landscape Mode",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/64f17397-b774-400d-a17e-ec9a9982f3c5/Frame+30.png"),
    ("login-signup-redesign", "Login & Signup Redesign",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1688563713761-FH1M4SVIEPIA5WPTGFZR/Cover.png"),
    ("cloud-music-podcast-fm", "Cloud Music Podcast FM",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1688386915080-B9UO2LI72069YHHQ8F14/Cover.png"),
    ("red-pulse-mobile", "Red Pulse Mobile",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1566905809552-X7VM0DJJO5GSNH3BE9L0/RedPulse+Mobile+Cover.png"),
    ("red-pulse-platform-1", "Red Pulse Platform",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1566464781748-9KF6I4UKFAYUI6S0AOWB/Red+Pulse+Platform+Preview.png"),
    ("red-pulse-workspace", "Red Pulse Workspace",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1566482834105-G9VZBQG3NIU4NE9SVGG3/Workspace+Preview.png"),
    ("mobile-ef-classroom", "Mobile EF Classroom",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1567001466836-0FIENTXQNROH5BH7T8E2/EF+Classroom+Preview.png"),
    ("smart-english-study-plan", "Smart English Study Plan",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1565856575423-RVKXEBAUBD0OEIN8NF20/Smt+Eng+Preview.png"),
    ("classroom-techcheck", "EF Classroom Tech Check Redesign",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1566296431320-67F9U8HERV3P0NUP3U1M/Tech+Check+Preview.png"),
    ("cpic-ecommerce-platform", "CPIC E-Commerce Platform",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1565697699369-AQY27NMM6J8S3ZKUTYUN/taibao0.png"),
    ("saic-mobile-app-usability-testing", "SAIC Mobile App Usability Testing",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1565857349070-YR6ITOQJUVI2X00GITWU/SAIC+Preview.png"),
    ("bank-of-hangzhou-mobile-banking-app", "Bank of Hangzhou Mobile Banking App",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1565697382799-N38O5VG4ZTGLIK5VASDC/hz.jpg"),
    ("konica-minolta-pswc-optimization", "Konica Minolta PSWC Optimization",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1565856847845-XN7BIRNHP6TBICJFJXTA/KM+Preview.png"),
]

WORKCN_THUMBS = [
    ("red-pulse-mobile-cn", "Red Pulse 手机客户端",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1571716173616-L37XC7OIWDTQ6F4FSJMD/RedPulse+Mobile+Preview.png"),
    ("red-pulse-platform-cn", "Red Pulse 行研平台",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1571716229517-DGYCYAM8WO721LERF4Q4/Red+Pulse+Platform+Preview.png"),
    ("red-pulse-workspace-cn", "Red Pulse 工作间",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1571716285153-B2PEF54C4SCDSLOAF0W1/Workspace+Preview.png"),
    ("mobile-ef-classroom-cn", "英孚手机教室",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1571716132154-M2C02L3WHZSU3537LICT/EF+Classroom+Preview.png"),
    ("smart-english-study-plan-cn", "Smart English 学习计划",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1571716075744-1BHWEZ3PGW5URI3Y3VNY/Smt+Eng+Preview.png"),
    ("ef-classroom-tech-check-redesign-cn", "英孚在线教室技术检测",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1571716401292-H15I90AX21HUJ5BR6722/Tech+Check+Preview.png"),
    ("cpic-e-commerce-platform-cn", "太平洋保险在线商城",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1565697699369-AQY27NMM6J8S3ZKUTYUN/taibao0.png"),
    ("saic-mobile-app-usability-testing-cn", "上汽手机应用可用性测试",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1571716518063-0NNO2QJZ86VSUIZRQ4OW/SAIC+Preview.png"),
    ("bank-of-hangzhou-mobile-banking-app-cn", "杭州银行手机银行",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1565697382799-N38O5VG4ZTGLIK5VASDC/hz.jpg"),
    ("konica-minolta-pswc-optimization-cn", "柯尼卡美能达打印机管理系统优化",
     "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/1571716496326-4Q8WTR4CI2C48HZ4WEVH/KM+Preview.png"),
]

OTHER_PROJECTS_2015 = [
    "CPIC Group Client Remote Management Platform",
    "CPIC Client Resource Sharing Platform",
    "Johnson & Johnson Intranet Portal",
    "China Minsheng Bank Project Management Portal",
    "China Construction Bank CRM Mobile App",
    "Roche eProcess System",
    "Pactera Telematics Platform",
    "Pactera Knowledge Management System",
    "Pactera HR Management Platform",
    "Qualcomm Android 6.0 Design Specification",
]

OTHER_PROJECTS_2014 = [
    "Wanda Hotel & Resorts Intranet Portal",
    "Bank of Shanghai Retail & Credit System",
    "Bank of Shanghai Backend System User Experience Guidelines",
    "Konica Minolta Legal Storage Optimization",
    "China Everbright Bank Private Banking System",
    "Ericsson Broadcast Management Platform",
    "Alibaba Alike E-mail Transfer Design",
    "Sony Smart TV UX Optimization",
    "CGB Data Management Platform",
]


def all_projects_html() -> str:
    items = ['<h1><strong>Other Projects</strong></h1>', '<div class="year-groups">']

    year_2015 = ['<div class="year-group">', '<p class="year"><strong>2015</strong></p>']
    year_2015.extend(f'<div class="project">{title}</div>' for title in OTHER_PROJECTS_2015)
    year_2015.append('</div>')

    year_2014 = ['<div class="year-group">', '<p class="year"><strong>2014</strong></p>']
    year_2014.extend(f'<div class="project">{title}</div>' for title in OTHER_PROJECTS_2014)
    year_2014.append('</div>')

    items.extend(year_2015)
    items.extend(year_2014)
    items.append('</div>')
    return "\n      ".join(items)

ABOUT_IMAGE = (
    "https://images.squarespace-cdn.com/content/v1/5d4545b5bba29f00015bbc6d/"
    "1567763625111-50918JYNCX49VNW5Y5CA/Luke.png"
)
ABOUT_IMAGE_SRC = f"{ABOUT_IMAGE}?format=2500w"

ABOUT_EN = """
<h1 style="white-space:pre-wrap;">About me</h1>
<p style="white-space:pre-wrap;">It was 2008 when I took an undergraduate course named IT Management for Business at the University of Manchester and I came across with user experience. Since then I fell in love with UX design and therefore I went to the University of Bath to take the HCI course and completed my master degree there,</p>
<p style="white-space:pre-wrap;">Now I've committed myself into user experience design for for 10 years and have rich experiences in Business Development, Requirements Analysis, User Research, Data Analysis, IA, Interaction Design, Usability Testing, and Project Management. I have worked closely with clients providing my UX advises and designs for multi-platform products in different industries. I've worked as vendors and designed for different clients and also worked as in-house designer to design our own products. Both experiences have excited me.</p>
<p style="white-space:pre-wrap;">I also love various activities including dancing, scuba diving, traveling, reading, watching football, etc.</p>
"""

ABOUT_CN = """
<h1 style="white-space:pre-wrap;">关于我</h1>
<p style="white-space:pre-wrap;">2008年，我在曼彻斯特大学攻读了商务信息技术管理的本科课程。在那里我第一次了解到了用户体验。 从那以后我便爱上了用户体验和交互设计，因此我选择去巴斯大学继续攻读人机交互课程，并在那里完成了我的硕士学位，</p>
<p style="white-space:pre-wrap;">现在我已经在用户体验设计领域工作10年了，并且在需求分析、用户研究、数据分析、信息架构、交互设计、可用性测试、业务开发和项目管理等方面拥有丰富的经验。我曾与客户密切合作，为不同行业的多平台产品提供用户体验建议和设计。我曾作为供应商工作，为不同的客户设计，也有作为内部设计师设计自己产品的经验。两种经历我都非常享受并受益匪浅。</p>
<p style="white-space:pre-wrap;">我也喜欢参加各种活动，包括跳舞、潜水、旅游、阅读、看球赛等。</p>
"""


def about_header_image() -> str:
    return f"""
    <div class="extra-wrapper page-header">
      <div class="sqs-layout sqs-grid-12 columns-12">
        <div class="row sqs-row"><div class="col sqs-col-12 span-12">
          <div class="sqs-block image-block sqs-block-image" data-aspect-ratio="29.75"><div class="sqs-block-content">
            <div class="image-block-outer-wrapper layout-caption-below design-layout-inline">
              <figure class="sqs-block-image-figure intrinsic" style="max-width:100%;">
                <div class="image-block-wrapper">
                  <div class="sqs-image-shape-container-element has-aspect-ratio"
                    style="position:relative;padding-bottom:29.75%;overflow:hidden;">
                    <img src="{ABOUT_IMAGE_SRC}" alt="Ke Lyu" loading="lazy" decoding="async"
                      width="1920" height="594"
                      sizes="(max-width: 640px) 100vw, (max-width: 767px) 100vw, 100vw"
                      style="display:block;object-fit:cover;width:100%;height:100%;object-position:50% 50%;" />
                  </div>
                </div>
              </figure>
            </div>
          </div></div>
        </div></div>
      </div>
    </div>"""


def about_text_column(content: str) -> str:
    return f"""
            <div class="col sqs-col-6 span-6">
              <div class="sqs-block html-block sqs-block-html"><div class="sqs-block-content">
                <div class="sqs-html-content">{content}</div>
              </div></div>
            </div>"""

BODY_INDEX = (
    "blog-sidebar-display-auto index-thumb-title-position-below index-item-layout-auto "
    "thumbnail-layout-basic-grid thumbnails-on-open-page-show-all layout-style-left "
    "page-borders-none underline-body-links gallery-page-controls-tiny-thumbnails "
    "social-icon-style-normal show-category-navigation collection-type-index "
    "collection-layout-default homepage view-list mobile-style-available site-title has-primary-nav"
)

BODY_PAGE = (
    "blog-sidebar-display-auto layout-style-left page-borders-none underline-body-links "
    "collection-type-page collection-layout-default mobile-style-available site-title has-primary-nav"
)

BODY_BLOG = (
    "blog-sidebar-display-auto layout-style-left page-borders-none underline-body-links "
    "collection-type-blog collection-layout-default mobile-style-available site-title has-primary-nav"
)

def nav(active: str) -> str:
    items = [
        ("workcn", "中文案例", "/workcn"),
        ("work", "Work", "/"),
        ("blog", "Blog", "/blog/"),
        ("about", "About", "/about"),
        ("resume", "Resume", "/s/Ke-Lyu-Resume-tpm4.pdf", True),
    ]
    lis = []
    for item in items:
        key, label, href = item[0], item[1], item[2]
        external = item[3] if len(item) > 3 else False
        cls = "active-link" if key == active else ""
        target = ' target="_blank"' if external else ""
        lis.append(f'<li class="index-collection {cls}"><a href="{href}"{target}>{label}</a></li>')
    ul = "\n".join(lis)
    return f"""<nav class="main-nav"><ul>{ul}</ul></nav>"""


def shell(title: str, body_class: str, active_nav: str, main: str, extra_scripts: str = "") -> str:
    return f"""<!doctype html>
<html lang="en-US">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{title}</title>
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="preconnect" href="https://images.squarespace-cdn.com" />
  <link rel="stylesheet" href="/css/site.css" />
  <link rel="stylesheet" href="/css/overrides.css" />
</head>
<body class="{body_class}" id="site-body">
  <div id="canvas">
    <div id="mobileNav"><div id="mobileNavWrapper" class="wrapper">{nav(active_nav)}</div></div>
    <div id="mobileMenuLink"><a>Menu</a></div>
    <header id="header">
      <div id="logo"><h1 class="logo"><a href="/">Ke Lyu</a></h1></div>
      <div id="topNav">{nav(active_nav)}</div>
    </header>
    {main}
    <footer id="footer"><div class="sqs-layout sqs-grid-1 columns-1 empty"></div></footer>
  </div>
  <div class="sqs-spin" aria-hidden="true"></div>
  <script src="/js/main.js"></script>
  {extra_scripts}
</body>
</html>"""


def thumb_grid(thumbs, prefix: str) -> str:
    cards = []
    for slug, title, img in thumbs:
        url = f"/{slug}/"
        cards.append(f"""
        <a class="project" href="{url}">
          <div>
            <div class="project-image">
              <div class="intrinsic"><div class="content-fill">
                <img src="{img}?format=750w" alt="{title}" loading="lazy" />
              </div></div>
              <div class="project-item-count">0</div>
            </div>
            <div class="project-title">{title}</div>
          </div>
        </a>""")
    return f'<div id="projectThumbs"><div class="container">{"".join(cards)}</div></div>'


def clean_project_content(html: str) -> str:
    html = html.strip()
    section_match = re.match(r"\s*<section[^>]*>(.*)</section>\s*", html, re.S)
    if section_match:
        html = section_match.group(1).strip()
    html = re.sub(r"\s*</section>\s*$", "", html)
    html = re.sub(
        r'<div class="extra-wrapper page-footer">.*?</div>\s*$',
        "",
        html,
        flags=re.S,
    )
    return html.strip()


def project_controls_nav(slugs: list[str], current_slug: str, back_href: str, back_label: str) -> str:
    idx = slugs.index(current_slug) if current_slug in slugs else -1
    prev_html = (
        f'<a href="/{slugs[idx - 1]}/">prev</a>' if idx > 0 else '<span class="disabled">prev</span>'
    )
    next_html = (
        f'<a href="/{slugs[idx + 1]}/">next</a>'
        if 0 <= idx < len(slugs) - 1
        else '<span class="disabled">next</span>'
    )
    return f"""
  <div class="project-controls project-page-controls">
    <div>
      <div id="projectNav">{prev_html} / {next_html}</div>
      <a href="{back_href}" class="back-to-work">{back_label}</a>
    </div>
  </div>"""


def project_pages(thumbs, content_key: str) -> str:
    content_map = {p["slug"]: p["content"] for p in DATA[content_key]}
    blocks = []
    for slug, title, _ in thumbs:
        url = f"/{slug}/"
        content = clean_project_content(content_map.get(slug, ""))
        blocks.append(f"""
      <div class="project page-project" data-url="{url}">
        <div class="project-content-source" hidden>{content}</div>
      </div>""")
    return f'<div id="projectPages" data-collection-id="">{"".join(blocks)}</div>'


def index_page(thumbs, content_key: str, active_nav: str, show_hero: bool, show_footer: bool) -> str:
    hero = ""
    if show_hero:
        hero = """
    <div class="page-header">
      <h2>Hi! I'm Ke LYU<br>a&nbsp;passionate UX designer</h2>
      <h3>I like solving problems through design</h3>
    </div>"""
    footer = ""
    if show_footer:
        footer = f"""
    <div class="all-projects">
      {all_projects_html()}
    </div>
    <div class="page-divider"></div>"""
    main = f"""
    <div class="page-divider"></div>
    {hero}
    {project_pages(thumbs, content_key)}
    {thumb_grid(thumbs, content_key)}
    {footer}"""
    return shell("Ke Lyu", BODY_INDEX, active_nav, main, '<script src="/js/index.js"></script>')


def standalone_project_page(title: str, content: str, nav_html: str = "") -> str:
    cleaned = clean_project_content(content)
    main = f"""
    <div class="page-divider"></div>
    <section id="page" role="main"><div class="content">{cleaned}</div>{nav_html}</section>
    <div class="page-divider"></div>"""
    page_title = re.sub(r" — Ke Lyu$", "", title)
    return shell(f"{page_title} — Ke Lyu", BODY_PAGE, "work", main)


def about_page() -> str:
    main = f"""
    <div class="page-divider"></div>
    {about_header_image()}
    <section id="page" role="main">
      <div class="content"><div class="sqs-layout sqs-grid-12 columns-12">
        <div class="row sqs-row"><div class="col sqs-col-12 span-12">
          <div class="row sqs-row">{about_text_column(ABOUT_EN)}{about_text_column(ABOUT_CN)}
          </div>
        </div></div>
      </div></div>
    </section>
    <div class="page-divider"></div>"""
    return shell("About — Ke Lyu", BODY_PAGE, "about", main)


def clean_title(title: str) -> str:
    return re.sub(r"\s*(?:—|&mdash;)\s*Ke Lyu\s*$", "", title)


def blog_sidebar(active_slug=None) -> str:
    items = []
    for post in DATA["blog"]:
        slug = post["fullSlug"]
        title = clean_title(post["title"])
        date = post.get("date", "")
        href = f"/{slug}/"
        active_cls = " active-link" if active_slug == slug else ""
        items.append(f"""
        <article class="summary-item summary-item-record-type-text">
          <div class="summary-content">
            <time class="summary-metadata-item summary-metadata-item--date timestamp">{date}</time>
            <div class="summary-title"><a href="{href}" class="summary-title-link{active_cls}">{title}</a></div>
          </div>
        </article>""")
    return f"""
    <aside id="sidebar" data-content-field="Sidebar">
      <div class="sqs-layout sqs-grid-1 columns-1" id="sidebarBlocks">
        <div class="row sqs-row"><div class="col sqs-col-1 span-1">
          <div class="sqs-block html-block sqs-block-html"><div class="sqs-block-content">
            <div class="sqs-html-content"><h2 style="white-space:pre-wrap;">Latest Posts</h2></div>
          </div></div>
          <div class="sqs-block summary-block summary-v2-block"><div class="sqs-block-content">
            <div class="summary-block"><div class="summary-item-list">{"".join(items)}</div></div>
          </div></div>
        </div></div>
      </div>
    </aside>"""


def blog_list_page() -> str:
    entries = []
    for i, post in enumerate(DATA["blog"], 1):
        entries.append(f"""
    <article class="hentry post-type-text article-index-{i}">
      {post["content"]}
    </article>""")
    main = f"""
    <div class="page-divider"></div>
    <section id="page" role="main"><div class="content"><div class="article-list hfeed">{"".join(entries)}</div>{blog_sidebar()}</div></section>
    <div class="page-divider"></div>"""
    return shell("Blog — Ke Lyu", BODY_BLOG, "blog", main)


def blog_post_page(post: dict) -> str:
    title = clean_title(post["title"])
    main = f"""
    <div class="page-divider"></div>
    <section id="page" role="main">
      <div class="content"><div class="article-wrapper"><article class="hentry hentry-single">{post["content"]}</article></div>{blog_sidebar(post["fullSlug"])}</div>
    </section>
    <div class="page-divider"></div>"""
    return shell(f"{title} — Ke Lyu", BODY_BLOG, "blog", main)


def write(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def copy_assets() -> None:
    import shutil
    public = ROOT / "public"
    for name in ("css", "js", "favicon.ico", "s"):
        src = public / name
        dst = DIST / name
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        elif src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def main() -> None:
    if DIST.exists():
        import shutil
        shutil.rmtree(DIST)
    DIST.mkdir()

    write(DIST / "index.html", index_page(WORK_THUMBS, "work", "work", True, True))
    write(DIST / "workcn" / "index.html", index_page(WORKCN_THUMBS, "workcn", "workcn", False, False))
    write(DIST / "about" / "index.html", about_page())
    write(DIST / "blog" / "index.html", blog_list_page())

    for post in DATA["blog"]:
        write(DIST / post["fullSlug"] / "index.html", blog_post_page(post))

    work_slugs = [slug for slug, _, _ in WORK_THUMBS]
    workcn_slugs = [slug for slug, _, _ in WORKCN_THUMBS]

    content_map = {p["slug"]: p for p in DATA["work"] + DATA["workcn"]}
    for slug, info in content_map.items():
        if slug in work_slugs:
            nav = project_controls_nav(work_slugs, slug, "/", "Back to Work")
        elif slug in workcn_slugs:
            nav = project_controls_nav(workcn_slugs, slug, "/workcn", "Back to Work")
        else:
            nav = ""
        write(DIST / slug / "index.html", standalone_project_page(info["title"], info["content"], nav))

    copy_assets()
    print(f"Built site to {DIST}")


if __name__ == "__main__":
    main()
