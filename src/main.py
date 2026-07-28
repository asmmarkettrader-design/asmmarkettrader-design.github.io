import os
import csv
import math
import re
import shutil
import random
from datetime import datetime

def get_price(price_str):
    try:
        if not price_str: return 0
        clean_price = re.sub(r'[^\d.]', '', str(price_str))
        return float(clean_price)
    except Exception:
        return 0

def clean_html(raw_html):
    clean_text = re.sub(r'<[^>]+>', ' ', str(raw_html))
    return ' '.join(clean_text.split())

def local_seo_desc(name, desc):
    if desc and len(desc) > 10:
        return desc[:150] + "..."
    return f"Buy {name} online in Pakistan at the best price. Premium quality with Cash on Delivery from ASM VEO."

# کیٹیگری کے لحاظ سے آئیکن سیٹ کرنے کا فنکشن
def get_category_icon(category_name):
    cat = category_name.lower()
    if 'perfume' in cat or 'fragrance' in cat: return 'fa-spray-can'
    if 'watch' in cat: return 'fa-clock'
    if 'electronics' in cat or 'tech' in cat: return 'fa-laptop'
    if 'cloth' in cat or 'fashion' in cat or 'apparel' in cat: return 'fa-tshirt'
    if 'shoe' in cat or 'footwear' in cat: return 'fa-shoe-prints'
    if 'beauty' in cat or 'makeup' in cat: return 'fa-magic'
    if 'home' in cat or 'kitchen' in cat: return 'fa-home'
    return 'fa-box-open'

def generate_reviews(product_name):
    names = ["Ali", "Ayesha", "Usman", "Fatima", "Bilal", "Zainab", "Hassan", "Maryam", "Ahmad", "Sana", "Zohaib", "Iqra"]
    templates = [
        "Bohot achi quality hai, delivery bhi time par mili.",
        "I am really impressed. {name} is amazing!",
        "Price ke hisaab se kaafi behtar hai. Recommended!",
        "Original product mili hai, jesa dikhaya tha wesa hi aaya.",
        "Mujhe yeh bohat pasand aaya. Thanks ASM VEO!",
        "100% Genuine product. Will definitely buy again."
    ]
    
    reviews_html = ""
    for _ in range(random.randint(3, 7)): 
        reviewer = random.choice(names)
        comment = random.choice(templates).format(name=product_name)
        stars = random.randint(4, 5)
        
        reviews_html += f"""
        <div class="border-b border-gray-100 py-4">
            <div class="flex items-center gap-2 mb-1">
                <div class="w-8 h-8 rounded-full bg-teal-100 text-teal-700 flex items-center justify-center font-bold">{reviewer[0]}</div>
                <span class="font-bold text-gray-800">{reviewer}</span>
                <span class="text-[10px] text-green-600 bg-green-50 px-2 py-0.5 rounded-full"><i class="fas fa-check-circle"></i> Verified Buyer</span>
            </div>
            <div class="text-yellow-400 text-xs mb-2">
                {"<i class='fas fa-star'></i>" * stars}
            </div>
            <p class="text-gray-600 text-sm">{comment}</p>
        </div>
        """
    return reviews_html

