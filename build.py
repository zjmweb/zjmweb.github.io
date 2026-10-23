"""Rebuild the static website pages using only the Python standard library.

Run: python build.py
Content and shared HTML live here; appearance lives in styles.css.
The generated HTML also works directly without Python or a build step.
"""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent
EMAIL = 'Zjmweb0805@163.com'
NAV = [('Home', 'index.html'), ('Research', 'research.html'), ('Portfolio', 'portfolio.html'), ('CV', 'cv.html'), ('Work', 'work.html'), ('Contact', 'contact.html')]

def link(href, label, css='text-link', external=False):
    extra = ' target="_blank" rel="noopener noreferrer"' if external else ''
    return f'<a class="{css}" href="{escape(href)}"{extra}>{label}</a>'

def art(kind, title, caption):
    sizes = 'width="500" height="570"' if kind == 'portal' else 'width="500" height="275"'
    return f'''<figure class="art {kind}"><img src="assets/{kind}.svg" {sizes} alt="" loading="{'eager' if kind == 'portal' else 'lazy'}"><div class="art-title">{title}</div><figcaption>Concept illustration / {caption}</figcaption></figure>'''

def intro(number, title, description):
    return f'<header class="page-intro"><p class="eyebrow">{number}</p><h1>{title}</h1><p class="lead">{description}</p></header>'

def tags(items):
    return '<div class="tags">' + ''.join(f'<span class="tag">{escape(s)}</span>' for s in items) + '</div>'

DIRECTIONS = [
    ('Stories you can step into', 'Digital storytelling for cultural heritage: exploring how immersive narratives bring people closer to cultural stories.'),
    ('Culture meets computation', 'AI and human–computer interaction as tools for engaging with cultural knowledge and creative expression.'),
    ('Learning through discovery', 'Digital game-based learning, knowledge retention and cultural understanding.'),
]

def directions():
    return '<div class="directions">' + ''.join(f'<article class="direction"><h3>{title}</h3><p>{body}</p></article>' for title, body in DIRECTIONS) + '</div>'

PUBLICATIONS = [
    ('2024', 'Unity-based Chinese Digital Education Game: Journey to Cultural Relics of Ancient China', 'Lecture Notes in Education Psychology and Public Media, 49, 119–132.', '10.54254/2753-7048/49/20231879'),
    ('2023', 'Fan economy and Digital Media: How Does Produce 101(china) utilize digital media to gain commercial benefit?', 'Advances in Social Science, Education and Humanities Research, 141–147.', '10.2991/978-2-38476-130-2_18'),
]

from portfolio_content import PROJECTS

def project_visual(p, caption=True):
    width, height = json.loads((ROOT / 'assets/projects/dimensions.json').read_text())[p['image']]
    cover_class = ' supplied-cover' if p['image'].endswith('-cover.jpg') else ''
    return f'''<figure class="project-photo {p['kind']}{cover_class}"><img src="assets/projects/{p['image']}" width="{width}" height="{height}" alt="{escape(p['alt'])}" loading="lazy">{('<figcaption>' + escape(p['short']) + '</figcaption>') if caption else ''}</figure>'''

def previews():
    cards = []
    for p in PROJECTS[:3]:
        cards.append(f'''<article class="preview-card"><a href="{p['page']}">{project_visual(p, False)}<p class="eyebrow">{p['meta']}</p><h3>{p['title']} <span aria-hidden="true">↗</span></h3><p class="muted small">{p['description']}</p></a></article>''')
    return '<div class="preview-grid">' + ''.join(cards) + '</div>'

HOME = f'''
<section class="hero" aria-labelledby="home-title">
  <div><p class="eyebrow">Durham University · PhD researcher · Exp. 2029</p>
  <h1 id="home-title">Vicky<br>Zhang</h1>
  <p class="tagline">Bringing heritage<br>to life through stories.</p>
  <p class="bio">I am Jinman (Vicky) Zhang, a PhD researcher at Durham University. I explore digital storytelling for cultural heritage through VR, AI and human–computer interaction.</p>
  {tags(['VR storytelling', 'AI', 'HCI', 'DGBL'])}
  <div class="actions">{link('portfolio.html', 'Explore selected work ↗', 'button')}{link('research.html', 'My research ↗', 'button secondary')}</div>
  <p class="supervisors">Digital Storytelling for Cultural Heritage<br>With Dr Stuart James &amp; Prof. Giles Gasper</p></div>
  {(ROOT / 'heritage-scene.inc').read_text(encoding='utf-8')}
</section>
<section class="section" aria-labelledby="research-preview"><div class="section-head"><div><p class="eyebrow">01 / A thread through my work</p><h2 id="research-preview">Heritage, reimagined.</h2></div>{link('research.html', 'Explore research ↗')}</div>{directions()}</section>
<section class="section" aria-labelledby="work-preview"><div class="section-head"><div><p class="eyebrow">02 / Selected portfolio</p><h2 id="work-preview">Research, made tangible.</h2></div>{link('portfolio.html', 'View portfolio ↗')}</div>{previews()}</section>
'''

