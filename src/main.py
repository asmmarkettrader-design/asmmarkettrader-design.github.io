import os
import csv
import time
import math
import re
from google import genai

# --- جیمنائی اے پی آئی سیٹ اپ ---
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

def get_price(price_str):
    """قیمت کے کالم سے سٹرنگ کو نمبر میں تبدیل کرتا ہے"""
    try:
        if not price_str: return 0
        clean_price = re.sub(r'[^\d.]', '', str(price_str))
        return float(clean_price)
    except Exception:
        return 0

def load_woocommerce_csv():
    """یہ فنکشن روٹ فولڈر سے CSV فائل پڑھے گا اور 30% مارجن لگائے گا"""
    file_path = "woocommerce-products-export.csv"
    print(f"فائل تلاش کی جا رہی ہے: {file_path}")
    
    if not os.path.exists(file_path):
        print("❌ CSV فائل نہیں ملی! برائے مہربانی چیک کریں کہ فائل کا نام 'woocommerce-products-export.csv' ہی ہے۔")
        return {"categories": [], "sections": [], "all_products": []}

    products = []
    categories_set = set()
    
    print("✔ CSV فائل مل گئی، ڈیٹا پروسیس ہو رہا ہے...")
    
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            if not name:
                continue
                
            # قیمت نکالنا (پہلے Sale price چیک کرے گا، نہ ہو تو Regular price)
            sale_price = row.get('Sale price', '')
            reg_price = row.get('Regular price', '')
            base_price_str = sale_price if sale_price else reg_price
            base_price = get_price(base_price_str)
            
            if base_price == 0:
                continue
                
            # 30% پرافٹ مارجن کیلکولیشن
            final_price = math.ceil(base_price * 1.30) 
            
            # کیٹیگری (اگر ایک سے زیادہ ہوں تو پہلی لے گا)
            cat_raw = row.get('Categories', 'Uncategorized')
            category = cat_raw.split(',')[0].strip() if cat_raw else 'Special Items'
            categories_set.add(category)
            
            # امیج (پہلی تصویر کا لنک لے گا)
            images_raw = row.get('Images', '')
            image = images_raw.split(',')[0].strip() if images_raw else 'https://via.placeholder.com/500?text=No+Image'
            
            desc = row.get('Short description', '') or row.get('Description', 'High quality premium product.')
            
            # ایچ ٹی ایم ایل ٹیگز کو صاف کرنا
            clean_desc = re.sub(r'<[^>]+>', '', desc).strip()
            
            products.append({
                'id': row.get('ID', str(len(products)+1)),
                'name': name,
                'category': category,
                'base_price': int(base_price),
                'final_price': final_price,
                'image': image,
                'desc': clean_desc[:100] + '...'
            })

    # ہوم پیج کے لیے پروڈکٹس کو کیٹیگریز (Sections) میں تقسیم کرنا
    grouped_products = {}
    for p in products:
        c = p['category']
        if c not in grouped_products:
            grouped_products[c] = []
        grouped_products[c].append(p)
        
    sections = []
    for cat_name, prods in grouped_products.items():
        sections.append({
            "title": cat_name,
            "products": prods[:10] # ہوم پیج پر ہر کیٹیگری کی زیادہ سے زیادہ 10 پروڈکٹس دکھائے گا
        })
        
    print(f"✔ کل {len(products)} پروڈکٹس اور {len(sections)} کیٹیگریز کامیابی سے لوڈ ہو گئیں۔")
    
    return {
        "categories": list(categories_set),
        "sections": sections,
        "all_products": products
    }

def fallback_seo_generator(name, desc):
    return f"Buy {name} online in Pakistan at ASM VEO. Premium quality guaranteed."

def generate_seo_content(product_name, description):
    if not client:
        return fallback_seo_generator(product_name, description)
    prompt = f"Write a short, engaging 2-line SEO description for an e-commerce store ASM VEO for this product: {product_name}. Return only text without quotes."
    for attempt in range(3):
        try:
            return client.models.generate_content(model='gemini-1.5-flash', contents=prompt).text.strip()
        except Exception:
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
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
        body {{ font-family: 'Poppins', sans-serif; }}
        .product-card {{ transition: all 0.3s ease; }}
        .product-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }}
        .image-container img {{ transition: transform 0.5s ease; }}
        .product-card:hover .image-container img {{ transform: scale(1.08); }}
    </style>
