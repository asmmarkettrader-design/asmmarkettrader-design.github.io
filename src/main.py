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

def get_category_icon(category):
    cat_lower = category.lower()
    if any(word in cat_lower for word in ['perfume', 'fragrance', 'scent', 'attar']): return 'fa-spray-can'
    if any(word in cat_lower for word in ['watch', 'clock', 'smartwatch']): return 'fa-clock'
    if any(word in cat_lower for word in ['apparel', 'cloth', 'fashion', 'shirt', 'dress']): return 'fa-tshirt'
    if any(word in cat_lower for word in ['shoe', 'footwear', 'sneaker']): return 'fa-shoe-prints'
    if any(word in cat_lower for word in ['electronic', 'tech', 'mobile', 'gadget']): return 'fa-mobile-screen-button'
    if any(word in cat_lower for word in ['beauty', 'cosmetic', 'makeup', 'care']): return 'fa-spa'
    if any(word in cat_lower for word in ['home', 'decor', 'kitchen']): return 'fa-house'
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
                <div class="w-8 h-8 rounded-full bg-teal-100 text-teal-800 flex items-center justify-center font-bold" aria-hidden="true">{reviewer[0]}</div>
                <span class="font-bold text-gray-900">{reviewer}</span>
                <span class="text-[10px] text-green-700 bg-green-50 px-2 py-0.5 rounded-full"><i class="fas fa-check-circle" aria-hidden="true"></i> Verified Buyer</span>
            </div>
            <div class="text-yellow-500 text-xs mb-2" aria-label="{stars} out of 5 stars">
                {"<i class='fas fa-star' aria-hidden='true'></i>" * stars}
            </div>
            <p class="text-gray-700 text-sm">{comment}</p>
        </div>
        """
    return reviews_html

def get_html_header(title, categories_list=[], seo_desc="ASM VEO - Premium Shopping in Pakistan"):
    # Generate Dropdown Links
    cat_links = ""
    for cat in categories_list:
        c_slug = re.sub(r'[^a-z0-9]+', '-', cat.lower())
        cat_links += f'<a href="/category/{c_slug}.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-700">{cat}</a>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - ASM VEO</title>
    
    <!-- Auto SEO Meta Tags -->
    <meta name="description" content="{seo_desc}">
    <meta name="keywords" content="{title}, buy online, Pakistan, shopping, ASM Digital Solutions, ASM VEO, cash on delivery">
    <meta name="author" content="ASM Digital Solutions">
    <meta name="robots" content="index, follow">
    
    <!-- Performance Boosters -->
    <link rel="preconnect" href="https://cdn.tailwindcss.com">
    <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet" media="print" onload="this.media='all'">
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; }}
        .product-card {{ transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }}
        .product-card:hover {{ transform: translateY(-8px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }}
        .image-zoom img {{ transition: transform 0.5s ease; }}
        .product-card:hover .image-zoom img {{ transform: scale(1.1); }}
        .dropdown:hover .dropdown-menu {{ display: block; }}
    </style>

    <!-- Global Cart Scripts -->
    <script>
        function updateCartBadge() {{
            let cart = JSON.parse(localStorage.getItem('asm_cart')) || [];
            document.getElementById('cart-badge').innerText = cart.length;
        }}

        function addToCart(name, price, image, event) {{
            if(event) event.stopPropagation();
            let cart = JSON.parse(localStorage.getItem('asm_cart')) || [];
            cart.push({{name: name, price: price, image: image}});
            localStorage.setItem('asm_cart', JSON.stringify(cart));
            updateCartBadge();
            
            // Show toast notification
            const toast = document.createElement('div');
            toast.className = 'fixed bottom-4 right-4 bg-teal-600 text-white px-6 py-3 rounded-xl shadow-2xl z-50 transform transition-all duration-300 translate-y-0 opacity-100 flex items-center gap-3 font-bold';
            toast.innerHTML = `<i class="fas fa-check-circle text-xl"></i> Added to Cart!`;
            document.body.appendChild(toast);
            setTimeout(() => {{ toast.style.opacity = '0'; setTimeout(() => toast.remove(), 300); }}, 2000);
        }}

        function buyNow(name, price, event) {{
            if(event) event.stopPropagation();
            window.location.href = '/checkout.html?buy_now=true&product=' + encodeURIComponent(name) + '&price=' + price;
        }}

        function handleSearch(e) {{
            if (e.key === 'Enter') executeSearch();
        }}
        function executeSearch() {{
            let val = document.getElementById('searchInput').value;
            if(val.trim() !== "") window.location.href = '/index.html?search=' + encodeURIComponent(val);
        }}

        window.onload = updateCartBadge;
    </script>
</head>
<body class="text-gray-900">
    <!-- Navbar -->
    <header class="bg-white shadow-md sticky top-0 z-50">
        <!-- Top Bar for Pages & Navigation -->
        <div class="bg-gray-900 text-white text-xs md:text-sm py-2">
            <div class="container mx-auto px-4 flex justify-between items-center">
                <div class="flex space-x-4">
                    <a href="/index.html" class="hover:text-teal-400 transition font-semibold"><i class="fas fa-home mr-1"></i> Home</a>
                    <div class="relative dropdown z-50 hidden md:block">
                        <button class="hover:text-teal-400 transition font-semibold focus:outline-none"><i class="fas fa-list mr-1"></i> Categories <i class="fas fa-chevron-down text-[10px] ml-1"></i></button>
                        <div class="dropdown-menu absolute hidden text-gray-700 bg-white shadow-xl rounded-xl mt-1 w-48 py-2 border border-gray-100">
                            {cat_links}
                        </div>
                    </div>
                    <a href="/about.html" class="hover:text-teal-400 transition font-semibold"><i class="fas fa-info-circle mr-1"></i> About Us</a>
                    <a href="/contact.html" class="hover:text-teal-400 transition font-semibold"><i class="fas fa-envelope mr-1"></i> Contact</a>
                </div>
                <div class="hidden md:block text-teal-400 font-bold"><i class="fas fa-truck-fast"></i> Nationwide Cash on Delivery</div>
            </div>
        </div>

        <!-- Main Search Bar Area -->
        <div class="container mx-auto px-4 py-4 flex flex-wrap justify-between items-center gap-4">
            <a href="/index.html" class="text-2xl md:text-3xl font-extrabold text-teal-800 tracking-tight flex items-center gap-2" aria-label="ASM VEO Home">
                <div class="bg-teal-700 text-white p-2 rounded-lg shadow-md" aria-hidden="true"><i class="fas fa-shopping-bag"></i></div>
                ASM VEO
            </a>
            
            <div class="flex-1 min-w-[200px] max-w-xl mx-0 md:mx-8 relative">
                <label for="searchInput" class="sr-only">Search</label>
                <input type="text" id="searchInput" onkeypress="handleSearch(event)" placeholder="Search any product..." class="w-full bg-gray-50 border-2 border-gray-200 focus:bg-white focus:border-teal-600 rounded-xl py-3 px-6 outline-none transition-all text-gray-800 font-semibold shadow-sm">
                <button onclick="executeSearch()" aria-label="Submit" class="absolute right-4 top-3 text-gray-500 hover:text-teal-700"><i class="fas fa-search text-xl" aria-hidden="true"></i></button>
            </div>
            
            <a href="/checkout.html" class="relative bg-teal-50 text-teal-800 px-5 py-3 rounded-xl font-bold hover:bg-teal-700 hover:text-white transition-colors border border-teal-200 shadow-sm flex items-center gap-2" aria-label="Go to Cart">
                <i class="fas fa-shopping-cart text-xl" aria-hidden="true"></i>
                <span class="hidden md:inline">Cart</span>
                <span id="cart-badge" class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-black px-2 py-0.5 rounded-full shadow">0</span>
            </a>
        </div>
    </header>
    <main id="main-content">
"""

