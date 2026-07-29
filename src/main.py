import os
import csv
import math
import re
import shutil
import random
import json
import urllib.parse
from datetime import datetime, timedelta

# ==================== 2000 NAMES DATABASE ====================

def generate_pakistani_names():
    first_names = ["Muhammad", "Ali", "Ahmed", "Hassan", "Hussain", "Bilal", "Usman", "Umar", "Hamza", "Zain", 
                   "Ayesha", "Fatima", "Maryam", "Zainab", "Hira", "Sana", "Iqra", "Anum", "Sadia", "Aiman",
                   "Abdullah", "Rehman", "Tariq", "Imran", "Kamran", "Asad", "Faisal", "Shahid", "Waqar", "Naveed",
                   "Bilal", "Sana", "Adnan", "Farhan", "Nida", "Saba", "Komail", "Mahnoor",
                   "Rizwan", "Sohail", "Asif", "Nadeem", "Tahir", "Amir", "Babar", "Saad", "Fahad", "Junaid",
                   "Hina", "Areeba", "Tooba", "Rabia", "Anila", "Faiza", "Samina", "Naila", "Shazia", "Rimsha",
                   "Ahsan", "Zeeshan", "Kashif", "Noman", "Waseem", "Imtiaz", "Ghulam", "Sajid", "Rashid", "Aslam"]
    last_names = ["Khan", "Raza", "Malik", "Sheikh", "Qureshi", "Siddiqui", "Chaudhry", "Butt", "Awan", "Mughal",
                  "Baig", "Mirza", "Hashmi", "Tariq", "Ahmed", "Iqbal", "Hussain", "Aslam", "Akram", "Yousaf",
                  "Shah", "Rana", "Cheema", "Tipu", "Afridi", "Khattak", "Wazir", "Mehmood", "Sattar"]
    
    all_names = [f"{f} {l}" for f in first_names for l in last_names]
    random.shuffle(all_names)
    return all_names

PAKISTANI_NAMES = generate_pakistani_names()

# ==================== UTILITY FUNCTIONS ====================

# Bug 10 Fix: Global set to prevent duplicate slugs
GENERATED_SLUGS = set()

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

def make_slug(text):
    if not text: return "uncategorized"
    slug = re.sub(r'[^a-z0-9]+', '-', str(text).lower()).strip('-')
    if not slug: slug = "uncategorized"
    
    base_slug = slug
    counter = 1
    while slug in GENERATED_SLUGS:
        slug = f"{base_slug}-{counter}"
        counter += 1
    GENERATED_SLUGS.add(slug)
    return slug

def local_seo_desc(name, desc):
    if desc and len(desc) > 50:
        return desc[:160] + "..."
    return f"Buy {name} online in Pakistan at best price. Premium quality with Cash on Delivery, fast shipping & easy returns from ASM VEO."

def get_category_icon(category):
    cat_lower = category.lower()
    icons = {
        'perfume|fragrance|scent|attar': 'fa-spray-can',
        'watch|clock|smartwatch': 'fa-clock',
        'apparel|cloth|fashion|shirt|dress': 'fa-tshirt',
        'shoe|footwear|sneaker': 'fa-shoe-prints',
        'electronic|tech|mobile|gadget|phone': 'fa-mobile-screen-button',
        'beauty|cosmetic|makeup|care|skin': 'fa-spa',
        'home|decor|kitchen': 'fa-house',
        'jewelry|jewel|ring|necklace|gold': 'fa-gem',
        'bag|wallet|purse|luggage': 'fa-bag-shopping',
        'book|stationary|pen': 'fa-book',
        'toy|game|kid|baby': 'fa-gamepad',
        'food|grocery|snack|drink': 'fa-basket-shopping',
        'health|medical|fitness|gym': 'fa-heart-pulse',
        'garden|plant|outdoor': 'fa-seedling',
        'auto|car|bike|motor': 'fa-car',
    }
    for pattern, icon in icons.items():
        if any(word in cat_lower for word in pattern.split('|')):
            return icon
    return 'fa-box-open'

def generate_reviews(product_name):
    templates = [
        "Bohot achi quality hai, delivery bhi time par mili. Highly recommended!",
        "I am really impressed with {name}. Exceeded my expectations!",
        "Price ke hisaab se kaafi behtar hai. Recommended for everyone.",
        "Original product mili hai, jesa dikhaya tha wesa hi aaya. Thank you!",
        "Mujhe yeh bohat pasand aaya. Thanks ASM VEO for quick delivery!",
        "100% Genuine product. Will definitely buy again from here.",
        "Packaging bohot achi thi aur product bhi perfect hai.",
        "Quality is outstanding, delivery was fast. 5 stars from me!",
        "Got exactly what was shown. Genuine product at best price.",
        "Bahut khush hoon is product se. ASM VEO is trustworthy."
    ]
    
    reviews_html = ""
    num_reviews = random.randint(4, 8)
    for i in range(num_reviews):
        reviewer = random.choice(PAKISTANI_NAMES)
        comment = random.choice(templates).format(name=product_name)
        stars = random.randint(4, 5)
        days_ago = random.randint(1, 60)
        
        reviews_html += f"""
        <div class="border-b border-gray-100 dark:border-gray-700 py-4 last:border-0 reveal">
            <div class="flex items-center gap-2 mb-2">
                <div class="w-9 h-9 rounded-full bg-[#E53935] text-white flex items-center justify-center font-bold text-sm" aria-hidden="true">{reviewer[0]}</div>
                <div>
                    <span class="font-bold text-gray-900 dark:text-white text-sm block">{reviewer}</span>
                    <span class="text-[10px] text-gray-500">{days_ago} days ago</span>
                </div>
                <span class="ml-auto text-[10px] text-green-700 bg-green-50 px-2 py-1 rounded-full font-bold"><i class="fas fa-check-circle" aria-hidden="true"></i> Verified</span>
            </div>
            <div class="text-yellow-500 text-xs mb-2" aria-label="{stars} out of 5 stars">
                {"<i class='fas fa-star' aria-hidden='true'></i>" * stars}
            </div>
            <p class="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">{comment}</p>
        </div>
        """
    
    avg_rating = round(sum(random.randint(4,5) for _ in range(num_reviews)) / num_reviews, 1)
    return reviews_html, avg_rating, num_reviews

# ==================== HTML HEADER ====================

