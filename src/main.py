import os
import time
import math
import re
import requests
from bs4 import BeautifulSoup
from google import genai

# --- جیمنائی اے پی آئی سیٹ اپ ---
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

def calculate_selling_price(base_price_str):
    """یہ فنکشن سکرپ کی گئی قیمت (جیسے PKR 1,870) میں سے ہندسے نکال کر 30% مارجن لگاتا ہے"""
    try:
        # 'PKR 1,870' میں سے صرف نمبرز (1870) نکالے گا
        clean_price = re.sub(r'[^\d]', '', base_price_str)
        if not clean_price:
            return 0, 0
            
        base_price = int(clean_price)
        profit_margin = 0.30  # 30% Profit
        selling_price = base_price + (base_price * profit_margin)
        return base_price, math.ceil(selling_price)
    except Exception:
        return 0, 0

def scrape_markaz_realtime():
    print("انٹرنیٹ سے مرکز (markaz.app) کا لائیو ڈیٹا سکریپ ہو رہا ہے...")
    url = "https://www.markaz.app/"
    
    # ہیڈرز تاکہ مرکز کی ویب سائٹ اس سکرپٹ کو براؤزر سمجھے اور بلاک نہ کرے
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    scraped_sections = []
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        # BeautifulSoup کا استعمال
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # ہم لائیو ویب سائٹ سے قیمتوں (PKR) والے ایلیمنٹس ڈھونڈیں گے
        # نوٹ: اگر ویب سائٹ کا سٹرکچر بدلا ہو، تو یہ fallback ڈیٹا کی طرف چلا جائے گا تاکہ سائیٹ کریش نہ ہو۔
        price_elements = soup.find_all(text=re.compile(r'PKR\s*[\d,]+'))
        
        live_products = []
        product_id = 1
        
        for price_text in price_elements:
            parent = price_text.parent.parent # قیمت کے اوپر والے کنٹینر میں جائیں گے
            if parent:
                # تصویر اور ٹائٹل ڈھونڈنے کی کوشش
                img_tag = parent.find('img')
                title_tag = parent.find(['h3', 'h4', 'p', 'div'], text=True)
                
                if img_tag and img_tag.get('src'):
                    image_url = img_tag['src']
                    title = title_tag.text.strip() if title_tag else "Premium Quality Product"
                    
                    # 30% پرافٹ کے ساتھ قیمت نکالنا
                    base_p, final_p = calculate_selling_price(price_text)
                    
                    if base_p > 0:
                        live_products.append({
                            "id": product_id,
                            "name": title,
                            "desc": "High quality product directly sourced from Markaz.",
                            "base_price": base_p,
                            "final_price": final_p,
                            "image": image_url
                        })
                        product_id += 1
                        
                        # 20 پروڈکٹس ہو جائیں تو بس کر دیں
                        if len(live_products) >= 20:
                            break

        if live_products:
            print(f"✔ کامیابی سے {len(live_products)} ریئل پروڈکٹس سکریپ ہو گئیں!")
            scraped_sections.append({
                "title": "Fresh Arrivals (Live Data)",
                "products": live_products
            })
        else:
            raise Exception("No products found via BeautifulSoup (JavaScript rendering blocking).")

    except Exception as e:
        print(f"لائیو سکریپنگ میں رکاوٹ (وجہ: {e})۔ فال بیک ڈیٹا استعمال ہو رہا ہے...")
        # اگر مرکز ایپ نے جاوا سکرپٹ (React) کی وجہ سے سکریپنگ بلاک کی، تو یہ پروفیشنل بیک اپ چلے گا۔
        base1, final1 = calculate_selling_price("PKR 1870")
        base2, final2 = calculate_selling_price("PKR 2529")
        base3, final3 = calculate_selling_price("PKR 3140")
        
        scraped_sections = [
            {
                "title": "14th August Special",
                "products": [
                    {"id": 101, "name": "Green White Leaf Printed Lawn", "desc": "2 Piece Women's Unstitched Lawn Suit.", "base_price": base1, "final_price": final1, "image": "https://images.unsplash.com/photo-1608234808654-2a8875faa7fd?w=500&q=80"},
                    {"id": 102, "name": "White Floral Printed Suit", "desc": "Beautiful 3 piece unstitched summer collection.", "base_price": base2, "final_price": final2, "image": "https://images.unsplash.com/photo-1550614000-4b95d4ebf519?w=500&q=80"}
                ]
            },
            {
                "title": "Trending Unstitched Suits",
                "products": [
                    {"id": 201, "name": "Bin Saeed Digital Print", "desc": "Premium lawn 3 piece suit for women.", "base_price": base3, "final_price": final3, "image": "https://images.unsplash.com/photo-1610419828456-11f81dfce043?w=500&q=80"}
                ]
            }
        ]

    return {
        "top_categories": [
            {"name": "Womens", "icon": "fa-female"},
            {"name": "Mens", "icon": "fa-male"},
            {"name": "Kids", "icon": "fa-child"},
            {"name": "Cosmetics", "icon": "fa-magic"}
        ],
        "sections": scraped_sections
    }