pubs = ''.join(f'''<article class="publication"><time datetime="{year}">{year}</time><div><h3>{title}</h3><p class="meta">Zhang, J. · {venue}</p><div class="links">{link('https://doi.org/' + doi, 'Read publication ↗', external=True)}</div><p class="small muted" style="margin-top:14px">DOI: {doi}</p></div></article>''' for year, title, venue, doi in PUBLICATIONS)

RESEARCH = intro('01 / Research', 'Heritage,<br><span class="serif-italic">reimagined.</span>', 'Cultural heritage is the thread. Storytelling is the way in.') + f'''
<section class="research-note" aria-labelledby="phd-focus"><div><p class="eyebrow">Current PhD focus</p><h3 id="phd-focus">Digital Storytelling<br>for Cultural Heritage</h3></div><div><p>Computer Science · Durham University<br>Expected graduation: 2029</p><p class="small muted">Supervisors: Dr Stuart James &amp; Prof. Giles Gasper</p></div></section>
<section aria-label="Research interests">{directions()}</section>
<section id="publications" class="section" aria-labelledby="publications-title"><p class="eyebrow">Publications</p><h2 id="publications-title">Selected writing</h2>{pubs}</section>
'''

projects_html = ''.join(f'''<article class="project" id="{p['id']}" data-category="{p['category']}"><a href="{p['page']}" aria-label="View {escape(p['title'])} case study">{project_visual(p)}</a><div><p class="eyebrow">{p['meta']}</p><h2><a href="{p['page']}">{p['title']}</a></h2><p class="description">{p['description']}</p>{tags(p['tags'])}<div class="actions">{link(p['page'], 'Explore case study ↗', 'button secondary')}{link('https://www.youtube.com/watch?v=' + p['video'], 'Watch film ↗', external=True)}</div></div></article>''' for p in PROJECTS)

PORTFOLIO = intro('02 / Portfolio', 'Stories take<br><span class="serif-italic">many forms.</span>', 'Games, cultural encounters and interactive experiences — a selection of research and creative practice.') + f'''
<div class="filter-bar" role="group" aria-label="Filter projects"><button data-filter="all" aria-pressed="true">All work</button><button data-filter="games" aria-pressed="false">Games &amp; learning</button><button data-filter="installation" aria-pressed="false">Interactive installation</button><button data-filter="web" aria-pressed="false">Web &amp; interaction</button></div><p class="visually-hidden" id="filter-status" role="status" aria-live="polite">4 projects shown.</p>
<div class="projects">{projects_html}</div>
'''

EDUCATION = [
    ('Expected 2029', 'Durham University', 'PhD in Computer Science', 'Digital Storytelling for Cultural Heritage<br>Supervisors: Dr Stuart James &amp; Prof. Giles Gasper'),
    ('2021–2022', 'The University of Edinburgh', 'MSc in Design and Digital Media · Merit', ''),
    ('2017–2021', 'Beijing Language and Culture University', 'BEng in Digital Media Technology', ''),
    ('2019–2020', 'University of Birmingham', 'Exchange in Computer Science and Software Engineering', ''),
]
education_html = ''.join(f'<article class="timeline-row"><time>{date}</time><div><h3>{school}</h3><p>{degree}</p><p class="small">{detail}</p></div></article>' for date, school, degree, detail in EDUCATION)

CV = intro('03 / CV', 'A journey through<br><span class="serif-italic">stories &amp; making.</span>', 'Education, research and a practice shaped by digital media, learning and interaction.') + f'''
<div class="split"><section aria-labelledby="education-title"><p class="eyebrow">Education</p><h2 id="education-title">Academic background</h2><div class="timeline">{education_html}</div></section>
<aside class="aside-card"><p class="eyebrow">Curriculum vitae</p><h3>A little more<br>of the story.</h3><p class="muted">Explore my teaching, professional experience and research through the pages of this website.</p>{link('work.html', 'Work &amp; teaching ↗', 'text-link')}<br><a class="button" href="assets/CV-Jinman-Zhang.pdf" download>Download original CV ↓</a><p class="note">This is the original uploaded CV. It predates the Durham PhD and the updated 2023–2026 New Oriental dates; the website reflects these updates.</p></aside></div>
<section class="section" aria-labelledby="skills-title"><p class="eyebrow">Tools &amp; languages</p><h2 id="skills-title">Ways of making</h2>{tags(['Unity', 'Unreal', 'TouchDesigner', 'Maya', 'Adobe Creative Suite', 'C#', 'Python', 'HTML & CSS'])}<p class="muted">Chinese (native) · English (IELTS 7)</p></section>
'''

