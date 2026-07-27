import os
import time
import math
from google import genai
from google.genai import errors

# --- جیمنائی اے پی آئی سیٹ اپ ---
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

def scrape_markaz():
    print("مرکز ایپ کا ڈیٹا لوڈ ہو رہا ہے (30% مارجن کیلکولیشن کے لیے)...")
    # یہ وہ ڈیٹا ہے جو آپ مرکز سے سکریپ کریں گے۔ base_price مرکز کی اصل قیمت ہے۔
    return {
        "top_categories": [
            {"name": "Womens", "icon": "fa-female"},
            {"name": "Mens", "icon": "fa-male"},
            {"name": "Kids", "icon": "fa-child"},
            {"name": "Cosmetics", "icon": "fa-magic"}
        ],
        "sections": [
            {
                "title": "14th August Special",
                "products": [
                    {"id": 101, "name": "Green White Leaf Printed Lawn", "desc": "2 Piece Women's Unstitched Lawn Suit.", "base_price": 1870, "image": "https://images.unsplash.com/photo-1608234808654-2a8875faa7fd?w=500&q=80"},
                    {"id": 102, "name": "White Floral Printed Suit", "desc": "Beautiful 3 piece unstitched summer collection.", "base_price": 2529, "image": "https://images.unsplash.com/photo-1550614000-4b95d4ebf519?w=500&q=80"}
                ]
            },
            {
                "title": "Trending Unstitched Suits",
                "products": [
                    {"id": 201, "name": "Bin Saeed Digital Print", "desc": "Premium lawn 3 piece suit for women.", "base_price": 3140, "image": "https://images.unsplash.com/photo-1610419828456-11f81dfce043?w=500&q=80"},
                    {"id": 202, "name": "Purple Embroidered Lawn", "desc": "Luxury embroidered unstitched collection.", "base_price": 2270, "image": "https://images.unsplash.com/photo-1583391733958-67524ce4d31f?w=500&q=80"}
                ]
            },
            {
                "title": "Summer Comfort",
                "products": [
                    {"id": 301, "name": "Men's Jersey Printed Trouser", "desc": "Comfortable summer trousers for men.", "base_price": 899, "image": "https://images.unsplash.com/photo-1584865288642-42078afe6942?w=500&q=80"},
                    {"id": 302, "name": "Stylish Fleece Plain Double Bed", "desc": "Summer friendly bed sheet set.", "base_price": 2048, "image": "https://images.unsplash.com/photo-1522771731478-44eb10e5c776?w=500&q=80"}
                ]
            },
            {
                "title": "Fast Movers For You",
                "products": [
                    {"id": 401, "name": "Men's Casual Analog Watch", "desc": "Waterproof analog watch with black dial.", "base_price": 1500, "image": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=500&q=80"},
                    {"id": 402, "name": "Whitening Brightening Facial", "desc": "Premium cosmetics facial kit.", "base_price": 750, "image": "https://images.unsplash.com/photo-1596462502278-27bf85033e5a?w=500&q=80"}
                ]
            }
        ]
    }

def calculate_selling_price(base_price):
    """مرکز کی قیمت پر 30% منافع شامل کرنے کا فنکشن"""
    profit_margin = 0.30 # 30% Profit
    selling_price = base_price + (base_price * profit_margin)
    return math.ceil(selling_price) # قیمت کو راؤنڈ فگر کر دے گا

def fallback_seo_generator(name, desc):
    return f"Buy the best {name} online in Pakistan at ASM VEO. {desc} Cash on Delivery available."

def generate_seo_content(product_name, description):
    if not client:
        return fallback_seo_generator(product_name, description)
    
    prompt = f"Write a catchy, short SEO-friendly description for an e-commerce store ASM VEO for: {product_name}. Details: {description}. Return only text."
    
    for attempt in range(3):
        try:
            print(f"جیمنائی سے ایس ای او ٹرائی {attempt + 1}: {product_name}...")
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"ایرر آیا (Try {attempt + 1}): {e}")
            time.sleep(2)
            
    return fallback_seo_generator(product_name, description)

def get_html_header(title):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - ASM VEO</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .product-card:hover img {{ transform: scale(1.05); }}
        .product-card img {{ transition: transform 0.3s ease; }}
    </style>
