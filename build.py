"""Saytni 3 tilda (uz, ru, en) yig'adi: python build.py"""
import html, json, re, shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
FACEBOOK = "FACEBOOK_HAVOLA"            # Facebook sahifa havolasini shu yerga yozing
TELEGRAM = "https://t.me/rsteiam_tvf"
INSTAGRAM = "https://www.instagram.com/rsteiam_tvf/"
TEL, PHONE = "tel:+998555159645", "55-515-96-45"
LANGS = ["uz", "ru", "en"]
LANGNAME = {"uz": "Özbekça", "ru": "Русский", "en": "English"}
KEYS = ["home", "about", "services", "news", "contact"]
SLUG = {"uz": dict(home="", about="haqida", services="xizmatlar", news="yangiliklar", contact="aloqa"),
        "ru": dict(home="", about="o-filiale", services="uslugi", news="novosti", contact="kontakty"),
        "en": dict(home="", about="about", services="services", news="news", contact="contact")}

T = {
"uz": dict(
  nav=dict(home="Boş sahifa", about="Taşkilot haqida", services="Xizmatlar", news="Yangiliklar", contact="Aloqa"),
  b1="Respublika sud-tibbiy ekspertiza ilmiy-amaliy markazi", b2="Toşkent viloyat filiali",
  eyebrow="Özbekiston Respublikasi", hero="Filialda sud-tibbiy ekspertizalar ötkaziladi.",
  addr_l="Manzil", hours_l="Iş vaqti", phone_l="Telefon", mail_l="E-mail",
  addr="100037, Toşkent şahar, Mirzo Uluğbek tumani, Alişerobod MFY, Nurli zamin, 6A",
  hours="8:30 dan 17:00 gaça", theme="Yoruğ / qoronği rejim", callc="(call-markaz)", soon="Tez orada kiritiladi",
  sec="Bölimlar", latest="Sönggi yangiliklar", more="Barça yangiliklar", call="Qönğiroq qilish",
  tdesc=dict(about="Filial faoliyati haqida qisqaça ma'lumot.", services="Filialda ötkaziladigan ekspertiza turlari.",
             news="Filial yangiliklari va e'lonlari.", contact="Manzil, iş vaqti va aloqa ma'lumotlari."),
  about_p=["Respublika sud-tibbiy ekspertiza ilmiy-amaliy markazining Toşkent viloyat filiali sud-tibbiy ekspertizalarni ötkazadi.",
           "Filial Toşkent şahridagi Mirzo Uluğbek tumanida joylaşgan."],
  svc=[("Tirik şaxslar ekspertizasi", "Tan jarohatlari va soğliqqa yetkazilgan zarar darajasini aniqlaş."),
       ("Murda ekspertizasi", "Ölim sababi va holatlarini sud-tibbiy jihatdan aniqlaş."),
       ("Laboratoriya tekşiruvlari", "Ekspertiza uçun zarur laboratoriya tahlillari."),
       ("Komission ekspertizalar", "Murakkab holatlarda bir neça mutaxassis iştirokida ötkaziladigan ekspertizalar.")]),
"ru": dict(
  nav=dict(home="Главная", about="О филиале", services="Услуги", news="Новости", contact="Контакты"),
  b1="Республиканский научно-практический центр судебно-медицинской экспертизы", b2="Ташкентский областной филиал",
  eyebrow="Республика Узбекистан", hero="В филиале проводятся судебно-медицинские экспертизы.",
  addr_l="Адрес", hours_l="Режим работы", phone_l="Телефон", mail_l="E-mail",
  addr="100037, г. Ташкент, Мирзо-Улугбекский район, махалля Алишеробод, Нурли замин, 6А",
  hours="с 8:30 до 17:00", theme="Светлая / тёмная тема", callc="(колл-центр)", soon="Будет добавлен позже",
  sec="Разделы", latest="Последние новости", more="Все новости", call="Позвонить",
  tdesc=dict(about="Краткая информация о деятельности филиала.", services="Виды проводимых экспертиз.",
             news="Новости и объявления филиала.", contact="Адрес, режим работы и контактные данные."),
  about_p=["Ташкентский областной филиал Республиканского научно-практического центра судебно-медицинской экспертизы проводит судебно-медицинские экспертизы.",
           "Филиал расположен в Мирзо-Улугбекском районе города Ташкента."],
  svc=[("Экспертиза живых лиц", "Установление степени телесных повреждений и вреда, причинённого здоровью."),
       ("Экспертиза трупов", "Установление причины и обстоятельств смерти с судебно-медицинской точки зрения."),
       ("Лабораторные исследования", "Лабораторные анализы, необходимые для проведения экспертиз."),
       ("Комиссионные экспертизы", "Экспертизы, проводимые с участием нескольких специалистов в сложных случаях.")]),
"en": dict(
  nav=dict(home="Home", about="About the branch", services="Services", news="News", contact="Contact"),
  b1="Republican Scientific and Practical Center of Forensic Medical Examination", b2="Tashkent Regional Branch",
  eyebrow="Republic of Uzbekistan", hero="The branch carries out forensic medical examinations.",
  addr_l="Address", hours_l="Working hours", phone_l="Phone", mail_l="E-mail",
  addr="100037, Tashkent, Mirzo Ulugbek district, Alisherobod mahalla, Nurli zamin, 6A",
  hours="8:30 to 17:00", theme="Light / dark mode", callc="(call center)", soon="Coming soon",
  sec="Sections", latest="Latest news", more="All news", call="Call us",
  tdesc=dict(about="A brief overview of the branch's activities.", services="Types of examinations carried out.",
             news="News and announcements of the branch.", contact="Address, working hours and contact details."),
  about_p=["The Tashkent Regional Branch of the Republican Scientific and Practical Center of Forensic Medical Examination carries out forensic medical examinations.",
           "The branch is located in the Mirzo Ulugbek district of Tashkent."],
  svc=[("Examination of living persons", "Determining the nature of bodily injuries and the degree of harm caused to health."),
       ("Post-mortem examination", "Establishing the cause and circumstances of death from a forensic medical standpoint."),
       ("Laboratory testing", "Laboratory analyses required for examinations."),
       ("Commission examinations", "Examinations in complex cases carried out with the participation of several specialists.")]),
}