def get_html_header(title, categories_list=[], seo_desc="ASM VEO - Premium Online Shopping in Pakistan", 
                    product_data=None, breadcrumb_data=None, og_image=None):
    
    cat_links = ""
    for cat in categories_list:
        c_slug = make_slug(cat) # Bug 10 fix applies here, but we need consistent mapping
        # Since make_slug now modifies global state, we must ensure categories are processed once.
        # To avoid complexity, we map categories to their final slugs before header generation in main.
        pass

    # Actually, let's handle category links safely outside to avoid global state issues in loops.
    # We will build cat_links in the main processor and pass it here if needed, 
    # but to keep the function signature, we'll just build it safely.
    cat_links = ""
    for cat in categories_list:
        c_slug = re.sub(r'[^a-z0-9]+', '-', cat.lower()).strip('-')
        cat_links += f'<a href="/category/{c_slug}.html" class="block px-4 py-2.5 text-sm text-gray-700 hover:bg-[#E53935] hover:text-white transition-colors">{cat}</a>\n'

    structured_data = ""
    if product_data:
        # Bug 1 Fix: Escape double quotes for JSON-LD schema
        safe_schema_name = product_data['name'].replace('\\', '\\\\').replace('"', '\\"')
        safe_schema_desc = product_data.get('seo_desc', '').replace('\\', '\\\\').replace('"', '\\"')
        structured_data = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org/",
      "@type": "Product",
      "name": "{safe_schema_name}",
      "image": ["{product_data['image']}"],
      "description": "{safe_schema_desc}",
      "brand": {{ "@type": "Brand", "name": "ASM VEO" }},
      "offers": {{
        "@type": "Offer",
        "priceCurrency": "PKR",
        "price": "{product_data['final_price']}",
        "availability": "https://schema.org/InStock",
        "seller": {{ "@type": "Organization", "name": "ASM VEO" }}
      }},
      "aggregateRating": {{
        "@type": "AggregateRating",
        "ratingValue": "{product_data.get('rating', 4.5)}",
        "reviewCount": "{product_data.get('review_count', 10)}"
      }}
    }}
    </script>"""
    
    if breadcrumb_data:
        safe_bc_cat = breadcrumb_data['category'].replace('\\', '\\\\').replace('"', '\\"')
        safe_bc_name = breadcrumb_data['name'].replace('\\', '\\\\').replace('"', '\\"')
        c_slug = re.sub(r'[^a-z0-9]+', '-', breadcrumb_data['category'].lower()).strip('-')
        structured_data += f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.asmveo.com/" }},
        {{ "@type": "ListItem", "position": 2, "name": "{safe_bc_cat}", "item": "https://www.asmveo.com/category/{c_slug}.html" }},
        {{ "@type": "ListItem", "position": 3, "name": "{safe_bc_name}", "item": "https://www.asmveo.com/product/{breadcrumb_data['slug']}.html" }}
      ]
    }}
    </script>"""

    og_image_final = og_image or "https://www.asmveo.com/assets/og-image.jpg"
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <title>{title} | Buy Online in Pakistan | ASM VEO</title>
    
    <meta name="title" content="{title} | Buy Online in Pakistan | ASM VEO">
    <meta name="description" content="Buy {title} online in Pakistan at best price. Cash on Delivery available all over Pakistan. Shop premium quality products with fast shipping & easy returns at ASM VEO.">
    <meta name="keywords" content="buy {title} in Pakistan, {title} price in Pakistan, online shopping Pakistan, cash on delivery, ASM VEO, best online store Pakistan, Karachi, Lahore, Islamabad">
    <meta name="author" content="ASM Digital Solutions">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta name="theme-color" content="#E53935">
    <link rel="canonical" href="https://www.asmveo.com/">
    
    <meta name="geo.region" content="PK" />
    <meta name="geo.placename" content="Pakistan" />
    <meta name="geo.position" content="30.3753;69.3451" />
    <meta name="ICBM" content="30.3753, 69.3451" />
    
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://www.asmveo.com/">
    <meta property="og:title" content="{title} | Buy Online in Pakistan | ASM VEO">
    <meta property="og:description" content="Shop {title} online in Pakistan. Cash on Delivery available. Fast shipping & easy returns.">
    <meta property="og:image" content="{og_image_final}">
    <meta property="og:locale" content="en_PK">
    <meta property="og:site_name" content="ASM VEO">
    
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:title" content="{title} | ASM VEO Pakistan">
    <meta property="twitter:description" content="Shop {title} online in Pakistan. COD available.">
    <meta property="twitter:image" content="{og_image_final}">
    
    <link rel="manifest" href="/manifest.json">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="ASM VEO">
    
    <link rel="preconnect" href="https://cdn.tailwindcss.com">
    <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{ pk: {{ red: '#E53935', light: '#FFEBEE', dark: '#C62828' }} }}
                }}
            }}
        }}
    </script>
    
    <link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"></noscript>
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');
        
        body {{ 
            font-family: 'Plus Jakarta Sans', sans-serif; 
            background: #f3f4f6; 
            color: #1f2937;
            transition: background-color 0.3s; 
            padding-bottom: 70px; 
        }}
        .dark body {{ background: #111827; color: #f3f4f6; }}
        
        .product-card {{ transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); content-visibility: auto; contain-intrinsic-size: 300px; }}
        .product-card:hover {{ transform: translateY(-5px); box-shadow: 0 15px 30px -10px rgba(229, 57, 53, 0.2); }}
        .image-zoom img {{ transition: transform 0.5s ease; }}
        .product-card:hover .image-zoom img {{ transform: scale(1.08); }}
        .dropdown:hover .dropdown-menu {{ display: block; }}
        
        ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
        ::-webkit-scrollbar-track {{ background: #f1f5f9; }}
        ::-webkit-scrollbar-thumb {{ background: #E53935; border-radius: 4px; }}
        
        .line-clamp-1 {{ display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden; }}
        .line-clamp-2 {{ display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
        
        @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-15px); }} }}
        .animate-float {{ animation: float 6s ease-in-out infinite; }}
        
        @keyframes pulse-ring {{ 0% {{ box-shadow: 0 0 0 0 rgba(229, 57, 53, 0.7); }} 70% {{ box-shadow: 0 0 0 15px rgba(229, 57, 53, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(229, 57, 53, 0); }} }}
        .pulse-ring {{ animation: pulse-ring 2s infinite; }}
        
        @keyframes slideIn {{ from {{ transform: translateY(20px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}
        .slide-in {{ animation: slideIn 0.4s ease-out; }}
        
        .carousel-track {{ display: flex; transition: transform 0.8s cubic-bezier(0.65, 0, 0.35, 1); }}
        .carousel-slide {{ min-width: 100%; box-sizing: border-box; }}
        
        .glass {{ background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); color: #1f2937; }}
        .dark .glass {{ background: rgba(17, 24, 39, 0.95); color: #fff; }}
        
        .reveal {{ opacity: 0; transform: translateY(40px); transition: all 0.8s cubic-bezier(0.5, 0, 0, 1); }}
        .reveal.active {{ opacity: 1; transform: translateY(0); }}
        
        .animated-bg {{ background: linear-gradient(-45deg, #E53935, #C62828, #E53935, #B71C1C); background-size: 400% 400%; animation: gradient 15s ease infinite; }}
        @keyframes gradient {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
    </style>
    {structured_data}

    <script>
        function getCart() {{ return JSON.parse(localStorage.getItem('asm_cart')) || []; }}
        function saveCart(cart) {{ localStorage.setItem('asm_cart', JSON.stringify(cart)); updateCartBadge(); }}
        
        function updateCartBadge() {{
            let cart = getCart();
            let cartCount = cart.reduce((sum, item) => sum + (item.qty || 1), 0);
            document.querySelectorAll('.cart-badge').forEach(el => el.innerText = cartCount);
        }}

        function addToCart(name, price, image, event) {{
            if(event) event.stopPropagation();
            let cart = getCart();
            let existing = cart.find(item => item.name === name);
            if (existing) {{ existing.qty = (existing.qty || 1) + 1; }}
            else {{ cart.push({{name, price: parseFloat(price), image, qty: 1}}); }}
            saveCart(cart);
            showToast('Added to Cart!', 'fa-cart-plus', 'pk');
            pulseCartIcon();
        }}

        function removeFromCart(index) {{
            let cart = getCart();
            cart.splice(index, 1);
            saveCart(cart);
            if (typeof renderCart === 'function') renderCart();
        }}

        function updateQty(index, delta) {{
            let cart = getCart();
            if (!cart[index]) return;
            cart[index].qty = (cart[index].qty || 1) + delta;
            if (cart[index].qty < 1) {{ cart.splice(index, 1); }}
            saveCart(cart);
            if (typeof renderCart === 'function') renderCart();
        }}

        function buyNow(name, price, image, event) {{
            if(event) event.stopPropagation();
            window.location.href = '/checkout.html?buy_now=true&product=' + encodeURIComponent(name) + '&price=' + price;
        }}

        function getWishlist() {{ return JSON.parse(localStorage.getItem('asm_wishlist')) || []; }}
        function toggleWishlist(name, price, image, event) {{
            if(event) event.stopPropagation();
            let wishlist = getWishlist();
            let idx = wishlist.findIndex(item => item.name === name);
            if (idx > -1) {{ wishlist.splice(idx, 1); showToast('Removed from Wishlist', 'fa-heart-broken', 'gray'); }}
            else {{ wishlist.push({{name, price, image}}); showToast('Added to Wishlist!', 'fa-heart', 'red'); }}
            localStorage.setItem('asm_wishlist', JSON.stringify(wishlist));
            updateWishlistBadge();
        }}
        function updateWishlistBadge() {{
            let wl = getWishlist();
            document.querySelectorAll('.wishlist-badge').forEach(el => el.innerText = wl.length);
        }}

        function addToRecentlyViewed(product) {{
            let recent = JSON.parse(localStorage.getItem('asm_recent')) || [];
            recent = recent.filter(p => p.slug !== product.slug);
            recent.unshift(product);
            recent = recent.slice(0, 10);
            localStorage.setItem('asm_recent', JSON.stringify(recent));
        }}

        function showToast(msg, icon='fa-check-circle', color='pk') {{
            const colors = {{ pk: 'bg-[#E53935]', red: 'bg-red-500', gray: 'bg-gray-600', green: 'bg-green-500' }};
            const toast = document.createElement('div');
            toast.className = `fixed bottom-20 md:bottom-4 right-4 ${{colors[color]}} text-white px-6 py-3 rounded-xl shadow-2xl z-[9999] transform transition-all duration-300 translate-y-0 opacity-100 flex items-center gap-3 font-bold slide-in`;
            toast.innerHTML = `<i class="fas ${{icon}} text-xl"></i> ${{msg}}`;
            document.body.appendChild(toast);
            setTimeout(() => {{ toast.style.opacity = '0'; toast.style.transform = 'translateY(20px)'; setTimeout(() => toast.remove(), 300); }}, 2500);
        }}

        function pulseCartIcon() {{
            let cartIcon = document.querySelector('.cart-icon-pulse');
            if (cartIcon) {{ cartIcon.classList.add('scale-125'); setTimeout(() => cartIcon.classList.remove('scale-125'), 200); }}
        }}

        let searchLoaded = false;
        function loadSearchData() {{
            if(searchLoaded) return;
            searchLoaded = true;
            let script = document.createElement('script');
            script.src = '/search-data.js';
            document.head.appendChild(script);
        }}

        function executeSearch() {{
            let val = document.getElementById('searchInput').value;
            if(val.trim() !== "") window.location.href = '/index.html?search=' + encodeURIComponent(val);
        }}
        function handleSearch(e) {{ if (e.key === 'Enter') executeSearch(); }}

        function toggleDarkMode() {{
            document.documentElement.classList.toggle('dark');
            localStorage.setItem('asm_dark', document.documentElement.classList.contains('dark'));
            updateDarkModeIcon();
        }}
        function updateDarkModeIcon() {{
            let isDark = document.documentElement.classList.contains('dark');
            document.querySelectorAll('.dark-mode-icon').forEach(el => {{
                el.className = `fas ${{isDark ? 'fa-sun' : 'fa-moon'}} dark-mode-icon`;
            }});
        }}

        function scrollTop() {{ window.scrollTo({{top: 0, behavior: 'smooth'}}); }}

        function quickView(name, price, image, desc, slug) {{
            let modal = document.getElementById('quickViewModal');
            document.getElementById('qvImage').src = image;
            document.getElementById('qvName').innerText = name;
            document.getElementById('qvPrice').innerText = "Rs " + price;
            document.getElementById('qvDesc').innerText = desc.substring(0, 150) + '...';
            
            let safeName = name.split("'").join("\\'");
            let safeImage = image.split("'").join("\\'");
            document.getElementById('qvAddCart').setAttribute('onclick', `addToCart('${safeName}', ${price}, '${safeImage}', event); closeQuickView();`);
            document.getElementById('qvBuyNow').setAttribute('onclick', `buyNow('${safeName}', ${price}, '${safeImage}', event);`);
            document.getElementById('qvLink').href = '/product/' + slug + '.html';
            modal.classList.remove('hidden');
            modal.classList.add('flex');
        }}
        function closeQuickView() {{
            document.getElementById('quickViewModal').classList.add('hidden');
            document.getElementById('quickViewModal').classList.remove('flex');
        }}

        function toggleMobileCats() {{
            let menu = document.getElementById('mobileCatMenu');
            menu.classList.toggle('hidden');
        }}

        window.onload = function() {{
            updateCartBadge();
            updateWishlistBadge();
            if (localStorage.getItem('asm_dark') === 'true') {{
                document.documentElement.classList.add('dark');
                updateDarkModeIcon();
            }}
            if (!localStorage.getItem('asm_cookie_consent')) {{
                document.getElementById('cookieConsent').classList.remove('hidden');
            }}
            if (!localStorage.getItem('asm_exit_intent')) {{
                document.addEventListener('mouseleave', function(e) {{
                    if (e.clientY < 10) {{
                        document.getElementById('exitModal').classList.remove('hidden');
                        document.getElementById('exitModal').classList.add('flex');
                        localStorage.setItem('asm_exit_intent', 'true');
                    }}
                }});
            }}
            window.addEventListener('scroll', function() {{
                let btn = document.getElementById('backToTop');
                if (btn) btn.style.display = window.scrollY > 400 ? 'flex' : 'none';
            }});

            let reveals = document.querySelectorAll('.reveal');
            function checkReveals() {{
                reveals.forEach(el => {{
                    let elTop = el.getBoundingClientRect().top;
                    if (elTop < window.innerHeight - 50) el.classList.add('active');
                }});
            }}
            window.addEventListener('scroll', checkReveals);
            checkReveals();

            let searchInput = document.getElementById('searchInput');
            if(searchInput) {{
                searchInput.addEventListener('focus', loadSearchData);
            }}
            
            // Bug 8 Fix: Close mobile menu on outside click
            document.addEventListener('click', function(event) {{
                let menu = document.getElementById('mobileCatMenu');
                let btn = document.querySelector('[onclick="toggleMobileCats()"]');
                if (menu && !menu.classList.contains('hidden') && !menu.contains(event.target) && !btn.contains(event.target)) {{
                    menu.classList.add('hidden');
                }}
            }});
        }};

        function acceptCookies() {{
            localStorage.setItem('asm_cookie_consent', 'true');
            document.getElementById('cookieConsent').classList.add('hidden');
        }}
    </script>
</head>
<body class="text-gray-900 dark:text-gray-100">
    <!-- Flashmart Style Top Bar -->
    <div class="bg-gray-900 text-white text-xs py-2 hidden md:block">
        <div class="container mx-auto px-4 flex justify-between items-center">
            <span>Welcome to ASM VEO! Fast Delivery & Cash on Delivery Available</span>
            <div class="flex gap-4 items-center">
                <button onclick="toggleDarkMode()" class="hover:text-[#E53935]" aria-label="Toggle Dark Mode"><i class="fas fa-moon dark-mode-icon"></i></button>
                <span class="border-l border-gray-700 pl-4">EN</span>
                <span class="border-l border-gray-700 pl-4">PKR</span>
                <a href="/about.html" class="hover:text-[#E53935] border-l border-gray-700 pl-4">About</a>
                <a href="/contact.html" class="hover:text-[#E53935] border-l border-gray-700 pl-4">Contact</a>
            </div>
        </div>
    </div>

    <header class="glass shadow-md sticky top-0 z-50 transition-colors border-b border-gray-100 dark:border-gray-800">
        <div class="bg-[#E53935] text-white text-xs md:text-sm py-2 md:hidden">
            <div class="container mx-auto px-4 flex justify-between items-center">
                <a href="/index.html" class="hover:text-gray-300 transition font-semibold"><i class="fas fa-home mr-1"></i> Home</a>
                <button onclick="toggleMobileCats()" class="hover:text-gray-300 transition font-semibold focus:outline-none"><i class="fas fa-list mr-1"></i> Categories</button>
            </div>
        </div>

        <div id="mobileCatMenu" class="hidden md:hidden bg-white dark:bg-gray-800 border-b border-gray-100 dark:border-gray-700">
            <div class="container mx-auto px-4 py-2 grid grid-cols-2 gap-2 max-h-60 overflow-y-auto">
                {''.join([f'<a href="/category/{re.sub(r"[^a-z0-9]+", "-", cat.lower()).strip("-")}.html" class="block py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-[#E53935] hover:text-white px-2 rounded">{cat}</a>' for cat in categories_list])}
            </div>
        </div>

        <div class="container mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-4">
            <a href="/index.html" class="flex items-center gap-2" aria-label="ASM VEO Home">
                <svg width="40" height="40" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="50" r="48" fill="#E53935"></circle>
                    <path d="M65 35 A 25 25 0 1 0 65 65 A 20 20 0 1 1 65 35 Z" fill="#ffffff"></path>
                    <text x="50" y="58" font-family="Arial" font-size="24" font-weight="900" fill="#E53935" text-anchor="middle">AV</text>
                </svg>
                <div class="flex flex-col leading-none">
                    <span class="text-xl font-extrabold text-[#E53935] dark:text-white tracking-tight">ASM VEO</span>
                    <span class="text-[9px] tracking-widest text-gray-500 dark:text-gray-400 font-bold">PAKISTAN</span>
                </div>
            </a>
            
            <div class="flex-1 min-w-[200px] max-w-xl mx-0 md:mx-8 relative flex">
                <label for="searchInput" class="sr-only">Search products in Pakistan</label>
                <input type="text" id="searchInput" onkeypress="handleSearch(event)" placeholder="Search products, brands, categories..." class="w-full bg-gray-50 dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 focus:bg-white dark:focus:bg-gray-700 focus:border-[#E53935] rounded-l-xl py-2.5 px-6 outline-none transition-all text-gray-800 dark:text-gray-100 font-semibold shadow-sm text-sm">
                <button onclick="executeSearch()" aria-label="Search" class="bg-[#E53935] text-white px-6 rounded-r-xl hover:bg-[#C62828] transition-colors flex items-center justify-center"><i class="fas fa-search text-lg" aria-hidden="true"></i></button>
            </div>
            
            <div class="flex items-center gap-3">
                <a href="/wishlist.html" class="relative bg-gray-50 text-[#E53935] p-2.5 rounded-xl hover:bg-[#E53935] hover:text-white transition-colors border border-gray-200" aria-label="Wishlist">
                    <i class="fas fa-heart"></i>
                    <span class="wishlist-badge absolute -top-2 -right-2 bg-[#E53935] text-white text-xs font-black px-1.5 py-0.5 rounded-full shadow min-w-[20px] text-center">0</span>
                </a>
                <a href="/checkout.html" class="cart-icon-pulse relative bg-[#E53935] text-white px-4 py-2.5 rounded-xl font-bold hover:bg-[#C62828] transition-colors shadow-sm flex items-center gap-2 text-sm" aria-label="Go to Cart">
                    <i class="fas fa-shopping-cart text-lg" aria-hidden="true"></i>
                    <span class="hidden md:inline">Cart</span>
                    <span class="cart-badge absolute -top-2 -right-2 bg-gray-900 text-white text-xs font-black px-1.5 py-0.5 rounded-full shadow min-w-[20px] text-center">0</span>
                </a>
            </div>
        </div>

        <!-- Flashmart Style Navigation Bar -->
        <nav class="hidden md:block border-t border-gray-100 dark:border-gray-800">
            <div class="container mx-auto px-4 flex items-center gap-6">
                <div class="relative dropdown z-50">
                    <button class="bg-[#E53935] text-white px-4 py-2.5 font-bold text-sm flex items-center gap-2 hover:bg-[#C62828] transition-colors"><i class="fas fa-list"></i> All Categories <i class="fas fa-chevron-down text-[10px]"></i></button>
                    <div class="dropdown-menu absolute hidden text-gray-700 bg-white dark:bg-gray-800 dark:text-gray-200 shadow-2xl rounded-b-xl mt-0 w-56 py-2 border border-gray-100 dark:border-gray-700 max-h-96 overflow-y-auto">
                        {cat_links}
                    </div>
                </div>
                <a href="/index.html" class="py-2.5 text-sm font-bold text-gray-700 dark:text-gray-200 hover:text-[#E53935] transition">Home</a>
                <a href="/index.html#products" class="py-2.5 text-sm font-bold text-gray-700 dark:text-gray-200 hover:text-[#E53935] transition">Shop</a>
                <a href="/about.html" class="py-2.5 text-sm font-bold text-gray-700 dark:text-gray-200 hover:text-[#E53935] transition">About Us</a>
                <a href="/contact.html" class="py-2.5 text-sm font-bold text-gray-700 dark:text-gray-200 hover:text-[#E53935] transition">Contact Us</a>
                <a href="/faq.html" class="py-2.5 text-sm font-bold text-gray-700 dark:text-gray-200 hover:text-[#E53935] transition">FAQ</a>
                <div class="ml-auto text-xs font-bold text-gray-500 dark:text-gray-400"><i class="fas fa-phone mr-1 text-[#E53935]"></i> 0342 54 786 83</div>
            </div>
        </nav>
    </header>

    <div id="cookieConsent" class="hidden fixed bottom-20 md:bottom-0 left-0 right-0 bg-gray-900 text-white p-4 z-[9998] shadow-2xl">
        <div class="container mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-3">
                <i class="fas fa-cookie-bite text-2xl text-white"></i>
                <p class="text-sm">We use cookies to improve your experience. By continuing to browse, you agree to our use of cookies.</p>
            </div>
            <div class="flex gap-3">
                <a href="/privacy.html" class="text-white hover:text-gray-300 text-sm font-bold">Privacy Policy</a>
                <button onclick="acceptCookies()" class="bg-[#E53935] hover:bg-[#C62828] px-6 py-2 rounded-lg font-bold text-sm transition">Accept</button>
            </div>
        </div>
    </div>

    <nav class="fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-900 shadow-2xl border-t border-gray-100 dark:border-gray-800 flex justify-around py-2 md:hidden z-50">
        <a href="/index.html" class="flex flex-col items-center text-[#E53935] text-xs font-bold"><i class="fas fa-home text-lg mb-1"></i> Home</a>
        <button onclick="toggleMobileCats()" class="flex flex-col items-center text-gray-500 dark:text-gray-400 text-xs font-bold"><i class="fas fa-th-large text-lg mb-1"></i> Categories</button>
        <a href="/checkout.html" class="flex flex-col items-center text-gray-500 dark:text-gray-400 text-xs font-bold relative">
            <i class="fas fa-shopping-cart text-lg mb-1"></i> Cart
            <span class="cart-badge absolute -top-1 right-2 bg-[#E53935] text-white text-[8px] font-black px-1 py-0.5 rounded-full">0</span>
        </a>
        <a href="/wishlist.html" class="flex flex-col items-center text-gray-500 dark:text-gray-400 text-xs font-bold relative">
            <i class="fas fa-heart text-lg mb-1"></i> Wishlist
            <span class="wishlist-badge absolute -top-1 right-2 bg-[#E53935] text-white text-[8px] font-black px-1 py-0.5 rounded-full">0</span>
        </a>
    </nav>

    <div id="exitModal" class="hidden fixed inset-0 bg-black/70 z-[9999] items-center justify-center p-4">
        <div class="bg-white dark:bg-gray-800 rounded-3xl p-8 max-w-md w-full text-center relative slide-in">
            <button onclick="document.getElementById('exitModal').classList.add('hidden')" class="absolute top-4 right-4 text-gray-400 hover:text-gray-600"><i class="fas fa-times text-xl"></i></button>
            <i class="fas fa-gift text-6xl text-[#E53935] mb-4"></i>
            <h2 class="text-2xl font-extrabold text-gray-900 dark:text-white mb-2">Wait! Here's 10% OFF</h2>
            <p class="text-gray-500 dark:text-gray-400 mb-6">Don't leave empty-handed. Use this code at checkout for an instant 10% discount on your order!</p>
            <div class="bg-gray-50 border-2 border-dashed border-[#E53935] rounded-xl py-4 mb-6">
                <span class="text-3xl font-black text-[#E53935] tracking-widest">ASM10</span>
            </div>
            <a href="/index.html#products" onclick="document.getElementById('exitModal').classList.add('hidden')" class="block bg-[#E53935] text-white py-3 rounded-xl font-bold hover:bg-[#C62828] transition">Continue Shopping</a>
        </div>
    </div>

    <div id="quickViewModal" class="hidden fixed inset-0 bg-black/70 z-[9999] items-center justify-center p-4">
        <div class="bg-white dark:bg-gray-800 rounded-3xl max-w-3xl w-full overflow-hidden relative slide-in flex flex-col md:flex-row">
            <button onclick="closeQuickView()" class="absolute top-4 right-4 bg-white/80 rounded-full p-2 text-gray-700 hover:bg-white z-10"><i class="fas fa-times text-xl"></i></button>
            <div class="md:w-1/2 bg-gray-50 dark:bg-gray-900 p-4 flex items-center justify-center">
                <img id="qvImage" src="" alt="Product Image" class="max-h-[300px] object-contain rounded-xl" width="300" height="300">
            </div>
            <div class="md:w-1/2 p-6 flex flex-col">
                <h2 id="qvName" class="text-xl font-extrabold text-gray-900 dark:text-white mb-2"></h2>
                <p id="qvPrice" class="text-2xl font-black text-[#E53935] dark:text-white mb-3"></p>
                <p id="qvDesc" class="text-sm text-gray-500 dark:text-gray-400 mb-6"></p>
                <div class="mt-auto flex flex-col gap-2">
                    <button id="qvAddCart" class="w-full bg-[#E53935] text-white py-3 rounded-xl font-bold hover:bg-[#C62828] transition flex items-center justify-center gap-2"><i class="fas fa-cart-plus"></i> Add to Cart</button>
                    <button id="qvBuyNow" class="w-full bg-gray-900 dark:bg-white text-white dark:text-gray-900 py-3 rounded-xl font-bold hover:bg-gray-800 dark:hover:bg-gray-100 transition flex items-center justify-center gap-2"><i class="fas fa-bolt"></i> Buy Now</button>
                    <a id="qvLink" href="#" class="text-center text-sm text-[#E53935] hover:underline mt-2">View Full Details</a>
                </div>
            </div>
        </div>
    </div>

    <a href="https://wa.me/923425478683?text=Hi,%20I%20want%20to%20know%20about%20your%20products" target="_blank" 
       class="fixed bottom-24 right-4 bg-green-500 text-white w-14 h-14 rounded-full shadow-2xl flex items-center justify-center hover:bg-green-600 transition-all z-50 hover:scale-110 pulse-ring" 
       aria-label="Chat on WhatsApp">
        <i class="fab fa-whatsapp text-3xl"></i>
    </a>

    <button id="backToTop" onclick="scrollTop()" class="hidden fixed bottom-24 left-4 bg-[#E53935] text-white w-12 h-12 rounded-full shadow-2xl items-center justify-center hover:bg-[#C62828] transition z-50" aria-label="Back to top">
        <i class="fas fa-arrow-up text-xl"></i>
    </button>

    <main id="main-content" class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 shadow-2xl">
"""

# ==================== HTML FOOTER ====================

def get_html_footer():
    return """
    </main>
    <!-- Flashmart Style Footer -->
    <footer class="bg-gray-50 dark:bg-gray-950 text-gray-800 dark:text-gray-200 mt-16 pt-12 pb-20 md:pb-8 border-t-4 border-[#E53935]">
        <div class="container mx-auto px-4">
            <div class="flex flex-wrap justify-center items-center gap-8 mb-12 pb-8 border-b border-gray-200 dark:border-gray-800">
                <div class="text-gray-300 dark:text-gray-700 font-extrabold text-2xl">EVERSOURCE</div>
                <div class="text-gray-300 dark:text-gray-700 font-extrabold text-2xl">LOGO</div>
                <div class="text-gray-300 dark:text-gray-700 font-extrabold text-2xl">CYCLOPS</div>
                <div class="text-gray-300 dark:text-gray-700 font-extrabold text-2xl">ENVATO</div>
                <div class="text-gray-300 dark:text-gray-700 font-extrabold text-2xl">ASM</div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-5 gap-10 mb-10">
                <div>
                    <h3 class="text-lg font-bold mb-5 text-gray-900 dark:text-white border-b border-gray-200 dark:border-gray-800 pb-2">Company</h3>
                    <ul class="space-y-3 text-sm font-semibold">
                        <li><a href="/about.html" class="hover:text-[#E53935] transition">About Us</a></li>
                        <li><a href="/contact.html" class="hover:text-[#E53935] transition">Contact Us</a></li>
                        <li><a href="/faq.html" class="hover:text-[#E53935] transition">FAQ</a></li>
                        <li><a href="/privacy.html" class="hover:text-[#E53935] transition">Privacy Policy</a></li>
                        <li><a href="/terms.html" class="hover:text-[#E53935] transition">Terms & Conditions</a></li>
                    </ul>
                </div>
                <div>
                    <h3 class="text-lg font-bold mb-5 text-gray-900 dark:text-white border-b border-gray-200 dark:border-gray-800 pb-2">Support</h3>
                    <ul class="space-y-3 text-sm font-semibold">
                        <li><a href="/faq.html" class="hover:text-[#E53935] transition">Help Center</a></li>
                        <li><a href="/order-success.html" class="hover:text-[#E53935] transition">Track Order</a></li>
                        <li><a href="/terms.html" class="hover:text-[#E53935] transition">Returns Policy</a></li>
                        <li><a href="/privacy.html" class="hover:text-[#E53935] transition">Data Security</a></li>
                    </ul>
                </div>
                <div>
                    <h3 class="text-lg font-bold mb-5 text-gray-900 dark:text-white border-b border-gray-200 dark:border-gray-800 pb-2">Shop</h3>
                    <ul class="space-y-3 text-sm font-semibold">
                        <li><a href="/index.html#products" class="hover:text-[#E53935] transition">All Products</a></li>
                        <li><a href="/wishlist.html" class="hover:text-[#E53935] transition">My Wishlist</a></li>
                        <li><a href="/checkout.html" class="hover:text-[#E53935] transition">My Cart</a></li>
                        <li><a href="/index.html" class="hover:text-[#E53935] transition">Flash Sale</a></li>
                    </ul>
                </div>
                <div>
                    <h3 class="text-lg font-bold mb-5 text-gray-900 dark:text-white border-b border-gray-200 dark:border-gray-800 pb-2">Quick Links</h3>
                    <ul class="space-y-3 text-sm font-semibold">
                        <li><a href="/index.html" class="hover:text-[#E53935] transition">Home</a></li>
                        <li><a href="/checkout.html" class="hover:text-[#E53935] transition">Checkout</a></li>
                        <li><a href="/about.html" class="hover:text-[#E53935] transition">About Us</a></li>
                    </ul>
                </div>
                <div>
                    <h3 class="text-lg font-bold mb-5 text-gray-900 dark:text-white border-b border-gray-200 dark:border-gray-800 pb-2">Our Mission</h3>
                    <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">ASM VEO is Pakistan's premium online shopping platform by <strong class="text-gray-900 dark:text-white">ASM Digital Solutions</strong>. Enjoy premium quality products, nationwide COD, and 100% secure shopping.</p>
                    <div class="flex gap-3">
                        <a href="#" aria-label="Facebook" class="w-9 h-9 rounded-full bg-gray-200 dark:bg-gray-800 flex items-center justify-center hover:bg-[#E53935] hover:text-white transition text-gray-900 dark:text-white"><i class="fab fa-facebook-f"></i></a>
                        <a href="#" aria-label="Instagram" class="w-9 h-9 rounded-full bg-gray-200 dark:bg-gray-800 flex items-center justify-center hover:bg-[#E53935] hover:text-white transition text-gray-900 dark:text-white"><i class="fab fa-instagram"></i></a>
                        <a href="https://wa.me/923425478683" aria-label="WhatsApp" class="w-9 h-9 rounded-full bg-gray-200 dark:bg-gray-800 flex items-center justify-center hover:bg-[#E53935] hover:text-white transition text-gray-900 dark:text-white"><i class="fab fa-whatsapp"></i></a>
                    </div>
                </div>
            </div>
            <div class="bg-gray-100 dark:bg-gray-900 rounded-xl p-6 text-center mb-6">
                <h4 class="font-bold text-lg mb-2 text-gray-900 dark:text-white">Service Center</h4>
                <p class="text-sm text-gray-600 dark:text-gray-400 mb-1"><i class="fas fa-building mr-2 text-[#E53935]"></i> ASM Digital Solutions, Karachi, Pakistan</p>
                <p class="text-sm text-gray-600 dark:text-gray-400"><i class="fas fa-phone mr-2 text-[#E53935]"></i> <a href="https://wa.me/923425478683" class="font-bold hover:text-[#E53935]">0342 54 786 83</a> (Mon-Sun: 9AM - 11PM)</p>
            </div>
            <div class="border-t border-gray-200 dark:border-gray-800 text-center pt-8">
                <p class="text-gray-500 text-sm font-semibold">&copy; 2026 ASM Digital Solutions. All Rights Reserved. | Powered by ASM VEO</p>
            </div>
        </div>
    </footer>
</body>
</html>
"""

# ==================== SITEMAP & ROBOTS ====================

def generate_sitemap(urls):
    # Bug 5 Fix: Ensure unique URLs in sitemap
    urls = list(set(urls))
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    date_str = datetime.now().strftime("%Y-%m-%d")
    for url in urls:
        xml_content += f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{date_str}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"
    xml_content += '</urlset>'
    with open("output/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)

def generate_robots_txt():
    content = """User-agent: *
Allow: /
Disallow: /checkout.html

Sitemap: https://www.asmveo.com/sitemap.xml
"""
    with open("output/robots.txt", "w") as f:
        f.write(content)

def generate_manifest():
    manifest = {
        "name": "ASM VEO - Online Shopping in Pakistan",
        "short_name": "ASM VEO",
        "description": "Premium online shopping in Pakistan with Cash on Delivery",
        "start_url": "/index.html",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#E53935",
        "icons": [
            {"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}
        ]
    }
    with open("output/manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

# ==================== PRODUCT CARD GENERATOR ====================

def generate_product_card(prod, lazy=True, show_wishlist=True):
    # Bug 7 Fix: Prevent ZeroDivisionError
    discount = math.ceil(((prod['fake_price'] - prod['final_price']) / prod['fake_price']) * 100) if prod['fake_price'] > 0 and prod['fake_price'] > prod['final_price'] else 0
    stock_left = random.randint(3, 20)
    img_loading = 'loading="lazy"' if lazy else 'fetchpriority="high"'
    
    escaped_name = prod['name'].replace("\\", "\\\\").replace("'", "\\'")
    escaped_desc = prod['seo_desc'].replace("\\", "\\\\").replace("'", "\\'")
    
    # Bug 3 Fix: Escape double quotes for HTML attributes
    alt_name = prod['name'].replace('"', '&quot;')
    
    wishlist_btn = ""
    if show_wishlist:
        wishlist_btn = """
            <button onclick="toggleWishlist('__SAFE_NAME__', __PRICE__, '__IMAGE__', event)" 
                    class="wishlist-btn absolute top-2 right-2 w-8 h-8 bg-white rounded-full shadow-md flex items-center justify-center hover:bg-pink-50 transition z-10" 
                    aria-label="Add to Wishlist">
                <i class="fas fa-heart text-pink-500 text-sm"></i>
            </button>"""
    
    quick_view_btn = """
        <button onclick="quickView('__SAFE_NAME__', __PRICE__, '__IMAGE__', '__SAFE_DESC__', '__SLUG__')" 
                class="absolute top-2 right-12 w-8 h-8 bg-white rounded-full shadow-md flex items-center justify-center hover:bg-gray-100 transition z-10" 
                aria-label="Quick View">
            <i class="fas fa-eye text-[#E53935] text-sm"></i>
        </button>"""
    
    # Bug 4 Fix: Removed Dead Code (wa_text, wa_link)
    card = f"""
    <div class="product-card reveal bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col relative cursor-pointer" onclick="window.location.href='/product/{prod['slug']}.html'">
        {wishlist_btn}
        {quick_view_btn}
        {f'<div class="absolute top-2 left-2 bg-[#E53935] text-white text-[10px] font-black px-1.5 py-0.5 rounded z-10 shadow-md">-{discount}% OFF</div>' if discount > 0 else ''}
        <div class="image-zoom h-32 md:h-40 bg-gray-50 dark:bg-gray-700 overflow-hidden relative border-b border-gray-200 dark:border-gray-700 flex justify-center items-center">
            <img src="{prod['image']}" alt="{alt_name}" width="200" height="200" {img_loading} class="w-full h-full object-contain p-1" onerror="this.src='https://via.placeholder.com/200x200/E53935/ffffff?text=ASM+VEO'">
        </div>
        <div class="p-2 flex flex-col flex-grow">
            <span class="text-[9px] font-bold text-[#E53935] dark:text-white uppercase tracking-wider mb-1 line-clamp-1">{prod['category']}</span>
            <h3 class="text-[10px] md:text-xs font-bold text-gray-900 dark:text-gray-100 leading-tight mb-1 line-clamp-2">{prod['name']}</h3>
            <div class="mt-auto">
                <div class="flex items-center gap-1 mb-1">
                    <span class="text-xs md:text-sm font-black text-[#E53935] dark:text-white">Rs {prod['final_price']}</span>
                    <span class="text-[9px] text-gray-400 font-bold line-through">Rs {prod['fake_price']}</span>
                </div>
                <button onclick="addToCart('__SAFE_NAME__', __PRICE__, '__IMAGE__', event)" class="w-full bg-gray-50 text-[#E53935] py-1.5 rounded-md text-[10px] font-bold border border-gray-200 hover:bg-[#E53935] hover:text-white transition flex justify-center items-center" aria-label="Add to Cart">
                    <i class="fas fa-cart-plus"></i>
                </button>
            </div>
        </div>
    </div>
    """
    
    return card.replace("__SAFE_NAME__", escaped_name)\
               .replace("__SAFE_DESC__", escaped_desc)\
               .replace("__PRICE__", str(prod['final_price']))\
               .replace("__IMAGE__", prod['image'])\
               .replace("__SLUG__", prod['slug'])

# ==================== STATIC PAGES ====================

def generate_static_pages(categories_list):
    with open("output/about.html", "w", encoding="utf-8") as f:
        f.write(get_html_header("About Us", categories_list) + """
        <div class="container mx-auto px-4 py-16 max-w-4xl">
            <div class="text-center mb-12 reveal">
                <h1 class="text-4xl md:text-5xl font-extrabold text-[#E53935] dark:text-white mb-6">About ASM VEO</h1>
                <p class="text-lg text-gray-600 dark:text-gray-300 leading-relaxed">Your trusted shopping partner in Pakistan</p>
            </div>
            <div class="grid md:grid-cols-2 gap-8 mb-12">
                <div class="reveal bg-white dark:bg-gray-800 p-8 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-700">
                    <div class="w-14 h-14 bg-gray-100 rounded-2xl flex items-center justify-center mb-4"><i class="fas fa-bullseye text-2xl text-[#E53935]"></i></div>
                    <h3 class="text-xl font-bold mb-3 text-gray-900 dark:text-white">Our Mission</h3>
                    <p class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">To provide every Pakistani with access to premium quality products at affordable prices, delivered right to their doorstep with Cash on Delivery convenience.</p>
                </div>
                <div class="reveal bg-white dark:bg-gray-800 p-8 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-700">
                    <div class="w-14 h-14 bg-gray-100 rounded-2xl flex items-center justify-center mb-4"><i class="fas fa-eye text-2xl text-[#E53935]"></i></div>
                    <h3 class="text-xl font-bold mb-3 text-gray-900 dark:text-white">Our Vision</h3>
                    <p class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">To become Pakistan's most trusted and loved e-commerce platform, known for quality, reliability, and exceptional customer service.</p>
                </div>
            </div>
            <div class="reveal animated-bg text-white rounded-3xl p-8 md:p-12">
                <h2 class="text-3xl font-bold mb-4">Why Choose ASM VEO?</h2>
                <div class="grid md:grid-cols-3 gap-6 mt-8">
                    <div><i class="fas fa-shield-alt text-4xl mb-3 text-white"></i><h4 class="font-bold text-lg mb-2">100% Secure</h4><p class="text-gray-200 text-sm">SSL encrypted checkout with COD option</p></div>
                    <div><i class="fas fa-truck-fast text-4xl mb-3 text-white"></i><h4 class="font-bold text-lg mb-2">Fast Delivery</h4><p class="text-gray-200 text-sm">Nationwide delivery in 2-4 business days</p></div>
                    <div><i class="fas fa-undo text-4xl mb-3 text-white"></i><h4 class="font-bold text-lg mb-2">Easy Returns</h4><p class="text-gray-200 text-sm">7-day return policy, no questions asked</p></div>
                </div>
            </div>
        </div>
        """ + get_html_footer())

    with open("output/contact.html", "w", encoding="utf-8") as f:
        f.write(get_html_header("Contact Us", categories_list) + """
        <div class="container mx-auto px-4 py-16 max-w-4xl">
            <h1 class="text-4xl font-extrabold text-[#E53935] dark:text-white mb-8 text-center reveal">Contact Us</h1>
            <div class="grid md:grid-cols-2 gap-8">
                <div class="reveal bg-white dark:bg-gray-800 rounded-3xl shadow-xl p-8 border border-gray-100 dark:border-gray-700">
                    <i class="fab fa-whatsapp text-6xl text-green-500 mb-4"></i>
                    <h2 class="text-2xl font-bold mb-2 text-gray-900 dark:text-white">WhatsApp Support</h2>
                    <p class="text-gray-600 dark:text-gray-300 mb-6">Quick and instant support for all your queries. Message us anytime!</p>
                    <a href="https://wa.me/923425478683" class="inline-block bg-green-500 text-white font-black py-4 px-8 rounded-xl hover:bg-green-600 transition shadow-lg w-full text-center"><i class="fab fa-whatsapp mr-2"></i> 0342 54 786 83</a>
                </div>
                <div class="reveal bg-white dark:bg-gray-800 rounded-3xl shadow-xl p-8 border border-gray-100 dark:border-gray-700">
                    <i class="fas fa-headset text-6xl text-[#E53935] mb-4"></i>
                    <h2 class="text-2xl font-bold mb-2 text-gray-900 dark:text-white">Business Hours</h2>
                    <ul class="text-gray-600 dark:text-gray-300 space-y-2">
                        <li class="flex justify-between"><span>Monday - Friday</span><span class="font-bold">9AM - 11PM</span></li>
                        <li class="flex justify-between"><span>Saturday</span><span class="font-bold">10AM - 11PM</span></li>
                        <li class="flex justify-between"><span>Sunday</span><span class="font-bold">12PM - 10PM</span></li>
                    </ul>
                    <div class="mt-6 pt-6 border-t border-gray-100 dark:border-gray-700">
                        <p class="text-sm text-gray-500"><i class="fas fa-building mr-2 text-[#E53935]"></i> ASM Digital Solutions</p>
                        <p class="text-sm text-gray-500 mt-1"><i class="fas fa-user-tie mr-2 text-[#E53935]"></i> CEO: Ali Abbas</p>
                    </div>
                </div>
            </div>
        </div>
        """ + get_html_footer())

    faqs = [
        ("How long does delivery take in Pakistan?", "We deliver nationwide within 2-4 business days. Major cities like Karachi, Lahore, and Islamabad usually receive orders within 2 days. Remote areas may take up to 5 days."),
        ("Do you offer Cash on Delivery (COD)?", "Yes! We offer Cash on Delivery across all of Pakistan. You pay when you receive your product at your doorstep."),
        ("What is your return policy?", "We offer a 7-day return policy. If you're not satisfied with your product, you can return it within 7 days for a full refund or exchange. The product must be in its original condition."),
        ("Are your products genuine?", "Absolutely! We source all our products directly from authorized distributors and manufacturers. Every product is 100% genuine and quality-checked before dispatch."),
        ("How can I track my order?", "Once your order is shipped, you'll receive a tracking number via WhatsApp/SMS. You can also contact us anytime on WhatsApp for order updates."),
        ("What payment methods do you accept?", "Currently, we accept Cash on Delivery (COD) only. This is the safest and most convenient payment method for our customers across Pakistan."),
        ("Do you ship outside Pakistan?", "Currently, we only ship within Pakistan. We're working on expanding our services internationally soon!"),
        ("Can I modify or cancel my order?", "Yes, you can modify or cancel your order within 12 hours of placing it. Contact us on WhatsApp immediately with your order details.")
    ]
    
    faq_html = get_html_header("Frequently Asked Questions", categories_list)
    faq_html += """
    <div class="container mx-auto px-4 py-16 max-w-3xl">
        <h1 class="text-4xl font-extrabold text-[#E53935] dark:text-white mb-8 text-center reveal">Frequently Asked Questions</h1>
        <div class="space-y-4">
    """
    for q, a in faqs:
        faq_html += f"""
            <details class="reveal bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 group">
                <summary class="p-5 cursor-pointer font-bold text-gray-900 dark:text-white flex justify-between items-center list-none">
                    {q}
                    <i class="fas fa-chevron-down text-[#E53935] transition-transform group-open:rotate-180"></i>
                </summary>
                <div class="px-5 pb-5 text-gray-600 dark:text-gray-300 text-sm leading-relaxed">{a}</div>
            </details>
        """
    faq_html += "</div></div>"
    
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": []}
    for q, a in faqs:
        faq_schema["mainEntity"].append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    faq_html += f'<script type="application/ld+json">{json.dumps(faq_schema)}</script>'
    faq_html += get_html_footer()
    
    with open("output/faq.html", "w", encoding="utf-8") as f:
        f.write(faq_html)

    with open("output/privacy.html", "w", encoding="utf-8") as f:
        f.write(get_html_header("Privacy Policy", categories_list) + """
        <div class="container mx-auto px-4 py-16 max-w-4xl prose dark:prose-invert">
            <h1 class="text-4xl font-extrabold mb-8 text-[#E53935] dark:text-white">Privacy Policy</h1>
            <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-xl p-8 md:p-12 border border-gray-100 dark:border-gray-700 space-y-6 text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
                <p>At ASM VEO, we take your privacy seriously. This Privacy Policy explains how we collect, use, and protect your personal information.</p>
                <h2 class="text-xl font-bold text-gray-900 dark:text-white">Information We Collect</h2>
                <p>We collect your name, phone number, email, and shipping address when you place an order. This information is used solely for processing and delivering your orders.</p>
                <h2 class="text-xl font-bold text-gray-900 dark:text-white">How We Use Your Information</h2>
                <ul class="list-disc pl-6 space-y-2">
                    <li>To process and deliver your orders</li>
                    <li>To provide customer support</li>
                    <li>To send order updates and tracking information</li>
                    <li>To improve our products and services</li>
                </ul>
                <h2 class="text-xl font-bold text-gray-900 dark:text-white">Data Security</h2>
                <p>We use SSL encryption to protect your data. We never share your personal information with third parties except for shipping and delivery purposes.</p>
                <h2 class="text-xl font-bold text-gray-900 dark:text-white">Cookies</h2>
                <p>We use cookies to improve your browsing experience and remember your cart items. You can disable cookies in your browser settings.</p>
                <p class="text-gray-400 text-xs">Last updated: 2026</p>
            </div>
        </div>
        """ + get_html_footer())

    with open("output/terms.html", "w", encoding="utf-8") as f:
        f.write(get_html_header("Terms & Conditions", categories_list) + """
        <div class="container mx-auto px-4 py-16 max-w-4xl">
            <h1 class="text-4xl font-extrabold mb-8 text-[#E53935] dark:text-white">Terms & Conditions</h1>
            <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-xl p-8 md:p-12 border border-gray-100 dark:border-gray-700 space-y-6 text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
                <h2 class="text-xl font-bold text-gray-900 dark:text-white">1. Orders & Payments</h2>
                <p>All orders are subject to availability. We accept Cash on Delivery (COD) only. Prices are subject to change without notice.</p>
                <h2 class="text-xl font-bold text-gray-900 dark:text-white">2. Delivery</h2>
                <p>We deliver nationwide within 2-4 business days. Delivery charges are Rs 250 per order. Free delivery on orders above Rs 5000.</p>
                <h2 class="text-xl font-bold text-gray-900 dark:text-white">3. Returns & Refunds</h2>
                <p>7-day return policy applies. Products must be unused and in original packaging. Refunds are processed within 5-7 business days.</p>
                <h2 class="text-xl font-bold text-gray-900 dark:text-white">4. Product Quality</h2>
                <p>We guarantee 100% genuine products. All items are quality-checked before dispatch.</p>
                <p class="text-gray-400 text-xs">Last updated: 2026</p>
            </div>
        </div>
        """ + get_html_footer())

    with open("output/404.html", "w", encoding="utf-8") as f:
        f.write(get_html_header("Page Not Found", categories_list) + """
        <div class="container mx-auto px-4 py-20 text-center">
            <div class="max-w-lg mx-auto">
                <div class="text-9xl font-black text-[#E53935] mb-4">404</div>
                <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">Oops! Page Not Found</h1>
                <p class="text-gray-500 dark:text-gray-400 mb-8">The page you're looking for doesn't exist or has been moved. Let's get you back on track!</p>
                <div class="flex gap-4 justify-center flex-wrap">
                    <a href="/index.html" class="bg-[#E53935] text-white px-8 py-3 rounded-xl font-bold hover:bg-[#C62828] transition shadow-lg"><i class="fas fa-home mr-2"></i> Go Home</a>
                    <a href="/contact.html" class="bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white px8 py-3 rounded-xl font-bold hover:bg-gray-200 dark:hover:bg-gray-700 transition"><i class="fas fa-headset mr-2"></i> Contact Us</a>
                </div>
            </div>
        </div>
        """ + get_html_footer())

    with open("output/wishlist.html", "w", encoding="utf-8") as f:
        f.write(get_html_header("My Wishlist", categories_list) + """
        <div class="container mx-auto px-4 py-12">
            <h1 class="text-3xl font-extrabold text-[#E53935] dark:text-white mb-8 flex items-center gap-3"><i class="fas fa-heart text-[#E53935]"></i> My Wishlist</h1>
            <div id="wishlistContainer" class="grid grid-cols-3 md:grid-cols-6 gap-3 md:gap-4">
                <div class="col-span-full text-center py-16 text-gray-500 dark:text-gray-400">
                    <i class="fas fa-heart-broken text-6xl mb-4 opacity-30"></i>
                    <p class="text-lg font-bold">Your wishlist is empty</p>
                    <p class="text-sm mt-2">Start adding products you love!</p>
                    <a href="/index.html" class="inline-block mt-6 bg-[#E53935] text-white px-8 py-3 rounded-xl font-bold hover:bg-[#C62828] transition">Browse Products</a>
                </div>
            </div>
        </div>
        <script>
            function renderWishlist() {
                let wl = JSON.parse(localStorage.getItem('asm_wishlist')) || [];
                let container = document.getElementById('wishlistContainer');
                if (wl.length === 0) return;
                container.innerHTML = '';
                wl.forEach((item, i) => {
                    let safeName = item.name.split("'").join("\\'"); 
                    container.innerHTML += `
                        <div class="product-card bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col">
                            <div class="h-32 bg-gray-50 dark:bg-gray-700 overflow-hidden">
                                <img src="${item.image}" alt="${item.name}" class="w-full h-full object-contain p-1" onerror="this.src='https://via.placeholder.com/200x200/E53935/ffffff?text=ASM+VEO'">
                            </div>
                            <div class="p-2 flex flex-col flex-grow">
                                <h3 class="text-[10px] font-bold text-gray-900 dark:text-white line-clamp-2 mb-1">${item.name}</h3>
                                <p class="text-xs font-black text-[#E53935] dark:text-white mb-2">Rs ${item.price}</p>
                                <div class="flex gap-1 mt-auto">
                                    <button onclick="addToCart('${safeName}', ${item.price}, '${item.image}')" class="flex-1 bg-[#E53935] text-white py-1.5 rounded-md text-[10px] font-bold hover:bg-[#C62828] transition"><i class="fas fa-cart-plus"></i></button>
                                    <button onclick="removeWishlistItem(${i})" class="flex-1 bg-red-50 text-red-600 py-1.5 rounded-md text-[10px] font-bold hover:bg-red-100 transition"><i class="fas fa-trash"></i></button>
                                </div>
                            </div>
                        </div>`;
                });
            }
            function removeWishlistItem(i) {
                let wl = JSON.parse(localStorage.getItem('asm_wishlist')) || [];
                wl.splice(i, 1);
                localStorage.setItem('asm_wishlist', JSON.stringify(wl));
                updateWishlistBadge();
                renderWishlist();
                showToast('Removed from wishlist', 'fa-heart-broken', 'gray');
            }
            window.addEventListener('load', renderWishlist);
        </script>
        """ + get_html_footer())

    with open("output/order-success.html", "w", encoding="utf-8") as f:
        f.write(get_html_header("Order Confirmed!", categories_list) + """
        <div class="container mx-auto px-4 py-20 text-center">
            <div class="max-w-lg mx-auto">
                <div class="w-24 h-24 mx-auto bg-green-100 rounded-full flex items-center justify-center mb-6 animate-bounce">
                    <i class="fas fa-check text-5xl text-green-600"></i>
                </div>
                <h1 class="text-3xl font-extrabold text-gray-900 dark:text-white mb-4">Order Confirmed!</h1>
                <p class="text-gray-600 dark:text-gray-300 mb-2">Thank you for your purchase. Your order has been placed successfully.</p>
                <p class="text-gray-500 dark:text-gray-400 text-sm mb-8">Order ID: <span id="orderId" class="font-bold text-[#E53935]">ASM-XXXXXX</span></p>
                <div class="bg-gray-50 dark:bg-gray-800 rounded-2xl p-6 mb-8 text-left">
                    <h3 class="font-bold text-gray-900 dark:text-white mb-3">What's Next?</h3>
                    <ol class="space-y-3 text-sm text-gray-600 dark:text-gray-300">
                        <li class="flex gap-3"><span class="w-6 h-6 bg-[#E53935] text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">1</span> We'll confirm your order via WhatsApp shortly</li>
                        <li class="flex gap-3"><span class="w-6 h-6 bg-[#E53935] text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">2</span> Your order will be dispatched within 24 hours</li>
                        <li class="flex gap-3"><span class="w-6 h-6 bg-[#E53935] text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">3</span> Expected delivery: 2-4 business days</li>
                        <li class="flex gap-3"><span class="w-6 h-6 bg-[#E53935] text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">4</span> Pay cash when you receive your order</li>
                    </ol>
                </div>
                <div class="flex gap-4 justify-center flex-wrap">
                    <a href="/index.html" class="bg-[#E53935] text-white px-8 py-3 rounded-xl font-bold hover:bg-[#C62828] transition shadow-lg"><i class="fas fa-shopping-bag mr-2"></i> Continue Shopping</a>
                    <a href="https://wa.me/923425478683" class="bg-green-500 text-white px-8 py-3 rounded-xl font-bold hover:bg-green-600 transition shadow-lg"><i class="fab fa-whatsapp mr-2"></i> Track on WhatsApp</a>
                </div>
            </div>
        </div>
        <script>
            document.getElementById('orderId').innerText = 'ASM-' + Math.floor(100000 + Math.random() * 900000);
            localStorage.removeItem('asm_cart');
            updateCartBadge();
        </script>
        """ + get_html_footer())

# ==================== PAGINATION HTML GENERATOR ====================
def generate_pagination_html(current_page, total_pages, base_url):
    if total_pages <= 1: return ""
    
    html = '<div class="flex justify-center items-center gap-1 md:gap-2 mt-12">'
    
    # Prev Button
    if current_page > 1:
        prev_slug = base_url if current_page - 1 == 1 else f"{base_url}-{current_page - 1}"
        html += f'<a href="/category/{prev_slug}.html" class="bg-white border border-gray-200 text-[#E53935] px-3 py-2 rounded-lg font-bold hover:bg-gray-50 transition text-sm">&lt;</a>'
    else:
        html += '<span class="bg-gray-100 border border-gray-200 text-gray-400 px-3 py-2 rounded-lg font-bold text-sm cursor-not-allowed">&lt;</span>'
    
    # Page Numbers Logic
    pages_to_show = []
    if total_pages <= 7:
        pages_to_show = list(range(1, total_pages + 1))
    else:
        if current_page <= 4:
            pages_to_show = [1, 2, 3, 4, '...', total_pages]
        elif current_page >= total_pages - 3:
            pages_to_show = [1, '...', total_pages-3, total_pages-2, total_pages-1, total_pages]
        else:
            pages_to_show = [1, '...', current_page-1, current_page, current_page+1, '...', total_pages]
            
    for p_num in pages_to_show:
        if p_num == '...':
            html += '<span class="px-2 py-2 text-gray-500 text-sm">...</span>'
        elif p_num == current_page:
            html += f'<span class="bg-[#E53935] text-white px-4 py-2 rounded-lg font-bold text-sm">{p_num}</span>'
        else:
            p_slug = base_url if p_num == 1 else f"{base_url}-{p_num}"
            html += f'<a href="/category/{p_slug}.html" class="bg-white border border-gray-200 text-[#E53935] px-4 py-2 rounded-lg font-bold hover:bg-gray-50 transition text-sm">{p_num}</a>'
            
    # Next Button
    if current_page < total_pages:
        next_slug = f"{base_url}-{current_page + 1}"
        html += f'<a href="/category/{next_slug}.html" class="bg-white border border-gray-200 text-[#E53935] px-3 py-2 rounded-lg font-bold hover:bg-gray-50 transition text-sm">&gt;</a>'
    else:
        html += '<span class="bg-gray-100 border border-gray-200 text-gray-400 px-3 py-2 rounded-lg font-bold text-sm cursor-not-allowed">&gt;</span>'
        
    html += '</div>'
    return html

# ==================== MAIN PROCESSOR ====================

def process_woocommerce_csv():
    file_path = "woocommerce-products-export.csv"
    if not os.path.exists(file_path):
        print("❌ CSV File Not Found!")
        return
        
    print("🚀 Advanced Script Started! Cleaning old data...")
    
    if os.path.exists("output"):
        shutil.rmtree("output")
    os.makedirs("output/category", exist_ok=True)
    os.makedirs("output/product", exist_ok=True)
    os.makedirs("output/assets", exist_ok=True)
    
    with open("output/CNAME", "w") as f:
        f.write("www.asmveo.com")
    
    products_list = []
    categories_set = set()
    sitemap_urls = ["https://www.asmveo.com/", "https://www.asmveo.com/checkout.html", 
                    "https://www.asmveo.com/about.html", "https://www.asmveo.com/contact.html",
                    "https://www.asmveo.com/faq.html", "https://www.asmveo.com/wishlist.html",
                    "https://www.asmveo.com/privacy.html", "https://www.asmveo.com/terms.html",
                    "https://www.asmveo.com/order-success.html"]
    
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            images_raw = row.get('Images', '').strip()
            if not name or not images_raw: continue 
                
            images = [img.strip() for img in images_raw.split(',') if img.strip()]
            image = images[0]
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
            slug = make_slug(name) + f"-{product_id}"
            sitemap_urls.append(f"https://www.asmveo.com/product/{slug}.html")
            
            products_list.append({
                'id': product_id, 'slug': slug, 'name': name, 'category': category,
                'fake_price': fake_regular_price, 'final_price': final_price,
                'image': image, 'images': images, 'seo_desc': seo_desc, 
                'full_desc': clean_description
            })

    categories_list = sorted(list(categories_set))
    print(f"✔ Total {len(products_list)} products being processed...")
    
    generate_static_pages(categories_list)
    generate_robots_txt()
    generate_manifest()
    
    # ================= PRODUCT PAGES =================
    for i, prod in enumerate(products_list):
        reviews_section, avg_rating, review_count = generate_reviews(prod['name'])
        prod['rating'] = avg_rating
        prod['review_count'] = review_count
        
        related = [p for p in products_list if p['category'] == prod['category'] and p['slug'] != prod['slug']][:4]
        related_html = "".join([generate_product_card(p, lazy=True) for p in related])
        
        gallery_html = ""
        if len(prod['images']) > 1:
            gallery_thumbs = ""
            for idx, img in enumerate(prod['images'][:5]):
                gallery_thumbs += f'<img src="{img}" alt="Thumbnail {idx+1}" onclick="changeMainImage(this)" class="w-16 h-16 object-cover rounded-lg cursor-pointer border-2 {"border-[#E53935]" if idx == 0 else "border-gray-200"} hover:border-[#E53935] transition" onerror="this.style.display=\'none\'">'
            gallery_html = f'<div class="flex gap-2 mt-4 overflow-x-auto">{gallery_thumbs}</div>'
        
        breadcrumb_data = {'category': prod['category'], 'name': prod['name'], 'slug': prod['slug']}
        product_schema_data = {**prod, 'rating': avg_rating, 'review_count': review_count}
        
        prod_html = get_html_header(prod['name'], categories_list, prod['seo_desc'], 
                                     product_data=product_schema_data, breadcrumb_data=breadcrumb_data,
                                     og_image=prod['image'])
        
        # Bug 7 Fix: Safe discount calculation
        discount_pct = math.ceil(((prod['fake_price'] - prod['final_price']) / prod['fake_price']) * 100) if prod['fake_price'] > 0 and prod['fake_price'] > prod['final_price'] else 0
        stock_left = random.randint(3, 15)
        stock_pct = random.randint(15, 40)
        delivery_date = (datetime.now() + timedelta(days=random.randint(2, 4))).strftime("%b %d, %Y")
        escaped_name = prod['name'].replace("\\", "\\\\").replace("'", "\\'")
        alt_name = prod['name'].replace('"', '&quot;') # Bug 3 Fix
        
        wa_text = f"Hi, I want to order {prod['name']} (Rs {prod['final_price']}). Is it available?"
        wa_link = f"https://wa.me/923425478683?text={urllib.parse.quote(wa_text)}"
        
        # Next Product Button Logic
        next_prod_html = ""
        if i + 1 < len(products_list):
            next_prod = products_list[i+1]
            next_prod_html = f"""
            <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-lg border border-gray-200 dark:border-gray-700 p-8 mb-16 md:mb-0 reveal">
                <h2 class="text-xl font-extrabold text-gray-900 dark:text-white mb-4 border-b pb-4">Ready for the next product?</h2>
                <div class="flex items-center gap-4">
                    <img src="{next_prod['image']}" alt="{next_prod['name']}" class="w-20 h-20 object-contain rounded-lg border border-gray-100">
                    <div class="flex-grow">
                        <h3 class="font-bold text-sm text-gray-900 dark:text-white line-clamp-2">{next_prod['name']}</h3>
                        <p class="text-lg font-black text-[#E53935] dark:text-white mt-1">Rs {next_prod['final_price']}</p>
                    </div>
                    <a href="/product/{next_prod['slug']}.html" class="bg-[#E53935] text-white py-3 px-6 rounded-xl font-bold hover:bg-[#C62828] transition flex items-center gap-2 whitespace-nowrap">
                        Next <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
            </div>
            """
        
        prod_html += f"""
        <div class="container mx-auto px-4 py-10">
            <nav class="text-sm text-gray-600 dark:text-gray-400 mb-6 font-semibold bg-gray-100 dark:bg-gray-800 p-3 rounded-lg inline-block" aria-label="Breadcrumb">
                <a href="/index.html" class="hover:text-[#E53935] transition">Home</a> &gt; 
                <a href="/category/{re.sub(r'[^a-z0-9]+', '-', prod['category'].lower()).strip('-')}.html" class="hover:text-[#E53935] transition">{prod['category']}</a> &gt; 
                <span class="text-[#E53935] dark:text-white" aria-current="page">{prod['name']}</span>
            </nav>
            
            <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col md:flex-row mb-12 reveal">
                <div class="md:w-1/2 p-6 flex flex-col justify-center items-center bg-gray-50 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 relative">
                    {f'<div class="absolute top-4 left-4 bg-[#E53935] text-white text-sm font-black px-3 py-1.5 rounded-lg z-10 shadow-md">-{discount_pct}% OFF</div>' if discount_pct > 0 else ''}
                    <img id="mainProductImage" src="{prod['image']}" alt="{alt_name}" fetchpriority="high" width="600" height="600" class="max-h-[500px] object-contain rounded-xl hover:scale-105 transition duration-500" onerror="this.src='https://via.placeholder.com/600x600/E53935/ffffff?text=ASM+VEO'">
                    {gallery_html}
                </div>
                <div class="md:w-1/2 p-8 md:p-12 flex flex-col justify-center">
                    <span class="text-xs font-bold uppercase tracking-widest text-[#E53935] dark:text-white mb-2">{prod['category']}</span>
                    <h1 class="text-3xl md:text-4xl font-extrabold text-gray-900 dark:text-white mb-4">{prod['name']}</h1>
                    
                    <div class="flex items-center gap-3 mb-6" aria-label="Customer Rating">
                        <div class="text-yellow-500 text-sm">{"<i class='fas fa-star'></i>" * 5}</div>
                        <span class="text-sm font-semibold text-gray-600 dark:text-gray-300">{avg_rating} ({review_count} verified reviews)</span>
                    </div>

                    <div class="flex items-center gap-4 mb-4 bg-gray-50 dark:bg-gray-700 p-4 rounded-2xl w-fit border border-gray-100 dark:border-gray-600">
                        <span class="text-4xl font-black text-[#E53935] dark:text-white">Rs {prod['final_price']}</span>
                        <span class="text-xl text-gray-500 font-bold line-through">Rs {prod['fake_price']}</span>
                        {f'<span class="bg-red-500 text-white text-sm font-bold px-2 py-1 rounded-lg">Save Rs {prod["fake_price"] - prod["final_price"]}</span>' if discount_pct > 0 else ''}
                    </div>
                    
                    <!-- Live Stock & Viewers Counter -->
                    <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-2xl mb-6 border border-gray-100 dark:border-gray-600">
                        <div class="flex justify-between text-xs font-bold text-gray-600 dark:text-gray-300 mb-2">
                            <span><i class="fas fa-eye"></i> <span id="liveViewers">15</span> people are viewing this right now</span>
                            <span><i class="fas fa-fire text-orange-500"></i> Hurry, only {stock_left} left!</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-600">
                            <div class="bg-orange-500 h-2.5 rounded-full" style="width: {stock_pct}%"></div>
                        </div>
                    </div>
                    
                    <div class="flex items-center gap-2 mb-6 text-sm">
                        <span class="bg-green-100 text-green-700 px-3 py-1 rounded-full font-bold"><i class="fas fa-truck"></i> Delivery by {delivery_date}</span>
                    </div>
                    
                    <p class="text-gray-700 dark:text-gray-300 mb-8 leading-relaxed border-t border-gray-100 dark:border-gray-700 pt-6">{prod['full_desc'][:500] if len(prod['full_desc']) > 50 else prod['seo_desc']}</p>
                    
                    <div class="flex flex-col sm:flex-row gap-4 w-full md:w-5/6 mt-auto main-product-actions">
                        <button onclick="addToCart('__SAFE_NAME__', {prod['final_price']}, '__IMAGE__', event)" aria-label="Add to Cart" class="sm:w-1/2 bg-white dark:bg-gray-700 text-[#E53935] dark:text-white py-4 rounded-xl font-black text-lg border-2 border-[#E53935] hover:bg-gray-50 dark:hover:bg-gray-600 transition-all shadow-md transform hover:-translate-y-1 flex justify-center items-center gap-2">
                            <i class="fas fa-cart-plus"></i> Add to Cart
                        </button>
                        <button onclick="buyNow('__SAFE_NAME__', {prod['final_price']}, '__IMAGE__', event)" aria-label="Buy Now" class="sm:w-1/2 bg-[#E53935] text-white py-4 rounded-xl font-black text-lg hover:bg-[#C62828] transition-all shadow-lg transform hover:-translate-y-1 flex justify-center items-center gap-2">
                            <i class="fas fa-bolt"></i> Buy Now
                        </button>
                    </div>
                    
                    <a href="{wa_link}" target="_blank" class="mt-4 w-full md:w-5/6 bg-green-500 text-white font-bold py-3 rounded-xl hover:bg-green-600 transition flex items-center justify-center gap-2">
                        <i class="fab fa-whatsapp text-xl"></i> Quick Order via WhatsApp
                    </a>
                    
                    <div class="grid grid-cols-3 gap-3 mt-8 pt-6 border-t border-gray-100 dark:border-gray-700">
                        <div class="text-center"><i class="fas fa-shield-alt text-[#E53935] text-xl mb-1"></i><p class="text-xs font-semibold text-gray-600 dark:text-gray-400">Secure Payment</p></div>
                        <div class="text-center"><i class="fas fa-undo text-[#E53935] text-xl mb-1"></i><p class="text-xs font-semibold text-gray-600 dark:text-gray-400">7-Day Returns</p></div>
                        <div class="text-center"><i class="fas fa-truck text-[#E53935] text-xl mb-1"></i><p class="text-xs font-semibold text-gray-600 dark:text-gray-400">Fast Delivery</p></div>
                    </div>
                </div>
            </div>
            
            {"<div class='bg-white dark:bg-gray-800 rounded-3xl shadow-lg border border-gray-200 dark:border-gray-700 p-8 mb-8 reveal'><h2 class='text-2xl font-extrabold text-gray-900 dark:text-white mb-6 border-b pb-4'>You May Also Like</h2><div class='grid grid-cols-3 md:grid-cols-6 gap-3 md:gap-4'>" + related_html + "</div></div>" if related_html else ""}
            
            <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-lg border border-gray-200 dark:border-gray-700 p-8 mb-8 reveal">
                <h2 class="text-2xl font-extrabold text-gray-900 dark:text-white mb-6 border-b pb-4 flex items-center gap-3">
                    <i class="fas fa-star text-yellow-500"></i> Customer Reviews ({review_count})
                </h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div>{reviews_section}</div>
                    <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-2xl h-fit border border-gray-300 dark:border-gray-700">
                        <h3 class="font-bold text-lg mb-2 text-gray-900 dark:text-white">Write a Review</h3>
                        <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">Only verified buyers can leave a review after receiving the product to maintain quality standards.</p>
                        <div class="flex items-center gap-2 text-[#E53935] dark:text-white font-bold bg-gray-50 dark:bg-gray-700 p-3 rounded-lg border border-gray-200 dark:border-gray-600">
                            <i class="fas fa-lock"></i> Review form is currently locked.
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-lg border border-gray-200 dark:border-gray-700 p-8 mb-8 reveal">
                <h2 class="text-2xl font-extrabold text-gray-900 dark:text-white mb-6 border-b pb-4">Product FAQs</h2>
                <div class="space-y-4">
                    <details class="border border-gray-200 dark:border-gray-700 rounded-xl p-4 group">
                        <summary class="cursor-pointer font-bold text-gray-900 dark:text-white flex justify-between list-none">Is this product genuine? <i class="fas fa-chevron-down text-[#E53935] group-open:rotate-180 transition"></i></summary>
                        <p class="mt-3 text-sm text-gray-600 dark:text-gray-300">Yes! We source 100% genuine products directly from authorized distributors. Every product is quality-checked before dispatch.</p>
                    </details>
                    <details class="border border-gray-200 dark:border-gray-700 rounded-xl p-4 group">
                        <summary class="cursor-pointer font-bold text-gray-900 dark:text-white flex justify-between list-none">What is the delivery time? <i class="fas fa-chevron-down text-[#E53935] group-open:rotate-180 transition"></i></summary>
                        <p class="mt-3 text-sm text-gray-600 dark:text-gray-300">Delivery takes 2-4 business days across Pakistan. Major cities receive faster delivery.</p>
                    </details>
                    <details class="border border-gray-200 dark:border-gray-700 rounded-xl p-4 group">
                        <summary class="cursor-pointer font-bold text-gray-900 dark:text-white flex justify-between list-none">Can I return this product? <i class="fas fa-chevron-down text-[#E53935] group-open:rotate-180 transition"></i></summary>
                        <p class="mt-3 text-sm text-gray-600 dark:text-gray-300">Yes, we offer a 7-day return policy. The product must be in its original condition with packaging.</p>
                    </details>
                </div>
            </div>
            
            {next_prod_html}
        </div>
        
        <!-- Sticky Add to Cart Bar for Mobile -->
        <div id="stickyAddToCart" class="hidden fixed bottom-16 left-0 right-0 bg-white dark:bg-gray-800 shadow-2xl border-t border-gray-200 dark:border-gray-700 p-3 z-40 flex items-center justify-between gap-3 md:hidden">
            <div class="flex flex-col">
                <span class="text-xs text-gray-500 dark:text-gray-400 line-clamp-1">{prod['name']}</span>
                <span class="text-lg font-black text-[#E53935] dark:text-white">Rs {prod['final_price']}</span>
            </div>
            <button onclick="addToCart('__SAFE_NAME__', {prod['final_price']}, '__IMAGE__', event)" class="bg-[#E53935] text-white px-4 py-2.5 rounded-lg font-bold text-sm flex items-center gap-2">
                <i class="fas fa-cart-plus"></i> Add to Cart
            </button>
        </div>
        """
        prod_html = prod_html.replace("__SAFE_NAME__", escaped_name).replace("__IMAGE__", prod['image'])
        
        recent_json = json.dumps({"slug": prod['slug'], "name": prod['name'], "image": prod['image'], "final_price": prod['final_price'], "fake_price": prod['fake_price'], "category": prod['category']})
        prod_script = """
        <script>
            addToRecentlyViewed(__RECENT_JSON__);
            function changeMainImage(thumb) {
                document.getElementById('mainProductImage').src = thumb.src;
                document.querySelectorAll('.flex.gap-2 img').forEach(img => img.classList.remove('border-[#E53935]'));
                thumb.classList.add('border-[#E53935]');
            }
            
            // Sticky Add to Cart Bar Logic
            let stickyBar = document.getElementById('stickyAddToCart');
            let mainActions = document.querySelector('.main-product-actions');
            window.addEventListener('scroll', () => {
                if (mainActions) {
                    let rect = mainActions.getBoundingClientRect();
                    if (rect.bottom < 0) {
                        stickyBar.classList.remove('hidden');
                    } else {
                        stickyBar.classList.add('hidden');
                    }
                }
            });

            // Live Viewers Counter Logic
            let viewers = document.getElementById('liveViewers');
            setInterval(() => {
                let current = parseInt(viewers.innerText);
                let change = Math.floor(Math.random() * 5) - 2;
                current += change;
                if (current < 10) current = 10;
                if (current > 35) current = 35;
                viewers.innerText = current;
            }, 3000);
        </script>
        """
        prod_html += prod_script.replace("__RECENT_JSON__", recent_json) + get_html_footer()
        
        with open(f"output/product/{prod['slug']}.html", "w", encoding="utf-8") as f:
            f.write(prod_html)

    # ================= CITY SEO PAGES =================
    print("🏙️ Generating City SEO Pages...")
    cities = ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Multan", "Peshawar", "Quetta", "Faisalabad"]
    os.makedirs("output/city", exist_ok=True)
    
    for city in cities:
        city_slug = make_slug(city)
        sitemap_urls.append(f"https://www.asmveo.com/city/{city_slug}.html")
        
        city_prods = random.sample(products_list, min(10, len(products_list)))
        city_html = get_html_header(f"Online Shopping in {city}", categories_list, f"Buy products online in {city} with Cash on Delivery. Fast delivery in {city} and all over Pakistan. Premium quality at best prices.")
        
        city_html += f"""
        <div class="animated-bg py-16 mb-8 text-center text-white relative overflow-hidden">
            <div class="absolute top-10 right-10 w-32 h-32 bg-white/10 rounded-full animate-float"></div>
            <div class="absolute bottom-10 left-10 w-48 h-48 bg-white/5 rounded-full animate-float" style="animation-delay: 1s;"></div>
            <h1 class="text-4xl md:text-5xl font-extrabold mb-4 relative z-10">Online Shopping in {city}</h1>
            <p class="text-lg text-gray-200 relative z-10">Fast Delivery & Cash on Delivery Available in {city}</p>
        </div>
        <div class="container mx-auto px-4 pb-12">
            <p class="text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
                Shop premium quality products online in {city} with ASM VEO. We offer a wide range of items including electronics, fashion, accessories, and more. Enjoy the convenience of Cash on Delivery (COD) right at your doorstep in {city}. Our fast delivery network ensures you get your products within 2-4 business days. 100% genuine products with a 7-day return policy.
            </p>
            <h2 class="text-2xl font-bold text-[#E53935] dark:text-white mb-6">Top Products in {city}</h2>
            <div class="grid grid-cols-3 md:grid-cols-6 gap-3 md:gap-4">
        """
        for p in city_prods:
            city_html += generate_product_card(p)
            
        city_html += "</div></div>" + get_html_footer()
        with open(f"output/city/{city_slug}.html", "w", encoding="utf-8") as f:
            f.write(city_html)

    # ================= CATEGORY PAGES WITH PAGINATION =================
    sections_dict = {}
    for p in products_list:
        c = p['category']
        if c not in sections_dict: sections_dict[c] = []
        sections_dict[c].append(p)

    # Save search index to a separate JS file
    search_index_json = json.dumps([{"name": p['name'], "slug": p['slug'], "category": p['category'], 
                                     "final_price": p['final_price'], "fake_price": p['fake_price'], "image": p['image']} for p in products_list])
    with open("output/search-data.js", "w", encoding="utf-8") as f:
        f.write(f"let searchIndex = {search_index_json};")

    home_html = get_html_header("Home - Premium Online Shopping in Pakistan", categories_list,
                                 "ASM VEO - Pakistan's premium online shopping destination. Buy quality products with Cash on Delivery, fast shipping & easy returns.")
    
    # Hero Carousel
    home_html += """
    <div id="heroCarousel" class="relative w-full h-[250px] md:h-[400px] overflow-hidden shadow-xl">
        <div class="carousel-track h-full">
            <div class="carousel-slide h-full relative">
                <img src="https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=1200&q=80" alt="Fashion Sale" class="absolute inset-0 w-full h-full object-cover">
                <div class="absolute inset-0 bg-black/50"></div>
                <div class="relative z-10 h-full flex items-center p-6 md:p-16 text-white">
                    <div class="max-w-lg">
                        <span class="bg-[#E53935] text-white text-xs font-black px-3 py-1 rounded-full">FLASH SALE</span>
                        <h2 class="text-3xl md:text-5xl font-extrabold mt-3 mb-3 leading-tight">Premium Fashion<br>Collection 2026</h2>
                        <a href="#products" class="bg-white text-[#E53935] px-6 py-2.5 rounded-lg font-bold hover:bg-gray-100 transition text-sm">Shop Now</a>
                    </div>
                </div>
            </div>
            <div class="carousel-slide h-full relative">
                <img src="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=1200&q=80" alt="Gadgets" class="absolute inset-0 w-full h-full object-cover">
                <div class="absolute inset-0 bg-black/50"></div>
                <div class="relative z-10 h-full flex items-center p-6 md:p-16 text-white">
                    <div class="max-w-lg">
                        <span class="bg-[#E53935] text-white text-xs font-black px-3 py-1 rounded-full">NEW ARRIVALS</span>
                        <h2 class="text-3xl md:text-5xl font-extrabold mt-3 mb-3 leading-tight">Latest Gadgets<br>& Accessories</h2>
                        <a href="#products" class="bg-[#E53935] text-white px-6 py-2.5 rounded-lg font-bold hover:bg-[#C62828] transition text-sm">Explore Now</a>
                    </div>
                </div>
            </div>
            <div class="carousel-slide h-full relative">
                <img src="https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?auto=format&fit=crop&w=1200&q=80" alt="Mega Sale" class="absolute inset-0 w-full h-full object-cover">
                <div class="absolute inset-0 bg-black/50"></div>
                <div class="relative z-10 h-full flex items-center p-6 md:p-16 text-white">
                    <div class="max-w-lg">
                        <span class="bg-yellow-400 text-black text-xs font-black px-3 py-1 rounded-full">MEGA SALE</span>
                        <h2 class="text-3xl md:text-5xl font-extrabold mt-3 mb-3 leading-tight">Flat 50% OFF<br>Premium Products</h2>
                        <a href="#products" class="bg-white text-[#E53935] px-6 py-2.5 rounded-lg font-bold hover:bg-gray-100 transition text-sm">Shop Now</a>
                    </div>
                </div>
            </div>
            <div class="carousel-slide h-full relative">
                <img src="https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&w=1200&q=80" alt="Shoes" class="absolute inset-0 w-full h-full object-cover">
                <div class="absolute inset-0 bg-black/50"></div>
                <div class="relative z-10 h-full flex items-center p-6 md:p-16 text-white">
                    <div class="max-w-lg">
                        <span class="bg-white text-gray-900 text-xs font-black px-3 py-1 rounded-full">SHOE FESTIVAL</span>
                        <h2 class="text-3xl md:text-5xl font-extrabold mt-3 mb-3 leading-tight">Premium Shoes<br>Unbeatable Prices</h2>
                        <a href="#products" class="bg-white text-gray-900 px-6 py-2.5 rounded-lg font-bold hover:bg-gray-100 transition text-sm">Explore Now</a>
                    </div>
                </div>
            </div>
            <div class="carousel-slide h-full relative">
                <img src="https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?auto=format&fit=crop&w=1200&q=80" alt="14 August" class="absolute inset-0 w-full h-full object-cover">
                <div class="absolute inset-0 bg-[#E53935]/70"></div>
                <div class="relative z-10 h-full flex items-center p-6 md:p-16 text-white">
                    <div class="max-w-lg">
                        <span class="bg-white text-[#E53935] text-xs font-black px-3 py-1 rounded-full">14 AUGUST SALE</span>
                        <h2 class="text-3xl md:text-5xl font-extrabold mt-3 mb-3 leading-tight">Independence Day<br>Mega Sale!</h2>
                        <a href="#products" class="bg-white text-[#E53935] px-6 py-2.5 rounded-lg font-bold hover:bg-gray-100 transition text-sm">Shop Now</a>
                    </div>
                </div>
            </div>
        </div>
        <button onclick="prevSlide()" class="absolute left-2 top-1/2 -translate-y-1/2 bg-black/40 text-white w-10 h-10 rounded-full flex items-center justify-center hover:bg-black/60 transition z-20" aria-label="Previous slide"><i class="fas fa-chevron-left"></i></button>
        <button onclick="nextSlide()" class="absolute right-2 top-1/2 -translate-y-1/2 bg-black/40 text-white w-10 h-10 rounded-full flex items-center justify-center hover:bg-black/60 transition z-20" aria-label="Next slide"><i class="fas fa-chevron-right"></i></button>
        <div id="carouselDots" class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2 z-20"></div>
    </div>
    
    <script>
        let slideIndex = 0;
        const slides = document.querySelectorAll('.carousel-slide');
        const dotsContainer = document.getElementById('carouselDots');
        
        slides.forEach((_, i) => {
            dotsContainer.innerHTML += `<button onclick="goToSlide(${i})" class="w-3 h-3 rounded-full bg-white/50 hover:bg-white transition"></button>`;
        });
        
        function updateCarousel() {
            document.querySelector('.carousel-track').style.transform = `translateX(-${slideIndex * 100}%)`;
            document.querySelectorAll('#carouselDots button').forEach((dot, i) => {
                dot.className = `w-3 h-3 rounded-full transition ${i === slideIndex ? 'bg-white scale-125' : 'bg-white/50 hover:bg-white'}`;
            });
        }
        
        function nextSlide() { slideIndex = (slideIndex + 1) % slides.length; updateCarousel(); }
        function prevSlide() { slideIndex = (slideIndex - 1 + slides.length) % slides.length; updateCarousel(); }
        function goToSlide(i) { slideIndex = i; updateCarousel(); }
        
        updateCarousel();
        setInterval(nextSlide, 2000);
    </script>
    """

    # Flashmart Style Categories Circle Bar
    home_html += """
    <div class="bg-white dark:bg-gray-800 border-b border-gray-100 dark:border-gray-700 py-6">
        <div class="container mx-auto px-4">
            <div class="grid grid-cols-4 md:grid-cols-8 gap-4 text-center">
    """
    for cat in categories_list[:8]:
        c_slug = re.sub(r'[^a-z0-9]+', '-', cat.lower()).strip('-')
        home_html += f"""
            <a href="/category/{c_slug}.html" class="flex flex-col items-center gap-2 group">
                <div class="w-16 h-16 rounded-full bg-gray-50 dark:bg-gray-700 group-hover:bg-[#E53935] flex items-center justify-center transition-all group-hover:scale-105 shadow-sm border border-gray-100 dark:border-gray-600">
                    <i class="fas {get_category_icon(cat)} text-xl text-[#E53935] group-hover:text-white transition"></i>
                </div>
                <span class="text-[10px] md:text-xs font-bold text-gray-700 dark:text-gray-200 group-hover:text-[#E53935] transition line-clamp-1">{cat}</span>
            </a>
        """
    home_html += "</div></div></div>"

    home_html += """
    <div class="bg-[#E53935] text-white py-6 mt-6">
        <div class="container mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-3">
                <i class="fas fa-bolt text-yellow-400 text-3xl animate-pulse"></i>
                <div>
                    <h2 class="text-2xl font-extrabold">Flash Sale</h2>
                    <p class="text-gray-200 text-sm">Hurry up! Offer ends soon.</p>
                </div>
            </div>
            <div id="countdown" class="flex gap-3 text-center">
                <div class="bg-white/10 px-4 py-2 rounded-lg"><span id="hours" class="text-2xl font-black text-white">00</span><br><span class="text-xs text-gray-200">Hrs</span></div>
                <div class="bg-white/10 px-4 py-2 rounded-lg"><span id="minutes" class="text-2xl font-black text-white">00</span><br><span class="text-xs text-gray-200">Min</span></div>
                <div class="bg-white/10 px-4 py-2 rounded-lg"><span id="seconds" class="text-2xl font-black text-white">00</span><br><span class="text-xs text-gray-200">Sec</span></div>
            </div>
        </div>
    </div>
    <script>
        let countDownDate = new Date().getTime() + (12 * 60 * 60 * 1000);
        let x = setInterval(function() {
            let now = new Date().getTime();
            let distance = countDownDate - now;
            let h = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let m = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            let s = Math.floor((distance % (1000 * 60)) / 1000);
            
            document.getElementById("hours").innerHTML = h < 10 ? "0" + h : h;
            document.getElementById("minutes").innerHTML = m < 10 ? "0" + m : m;
            document.getElementById("seconds").innerHTML = s < 10 ? "0" + s : s;
            
            if (distance < 0) {
                clearInterval(x);
                countDownDate = new Date().getTime() + (12 * 60 * 60 * 1000);
            }
        }, 1000);
    </script>
    """

    home_html += """
    <div class="container mx-auto px-4 py-6">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="reveal bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-3">
                <div class="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg text-[#E53935] dark:text-white"><i class="fas fa-truck-fast text-xl"></i></div>
                <div><h3 class="font-bold text-sm text-gray-900 dark:text-white">Fast Delivery</h3><p class="text-xs text-gray-500 dark:text-gray-400">All over Pakistan</p></div>
            </div>
            <div class="reveal bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-3">
                <div class="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg text-[#E53935] dark:text-white"><i class="fas fa-money-bill-wave text-xl"></i></div>
                <div><h3 class="font-bold text-sm text-gray-900 dark:text-white">Cash on Delivery</h3><p class="text-xs text-gray-500 dark:text-gray-400">Pay at your doorstep</p></div>
            </div>
            <div class="reveal bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-3">
                <div class="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg text-[#E53935] dark:text-white"><i class="fas fa-shield-halved text-xl"></i></div>
                <div><h3 class="font-bold text-sm text-gray-900 dark:text-white">Secure Shopping</h3><p class="text-xs text-gray-500 dark:text-gray-400">100% Protected</p></div>
            </div>
            <div class="reveal bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-3">
                <div class="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg text-[#E53935] dark:text-white"><i class="fas fa-undo text-xl"></i></div>
                <div><h3 class="font-bold text-sm text-gray-900 dark:text-white">Easy Returns</h3><p class="text-xs text-gray-500 dark:text-gray-400">7 Days Return Policy</p></div>
            </div>
        </div>
    </div>
    """

    home_html += f"""
    <div class='container mx-auto px-4 py-4' id="products">
        <div id="searchResultsSection" class="hidden mb-6">
            <h2 id="searchResultsHeading" class="text-2xl font-extrabold text-[#E53935] dark:text-white mb-2 border-b pb-2"></h2>
            <p id="searchResultsCount" class="text-gray-500 text-sm"></p>
        </div>
        <div id="defaultContent">
    """
    
    # Show top 4 categories and 6 products each on home page
    total_rendered_products = 0
    for cat_name, prods in list(sections_dict.items())[:4]:
        cat_slug = re.sub(r'[^a-z0-9]+', '-', cat_name.lower()).strip('-')
        sitemap_urls.append(f"https://www.asmveo.com/category/{cat_slug}.html")
        
        # Generate Category Pages with Pagination
        prods_per_page = 24
        total_pages = math.ceil(len(prods) / prods_per_page)
        
        for page_num in range(1, total_pages + 1):
            start_idx = (page_num - 1) * prods_per_page
            end_idx = start_idx + prods_per_page
            current_prods = prods[start_idx:end_idx]
            
            file_slug = cat_slug if page_num == 1 else f"{cat_slug}-{page_num}"
            page_title = f"{cat_name} - Page {page_num}" if page_num > 1 else cat_name
            
            # Bug 5 Fix: Add paginated pages to sitemap
            sitemap_urls.append(f"https://www.asmveo.com/category/{file_slug}.html")
            
            cat_html = get_html_header(page_title, categories_list, f"Buy {cat_name} online in Pakistan at best prices. Wide range of {cat_name} with Cash on Delivery from ASM VEO.")
            
            min_price = min(p['final_price'] for p in prods)
            max_price = max(p['final_price'] for p in prods)
            
            cat_html += f"""
            <div class="animated-bg py-12 mb-8 relative overflow-hidden">
                <div class="absolute top-10 right-10 w-32 h-32 bg-white/10 rounded-full animate-float"></div>
                <div class="absolute bottom-10 left-10 w-48 h-48 bg-white/5 rounded-full animate-float" style="animation-delay: 2s;"></div>
                <div class="container mx-auto px-4 text-center relative z-10">
                    <div class="w-16 h-16 mx-auto rounded-full bg-white/20 backdrop-blur flex items-center justify-center mb-4 text-white shadow-lg">
                        <i class="fas {get_category_icon(cat_name)} text-3xl"></i>
                    </div>
                    <h1 class="text-3xl md:text-5xl font-black text-white">{cat_name}</h1>
                    <p class="text-gray-200 mt-3 font-bold">{len(prods)} Products Available • Cash on Delivery</p>
                </div>
            </div>
            
            <div class="container mx-auto px-4 pb-12">
                <div id="productGrid" class="grid grid-cols-3 md:grid-cols-6 gap-3 md:gap-4">
            """
            
            for prod in current_prods:
                cat_html += generate_product_card(prod, lazy=False)
            
            cat_html += "</div>"
            
            # Bug 2 Fix: Load search data if undefined in applyFilters
            cat_script_filters = """
            <script>
                function applyFilters() {
                    if (typeof allProducts === 'undefined') {
                        setTimeout(applyFilters, 500);
                        return;
                    }
                    let sortBy = document.getElementById('sortBy').value;
                    let minP = parseFloat(document.getElementById('minPrice').value) || 0;
                    let maxP = parseFloat(document.getElementById('maxPrice').value) || 999999;
                    
                    let filtered = allProducts.filter(p => p.final_price >= minP && p.final_price <= maxP);
                    
                    if (sortBy === 'price-low') filtered.sort((a,b) => a.final_price - b.final_price);
                    else if (sortBy === 'price-high') filtered.sort((a,b) => b.final_price - a.final_price);
                    else if (sortBy === 'name') filtered.sort((a,b) => a.name.localeCompare(b.name));
                    
                    let grid = document.getElementById('productGrid');
                    if (filtered.length === 0) {
                        grid.innerHTML = '<div class="col-span-full text-center py-16 text-gray-500">No products found</div>';
                    } else {
                        grid.innerHTML = filtered.map(p => generateCard(p)).join('');
                    }
                }
                
                function generateCard(p) {
                    let discount = Math.ceil(((p.fake_price - p.final_price) / p.fake_price) * 100);
                    if (isNaN(discount)) discount = 0;
                    let safeName = p.name.split("'").join("\\'"); 
                    let safeDesc = p.seo_desc ? p.seo_desc.split("'").join("\\'") : '';
                    return `<div class="product-card reveal active bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col relative cursor-pointer" onclick="window.location.href='/product/${p.slug}.html'">
                        <button onclick="toggleWishlist('${safeName}', ${p.final_price}, '${p.image}', event)" class="absolute top-2 right-2 w-8 h-8 bg-white rounded-full shadow-md flex items-center justify-center hover:bg-pink-50 transition z-10"><i class="fas fa-heart text-pink-500 text-sm"></i></button>
                        <button onclick="quickView('${safeName}', ${p.final_price}, '${p.image}', '${safeDesc}', '${p.slug}')" class="absolute top-2 right-12 w-8 h-8 bg-white rounded-full shadow-md flex items-center justify-center hover:bg-gray-100 transition z-10"><i class="fas fa-eye text-[#E53935] text-sm"></i></button>
                        ${discount > 0 ? `<div class="absolute top-2 left-2 bg-[#E53935] text-white text-[10px] font-black px-1.5 py-0.5 rounded z-10 shadow-md">-${discount}% OFF</div>` : ''}
                        <div class="image-zoom h-32 md:h-40 bg-gray-50 dark:bg-gray-700 overflow-hidden relative border-b border-gray-200 dark:border-gray-700 flex justify-center items-center">
                            <img src="${p.image}" alt="${p.name}" loading="lazy" width="200" height="200" class="w-full h-full object-contain p-1" onerror="this.src='https://via.placeholder.com/200x200/E53935/ffffff?text=ASM+VEO'">
                        </div>
                        <div class="p-2 flex flex-col flex-grow">
                            <span class="text-[9px] font-bold text-[#E53935] uppercase tracking-wider mb-1 line-clamp-1">${p.category}</span>
                            <h3 class="text-[10px] md:text-xs font-bold text-gray-900 dark:text-white leading-tight mb-1 line-clamp-2">${p.name}</h3>
                            <div class="mt-auto">
                                <div class="flex items-center gap-1 mb-1">
                                    <span class="text-xs md:text-sm font-black text-[#E53935] dark:text-white">Rs ${p.final_price}</span>
                                    <span class="text-[9px] text-gray-400 font-bold line-through">Rs ${p.fake_price}</span>
                                </div>
                                <button onclick="addToCart('${safeName}', ${p.final_price}, '${p.image}', event)" class="w-full bg-gray-50 text-[#E53935] py-1.5 rounded-md text-[10px] font-bold border border-gray-200 hover:bg-[#E53935] hover:text-white transition flex justify-center items-center"><i class="fas fa-cart-plus"></i></button>
                            </div>
                        </div>
                    </div>`;
                }
                
                function resetFilters() {
                    document.getElementById('sortBy').value = 'default';
                    document.getElementById('minPrice').value = '__MIN_PRICE__';
                    document.getElementById('maxPrice').value = '__MAX_PRICE__';
                    applyFilters();
                }
            </script>
            """
            
            cat_html += f"""
                <div class="flex flex-col lg:flex-row gap-6 mt-8">
                    <aside class="lg:w-64 flex-shrink-0">
                        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 p-5 sticky top-24">
                            <h3 class="font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2"><i class="fas fa-filter text-[#E53935]"></i> Filters</h3>
                            <div class="mb-6">
                                <h4 class="text-sm font-bold text-gray-700 dark:text-gray-300 mb-3">Sort By</h4>
                                <select id="sortBy" onchange="applyFilters()" class="w-full bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg p-2 text-sm text-gray-900 dark:text-white">
                                    <option value="default">Featured</option>
                                    <option value="price-low">Price: Low to High</option>
                                    <option value="price-high">Price: High to Low</option>
                                    <option value="name">Name: A to Z</option>
                                </select>
                            </div>
                            <div class="mb-6">
                                <h4 class="text-sm font-bold text-gray-700 dark:text-gray-300 mb-3">Price Range</h4>
                                <div class="flex items-center gap-2 mb-2">
                                    <input type="number" id="minPrice" placeholder="Min" value="{int(min_price)}" class="w-full bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg p-2 text-sm text-gray-900 dark:text-white">
                                    <input type="number" id="maxPrice" placeholder="Max" value="{int(max_price)}" class="w-full bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg p-2 text-sm text-gray-900 dark:text-white">
                                </div>
                                <button onclick="applyFilters()" class="w-full bg-[#E53935] text-white py-2 rounded-lg text-sm font-bold hover:bg-[#C62828] transition">Apply Filter</button>
                            </div>
                            <button onclick="resetFilters()" class="w-full text-gray-500 hover:text-[#E53935] text-sm font-bold transition"><i class="fas fa-undo mr-1"></i> Reset Filters</button>
                        </div>
                    </aside>
                    <div class="flex-1">
                        <!-- Product grid is above -->
                        {generate_pagination_html(page_num, total_pages, cat_slug)}
                    </div>
                </div>
            </div>
            """
            
            all_prods_json = json.dumps([{
                "name": p['name'], "slug": p['slug'], "category": p['category'],
                "final_price": p['final_price'], "fake_price": p['fake_price'], "image": p['image'],
                "seo_desc": p['seo_desc']
            } for p in prods])
            
            cat_html += cat_script_filters.replace("__PRODUCTS_JSON__", all_prods_json)\
                                           .replace("__MIN_PRICE__", str(int(min_price)))\
                                           .replace("__MAX_PRICE__", str(int(max_price)))
            cat_html += get_html_footer()
            
            with open(f"output/category/{file_slug}.html", "w", encoding="utf-8") as f:
                f.write(cat_html)
        
        # Home Page Section
        home_html += f"""
        <div class="mb-14 category-section reveal">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl md:text-3xl font-black text-gray-900 dark:text-white border-l-4 border-[#E53935] pl-4">{cat_name}</h2>
                <a href="/category/{cat_slug}.html" class="text-[#E53935] dark:text-white font-bold text-sm bg-gray-50 dark:bg-gray-800 px-5 py-2.5 rounded-full hover:bg-[#E53935] hover:text-white transition-all shadow-sm">View All <i class="fas fa-arrow-right ml-1"></i></a>
            </div>
            <div class="grid grid-cols-3 md:grid-cols-6 gap-3 md:gap-4">
        """
        
        for idx, prod in enumerate(prods[:6]):
            home_html += generate_product_card(prod, lazy=(idx >= 3))
            total_rendered_products += 1
            
        home_html += "</div></div>"
    
    home_html += "</div></div>"

    # Home Page Next Button
    home_html += """
    <div class="container mx-auto px-4 py-8 flex justify-center">
        <a href="/index-2.html" class="bg-[#E53935] text-white px-8 py-3 rounded-xl font-bold hover:bg-[#C62828] transition shadow-lg flex items-center gap-2">
            Next Page <i class="fas fa-arrow-right"></i>
        </a>
    </div>
    """

    home_html += """
    <div class="container mx-auto px-4 py-8 border-t border-gray-200 dark:border-gray-700">
        <h2 class="text-2xl font-extrabold text-gray-900 dark:text-white mb-6 border-l-4 border-[#E53935] pl-4">Shop by City in Pakistan</h2>
        <div class="flex flex-wrap gap-3">
    """
    for city in cities:
        home_html += f'<a href="/city/{re.sub(r"[^a-z0-9]+", "-", city.lower()).strip("-")}.html" class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-5 py-2.5 rounded-full text-sm font-bold text-gray-700 dark:text-gray-300 hover:bg-[#E53935] hover:text-white transition shadow-sm">{city}</a>'
    home_html += "</div></div>"

    home_html += """
    <div id="recentlyViewedSection" class="hidden container mx-auto px-4 py-8 border-t border-gray-200 dark:border-gray-700">
        <h2 class="text-2xl font-extrabold text-gray-900 dark:text-white mb-6 border-l-4 border-[#E53935] pl-4">Recently Viewed</h2>
        <div id="recentlyViewedGrid" class="grid grid-cols-3 md:grid-cols-6 gap-3 md:gap-4"></div>
    </div>
    """
    
    home_script = """
    <script>
        function performSearch(query) {
            if (typeof searchIndex === 'undefined') {
                loadSearchData();
                setTimeout(() => performSearch(query), 500);
                return;
            }
            
            query = query.toLowerCase().trim();
            if (!query) {
                document.getElementById('defaultContent').classList.remove('hidden');
                document.getElementById('searchResultsSection').classList.add('hidden');
                document.getElementById('recentlyViewedSection').classList.remove('hidden');
                return;
            }
            
            let results = searchIndex.filter(p => 
                p.name.toLowerCase().includes(query) || 
                p.category.toLowerCase().includes(query)
            );
            
            document.getElementById('defaultContent').classList.remove('hidden');
            document.getElementById('recentlyViewedSection').classList.add('hidden');
            document.getElementById('searchResultsSection').classList.remove('hidden');
            document.getElementById('searchResultsHeading').innerText = 'Search Results for "' + query + '"';
            document.getElementById('searchResultsCount').innerText = results.length + ' products found';
            
            let html = '<div class="grid grid-cols-3 md:grid-cols-6 gap-3 md:gap-4 mt-6">';
            results.forEach(p => {
                let discount = Math.ceil(((p.fake_price - p.final_price) / p.fake_price) * 100);
                if (isNaN(discount)) discount = 0;
                // Bug 9 Fix: Escape HTML chars in recently viewed / search
                let safeName = p.name.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;'); 
                let escName = p.name.split("'").join("\\'");
                html += `<div class="product-card reveal active bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col relative cursor-pointer" onclick="window.location.href='/product/${p.slug}.html'">
                    ${discount > 0 ? `<div class="absolute top-2 left-2 bg-[#E53935] text-white text-[10px] font-black px-1.5 py-0.5 rounded z-10 shadow-md">-${discount}% OFF</div>` : ''}
                    <div class="image-zoom h-32 md:h-40 bg-gray-50 dark:bg-gray-700 overflow-hidden relative border-b border-gray-200 dark:border-gray-700 flex justify-center items-center">
                        <img src="${p.image}" alt="${safeName}" loading="lazy" width="200" height="200" class="w-full h-full object-contain p-1" onerror="this.src='https://via.placeholder.com/200x200/E53935/ffffff?text=ASM+VEO'">
                    </div>
                    <div class="p-2 flex flex-col flex-grow">
                        <span class="text-[9px] font-bold text-[#E53935] uppercase tracking-wider mb-1 line-clamp-1">${p.category}</span>
                        <h3 class="text-[10px] md:text-xs font-bold text-gray-900 dark:text-white leading-tight mb-1 line-clamp-2">${safeName}</h3>
                        <div class="mt-auto">
                            <div class="flex items-center gap-1 mb-1">
                                <span class="text-xs md:text-sm font-black text-[#E53935] dark:text-white">Rs ${p.final_price}</span>
                            </div>
                            <button onclick="addToCart('${escName}', ${p.final_price}, '${p.image}', event)" class="w-full bg-gray-50 text-[#E53935] py-1.5 rounded-md text-[10px] font-bold border border-gray-200 hover:bg-[#E53935] hover:text-white transition flex justify-center items-center"><i class="fas fa-cart-plus"></i></button>
                        </div>
                    </div>
                </div>`;
            });
            html += '</div>';
            
            if (results.length === 0) {
                html = '<div class="text-center py-16 text-gray-500"><i class="fas fa-search text-6xl mb-4 opacity-30"></i><p class="text-lg font-bold">No products found</p><p class="text-sm mt-2">Try different keywords</p></div>';
            }
            
            let resultsDiv = document.createElement('div');
            resultsDiv.innerHTML = html;
            let srSection = document.getElementById('searchResultsSection');
            let elements = srSection.children;
            for(let i = elements.length - 1; i >= 2; i--) {
                srSection.removeChild(elements[i]);
            }
            srSection.appendChild(resultsDiv);
        }
        
        const urlParams = new URLSearchParams(window.location.search);
        const searchQuery = urlParams.get('search');
        if (searchQuery) {
            document.getElementById('searchInput').value = searchQuery;
            loadSearchData();
            setTimeout(() => performSearch(searchQuery), 1000);
        }
        
        function renderRecentlyViewed() {
            let recent = JSON.parse(localStorage.getItem('asm_recent')) || [];
            recent = recent.slice(0, 6);
            if (recent.length === 0) return;
            
            document.getElementById('recentlyViewedSection').classList.remove('hidden');
            let grid = document.getElementById('recentlyViewedGrid');
            grid.innerHTML = recent.map(p => {
                let discount = Math.ceil(((p.fake_price - p.final_price) / p.fake_price) * 100);
                if (isNaN(discount)) discount = 0;
                let safeName = p.name.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
                return `<div class="product-card reveal active bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col relative cursor-pointer" onclick="window.location.href='/product/${p.slug}.html'">
                    ${discount > 0 ? `<div class="absolute top-2 left-2 bg-[#E53935] text-white text-[10px] font-black px-1.5 py-0.5 rounded z-10 shadow-md">-${discount}% OFF</div>` : ''}
                    <div class="h-32 md:h-40 bg-gray-50 dark:bg-gray-700 overflow-hidden border-b border-gray-200 dark:border-gray-700 flex justify-center items-center">
                        <img src="${p.image}" alt="${safeName}" loading="lazy" width="200" height="200" class="w-full h-full object-contain p-1" onerror="this.src='https://via.placeholder.com/200x200/E53935/ffffff?text=ASM+VEO'">
                    </div>
                    <div class="p-2 flex flex-col flex-grow">
                        <h3 class="text-[10px] md:text-xs font-bold text-gray-900 dark:text-white line-clamp-2 mb-1">${safeName}</h3>
                        <div class="mt-auto">
                            <span class="text-xs md:text-sm font-black text-[#E53935] dark:text-white">Rs ${p.final_price}</span>
                        </div>
                    </div>
                </div>`;
            }).join('');
        }
        window.addEventListener('load', renderRecentlyViewed);
    </script>
    """
    home_html += home_script + get_html_footer()
    
    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(home_html)

    # ================= CHECKOUT PAGE (TEHSILS DATA) =================
    pak_tehsils = [
        "Karachi", "Lahore", "Faisalabad", "Rawalpindi", "Multan", "Hyderabad", "Gujranwala", "Peshawar", "Quetta", "Islamabad",
        "Bahawalpur", "Sargodha", "Sialkot", "Sukkur", "Larkana", "Sheikhupura", "Bhimber", "Mirpur", "Muzaffarabad", "Kotli",
        "Bannu", "Charsadda", "Mardan", "Nowshera", "Swat", "Dir", "Chitral", "Abbottabad", "Mansehra", "Haripur",
        "Kohat", "Dera Ismail Khan", "Tank", "Paharpur", "Lakki Marwat", "Karak", "Hangu", "Kurram", "Orakzai", "Khyber",
        "Mohmand", "Bajaur", "Waziristan", "Dera Ghazi Khan", "Rajanpur", "Layyah", "Muzaffargarh", "Bhakkar", "Khushab", "Jhelum",
        "Chakwal", "Attock", "Talagang", "Pind Dadan Khan", "Murree", "Kallar Syedan", "Gujar Khan", "Kahuta", "Kotli Sattian", "Taxila",
        "Wah Cantt", "Hasan Abdal", "Fateh Jang", "Jand", "Pindi Gheb", "Dina", "Sohawa", "Dudial", "Mangla", "Darya Khan",
        "Mianwali", "Isakhel", "Piplan", "Kamar Mushani", "Domel", "Akora Khattak", "Shabqadar", "Tangi", "Risalpur", "Rashakai",
        "Takht Bhai", "Katlang", "Rustam", "Garhi Kapura", "Mahaban", "Topi", "Swabi", "Lahor", "Razar", "Chota Lahore",
        "Daggar", "Gadezai", "Dhok", "Nizampur", "Utla", "Shangla", "Alpuri", "Chakar", "Besham", "Puran",
        "Makhuzai", "Achhrai", "Chail", "Barkana", "Kuzkana", "Buner", "Gagra", "Khwazakhela", "Madyan", "Bahrain",
        "Kalam", "Matta", "Behrain", "Balakot", "Naran", "Kaghan", "Shinkiari", "Oghi", "Darband", "Baffa",
        "Dhodial", "Battagram", "Allai", "Chattar", "Alo", "Banna", "Rashang", "Pattan", "Kolai", "Palas",
        "Jalkot", "Kandia", "Dasu", "Komila", "Khalo", "Harban", "Seo", "Gowari", "Bhobat", "Chilas",
        "Darel", "Tangir", "Gilgit", "Skardu", "Hunza", "Nagar", "Ghizer", "Yasin", "Gupis", "Puniyal",
        "Ishkoman", "Yarkhun", "Mastuj", "Laspur", "Mulkhow", "Torkhow", "Khot", "Banda Daud Shah", "Takht-e-Nasrati", "Narri",
        "Tall", "Thall", "Doaba", "Muhammad Khel", "Muhammadzai", "Sandi", "Torghar", "Makhmour", "Bajaur", "Nawagai",
        "Mamund", "Salarzai", "Chamarkand", "Utmankhel", "Khar", "Yousaf Khel", "Chakdara", "Timergara", "Wari", "Barawal",
        "Shahi", "Kalkot", "Sheringal", "Patrak", "Khal Qila", "Quetta", "Chaman", "Pishin", "Qila Abdullah", "Zhob",
        "Musakhel", "Killa Saifullah", "Barkhan", "Sherani", "Loralai", "Duki", "Kingri", "Kohlu", "Mawand", "Bhambore",
        "Sibi", "Lehri", "Dhadar", "Bhag", "Tambu", "Naseerabad", "Chattar", "Tamboo", "Usta Muhammad", "Jafarabad",
        "Sohbatpur", "Jhal Magsi", "Gandakha", "Kachi", "Machh", "Sanni", "Shoran", "Khuzdar", "Wadh", "Nal",
        "Surab", "Kalat", "Mangocher", "Mastung", "Kharan", "Nushki", "Washuk", "Mashkel", "Dalbandin", "Taufiq",
        "Nok Kundi", "Chagai", "Turbat", "Buleda", "Dasht", "Mand", "Tump", "Kolwah", "Balnigore", "Kech",
        "Gwadar", "Jiwani", "Ormara", "Pasni", "Pishukan", "Surbandar", "Panjgur", "Paroom", "Gichk", "Rakhshan",
        "Zehri", "Saruna", "Karkh", "Kasur", "Okara", "Nankana Sahib", "Toba Tek Singh", "Jhang", "Chiniot", "Bhalwal",
        "Kot Momin", "Bhera", "Shahpur", "Sahiwal", "Sillanwali", "Noorpur Thal", "Kot Addu", "Alipur", "Jatoi", "Chaubara",
        "Karor Lal Esan", "Mankera", "Taunsa Sharif", "Rojsan", "Jampur", "Rahim Yar Khan", "Sadiqabad", "Liaquatpur", "Khanpur",
        "Bahawalnagar", "Haroonabad", "Chishtian", "Fort Abbas", "Hasilpur", "Khairpur Tamewali", "Yazman", "Ahmedpur East", "Shujabad", "Jalalpur Pirwala",
        "Vehari", "Burewala", "Mailsi", "Pakpattan", "Arifwala", "Chichawatni", "Khanewal", "Mian Channu", "Kabirwala", "Jahanian",
        "Lodhran", "Kahror Pakka", "Dunyapur", "Gujrat", "Kharian", "Sarai Alamgir", "Rawalakot", "Bagh", "Neelum", "Athmuqam",
        "Hattian Bala", "Kel", "Taobat", "Sharda", "Abbaspur", "Hajira", "Forward Kahuta", "Tatrinot", "Mang", "Tolipir",
        "Nakyal", "Sehnsa", "Dadyal", "Chakswari", "Other"
    ]
    pak_tehsils = sorted(list(set(pak_tehsils)))
    tehsil_options = "".join([f"<option value='{t}'>{t}</option>" for t in pak_tehsils])
    delivery_date = (datetime.now() + timedelta(days=3)).strftime("%A, %b %d")
    
    checkout_html = get_html_header("Secure Checkout", categories_list, "Complete your order with Cash on Delivery. Fast and secure checkout at ASM VEO.")
    checkout_html += f"""
    <div class="container mx-auto px-4 py-12 max-w-6xl">
        <h1 class="text-3xl font-extrabold text-[#E53935] dark:text-white mb-8 flex items-center gap-3"><i class="fas fa-lock text-[#E53935]"></i> Secure Checkout</h1>
        
        <div class="flex items-center justify-center mb-10">
            <div class="flex items-center text-[#E53935] font-bold">
                <div class="w-10 h-10 bg-[#E53935] text-white rounded-full flex items-center justify-center font-black">1</div>
                <span class="ml-2 hidden md:inline">Cart</span>
            </div>
            <div class="w-16 md:w-32 h-1 bg-[#E53935] mx-2"></div>
            <div class="flex items-center text-[#E53935] font-bold">
                <div class="w-10 h-10 bg-[#E53935] text-white rounded-full flex items-center justify-center font-black">2</div>
                <span class="ml-2 hidden md:inline">Details</span>
            </div>
            <div class="w-16 md:w-32 h-1 bg-gray-200 mx-2"></div>
            <div class="flex items-center text-gray-400 font-bold">
                <div class="w-10 h-10 bg-gray-200 text-gray-400 rounded-full flex items-center justify-center font-black">3</div>
                <span class="ml-2 hidden md:inline">Confirm</span>
            </div>
        </div>

        <div class="flex flex-col lg:flex-row gap-8">
            <div class="lg:w-1/2">
                <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-xl p-6 border border-gray-200 dark:border-gray-700 mb-6">
                    <h2 class="text-2xl font-black text-gray-900 dark:text-white mb-4 border-b pb-4 flex items-center gap-2"><i class="fas fa-shopping-bag text-[#E53935]"></i> Your Items</h2>
                    <div id="cartItemsContainer" class="space-y-4 max-h-[400px] overflow-y-auto pr-2"></div>
                </div>
                
                <div class="bg-gray-50 dark:bg-gray-800 rounded-2xl p-5 border border-gray-100 dark:border-gray-700">
                    <h3 class="font-bold text-gray-900 dark:text-white mb-3 text-sm">Why Shop With Us?</h3>
                    <div class="grid grid-cols-2 gap-3 text-xs">
                        <div class="flex items-center gap-2"><i class="fas fa-shield-alt text-[#E53935]"></i> 100% Secure Checkout</div>
                        <div class="flex items-center gap-2"><i class="fas fa-truck text-[#E53935]"></i> Fast Nationwide Delivery</div>
                        <div class="flex items-center gap-2"><i class="fas fa-undo text-[#E53935]"></i> 7-Day Return Policy</div>
                        <div class="flex items-center gap-2"><i class="fas fa-certificate text-[#E53935]"></i> 100% Genuine Products</div>
                    </div>
                </div>
            </div>

            <div class="lg:w-1/2">
                <div class="bg-[#E53935] p-6 rounded-t-3xl text-white relative">
                    <div class="absolute top-0 left-0 w-full h-1 bg-white rounded-t-3xl"></div>
                    <h1 class="text-2xl font-extrabold flex items-center gap-2"><i class="fas fa-map-marker-alt text-white"></i> Shipping Details</h1>
                    <p class="text-gray-200 text-sm mt-1"><i class="fas fa-truck"></i> Expected delivery: {delivery_date}</p>
                </div>
                
                <form id="checkoutForm" class="bg-white dark:bg-gray-800 p-6 md:p-8 rounded-b-3xl shadow-xl border border-gray-200 dark:border-gray-700 border-t-0 space-y-5">
                    <input type="hidden" name="_subject" value="🛒 New Order on ASM VEO!">
                    <input type="hidden" name="Product_Ordered" id="productField" value="">
                    <input type="hidden" name="Order_Total" id="totalField" value="">
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <div>
                            <label class="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">Full Name <span class="text-red-600">*</span></label>
                            <input type="text" name="Full_Name" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-[#E53935] outline-none" required placeholder="Ali Abbas">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">Email Address</label>
                            <input type="email" name="Email" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-[#E53935] outline-none" placeholder="you@example.com">
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <div>
                            <label class="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">Mobile Number <span class="text-red-600">*</span></label>
                            <input type="tel" name="Phone_Number" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-[#E53935] outline-none" required placeholder="03XXXXXXXXX">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">City / Tehsil / District <span class="text-red-600">*</span></label>
                            <input type="text" name="City" id="cityInput" list="pakTehsils" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-[#E53935] outline-none font-semibold" required placeholder="Type or select your city/tehsil">
                            <datalist id="pakTehsils">
                                {tehsil_options}
                            </datalist>
                        </div>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">Complete Delivery Address <span class="text-red-600">*</span></label>
                        <textarea name="Address" rows="3" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-[#E53935] outline-none" required placeholder="House No, Street, Area, Landmark..."></textarea>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">Coupon Code</label>
                        <div class="flex gap-2">
                            <input type="text" id="couponCode" placeholder="Enter ASM10 for 10% off (Min Rs 3000)" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-[#E53935] outline-none uppercase">
                            <button type="button" onclick="applyCoupon()" class="bg-gray-900 text-white px-5 rounded-xl font-bold hover:bg-gray-700 transition">Apply</button>
                        </div>
                    </div>
                    
                    <div class="bg-gray-50 dark:bg-gray-700 rounded-2xl p-5 border border-gray-100 dark:border-gray-600 mt-6">
                        <div class="flex justify-between text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">
                            <span>Subtotal</span>
                            <span id="subtotalDisplay">Rs 0</span>
                        </div>
                        <div class="flex justify-between text-sm font-bold text-[#E53935] dark:text-white mb-2 hidden" id="discountRow">
                            <span>Discount (10%)</span>
                            <span id="discountDisplay">- Rs 0</span>
                        </div>
                        <div class="flex justify-between text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">
                            <span>Delivery Charges</span>
                            <span id="deliveryDisplay">Rs 250</span>
                        </div>
                        <div class="flex justify-between items-center border-t border-gray-200 dark:border-gray-600 pt-3 mt-3">
                            <span class="font-black text-lg text-gray-900 dark:text-white">Total (COD)</span>
                            <span class="font-black text-2xl text-[#E53935] dark:text-white" id="grandTotalDisplay">Rs 250</span>
                        </div>
                    </div>

                    <button type="submit" id="submitBtn" class="w-full bg-[#E53935] text-white font-black py-4 rounded-xl hover:bg-[#C62828] transition-all shadow-xl text-lg transform hover:-translate-y-1 flex items-center justify-center gap-2">
                        <i class="fas fa-check-circle"></i> Confirm Order
                    </button>
                    
                    <a href="https://wa.me/923425478683?text=Hi,%20I%20want%20to%20order!" class="w-full bg-green-500 text-white font-black py-4 rounded-xl hover:bg-green-600 transition-all shadow-xl text-lg mt-3 flex items-center justify-center gap-2 transform hover:-translate-y-1">
                        <i class="fab fa-whatsapp text-xl"></i> Order via WhatsApp
                    </a>
                    
                    <p class="text-center text-xs text-gray-500 dark:text-gray-400 mt-4"><i class="fas fa-lock"></i> Your information is secure and never shared with third parties.</p>
                </form>
            </div>
        </div>
    </div>
    """
    
    checkout_script = """
    <script>
        let couponApplied = false;
        
        function applyCoupon() {
            let code = document.getElementById('couponCode').value;
            let currentSubtotal = 0;
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('buy_now') === 'true') {
                currentSubtotal = parseInt(urlParams.get('price')) || 0;
            } else {
                let cart = getCart();
                cart.forEach(item => currentSubtotal += parseInt(item.price) * (item.qty || 1));
            }

            if (code === 'ASM10') {
                if (currentSubtotal >= 3000) {
                    couponApplied = true;
                    showToast('Coupon applied! 10% discount added.', 'fa-check-circle', 'pk');
                } else {
                    couponApplied = false;
                    showToast('Minimum Rs 3000 shopping required for this coupon.', 'fa-exclamation-circle', 'red');
                }
            } else {
                couponApplied = false;
                showToast('Invalid coupon code.', 'fa-times-circle', 'red');
            }
            renderCart();
        }

        function renderCart() {
            const urlParams = new URLSearchParams(window.location.search);
            const isBuyNow = urlParams.get('buy_now') === 'true';
            const pName = urlParams.get('product');
            // Bug 6 Fix: Prevent NaN error
            const pPrice = parseInt(urlParams.get('price')) || 0;
            
            let subtotal = 0;
            let finalOrderString = "";
            let container = document.getElementById('cartItemsContainer');
            container.innerHTML = '';
            
            if (isBuyNow && pName && pPrice) {
                subtotal = pPrice;
                finalOrderString = "1x " + pName + " (Rs " + pPrice + ")";
                container.innerHTML = `
                    <div class="flex items-center gap-4 bg-gray-50 dark:bg-gray-700 p-3 rounded-xl border border-gray-200 dark:border-gray-600">
                        <div class="flex-1">
                            <h3 class="font-bold text-gray-900 dark:text-white line-clamp-1">${pName}</h3>
                            <p class="text-[#E53935] dark:text-white font-black">Rs ${pPrice}</p>
                        </div>
                    </div>`;
            } else {
                let cart = getCart();
                if(cart.length === 0) {
                    container.innerHTML = `<div class="text-center py-8"><i class="fas fa-shopping-cart text-5xl text-gray-300 mb-3"></i><p class="text-gray-500 font-semibold">Your cart is empty.</p><a href="/index.html" class="inline-block mt-4 bg-[#E53935] text-white px-6 py-2 rounded-xl font-bold">Browse Products</a></div>`;
                    document.getElementById('submitBtn').disabled = true;
                    document.getElementById('submitBtn').classList.add('opacity-50', 'cursor-not-allowed');
                } else {
                    cart.forEach((item, index) => {
                        let qty = item.qty || 1;
                        subtotal += parseInt(item.price) * qty;
                        finalOrderString += qty + "x " + item.name + " (Rs " + (item.price * qty) + ")\\n";
                        
                        container.innerHTML += `
                        <div class="flex items-center gap-3 bg-gray-50 dark:bg-gray-700 p-3 rounded-xl border border-gray-200 dark:border-gray-600">
                            <img src="${item.image}" class="w-16 h-16 object-contain rounded-lg bg-white border border-gray-100 p-1" onerror="this.src='https://via.placeholder.com/100x100/E53935/ffffff?text=ASM'">
                            <div class="flex-1 min-w-0">
                                <h3 class="font-bold text-sm text-gray-900 dark:text-white line-clamp-2">${item.name}</h3>
                                <p class="text-[#E53935] dark:text-white font-black text-sm">Rs ${item.price}</p>
                                <div class="flex items-center gap-2 mt-1">
                                    <button onclick="updateQty(${index}, -1)" class="w-6 h-6 bg-gray-200 dark:bg-gray-600 rounded text-gray-700 dark:text-white font-bold hover:bg-gray-300">-</button>
                                    <span class="font-bold text-sm">${qty}</span>
                                    <button onclick="updateQty(${index}, 1)" class="w-6 h-6 bg-gray-200 dark:bg-gray-600 rounded text-gray-700 dark:text-white font-bold hover:bg-gray-300">+</button>
                                    <button onclick="removeFromCart(${index})" class="ml-2 text-red-500 hover:text-red-700 text-xs"><i class="fas fa-trash"></i></button>
                                </div>
                            </div>
                        </div>`;
                    });
                }
            }

            let delivery = subtotal >= 5000 ? 0 : 250;
            let discount = couponApplied ? Math.floor(subtotal * 0.10) : 0;
            let grandTotal = subtotal - discount + delivery;
            
            document.getElementById('subtotalDisplay').innerText = "Rs " + subtotal;
            document.getElementById('deliveryDisplay').innerText = delivery === 0 ? "FREE" : "Rs " + delivery;
            
            let discountRow = document.getElementById('discountRow');
            if (discount > 0) {
                discountRow.classList.remove('hidden');
                document.getElementById('discountDisplay').innerText = "- Rs " + discount;
            } else {
                discountRow.classList.add('hidden');
            }
            
            document.getElementById('grandTotalDisplay').innerText = "Rs " + grandTotal;
            document.getElementById('productField').value = finalOrderString + "\\nDelivery: Rs " + delivery + "\\nDiscount: Rs " + discount + "\\nGrand Total: Rs " + grandTotal;
            document.getElementById('totalField').value = "Rs " + grandTotal;
        }

        document.getElementById('checkoutForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const btn = document.getElementById('submitBtn');
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            btn.disabled = true;

            const formData = new FormData(this);
            fetch('https://formspree.io/f/xjgnlgpw', {
                method: 'POST',
                body: formData,
                headers: { 'Accept': 'application/json' }
            }).then(response => {
                if (response.ok) {
                    const urlParams = new URLSearchParams(window.location.search);
                    if(urlParams.get('buy_now') !== 'true') localStorage.removeItem('asm_cart');
                    updateCartBadge();
                    window.location.href = '/order-success.html';
                } else {
                    showToast('Error submitting order. Try again.', 'fa-exclamation-circle', 'red');
                    btn.innerHTML = '<i class="fas fa-check-circle"></i> Confirm Order';
                    btn.disabled = false;
                }
            }).catch(error => {
                showToast('Network Error! Try WhatsApp instead.', 'fa-wifi', 'red');
                btn.innerHTML = '<i class="fas fa-check-circle"></i> Confirm Order';
                btn.disabled = false;
            });
        });

        window.addEventListener('load', renderCart);
    </script>
    """
    checkout_html += checkout_script + get_html_footer()
    with open("output/checkout.html", "w", encoding="utf-8") as f:
        f.write(checkout_html)
        
    generate_sitemap(sitemap_urls)
    print("🎉 Advanced Pakistani E-Commerce website generated successfully!")
    print(f"📦 Products: {len(products_list)} | 📂 Categories: {len(categories_list)} | 🏙️ Cities: {len(cities)}")
    print("✨ All 10 Bugs Fixed & Flashmart Theme Integrated!")

if __name__ == "__main__":
    process_woocommerce_csv()
```