TEACHING = ['Game design', 'Web development', 'VR narrative', 'Immersive spatial installation', 'AR applications', 'User experience']
WORK = intro('04 / Work', 'Teaching &amp;<br><span class="serif-italic">professional practice.</span>', 'Bringing together creative technology, education and multimedia production.') + f'''
<section aria-labelledby="professional-title"><p class="eyebrow">Professional experience</p><article class="timeline-row"><time>2023–2026</time><div><h2 id="professional-title">New Oriental</h2><p class="lead">Star Mentor · 明星导师</p><p class="muted">Teaching across game design, web development and immersive media.</p><div class="teaching">{''.join(f'<article><h4>{s}</h4></article>' for s in TEACHING)}</div></div></article></section>
<section class="section" aria-labelledby="internship-title"><p class="eyebrow">Internship experience</p><article class="timeline-row"><time>2021–2022</time><div><h2 id="internship-title">China Global Television Network</h2><p class="lead">CGTN · Financial News Department</p><p class="muted">Multimedia production, social media content, video editing and motion graphics.</p><h3>Chinese Hanfu · 汉服世代</h3><p class="muted">Launched and built the Xiaohongshu account from scratch during my internship, combining content curation, video editing, motion graphics and event visuals to share stories of Chinese Hanfu culture.</p><div class="social-account"><div><p class="eyebrow">Xiaohongshu / 小红书</p><h4>CGTN @汉服世代</h4><p class="small muted">Account snapshot: 8,458 followers · October 2026</p></div>{link('https://xhslink.cn/o/9mfyI6qfIQh', 'Explore the account ↗', 'button secondary', external=True)}</div><p class="small muted" style="margin-top:20px">Chinese Hanfu is also present on Facebook, Instagram and Douyin.</p></div></article></section>
'''

WORK = WORK.replace('<p class="small muted" style="margin-top:20px">Chinese Hanfu is also present on Facebook, Instagram and Douyin.</p>', '<div class="actions">' + link('https://www.facebook.com/ChineseHanfu2003', 'Facebook ↗', external=True) + link('https://www.instagram.com/chinese_hanfu_/', 'Instagram ↗', external=True) + link('https://v.douyin.com/8X9xg0kQWMA/', 'Douyin / 抖音 ↗', external=True) + '</div>')

from student_work import selected_student_work
from student_research import selected_student_research
WORK = WORK.replace('<section class="section" aria-labelledby="internship-title">', selected_student_work() + selected_student_research() + '<section class="section" aria-labelledby="internship-title">')

CONTACT = intro('05 / Contact', 'Every heritage story<br>has a <span class="serif-italic">next chapter.</span>', 'For conversations about digital storytelling, cultural heritage, immersive experiences and creative collaboration.') + f'''
<div class="contact-layout"><section class="contact-panel" aria-labelledby="email-title"><p class="eyebrow">Say hello</p><h2 id="email-title">Let’s start<br>a conversation.</h2><a class="contact-email" href="mailto:{EMAIL}">{EMAIL}</a><div class="actions">{link('mailto:' + EMAIL, 'Send an email ↗', 'button')}</div><button class="copy-button" type="button">Copy email address</button><p class="copy-status" role="status" aria-live="polite"></p></section><section><p class="eyebrow">Based in</p><h2>Durham, UK</h2><p class="lead">PhD researcher<br>Department of Computer Science<br>Durham University</p><p class="muted">Digital Storytelling for Cultural Heritage</p>{tags(['Cultural heritage', 'VR', 'AI', 'HCI'])}<div class="actions">{link('research.html', 'Research ↗', 'text-link')}{link('portfolio.html', 'Portfolio ↗', 'text-link')}</div></section></div>
'''

PAGES = [
    ('index.html', 'Home', 'Jinman (Vicky) Zhang — PhD researcher at Durham University exploring digital storytelling for cultural heritage, VR, AI and HCI.', HOME),
    ('research.html', 'Research', 'Research interests and publications in digital storytelling, cultural heritage, AI and game-based learning.', RESEARCH),
    ('portfolio.html', 'Portfolio', 'Selected games and interactive installations by Jinman (Vicky) Zhang.', PORTFOLIO),
    ('cv.html', 'CV', 'Education and curriculum vitae of Jinman (Vicky) Zhang, Durham University PhD researcher.', CV),
    ('work.html', 'Work', 'Teaching at New Oriental and multimedia internship experience at CGTN.', WORK),
    ('contact.html', 'Contact', 'Contact Jinman (Vicky) Zhang for research and creative conversations.', CONTACT),
]

