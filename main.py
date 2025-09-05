import time
from pathlib import Path
from PIL import ImageGrab

from image_processing import make_rm_from_image
import notifications
from remarkable_api import send_to_remarkable

def clean_up(tmp_file: Path):
    if tmp_file.exists():
        tmp_file.unlink()
    for ext in [".pdf", ".hcl", ".rmdoc"]:
        if tmp_file.with_suffix(ext).exists():
            tmp_file.with_suffix(ext).unlink()

def process_clipboard():
    img = ImageGrab.grabclipboard()
    if img is None:
        print("No image in clipboard.")
        notifications.no_image_in_clipboard()
        return
    notifications.starting_process()

    BASE_DIR = Path(__file__).resolve().parent
    temp_dir = BASE_DIR / "temp"
    try:
        temp_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        notifications.notify(f"Failed to create temp dir: {e}")
        return
    tmp_file = temp_dir / "clipboard.png"

    try:
        img.save(tmp_file)
    except Exception as e:
        notifications.notify(f"Failed to save image to {tmp_file}: {e}")
        return

    print("Got image from clipboard...")
    try:
        make_rm_from_image(str(tmp_file))
        notifications.starting_upload()
        send_to_remarkable(tmp_file.with_suffix(".rmdoc"))
        time.sleep(0.5)
    except Exception as e:
        notifications.upload_failed(str(e))
    finally:
        clean_up(tmp_file)



if __name__ == "__main__":
    process_clipboard()
