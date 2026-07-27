import os
import time
from google import genai
from google.genai import errors

# --- جیمنائی اے پی آئی سیٹ اپ ---
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

def scrape_markaz():
    print("ڈمی ڈیٹا لوڈ ہو رہا ہے (امیجز اور کیٹیگریز کے ساتھ)...")
    return {
        "categories": ["Womens Fashion", "Mens Fashion", "Home Decor", "Cosmetics"],
        "products": [
            {"id": 1, "name": "Premium Leather Handbag", "category": "Womens Fashion", "desc": "High-quality leather handbag for everyday use.", "price": "3500", "image": "https://images.unsplash.com/photo-1584916201218-f4242ceb4809?w=500&q=80"},
            {"id": 2, "name": "Embroidered Unstitched Suit", "category": "Womens Fashion", "desc": "Beautiful 3-piece unstitched lawn suit.", "price": "4200", "image": "https://images.unsplash.com/photo-1608234808654-2a8875faa7fd?w=500&q=80"},
            {"id": 3, "name": "Mens Casual Analog Watch", "category": "Mens Fashion", "desc": "Waterproof analog watch with leather strap.", "price": "1500", "image": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=500&q=80"},
            {"id": 4, "name": "Luxury Bed Sheet Set", "category": "Home Decor", "desc": "Soft cotton king size bed sheet with 2 pillow covers.", "price": "2800", "image": "https://images.unsplash.com/photo-1522771731478-44eb10e5c776?w=500&q=80"}
        ]
    }

def fallback_seo_generator(name, desc):
    """اگر جیمنائی کام نہ کرے تو یہ فنکشن خودکار ایس ای او کنٹینٹ بنائے گا"""
    return f"Buy the best {name} online in Pakistan at ASM VEO. {desc} Enjoy fast shipping and Cash on Delivery nationwide."

def generate_seo_content(product_name, description):
    """جیمنائی اے پی آئی 3 بار ٹرائی کرے گا، ورنہ فیل بیک چلائے گا"""
    if not client:
        return fallback_seo_generator(product_name, description)
    
    prompt = f"Write a catchy, highly SEO-friendly 2-line description for an e-commerce store named ASM VEO for this product: {product_name}. Details: {description}. Return only text."
    
    for attempt in range(3):
        try:
            print(f"جیمنائی سے ایس ای او ٹرائی {attempt + 1} پروڈکٹ کے لیے: {product_name}...")
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"ایرر آیا (Try {attempt + 1}): {e}")
            time.sleep(2) # 2 سیکنڈ انتظار کر کے دوبارہ ٹرائی کرے گا
            
    print(f"جیمنائی 3 بار فیل ہو گیا۔ لوکل ایس ای او اسکرپٹ استعمال ہو رہی ہے۔")
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
</head>
<body class="bg-gray-50 text-gray-800 font-sans">
    <!-- Header / Navigation -->
    <header class="bg-white shadow-md sticky top-0 z-50">
        <div class="container mx-auto px-4 py-4 flex justify-between items-center">
            <a href="/index.html" class="text-3xl font-extrabold text-teal-600 tracking-wider">
                <i class="fas fa-shopping-bag mr-2"></i>ASM VEO
            </a>
            <div class="hidden md:flex space-x-6">
                <a href="/index.html" class="text-gray-600 hover:text-teal-600 font-semibold">Home</a>
                <a href="#categories" class="text-gray-600 hover:text-teal-600 font-semibold">Shop by Category</a>
            </div>
            <a href="/checkout.html" class="bg-teal-600 text-white px-5 py-2 rounded-full font-bold hover:bg-teal-700 transition">
                <i class="fas fa-truck mr-2"></i>Track Order
            </a>
        </div>
    </header>
"""

def get_html_footer():
    return """
    <!-- Footer -->
    <footer class="bg-gray-900 text-white mt-12 py-8">
        <div class="container mx-auto px-4 text-center">
            <h2 class="text-2xl font-bold mb-4">ASM VEO Store</h2>
            <p class="text-gray-400 mb-4">Premium Products, Delivered Fast Nationwide.</p>
            <p class="text-gray-500 text-sm">&copy; 2026 ASM VEO Digital Solutions. All Rights Reserved.</p>
        </div>
    </footer>
