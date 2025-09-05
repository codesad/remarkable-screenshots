import subprocess
import time
from pathlib import Path

from notifications import upload_success


def rmapi_ls(dest: str = "/") -> str:
    try:
        result = subprocess.run(
            ["rmapi", "ls", dest],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ""


def rmapi_remove(title: str, dest: str = "/"):
    print(f"[~] Removing existing {title} from reMarkable...")
    subprocess.run(["rmapi", "rm", title], check=False)
    subprocess.run(["rmapi", "ls", dest], check=False)  # refresh tree


def rmapi_put(rm_path: Path, dest: str = "/"):
    subprocess.run(
        ["rmapi", "put", str(rm_path), dest],
        capture_output=True, text=True, check=True
    )


def upload_with_retries(rm_path: Path, doc_title: str, dest: str = "/", max_retries=6, delay_sec=1.5):
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Uploading {doc_title} to reMarkable... (attempt {attempt}/{max_retries})")
            rmapi_put(rm_path, dest)
            print(f"Sent {doc_title} to reMarkable")
            upload_success()
            return
        except subprocess.CalledProcessError as e:
            out = (e.stdout or "") + (e.stderr or "")
            if "entry already exists" in out.lower():
                print("Entry already exists, removing and retrying...")
                rmapi_remove(doc_title, dest)
                time.sleep(delay_sec)
                continue
            raise
    raise RuntimeError(f"Failed to upload {doc_title} after {max_retries} attempts.")


def send_to_remarkable(rm_path: Path, dest: str = "/"):
    if not rm_path.exists():
        raise FileNotFoundError(f"RM file not found: {rm_path}")

    doc_title = rm_path.stem

    if doc_title in rmapi_ls(dest):
        rmapi_remove(doc_title, dest)

    upload_with_retries(rm_path, doc_title, dest)