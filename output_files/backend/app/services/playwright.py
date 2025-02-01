# backend/app/services/playwright.py
import os

from playwright.sync_api import sync_playwright

from backend.app.core.config import settings
from backend.app.core.llm import generate_text
from backend.app.core.utils import get_current_time


async def run_playwright_task(task_definition: dict, user: str):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            if "url" not in task_definition:
                return {"message": "No URL defined"}
            url = task_definition["url"]
            await page.goto(url)
            if "selector" in task_definition:
                selector = task_definition["selector"]
                content = page.locator(selector).text_content()
                browser.close()
                return {
                    "message": f"Content extracted: {content} from {url} at {get_current_time()}"
                }
            else:
                browser.close()
                return {
                    "message": f"No selector provided for {url} at {get_current_time()}"
                }
    except Exception as e:
        return {"message": f"An error occurred: {e}"}
