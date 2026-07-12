#!/usr/bin/env python3
"""Generate static HTML pages from scraped kelyu.com content."""

import json
import re
from pathlib import Path
from typing import Optional

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

OTHER_PROJECTS_CN_2015 = [
    "太平洋保险集团客户经理移动平台",
    "太平洋保险客户资源共享平台",
    "强生中国内网门户",
    "中国民生银行项目管理门户",
    "中国建设银行CRM手机应用",
    "罗氏eProcess医院价格谈判系统",
    "文思海辉车联网数据服务平台",
    "文思海辉知识管理平台",
    "文思海辉人力资源管理平台",
    "高通安卓6.0 OS设计规范",
]

OTHER_PROJECTS_CN_2014 = [
    "万达酒店及度假村业务信息服务平台",
    "上海银行零售信贷系统",
    "上海银行后台管理系统用户体验规范",
    "柯尼卡美能达法律文案储存系统优化",
    "中国光大银行私人银行",
    "爱立信广播管理平台",
    "阿里巴巴阿里客邮箱搬迁设计",
    "索尼智能电视用户体验优化",
    "广发银行数控管理平台",
]


def all_projects_html(lang: str = "en") -> str:
    if lang == "zh-CN":
        heading = "其他项目"
        projects_2015 = OTHER_PROJECTS_CN_2015
        projects_2014 = OTHER_PROJECTS_CN_2014
    else:
        heading = "Other Projects"
        projects_2015 = OTHER_PROJECTS_2015
        projects_2014 = OTHER_PROJECTS_2014

    def year_column(year: str, titles: list[str]) -> str:
        items = "".join(
            f'<p class="" style="white-space:pre-wrap;">{title}</p>' for title in titles
        )
        return f"""
            <div class="col sqs-col-6 span-6">
              <div class="sqs-block html-block sqs-block-html"><div class="sqs-block-content">
                <div class="sqs-html-content">
                  <p class="" style="white-space:pre-wrap;"><strong>{year}</strong></p>
                  {items}
                </div>
              </div></div>
            </div>"""

    return f"""
      <div class="sqs-layout sqs-grid-12 columns-12">
        <div class="row sqs-row"><div class="col sqs-col-12 span-12">
          <div class="sqs-block html-block sqs-block-html"><div class="sqs-block-content">
            <div class="sqs-html-content">
              <h1 style="white-space:pre-wrap;"><strong>{heading}</strong></h1>
            </div>
          </div></div>
          <div class="row sqs-row">{year_column("2015", projects_2015)}{year_column("2014", projects_2014)}
          </div>
        </div></div>
      </div>"""

ABOUT_IMAGE = "/images/luke.png"
ABOUT_IMAGE_SRC = ABOUT_IMAGE

ABOUT_EN = """
<h1 style="white-space:pre-wrap;">About me</h1>
<p style="white-space:pre-wrap;">My passion for UX began in 2008 during my undergraduate studies at the University of Manchester, which inspired me to pursue a Master's degree in Human-Computer Interaction at the University of Bath. Since then, I have spent more than 10 years designing user-centered digital products across music streaming, fintech, education, e-commerce, and enterprise platforms.</p>
<p style="white-space:pre-wrap;">Currently, I am a Lead UX Designer at NetEase Cloud Music, leading the podcast experience from user research and interaction design to usability testing and mentoring junior designers. My work has contributed to significant user growth and engagement through data-driven, end-to-end design.</p>
<p style="white-space:pre-wrap;">Having worked in both in-house product teams and design agencies, I enjoy solving complex problems while balancing user needs with business goals. Beyond product design, I also deliver UX training, write design articles, and actively share knowledge with the design community. Outside work, I enjoy traveling, scuba diving, dancing, reading, and football, all of which continually inspire my creativity and empathy as a designer.</p>
"""