def fallback_seo_generator(name, desc):
    return f"Buy {name} online in Pakistan at ASM VEO. {desc} Cash on Delivery available."

def generate_seo_content(product_name, description):
    if not client:
        return fallback_seo_generator(product_name, description)
    prompt = f"Write a catchy, short SEO-friendly description for an e-commerce store ASM VEO for: {product_name}. Details: {description}. Return only text."
    for attempt in range(3):
        try:
            print(f"جیمنائی سے ایس ای او ٹرائی {attempt + 1}: {product_name}...")
            return client.models.generate_content(model='gemini-1.5-flash', contents=prompt).text
        except Exception as e:
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
    <style>.product-card:hover img {{ transform: scale(1.05); }} .product-card img {{ transition: transform 0.3s ease; }}</style>
</head>
<body class="bg-gray-100 text-gray-800 font-sans">
    <header class="bg-white shadow-md sticky top-0 z-50">
        <div class="container mx-auto px-4 py-3 flex justify-between items-center">
            <a href="/index.html" class="text-2xl font-extrabold text-teal-700 tracking-wider flex items-center">
                <i class="fas fa-shopping-cart text-3xl mr-2"></i> ASM VEO
            </a>
            <a href="/checkout.html" class="bg-teal-600 text-white px-6 py-2 rounded-full font-bold hover:bg-teal-700 transition">
                <i class="fas fa-truck mr-1"></i> Orders
            </a>
        </div>
    </header>
"""

def get_html_footer():
    return """
    <footer class="bg-gray-900 text-white mt-12 py-8 border-t-4 border-teal-600">
        <div class="container mx-auto px-4 text-center">
            <h2 class="text-2xl font-bold mb-2">ASM VEO Store</h2>
            <p class="text-gray-400 mb-4">Built for Pakistan. Trusted Nationwide.</p>
            <p class="text-gray-500 text-sm">&copy; 2026 ASM Digital Solutions. All Rights Reserved.</p>
        </div>
    </footer>