IC = {
 "call": '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
 "tg": '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>',
 "ig": '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>',
 "fb": '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>'}

esc = html.escape
MOON = '<svg class="ic ic-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
SUN = '<svg class="ic ic-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'
HEAD_JS = '<script>try{if(localStorage.getItem("theme")==="dark")document.documentElement.dataset.theme="dark"}catch(e){}</script>'
THEME_JS = """<script>
(function(){var b=document.getElementById("theme");if(!b)return;
var d=document.documentElement;b.setAttribute("aria-pressed",d.dataset.theme==="dark");
b.addEventListener("click",function(){var n=d.dataset.theme==="dark"?"light":"dark";d.dataset.theme=n;
try{localStorage.setItem("theme",n)}catch(e){}b.setAttribute("aria-pressed",n==="dark")});})();
</script>"""
PTITLE = {"uz": "Foydali havolalar", "ru": "Полезные ссылки", "en": "Useful links"}
def find_img(name):
    for ext in ("jpg", "jpeg", "png", "webp"):
        if (ROOT / "images" / f"{name}.{ext}").exists():
            return f"/images/{name}.{ext}"
def banner(key):
    u = find_img("bolim-" + key)
    return f'<div class="wrap bannerwrap"><img class="banner" src="{u}" alt=""></div>\n' if u else ""
def tile_img(key):
    u = find_img("bolim-" + key)
    return f'<img src="{u}" alt="">' if u else ""
def partners(L):
    p = ROOT / "links.json"
    items = json.loads(p.read_text("utf-8")) if p.exists() else []
    if not items:
        return ""
    out = []
    for i in items:
        ok = i.get("image") and (ROOT / i["image"]).exists()
        inner = f'<img src="/{i["image"]}" alt="{esc(i["name"])}">' if ok else esc(i["name"])
        out.append(f'<a href="{i["url"]}" target="_blank" rel="noopener" title="{esc(i["name"])}">{inner}</a>')
    return (f'<div class="partners">\n<div class="wrap">\n<h2>{PTITLE[L]}</h2>\n<div class="plist">\n' + "\n".join(out) + '\n</div>\n</div>\n</div>')
