import argparse
import base64
import hashlib
import json
from pathlib import Path

import fitz

def normalize(text):
    return " ".join(text.split())

def compile_package(pdf, manifest):
    cards = []
    with fitz.open(pdf) as document:
        for source in manifest["cards"]:
            page = document[source["page"] - 1]
            crop = fitz.Rect(source["clip"])
            if crop.is_empty or not page.rect.contains(crop):
                raise ValueError(f"Izrezek je zunaj strani: {source['id']}")
            found = normalize(page.get_text())
            if normalize(source["question"]) not in found:
                raise ValueError(f"Vprašanje ni na označeni strani: {source['id']}")
            if normalize(source["question"]) in normalize(page.get_text(clip=crop)):
                raise ValueError(f"Izrezek vključuje vprašanje: {source['id']}")
            bitmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=crop, alpha=False)
            image = "data:image/png;base64," + base64.b64encode(bitmap.tobytes("png")).decode()
            cards.append({key: source[key] for key in ("id", "question", "criteria", "pdfRef", "page")} |
                         {"image": image})
    return {"date": manifest["date"], "pdf": pdf.name,
            "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(), "cards": cards}

if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("pdf", type=Path)
    cli.add_argument("manifest", type=Path)
    cli.add_argument("output", type=Path)
    args = cli.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
    package = compile_package(args.pdf, manifest)
    args.output.write_text(json.dumps(package, ensure_ascii=False), encoding="utf-8")
