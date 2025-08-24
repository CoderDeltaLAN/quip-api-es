#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

import pytesseract
from PIL import Image
from unidecode import unidecode

ROOT = Path("/home/user/Proyectos/quip-api-es")
RAW = ROOT / "raw_pins"
OUT = ROOT / "data" / "quotes_es.json"


def normalize_text(s: str) -> str:
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def split_author(text: str):
    # heurística simple: frases tipo '..." — Autor' o '..." - Autor'
    m = re.search(r"[\-—]\s*([^\\-—]{2,120})$", text)
    if m and len(text) > 20:
        body = text[: m.start()].strip().strip("-— ").strip()
        author = m.group(1).strip()
        if 2 <= len(author) <= 120 and len(body) >= 6:
            return body, author
    return text, None


def load_existing():
    if OUT.exists():
        return json.loads(OUT.read_text(encoding="utf-8"))
    return []


def main():
    dataset = load_existing()
    seen = set((unidecode(d["texto"]).lower(), (d.get("autor") or "").lower()) for d in dataset)
    added = 0

    for img_path in sorted(RAW.glob("*")):
        if img_path.suffix.lower() not in {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
            ".bmp",
            ".tif",
            ".tiff",
        }:
            continue
        try:
            img = Image.open(img_path)
            text = pytesseract.image_to_string(img, lang="spa+eng").strip()
            text = normalize_text(text)
            if len(text) < 8:
                continue
            texto, autor = split_author(text)
            k = (unidecode(texto).lower(), (autor or "").lower())
            if k in seen:
                continue
            item = {
                "texto": texto,
                "autor": autor,
                "categoria": "otro",
                "fuente_url": None,
                "licencia": "desconocida",
            }
            dataset.append(item)
            seen.add(k)
            added += 1
        except Exception as e:
            print(f"[WARN] {img_path.name}: {e}", file=sys.stderr)

    OUT.write_text(json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: añadidas {added} frases. Total: {len(dataset)}")


if __name__ == "__main__":
    main()