</head>
<body class="bg-gray-50 text-gray-800">
    <!-- Navigation Bar -->
    <header class="bg-white shadow-sm sticky top-0 z-50">
        <div class="container mx-auto px-4 py-4 flex justify-between items-center">
            <a href="/index.html" class="text-2xl md:text-3xl font-extrabold text-teal-700 tracking-tight flex items-center gap-2">
                <i class="fas fa-shopping-bag text-teal-500"></i> ASM VEO
            </a>
            <div class="hidden md:flex flex-1 max-w-xl mx-8">
                <div class="relative w-full">
                    <input type="text" placeholder="Search products, categories..." class="w-full bg-gray-100 border-none rounded-full py-2.5 px-6 focus:ring-2 focus:ring-teal-500 focus:outline-none transition">
                    <i class="fas fa-search absolute right-4 top-3.5 text-gray-400"></i>
                </div>
            </div>
            <a href="/checkout.html" class="bg-teal-600 text-white px-5 md:px-6 py-2 md:py-2.5 rounded-full font-semibold hover:bg-teal-700 transition shadow-md flex items-center gap-2">
                <i class="fas fa-truck-fast"></i> <span class="hidden md:inline">Track Order</span>
            </a>
        </div>
    </header>
"""

def get_html_footer():
    return """
    <!-- Footer -->
    <footer class="bg-gray-900 text-white mt-16 pt-12 pb-6 border-t-4 border-teal-500">
        <div class="container mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            <div>
                <h3 class="text-xl font-bold mb-4 flex items-center gap-2"><i class="fas fa-shopping-bag text-teal-400"></i> ASM VEO</h3>
                <p class="text-gray-400 text-sm leading-relaxed">Your premium destination for high-quality products. We offer nationwide delivery with a secure and seamless shopping experience.</p>
            </div>
            <div>
                <h3 class="text-lg font-bold mb-4">Quick Links</h3>
                <ul class="space-y-2 text-gray-400 text-sm">
                    <li><a href="/index.html" class="hover:text-teal-400 transition">Home</a></li>
                    <li><a href="/checkout.html" class="hover:text-teal-400 transition">Checkout</a></li>
                    <li><a href="#" class="hover:text-teal-400 transition">Contact Us</a></li>
                </ul>
            </div>
            <div>
                <h3 class="text-lg font-bold mb-4">Customer Support</h3>
                <p class="text-gray-400 text-sm"><i class="fas fa-envelope mr-2"></i> support@asmveo.com</p>
                <p class="text-gray-400 text-sm mt-2"><i class="fas fa-shield-alt mr-2"></i> 100% Secure Checkout</p>
            </div>
        </div>
        <div class="border-t border-gray-800 text-center pt-6">
            <p class="text-gray-500 text-xs tracking-wider">&copy; 2026 ASM Digital Solutions. All Rights Reserved.</p>
        </div>
    </footer>
