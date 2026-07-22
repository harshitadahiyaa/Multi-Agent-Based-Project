from firecrawl import Firecrawl

from typing import List, Dict, Any
from utils.config import Settings
from utils.constants import MAX_PRODUCTS_PER_SOURCE
from utils.helpers import normalize_price


class FirecrawlService:

    STORES = {
        "Croma": "https://www.croma.com/searchB?q={query}",
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
                result = self.app.scrape_url(
                    url,
                    {
                        "extractorOptions": {
                            "mode": "llm-extraction",
                            "extractionSchema": {
                                "type": "object",
                                "properties": {
                                    "products": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "name": {
                                                    "type": "string"
                                                },
                                                "price": {
                                                    "type": "string"
                                                },
                                                "rating": {
                                                    "type": "number"
                                                },
                                                "image_url": {
                                                    "type": "string"
                                                },
                                                "url": {
                                                    "type": "string"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                )

                if not result:
                    continue

                extracted = result.get("llm_extraction", {})
                product_list = extracted.get("products", [])

                for item in product_list[:MAX_PRODUCTS_PER_SOURCE]:

                    product: Dict[str, Any] = {
                        "name": item.get("name", "Unknown Product"),
                        "price": normalize_price(item.get("price", "")),
                        "rating": float(item.get("rating", 0) or 0),
                        "reviews": int(item.get("reviews", 0) or 0),
                        "delivery_info": item.get("delivery_info", ""),
                        "brand": item.get("brand", ""),
                        "specifications": item.get("specifications", {}),
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