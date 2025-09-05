import subprocess
from pathlib import Path
from typing import Any

from PIL import Image

from dimensions import RESOLUTION, DOTS_PER_INCH


def preprocess_image(image_file: str) -> tuple[Path, tuple[Any, Any]]:
    tw, th = RESOLUTION
    img_path = Path(image_file)
    if not img_path.exists():
        raise FileNotFoundError(f"Image not found: {image_file}")

    img = Image.open(img_path).convert("RGB")

    # img = boost_contrast(img, 2.0)
    # img = _bw_by_lightness(img, threshold=100)

    w0, h0 = img.size
    scale = min(tw / w0, th / h0)

    new_w = max(1, min(tw - 1, int(round(w0 * scale))))
    new_h = max(1, min(th - 1, int(round(h0 * scale))))

    if (new_w, new_h) != (w0, h0):
        img = img.resize((new_w, new_h), Image.LANCZOS)

    w, h = img.size
    print(w, h)

    canvas = Image.new("RGB", (tw, th), "white")

    canvas.paste(img, (0, 0))

    pdf_path = img_path.with_suffix(".pdf")
    canvas.save(pdf_path, "PDF", dpi=DOTS_PER_INCH)

    print(f"Preprocessed {img_path} -> {pdf_path}, canvas {(tw, th)}, pasted at top-left")
    return pdf_path, (tw, th)


def make_rm_from_image(image_file: str) -> Path:
    pdf_path, size = preprocess_image(image_file)

    out_file = Path(image_file).with_suffix(".rmdoc")

    scale = 75
    dpc = 104.43
    hcl_width = 1/dpc * size[0] * 10 / (scale / 100)
    hcl_height = 1/dpc * size[1] * 10 / (scale / 100)

    mul = (1 - scale / 100)

    center_offset = -(hcl_width / 2) * mul
    height_offset = -60 * mul

    hcl_file = pdf_path.with_suffix(".hcl")
    hcl_content = f"""
    unitlength [{1/dpc}] m
    image {pdf_path.resolve()} 1 {center_offset} {height_offset} {scale}
    """
    hcl_file.write_text(hcl_content, encoding="utf-8")

    print(f"Created wrapper: {hcl_file}")
    cmd = ["drawj2d", "-Trmdoc", "-W157", "-H209", str(hcl_file), "-o", str(out_file)]
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"Created {out_file}")
    return out_file