def get_html_footer():
    return """
    </main>
    <!-- Footer -->
    <footer class="bg-gray-900 text-white mt-16 pt-16 pb-8 border-t-4 border-teal-600">
        <div class="container mx-auto px-4 grid grid-cols-1 md:grid-cols-4 gap-10 mb-10">
            <div class="col-span-1 md:col-span-2">
                <h3 class="text-3xl font-extrabold mb-4 flex items-center gap-2 text-white"><i class="fas fa-shopping-bag text-teal-400" aria-hidden="true"></i> ASM VEO</h3>
                <p class="text-gray-400 text-sm leading-relaxed mb-6 pr-4">ASM VEO is a top-tier professional shopping platform bringing you the best products across multiple categories. Enjoy premium quality, nationwide Cash on Delivery, and a 100% secure shopping experience.</p>
                <div class="flex gap-4">
                    <a href="#" aria-label="Facebook" class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-teal-600 transition text-white"><i class="fab fa-facebook-f" aria-hidden="true"></i></a>
                    <a href="#" aria-label="Instagram" class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-teal-600 transition text-white"><i class="fab fa-instagram" aria-hidden="true"></i></a>
                </div>
            </div>
            <div>
                <h3 class="text-xl font-bold mb-5 text-white border-b border-gray-700 pb-2">Quick Links</h3>
                <ul class="space-y-3 text-gray-400 text-sm font-semibold">
                    <li><a href="/index.html" class="hover:text-teal-400 transition"><i class="fas fa-angle-right mr-2 text-teal-600"></i> Home</a></li>
                    <li><a href="/about.html" class="hover:text-teal-400 transition"><i class="fas fa-angle-right mr-2 text-teal-600"></i> About Us</a></li>
                    <li><a href="/contact.html" class="hover:text-teal-400 transition"><i class="fas fa-angle-right mr-2 text-teal-600"></i> Contact Us</a></li>
                    <li><a href="/checkout.html" class="hover:text-teal-400 transition"><i class="fas fa-angle-right mr-2 text-teal-600"></i> Cart / Checkout</a></li>
                </ul>
            </div>
            <div>
                <h3 class="text-xl font-bold mb-5 text-white border-b border-gray-700 pb-2">Contact Info</h3>
                <ul class="space-y-4 text-gray-400 text-sm">
                    <li class="flex items-center gap-3"><div class="bg-gray-800 p-2 rounded text-teal-400"><i class="fas fa-user-tie"></i></div> CEO: Ali Abbas</li>
                    <li class="flex items-center gap-3"><div class="bg-gray-800 p-2 rounded text-teal-400"><i class="fas fa-building"></i></div> ASM Digital Solutions</li>
                    <li class="flex items-center gap-3"><div class="bg-green-500 p-2 rounded text-white"><i class="fab fa-whatsapp text-lg"></i></div> <a href="https://wa.me/923425478683" class="hover:text-white transition font-bold text-base">0342 54 786 83</a></li>
                </ul>
            </div>
        </div>
        <div class="border-t border-gray-800 text-center pt-8">
            <p class="text-gray-500 text-sm font-semibold">&copy; 2026 ASM Digital Solutions. All Rights Reserved.</p>
        </div>
    </footer>
</body>
</html>
"""