def case_study(p):
    sections = ''.join(f'<section class="case-section"><p class="eyebrow">0{i + 1} / The approach</p><h2>{heading}</h2><p>{body}</p></section>' for i, (heading, body) in enumerate(p['sections']))
    sizes = json.loads((ROOT / 'assets/projects/dimensions.json').read_text())
    gallery = ''.join(f'<figure class="case-figure" style="max-width:min(100%, {min(1100, sizes[image][0])}px)"><a href="assets/projects/{image}" target="_blank" rel="noopener" aria-label="Open full-size project image"><img src="assets/projects/{image}" width="{sizes[image][0]}" height="{sizes[image][1]}" alt="{escape(caption)}" loading="lazy"></a><figcaption>{caption}</figcaption></figure>' for image, caption in p['gallery'])
    related = link(p['related'][0], p['related'][1], external=True) if p['related'] else ''
    next_p = PROJECTS[(PROJECTS.index(p) + 1) % len(PROJECTS)]
    return f'''<a class="text-link breadcrumb" href="portfolio.html">← Portfolio</a>
<header class="case-header"><p class="eyebrow">{p['meta']}</p><h1>{p['title']}</h1><p class="lead">{p['description']}</p>{tags(p['tags'])}</header>
<div class="case-hero">{project_visual(p)}</div>
<dl class="case-facts"><div><dt>Context</dt><dd>{p['context']}</dd></div><div><dt>Practice</dt><dd>{p['role']}</dd></div><div><dt>Tools &amp; methods</dt><dd>{p['tools']}</dd></div></dl>
<section class="case-question"><p class="eyebrow">The question</p><h2>{p['question']}</h2><p>{p['introduction']}</p></section>
<div class="case-body">{sections}</div>
<section class="section" aria-labelledby="film-title"><div class="section-head"><div><p class="eyebrow">In motion</p><h2 id="film-title">Watch the project.</h2></div>{link('https://www.youtube.com/watch?v=' + p['video'], 'Open on YouTube ↗', external=True)}</div><div class="video-shell" data-video="{p['video']}" data-title="{escape(p['title'])}"><img src="assets/projects/{p['image']}" alt="" loading="lazy"><button class="video-play" type="button" aria-label="Play {escape(p['title'])} project film"><span aria-hidden="true">▶</span> Play project film</button></div><p class="note">The film loads from YouTube when you press play. You can also use the direct link above.</p></section>
<section class="section" aria-label="Project documentation">{gallery}</section>
<section class="case-outcome"><p class="eyebrow">What this project contributes</p><h2>Part of a continuing practice.</h2><p>{p['outcome']}</p>{related}</section>
<nav class="case-next" aria-label="More portfolio projects">{link('portfolio.html', '← All projects')}{link(next_p['page'], 'Next: ' + next_p['title'] + ' ↗')}</nav>'''

PAGES += [(p['page'], p['title'], p['description'], case_study(p)) for p in PROJECTS]

for filename, title, description, content in PAGES:
    active = 'portfolio.html' if filename in {p['page'] for p in PROJECTS} else filename
    navigation = ''.join(f'<a href="{href}"' + (' aria-current="page"' if active == href else '') + f'>{label}</a>' for label, href in NAV)
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{escape(description)}"><meta name="theme-color" content="#fff9ee"><title>{title} — Vicky (Jinman) Zhang</title><link rel="icon" href="assets/favicon-moon-gate.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css"><script src="script.js" defer></script></head>
<body id="top"><a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap header-inner"><a class="brand brand-logo" href="index.html" aria-label="Vicky Zhang, home"><img src="assets/vicky-logo.svg" alt="Vicky — moon gate logo" width="400" height="148"></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-nav">Menu <span aria-hidden="true">＋</span></button><nav class="nav" id="primary-nav" aria-label="Main navigation">{navigation}</nav></div></header>
<main id="main" class="wrap">{content}</main>
<footer class="site-footer"><div class="wrap"><div class="footer-top"><div><p class="eyebrow">A conversation begins here</p><h2>Every heritage story<br>has a next chapter.</h2></div><a class="footer-email text-link" href="mailto:{EMAIL}">{EMAIL} ↗</a></div><div class="footer-bottom"><span>© 2026 Jinman Zhang / Vicky · Durham, UK</span><span>Digital storytelling · Cultural heritage · Creative technology</span><a class="back-top" href="#top">Back to top ↑</a></div></div></footer>
</body></html>'''
    (ROOT / filename).write_text(html, encoding='utf-8')
    print(f'Created {filename}')