def url(L, key, nid=None):
    base = "" if L == "uz" else "/" + L
    s = SLUG[L][key]
    return (base + "/" if not s else f"{base}/{s}/") + (f"{nid}/" if nid else "")
def cur(c): return ' aria-current="page"' if c else ""
def iso(d): return datetime.strptime(d, "%d.%m.%Y").strftime("%Y-%m-%d")
def load(): return json.loads((ROOT / "news.json").read_text("utf-8")) if (ROOT / "news.json").exists() else []
def view(n, L):
    if L == "uz": return n["title"], n["text"]
    t, x = n.get("title_" + L), n.get("text_" + L)
    return (t, x) if t and x else None
def paras(t): return "".join(f"<p>{esc(p.strip())}</p>\n" for p in re.split(r"\n\s*\n", t.strip()) if p.strip())
def excerpt(t):
    f = re.split(r"\n\s*\n", t.strip())[0].strip()
    return f if len(f) <= 160 else f[:157].rsplit(" ", 1)[0] + "..."
def card(n, L):
    title, text = view(n, L)
    th = f'<img class="thumb" src="/{n["photo"]}" alt="">' if n.get("photo") else ""
    return (f'<article>\n<time datetime="{iso(n["date"])}">{n["date"]}</time>\n<div><h3><a href="{url(L, "news", n["id"])}">'
            f'{esc(title)}</a></h3><p>{esc(excerpt(text))}</p>{th}</div>\n</article>')
def write(u, content):
    d = ROOT / u.strip("/")
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(content, "utf-8")

def page(L, key, title, body, alt):
    S = T[L]
    org = S["b1"] + " " + S["b2"]
    nav = "".join(f'<a href="{url(L, k)}"{cur(k == key)}>{S["nav"][k]}</a>' for k in KEYS)
    lang = "".join(f'<a href="{alt[l]}" hreflang="{l}" lang="{l}" aria-label="{LANGNAME[l]}"{cur(l == L)}>{l.upper()}</a>' for l in LANGS)
    links = [("call", TEL, S["call"], ""), ("tg", TELEGRAM, "Telegram", " target=\"_blank\" rel=\"noopener\""),
             ("ig", INSTAGRAM, "Instagram", " target=\"_blank\" rel=\"noopener\""), ("fb", FACEBOOK, "Facebook", " target=\"_blank\" rel=\"noopener\"")]
    icons = "".join(f'<a href="{h}"{e} aria-label="{t}">{IC[k]}</a>' for k, h, t, e in links)
    return f'''<!DOCTYPE html>
<html lang="{L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | {esc(org)}</title>
<meta name="description" content="{esc(org)}. {esc(S["hero"])}">
<link rel="icon" href="/logo.png">
<link rel="stylesheet" href="/style.css">
{HEAD_JS}
</head>
<body>
<header>
<div class="wrap">
<a class="brand" href="{url(L, "home")}"><img src="/logo.png" alt="Logo"><span>{S["b1"]}<br>{S["b2"]}</span></a>
<nav aria-label="Menu">{nav}</nav>
<div class="tools"><div class="lang">{lang}</div><button type="button" id="theme" class="theme" aria-label="{S["theme"]}" title="{S["theme"]}">{MOON}{SUN}</button></div>
</div>
</header>
<main>
{body}
</main>
{partners(L)}
<footer>
<div class="wrap foot"><span>© 2026 {esc(org)}</span><div class="flinks">{icons}</div></div>
</footer>
{THEME_JS}
</body>
</html>
'''

def head(t): return f'<div class="pagehead"><div class="wrap"><h1>{esc(t)}</h1></div></div>'

