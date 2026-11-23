"""Yangilik qo'shish: python yangilik.py
Qayta yig'ish (news.json yoki build.py o'zgargach): python yangilik.py rebuild"""
import json, shutil, sys
from datetime import datetime
from pathlib import Path
import build

ROOT, DB, IMG = build.ROOT, build.ROOT / "news.json", build.ROOT / "images"

def ask_text(label):
    print(label + " (tugatish uchun alohida qatorga nuqta . yozing; bo'sh qoldirish uchun darrov . yozing):")
    lines = []
    while (l := input()) != ".":
        lines.append(l)
    return "\n".join(lines).strip()

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
    items = build.load()
    n = max([i["id"] for i in items], default=0) + 1
    today = datetime.now().strftime("%d.%m.%Y")
    item = {"id": n}
    item["title"] = input("Sarlavha (o'zbekcha): ").strip()
    while True:
        d = input(f"Sana [{today}]: ").strip() or today
        try:
            build.iso(d); break
        except ValueError:
            print("Sana kk.oo.yyyy ko'rinishida bo'lsin, masalan 11.11.2026")
    item["date"] = d
    item["text"] = ask_text("Matn (o'zbekcha)")
    for code, name in (("ru", "Rus"), ("en", "Ingliz")):
        t = input(f"{name} tilida sarlavha (bo'sh = shu tilda chiqmaydi): ").strip()
        if t:
            item["title_" + code] = t
            item["text_" + code] = ask_text(f"{name} tilida matn")
    photo = input("Foto yo'li (bo'sh = fotosiz): ").strip().strip('"')
    if photo:
        item["photo"] = put_photo(photo, n)
    items.append(item)
    DB.write_text(json.dumps(items, ensure_ascii=False, indent=2), "utf-8")
    print("\nHostingga yuklang: yangiliklar/, ru/, en/ papkalari, index.html" + (f", {item['photo']}" if photo else ""))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "rebuild":
        build.build()
    else:
        add()
        build.build()
