import subprocess

APP_TITLE = "ReMarkable Screenshots"


def notify(message: str, title: str = APP_TITLE):
    subprocess.run([
        "osascript", "-e",
        f'display notification "{message}" with title "{title}"'
    ])


def starting_upload():
    notify("📤 Sending your image to the tablet...")


def upload_success():
    notify("✅ All done!\nCheck your tablet.")


def upload_failed(error: str):
    notify(f"❌ Upload went wrong:\n{error}")


def no_image_in_clipboard():
    notify("⚠️ Clipboard is empty.\nCopy an image first!")


def starting_process():
    notify("🖼️ Preparing your image...")