</head>
<body class="bg-gray-100 text-gray-800 font-sans">
    <!-- Header / Navigation -->
    <header class="bg-white shadow-md sticky top-0 z-50">
        <div class="container mx-auto px-4 py-3 flex justify-between items-center">
            <a href="/index.html" class="text-2xl font-extrabold text-teal-700 tracking-wider flex items-center">
                <i class="fas fa-shopping-cart text-3xl mr-2"></i> ASM VEO
            </a>
            <div class="hidden md:flex space-x-6 items-center">
                <div class="relative">
                    <input type="text" placeholder="Search products, brands & stores" class="bg-gray-100 border border-gray-300 rounded-full py-2 px-4 w-96 focus:outline-none focus:ring-2 focus:ring-teal-500">
                    <i class="fas fa-search absolute right-3 top-3 text-gray-400"></i>
                </div>
            </div>
            <div class="flex space-x-4">
                <a href="/checkout.html" class="bg-teal-600 text-white px-6 py-2 rounded-full font-bold hover:bg-teal-700 transition">
                    <i class="fas fa-truck mr-1"></i> Orders
                </a>
            </div>
        </div>
    </header>
"""

def get_html_footer():
    return """
    <!-- Footer -->
    <footer class="bg-gray-900 text-white mt-12 py-8 border-t-4 border-teal-600">
        <div class="container mx-auto px-4 text-center">
            <h2 class="text-2xl font-bold mb-4">ASM VEO Store</h2>
            <p class="text-gray-400 mb-4">Built for Pakistan. Trusted Nationwide.</p>
            <p class="text-gray-500 text-sm">&copy; 2026 ASM Digital Solutions. All Rights Reserved.</p>
        </div>
    </footer>