def get_html_header(title, seo_desc="ASM VEO - Premium Shopping Platform in Pakistan"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - ASM VEO</title>
    <!-- Auto SEO Meta Tags -->
    <meta name="description" content="{seo_desc}">
    <meta name="keywords" content="{title}, buy online, Pakistan, shopping, ASM Digital Solutions, ASM VEO, cash on delivery">
    <meta name="author" content="Ali Abbas - ASM Digital Solutions">
    <meta name="robots" content="index, follow">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; }}
        .product-card {{ transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }}
        .product-card:hover {{ transform: translateY(-8px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }}
        .image-zoom img {{ transition: transform 0.5s ease; }}
        .product-card:hover .image-zoom img {{ transform: scale(1.1); }}
        
        /* Custom Scrollbar for categories */
        .cat-scroll::-webkit-scrollbar {{ height: 6px; }}
        .cat-scroll::-webkit-scrollbar-track {{ background: #f1f1f1; border-radius: 10px; }}
        .cat-scroll::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 10px; }}
        .cat-scroll::-webkit-scrollbar-thumb:hover {{ background: #94a3b8; }}
    </style>
</head>
<body class="text-gray-800">
    <!-- Navbar -->
    <header class="bg-white shadow-md sticky top-0 z-50">
        <div class="container mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-4">
            <a href="/index.html" class="text-2xl md:text-3xl font-extrabold text-teal-700 tracking-tight flex items-center gap-2">
                <div class="bg-teal-600 text-white p-2 rounded-lg"><i class="fas fa-shopping-bag"></i></div>
                ASM VEO
            </a>
            
            <div class="flex-1 min-w-[250px] max-w-xl mx-0 md:mx-8 relative">
                <input type="text" id="searchInput" onkeypress="handleSearch(event)" placeholder="Search any product..." class="w-full bg-gray-100 border border-gray-200 focus:border-teal-500 rounded-full py-2.5 px-6 outline-none transition-all">
                <button onclick="executeSearch()" class="absolute right-4 top-2.5 text-gray-500 hover:text-teal-600"><i class="fas fa-search text-lg"></i></button>
            </div>
            
            <a href="/checkout.html" class="relative bg-gray-900 text-white px-5 py-2.5 rounded-full font-bold hover:bg-teal-600 transition-colors shadow-lg flex items-center gap-2 whitespace-nowrap">
                <i class="fas fa-shopping-cart"></i> 
                <span class="hidden md:inline">My Cart</span>
                <span id="cartCountBadge" class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-black w-6 h-6 flex items-center justify-center rounded-full border-2 border-white shadow-sm hidden">0</span>
            </a>
        </div>
    </header>
    
    <!-- Cart Logic JS -->
    <script>
    function updateCartBadge() {{
        let cart = JSON.parse(localStorage.getItem('asmveo_cart')) || [];
        let badge = document.getElementById('cartCountBadge');
        if(cart.length > 0) {{
            badge.innerText = cart.length;
            badge.style.display = 'flex';
        }} else {{
            badge.style.display = 'none';
        }}
    }}
    
    function addToCart(id, name, price, image, isDirectBuy = false) {{
        let cart = JSON.parse(localStorage.getItem('asmveo_cart')) || [];
        let sizeSelect = document.getElementById('productSize');
        let size = sizeSelect ? sizeSelect.value : 'Standard';
        
        cart.push({{ id: id, name: name, price: parseInt(price), image: image, size: size }});
        localStorage.setItem('asmveo_cart', JSON.stringify(cart));
        
        updateCartBadge();
        
        if(isDirectBuy) {{
            window.location.href = '/checkout.html';
        }} else {{
            alert(name + " has been added to your cart!");
        }}
    }}

    function handleSearch(e) {{
        if (e.key === 'Enter') executeSearch();
    }}
    function executeSearch() {{
        let val = document.getElementById('searchInput').value;
        if(val.trim() !== "") window.location.href = '/index.html?search=' + encodeURIComponent(val);
    }}
    
    window.addEventListener('DOMContentLoaded', updateCartBadge);
    </script>
"""

def get_html_footer():
    return """
    <!-- Footer -->
    <footer class="bg-gray-900 text-white mt-16 pt-12 pb-6 border-t-4 border-teal-500">
        <div class="container mx-auto px-4 grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div class="col-span-1 md:col-span-2">
                <h3 class="text-2xl font-bold mb-4 flex items-center gap-2"><i class="fas fa-shopping-bag text-teal-400"></i> ASM VEO</h3>
                <p class="text-gray-400 text-sm leading-relaxed mb-4">ASM VEO is a professional shopping platform by ASM Digital Solutions. We bring you top-tier products across multiple categories with nationwide Cash on Delivery and a 100% secure shopping experience.</p>
            </div>
            <div>
                <h3 class="text-lg font-bold mb-4">Management</h3>
                <ul class="space-y-3 text-gray-400 text-sm">
                    <li class="flex items-center gap-2"><i class="fas fa-user-tie text-teal-400"></i> CEO: Ali Abbas</li>
                    <li class="flex items-center gap-2"><i class="fas fa-building text-teal-400"></i> ASM Digital Solutions</li>
                    <li class="flex items-center gap-2"><i class="fab fa-whatsapp text-green-500 text-lg"></i> <a href="https://wa.me/923425478683" class="hover:text-white transition">0342 54 786 83</a></li>
                </ul>
            </div>
            <div>
                <h3 class="text-lg font-bold mb-4">Customer Support</h3>
                <p class="text-gray-400 text-sm mb-2"><i class="fas fa-money-bill-wave text-green-400 mr-2"></i> Cash on Delivery Available</p>
                <p class="text-gray-400 text-sm mb-2"><i class="fas fa-undo text-teal-400 mr-2"></i> Easy Return Policy</p>
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

def generate_sitemap(urls):
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    for url in urls:
        xml_content += f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{date_str}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>0.8</priority>\n  </url>\n"
    
    xml_content += '</urlset>'
    
    with open("output/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)

def process_woocommerce_csv():
    file_path = "woocommerce-products-export.csv"
    if not os.path.exists(file_path):
        print("❌ CSV File Not Found! Make sure 'woocommerce-products-export.csv' is in the folder.")
        return
        
    print("🚀 سکرپٹ شروع ہو گئی ہے! پرانا ڈیٹا ڈیلیٹ کیا جا رہا ہے...")
    
    if os.path.exists("output"):
        shutil.rmtree("output")
    os.makedirs("output/category", exist_ok=True)
    os.makedirs("output/product", exist_ok=True)
    
    with open("output/CNAME", "w") as f:
        f.write("www.asmveo.com")
    
    products_list = []
    categories_set = set()
    sitemap_urls = ["https://www.asmveo.com/", "https://www.asmveo.com/checkout.html"]
    
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            if not name: continue
            
            # 1. صرف تصویر والی پروڈکٹس رکھیں
            images_raw = row.get('Images', '').strip()
            if not images_raw: 
                continue 
                
            image = images_raw.split(',')[0].strip()
            
            base_price = get_price(row.get('Sale price', '') or row.get('Regular price', ''))
            if base_price == 0: continue
            
            # پرائسنگ سٹرکچر
            final_price = math.ceil(base_price * 1.30)
            fake_regular_price = math.ceil(final_price * 1.61) 
            
            cat_raw = row.get('Categories', 'Uncategorized')
            category = cat_raw.split(',')[0].strip() if cat_raw else 'Exclusive'
            categories_set.add(category)
            
            desc_raw = row.get('Short description', '') or row.get('Description', '')
            clean_description = clean_html(desc_raw)
            seo_desc = local_seo_desc(name, clean_description)
            
            # 2. سائز چیک کریں (صرف تب شو ہوگا جب ڈسکرپشن میں ذکر ہو)
            size_keywords = r'\b(size|small|medium|large|xl|xxl|cm|inches)\b'
            has_size = bool(re.search(size_keywords, clean_description.lower()))
            
            product_id = row.get('ID', str(len(products_list)+1))
            slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-') + f"-{product_id}"
            
            sitemap_urls.append(f"https://www.asmveo.com/product/{slug}.html")
            
            products_list.append({
                'id': product_id,
                'slug': slug,
                'name': name,
                'category': category,
                'fake_price': fake_regular_price,
                'final_price': final_price,
                'image': image,
                'seo_desc': seo_desc,
                'full_desc': clean_description,
                'has_size': has_size
            })

    print(f"✔ کل {len(products_list)} پروڈکٹس پراسیس ہو رہی ہیں (صرف تصاویر والی)...")
    
    # ================= GENERATE PRODUCT PAGES =================
    for prod in products_list:
        prod_html = get_html_header(prod['name'], prod['seo_desc'])
        reviews_section = generate_reviews(prod['name'])
        
        # سائز ڈراپ ڈاؤن کنڈیشن
        size_html = ""
        if prod['has_size']:
            size_html = """
            <div class="mb-6">
                <label class="block text-sm font-bold text-gray-700 mb-2">Select Size</label>
                <select id="productSize" class="w-full md:w-2/3 border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-teal-500 bg-white font-semibold shadow-sm">
                    <option value="Small (S)">Small (S)</option>
                    <option value="Medium (M)" selected>Medium (M)</option>
                    <option value="Large (L)">Large (L)</option>
                    <option value="Extra Large (XL)">Extra Large (XL)</option>
                </select>
            </div>
            """
            
        prod_html += f"""
        <div class="container mx-auto px-4 py-10">
            <nav class="text-sm text-gray-500 mb-6 font-semibold">
                <a href="/index.html" class="hover:text-teal-600 transition">Home</a> &gt; 
                <a href="/category/{re.sub(r'[^a-z0-9]+', '-', prod['category'].lower())}.html" class="hover:text-teal-600 transition">{prod['category']}</a> &gt; 
                <span class="text-gray-800">{prod['name']}</span>
            </nav>
            
            <div class="bg-white rounded-3xl shadow-xl border border-gray-100 overflow-hidden flex flex-col md:flex-row mb-12">
                <div class="md:w-1/2 p-6 flex justify-center items-center bg-gray-50 border-r border-gray-100 relative">
                    <div class="absolute top-4 left-4 bg-red-500 text-white text-xs font-black px-3 py-1.5 rounded-lg z-10 shadow-md">SALE</div>
                    <img src="{prod['image']}" alt="{prod['name']}" class="max-h-[500px] object-contain rounded-xl hover:scale-105 transition duration-500">
                </div>
                <div class="md:w-1/2 p-8 md:p-12 flex flex-col justify-center">
                    <span class="text-xs font-bold uppercase tracking-widest text-teal-600 mb-2">{prod['category']}</span>
                    <h1 class="text-3xl md:text-4xl font-extrabold text-gray-900 mb-4">{prod['name']}</h1>
                    
                    <div class="flex items-center gap-3 mb-6">
                        <div class="text-yellow-400 text-sm"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star-half-alt"></i></div>
                        <span class="text-sm font-semibold text-gray-500">(Verified Reviews)</span>
                    </div>

                    <div class="flex items-center gap-4 mb-6 bg-gray-50 p-4 rounded-2xl w-fit border border-gray-200">
                        <span class="text-4xl font-black text-teal-700">Rs {prod['final_price']}</span>
                        <span class="text-xl text-gray-400 font-bold line-through">Rs {prod['fake_price']}</span>
                    </div>
                    
                    {size_html}

                    <p class="text-gray-600 mb-8 leading-relaxed">{prod['full_desc'][:400] if len(prod['full_desc']) > 50 else prod['seo_desc']}</p>
                    
                    <!-- 3. Add to Cart & Buy Now Buttons Separate -->
                    <div class="flex flex-col sm:flex-row gap-4 w-full md:w-5/6">
                        <button onclick="addToCart('{prod['id']}', '{prod['name'].replace("'", "")}', '{prod['final_price']}', '{prod['image']}', false)" class="flex-1 bg-white text-teal-700 border-2 border-teal-600 text-center py-4 rounded-xl font-black text-lg hover:bg-teal-50 transition-all shadow-sm flex justify-center items-center gap-2">
                            <i class="fas fa-cart-plus"></i> Add to Cart
                        </button>
                        <button onclick="addToCart('{prod['id']}', '{prod['name'].replace("'", "")}', '{prod['final_price']}', '{prod['image']}', true)" class="flex-1 bg-gray-900 text-white text-center py-4 rounded-xl font-black text-lg hover:bg-teal-600 transition-all shadow-lg transform hover:-translate-y-1 flex justify-center items-center gap-2">
                            <i class="fas fa-bolt"></i> Buy Now
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="bg-white rounded-3xl shadow-lg border border-gray-100 p-8">
                <h2 class="text-2xl font-extrabold text-gray-900 mb-6 border-b pb-4">Customer Reviews</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div>{reviews_section}</div>
                    <div class="bg-gray-50 p-6 rounded-2xl h-fit border border-gray-200">
                        <h3 class="font-bold text-lg mb-2">Write a Review</h3>
                        <p class="text-sm text-gray-500 mb-4">Only verified buyers can leave a review after receiving the product.</p>
                        <div class="flex items-center gap-2 text-teal-600 font-bold bg-teal-50 p-3 rounded-lg border border-teal-100">
                            <i class="fas fa-lock"></i> Review form is currently locked.
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """ + get_html_footer()
        
        with open(f"output/product/{prod['slug']}.html", "w", encoding="utf-8") as f:
            f.write(prod_html)

    # ================= GENERATE HOME & CATEGORY PAGES =================
    sections_dict = {}
    for p in products_list:
        c = p['category']
        if c not in sections_dict: sections_dict[c] = []
        sections_dict[c].append(p)

    home_html = get_html_header("Home")
    
    # 4. ہوم پیج پر کیٹیگری آئیکنز کا سیکشن
    cat_icons_html = """
    <div class="bg-white py-6 border-b border-gray-200 shadow-sm mb-8">
        <div class="container mx-auto px-4">
            <h2 class="text-lg font-bold text-gray-800 mb-4">Shop by Categories</h2>
            <div class="flex overflow-x-auto gap-6 pb-4 cat-scroll">
    """
    for cat in categories_set:
        icon = get_category_icon(cat)
        cat_slug = re.sub(r'[^a-z0-9]+', '-', cat.lower())
        cat_icons_html += f"""
                <a href="/category/{cat_slug}.html" class="flex flex-col items-center gap-2 min-w-[80px] group">
                    <div class="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center text-teal-600 group-hover:bg-teal-600 group-hover:text-white transition-all shadow-sm">
                        <i class="fas {icon} text-2xl"></i>
                    </div>
                    <span class="text-xs font-bold text-gray-700 text-center">{cat}</span>
                </a>
        """
    cat_icons_html += "</div></div></div>"
    
    home_html += cat_icons_html + """
    <script>
        window.addEventListener('DOMContentLoaded', (event) => {
            const urlParams = new URLSearchParams(window.location.search);
            const searchQuery = urlParams.get('search');
            if (searchQuery) {
                const query = searchQuery.toLowerCase();
                const cards = document.querySelectorAll('.product-card');
                let found = 0;
                cards.forEach(card => {
                    if (card.querySelector('.prod-title').innerText.toLowerCase().includes(query)) {
                        card.style.display = 'flex';
                        found++;
                    } else {
                        card.style.display = 'none';
                    }
                });
                document.getElementById('searchResultsHeading').innerText = `Search Results for "${searchQuery}" (${found} found)`;
                document.getElementById('searchResultsHeading').style.display = 'block';
            }
        });
    </script>
    <div class='container mx-auto px-4'>
        <h2 id="searchResultsHeading" class="text-2xl font-extrabold text-teal-700 mb-6 hidden border-b pb-2"></h2>
    """
    
    for cat_name, prods in sections_dict.items():
        cat_slug = re.sub(r'[^a-z0-9]+', '-', cat_name.lower())
        sitemap_urls.append(f"https://www.asmveo.com/category/{cat_slug}.html")
        
        # Category Page Build
        cat_html = get_html_header(cat_name)
        cat_html += f"""
        <div class="bg-gray-100 py-10 mb-8 border-b border-gray-200">
            <div class="container mx-auto px-4 text-center">
                <div class="inline-block p-4 rounded-full bg-white text-teal-600 shadow-sm mb-4"><i class="fas {get_category_icon(cat_name)} text-4xl"></i></div>
                <h1 class="text-3xl md:text-5xl font-black text-gray-900">{cat_name}</h1>
                <p class="text-gray-600 mt-3 font-semibold">{len(prods)} Exclusive Products</p>
            </div>
        </div>
        <div class="container mx-auto px-4 pb-12"><div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
        """
        
        home_html += f"""
        <div class="mb-14 category-section">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl md:text-3xl font-black text-gray-800 border-l-4 border-teal-500 pl-4">{cat_name}</h2>
                <a href="/category/{cat_slug}.html" class="text-teal-600 font-bold text-sm bg-teal-50 px-5 py-2.5 rounded-full hover:bg-teal-600 hover:text-white transition-all">View All <i class="fas fa-arrow-right ml-1"></i></a>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
        """
        
        for idx, prod in enumerate(prods):
            card_ui = f"""
                <div class="product-card bg-white rounded-2xl shadow-sm hover:shadow-xl border border-gray-100 overflow-hidden flex flex-col relative cursor-pointer" onclick="window.location.href='/product/{prod['slug']}.html'">
                    <div class="image-zoom h-48 md:h-60 bg-gray-50 overflow-hidden relative border-b border-gray-100">
                        <img src="{prod['image']}" alt="{prod['name']}" class="w-full h-full object-cover" loading="lazy">
                    </div>
                    <div class="p-4 flex flex-col flex-grow">
                        <span class="text-[10px] font-bold text-teal-600 uppercase tracking-wider mb-1">{prod['category']}</span>
                        <h3 class="prod-title text-sm md:text-base font-bold text-gray-900 leading-tight mb-2 line-clamp-2">{prod['name']}</h3>
                        <div class="mt-auto">
                            <div class="flex items-center gap-2 mb-3">
                                <span class="text-lg md:text-xl font-black text-gray-900">Rs {prod['final_price']}</span>
                                <span class="text-xs text-gray-400 font-bold line-through">Rs {prod['fake_price']}</span>
                            </div>
                            <!-- Direct Add to Cart from Grid -->
                            <button onclick="event.stopPropagation(); addToCart('{prod['id']}', '{prod['name'].replace("'", "")}', '{prod['final_price']}', '{prod['image']}', false)" class="block text-center bg-teal-50 text-teal-700 py-2.5 rounded-xl text-sm font-bold w-full border border-teal-100 hover:bg-teal-600 hover:text-white transition-colors">
                                <i class="fas fa-cart-shopping mr-1"></i> Add
                            </button>
                        </div>
                    </div>
                </div>
            """
            cat_html += card_ui
            if idx < 10: home_html += card_ui
            
        cat_html += "</div></div>" + get_html_footer()
        with open(f"output/category/{cat_slug}.html", "w", encoding="utf-8") as f:
            f.write(cat_html)
            
        home_html += "</div></div>"
    
    home_html += "</div>" + get_html_footer()
    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(home_html)

    # ================= 5. GENERATE ADVANCED CHECKOUT PAGE (CART + WHATSAPP) =================
    pak_cities = ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Multan", "Peshawar", "Quetta", "Gujranwala", "Sialkot", "Hyderabad", "Bahawalpur", "Sargodha", "Other"]
    city_options = "".join([f"<option value='{city}'>{city}</option>" for city in pak_cities])
    
    checkout_html = get_html_header("Cart & Checkout")
    checkout_html += f"""
    <div class="container mx-auto px-4 py-12 max-w-5xl">
        <div class="flex flex-col lg:flex-row gap-8">
            
            <!-- Cart Items Display Section -->
            <div class="lg:w-1/2">
                <div class="bg-white rounded-3xl shadow-lg border border-gray-100 p-6 mb-6">
                    <h2 class="text-2xl font-black text-gray-900 border-b border-gray-100 pb-4 mb-4"><i class="fas fa-shopping-cart text-teal-600 mr-2"></i> Your Cart Items</h2>
                    <div id="cartItemsContainer" class="space-y-4 max-h-[400px] overflow-y-auto pr-2 cat-scroll">
                        <!-- Items will be loaded here by JS -->
                    </div>
                    <button onclick="clearCart()" class="mt-4 text-sm text-red-500 font-bold hover:underline"><i class="fas fa-trash-alt mr-1"></i> Clear Cart</button>
                </div>
                
                <!-- 6. WhatsApp Order Button -->
                <button onclick="orderViaWhatsApp()" class="w-full bg-[#25D366] text-white font-black py-4 rounded-xl shadow-lg hover:bg-green-600 transition-all flex justify-center items-center gap-2 text-lg transform hover:-translate-y-1">
                    <i class="fab fa-whatsapp text-2xl"></i> Order directly via WhatsApp
                </button>
                <p class="text-center text-xs text-gray-500 mt-2 font-semibold">Prefer chatting? Send your order to our team.</p>
            </div>

            <!-- Form Section -->
            <div class="lg:w-1/2 bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100">
                <div class="bg-gray-900 p-6 text-white relative">
                    <div class="absolute top-0 left-0 w-full h-1 bg-teal-500"></div>
                    <h1 class="text-xl font-extrabold"><i class="fas fa-map-marker-alt text-teal-400 mr-2"></i> Shipping Details (Formspree)</h1>
                </div>
                
                <form id="checkoutForm" class="p-6 space-y-4">
                    <input type="hidden" name="_subject" value="New Bulk Order Received on ASM VEO!">
                    <!-- Hidden input to send entire cart data to Formspree -->
                    <input type="hidden" name="Order_Details" id="cartDetailsInput" value="">
                    
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-1">Full Name <span class="text-red-500">*</span></label>
                        <input type="text" id="waName" name="Full_Name" class="w-full border-2 border-gray-200 p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-500 outline-none" required>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-bold text-gray-700 mb-1">Mobile Number <span class="text-red-500">*</span></label>
                            <input type="tel" id="waPhone" name="Phone_Number" class="w-full border-2 border-gray-200 p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-500 outline-none" required>
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-gray-700 mb-1">City <span class="text-red-500">*</span></label>
                            <select id="waCity" name="City" class="w-full border-2 border-gray-200 p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-500 outline-none font-semibold" required>
                                <option value="" disabled selected>Select City</option>
                                {city_options}
                            </select>
                        </div>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-1">Complete Address <span class="text-red-500">*</span></label>
                        <textarea id="waAddress" name="Address" rows="2" class="w-full border-2 border-gray-200 p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-500 outline-none" required></textarea>
                    </div>

                    <div class="bg-teal-50 p-4 rounded-xl border border-teal-100 mt-4">
                        <div class="flex justify-between items-center mb-2 text-sm font-bold text-gray-700">
                            <span>Subtotal:</span> <span id="subTotalDisplay">Rs 0</span>
                        </div>
                        <div class="flex justify-between items-center mb-2 text-sm font-bold text-teal-700 border-b border-teal-200 pb-2">
                            <span>Delivery:</span> <span>Rs 250</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-lg font-black text-gray-900">Total (COD):</span> 
                            <span class="text-2xl font-black text-teal-700" id="grandTotalDisplay">Rs 0</span>
                        </div>
                    </div>

                    <button type="submit" id="submitBtn" class="w-full bg-gray-900 text-white font-black py-4 rounded-xl hover:bg-teal-600 transition-all shadow-xl text-lg mt-2">
                        <i class="fas fa-check-circle mr-2"></i> Confirm Order
                    </button>
                </form>
            </div>
        </div>
    </div>
    
    <script>
        let cartData = [];
        let grandTotal = 0;

        function renderCart() {{
            cartData = JSON.parse(localStorage.getItem('asmveo_cart')) || [];
            let container = document.getElementById('cartItemsContainer');
            let subTotalDisplay = document.getElementById('subTotalDisplay');
            let grandTotalDisplay = document.getElementById('grandTotalDisplay');
            let formInput = document.getElementById('cartDetailsInput');
            
            if(cartData.length === 0) {{
                container.innerHTML = '<div class="text-center py-8 text-gray-400 font-bold"><i class="fas fa-box-open text-4xl mb-3"></i><br>Your cart is empty.</div>';
                subTotalDisplay.innerText = "Rs 0";
                grandTotalDisplay.innerText = "Rs 0";
                document.getElementById('submitBtn').disabled = true;
                return;
            }}
            
            document.getElementById('submitBtn').disabled = false;
            let html = "";
            let subtotal = 0;
            let orderText = "";
            
            cartData.forEach((item, index) => {{
                subtotal += item.price;
                orderText += `[${item.name} | Size: ${item.size} | Rs ${item.price}] `;
                html += `
                <div class="flex items-center gap-4 bg-gray-50 p-3 rounded-xl border border-gray-100 relative">
                    <img src="${{item.image}}" class="w-16 h-16 object-cover rounded-lg border border-gray-200">
                    <div class="flex-1">
                        <h4 class="font-bold text-sm text-gray-900 leading-tight">${{item.name}}</h4>
                        <p class="text-xs text-gray-500 mt-1">Size: ${{item.size}}</p>
                        <p class="text-teal-700 font-black mt-1">Rs ${{item.price}}</p>
                    </div>
                    <button onclick="removeItem(${{index}})" class="absolute top-2 right-2 text-gray-400 hover:text-red-500"><i class="fas fa-times-circle text-lg"></i></button>
                </div>`;
            }});
            
            grandTotal = subtotal + 250;
            container.innerHTML = html;
            subTotalDisplay.innerText = "Rs " + subtotal;
            grandTotalDisplay.innerText = "Rs " + grandTotal;
            
            // Setting hidden input for Formspree
            formInput.value = orderText + " || Total to Pay: Rs " + grandTotal;
        }}

        function removeItem(index) {{
            cartData.splice(index, 1);
            localStorage.setItem('asmveo_cart', JSON.stringify(cartData));
            updateCartBadge();
            renderCart();
        }}
        
        function clearCart() {{
            localStorage.removeItem('asmveo_cart');
            updateCartBadge();
            renderCart();
        }}

        // WhatsApp Order Logic
        function orderViaWhatsApp() {{
            if(cartData.length === 0) {{ alert("Your cart is empty!"); return; }}
            
            let name = document.getElementById('waName').value || "Customer";
            let phone = document.getElementById('waPhone').value || "Not provided";
            let city = document.getElementById('waCity').value || "Not provided";
            let address = document.getElementById('waAddress').value || "Not provided";
            
            let text = `*New Order from ASM VEO*%0A%0A`;
            text += `*Name:* ${name}%0A*Phone:* ${phone}%0A*City:* ${city}%0A*Address:* ${address}%0A%0A*Order Details:*%0A`;
            
            cartData.forEach((item, i) => {{
                text += `${i+1}. ${item.name} (Size: ${item.size}) - Rs ${item.price}%0A`;
            }});
            
            text += `%0A*Delivery:* Rs 250%0A*Total Amount (COD):* Rs ${grandTotal}`;
            
            window.open('https://wa.me/923425478683?text=' + text, '_blank');
        }}

        document.getElementById('checkoutForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            const btn = document.getElementById('submitBtn');
            btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Processing...';
            btn.disabled = true;

            const formData = new FormData(this);

            fetch('https://formspree.io/f/xjgnlgpw', {{
                method: 'POST',
                body: formData,
                headers: {{ 'Accept': 'application/json' }}
            }}).then(response => {{
                if (response.ok) {{
                    alert('Order Confirmed! Total Amount to pay on delivery is Rs ' + grandTotal);
                    clearCart();
                    window.location.href = '/index.html';
                }} else {{
                    alert('Oops! There was a problem submitting your order.');
                    btn.innerHTML = '<i class="fas fa-check-circle mr-2"></i> Confirm Order';
                    btn.disabled = false;
                }}
            }}).catch(error => {{
                alert('Network Error! Please try again.');
                btn.innerHTML = '<i class="fas fa-check-circle mr-2"></i> Confirm Order';
                btn.disabled = false;
            }});
        }});
        
        // Initialize cart on load
        window.addEventListener('DOMContentLoaded', renderCart);
    </script>
    """
    checkout_html += get_html_footer()
    with open("output/checkout.html", "w", encoding="utf-8") as f:
        f.write(checkout_html)
        
    generate_sitemap(sitemap_urls)
    print("🎉 تمام فائلز، پیجز، کارٹ سسٹم اور واٹس ایپ آرڈرنگ کامیابی کے ساتھ بن چکے ہیں!")

if __name__ == "__main__":
    process_woocommerce_csv()
