import hashlib
from typing import List, Dict, Tuple, Any

def get_pricing_details(price: float, seed_str: str) -> Tuple[float, str]:
    """Generates a stable, mock original price and discount percentage badge 
    based on a deterministic hash of the product name.
    """
    if not price or price <= 0:
        return 0.0, "0%"
    
    # Deterministic hash of name
    h = int(hashlib.md5(seed_str.encode('utf-8')).hexdigest(), 16)
    discount_pct = 10 + (h % 21) # Stable discount between 10% and 30%
    
    # original_price = price / (1 - discount_pct/100)
    original_price = price / (1.0 - (discount_pct / 100.0))
    # Round to clean nearest 100 and subtract 1 (e.g., 34999)
    original_price = round(original_price / 100) * 100 - 1
    
    if original_price <= price:
        original_price = price + 1999
        
    discount_pct = int(round((1.0 - price / original_price) * 100))
    return original_price, f"-{discount_pct}%"

def generate_mock_products(query: str) -> List[Dict[str, Any]]:
    """Generates realistic mockup products based on the search query.
    This acts as a high-fidelity local sandbox fallback if SerpAPI keys
    are not present or are failing.
    """
    q_lower = query.lower().strip()
    
    # Standard mocks for "Sony WH-1000XM5" (matching UI reference image perfectly)
    if "sony" in q_lower or "xm5" in q_lower or "headphone" in q_lower:
        return [
            {
                "name": "Sony WH-1000XM5 Wireless Headphones",
                "price": 26990.0,
                "rating": 4.7,
                "reviews": 2841,
                "seller": "Appario Retail",
                "url": "https://www.amazon.in/Sony-WH-1000XM5-Wireless-Noise-Cancelling/dp/B0B3C572G9",
                "image_url": "",
                "source": "Amazon",
                "delivery_info": "Free • Tomorrow",
                "specifications": "Over-Ear, 30hr Battery, Active Noise Cancellation",
                "brand": "Sony"
            },
            {
                "name": "Sony WH-1000XM5 Noise Cancelling",
                "price": 27499.0,
                "rating": 4.6,
                "reviews": 1902,
                "seller": "RetailNet",
                "url": "https://www.flipkart.com/sony-wh-1000xm5-active-noise-cancellation-anc-bluetooth-headset/p/itm5b13867ff1f58",
                "image_url": "",
                "source": "Flipkart",
                "delivery_info": "Free • 2 days",
                "specifications": "Over-Ear, ANC, Quick Charge",
                "brand": "Sony"
            },
            {
                "name": "Sony WH-1000XM5 (Silver) Headset",
                "price": 28990.0,
                "rating": 4.5,
                "reviews": 512,
                "seller": "Croma Retail",
                "url": "https://www.croma.com/sony-wh-1000xm5-wireless-headphone-with-mic/p/251345",
                "image_url": "",
                "source": "Croma",
                "delivery_info": "₹99 • 3 days",
                "specifications": "Over-Ear, 30hr Battery, Multi-Point Connection",
                "brand": "Sony"
            },
            {
                "name": "Bose QuietComfort Wireless Headphones",
                "price": 29990.0,
                "rating": 4.5,
                "reviews": 1240,
                "seller": "Bose Store",
                "url": "https://www.amazon.in/Bose-QuietComfort-Wireless-Noise-Cancelling/dp/B0CCZ1E4F5",
                "image_url": "",
                "source": "Amazon",
                "delivery_info": "Free • Tomorrow",
                "specifications": "Over-Ear, World-class ANC, Comfort Fit",
                "brand": "Bose"
            },
            {
                "name": "Sennheiser Accentum Wireless Over-Ear",
                "price": 12990.0,
                "rating": 4.3,
                "reviews": 843,
                "seller": "Sennheiser Official",
                "url": "https://www.flipkart.com/sennheiser-accentum-wireless-headphone/p/itm64235e12",
                "image_url": "",
                "source": "Flipkart",
                "delivery_info": "Free • 3 days",
                "specifications": "50-Hour Battery, Hybrid ANC, Foldable",
                "brand": "Sennheiser"
            },
            {
                "name": "JBL Tune 770NC Adaptive ANC",
                "price": 5999.0,
                "rating": 4.1,
                "reviews": 3410,
                "seller": "JBL India",
                "url": "https://www.croma.com/jbl-tune-770nc-wireless-headphone/p/284120",
                "image_url": "",
                "source": "Croma",
                "delivery_info": "Free • 2 days",
                "specifications": "70-Hour Battery, Bluetooth 5.3, Pure Bass",
                "brand": "JBL"
            },
            {
                "name": "Apple AirPods Max Wireless",
                "price": 59900.0,
                "rating": 4.7,
                "reviews": 920,
                "seller": "Appario Retail",
                "url": "https://www.amazon.in/Apple-AirPods-Max-Space-Grey/dp/B08P5GKHD6",
                "image_url": "",
                "source": "Amazon",
                "delivery_info": "Free • Tomorrow",
                "specifications": "High-fidelity audio, Active Noise Cancellation, Spatial Audio",
                "brand": "Apple"
            }
        ]
        
    # Standard mocks for "iPhone 15" or Apple products
    elif "iphone" in q_lower or "apple" in q_lower:
        return [
            {
                "name": "iPhone 15 128GB Blue",
                "price": 65999.0,
                "rating": 4.6,
                "reviews": 12500,
                "seller": "Appario Retail",
                "url": "https://www.amazon.in/Apple-iPhone-15-128-GB/dp/B0CHX1W1YW",
                "image_url": "",
                "source": "Amazon",
                "delivery_info": "Free • Tomorrow",
                "specifications": "128GB, 6.1-inch OLED, A16 Bionic, 48MP Camera",
                "brand": "Apple"
            },
            {
                "name": "Apple iPhone 15 (128 GB) - Blue",
                "price": 64999.0,
                "rating": 4.5,
                "reviews": 8300,
                "seller": "RetailNet",
                "url": "https://www.flipkart.com/apple-iphone-15-blue-128-gb/p/itm2d83c1e21b2b4",
                "image_url": "",
                "source": "Flipkart",
                "delivery_info": "Free • 2 days",
                "specifications": "128GB, Dynamic Island, A16 Bionic",
                "brand": "Apple"
            },
            {
                "name": "Samsung Galaxy S24 128GB",
                "price": 59999.0,
                "rating": 4.4,
                "reviews": 6100,
                "seller": "Samsung Store",
                "url": "https://www.amazon.in/Samsung-Galaxy-S24-5G/dp/B0CSD8P4D9",
                "image_url": "",
                "source": "Amazon",
                "delivery_info": "Free • Tomorrow",
                "specifications": "8GB RAM, 128GB, Snapdragon 8 Gen 3",
                "brand": "Samsung"
            },
            {
                "name": "Samsung Galaxy S24 5G 128GB",
                "price": 57499.0,
                "rating": 4.3,
                "reviews": 4200,
                "seller": "SuperComNet",
                "url": "https://www.flipkart.com/samsung-galaxy-s24-5g-amber-yellow-128-gb/p/itm5ab436e2f1f58",
                "image_url": "",
                "source": "Flipkart",
                "delivery_info": "Free • 3 days",
                "specifications": "8GB RAM, 128GB Storage, AI Features",
                "brand": "Samsung"
            },
            {
                "name": "OnePlus 12 256GB Flowy Emerald",
                "price": 64999.0,
                "rating": 4.5,
                "reviews": 3100,
                "seller": "OnePlus Store",
                "url": "https://www.amazon.in/OnePlus-Emerald-256GB-Storage-12GB/dp/B0CQYG5F93",
                "image_url": "",
                "source": "Amazon",
                "delivery_info": "Free • 2 days",
                "specifications": "12GB RAM, 256GB Storage, Snapdragon 8 Gen 3",
                "brand": "OnePlus"
            },
            {
                "name": "Suspiciously Cheap iPhone 15 Clone",
                "price": 4999.0,
                "rating": 3.1,
                "reviews": 40,
                "seller": "Shady Electronics",
                "url": "https://www.shadyclone.com/iphone15",
                "image_url": "",
                "source": "Other",
                "delivery_info": "10-15 days",
                "specifications": "Android OS skinned as iOS, Plastic Frame",
                "brand": "Apple"
            }
        ]
        
    # Default/dynamic mocks for other arbitrary search queries
    else:
        # Capitalize words
        q_title = query.title()
        words = q_title.split()
        brand = words[0] if words else "Generic"
        
        return [
            {
                "name": f"{q_title} Pro Max",
                "price": 45000.0,
                "rating": 4.7,
                "reviews": 1250,
                "seller": "Cloudtail India",
                "url": "https://amazon.in/mock-prod-1",
                "image_url": "",
                "source": "Amazon",
                "delivery_info": "Free • Tomorrow",
                "specifications": "Premium Edition, High Specs",
                "brand": brand
            },
            {
                "name": f"{q_title} Standard Edition",
                "price": 43500.0,
                "rating": 4.5,
                "reviews": 920,
                "seller": "RetailNet",
                "url": "https://flipkart.com/mock-prod-2",
                "image_url": "",
                "source": "Flipkart",
                "delivery_info": "Free • 2 days",
                "specifications": "Standard Edition, Balance Specs",
                "brand": brand
            },
            {
                "name": f"{q_title} Slim & Lightweight",
                "price": 41999.0,
                "rating": 4.4,
                "reviews": 310,
                "seller": "Croma Online",
                "url": "https://croma.com/mock-prod-3",
                "image_url": "",
                "source": "Croma",
                "delivery_info": "₹99 • 3 days",
                "specifications": "Slim Edition, Lightweight",
                "brand": brand
            },
            {
                "name": f"Alternative Premium Brand Tracker",
                "price": 49999.0,
                "rating": 4.6,
                "reviews": 1500,
                "seller": "Alternative Store",
                "url": "https://amazon.in/mock-prod-4",
                "image_url": "",
                "source": "Amazon",
                "delivery_info": "Free • Tomorrow",
                "specifications": "Elite Series",
                "brand": "OtherBrand"
            }
        ]