</body>
</html>
"""

def build_store(data):
    if not data["sections"]:
        print("کوئی ڈیٹا نہیں ملا۔ سکرپٹ بند ہو رہی ہے۔")
        return

    print("ویب سائٹ کے پیجز جنریٹ ہو رہے ہیں...")
    os.makedirs("output/category", exist_ok=True)
    with open("output/CNAME", "w") as f:
        f.write("www.asmveo.com")

    # جیمنائی سے ایس ای او ڈسکرپشن لکھوانا (ہر پروڈکٹ کے لیے)
    for p in data["all_products"]:
        p['seo_desc'] = generate_seo_content(p['name'], p['desc'])

    # --- Home Page ---
    html = get_html_header("Home")
    
    # Categories Top Bar (Icons)
    html += """
    <div class="bg-gradient-to-b from-teal-50 to-white py-10 shadow-inner">
        <div class="container mx-auto px-4">
            <div class="text-center mb-8">
                <h1 class="text-3xl md:text-4xl font-extrabold text-gray-800 mb-2">Hand-picked for You</h1>
                <p class="text-gray-500">Discover our top categories</p>
            </div>
            <div class="flex flex-wrap justify-center gap-6 md:gap-10">
    """
    
    # آئیکنز کی لسٹ
    icons = ['fa-gem', 'fa-tshirt', 'fa-shoe-prints', 'fa-glasses', 'fa-clock', 'fa-home', 'fa-mobile']
    for idx, cat in enumerate(data["categories"]):
        icon = icons[idx % len(icons)]
        cat_slug = cat.lower().replace(" ", "-").replace("/", "-")
        html += f"""
                <a href="/category/{cat_slug}.html" class="flex flex-col items-center group cursor-pointer w-20 md:w-24">
                    <div class="w-16 h-16 md:w-20 md:h-20 rounded-2xl bg-white shadow-md border border-gray-100 flex items-center justify-center text-teal-500 group-hover:bg-teal-500 group-hover:text-white group-hover:shadow-lg transition-all duration-300 transform group-hover:-translate-y-1">
                        <i class="fas {icon} text-2xl md:text-3xl"></i>
                    </div>
                    <span class="mt-3 text-xs md:text-sm font-semibold text-gray-700 text-center leading-tight group-hover:text-teal-600">{cat}</span>
                </a>
        """
    html += "</div></div></div>"

    # Category Sections (Products Grid)
    html += "<div class='container mx-auto px-4 py-10'>"
    for section in data["sections"]:
        section_slug = section["title"].lower().replace(" ", "-").replace("/", "-")
        html += f"""
        <div class="mb-14">
            <div class="flex justify-between items-end border-b-2 border-gray-100 pb-3 mb-6">
                <div>
                    <h2 class="text-2xl md:text-3xl font-bold text-gray-800">{section["title"]}</h2>
                    <div class="h-1 w-16 bg-teal-500 mt-2 rounded"></div>
                </div>
                <a href="/category/{section_slug}.html" class="text-teal-600 hover:text-teal-800 font-semibold text-sm flex items-center gap-1 transition">
                    View All <i class="fas fa-arrow-right"></i>
                </a>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
        """
        for prod in section["products"]:
            html += f"""
                <div class="product-card bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden flex flex-col relative group">
                    <div class="absolute top-2 right-2 bg-red-500 text-white text-[10px] font-bold px-2 py-1 rounded-full z-10 shadow">30% OFF</div>
                    <div class="image-container h-48 md:h-56 bg-gray-50 overflow-hidden relative">
                        <img src="{prod['image']}" alt="{prod['name']}" class="w-full h-full object-cover" loading="lazy">
                    </div>
                    <div class="p-4 flex flex-col flex-grow">
                        <h3 class="text-sm md:text-base font-bold text-gray-800 leading-tight mb-1 line-clamp-2">{prod['name']}</h3>
                        <p class="text-xs text-gray-500 mb-3 flex-grow line-clamp-2">{prod['seo_desc']}</p>
                        <div class="mt-auto">
                            <div class="flex items-center gap-2 mb-3">
                                <span class="text-lg md:text-xl font-extrabold text-teal-600">Rs {prod['final_price']}</span>
                                <span class="text-xs text-gray-400 line-through">Rs {prod['base_price']}</span>
                            </div>
                            <a href="/checkout.html?id={prod['id']}" class="block text-center bg-gray-900 text-white py-2 rounded-lg text-sm font-bold hover:bg-teal-500 transition-colors w-full shadow-md">
                                Order Now
                            </a>
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
        section_slug = section["title"].lower().replace(" ", "-").replace("/", "-")
        cat_html = get_html_header(section["title"])
        
        # اس کیٹیگری کی ساری پروڈکٹس تلاش کرنا
        cat_products = [p for p in data["all_products"] if p['category'] == section["title"]]
        
        cat_html += f"""
        <div class="container mx-auto px-4 py-10">
            <h1 class="text-3xl md:text-4xl font-bold text-gray-800 mb-2">{section["title"]} Collection</h1>
            <p class="text-gray-500 mb-8">{len(cat_products)} Products Found</p>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
        """
        for prod in cat_products:
            cat_html += f"""
                <div class="product-card bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden flex flex-col relative">
                    <div class="image-container h-48 md:h-56 bg-gray-50 overflow-hidden relative">
                        <img src="{prod['image']}" alt="{prod['name']}" class="w-full h-full object-cover" loading="lazy">
                    </div>
                    <div class="p-4 flex flex-col flex-grow">
                        <h3 class="text-sm md:text-base font-bold text-gray-800 leading-tight mb-1">{prod['name']}</h3>
                        <p class="text-xs text-gray-500 mb-3 flex-grow line-clamp-2">{prod['seo_desc']}</p>
                        <div class="mt-auto">
                            <span class="text-xl font-extrabold text-teal-600 block mb-3">Rs {prod['final_price']}</span>
                            <a href="/checkout.html?id={prod['id']}" class="block text-center bg-gray-900 text-white py-2 rounded-lg text-sm font-bold hover:bg-teal-500 transition-colors shadow-md">
                                Order via COD
                            </a>
                        </div>
                    </div>
                </div>
            """
        cat_html += "</div></div>" + get_html_footer()
        with open(f"output/category/{section_slug}.html", "w", encoding="utf-8") as f:
            f.write(cat_html)

    # --- Checkout Page ---
    checkout_html = get_html_header("Secure Checkout")
    checkout_html += """
    <div class="container mx-auto px-4 py-12 max-w-2xl">
        <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
            <div class="bg-gradient-to-r from-teal-500 to-teal-600 p-8 text-center text-white">
                <h1 class="text-3xl font-extrabold"><i class="fas fa-money-bill-wave mr-2"></i> Cash on Delivery</h1>
                <p class="text-teal-100 mt-2 text-sm font-medium">Pay securely at your doorstep when the order arrives.</p>
            </div>
            <form class="p-6 md:p-8 space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-1.5">Full Name (پورا نام)</label>
                        <input type="text" class="w-full border border-gray-300 p-3 rounded-lg bg-gray-50 focus:bg-white focus:ring-2 focus:ring-teal-500 focus:border-teal-500 transition outline-none" required placeholder="Ali Abbas">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-1.5">Mobile Number (موبائل نمبر)</label>
                        <input type="tel" class="w-full border border-gray-300 p-3 rounded-lg bg-gray-50 focus:bg-white focus:ring-2 focus:ring-teal-500 focus:border-teal-500 transition outline-none" required placeholder="0300-1234567">
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-1.5">Complete Address (مکمل پتہ)</label>
                    <textarea rows="3" class="w-full border border-gray-300 p-3 rounded-lg bg-gray-50 focus:bg-white focus:ring-2 focus:ring-teal-500 focus:border-teal-500 transition outline-none" required placeholder="House No, Street, City..."></textarea>
                </div>
                
                <div class="mt-8 bg-teal-50 p-4 rounded-lg border border-teal-100 flex justify-between items-center">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-full bg-teal-100 text-teal-600 flex items-center justify-center">
                            <i class="fas fa-truck"></i>
                        </div>
                        <div>
                            <span class="block font-bold text-teal-900">Delivery Charges</span>
                            <span class="text-xs text-teal-700 font-medium">Free Delivery Nationwide</span>
                        </div>
                    </div>
                    <span class="font-extrabold text-xl text-teal-900">Rs 0</span>
                </div>

                <button type="button" onclick="alert('Congratulations! Your Order has been placed successfully. Our team will contact you soon.')" class="w-full bg-gray-900 text-white font-bold py-4 px-4 rounded-xl hover:bg-teal-500 transition-colors duration-300 shadow-lg text-lg mt-6">
                    Confirm Order (آرڈر کنفرم کریں)
                </button>
            </form>
        </div>
    </div>
    """
    checkout_html += get_html_footer()
    with open("output/checkout.html", "w", encoding="utf-8") as f:
        f.write(checkout_html)

if __name__ == "__main__":
    print("--- ASM VEO Automation Script Started ---")
    data = load_woocommerce_csv()
    build_store(data)
    print("--- ASM VEO Automation Script Finished ---")