</body>
</html>
"""

def build_store(data):
    print("ویب سائٹ کی فائلز تیار ہو رہی ہیں...")
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/category", exist_ok=True)

    # 1. CNAME File
    with open("output/CNAME", "w") as f:
        f.write("www.asmveo.com")

    # 2. SEO Content Generation
    for prod in data["products"]:
        prod['seo_desc'] = generate_seo_content(prod['name'], prod['desc'])

    # 3. Main Index Page (Home)
    html = get_html_header("Home")
    
    # Hero Section & Categories
    html += """
    <div class="bg-teal-50 py-10">
        <div class="container mx-auto px-4 text-center">
            <h1 class="text-4xl font-bold text-gray-800 mb-2">Hand-picked for All</h1>
            <p class="text-gray-600 mb-8">Curated items — refreshed regularly.</p>
            
            <div id="categories" class="flex flex-wrap justify-center gap-6">
    """
    for cat in data["categories"]:
        cat_slug = cat.lower().replace(" ", "-")
        html += f"""
                <a href="/category/{cat_slug}.html" class="flex flex-col items-center group">
                    <div class="w-20 h-20 rounded-full bg-white shadow-md flex items-center justify-center text-teal-600 group-hover:bg-teal-600 group-hover:text-white transition duration-300">
                        <i class="fas fa-tags text-2xl"></i>
                    </div>
                    <span class="mt-2 font-medium text-gray-700 group-hover:text-teal-600">{cat}</span>
                </a>
        """
    html += "</div></div></div>"

    # All Products Grid (Home Page)
    html += """
    <div class="container mx-auto px-4 py-12">
        <h2 class="text-2xl font-bold mb-6 border-b-2 border-teal-600 inline-block pb-2">Trending Now</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
    """
    for prod in data["products"]:
        html += f"""
            <div class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition duration-300 flex flex-col">
                <img src="{prod['image']}" alt="{prod['name']}" class="w-full h-56 object-cover">
                <div class="p-5 flex-grow flex flex-col">
                    <span class="text-xs font-bold text-teal-600 uppercase tracking-wide">{prod['category']}</span>
                    <h3 class="text-lg font-bold text-gray-900 mt-1">{prod['name']}</h3>
                    <p class="text-sm text-gray-600 mt-2 flex-grow">{prod['seo_desc']}</p>
                    <div class="mt-4 flex justify-between items-center">
                        <span class="text-xl font-extrabold text-gray-900">Rs {prod['price']}</span>
                    </div>
                    <a href="/checkout.html?product={prod['id']}" class="mt-4 block text-center bg-gray-900 text-white py-2 rounded-lg font-bold hover:bg-teal-600 transition w-full">
                        Order via COD
                    </a>
                </div>
            </div>
        """
    html += "</div></div>"
    html += get_html_footer()
    
    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(html)

    # 4. Category Pages Generation (Multiple Pages)
    for cat in data["categories"]:
        cat_slug = cat.lower().replace(" ", "-")
        cat_html = get_html_header(cat)
        cat_html += f"""
        <div class="container mx-auto px-4 py-8">
            <h1 class="text-3xl font-bold mb-6 text-gray-800">{cat} Collection</h1>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        """
        cat_products = [p for p in data["products"] if p["category"] == cat]
        if not cat_products:
            # یہاں سنٹیکس ایرر کو ٹھیک کیا گیا ہے (ڈبل کوٹس کی جگہ سنگل کوٹس لگائے ہیں)
            cat_html += '<p class="col-span-full text-center text-gray-500">No products found in this category.</p>'
        else:
            for prod in cat_products:
                cat_html += f"""
                <div class="bg-white rounded-xl shadow-lg overflow-hidden flex flex-col">
                    <img src="{prod['image']}" alt="{prod['name']}" class="w-full h-56 object-cover">
                    <div class="p-5 flex flex-col flex-grow">
                        <h3 class="text-lg font-bold text-gray-900">{prod['name']}</h3>
                        <p class="text-sm text-gray-600 mt-2 flex-grow">{prod['seo_desc']}</p>
                        <span class="text-xl font-extrabold text-gray-900 mt-4">Rs {prod['price']}</span>
                        <a href="/checkout.html?product={prod['id']}" class="mt-4 block text-center bg-gray-900 text-white py-2 rounded-lg font-bold hover:bg-teal-600 transition">Order via COD</a>
                    </div>
                </div>
                """
        cat_html += "</div></div>"
        cat_html += get_html_footer()
        
        with open(f"output/category/{cat_slug}.html", "w", encoding="utf-8") as f:
            f.write(cat_html)

    # 5. Professional COD Checkout Page
    checkout_html = get_html_header("Secure Checkout")
    checkout_html += """
    <div class="container mx-auto px-4 py-12 max-w-2xl">
        <div class="bg-white rounded-2xl shadow-2xl overflow-hidden">
            <div class="bg-teal-600 text-white p-6 text-center">
                <h1 class="text-3xl font-bold"><i class="fas fa-lock mr-2"></i>Secure Cash on Delivery</h1>
                <p class="mt-2 text-teal-100">Pay only when you receive your order at your doorstep.</p>
            </div>
            <form class="p-8 space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Full Name</label>
                        <input type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 border p-2" required placeholder="Ali Abbas">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Mobile Number</label>
                        <input type="tel" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 border p-2" required placeholder="0300-1234567">
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Complete Delivery Address</label>
                    <textarea rows="3" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 border p-2" required placeholder="House No, Street, Area..."></textarea>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">City</label>
                    <input type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 border p-2" required placeholder="Islamabad">
                </div>
                <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 flex items-center justify-between">
                    <span class="font-bold text-gray-700">Payment Method:</span>
                    <span class="text-green-600 font-bold bg-green-100 px-3 py-1 rounded-full"><i class="fas fa-money-bill-wave mr-1"></i> Cash on Delivery</span>
                </div>
                <button type="button" onclick="alert('Order Confirmed Successfully! Our team will contact you soon.')" class="w-full bg-teal-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-teal-700 transition duration-300 text-lg shadow-lg">
                    Confirm Order
                </button>
            </form>
        </div>
    </div>
    """
    checkout_html += get_html_footer()
    
    with open("output/checkout.html", "w", encoding="utf-8") as f:
        f.write(checkout_html)

    print("✔ تمام پیجز (Home, Categories, Checkout) کامیابی سے بن گئے ہیں!")

if __name__ == "__main__":
    print("--- ASM VEO Automation Script Started ---")
    scraped_data = scrape_markaz()
    build_store(scraped_data)
    print("--- ASM VEO Automation Script Finished ---")
