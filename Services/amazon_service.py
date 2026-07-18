import requests

from models.product import Product
from utils.config import SERPAPI_KEY


class AmazonService:

    def search(self, query):

        url = "https://serpapi.com/search"

        params = {
            "engine": "amazon",
            "k": query,
            "amazon_domain": "amazon.in",
            "api_key": SERPAPI_KEY
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            products = []

            for item in data.get("organic_results", [])[:10]:

                # Get price
                price = 0.0
                if isinstance(item.get("price"), dict):
                    price = float(item["price"].get("value", 0))
                else:
                    try:
                        price = float(str(item.get("price", 0)).replace("₹", "").replace(",", ""))
                    except:
                        price = 0.0

                product = Product(
                    name=item.get("title", "N/A"),
                    price=price,
                    rating=float(item.get("rating", 0)),
                    image=item.get("thumbnail", ""),
                    url=item.get("link", ""),
                    source="Amazon"
                )

                products.append(product)

            return products

        except Exception as e:
            print("Amazon Error:", e)
            return []