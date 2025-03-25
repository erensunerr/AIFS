from langchain_core.tools import tool
from bs4 import BeautifulSoup
import asyncio
from playwright.async_api import async_playwright
import logging
from .describe_image import describe_image

logger = logging.getLogger(__name__)

@tool
def link_clothing_description_tool(link: str) -> str:
    """
    Given a url / link to a clothing item, this tool returns a description.
    """
    logger.info(f"Starting to scrape clothing description from: {link}")
    print("LINK _CLTHING")
    async def scrape_page(url):
        async with async_playwright() as p:
            logger.info("Launching webkit browser")
            browser = await p.webkit.launch(headless=False)  # use Safari engine
            logger.info("Opening new page")
            page = await browser.new_page()
            logger.info(f"Navigating to URL: {url}")
            await page.goto(url, timeout=20000)
            logger.info("Taking screenshot")
            await page.screenshot(path="temp/test.png")
            logger.info("Getting page content")
            content = await page.content()
            logger.info("Closing browser")
            await browser.close()
            logger.debug(f"Content length: {len(content)} characters")
            logger.info("Page content retrieved successfully")
            return content
    try:
        html = asyncio.run(scrape_page(link))
        description = describe_image("temp/test.png")
        return description
    except Exception as e:
        logger.error(f"Failed to scrape page: {str(e)}", exc_info=True)
        return f"❌ Failed to scrape page: {e}"
