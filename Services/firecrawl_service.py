from firecrawl import Firecrawl
from pydantic import BaseModel, Field

from typing import List, Dict, Any, Optional
from utils.config import Settings
from utils.constants import MAX_PRODUCTS_PER_SOURCE
from utils.helpers import normalize_price

class ExtractedProduct(BaseModel):
    name: str = Field(description="Product name/title")
    price: str = Field(description="Product price as shown on the page, e.g. '₹1,299'")
    rating: Optional[float] = Field(default=0, description="Star rating out of 5, 0 if not shown")
    reviews: Optional[int] = Field(default=0, description="Number of reviews/ratings, 0 if not shown")
    delivery_info: Optional[str] = Field(default="", description="Delivery/shipping text shown on the page, as a single string")
    brand: Optional[str] = Field(default="", description="Brand name if shown")
    image_url: Optional[str] = Field(default="", description="Main product image URL")
    url: Optional[str] = Field(default="", description="Product page URL")


class ExtractedProductList(BaseModel):
    products: List[ExtractedProduct] = Field(description="List of products found on the search results page")

class FirecrawlService:

    STORES = {
        "Reliance Digital": "https://www.reliancedigital.in/search?q={query}"
    }

    def __init__(self):
        self.app = Firecrawl(api_key=Settings().FIRECRAWL_API_KEY)

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search products from Croma and Reliance Digital."""

        products: List[Dict[str, Any]] = []

        query = query.strip().replace(" ", "%20")

        if not query:
            return products

        for store, url_template in self.STORES.items():
            url = url_template.format(query=query)

            try:
                scrape_kwargs = {
                    "url": url,
                    "formats": [
                        {
                            "type": "json",
                            "schema": ExtractedProductList,
                            "prompt": (
                                "Extract every product listed on this e-commerce search "
                                "results page, including its name, price, rating, number "
                                "of reviews, delivery/shipping text, brand, main image URL, "
                                "and the product page URL."
                            ),
                        }
                    ],
                }

                if store == "Reliance Digital":
                    scrape_kwargs["actions"] = [
                        {"type": "wait", "milliseconds": 3000},
                        {"type": "click", "selector": "input[placeholder*='Search' i]"},
                        {"type": "write", "text": query},
                        {"type": "press", "key": "Enter"},
                        {"type": "wait", "milliseconds": 5000},
                    ]

                result = self.app.scrape(**scrape_kwargs)

                if not result or not getattr(result, "json", None):
                    continue

                extracted = result.json
                product_list = extracted.get("products", []) if isinstance(extracted, dict) else []

                for item in product_list[:MAX_PRODUCTS_PER_SOURCE]:

                    raw_delivery = item.get("delivery_info", "")
                    if isinstance(raw_delivery, list):
                        delivery_info = ", ".join(str(v) for v in raw_delivery if v)
                    elif raw_delivery is None:
                        delivery_info = ""
                    else:
                        delivery_info = str(raw_delivery)

                    raw_reviews = item.get("reviews", 0)
                    if isinstance(raw_reviews, list):
                        raw_reviews = raw_reviews[0] if raw_reviews else 0
                    try:
                        reviews = int(raw_reviews or 0)
                    except (ValueError, TypeError):
                        reviews = 0

                    product: Dict[str, Any] = {
                        "name": str(item.get("name", "Unknown Product")),
                        "price": normalize_price(item.get("price", "")),
                        "rating": float(item.get("rating", 0) or 0),
                        "reviews": reviews,
                        "delivery_info": delivery_info,
                        "brand": str(item.get("brand", "") or ""),
                        "specifications": {},
                        "seller": store,
                        "source": store,
                        "url": item.get("url", ""),
                        "image_url": item.get("image_url", "")
                    }

                    products.append(product)

            except Exception as e:
                print(f"Firecrawl Error ({store}): {e}")
                continue

        return products