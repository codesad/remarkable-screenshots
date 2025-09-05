from PIL import ImageEnhance, Image


def boost_contrast(img: Image.Image, factor: float = 1.6) -> Image.Image:
    return ImageEnhance.Contrast(img).enhance(factor)


def _bw_by_lightness(img: Image.Image, threshold: int = 100) -> Image.Image:
    gray = img.convert("L")
    bw = gray.point(lambda v: 0 if v < threshold else 255, mode="L")
    return bw.convert("RGB")