ABOUT_CN = """
<h1 style="white-space:pre-wrap;">关于我</h1>
<p style="white-space:pre-wrap;">对用户体验的热爱是从2008年开始的，当时在曼彻斯特大学攻读本科，这段经历激励我在巴斯大学继续深造，获得了人机交互硕士学位。此后，我花了超过十年的时间，为音乐流媒体、金融科技、教育、电商和企业平台设计以用户为中心的数字产品。</p>
<p style="white-space:pre-wrap;">目前，我是网易云音乐的高级用户体验设计师，负责播客体验的设计工作，涵盖用户研究、交互设计、可用性测试，以及指导初级设计师。我的设计通过数据驱动帮助产品实现了用户增长和活跃度的明显提升。</p>
<p style="white-space:pre-wrap;">我既在产品团队内部工作过，也曾在设计机构任职，善于在满足用户需求与实现商业目标之间找到平衡，解决复杂问题。除了产品设计，我也会给团队做UX培训、写写设计文章，平时也喜欢在社区里跟同行分享交流。工作之外，我喜欢旅行、舞蹈、阅读和足球，这些爱好不断激发我的创造力，也让我做设计的时候更能站在用户角度去感受。</p>
"""

HERO_EN = """
      <h2>Hi! I'm Ke LYU<br>a&nbsp;passionate UX designer</h2>
      <h3>I like solving problems through design</h3>"""

HERO_CN = """
      <h2 style="white-space:pre-wrap;">你好！我叫吕可<br>是一名充满热情的用户体验设计师</h2>
      <h3 style="white-space:pre-wrap;">我希望通过设计解决各种问题</h3>"""


def page_header_hero(content: str, lang: Optional[str] = None) -> str:
    lang_attr = f' lang="{lang}"' if lang else ""
    return f"""
    <div class="extra-wrapper page-header"{lang_attr}>
      {content}
    </div>"""


def about_header_image() -> str:
    return f"""
    <div class="extra-wrapper page-header">
      <div class="sqs-layout sqs-grid-12 columns-12">
        <div class="row sqs-row"><div class="col sqs-col-12 span-12">
          <div class="sqs-block image-block sqs-block-image" data-aspect-ratio="29.75"><div class="sqs-block-content">
            <div class="image-block-outer-wrapper layout-caption-below design-layout-inline">
              <figure class="sqs-block-image-figure intrinsic" style="max-width:100%;">
                <div class="image-block-wrapper">
                  <div class="sqs-image-shape-container-element has-aspect-ratio">
                    <img src="{ABOUT_IMAGE_SRC}" alt="Ke Lyu" loading="lazy" decoding="async"
                      width="1920" height="594"
                      sizes="(max-width: 640px) 100vw, (max-width: 767px) 100vw, 100vw" />
                  </div>
                </div>
              </figure>
            </div>
          </div></div>
        </div></div>
      </div>
    </div>"""