</body>
</html>
"""

def build_store(data):
    print("ویب سائٹ اور پیجز تیار ہو رہے ہیں...")
    os.makedirs("output/category", exist_ok=True)
    with open("output/CNAME", "w") as f:
        f.write("www.asmveo.com")

    for section in data["sections"]:
        for prod in section["products"]:
            prod['seo_desc'] = generate_seo_content(prod['name'], prod['desc'])

    # --- Home Page ---
    html = get_html_header("Home")
    html += """
    <div class="bg-teal-50 py-8 shadow-inner"><div class="container mx-auto px-4 text-center">
        <h1 class="text-3xl font-extrabold text-gray-800 mb-1">Hand-picked for All</h1>
        <div class="flex flex-wrap justify-center gap-8 mt-6">
    """
    for cat in data["top_categories"]:
        html += f"""
            <a href="#" class="flex flex-col items-center group">
                <div class="w-16 h-16 rounded-full bg-white shadow-md flex items-center justify-center text-teal-600 group-hover:bg-teal-600 group-hover:text-white transition duration-300">
                    <i class="fas {cat['icon']} text-2xl"></i>
                </div>
                <span class="mt-2 text-sm font-semibold text-gray-700">{cat['name']}</span>
            </a>
        """
    html += "</div></div></div><div class='container mx-auto px-4 py-8'>"
    
    for section in data["sections"]:
        section_slug = section["title"].lower().replace(" ", "-")
        html += f"""
        <div class="mb-12">
            <div class="flex justify-between items-center border-b-2 border-gray-200 pb-2 mb-6">
                <h2 class="text-2xl font-bold text-gray-800">{section["title"]}</h2>
                <a href="/category/{section_slug}.html" class="text-teal-600 font-semibold text-sm">View All <i class="fas fa-chevron-right ml-1"></i></a>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
        """
        for prod in section["products"]:
            html += f"""
                <div class="product-card bg-white rounded-lg shadow overflow-hidden flex flex-col border border-gray-100">
                    <div class="h-48 bg-gray-200"><img src="{prod['image']}" alt="{prod['name']}" class="w-full h-full object-cover"></div>
                    <div class="p-3 flex flex-col flex-grow">
                        <h3 class="text-sm font-bold text-gray-900 mb-1 line-clamp-2">{prod['name']}</h3>
                        <p class="text-xs text-gray-500 mb-2 flex-grow line-clamp-2">{prod['seo_desc']}</p>
                        <div class="mt-auto">
                            <span class="text-lg font-extrabold text-teal-700">Rs {prod['final_price']}</span>
                            <span class="text-xs text-gray-400 line-through ml-1">Rs {prod['base_price']}</span>
                            <a href="/checkout.html?id={prod['id']}" class="mt-3 block text-center bg-gray-900 text-white py-1.5 rounded text-sm font-bold hover:bg-teal-600 transition w-full">Order Now</a>
                        </div>
                    </div>
                </div>
            """
        html += "</div></div>"
    
    html += "</div>" + get_html_footer()
    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(html)

    # --- Category Pages ---
    for section in data["sections"]:
        section_slug = section["title"].lower().replace(" ", "-")
        cat_html = get_html_header(section["title"])
        cat_html += f'<div class="container mx-auto px-4 py-8"><h1 class="text-3xl font-bold mb-6 text-gray-800 border-b-2 border-teal-600 inline-block pb-2">{section["title"]}</h1><div class="grid grid-cols-2 md:grid-cols-4 gap-6">'
        for prod in section["products"]:
            cat_html += f"""
                <div class="product-card bg-white rounded-lg shadow overflow-hidden flex flex-col border border-gray-100">
                    <div class="h-48 bg-gray-200"><img src="{prod['image']}" alt="{prod['name']}" class="w-full h-full object-cover"></div>
                    <div class="p-4 flex flex-col flex-grow">
                        <h3 class="text-sm font-bold text-gray-900 mb-1">{prod['name']}</h3>
                        <div class="mt-auto"><span class="text-lg font-extrabold text-teal-700 block">Rs {prod['final_price']}</span>
                        <a href="/checkout.html?id={prod['id']}" class="mt-3 block text-center bg-teal-600 text-white py-2 rounded text-sm font-bold">Order via COD</a></div>
                    </div>
                </div>
            """
        cat_html += "</div></div>" + get_html_footer()
        with open(f"output/category/{section_slug}.html", "w", encoding="utf-8") as f:
            f.write(cat_html)

    # --- Checkout Page ---
    checkout_html = get_html_header("Secure Checkout")
    checkout_html += """
    <div class="container mx-auto px-4 py-10 max-w-3xl">
        <div class="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200">
            <div class="bg-teal-50 p-6 text-center">
                <h1 class="text-2xl font-extrabold text-teal-800">Cash on Delivery</h1>
                <p class="text-sm text-teal-600 mt-1">Pay when you receive your order.</p>
            </div>
            <form class="p-6 md:p-8 space-y-5">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                    <div><label class="block text-sm font-bold text-gray-700 mb-1">Full Name</label><input type="text" class="w-full border p-2.5 rounded bg-gray-50" required></div>
                    <div><label class="block text-sm font-bold text-gray-700 mb-1">Mobile</label><input type="tel" class="w-full border p-2.5 rounded bg-gray-50" required></div>
                </div>
                <div><label class="block text-sm font-bold text-gray-700 mb-1">Address</label><textarea rows="3" class="w-full border p-2.5 rounded bg-gray-50" required></textarea></div>
                <button type="button" onclick="alert('Order Placed Successfully!')" class="w-full bg-teal-600 text-white font-bold py-3.5 px-4 rounded-lg hover:bg-teal-700 transition mt-4">Confirm Order</button>
            </form>
        </div>
    </div>
    """
    checkout_html += get_html_footer()
    with open("output/checkout.html", "w", encoding="utf-8") as f:
        f.write(checkout_html)

if __name__ == "__main__":
    print("--- ASM VEO Automation Script Started ---")
    scraped_data = scrape_markaz_realtime()
    build_store(scraped_data)
    print("--- ASM VEO Automation Script Finished ---")
