import asyncio
import re

from typing import List, Dict, Any
from playwright.async_api import async_playwright

from utils.constants import MAX_PRODUCTS_PER_SOURCE
from utils.helpers import normalize_price


class FlipkartService:

    async def _scrape_products(self, query: str) -> List[Dict[str, Any]]:
        """Scrape products from Flipkart using Playwright."""

        products: List[Dict[str, Any]] = []

        query = query.strip()

        if not query:
            return products

        async with async_playwright() as p:

            browser = await p.chromium.launch(headless=True)

            page = await browser.new_page(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0 Safari/537.36"
                )
            )

            await page.goto(
                f"https://www.flipkart.com/search?q={query}",
                wait_until="networkidle",
            )

            # Close login popup if present
            try:
                await page.locator("button:has-text('✕')").click(timeout=3000)
            except Exception:
                pass

            cards = await page.locator("div[data-id]").all()

            for card in cards[:MAX_PRODUCTS_PER_SOURCE]:

                try:

                    text = await card.inner_text()

                    lines = [
                        line.strip()
                        for line in text.split("\n")
                        if line.strip()
                    ]

                    if not lines:
                        continue

                    name = lines[0]

                    # ---------------- Price ----------------

                    price_match = re.search(r"₹[\d,]+", text)

                    price = (
                        normalize_price(price_match.group())
                        if price_match
                        else 0.0
                    )

                    # ---------------- Rating ----------------

                    rating_match = re.search(r"\b([0-5]\.?[0-9]?)\b", text)

                    rating = (
                        float(rating_match.group(1))
                        if rating_match
                        else 0.0
                    )

                    # ---------------- Reviews ----------------

                    reviews_match = re.search(
                        r"([\d,]+)\s+Ratings",
                        text,
                        re.IGNORECASE,
                    )

                    reviews = (
                        int(reviews_match.group(1).replace(",", ""))
                        if reviews_match
                        else 0
                    )

                    # ---------------- Delivery ----------------

                    delivery_match = re.search(
                        r"(Free delivery.*|Delivery.*|Tomorrow.*|Today.*)",
                        text,
                        re.IGNORECASE,
                    )

                    delivery = (
                        delivery_match.group(1).strip()
                        if delivery_match
                        else ""
                    )

                    # ---------------- Image ----------------

                    image = await card.locator("img").first.get_attribute("src")

                    # ---------------- URL ----------------

                    href = ""

                    links = await card.locator("a").all()

                    for link in links:
                        candidate = await link.get_attribute("href")
                        if candidate:
                            href = candidate
                            break

                    if href and not href.startswith("http"):
                        href = "https://www.flipkart.com" + href

                    # ---------------- Product Dictionary ----------------

                    product: Dict[str, Any] = {
                        "name": name,
                        "price": price,
                        "rating": rating,
                        "reviews": reviews,
                        "delivery_info": delivery,
                        "brand": "",
                        "specifications": {},
                        "seller": "Flipkart",
                        "source": "Flipkart",
                        "url": href,
                        "image_url": image or "",
                    }

                    products.append(product)

                except Exception as e:
                    print(f"Flipkart Error: {e}")
                    continue

            await browser.close()

        return products

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search products from Flipkart."""
        return asyncio.run(self._scrape_products(query))