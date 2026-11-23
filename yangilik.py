"""Yangilik qo'shish: python yangilik.py
Qayta yig'ish (news.json qo'lda tahrirlangach): python yangilik.py rebuild"""
import html, json, re, shutil, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
DB, IMG = ROOT / "news.json", ROOT / "images"
esc = html.escape

def load():
    return json.loads(DB.read_text("utf-8")) if DB.exists() else []

def iso(d):
    return datetime.strptime(d, "%d.%m.%Y").strftime("%Y-%m-%d")

def paras(t):
    return "".join(f"<p>{esc(p.strip())}</p>\n" for p in re.split(r"\n\s*\n", t.strip()) if p.strip())

def excerpt(t):
    first = re.split(r"\n\s*\n", t.strip())[0].strip()
    return first if len(first) <= 160 else first[:157].rsplit(" ", 1)[0] + "..."

def card(n):
    thumb = f'<img class="thumb" src="/{n["photo"]}" alt="">' if n.get("photo") else ""
    return (f'<article>\n<time datetime="{iso(n["date"])}">{n["date"]}</time>\n'
            f'<div><h3><a href="/yangiliklar/{n["id"]}/">{esc(n["title"])}</a></h3>'
            f'<p>{esc(excerpt(n["text"]))}</p>{thumb}</div>\n</article>')

def replace_block(path, inner):
    s = path.read_text("utf-8")
    s = re.sub(r"<!--NEWS-START-->.*?<!--NEWS-END-->",
               lambda m: f"<!--NEWS-START-->\n{inner}\n<!--NEWS-END-->", s, flags=re.S)
    path.write_text(s, "utf-8")

def build():
    items = sorted(load(), key=lambda n: (iso(n["date"]), n["id"]), reverse=True)
    nd = ROOT / "yangiliklar"
    replace_block(nd / "index.html", "\n".join(card(n) for n in items))
    replace_block(ROOT / "index.html", "\n".join(card(n) for n in items[:3]))
    s = (nd / "index.html").read_text("utf-8")
    head, tail = s[:s.index("<main>") + 6], s[s.index("</main>"):]
    keep = set()
    for n in items:
        img = f'<img src="/{n["photo"]}" alt="{esc(n["title"])}">\n' if n.get("photo") else ""
        body = (f'\n<div class="pagehead"><div class="wrap"><h1>{esc(n["title"])}</h1></div></div>\n'
                f'<section>\n<div class="wrap post">\n<time datetime="{iso(n["date"])}">{n["date"]}</time>\n'
                f'{img}{paras(n["text"])}<a class="more" href="/yangiliklar/">Barça yangiliklar</a>\n'
                f'</div>\n</section>\n')
        h = head.replace("<title>Yangiliklar |", f"<title>{esc(n['title'])} |")
        d = nd / str(n["id"])
        d.mkdir(exist_ok=True)
        keep.add(d.name)
        (d / "index.html").write_text(h + body + tail, "utf-8")
    for d in nd.iterdir():
        if d.is_dir() and d.name.isdigit() and d.name not in keep:
            shutil.rmtree(d)
    return items

def put_photo(src, n):
    IMG.mkdir(exist_ok=True)
    try:
        from PIL import Image
        dst = IMG / f"yangilik-{n}.jpg"
        im = Image.open(src).convert("RGB")
        im.thumbnail((1400, 1400))
        im.save(dst, "JPEG", quality=82)
    except ImportError:
        dst = IMG / f"yangilik-{n}{Path(src).suffix.lower()}"
        shutil.copy(src, dst)
    return "images/" + dst.name

def add():
    items = load()
    n = max([i["id"] for i in items], default=0) + 1
    title = input("Sarlavha: ").strip()
    today = datetime.now().strftime("%d.%m.%Y")
    while True:
        d = input(f"Sana [{today}]: ").strip() or today
        try:
            iso(d); break
        except ValueError:
            print("Sana kk.oo.yyyy ko'rinishida bo'lsin, masalan 11.11.2026")
    print("Matn (tugatish uchun alohida qatorga nuqta . yozing):")
    lines = []
    while (l := input()) != ".":
        lines.append(l)
    photo = input("Foto yo'li (bo'sh = fotosiz): ").strip().strip('"')
    item = {"id": n, "date": d, "title": title, "text": "\n".join(lines)}
    if photo:
        item["photo"] = put_photo(photo, n)
    items.append(item)
    DB.write_text(json.dumps(items, ensure_ascii=False, indent=2), "utf-8")
    print(f"\nHostingga yuklang: yangiliklar/{n}/, yangiliklar/index.html, index.html" +
          (f", {item['photo']}" if photo else ""))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "rebuild":
        build()
    else:
        add()
        build()