def build():
    items = sorted(load(), key=lambda n: (iso(n["date"]), n["id"]), reverse=True)
    for L in LANGS:
        S = T[L]
        alt = lambda key: {l: url(l, key) for l in LANGS}
        mine = [n for n in items if view(n, L)]
        home_news = ""
        if mine:
            home_news = (f'<section class="news">\n<div class="wrap">\n<h2>{S["latest"]}</h2>\n' + "\n".join(card(n, L) for n in mine[:3]) +
                         f'\n<a class="more" href="{url(L, "news")}">{S["more"]}</a>\n</div>\n</section>')
        tiles = "\n".join(f'<a href="{url(L, k)}">{tile_img(k)}<h3>{S["nav"][k]}</h3><p>{S["tdesc"][k]}</p></a>' for k in KEYS[1:])
        hu = find_img("hero")
        hero_img = f'<img class="photo" src="{hu}" alt="">' if hu else '<img src="/logo.png" alt="Logo">'
        home = f'''<div class="hero">
<div class="wrap">
<div>
<small>{S["eyebrow"]}</small>
<h1>{S["b1"]} {S["b2"]}</h1>
<p>{S["hero"]}</p>
<a class="btn" href="{url(L, "services")}">{S["nav"]["services"]}</a><a class="btn alt" href="{url(L, "contact")}">{S["nav"]["contact"]}</a>
</div>
{hero_img}
</div>
</div>
<div class="info"><div class="wrap">
<div><span>{S["addr_l"]}</span>{S["addr"]}</div>
<div><span>{S["hours_l"]}</span>{S["hours"]}</div>
</div></div>
<section>
<div class="wrap">
<h2>{S["sec"]}</h2>
<div class="tiles">
{tiles}
</div>
</div>
</section>
{home_news}'''
        write(url(L, "home"), page(L, "home", S["nav"]["home"], home, alt("home")))
        about = head(S["nav"]["about"]) + banner("about") + '\n<section class="about">\n<div class="wrap">\n' + "".join(f"<p>{p}</p>\n" for p in S["about_p"]) + '</div>\n</section>'
        write(url(L, "about"), page(L, "about", S["nav"]["about"], about, alt("about")))
        svc = head(S["nav"]["services"]) + banner("services") + '\n<section class="services">\n<div class="wrap">\n<ul>\n' + "\n".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in S["svc"]) + '\n</ul>\n</div>\n</section>'
        write(url(L, "services"), page(L, "services", S["nav"]["services"], svc, alt("services")))
        news = head(S["nav"]["news"]) + banner("news") + '\n<section class="news">\n<div class="wrap">\n' + "\n".join(card(n, L) for n in mine) + '\n</div>\n</section>'
        write(url(L, "news"), page(L, "news", S["nav"]["news"], news, alt("news")))
        contact = head(S["nav"]["contact"]) + banner("contact") + f'''
<section class="contact">
<div class="wrap">
<dl>
<dt>{S["addr_l"]}</dt><dd>{S["addr"]}</dd>
<dt>{S["hours_l"]}</dt><dd>{S["hours"]}</dd>
<dt>{S["phone_l"]}</dt><dd><a href="{TEL}">{PHONE}</a> {S["callc"]}</dd>
<!-- TODO: e-mail -->
<dt>{S["mail_l"]}</dt><dd>{S["soon"]}</dd>
</dl>
</div>
</section>'''
        write(url(L, "contact"), page(L, "contact", S["nav"]["contact"], contact, alt("contact")))
        keep = set()
        for n in mine:
            title, text = view(n, L)
            img = f'<img src="/{n["photo"]}" alt="{esc(title)}">\n' if n.get("photo") else ""
            body = (head(title) + f'\n<section>\n<div class="wrap post">\n<time datetime="{iso(n["date"])}">{n["date"]}</time>\n'
                    f'{img}{paras(text)}<a class="more" href="{url(L, "news")}">{S["more"]}</a>\n</div>\n</section>')
            a = {l: (url(l, "news", n["id"]) if view(n, l) else url(l, "news")) for l in LANGS}
            write(url(L, "news", n["id"]), page(L, "news", title, body, a))
            keep.add(str(n["id"]))
        nd = ROOT / url(L, "news").strip("/")
        for d in nd.iterdir():
            if d.is_dir() and d.name.isdigit() and d.name not in keep:
                shutil.rmtree(d)

if __name__ == "__main__":
    build()
