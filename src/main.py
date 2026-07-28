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

def get_html_header(title, seo_desc="ASM VEO - Premium Shopping in Pakistan"):
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
    
    <!-- Performance Boosters (Preconnect & Prefetch) -->
    <link rel="preconnect" href="https://cdn.tailwindcss.com">
    <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="dns-prefetch" href="https://cdn.tailwindcss.com">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet" media="print" onload="this.media='all'">
    <noscript><link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet"></noscript>
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; }}
        .product-card {{ transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }}
        .product-card:hover {{ transform: translateY(-8px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }}
        .image-zoom img {{ transition: transform 0.5s ease; }}
        .product-card:hover .image-zoom img {{ transform: scale(1.1); }}
    </style>
</head>
<body class="text-gray-900">
    <!-- Navbar -->
    <header class="bg-white shadow-md sticky top-0 z-50">
        <div class="container mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-4">
            <a href="/index.html" class="text-2xl md:text-3xl font-extrabold text-teal-800 tracking-tight flex items-center gap-2" aria-label="ASM VEO Home">
                <div class="bg-teal-700 text-white p-2 rounded-lg" aria-hidden="true"><i class="fas fa-shopping-bag"></i></div>
                ASM VEO
            </a>
            
            <div class="flex-1 min-w-[250px] max-w-xl mx-0 md:mx-8 relative">
                <label for="searchInput" class="sr-only">Search any product</label>
                <input type="text" id="searchInput" onkeypress="handleSearch(event)" placeholder="Search any product..." class="w-full bg-gray-100 border border-gray-300 focus:border-teal-600 rounded-full py-2.5 px-6 outline-none transition-all text-gray-800">
                <button onclick="executeSearch()" aria-label="Submit Search" class="absolute right-4 top-2.5 text-gray-600 hover:text-teal-700"><i class="fas fa-search text-lg" aria-hidden="true"></i></button>
            </div>
            
            <a href="/checkout.html" class="bg-gray-900 text-white px-5 py-2.5 rounded-full font-bold hover:bg-teal-700 transition-colors shadow-lg flex items-center gap-2 whitespace-nowrap" aria-label="Go to Checkout">
                <i class="fas fa-shopping-cart" aria-hidden="true"></i> <span class="hidden md:inline">Cart / Checkout</span>
            </a>
        </div>
    </header>
    
    <!-- Main Content Wrapper (Landmark) -->
    <main id="main-content">
    
    <script>
    function handleSearch(e) {{
        if (e.key === 'Enter') {{
            executeSearch();
        }}
    }}
    function executeSearch() {{
        let val = document.getElementById('searchInput').value;
        if(val.trim() !== "") {{
            window.location.href = '/index.html?search=' + encodeURIComponent(val);
        }}
    }}
    </script>
"""

def get_html_footer():
    return """
    </main> <!-- End of Main Landmark -->
    <!-- Footer -->
    <footer class="bg-gray-900 text-white mt-16 pt-12 pb-6 border-t-4 border-teal-600">
        <div class="container mx-auto px-4 grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div class="col-span-1 md:col-span-2">
                <h3 class="text-2xl font-bold mb-4 flex items-center gap-2"><i class="fas fa-shopping-bag text-teal-400" aria-hidden="true"></i> ASM VEO</h3>
                <p class="text-gray-300 text-sm leading-relaxed mb-4">ASM VEO is a professional shopping platform bringing you the best products across multiple categories. Enjoy premium quality, nationwide Cash on Delivery, and a 100% secure shopping experience.</p>
                <div class="flex gap-4">
                    <a href="#" aria-label="Visit our Facebook page" class="w-12 h-12 rounded-full bg-gray-800 flex items-center justify-center hover:bg-teal-600 transition text-white"><i class="fab fa-facebook-f" aria-hidden="true"></i></a>
                    <a href="#" aria-label="Visit our Instagram page" class="w-12 h-12 rounded-full bg-gray-800 flex items-center justify-center hover:bg-teal-600 transition text-white"><i class="fab fa-instagram" aria-hidden="true"></i></a>
                </div>
            </div>
            <div>
                <h3 class="text-lg font-bold mb-4 text-white">Management & Contact</h3>
                <ul class="space-y-3 text-gray-300 text-sm">
                    <li class="flex items-center gap-2"><i class="fas fa-user-tie text-teal-400" aria-hidden="true"></i> CEO: Ali Abbas</li>
                    <li class="flex items-center gap-2"><i class="fas fa-building text-teal-400" aria-hidden="true"></i> ASM Digital Solutions</li>
                    <li class="flex items-center gap-2"><i class="fab fa-whatsapp text-green-400 text-lg" aria-hidden="true"></i> <a href="https://wa.me/923425478683" aria-label="Contact us on WhatsApp at 0342 54 786 83" class="hover:text-white transition focus:outline-none focus:ring-2 focus:ring-teal-400">0342 54 786 83</a></li>
                </ul>
            </div>
            <div>
                <h3 class="text-lg font-bold mb-4 text-white">Safe & Secure</h3>
                <p class="text-gray-300 text-sm mb-2"><i class="fas fa-money-bill-wave text-green-400 mr-2" aria-hidden="true"></i> Cash on Delivery Available</p>
                <p class="text-gray-300 text-sm mb-2"><i class="fas fa-undo text-teal-400 mr-2" aria-hidden="true"></i> Easy Return Policy</p>
                <p class="text-gray-300 text-sm"><i class="fas fa-shield-alt text-teal-400 mr-2" aria-hidden="true"></i> 100% Secure Checkout</p>
            </div>
        </div>
        <div class="border-t border-gray-800 text-center pt-6">
            <p class="text-gray-400 text-sm">&copy; 2026 ASM Digital Solutions. All Rights Reserved.</p>
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
    sitemap_urls = ["https://www.asmveo.com/", "https://www.asmveo.com/checkout.html"]
    
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            if not name: continue
            
            images_raw = row.get('Images', '').strip()
            if not images_raw: 
                continue 
                
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
                'id': product_id,
                'slug': slug,
                'name': name,
                'category': category,
                'fake_price': fake_regular_price,
                'final_price': final_price,
                'image': image,
                'seo_desc': seo_desc,
                'full_desc': clean_description
            })

    print(f"✔ کل {len(products_list)} پروڈکٹس پراسیس ہو رہی ہیں (جن کی تصاویر موجود ہیں)...")
    
    # ================= 1. GENERATE PRODUCT PAGES =================
    for prod in products_list:
        prod_html = get_html_header(prod['name'], prod['seo_desc'])
        reviews_section = generate_reviews(prod['name'])
        
        prod_html += f"""
        <div class="container mx-auto px-4 py-10">
            <nav class="text-sm text-gray-600 mb-6 font-semibold" aria-label="Breadcrumb">
                <a href="/index.html" class="hover:text-teal-700 transition focus:outline-none focus:ring-2 focus:ring-teal-500 rounded px-1">Home</a> &gt; 
                <a href="/category/{re.sub(r'[^a-z0-9]+', '-', prod['category'].lower())}.html" class="hover:text-teal-700 transition focus:outline-none focus:ring-2 focus:ring-teal-500 rounded px-1">{prod['category']}</a> &gt; 
                <span class="text-gray-900" aria-current="page">{prod['name']}</span>
            </nav>
            
            <div class="bg-white rounded-3xl shadow-xl border border-gray-200 overflow-hidden flex flex-col md:flex-row mb-12">
                <div class="md:w-1/2 p-6 flex justify-center items-center bg-gray-50 border-r border-gray-200 relative">
                    <div class="absolute top-4 left-4 bg-red-600 text-white text-xs font-black px-3 py-1.5 rounded-lg z-10 shadow-md" aria-hidden="true">SALE</div>
                    <!-- fetchpriority="high" and no loading="lazy" for main product image (Lighthouse FCP/LCP Fix) -->
                    <img src="{prod['image']}" alt="Image of {prod['name']}" fetchpriority="high" class="max-h-[500px] object-contain rounded-xl hover:scale-105 transition duration-500">
                </div>
                <div class="md:w-1/2 p-8 md:p-12 flex flex-col justify-center">
                    <span class="text-xs font-bold uppercase tracking-widest text-teal-700 mb-2">{prod['category']}</span>
                    <h1 class="text-3xl md:text-4xl font-extrabold text-gray-900 mb-4">{prod['name']}</h1>
                    
                    <div class="flex items-center gap-3 mb-6" aria-label="Customer Rating">
                        <div class="text-yellow-500 text-sm" aria-hidden="true"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star-half-alt"></i></div>
                        <span class="text-sm font-semibold text-gray-600">(Verified Reviews)</span>
                    </div>

                    <div class="flex items-center gap-4 mb-6 bg-gray-50 p-4 rounded-2xl w-fit border border-gray-300">
                        <span class="text-4xl font-black text-teal-800" aria-label="Sale Price">Rs {prod['final_price']}</span>
                        <span class="text-xl text-gray-500 font-bold line-through" aria-label="Original Price">Rs {prod['fake_price']}</span>
                    </div>
                    
                    <div class="mb-6">
                        <label for="sizeSelect" class="block text-sm font-bold text-gray-800 mb-2">Select Variation / Size (If Applicable)</label>
                        <select id="sizeSelect" class="w-full md:w-2/3 border-2 border-gray-300 rounded-xl p-3 outline-none focus:border-teal-600 bg-white font-semibold text-gray-800">
                            <option>Standard / Free Size</option>
                            <option>Small (S)</option>
                            <option>Medium (M)</option>
                            <option>Large (L)</option>
                        </select>
                    </div>

                    <p class="text-gray-700 mb-8 leading-relaxed">{prod['full_desc'][:400] if len(prod['full_desc']) > 50 else prod['seo_desc']}</p>
                    
                    <a href="/checkout.html?product={prod['name'].replace(' ', '%20')}&price={prod['final_price']}" aria-label="Order {prod['name']} Now" class="bg-gray-900 text-white text-center py-4 rounded-xl font-bold text-lg hover:bg-teal-700 transition-all shadow-lg w-full md:w-2/3 transform hover:-translate-y-1 flex justify-center items-center gap-2 focus:outline-none focus:ring-4 focus:ring-teal-500">
                        <i class="fas fa-cart-plus" aria-hidden="true"></i> Add to Cart / Order Now
                    </a>
                </div>
            </div>
            
            <!-- Reviews Section -->
            <div class="bg-white rounded-3xl shadow-lg border border-gray-200 p-8">
                <h2 class="text-2xl font-extrabold text-gray-900 mb-6 border-b pb-4">Customer Reviews</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div>
                        {reviews_section}
                    </div>
                    <div class="bg-gray-50 p-6 rounded-2xl h-fit border border-gray-300">
                        <h3 class="font-bold text-lg mb-2 text-gray-900">Write a Review</h3>
                        <p class="text-sm text-gray-600 mb-4">Only verified buyers can leave a review after receiving the product to maintain quality standards.</p>
                        <div class="flex items-center gap-2 text-teal-800 font-bold bg-teal-50 p-3 rounded-lg border border-teal-200">
                            <i class="fas fa-lock" aria-hidden="true"></i> Review form is currently locked.
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

    home_html = get_html_header("Home")
    
    home_html += """
    <script>
        window.addEventListener('DOMContentLoaded', (event) => {
            const urlParams = new URLSearchParams(window.location.search);
            const searchQuery = urlParams.get('search');
            
            if (searchQuery) {
                const query = searchQuery.toLowerCase();
                const cards = document.querySelectorAll('.product-card');
                let found = 0;
                
                cards.forEach(card => {
                    const title = card.querySelector('.prod-title').innerText.toLowerCase();
                    if (title.includes(query)) {
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
    <div class='container mx-auto px-4 py-8'>
        <h2 id="searchResultsHeading" class="text-2xl font-extrabold text-teal-800 mb-6 hidden border-b pb-2"></h2>
    """
    
    total_rendered_products = 0
    for cat_name, prods in sections_dict.items():
        cat_slug = re.sub(r'[^a-z0-9]+', '-', cat_name.lower())
        sitemap_urls.append(f"https://www.asmveo.com/category/{cat_slug}.html")
        
        cat_html = get_html_header(cat_name)
        cat_html += f"""
        <div class="bg-gray-100 py-10 mb-8 border-b border-gray-300">
            <div class="container mx-auto px-4 text-center">
                <h1 class="text-3xl md:text-5xl font-black text-gray-900">{cat_name}</h1>
                <p class="text-gray-700 mt-3 font-semibold">{len(prods)} Exclusive Products Available</p>
            </div>
        </div>
        <div class="container mx-auto px-4 pb-12"><div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
        """
        
        home_html += f"""
        <div class="mb-14 category-section">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl md:text-3xl font-black text-gray-900 border-l-4 border-teal-600 pl-4">{cat_name}</h2>
                <a href="/category/{cat_slug}.html" aria-label="View all products in {cat_name}" class="text-teal-700 font-bold text-sm bg-teal-50 px-5 py-2.5 rounded-full hover:bg-teal-700 hover:text-white transition-all shadow-sm focus:outline-none focus:ring-2 focus:ring-teal-500">View All <i class="fas fa-arrow-right ml-1" aria-hidden="true"></i></a>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
        """
        
        for idx, prod in enumerate(prods):
            # Only eager load the first 4 images on the homepage to optimize LCP without blocking other resources
            img_loading = 'loading="lazy"' if total_rendered_products >= 4 else 'fetchpriority="high"'
            
            card_ui = f"""
                <div class="product-card bg-white rounded-2xl shadow-sm hover:shadow-xl border border-gray-200 overflow-hidden flex flex-col relative cursor-pointer" onclick="window.location.href='/product/{prod['slug']}.html'" role="link" aria-label="View details for {prod['name']}" tabindex="0">
                    <div class="image-zoom h-48 md:h-60 bg-gray-50 overflow-hidden relative border-b border-gray-200">
                        <img src="{prod['image']}" alt="Image of {prod['name']}" {img_loading} class="w-full h-full object-cover">
                    </div>
                    <div class="p-4 flex flex-col flex-grow">
                        <span class="text-[10px] font-bold text-teal-700 uppercase tracking-wider mb-1">{prod['category']}</span>
                        <h3 class="prod-title text-sm md:text-base font-bold text-gray-900 leading-tight mb-2 line-clamp-2">{prod['name']}</h3>
                        <div class="mt-auto">
                            <div class="flex items-center gap-2 mb-3">
                                <span class="text-lg md:text-xl font-black text-gray-900">Rs {prod['final_price']}</span>
                                <span class="text-xs text-gray-500 font-bold line-through">Rs {prod['fake_price']}</span>
                            </div>
                            <div class="block text-center bg-teal-50 text-teal-800 py-2.5 rounded-xl text-sm font-bold w-full border border-teal-200 hover:bg-teal-100 transition" aria-hidden="true">
                                <i class="fas fa-cart-shopping mr-1"></i> Add to Cart
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

    # ================= 3. GENERATE CHECKOUT PAGE =================
    pak_cities = ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Multan", "Peshawar", "Quetta", "Gujranwala", "Sialkot", "Hyderabad", "Bahawalpur", "Sargodha", "Other"]
    city_options = "".join([f"<option value='{city}'>{city}</option>" for city in pak_cities])
    
    checkout_html = get_html_header("Secure Checkout")
    checkout_html += f"""
    <div class="container mx-auto px-4 py-12 max-w-4xl">
        <div class="flex flex-col md:flex-row gap-8">
            <!-- Form Section -->
            <div class="md:w-2/3 bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-200">
                <div class="bg-gray-900 p-6 text-white relative">
                    <div class="absolute top-0 left-0 w-full h-1 bg-teal-500"></div>
                    <h1 class="text-2xl font-extrabold"><i class="fas fa-map-marker-alt text-teal-400 mr-2" aria-hidden="true"></i> Shipping Details</h1>
                </div>
                
                <form id="checkoutForm" class="p-6 md:p-8 space-y-5">
                    <input type="hidden" name="_subject" value="New Order Received on ASM VEO!">
                    <input type="hidden" name="Product_Ordered" id="productField" value="Direct Checkout">
                    <input type="hidden" name="Total_Price" id="priceField" value="">

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <div>
                            <label for="fullName" class="block text-sm font-bold text-gray-800 mb-2">Full Name <span class="text-red-600">*</span></label>
                            <input type="text" id="fullName" name="Full_Name" class="w-full border-2 border-gray-300 p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-600 outline-none text-gray-900" required placeholder="e.g. Ali Abbas">
                        </div>
                        <div>
                            <label for="emailAddr" class="block text-sm font-bold text-gray-800 mb-2">Email Address</label>
                            <input type="email" id="emailAddr" name="Email" class="w-full border-2 border-gray-300 p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-600 outline-none text-gray-900" placeholder="you@example.com">
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <div>
                            <label for="phoneNum" class="block text-sm font-bold text-gray-800 mb-2">Mobile Number <span class="text-red-600">*</span></label>
                            <input type="tel" id="phoneNum" name="Phone_Number" class="w-full border-2 border-gray-300 p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-600 outline-none text-gray-900" required placeholder="0300-XXXXXXX">
                        </div>
                        <div>
                            <label for="citySelect" class="block text-sm font-bold text-gray-800 mb-2">City <span class="text-red-600">*</span></label>
                            <select id="citySelect" name="City" class="w-full border-2 border-gray-300 p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-600 outline-none font-semibold text-gray-900" required>
                                <option value="" disabled selected>Select your City</option>
                                {city_options}
                            </select>
                        </div>
                    </div>
                    
                    <div>
                        <label for="addressInput" class="block text-sm font-bold text-gray-800 mb-2">Complete Delivery Address <span class="text-red-600">*</span></label>
                        <textarea id="addressInput" name="Address" rows="2" class="w-full border-2 border-gray-300 p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-600 outline-none text-gray-900" required placeholder="House No, Street Name, Area..."></textarea>
                    </div>
                    
                    <div>
                        <label for="landmarkInput" class="block text-sm font-bold text-gray-800 mb-2">Nearest Landmark</label>
                        <input type="text" id="landmarkInput" name="Landmark" class="w-full border-2 border-gray-300 p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-600 outline-none text-gray-900" placeholder="e.g. Near HBL Bank">
                    </div>
                </form>
            </div>

            <!-- Order Summary Section -->
            <div class="md:w-1/3">
                <div class="bg-teal-50 rounded-3xl shadow-lg border border-teal-200 p-6 sticky top-24">
                    <h2 class="text-xl font-black text-gray-900 mb-4 border-b border-teal-300 pb-3">Order Summary</h2>
                    <div class="space-y-3 mb-6 text-sm font-semibold text-gray-800">
                        <div class="flex justify-between">
                            <span>Subtotal</span>
                            <span id="subtotalDisplay">Rs 0</span>
                        </div>
                        <div class="flex justify-between text-teal-800">
                            <span>Delivery Charges</span>
                            <span>Rs 250</span>
                        </div>
                    </div>
                    <div class="flex justify-between items-center border-t border-teal-300 pt-4 mb-6">
                        <span class="font-black text-lg text-gray-900">Total (COD)</span>
                        <span class="font-black text-2xl text-teal-800" id="grandTotalDisplay">Rs 250</span>
                    </div>
                    <button type="submit" form="checkoutForm" id="submitBtn" class="w-full bg-gray-900 text-white font-black py-4 px-4 rounded-xl hover:bg-teal-700 transition-all duration-300 shadow-xl text-lg transform hover:-translate-y-1 focus:outline-none focus:ring-4 focus:ring-teal-500">
                        <i class="fas fa-check-circle mr-2" aria-hidden="true"></i> Confirm Order
                    </button>
                    
                    <a href="https://wa.me/923425478683?text=Hi,%20I%20want%20to%20order%20manually!" aria-label="Order Manually via WhatsApp" class="w-full bg-green-500 text-white font-black py-4 px-4 rounded-xl hover:bg-green-600 transition-all duration-300 shadow-xl text-lg mt-4 flex items-center justify-center gap-2 transform hover:-translate-y-1 focus:outline-none focus:ring-4 focus:ring-green-400">
                        <i class="fab fa-whatsapp text-xl" aria-hidden="true"></i> Order via WhatsApp
                    </a>
                    
                    <div class="mt-6 flex flex-col gap-2 text-xs text-gray-600 font-semibold text-center">
                        <span class="flex justify-center items-center gap-1"><i class="fas fa-money-bill-wave text-green-600" aria-hidden="true"></i> Pay in Cash upon delivery</span>
                        <span class="flex justify-center items-center gap-1"><i class="fas fa-shield-alt text-teal-600" aria-hidden="true"></i> Your details are 100% secure</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const urlParams = new URLSearchParams(window.location.search);
        const productName = urlParams.get('product');
        const productPrice = urlParams.get('price');
        
        if(productName && productPrice) {{
            document.getElementById('productField').value = productName;
            document.getElementById('priceField').value = productPrice;
            document.getElementById('subtotalDisplay').innerText = "Rs " + productPrice;
            document.getElementById('grandTotalDisplay').innerText = "Rs " + (parseInt(productPrice) + 250);
        }}

        document.getElementById('checkoutForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            const btn = document.getElementById('submitBtn');
            btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2" aria-hidden="true"></i> Processing...';
            btn.disabled = true;

            const formData = new FormData(this);

            fetch('https://formspree.io/f/xjgnlgpw', {{
                method: 'POST',
                body: formData,
                headers: {{ 'Accept': 'application/json' }}
            }}).then(response => {{
                if (response.ok) {{
                    alert('Order Confirmed! Your order will be delivered soon.\\nTotal Amount to pay on delivery is ' + document.getElementById('grandTotalDisplay').innerText);
                    window.location.href = '/index.html';
                }} else {{
                    alert('Oops! There was a problem submitting your order. Please try again.');
                    btn.innerHTML = '<i class="fas fa-check-circle mr-2" aria-hidden="true"></i> Confirm Order';
                    btn.disabled = false;
                }}
            }}).catch(error => {{
                alert('Network Error! Please try again.');
                btn.innerHTML = '<i class="fas fa-check-circle mr-2" aria-hidden="true"></i> Confirm Order';
                btn.disabled = false;
            }});
        }});
    </script>
    """
    checkout_html += get_html_footer()
    with open("output/checkout.html", "w", encoding="utf-8") as f:
        f.write(checkout_html)
        
    generate_sitemap(sitemap_urls)
        
    print("🎉 تمام فائلز لائٹ ہاؤس (Lighthouse) کی اپڈیٹس کے ساتھ بن چکی ہیں!")

if __name__ == "__main__":
    process_woocommerce_csv()