def about_text_column(content: str, lang: str = "en") -> str:
    return f"""
            <div class="col sqs-col-6 span-6" lang="{lang}">
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
        lang_attr = ' lang="zh-CN"' if key == "workcn" else ""
        lis.append(f'<li class="index-collection {cls}"{lang_attr}><a href="{href}"{target}>{label}</a></li>')
    ul = "\n".join(lis)
    return f"""<nav class="main-nav"><ul>{ul}</ul></nav>"""


def page_lang(*, nav: Optional[str] = None, slug: Optional[str] = None) -> str:
    if nav == "workcn":
        return "zh-CN"
    if slug and (slug.endswith("-cn") or slug.endswith("-z85lh")):
        return "zh-CN"
    return "en-US"


def shell(title: str, body_class: str, active_nav: str, main: str, extra_scripts: str = "", lang: str = "en-US") -> str:
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{title}</title>
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="preconnect" href="https://images.squarespace-cdn.com" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+Pro:ital,wght@0,400;0,600;0,700;1,400&display=swap" />
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
    return f'<div id="projectThumbs"><div class="wrapper">{"".join(cards)}</div></div>'


def clean_project_content(html: str) -> str:
    html = html.strip()
    section_match = re.match(r"\s*<section[^>]*>(.*)</section>\s*", html, re.S)
    if section_match:
        html = section_match.group(1).strip()
    html = re.sub(
        r'<div class="extra-wrapper page-footer">.*?</div>\s*$',
        "",
        html,
        flags=re.S,
    )
    html = re.sub(r"</section>\s*$", "", html.strip())
    html = re.sub(r"</?section[^>]*>", "", html)
    return html.strip()


def project_controls_nav(
    slugs: list[str],
    current_slug: str,
    back_href: str,
    back_label: str,
    *,
    index_overlay: bool = False,
) -> str:
    idx = slugs.index(current_slug) if current_slug in slugs else -1
    prev_html = (
        f'<a href="/{slugs[idx - 1]}/">prev</a>' if idx > 0 else '<span class="disabled">prev</span>'
    )
    next_html = (
        f'<a href="/{slugs[idx + 1]}/">next</a>'
        if 0 <= idx < len(slugs) - 1
        else '<span class="disabled">next</span>'
    )
    classes = "project-controls" if index_overlay else "project-controls project-page-controls"
    return f"""
  <div class="{classes}">
    <div>
      <div id="projectNav">{prev_html} / {next_html}</div>
      <a href="{back_href}" class="back-to-work">{back_label}</a>
    </div>
  </div>"""


def index_project_controls(back_label: str) -> str:
    return f"""
    <div class="project-controls">
      <div>
        <div id="projectNav"><span class="prev-project">prev</span> / <span class="next-project">next</span></div>
        <a href="#" class="back-to-work">{back_label}</a>
      </div>
    </div>"""


def project_pages(thumbs, content_key: str, back_href: str, back_label: str) -> str:
    content_map = {p["slug"]: p["content"] for p in DATA[content_key]}
    blocks = []
    for slug, title, _ in thumbs:
        url = f"/{slug}/"
        content = clean_project_content(content_map.get(slug, ""))
        blocks.append(f"""
      <div class="project page-project" data-url="{url}">
        <div class="project-content-source" hidden>{content}</div>
      </div>""")
    nav = index_project_controls(back_label)
    return f'<div id="projectPages" data-collection-id="">{"".join(blocks)}{nav}\n    </div>'


def index_page(
    thumbs,
    content_key: str,
    active_nav: str,
    hero: Optional[str] = None,
    show_footer: bool = False,
    back_href: str = "/",
    back_label: str = "Back to Work",
    hero_lang: Optional[str] = None,
    footer_lang: Optional[str] = None,
) -> str:
    hero_html = page_header_hero(hero, hero_lang) if hero else ""
    footer = ""
    if show_footer:
        footer_lang_attr = f' lang="{footer_lang}"' if footer_lang else ""
        footer = f"""
    <div class="extra-wrapper page-footer"{footer_lang_attr}>
      {all_projects_html(footer_lang or "en")}
    </div>
    <div class="page-divider"></div>"""
    main = f"""
    <div class="page-divider"></div>
    {hero_html}
    <section id="page" role="main">
    {project_pages(thumbs, content_key, back_href, back_label)}
    {thumb_grid(thumbs, content_key)}
    </section>
    {footer}"""
    return shell("Ke Lyu", BODY_INDEX, active_nav, main, '<script src="/js/index.js"></script>', page_lang(nav=active_nav))


def standalone_project_page(title: str, content: str, nav_html: str = "", slug: str = "") -> str:
    cleaned = clean_project_content(content)
    main = f"""
    <div class="page-divider"></div>
    <section id="page" role="main"><div class="content">{cleaned}</div>{nav_html}</section>
    <div class="page-divider"></div>"""
    page_title = re.sub(r" — Ke Lyu$", "", title)
    return shell(f"{page_title} — Ke Lyu", BODY_PAGE, "work", main, lang=page_lang(slug=slug))


def about_page() -> str:
    main = f"""
    <div class="page-divider"></div>
    {about_header_image()}
    <section id="page" role="main" class="about-page">
      <div class="content"><div class="sqs-layout sqs-grid-12 columns-12">
        <div class="row sqs-row"><div class="col sqs-col-12 span-12">
          <div class="row sqs-row">{about_text_column(ABOUT_EN, "en")}{about_text_column(ABOUT_CN, "zh-CN")}
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
    return shell(f"{title} — Ke Lyu", BODY_BLOG, "blog", main, lang=page_lang(slug=post["fullSlug"]))


def write(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def copy_assets() -> None:
    import shutil
    public = ROOT / "public"
    for name in ("css", "js", "images", "favicon.ico", "s"):
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

    write(DIST / "index.html", index_page(WORK_THUMBS, "work", "work", HERO_EN, True, "/", "Back to Work"))
    write(DIST / "workcn" / "index.html", index_page(WORKCN_THUMBS, "workcn", "workcn", HERO_CN, True, "/workcn", "Back to Work", "zh-CN", "zh-CN"))
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
        write(DIST / slug / "index.html", standalone_project_page(info["title"], info["content"], nav, slug))

    copy_assets()
    print(f"Built site to {DIST}")


if __name__ == "__main__":
    main()