</body>
</html>
"""

def build_store(data):
    print("ویب سائٹ اور مارجنز تیار ہو رہے ہیں...")
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/category", exist_ok=True)

    with open("output/CNAME", "w") as f:
        f.write("www.asmveo.com")

    # جیمنائی SEO اور 30% پرائس کیلکولیشن ہر پروڈکٹ کے لیے
    for section in data["sections"]:
        for prod in section["products"]:
            prod['seo_desc'] = generate_seo_content(prod['name'], prod['desc'])
            prod['final_price'] = calculate_selling_price(prod['base_price'])

    # === ہوم پیج بنانا شروع ===
    html = get_html_header("Home")
    
    # ٹاپ آئیکن کیٹیگریز (جیسے مرکز میں Hand-picked for All کے نیچے ہوتی ہیں)
    html += """
    <div class="bg-teal-50 py-8 shadow-inner">
        <div class="container mx-auto px-4 text-center">
            <h1 class="text-3xl font-extrabold text-gray-800 mb-1">Hand-picked for All</h1>
            <p class="text-gray-600 mb-8 text-sm">Curated by ASM VEO — refreshed regularly.</p>
            
            <div class="flex flex-wrap justify-center gap-8">
    """
    for cat in data["top_categories"]:
        html += f"""
                <a href="#" class="flex flex-col items-center group cursor-pointer">
                    <div class="w-16 h-16 rounded-full bg-white shadow-md flex items-center justify-center text-teal-600 group-hover:bg-teal-600 group-hover:text-white transition duration-300">
                        <i class="fas {cat['icon']} text-2xl"></i>
                    </div>
                    <span class="mt-2 text-sm font-semibold text-gray-700">{cat['name']}</span>
                </a>
        """
    html += "</div></div></div>"

    # مرکز ایپ کی طرح الگ الگ سیکشنز (14 اگست، ٹرینڈنگ وغیرہ)
    html += '<div class="container mx-auto px-4 py-8">'
    
    for section in data["sections"]:
        section_slug = section["title"].lower().replace(" ", "-")
        html += f"""
        <div class="mb-12">
            <div class="flex justify-between items-center border-b-2 border-gray-200 pb-2 mb-6">
                <h2 class="text-2xl font-bold text-gray-800">{section["title"]}</h2>
                <a href="/category/{section_slug}.html" class="text-teal-600 hover:text-teal-800 font-semibold text-sm">View All <i class="fas fa-chevron-right ml-1"></i></a>
            </div>
            
            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
        """
        for prod in section["products"]:
            html += f"""
                <div class="product-card bg-white rounded-lg shadow hover:shadow-xl overflow-hidden flex flex-col border border-gray-100">
                    <div class="relative overflow-hidden h-48 bg-gray-200">
                        <img src="{prod['image']}" alt="{prod['name']}" class="w-full h-full object-cover">
                    </div>
                    <div class="p-3 flex flex-col flex-grow">
                        <h3 class="text-sm font-bold text-gray-900 leading-tight mb-1 line-clamp-2">{prod['name']}</h3>
                        <p class="text-xs text-gray-500 mb-2 line-clamp-2 flex-grow">{prod['seo_desc']}</p>
                        
                        <div class="mt-auto">
                            <div class="flex items-center space-x-2">
                                <span class="text-lg font-extrabold text-teal-700">Rs {prod['final_price']}</span>
                                <span class="text-xs text-gray-400 line-through">Rs {prod['base_price']}</span>
                            </div>
                            <span class="text-[10px] font-bold text-green-600 bg-green-100 px-2 py-0.5 rounded-full mt-1 inline-block">Free Delivery</span>
                            
                            <a href="/checkout.html?id={prod['id']}" class="mt-3 block text-center bg-gray-900 text-white py-1.5 rounded text-sm font-bold hover:bg-teal-600 transition w-full">
                                Order Now
                            </a>
                        </div>
                    </div>
                </div>
            """
        html += "</div></div>"
    
    html += "</div>"
    html += get_html_footer()
    
    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(html)

    # === کیٹیگری پیجز (Separate Pages) بنانا ===
    for section in data["sections"]:
        section_slug = section["title"].lower().replace(" ", "-")
        cat_html = get_html_header(section["title"])
        cat_html += f"""
        <div class="container mx-auto px-4 py-8">
            <h1 class="text-3xl font-bold mb-6 text-gray-800 border-b-2 border-teal-600 inline-block pb-2">{section["title"]}</h1>
            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6">
        """
        for prod in section["products"]:
            cat_html += f"""
                <div class="product-card bg-white rounded-lg shadow hover:shadow-xl overflow-hidden flex flex-col border border-gray-100">
                    <div class="relative overflow-hidden h-48 bg-gray-200">
                        <img src="{prod['image']}" alt="{prod['name']}" class="w-full h-full object-cover">
                    </div>
                    <div class="p-4 flex flex-col flex-grow">
                        <h3 class="text-sm font-bold text-gray-900 leading-tight mb-1">{prod['name']}</h3>
                        <p class="text-xs text-gray-500 mb-2 line-clamp-2 flex-grow">{prod['seo_desc']}</p>
                        <div class="mt-auto">
                            <span class="text-lg font-extrabold text-teal-700 block">Rs {prod['final_price']}</span>
                            <a href="/checkout.html?id={prod['id']}" class="mt-3 block text-center bg-teal-600 text-white py-2 rounded text-sm font-bold hover:bg-gray-900 transition w-full">
                                Order via COD
                            </a>
                        </div>
                    </div>
                </div>
            """
        cat_html += "</div></div>"
        cat_html += get_html_footer()
        
        with open(f"output/category/{section_slug}.html", "w", encoding="utf-8") as f:
            f.write(cat_html)

    # === زبردست COD چیک آؤٹ پیج ===
    checkout_html = get_html_header("Secure Checkout")
    checkout_html += """
    <div class="container mx-auto px-4 py-10 max-w-3xl">
        <div class="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200">
            <div class="bg-teal-50 border-b border-teal-100 p-6 text-center">
                <h1 class="text-2xl font-extrabold text-teal-800"><i class="fas fa-shield-alt mr-2"></i> Cash on Delivery</h1>
                <p class="text-sm text-teal-600 mt-1">آپ کا آرڈر موصول ہونے پر ہی پیسے ادا کریں۔</p>
            </div>
            <form class="p-6 md:p-8 space-y-5">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-1">Full Name (پورا نام)</label>
                        <input type="text" class="w-full rounded-md border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 border p-2.5 bg-gray-50" required placeholder="Ali Abbas">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-1">Mobile Number (موبائل نمبر)</label>
                        <input type="tel" class="w-full rounded-md border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 border p-2.5 bg-gray-50" required placeholder="0300-1234567">
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-1">Delivery Address (مکمل پتہ)</label>
                    <textarea rows="3" class="w-full rounded-md border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 border p-2.5 bg-gray-50" required placeholder="مکان نمبر، گلی، محلہ، شہر کا نام..."></textarea>
                </div>
                
                <div class="mt-6 bg-blue-50 p-4 rounded border border-blue-100 flex justify-between items-center">
                    <div>
                        <span class="block font-bold text-blue-900">Delivery Charges:</span>
                        <span class="text-xs text-blue-700">Free delivery nationwide</span>
                    </div>
                    <span class="font-extrabold text-lg text-blue-900">Rs 0</span>
                </div>

                <button type="button" onclick="alert('Congratulations! Your Order has been placed successfully. We will call you for confirmation.')" class="w-full bg-teal-600 text-white font-bold py-3.5 px-4 rounded-lg hover:bg-teal-700 transition duration-300 shadow-md text-lg mt-4">
                    Confirm Order (آرڈر کنفرم کریں)
                </button>
            </form>
        </div>
    </div>
    """
    checkout_html += get_html_footer()
    
    with open("output/checkout.html", "w", encoding="utf-8") as f:
        f.write(checkout_html)

    print("✔ تمام صفحات (مرکز اسٹائل) اور 30% مارجن قیمتوں کے ساتھ کامیابی سے بن گئے ہیں!")

if __name__ == "__main__":
    print("--- ASM VEO Automation Script Started ---")
    scraped_data = scrape_markaz()
    build_store(scraped_data)
    print("--- ASM VEO Automation Script Finished ---")
