from Services.amazon_service import AmazonService
from Services.flipkart_service import FlipkartService
from Services.firecrawl_service import FirecrawlService
from utils.helpers import deduplicate_products


def search_agent(state):

    query = state["query"]

    amazon = AmazonService()
    flipkart = FlipkartService()
    firecrawl = FirecrawlService()

    products = []

    # Search Amazon
    try:
        products.extend(amazon.search(query))
    except:
        print("Amazon search failed")

    # Search Flipkart
    try:
        products.extend(flipkart.search(query))
    except:
        print("Flipkart search failed")

    # Search Other Stores
    try:
        products.extend(firecrawl.search(query))
    except:
        print("Other store search failed")

    # Remove duplicate products
    products = deduplicate_products(products)

    return {
        "products": products
    }