def generate_sitemap(urls):
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    date_str = datetime.now().strftime("%Y-%m-%d")
    for url in urls:
        xml_content += f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{date_str}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"
    xml_content += '</urlset>'
    with open("output/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)

def process_woocommerce_csv():
    file_path = "woocommerce-products-export.csv"
    if not os.path.exists(file_path):
        print("❌ CSV File Not Found!")
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
    sitemap_urls = ["https://www.asmveo.com/", "https://www.asmveo.com/checkout.html", "https://www.asmveo.com/about.html", "https://www.asmveo.com/contact.html"]
    
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            images_raw = row.get('Images', '').strip()
            if not name or not images_raw: continue 
                
            image = images_raw.split(',')[0].strip()
            base_price = get_price(row.get('Sale price', '') or row.get('Regular price', ''))
            if base_price == 0: continue
            
            final_price = math.ceil(base_price * 1.30)
            fake_regular_price = math.ceil(final_price * 1.61) 
            
            cat_raw = row.get('Categories', 'Uncategorized')
            category = cat_raw.split(',')[0].strip() if cat_raw else 'Exclusive Collection'
            categories_set.add(category)
            
            desc_raw = row.get('Short description', '') or row.get('Description', '')
            clean_description = clean_html(desc_raw)
            seo_desc = local_seo_desc(name, clean_description)
            
            product_id = row.get('ID', str(len(products_list)+1))
            slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-') + f"-{product_id}"
            sitemap_urls.append(f"https://www.asmveo.com/product/{slug}.html")
            
            products_list.append({
                'id': product_id, 'slug': slug, 'name': name, 'category': category,
                'fake_price': fake_regular_price, 'final_price': final_price,
                'image': image, 'seo_desc': seo_desc, 'full_desc': clean_description
            })

    categories_list = sorted(list(categories_set))
    print(f"✔ کل {len(products_list)} پروڈکٹس پراسیس ہو رہی ہیں (جن کی تصاویر موجود ہیں)...")
    
    # ================= STATIC PAGES (About & Contact) =================
    with open("output/about.html", "w", encoding="utf-8") as f:
        f.write(get_html_header("About Us", categories_list) + """
        <div class="container mx-auto px-4 py-16 text-center max-w-3xl">
            <h1 class="text-4xl font-extrabold text-gray-900 mb-6">About ASM VEO</h1>
            <p class="text-lg text-gray-600 leading-relaxed mb-6">ASM VEO, a subsidiary of <strong>ASM Digital Solutions</strong> managed by CEO <strong>Ali Abbas</strong>, is Pakistan's premium online shopping platform. We aim to provide top-notch products across various categories with a 100% secure Cash on Delivery network.</p>
            <p class="text-lg text-gray-600 leading-relaxed">Shop with confidence, knowing every product is vetted for quality.</p>
        </div>
        """ + get_html_footer())

    with open("output/contact.html", "w", encoding="utf-8") as f:
        f.write(get_html_header("Contact Us", categories_list) + """
        <div class="container mx-auto px-4 py-16 text-center max-w-2xl">
            <h1 class="text-4xl font-extrabold text-gray-900 mb-6">Contact Us</h1>
            <div class="bg-white rounded-3xl shadow-xl p-8 border border-gray-100">
                <i class="fab fa-whatsapp text-6xl text-green-500 mb-4"></i>
                <h2 class="text-2xl font-bold mb-2">We're Here to Help!</h2>
                <p class="text-gray-600 mb-6">Have a question about your order or our products? Message us directly on WhatsApp for prompt support.</p>
                <a href="https://wa.me/923425478683" class="inline-block bg-green-500 text-white font-black py-4 px-8 rounded-xl hover:bg-green-600 transition shadow-lg"><i class="fab fa-whatsapp mr-2"></i> Message on WhatsApp (0342 54 786 83)</a>
            </div>
        </div>
        """ + get_html_footer())

    # ================= 1. GENERATE PRODUCT PAGES =================
    for prod in products_list:
        prod_html = get_html_header(prod['name'], categories_list, prod['seo_desc'])
        reviews_section = generate_reviews(prod['name'])
        
        prod_html += f"""
        <div class="container mx-auto px-4 py-10">
            <nav class="text-sm text-gray-600 mb-6 font-semibold bg-gray-100 p-3 rounded-lg inline-block" aria-label="Breadcrumb">
                <a href="/index.html" class="hover:text-teal-700 transition">Home</a> &gt; 
                <a href="/category/{re.sub(r'[^a-z0-9]+', '-', prod['category'].lower())}.html" class="hover:text-teal-700 transition">{prod['category']}</a> &gt; 
                <span class="text-teal-800" aria-current="page">{prod['name']}</span>
            </nav>
            
            <div class="bg-white rounded-3xl shadow-xl border border-gray-200 overflow-hidden flex flex-col md:flex-row mb-12">
                <div class="md:w-1/2 p-6 flex justify-center items-center bg-gray-50 border-r border-gray-200 relative">
                    <div class="absolute top-4 left-4 bg-red-600 text-white text-xs font-black px-3 py-1.5 rounded-lg z-10 shadow-md">SALE</div>
                    <img src="{prod['image']}" alt="Image of {prod['name']}" fetchpriority="high" class="max-h-[500px] object-contain rounded-xl hover:scale-105 transition duration-500">
                </div>
                <div class="md:w-1/2 p-8 md:p-12 flex flex-col justify-center">
                    <span class="text-xs font-bold uppercase tracking-widest text-teal-700 mb-2">{prod['category']}</span>
                    <h1 class="text-3xl md:text-4xl font-extrabold text-gray-900 mb-4">{prod['name']}</h1>
                    
                    <div class="flex items-center gap-3 mb-6" aria-label="Customer Rating">
                        <div class="text-yellow-500 text-sm"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star-half-alt"></i></div>
                        <span class="text-sm font-semibold text-gray-600">(Verified Reviews)</span>
                    </div>

                    <div class="flex items-center gap-4 mb-6 bg-teal-50 p-4 rounded-2xl w-fit border border-teal-100">
                        <span class="text-4xl font-black text-teal-800">Rs {prod['final_price']}</span>
                        <span class="text-xl text-gray-500 font-bold line-through">Rs {prod['fake_price']}</span>
                    </div>
                    
                    <p class="text-gray-700 mb-8 leading-relaxed border-t border-gray-100 pt-6">{prod['full_desc'][:400] if len(prod['full_desc']) > 50 else prod['seo_desc']}</p>
                    
                    <div class="flex flex-col sm:flex-row gap-4 w-full md:w-5/6 mt-auto">
                        <button onclick="addToCart('{prod['name'].replace("'", "\\'")}', {prod['final_price']}, '{prod['image']}', event)" aria-label="Add to Cart" class="sm:w-1/2 bg-white text-teal-700 py-4 rounded-xl font-black text-lg border-2 border-teal-600 hover:bg-teal-50 transition-all shadow-md transform hover:-translate-y-1 flex justify-center items-center gap-2">
                            <i class="fas fa-cart-plus"></i> Add to Cart
                        </button>
                        <button onclick="buyNow('{prod['name'].replace("'", "\\'")}', {prod['final_price']}, event)" aria-label="Buy Now" class="sm:w-1/2 bg-gray-900 text-white py-4 rounded-xl font-black text-lg hover:bg-teal-700 transition-all shadow-lg transform hover:-translate-y-1 flex justify-center items-center gap-2">
                            <i class="fas fa-bolt"></i> Buy Now
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="bg-white rounded-3xl shadow-lg border border-gray-200 p-8">
                <h2 class="text-2xl font-extrabold text-gray-900 mb-6 border-b pb-4">Customer Reviews</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div>{reviews_section}</div>
                    <div class="bg-gray-50 p-6 rounded-2xl h-fit border border-gray-300">
                        <h3 class="font-bold text-lg mb-2 text-gray-900">Write a Review</h3>
                        <p class="text-sm text-gray-600 mb-4">Only verified buyers can leave a review after receiving the product to maintain quality standards.</p>
                        <div class="flex items-center gap-2 text-teal-800 font-bold bg-teal-50 p-3 rounded-lg border border-teal-200">
                            <i class="fas fa-lock"></i> Review form is currently locked.
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """ + get_html_footer()
        
        with open(f"output/product/{prod['slug']}.html", "w", encoding="utf-8") as f:
            f.write(prod_html)

    # ================= 2. GENERATE HOME & CATEGORY PAGES =================
    sections_dict = {}
    for p in products_list:
        c = p['category']
        if c not in sections_dict: sections_dict[c] = []
        sections_dict[c].append(p)

    home_html = get_html_header("Home", categories_list)
    
    # Home Page: Category Icons Section (Top)
    home_html += """
    <div class="container mx-auto px-4 py-10 border-b border-gray-200 mb-6">
        <h2 class="text-2xl font-extrabold text-gray-900 mb-6 text-center">Shop by Category</h2>
        <div class="flex flex-wrap justify-center gap-4 md:gap-8">
    """
    for cat in categories_list:
        c_slug = re.sub(r'[^a-z0-9]+', '-', cat.lower())
        c_icon = get_category_icon(cat)
        home_html += f"""
            <a href="/category/{c_slug}.html" class="flex flex-col items-center justify-center bg-white border border-gray-100 shadow-sm hover:shadow-md rounded-2xl p-4 w-28 h-28 md:w-32 md:h-32 transition-all transform hover:-translate-y-2 group">
                <div class="w-12 h-12 rounded-full bg-teal-50 flex items-center justify-center mb-3 group-hover:bg-teal-600 transition-colors">
                    <i class="fas {c_icon} text-2xl text-teal-600 group-hover:text-white"></i>
                </div>
                <span class="text-xs font-bold text-gray-800 text-center line-clamp-2">{cat}</span>
            </a>
        """
    home_html += "</div></div>"
    
    home_html += """
    <div class='container mx-auto px-4 py-4'>
        <h2 id="searchResultsHeading" class="text-2xl font-extrabold text-teal-800 mb-6 hidden border-b pb-2"></h2>
    """
    
    total_rendered_products = 0
    for cat_name, prods in sections_dict.items():
        cat_slug = re.sub(r'[^a-z0-9]+', '-', cat_name.lower())
        sitemap_urls.append(f"https://www.asmveo.com/category/{cat_slug}.html")
        
        cat_html = get_html_header(cat_name, categories_list)
        cat_html += f"""
        <div class="bg-teal-50 py-12 mb-8 border-b border-teal-100">
            <div class="container mx-auto px-4 text-center">
                <div class="w-16 h-16 mx-auto rounded-full bg-teal-600 flex items-center justify-center mb-4 text-white shadow-lg">
                    <i class="fas {get_category_icon(cat_name)} text-3xl"></i>
                </div>
                <h1 class="text-3xl md:text-5xl font-black text-gray-900">{cat_name}</h1>
                <p class="text-teal-700 mt-3 font-bold">{len(prods)} Exclusive Products Available</p>
            </div>
        </div>
        <div class="container mx-auto px-4 pb-12"><div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
        """
        
        home_html += f"""
        <div class="mb-14 category-section">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl md:text-3xl font-black text-gray-900 border-l-4 border-teal-600 pl-4">{cat_name}</h2>
                <a href="/category/{cat_slug}.html" class="text-teal-700 font-bold text-sm bg-teal-50 px-5 py-2.5 rounded-full hover:bg-teal-700 hover:text-white transition-all shadow-sm">View All <i class="fas fa-arrow-right ml-1"></i></a>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
        """
        
        for idx, prod in enumerate(prods):
            img_loading = 'loading="lazy"' if total_rendered_products >= 4 else 'fetchpriority="high"'
            
            card_ui = f"""
                <div class="product-card bg-white rounded-2xl shadow-sm hover:shadow-xl border border-gray-200 overflow-hidden flex flex-col relative cursor-pointer" onclick="window.location.href='/product/{prod['slug']}.html'">
                    <div class="image-zoom h-48 md:h-60 bg-gray-50 overflow-hidden relative border-b border-gray-200 flex justify-center items-center">
                        <img src="{prod['image']}" alt="{prod['name']}" {img_loading} class="w-full h-full object-cover">
                    </div>
                    <div class="p-4 flex flex-col flex-grow">
                        <span class="text-[10px] font-bold text-teal-700 uppercase tracking-wider mb-1 line-clamp-1">{prod['category']}</span>
                        <h3 class="prod-title text-sm md:text-base font-bold text-gray-900 leading-tight mb-2 line-clamp-2">{prod['name']}</h3>
                        <div class="mt-auto">
                            <div class="flex items-center gap-2 mb-3">
                                <span class="text-lg font-black text-teal-800">Rs {prod['final_price']}</span>
                                <span class="text-xs text-gray-400 font-bold line-through">Rs {prod['fake_price']}</span>
                            </div>
                            <!-- Two Buttons for Add to Cart and Buy Now -->
                            <div class="flex gap-2 w-full">
                                <button onclick="addToCart('{prod['name'].replace("'", "\\'")}', {prod['final_price']}, '{prod['image']}', event)" class="w-1/2 bg-teal-50 text-teal-800 py-2.5 rounded-xl text-xs font-bold border border-teal-200 hover:bg-teal-100 transition flex justify-center items-center" aria-label="Add to Cart">
                                    <i class="fas fa-cart-plus"></i>
                                </button>
                                <button onclick="buyNow('{prod['name'].replace("'", "\\'")}', {prod['final_price']}, event)" class="w-1/2 bg-gray-900 text-white py-2.5 rounded-xl text-xs font-bold hover:bg-teal-700 transition text-center" aria-label="Buy Now">
                                    Buy Now
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            """
            cat_html += card_ui
            if idx < 10: 
                home_html += card_ui
                total_rendered_products += 1
            
        cat_html += "</div></div>" + get_html_footer()
        with open(f"output/category/{cat_slug}.html", "w", encoding="utf-8") as f:
            f.write(cat_html)
            
        home_html += "</div></div>"
    
    home_html += "</div>" + get_html_footer()
    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(home_html)

    # ================= 3. GENERATE CHECKOUT PAGE (Dynamic Cart + Direct Buy) =================
    pak_cities = ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Multan", "Peshawar", "Quetta", "Gujranwala", "Sialkot", "Hyderabad", "Bahawalpur", "Sargodha", "Other"]
    city_options = "".join([f"<option value='{city}'>{city}</option>" for city in pak_cities])
    
    checkout_html = get_html_header("Secure Checkout", categories_list)
    checkout_html += f"""
    <div class="container mx-auto px-4 py-12 max-w-6xl">
        <div class="flex flex-col lg:flex-row gap-8">
            
            <!-- Cart Items Section -->
            <div class="lg:w-1/2">
                <div class="bg-white rounded-3xl shadow-xl p-6 border border-gray-200 mb-6">
                    <h2 class="text-2xl font-black text-gray-900 mb-4 border-b pb-4"><i class="fas fa-shopping-bag text-teal-600 mr-2"></i> Your Items</h2>
                    <div id="cartItemsContainer" class="space-y-4 max-h-[400px] overflow-y-auto pr-2">
                        <!-- JS will populate this -->
                    </div>
                </div>
            </div>

            <!-- Checkout Form Section -->
            <div class="lg:w-1/2">
                <div class="bg-gray-900 p-6 rounded-t-3xl text-white relative">
                    <div class="absolute top-0 left-0 w-full h-1 bg-teal-500 rounded-t-3xl"></div>
                    <h1 class="text-2xl font-extrabold"><i class="fas fa-map-marker-alt text-teal-400 mr-2"></i> Shipping Details</h1>
                </div>
                
                <form id="checkoutForm" class="bg-white p-6 md:p-8 rounded-b-3xl shadow-xl border border-gray-200 border-t-0 space-y-5">
                    <input type="hidden" name="_subject" value="New Order Received on ASM VEO!">
                    <input type="hidden" name="Product_Ordered" id="productField" value="">
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <div>
                            <label class="block text-sm font-bold text-gray-800 mb-2">Full Name <span class="text-red-600">*</span></label>
                            <input type="text" name="Full_Name" class="w-full border-2 border-gray-300 p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-600 outline-none text-gray-900" required placeholder="Ali Abbas">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-gray-800 mb-2">Email Address</label>
                            <input type="email" name="Email" class="w-full border-2 border-gray-300 p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-600 outline-none text-gray-900" placeholder="you@example.com">
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <div>
                            <label class="block text-sm font-bold text-gray-800 mb-2">Mobile Number <span class="text-red-600">*</span></label>
                            <input type="tel" name="Phone_Number" class="w-full border-2 border-gray-300 p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-600 outline-none text-gray-900" required placeholder="0300-XXXXXXX">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-gray-800 mb-2">City <span class="text-red-600">*</span></label>
                            <select name="City" class="w-full border-2 border-gray-300 p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-600 outline-none font-semibold text-gray-900" required>
                                <option value="" disabled selected>Select City</option>
                                {city_options}
                            </select>
                        </div>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-bold text-gray-800 mb-2">Complete Delivery Address <span class="text-red-600">*</span></label>
                        <textarea name="Address" rows="2" class="w-full border-2 border-gray-300 p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-600 outline-none text-gray-900" required placeholder="House No, Street, Area..."></textarea>
                    </div>
                    
                    <div class="bg-teal-50 rounded-2xl p-5 border border-teal-100 mt-6">
                        <div class="flex justify-between text-sm font-bold text-gray-700 mb-2">
                            <span>Subtotal</span>
                            <span id="subtotalDisplay">Rs 0</span>
                        </div>
                        <div class="flex justify-between text-sm font-bold text-teal-800 mb-4 border-b border-teal-200 pb-4">
                            <span>Delivery Charges</span>
                            <span>Rs 250</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="font-black text-lg text-gray-900">Total (COD)</span>
                            <span class="font-black text-2xl text-teal-800" id="grandTotalDisplay">Rs 250</span>
                        </div>
                    </div>

                    <button type="submit" id="submitBtn" class="w-full bg-gray-900 text-white font-black py-4 rounded-xl hover:bg-teal-700 transition-all shadow-xl text-lg transform hover:-translate-y-1">
                        <i class="fas fa-check-circle mr-2"></i> Confirm Order
                    </button>
                    
                    <a href="https://wa.me/923425478683?text=Hi,%20I%20want%20to%20order!" class="w-full bg-green-500 text-white font-black py-4 rounded-xl hover:bg-green-600 transition-all shadow-xl text-lg mt-3 flex items-center justify-center gap-2 transform hover:-translate-y-1">
                        <i class="fab fa-whatsapp text-xl"></i> Order via WhatsApp
                    </a>
                </form>
            </div>
        </div>
    </div>
    
    <script>
        const urlParams = new URLSearchParams(window.location.search);
        const isBuyNow = urlParams.get('buy_now') === 'true';
        const pName = urlParams.get('product');
        const pPrice = parseInt(urlParams.get('price'));
        
        let subtotal = 0;
        let finalOrderString = "";
        let container = document.getElementById('cartItemsContainer');
        
        if (isBuyNow && pName && pPrice) {{
            // Direct Buy (Buy Now button)
            subtotal = pPrice;
            finalOrderString = "1x " + pName + " (Rs " + pPrice + ")";
            container.innerHTML = `
                <div class="flex items-center gap-4 bg-gray-50 p-3 rounded-xl border border-gray-200">
                    <div class="flex-1">
                        <h3 class="font-bold text-gray-900 line-clamp-1">${{pName}}</h3>
                        <p class="text-teal-700 font-black">Rs ${{pPrice}}</p>
                    </div>
                </div>`;
        }} else {{
            // Load Cart from Local Storage
            let cart = JSON.parse(localStorage.getItem('asm_cart')) || [];
            if(cart.length === 0) {{
                container.innerHTML = `<p class="text-gray-500 font-semibold text-center py-6">Your cart is empty.</p>`;
                document.getElementById('submitBtn').disabled = true;
                document.getElementById('submitBtn').classList.add('opacity-50', 'cursor-not-allowed');
            }} else {{
                cart.forEach((item, index) => {{
                    subtotal += parseInt(item.price);
                    finalOrderString += (index+1) + ". " + item.name + " (Rs " + item.price + ")\\n";
                    
                    container.innerHTML += `
                    <div class="flex items-center gap-4 bg-gray-50 p-3 rounded-xl border border-gray-200">
                        <img src="${{item.image}}" class="w-16 h-16 object-cover rounded-lg bg-white border border-gray-100">
                        <div class="flex-1">
                            <h3 class="font-bold text-sm text-gray-900 line-clamp-2">${{item.name}}</h3>
                            <p class="text-teal-700 font-black text-sm mt-1">Rs ${{item.price}}</p>
                        </div>
                    </div>`;
                }});
            }}
        }}

        // Update Totals
        if(subtotal > 0) {{
            document.getElementById('subtotalDisplay').innerText = "Rs " + subtotal;
            document.getElementById('grandTotalDisplay').innerText = "Rs " + (subtotal + 250);
            document.getElementById('productField').value = finalOrderString + "\\n\\nGrand Total: Rs " + (subtotal + 250);
        }}

        // Form Submission
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
                    if(!isBuyNow) localStorage.removeItem('asm_cart'); // Clear cart if it was a cart checkout
                    alert('Order Confirmed! Total to pay on delivery: ' + document.getElementById('grandTotalDisplay').innerText);
                    window.location.href = '/index.html';
                }} else {{
                    alert('Error submitting order. Try again.');
                    btn.innerHTML = '<i class="fas fa-check-circle mr-2"></i> Confirm Order';
                    btn.disabled = false;
                }}
            }}).catch(error => {{
                alert('Network Error!');
                btn.innerHTML = '<i class="fas fa-check-circle mr-2"></i> Confirm Order';
                btn.disabled = false;
            }});
        }});
    </script>
    """
    checkout_html += get_html_footer()
    with open("output/checkout.html", "w", encoding="utf-8") as f:
        f.write(checkout_html)
        
    generate_sitemap(sitemap_urls)
    print("🎉 مکمل پروفیشنل ویب سائٹ، نیویگیشن، کیٹیگریز اور ایڈ ٹو کارٹ کے ساتھ تیار ہے!")

if __name__ == "__main__":
    process_woocommerce_csv()
