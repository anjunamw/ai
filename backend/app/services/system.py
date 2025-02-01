# backend/app/services/system.py
import os
import shlex
import subprocess

from backend.app.core.config import settings
from backend.app.core.llm import generate_text
from backend.app.core.utils import get_current_time


async def install_package(package_name: str, user: str) -> str:
    ALLOWED_PACKAGES = ["nano", "vim"]  # example
    if package_name not in ALLOWED_PACKAGES:
        return f"Package '{package_name}' is not in allowed packages."
    try:
        command = [
            "sudo",
            "apt-get",
            "install",
            package_name,
            "-y",
        ]  # -y for non-interactive install
        process = subprocess.run(
            command, capture_output=True, text=True, check=True
        )  # check=True raises exception on non-zero exit code
        return f"Package '{package_name}' installed successfully."
    except subprocess.CalledProcessError as e:
        return f"Error installing package '{package_name}': {e.stderr}"
    except FileNotFoundError:
        return "Error: apt-get command not found (not a Debian/Ubuntu system?)."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


async def start_realtime(user: str) -> str:
    return f"Realtime capture started at {get_current_time()}"


async def stop_realtime(user: str) -> str:
    return f"Realtime capture stopped at {get_current_time()}"
