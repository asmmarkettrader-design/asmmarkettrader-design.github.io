import os
import csv
import math
import re
import time

def get_price(price_str):
    """سٹرنگ میں سے قیمت نکال کر اسے نمبر میں تبدیل کرتا ہے"""
    try:
        if not price_str: return 0
        clean_price = re.sub(r'[^\d.]', '', str(price_str))
        return float(clean_price)
    except Exception:
        return 0

def clean_html(raw_html):
    """ڈسکرپشن میں موجود فالتو HTML ٹیگز کو صاف کرتا ہے"""
    clean_text = re.sub(r'<[^>]+>', ' ', str(raw_html))
    return ' '.join(clean_text.split())

def local_seo_desc(name, desc):
    """بغیر انٹرنیٹ کے تیزی سے ایس ای او ڈسکرپشن بناتا ہے"""
    if desc and len(desc) > 10:
        return desc[:120] + "..."
    return f"Buy {name} online in Pakistan at the best price. Premium quality with Cash on Delivery."

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
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; }}
        .product-card {{ transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }}
        .product-card:hover {{ transform: translateY(-8px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04); }}
        .image-zoom img {{ transition: transform 0.5s ease; }}
        .product-card:hover .image-zoom img {{ transform: scale(1.1); }}
        .category-icon {{ transition: all 0.3s ease; }}
        .category-item:hover .category-icon {{ transform: scale(1.1) rotate(5deg); background-color: #0d9488; color: white; }}
    </style>
</head>
<body class="text-gray-800">
    <!-- Navbar -->
    <header class="bg-white shadow-md sticky top-0 z-50">
        <div class="container mx-auto px-4 py-3 flex justify-between items-center">
            <a href="/index.html" class="text-2xl md:text-3xl font-extrabold text-teal-700 tracking-tight flex items-center gap-2">
                <div class="bg-teal-600 text-white p-2 rounded-lg"><i class="fas fa-shopping-bag"></i></div>
                ASM VEO
            </a>
            <div class="hidden md:flex flex-1 max-w-xl mx-8 relative">
                <input type="text" placeholder="Search for products, brands and more..." class="w-full bg-gray-100 border border-transparent focus:border-teal-500 rounded-full py-2.5 px-6 outline-none transition-all">
                <button class="absolute right-4 top-2.5 text-gray-500 hover:text-teal-600"><i class="fas fa-search text-lg"></i></button>
            </div>
            <a href="/checkout.html" class="bg-gray-900 text-white px-5 py-2.5 rounded-full font-bold hover:bg-teal-600 transition-colors shadow-lg flex items-center gap-2">
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
                </ul>
            </div>
            <div>
                <h3 class="text-lg font-bold mb-4">Safe & Secure</h3>
                <p class="text-gray-400 text-sm mb-2"><i class="fas fa-money-bill-wave text-green-400 mr-2"></i> Cash on Delivery Available</p>
                <p class="text-gray-400 text-sm"><i class="fas fa-shield-alt text-teal-400 mr-2"></i> 100% Secure Checkout</p>
            </div>
        </div>
        <div class="border-t border-gray-800 text-center pt-6">
            <p class="text-gray-500 text-sm">&copy; 2026 ASM Digital Solutions. All Rights Reserved.</p>
        </div>
    </footer>
</body>
</html>
"""

def generate_website_live(products, categories_set, is_final=False):
    """یہ فنکشن ویب سائٹ کی فائلز کو لائیو لکھتا ہے تاکہ آپ ریفریش کر کے دیکھ سکیں"""
    os.makedirs("output/category", exist_ok=True)
    with open("output/CNAME", "w") as f:
        f.write("www.asmveo.com")

    # پروڈکٹس کو کیٹیگریز میں بانٹنا
    sections_dict = {}
    for p in products:
        c = p['category']
        if c not in sections_dict:
            sections_dict[c] = []
        sections_dict[c].append(p)

    # ================= HOME PAGE =================
    html = get_html_header("Home")
    
    # ہیرو سیکشن اور کیٹیگریز
    html += """
    <div class="bg-white py-8 shadow-sm mb-8">
        <div class="container mx-auto px-4">
            <h2 class="text-2xl font-extrabold text-gray-800 mb-6 flex items-center gap-2"><i class="fas fa-fire text-orange-500"></i> Top Categories</h2>
            <div class="flex overflow-x-auto gap-4 pb-4 scrollbar-hide">
    """
    
    icons = ['fa-tshirt', 'fa-shoe-prints', 'fa-glasses', 'fa-gem', 'fa-mobile-screen', 'fa-home', 'fa-clock']
    for idx, cat in enumerate(list(categories_set)[:10]):
        icon = icons[idx % len(icons)]
        cat_slug = cat.lower().replace(" ", "-").replace("/", "-")
        html += f"""
                <a href="/category/{cat_slug}.html" class="category-item flex flex-col items-center min-w-[80px] cursor-pointer group">
                    <div class="category-icon w-16 h-16 rounded-full bg-gray-50 border border-gray-200 flex items-center justify-center text-gray-600 shadow-sm mb-2">
                        <i class="fas {icon} text-2xl"></i>
                    </div>
                    <span class="text-xs font-semibold text-gray-700 text-center">{cat}</span>
                </a>
        """
    html += "</div></div></div>"

    html += "<div class='container mx-auto px-4'>"
    for cat_name, prods in sections_dict.items():
        cat_slug = cat_name.lower().replace(" ", "-").replace("/", "-")
        html += f"""
        <div class="mb-12">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl md:text-3xl font-extrabold text-gray-800 border-l-4 border-teal-500 pl-3">{cat_name}</h2>
                <a href="/category/{cat_slug}.html" class="text-teal-600 font-bold text-sm bg-teal-50 px-4 py-2 rounded-full hover:bg-teal-100 transition">See All <i class="fas fa-chevron-right ml-1 text-xs"></i></a>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3 md:gap-5">
        """
        # ہوم پیج پر ہر کیٹیگری کی پہلی 10 پروڈکٹس
        for prod in prods[:10]:
            html += f"""
                <div class="product-card bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col relative">
                    <div class="absolute top-3 right-3 bg-red-500 text-white text-[10px] font-black px-2 py-1 rounded-md z-10 shadow-md tracking-wider">30% OFF</div>
                    <div class="image-zoom h-48 md:h-60 bg-gray-100 overflow-hidden relative">
                        <img src="{prod['image']}" alt="{prod['name']}" class="w-full h-full object-cover" loading="lazy">
                    </div>
                    <div class="p-4 flex flex-col flex-grow">
                        <span class="text-[10px] uppercase font-bold text-teal-600 tracking-wider mb-1">{prod['category']}</span>
                        <h3 class="text-sm md:text-base font-bold text-gray-900 leading-tight mb-2 line-clamp-2">{prod['name']}</h3>
                        <p class="text-xs text-gray-500 mb-4 flex-grow line-clamp-2">{prod['seo_desc']}</p>
                        <div class="mt-auto">
                            <div class="flex items-center gap-2 mb-3">
                                <span class="text-lg md:text-xl font-extrabold text-gray-900">Rs {prod['final_price']}</span>
                                <span class="text-xs text-gray-400 line-through">Rs {prod['base_price']}</span>
                            </div>
                            <a href="/checkout.html?id={prod['id']}&price={prod['final_price']}" class="block text-center bg-teal-600 text-white py-2.5 rounded-xl text-sm font-bold hover:bg-gray-900 transition-colors shadow-md w-full">
                                Buy Now
                            </a>
                        </div>
                    </div>
                </div>
            """
        html += "</div></div>"
    html += "</div>" + get_html_footer()
    
    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(html)

    # ================= CATEGORY PAGES =================
    for cat_name, prods in sections_dict.items():
        cat_slug = cat_name.lower().replace(" ", "-").replace("/", "-")
        cat_html = get_html_header(cat_name)
        cat_html += f"""
        <div class="bg-gray-100 py-8 mb-8 border-b border-gray-200">
            <div class="container mx-auto px-4">
                <h1 class="text-3xl md:text-4xl font-extrabold text-gray-900">{cat_name}</h1>
                <p class="text-gray-500 mt-2 font-medium">{len(prods)} Exclusive Products Found</p>
            </div>
        </div>
        <div class="container mx-auto px-4 pb-12">
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
        """
        for prod in prods:
            cat_html += f"""
                <div class="product-card bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col relative">
                    <div class="image-zoom h-48 md:h-60 bg-gray-100 overflow-hidden relative">
                        <img src="{prod['image']}" alt="{prod['name']}" class="w-full h-full object-cover" loading="lazy">
                    </div>
                    <div class="p-4 flex flex-col flex-grow">
                        <h3 class="text-sm md:text-base font-bold text-gray-900 leading-tight mb-2 line-clamp-2">{prod['name']}</h3>
                        <div class="mt-auto">
                            <span class="text-xl font-extrabold text-teal-600 block mb-3">Rs {prod['final_price']}</span>
                            <a href="/checkout.html?id={prod['id']}" class="block text-center bg-gray-900 text-white py-2.5 rounded-xl text-sm font-bold hover:bg-teal-600 transition-colors shadow-md">Order via COD</a>
                        </div>
                    </div>
                </div>
            """
        cat_html += "</div></div>" + get_html_footer()
        with open(f"output/category/{cat_slug}.html", "w", encoding="utf-8") as f:
            f.write(cat_html)

    # ================= CHECKOUT PAGE =================
    if is_final:
        checkout_html = get_html_header("Secure Checkout")
        checkout_html += """
        <div class="container mx-auto px-4 py-12 max-w-2xl">
            <div class="bg-white rounded-3xl shadow-2xl overflow-hidden border border-gray-100">
                <div class="bg-gray-900 p-8 text-center text-white relative overflow-hidden">
                    <div class="absolute top-0 left-0 w-full h-1 bg-teal-500"></div>
                    <h1 class="text-3xl font-extrabold relative z-10"><i class="fas fa-box-open mr-2 text-teal-400"></i> Cash on Delivery</h1>
                    <p class="text-gray-400 mt-2 text-sm font-medium relative z-10">Pay securely when the rider delivers your parcel.</p>
                </div>
                <form class="p-6 md:p-10 space-y-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label class="block text-sm font-bold text-gray-700 mb-2">Full Name</label>
                            <input type="text" class="w-full border-2 border-gray-200 p-3.5 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-500 outline-none transition" required placeholder="e.g. Ali Abbas">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-gray-700 mb-2">Mobile Number</label>
                            <input type="tel" class="w-full border-2 border-gray-200 p-3.5 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-500 outline-none transition" required placeholder="0300-XXXXXXX">
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-2">Complete Delivery Address</label>
                        <textarea rows="3" class="w-full border-2 border-gray-200 p-3.5 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-500 outline-none transition" required placeholder="House No, Street, City Name..."></textarea>
                    </div>
                    
                    <div class="mt-8 bg-teal-50 p-5 rounded-2xl border border-teal-100 flex justify-between items-center">
                        <div class="flex items-center gap-4">
                            <div class="w-12 h-12 rounded-full bg-white text-teal-600 flex items-center justify-center shadow-sm">
                                <i class="fas fa-truck-fast text-xl"></i>
                            </div>
                            <div>
                                <span class="block font-bold text-gray-900">Delivery Options</span>
                                <span class="text-xs text-teal-700 font-bold">Standard Free Delivery</span>
                            </div>
                        </div>
                        <span class="font-extrabold text-2xl text-teal-700">Rs 0</span>
                    </div>

                    <button type="button" onclick="alert('Order Confirmed! Your order will be delivered soon.')" class="w-full bg-teal-600 text-white font-black py-4 px-4 rounded-2xl hover:bg-gray-900 transition-all duration-300 shadow-xl text-lg mt-6 transform hover:-translate-y-1">
                        Confirm Order Now
                    </button>
                </form>
            </div>
        </div>
        """
        checkout_html += get_html_footer()
        with open("output/checkout.html", "w", encoding="utf-8") as f:
            f.write(checkout_html)

def process_woocommerce_csv():
    file_path = "woocommerce-products-export.csv"
    if not os.path.exists(file_path):
        print("❌ CSV File Not Found!")
        return
        
    print("🚀 سکرپٹ شروع ہو گئی ہے! لائیو اپڈیٹس آن ہیں...")
    os.makedirs("output", exist_ok=True)
    
    products_list = []
    categories_set = set()
    
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        
        for row in reader:
            name = row.get('Name', '').strip()
            if not name: continue
                
            base_price = get_price(row.get('Sale price', '') or row.get('Regular price', ''))
            if base_price == 0: continue
                
            final_price = math.ceil(base_price * 1.30) # 30% Profit
            
            cat_raw = row.get('Categories', 'Uncategorized')
            category = cat_raw.split(',')[0].strip() if cat_raw else 'Hot Items'
            categories_set.add(category)
            
            images_raw = row.get('Images', '')
            image = images_raw.split(',')[0].strip() if images_raw else 'https://via.placeholder.com/500'
            
            desc_raw = row.get('Short description', '') or row.get('Description', '')
            clean_description = clean_html(desc_raw)
            seo_desc = local_seo_desc(name, clean_description)
            
            products_list.append({
                'id': row.get('ID', str(len(products_list)+1)),
                'name': name,
                'category': category,
                'base_price': int(base_price),
                'final_price': final_price,
                'image': image,
                'seo_desc': seo_desc
            })
            
            count += 1
            
            # === لائیو ریفریش کا جادو ===
            # ہر 100 پروڈکٹس کے بعد ویب سائٹ کی فائلز لائیو رائٹ (Write) ہو جائیں گی۔
            # آپ کسی بھی وقت ریفریش کریں گے تو پچھلی 100 پروڈکٹس لسٹ ہو چکی ہوں گی!
            if count % 100 == 0:
                print(f"[{count} Products Processed] ویب سائٹ لائیو اپڈیٹ ہو رہی ہے... آپ پیج ریفریش کر سکتے ہیں۔")
                generate_website_live(products_list, categories_set, is_final=False)
                
    # جب سارا ڈیٹا ختم ہو جائے تو فائنل اپڈیٹ (مع چیک آؤٹ پیج کے)
    print(f"✅ تمام {len(products_list)} پروڈکٹس پروسیس ہو گئیں۔ فائنل ویب سائٹ بن رہی ہے...")
    generate_website_live(products_list, categories_set, is_final=True)
    print("🎉 سکرپٹ کامیابی کے ساتھ 100% مکمل ہو گئی!")

if __name__ == "__main__":
    process_woocommerce_csv()
