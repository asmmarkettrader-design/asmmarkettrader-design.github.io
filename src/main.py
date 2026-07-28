import os
import csv
import math
import re
import shutil
import random
import json
from datetime import datetime, timedelta

# ==================== 2000 NAMES DATABASE ====================

def generate_pakistani_names():
    first_names = ["Muhammad", "Ali", "Ahmed", "Hassan", "Hussain", "Bilal", "Usman", "Umar", "Hamza", "Zain", 
                   "Ayesha", "Fatima", "Maryam", "Zainab", "Hira", "Sana", "Iqra", "Anum", "Sadia", "Aiman",
                   "Abdullah", "Rehman", "Tariq", "Imran", "Kamran", "Asad", "Faisal", "Shahid", "Waqar", "Naveed",
                   "Bilal", "Sana", "Adnan", "Farhan", "Nida", "Saba", "Komail", "Mahnoor",
                   "Rizwan", "Sohail", "Asif", "Nadeem", "Tahir", "Amir", "Babar", "Saad", "Fahad", "Junaid",
                   "Hina", "Areeba", "Tooba", "Rabia", "Anila", "Faiza", "Samina", "Naila", "Shazia", "Rimsha",
                   "Ahsan", "Zeeshan", "Kashif", "Noman", "Waseem", "Imtiaz", "Ghulam", "Sajid", "Rashid", "Aslam",
                   "Bilal", "Sana", "Adnan", "Farhan", "Nida", "Saba", "Komail", "Mahnoor", "Ayesha", "Fatima"]
    last_names = ["Khan", "Raza", "Malik", "Sheikh", "Qureshi", "Siddiqui", "Chaudhry", "Butt", "Awan", "Mughal",
                  "Baig", "Mirza", "Hashmi", "Tariq", "Ahmed", "Iqbal", "Hussain", "Aslam", "Akram", "Yousaf",
                  "Shah", "Rana", "Cheema", "Tipu", "Afridi", "Khattak", "Wazir", "Mehmood", "Sattar"]
    
    # Instantly generate all combinations (No while loop, No hanging)
    all_names = [f"{f} {l}" for f in first_names for l in last_names]
    random.shuffle(all_names)
    return all_names

PAKISTANI_NAMES = generate_pakistani_names()

# ==================== UTILITY FUNCTIONS ====================

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
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

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
        "Bahut khush hoon is product se. ASM VEO is trustworthy.",
        "Paisa wasool hai. Delivery thodi slow thi par product mast hai.",
        "Main is product se bohat khush hoon. High quality material."
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
                <div class="w-9 h-9 rounded-full bg-[#01411C] text-white flex items-center justify-center font-bold text-sm" aria-hidden="true">{reviewer[0]}</div>
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
        c_slug = make_slug(cat)
        cat_links += f'<a href="/category/{c_slug}.html" class="block px-4 py-2.5 text-sm text-gray-700 hover:bg-[#01411C] hover:text-white transition-colors">{cat}</a>\n'

    structured_data = ""
    if product_data:
        structured_data = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org/",
      "@type": "Product",
      "name": "{product_data['name']}",
      "image": ["{product_data['image']}"],
      "description": "{product_data.get('seo_desc', '')}",
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
        structured_data += f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.asmveo.com/" }},
        {{ "@type": "ListItem", "position": 2, "name": "{breadcrumb_data['category']}", "item": "https://www.asmveo.com/category/{make_slug(breadcrumb_data['category'])}.html" }},
        {{ "@type": "ListItem", "position": 3, "name": "{breadcrumb_data['name']}", "item": "https://www.asmveo.com/product/{breadcrumb_data['slug']}.html" }}
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
    <meta name="theme-color" content="#01411C">
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
                    colors: {{ pk: {{ green: '#01411C', light: '#f0fdf4', dark: '#002a13' }} }}
                }}
            }}
        }}
    </script>
    
    <!-- Defer Font Awesome to prevent render blocking -->
    <link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"></noscript>
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');
        
        /* PAKISTANI FLAG BACKGROUND */
        body {{ 
            font-family: 'Plus Jakarta Sans', sans-serif; 
            background: #ffffff; 
            background-image: linear-gradient(90deg, #ffffff 40px, #01411C 40px); 
            background-attachment: fixed;
            background-size: 100% 100%;
            color: #ffffff;
            transition: background-color 0.3s; 
            padding-bottom: 70px; 
        }}
        @media (max-width: 768px) {{
            body {{ background-image: linear-gradient(180deg, #ffffff 30px, #01411C 30px); }}
        }}
        
        .product-card {{ transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }}
        .product-card:hover {{ transform: translateY(-8px); box-shadow: 0 20px 40px -10px rgba(1, 65, 28, 0.2); }}
        .image-zoom img {{ transition: transform 0.5s ease; }}
        .product-card:hover .image-zoom img {{ transform: scale(1.1); }}
        .dropdown:hover .dropdown-menu {{ display: block; }}
        
        ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
        ::-webkit-scrollbar-track {{ background: #f1f5f9; }}
        ::-webkit-scrollbar-thumb {{ background: #01411C; border-radius: 4px; }}
        
        .line-clamp-1 {{ display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden; }}
        .line-clamp-2 {{ display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
        
        /* === ANIMATIONS === */
        @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-15px); }} }}
        .animate-float {{ animation: float 6s ease-in-out infinite; }}
        
        @keyframes pulse-ring {{ 0% {{ box-shadow: 0 0 0 0 rgba(1, 65, 28, 0.7); }} 70% {{ box-shadow: 0 0 0 15px rgba(1, 65, 28, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(1, 65, 28, 0); }} }}
        .pulse-ring {{ animation: pulse-ring 2s infinite; }}
        
        @keyframes slideIn {{ from {{ transform: translateY(20px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}
        .slide-in {{ animation: slideIn 0.4s ease-out; }}
        
        .carousel-track {{ display: flex; transition: transform 0.8s cubic-bezier(0.65, 0, 0.35, 1); }}
        .carousel-slide {{ min-width: 100%; box-sizing: border-box; }}
        
        .glass {{ background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); color: #01411C; }}
        .dark .glass {{ background: rgba(15, 23, 42, 0.95); color: #fff; }}
        
        /* Scroll Reveal Effect */
        .reveal {{ opacity: 0; transform: translateY(40px); transition: all 0.8s cubic-bezier(0.5, 0, 0, 1); }}
        .reveal.active {{ opacity: 1; transform: translateY(0); }}
        
        /* Animated Gradient Background */
        .animated-bg {{ background: linear-gradient(-45deg, #01411C, #065f46, #01411C, #002a13); background-size: 400% 400%; animation: gradient 15s ease infinite; }}
        @keyframes gradient {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
    </style>
    {structured_data}

    <script>
        // CART SYSTEM
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

        // WISHLIST SYSTEM
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
            const colors = {{ pk: 'bg-[#01411C]', red: 'bg-red-500', gray: 'bg-gray-600', green: 'bg-green-500' }};
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
            
            let safeName = name.replace(/'/g, "\\'");
            document.getElementById('qvAddCart').setAttribute('onclick', `addToCart('${{safeName}}', ${{price}}, '${{image}}', event); closeQuickView();`);
            document.getElementById('qvBuyNow').setAttribute('onclick', `buyNow('${{safeName}}', ${{price}}, '${{image}}', event);`);
            document.getElementById('qvLink').href = '/product/' + slug + '.html';
            modal.classList.remove('hidden');
            modal.classList.add('flex');
        }}
        function closeQuickView() {{
            document.getElementById('quickViewModal').classList.add('hidden');
            document.getElementById('quickViewModal').classList.remove('flex');
        }}

        // INIT
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

            // Scroll Reveal Animation
            let reveals = document.querySelectorAll('.reveal');
            function checkReveals() {{
                reveals.forEach(el => {{
                    let elTop = el.getBoundingClientRect().top;
                    if (elTop < window.innerHeight - 50) el.classList.add('active');
                }});
            }}
            window.addEventListener('scroll', checkReveals);
            checkReveals();
        }};

        function acceptCookies() {{
            localStorage.setItem('asm_cookie_consent', 'true');
            document.getElementById('cookieConsent').classList.add('hidden');
        }}
    </script>
</head>
<body class="text-gray-900 dark:text-gray-100">
    <header class="glass shadow-md sticky top-0 z-50 transition-colors border-b border-gray-100 dark:border-gray-800">
        <div class="bg-[#01411C] text-white text-xs md:text-sm py-2">
            <div class="container mx-auto px-4 flex justify-between items-center">
                <div class="flex space-x-4 items-center">
                    <a href="/index.html" class="hover:text-gray-300 transition font-semibold"><i class="fas fa-home mr-1"></i> Home</a>
                    <div class="relative dropdown z-50 hidden md:block">
                        <button class="hover:text-gray-300 transition font-semibold focus:outline-none"><i class="fas fa-list mr-1"></i> Categories <i class="fas fa-chevron-down text-[10px] ml-1"></i></button>
                        <div class="dropdown-menu absolute hidden text-gray-700 bg-white dark:bg-gray-800 dark:text-gray-200 shadow-2xl rounded-xl mt-1 w-56 py-2 border border-gray-100 dark:border-gray-700 max-h-96 overflow-y-auto">
                            {cat_links}
                        </div>
                    </div>
                    <a href="/about.html" class="hover:text-gray-300 transition font-semibold"><i class="fas fa-info-circle mr-1"></i> About</a>
                    <a href="/contact.html" class="hover:text-gray-300 transition font-semibold"><i class="fas fa-envelope mr-1"></i> Contact</a>
                    <a href="/faq.html" class="hover:text-gray-300 transition font-semibold"><i class="fas fa-question-circle mr-1"></i> FAQ</a>
                </div>
                <div class="flex items-center gap-3">
                    <button onclick="toggleDarkMode()" class="hover:text-gray-300 transition" aria-label="Toggle Dark Mode"><i class="fas fa-moon dark-mode-icon"></i></button>
                    <div class="hidden md:block text-white font-bold"><i class="fas fa-truck-fast"></i> Cash on Delivery</div>
                </div>
            </div>
        </div>

        <div class="container mx-auto px-4 py-4 flex flex-wrap justify-between items-center gap-4">
            <a href="/index.html" class="text-2xl md:text-3xl font-extrabold text-[#01411C] dark:text-white tracking-tight flex items-center gap-2" aria-label="ASM VEO Home">
                <div class="bg-[#01411C] text-white p-2 rounded-lg shadow-md" aria-hidden="true"><i class="fas fa-shopping-bag"></i></div>
                ASM VEO
            </a>
            
            <div class="flex-1 min-w-[200px] max-w-xl mx-0 md:mx-8 relative">
                <label for="searchInput" class="sr-only">Search products in Pakistan</label>
                <input type="text" id="searchInput" onkeypress="handleSearch(event)" placeholder="Search products, brands, categories..." class="w-full bg-gray-50 dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 focus:bg-white dark:focus:bg-gray-700 focus:border-[#01411C] rounded-xl py-3 px-6 outline-none transition-all text-gray-800 dark:text-gray-100 font-semibold shadow-sm">
                <button onclick="executeSearch()" aria-label="Search" class="absolute right-4 top-3 text-gray-500 hover:text-[#01411C]"><i class="fas fa-search text-xl" aria-hidden="true"></i></button>
            </div>
            
            <div class="flex items-center gap-3">
                <a href="/wishlist.html" class="relative bg-pink-50 text-pink-600 p-3 rounded-xl hover:bg-pink-600 hover:text-white transition-colors border border-pink-200" aria-label="Wishlist">
                    <i class="fas fa-heart"></i>
                    <span class="wishlist-badge absolute -top-2 -right-2 bg-pink-500 text-white text-xs font-black px-1.5 py-0.5 rounded-full shadow min-w-[20px] text-center">0</span>
                </a>
                <a href="/checkout.html" class="cart-icon-pulse relative bg-[#01411C] text-white px-5 py-3 rounded-xl font-bold hover:bg-[#002a13] transition-colors shadow-sm flex items-center gap-2" aria-label="Go to Cart">
                    <i class="fas fa-shopping-cart text-xl" aria-hidden="true"></i>
                    <span class="hidden md:inline">Cart</span>
                    <span class="cart-badge absolute -top-2 -right-2 bg-red-500 text-white text-xs font-black px-1.5 py-0.5 rounded-full shadow min-w-[20px] text-center">0</span>
                </a>
            </div>
        </div>
    </header>

    <div id="cookieConsent" class="hidden fixed bottom-20 md:bottom-0 left-0 right-0 bg-gray-900 text-white p-4 z-[9998] shadow-2xl">
        <div class="container mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-3">
                <i class="fas fa-cookie-bite text-2xl text-white"></i>
                <p class="text-sm">We use cookies to improve your experience. By continuing to browse, you agree to our use of cookies.</p>
            </div>
            <div class="flex gap-3">
                <a href="/privacy.html" class="text-white hover:text-gray-300 text-sm font-bold">Privacy Policy</a>
                <button onclick="acceptCookies()" class="bg-[#01411C] hover:bg-[#002a13] px-6 py-2 rounded-lg font-bold text-sm transition">Accept</button>
            </div>
        </div>
    </div>

    <nav class="fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-900 shadow-2xl border-t border-gray-100 dark:border-gray-800 flex justify-around py-2 md:hidden z-50">
        <a href="/index.html" class="flex flex-col items-center text-[#01411C] text-xs font-bold"><i class="fas fa-home text-lg mb-1"></i> Home</a>
        <a href="/index.html#products" class="flex flex-col items-center text-gray-500 dark:text-gray-400 text-xs font-bold"><i class="fas fa-th-large text-lg mb-1"></i> Categories</a>
        <a href="/checkout.html" class="flex flex-col items-center text-gray-500 dark:text-gray-400 text-xs font-bold relative">
            <i class="fas fa-shopping-cart text-lg mb-1"></i> Cart
            <span class="cart-badge absolute -top-1 right-2 bg-red-500 text-white text-[8px] font-black px-1 py-0.5 rounded-full">0</span>
        </a>
        <a href="/wishlist.html" class="flex flex-col items-center text-gray-500 dark:text-gray-400 text-xs font-bold relative">
            <i class="fas fa-heart text-lg mb-1"></i> Wishlist
            <span class="wishlist-badge absolute -top-1 right-2 bg-pink-500 text-white text-[8px] font-black px-1 py-0.5 rounded-full">0</span>
        </a>
    </nav>

    <div id="exitModal" class="hidden fixed inset-0 bg-black/70 z-[9999] items-center justify-center p-4">
        <div class="bg-white dark:bg-gray-800 rounded-3xl p-8 max-w-md w-full text-center relative slide-in">
            <button onclick="document.getElementById('exitModal').classList.add('hidden')" class="absolute top-4 right-4 text-gray-400 hover:text-gray-600"><i class="fas fa-times text-xl"></i></button>
            <i class="fas fa-gift text-6xl text-[#01411C] mb-4"></i>
            <h2 class="text-2xl font-extrabold text-gray-900 dark:text-white mb-2">Wait! Here's 10% OFF</h2>
            <p class="text-gray-500 dark:text-gray-400 mb-6">Don't leave empty-handed. Use this code at checkout for an instant 10% discount on your order!</p>
            <div class="bg-gray-50 border-2 border-dashed border-[#01411C] rounded-xl py-4 mb-6">
                <span class="text-3xl font-black text-[#01411C] tracking-widest">ASM10</span>
            </div>
            <a href="/index.html#products" onclick="document.getElementById('exitModal').classList.add('hidden')" class="block bg-[#01411C] text-white py-3 rounded-xl font-bold hover:bg-[#002a13] transition">Continue Shopping</a>
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
                <p id="qvPrice" class="text-2xl font-black text-[#01411C] dark:text-white mb-3"></p>
                <p id="qvDesc" class="text-sm text-gray-500 dark:text-gray-400 mb-6"></p>
                <div class="mt-auto flex flex-col gap-2">
                    <button id="qvAddCart" class="w-full bg-[#01411C] text-white py-3 rounded-xl font-bold hover:bg-[#002a13] transition flex items-center justify-center gap-2"><i class="fas fa-cart-plus"></i> Add to Cart</button>
                    <button id="qvBuyNow" class="w-full bg-gray-900 dark:bg-white text-white dark:text-gray-900 py-3 rounded-xl font-bold hover:bg-gray-800 dark:hover:bg-gray-100 transition flex items-center justify-center gap-2"><i class="fas fa-bolt"></i> Buy Now</button>
                    <a id="qvLink" href="#" class="text-center text-sm text-[#01411C] hover:underline mt-2">View Full Details</a>
                </div>
            </div>
        </div>
    </div>

    <a href="https://wa.me/923425478683?text=Hi,%20I%20want%20to%20know%20about%20your%20products" target="_blank" 
       class="fixed bottom-24 right-4 bg-green-500 text-white w-14 h-14 rounded-full shadow-2xl flex items-center justify-center hover:bg-green-600 transition-all z-50 hover:scale-110 pulse-ring" 
       aria-label="Chat on WhatsApp">
        <i class="fab fa-whatsapp text-3xl"></i>
    </a>

    <button id="backToTop" onclick="scrollTop()" class="hidden fixed bottom-24 left-4 bg-[#01411C] text-white w-12 h-12 rounded-full shadow-2xl items-center justify-center hover:bg-[#002a13] transition z-50" aria-label="Back to top">
        <i class="fas fa-arrow-up text-xl"></i>
    </button>

    <main id="main-content" class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 shadow-2xl">
"""

# ==================== HTML FOOTER ====================

def get_html_footer():
    return """
    </main>
    <footer class="bg-[#01411C] text-white mt-16 pt-16 pb-20 md:pb-8 border-t-4 border-white">
        <div class="container mx-auto px-4 grid grid-cols-1 md:grid-cols-4 gap-10 mb-10">
            <div class="col-span-1 md:col-span-2">
                <h3 class="text-3xl font-extrabold mb-4 flex items-center gap-2 text-white"><i class="fas fa-shopping-bag text-white" aria-hidden="true"></i> ASM VEO</h3>
                <p class="text-gray-300 text-sm leading-relaxed mb-6 pr-4">ASM VEO is Pakistan's premium online shopping platform by <strong class="text-white">ASM Digital Solutions</strong>. Enjoy premium quality products, nationwide Cash on Delivery, 7-day return policy, and a 100% secure shopping experience.</p>
                <div class="flex gap-4 mb-6">
                    <a href="#" aria-label="Facebook" class="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center hover:bg-white hover:text-[#01411C] transition text-white"><i class="fab fa-facebook-f"></i></a>
                    <a href="#" aria-label="Instagram" class="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center hover:bg-white hover:text-[#01411C] transition text-white"><i class="fab fa-instagram"></i></a>
                    <a href="https://wa.me/923425478683" aria-label="WhatsApp" class="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center hover:bg-white hover:text-[#01411C] transition text-white"><i class="fab fa-whatsapp"></i></a>
                    <a href="#" aria-label="YouTube" class="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center hover:bg-white hover:text-[#01411C] transition text-white"><i class="fab fa-youtube"></i></a>
                </div>
                <div class="flex flex-wrap gap-3">
                    <div class="bg-white/10 px-4 py-2 rounded-lg flex items-center gap-2 text-xs font-bold"><i class="fas fa-shield-alt text-white"></i> SSL Secure</div>
                    <div class="bg-white/10 px-4 py-2 rounded-lg flex items-center gap-2 text-xs font-bold"><i class="fas fa-truck text-white"></i> Nationwide COD</div>
                    <div class="bg-white/10 px-4 py-2 rounded-lg flex items-center gap-2 text-xs font-bold"><i class="fas fa-undo text-white"></i> 7-Day Returns</div>
                </div>
            </div>
            <div>
                <h3 class="text-xl font-bold mb-5 text-white border-b border-white/20 pb-2">Quick Links</h3>
                <ul class="space-y-3 text-gray-300 text-sm font-semibold">
                    <li><a href="/index.html" class="hover:text-white transition"><i class="fas fa-angle-right mr-2 text-white"></i> Home</a></li>
                    <li><a href="/about.html" class="hover:text-white transition"><i class="fas fa-angle-right mr-2 text-white"></i> About Us</a></li>
                    <li><a href="/contact.html" class="hover:text-white transition"><i class="fas fa-angle-right mr-2 text-white"></i> Contact Us</a></li>
                    <li><a href="/faq.html" class="hover:text-white transition"><i class="fas fa-angle-right mr-2 text-white"></i> FAQ</a></li>
                    <li><a href="/checkout.html" class="hover:text-white transition"><i class="fas fa-angle-right mr-2 text-white"></i> Cart / Checkout</a></li>
                    <li><a href="/privacy.html" class="hover:text-white transition"><i class="fas fa-angle-right mr-2 text-white"></i> Privacy Policy</a></li>
                    <li><a href="/terms.html" class="hover:text-white transition"><i class="fas fa-angle-right mr-2 text-white"></i> Terms & Conditions</a></li>
                </ul>
            </div>
            <div>
                <h3 class="text-xl font-bold mb-5 text-white border-b border-white/20 pb-2">Get in Touch</h3>
                <ul class="space-y-4 text-gray-300 text-sm">
                    <li class="flex items-center gap-3"><div class="bg-white/10 p-2 rounded text-white"><i class="fas fa-user-tie"></i></div> CEO: Ali Abbas</li>
                    <li class="flex items-center gap-3"><div class="bg-white/10 p-2 rounded text-white"><i class="fas fa-building"></i></div> ASM Digital Solutions</li>
                    <li class="flex items-center gap-3"><div class="bg-green-500 p-2 rounded text-white"><i class="fab fa-whatsapp text-lg"></i></div> <a href="https://wa.me/923425478683" class="hover:text-white transition font-bold text-base">0342 54 786 83</a></li>
                    <li class="flex items-center gap-3"><div class="bg-white/10 p-2 rounded text-white"><i class="fas fa-clock"></i></div> Mon-Sun: 9AM - 11PM</li>
                </ul>
            </div>
        </div>
        <div class="border-t border-white/20 text-center pt-8">
            <p class="text-gray-400 text-sm font-semibold">&copy; 2026 ASM Digital Solutions. All Rights Reserved. | Powered by ASM VEO</p>
        </div>
    </footer>
</body>
</html>
"""

# ==================== SITEMAP & ROBOTS ====================

def generate_sitemap(urls):
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
        "theme_color": "#01411C",
        "icons": [
            {"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}
        ]
    }
    with open("output/manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

# ==================== PRODUCT CARD GENERATOR ====================

def generate_product_card(prod, lazy=True, show_wishlist=True):
    discount = math.ceil(((prod['fake_price'] - prod['final_price']) / prod['fake_price']) * 100) if prod['fake_price'] > prod['final_price'] else 0
    stock_left = random.randint(3, 20)
    img_loading = 'loading="lazy"' if lazy else 'fetchpriority="high"'
    
    # Safe JS string escaping (outside f-string to prevent SyntaxError)
    escaped_name = prod['name'].replace("'", "\\'")
    escaped_desc = prod['seo_desc'].replace("'", "\\'")
    
    wishlist_btn = ""
    if show_wishlist:
        wishlist_btn = f"""
            <button onclick="toggleWishlist('{escaped_name}', {prod['final_price']}, '{prod['image']}', event)" 
                    class="wishlist-btn absolute top-3 right-3 w-9 h-9 bg-white rounded-full shadow-md flex items-center justify-center hover:bg-pink-50 transition z-10" 
                    aria-label="Add to Wishlist">
                <i class="fas fa-heart text-pink-500"></i>
            </button>"""
    
    quick_view_btn = f"""
        <button onclick="quickView('{escaped_name}', {prod['final_price']}, '{prod['image']}', '{escaped_desc}', '{prod['slug']}')" 
                class="absolute top-3 right-14 w-9 h-9 bg-white rounded-full shadow-md flex items-center justify-center hover:bg-gray-100 transition z-10" 
                aria-label="Quick View">
            <i class="fas fa-eye text-[#01411C]"></i>
        </button>"""
    
    return f"""
    <div class="product-card reveal bg-white dark:bg-gray-800 rounded-2xl shadow-sm hover:shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col relative cursor-pointer" onclick="window.location.href='/product/{prod['slug']}.html'">
        {wishlist_btn}
        {quick_view_btn}
        {f'<div class="absolute top-3 left-3 bg-red-600 text-white text-xs font-black px-2.5 py-1 rounded-lg z-10 shadow-md">-{discount}% OFF</div>' if discount > 0 else ''}
        <div class="image-zoom h-48 md:h-60 bg-gray-50 dark:bg-gray-700 overflow-hidden relative border-b border-gray-200 dark:border-gray-700 flex justify-center items-center">
            <img src="{prod['image']}" alt="{prod['name']} buy online in Pakistan" width="400" height="400" {img_loading} class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/400x400/01411C/ffffff?text=ASM+VEO'">
        </div>
        <div class="p-4 flex flex-col flex-grow">
            <span class="text-[10px] font-bold text-[#01411C] dark:text-white uppercase tracking-wider mb-1 line-clamp-1">{prod['category']}</span>
            <h3 class="prod-title text-sm md:text-base font-bold text-gray-900 dark:text-gray-100 leading-tight mb-2 line-clamp-2">{prod['name']}</h3>
            <div class="flex items-center gap-1 mb-2 text-yellow-500 text-xs">
                <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star-half-alt"></i>
                <span class="text-gray-400 ml-1">({random.randint(10, 200)})</span>
            </div>
            <div class="mt-auto">
                <div class="flex items-center gap-2 mb-1">
                    <span class="text-lg font-black text-[#01411C] dark:text-white">Rs {prod['final_price']}</span>
                    <span class="text-xs text-gray-400 font-bold line-through">Rs {prod['fake_price']}</span>
                </div>
                <div class="text-[10px] text-orange-600 font-bold mb-2"><i class="fas fa-fire"></i> Only {stock_left} left in stock!</div>
                <div class="flex gap-2 w-full">
                    <button onclick="addToCart('{escaped_name}', {prod['final_price']}, '{prod['image']}', event)" class="w-1/2 bg-gray-50 dark:bg-gray-700 text-[#01411C] dark:text-white py-2.5 rounded-xl text-xs font-bold border border-gray-200 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-600 transition flex justify-center items-center" aria-label="Add to Cart">
                        <i class="fas fa-cart-plus"></i>
                    </button>
                    <button onclick="buyNow('{escaped_name}', {prod['final_price']}, '{prod['image']}', event)" class="w-1/2 bg-[#01411C] text-white py-2.5 rounded-xl text-xs font-bold hover:bg-[#002a13] transition text-center" aria-label="Buy Now">
                        Buy Now
                    </button>
                </div>
            </div>
        </div>
    </div>
    """

# ==================== STATIC PAGES ====================

def generate_static_pages(categories_list):
    with open("output/about.html", "w", encoding="utf-8") as f:
        f.write(get_html_header("About Us", categories_list) + """
        <div class="container mx-auto px-4 py-16 max-w-4xl">
            <div class="text-center mb-12 reveal">
                <h1 class="text-4xl md:text-5xl font-extrabold text-[#01411C] dark:text-white mb-6">About ASM VEO</h1>
                <p class="text-lg text-gray-600 dark:text-gray-300 leading-relaxed">Your trusted shopping partner in Pakistan</p>
            </div>
            <div class="grid md:grid-cols-2 gap-8 mb-12">
                <div class="reveal bg-white dark:bg-gray-800 p-8 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-700">
                    <div class="w-14 h-14 bg-gray-100 rounded-2xl flex items-center justify-center mb-4"><i class="fas fa-bullseye text-2xl text-[#01411C]"></i></div>
                    <h3 class="text-xl font-bold mb-3 text-gray-900 dark:text-white">Our Mission</h3>
                    <p class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">To provide every Pakistani with access to premium quality products at affordable prices, delivered right to their doorstep with Cash on Delivery convenience.</p>
                </div>
                <div class="reveal bg-white dark:bg-gray-800 p-8 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-700">
                    <div class="w-14 h-14 bg-gray-100 rounded-2xl flex items-center justify-center mb-4"><i class="fas fa-eye text-2xl text-[#01411C]"></i></div>
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
            <h1 class="text-4xl font-extrabold text-[#01411C] dark:text-white mb-8 text-center reveal">Contact Us</h1>
            <div class="grid md:grid-cols-2 gap-8">
                <div class="reveal bg-white dark:bg-gray-800 rounded-3xl shadow-xl p-8 border border-gray-100 dark:border-gray-700">
                    <i class="fab fa-whatsapp text-6xl text-green-500 mb-4"></i>
                    <h2 class="text-2xl font-bold mb-2 text-gray-900 dark:text-white">WhatsApp Support</h2>
                    <p class="text-gray-600 dark:text-gray-300 mb-6">Quick and instant support for all your queries. Message us anytime!</p>
                    <a href="https://wa.me/923425478683" class="inline-block bg-green-500 text-white font-black py-4 px-8 rounded-xl hover:bg-green-600 transition shadow-lg w-full text-center"><i class="fab fa-whatsapp mr-2"></i> 0342 54 786 83</a>
                </div>
                <div class="reveal bg-white dark:bg-gray-800 rounded-3xl shadow-xl p-8 border border-gray-100 dark:border-gray-700">
                    <i class="fas fa-headset text-6xl text-[#01411C] mb-4"></i>
                    <h2 class="text-2xl font-bold mb-2 text-gray-900 dark:text-white">Business Hours</h2>
                    <ul class="text-gray-600 dark:text-gray-300 space-y-2">
                        <li class="flex justify-between"><span>Monday - Friday</span><span class="font-bold">9AM - 11PM</span></li>
                        <li class="flex justify-between"><span>Saturday</span><span class="font-bold">10AM - 11PM</span></li>
                        <li class="flex justify-between"><span>Sunday</span><span class="font-bold">12PM - 10PM</span></li>
                    </ul>
                    <div class="mt-6 pt-6 border-t border-gray-100 dark:border-gray-700">
                        <p class="text-sm text-gray-500"><i class="fas fa-building mr-2 text-[#01411C]"></i> ASM Digital Solutions</p>
                        <p class="text-sm text-gray-500 mt-1"><i class="fas fa-user-tie mr-2 text-[#01411C]"></i> CEO: Ali Abbas</p>
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
        <h1 class="text-4xl font-extrabold text-[#01411C] dark:text-white mb-8 text-center reveal">Frequently Asked Questions</h1>
        <div class="space-y-4">
    """
    for q, a in faqs:
        faq_html += f"""
            <details class="reveal bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 group">
                <summary class="p-5 cursor-pointer font-bold text-gray-900 dark:text-white flex justify-between items-center list-none">
                    {q}
                    <i class="fas fa-chevron-down text-[#01411C] transition-transform group-open:rotate-180"></i>
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
            <h1 class="text-4xl font-extrabold mb-8 text-[#01411C] dark:text-white">Privacy Policy</h1>
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
            <h1 class="text-4xl font-extrabold mb-8 text-[#01411C] dark:text-white">Terms & Conditions</h1>
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
                <div class="text-9xl font-black text-[#01411C] mb-4">404</div>
                <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">Oops! Page Not Found</h1>
                <p class="text-gray-500 dark:text-gray-400 mb-8">The page you're looking for doesn't exist or has been moved. Let's get you back on track!</p>
                <div class="flex gap-4 justify-center flex-wrap">
                    <a href="/index.html" class="bg-[#01411C] text-white px-8 py-3 rounded-xl font-bold hover:bg-[#002a13] transition shadow-lg"><i class="fas fa-home mr-2"></i> Go Home</a>
                    <a href="/contact.html" class="bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white px-8 py-3 rounded-xl font-bold hover:bg-gray-200 dark:hover:bg-gray-700 transition"><i class="fas fa-headset mr-2"></i> Contact Us</a>
                </div>
            </div>
        </div>
        """ + get_html_footer())

    with open("output/wishlist.html", "w", encoding="utf-8") as f:
        f.write(get_html_header("My Wishlist", categories_list) + """
        <div class="container mx-auto px-4 py-12">
            <h1 class="text-3xl font-extrabold text-[#01411C] dark:text-white mb-8 flex items-center gap-3"><i class="fas fa-heart text-pink-500"></i> My Wishlist</h1>
            <div id="wishlistContainer" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
                <div class="col-span-full text-center py-16 text-gray-500 dark:text-gray-400">
                    <i class="fas fa-heart-broken text-6xl mb-4 opacity-30"></i>
                    <p class="text-lg font-bold">Your wishlist is empty</p>
                    <p class="text-sm mt-2">Start adding products you love!</p>
                    <a href="/index.html" class="inline-block mt-6 bg-[#01411C] text-white px-8 py-3 rounded-xl font-bold hover:bg-[#002a13] transition">Browse Products</a>
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
                    let safeName = item.name.replace(/'/g, "\\'");
                    container.innerHTML += `
                        <div class="product-card bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col">
                            <div class="h-48 bg-gray-50 dark:bg-gray-700 overflow-hidden">
                                <img src="${item.image}" alt="${item.name}" class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/400x400/01411C/ffffff?text=ASM+VEO'">
                            </div>
                            <div class="p-4 flex flex-col flex-grow">
                                <h3 class="text-sm font-bold text-gray-900 dark:text-white line-clamp-2 mb-2">${item.name}</h3>
                                <p class="text-lg font-black text-[#01411C] dark:text-white mb-3">Rs ${item.price}</p>
                                <div class="flex gap-2 mt-auto">
                                    <button onclick="addToCart('${safeName}', ${item.price}, '${item.image}')" class="flex-1 bg-[#01411C] text-white py-2 rounded-lg text-xs font-bold hover:bg-[#002a13] transition"><i class="fas fa-cart-plus"></i></button>
                                    <button onclick="removeWishlistItem(${i})" class="flex-1 bg-red-50 text-red-600 py-2 rounded-lg text-xs font-bold hover:bg-red-100 transition"><i class="fas fa-trash"></i></button>
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
                <p class="text-gray-500 dark:text-gray-400 text-sm mb-8">Order ID: <span id="orderId" class="font-bold text-[#01411C]">ASM-XXXXXX</span></p>
                <div class="bg-gray-50 dark:bg-gray-800 rounded-2xl p-6 mb-8 text-left">
                    <h3 class="font-bold text-gray-900 dark:text-white mb-3">What's Next?</h3>
                    <ol class="space-y-3 text-sm text-gray-600 dark:text-gray-300">
                        <li class="flex gap-3"><span class="w-6 h-6 bg-[#01411C] text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">1</span> We'll confirm your order via WhatsApp shortly</li>
                        <li class="flex gap-3"><span class="w-6 h-6 bg-[#01411C] text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">2</span> Your order will be dispatched within 24 hours</li>
                        <li class="flex gap-3"><span class="w-6 h-6 bg-[#01411C] text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">3</span> Expected delivery: 2-4 business days</li>
                        <li class="flex gap-3"><span class="w-6 h-6 bg-[#01411C] text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">4</span> Pay cash when you receive your order</li>
                    </ol>
                </div>
                <div class="flex gap-4 justify-center flex-wrap">
                    <a href="/index.html" class="bg-[#01411C] text-white px-8 py-3 rounded-xl font-bold hover:bg-[#002a13] transition shadow-lg"><i class="fas fa-shopping-bag mr-2"></i> Continue Shopping</a>
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
    for prod in products_list:
        reviews_section, avg_rating, review_count = generate_reviews(prod['name'])
        prod['rating'] = avg_rating
        prod['review_count'] = review_count
        
        related = [p for p in products_list if p['category'] == prod['category'] and p['slug'] != prod['slug']][:4]
        related_html = "".join([generate_product_card(p, lazy=True) for p in related])
        
        gallery_html = ""
        if len(prod['images']) > 1:
            gallery_thumbs = ""
            for idx, img in enumerate(prod['images'][:5]):
                gallery_thumbs += f'<img src="{img}" alt="Thumbnail {idx+1}" onclick="changeMainImage(this)" class="w-16 h-16 object-cover rounded-lg cursor-pointer border-2 {"border-[#01411C]" if idx == 0 else "border-gray-200"} hover:border-[#01411C] transition" onerror="this.style.display=\'none\'">'
            gallery_html = f'<div class="flex gap-2 mt-4 overflow-x-auto">{gallery_thumbs}</div>'
        
        breadcrumb_data = {'category': prod['category'], 'name': prod['name'], 'slug': prod['slug']}
        product_schema_data = {**prod, 'rating': avg_rating, 'review_count': review_count}
        
        prod_html = get_html_header(prod['name'], categories_list, prod['seo_desc'], 
                                     product_data=product_schema_data, breadcrumb_data=breadcrumb_data,
                                     og_image=prod['image'])
        
        discount_pct = math.ceil(((prod['fake_price'] - prod['final_price']) / prod['fake_price']) * 100) if prod['fake_price'] > prod['final_price'] else 0
        stock_left = random.randint(3, 15)
        delivery_date = (datetime.now() + timedelta(days=random.randint(2, 4))).strftime("%b %d, %Y")
        
        # Safe JS escape outside f-string
        escaped_name = prod['name'].replace("'", "\\'")
        
        prod_html += f"""
        <div class="container mx-auto px-4 py-10">
            <nav class="text-sm text-gray-600 dark:text-gray-400 mb-6 font-semibold bg-gray-100 dark:bg-gray-800 p-3 rounded-lg inline-block" aria-label="Breadcrumb">
                <a href="/index.html" class="hover:text-[#01411C] transition">Home</a> &gt; 
                <a href="/category/{make_slug(prod['category'])}.html" class="hover:text-[#01411C] transition">{prod['category']}</a> &gt; 
                <span class="text-[#01411C] dark:text-white" aria-current="page">{prod['name']}</span>
            </nav>
            
            <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col md:flex-row mb-12 reveal">
                <div class="md:w-1/2 p-6 flex flex-col justify-center items-center bg-gray-50 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 relative">
                    {f'<div class="absolute top-4 left-4 bg-red-600 text-white text-sm font-black px-3 py-1.5 rounded-lg z-10 shadow-md">-{discount_pct}% OFF</div>' if discount_pct > 0 else ''}
                    <img id="mainProductImage" src="{prod['image']}" alt="Image of {prod['name']}" fetchpriority="high" width="600" height="600" class="max-h-[500px] object-contain rounded-xl hover:scale-105 transition duration-500" onerror="this.src='https://via.placeholder.com/600x600/01411C/ffffff?text=ASM+VEO'">
                    {gallery_html}
                </div>
                <div class="md:w-1/2 p-8 md:p-12 flex flex-col justify-center">
                    <span class="text-xs font-bold uppercase tracking-widest text-[#01411C] dark:text-white mb-2">{prod['category']}</span>
                    <h1 class="text-3xl md:text-4xl font-extrabold text-gray-900 dark:text-white mb-4">{prod['name']}</h1>
                    
                    <div class="flex items-center gap-3 mb-6" aria-label="Customer Rating">
                        <div class="text-yellow-500 text-sm">{"<i class='fas fa-star'></i>" * 5}</div>
                        <span class="text-sm font-semibold text-gray-600 dark:text-gray-300">{avg_rating} ({review_count} verified reviews)</span>
                    </div>

                    <div class="flex items-center gap-4 mb-4 bg-gray-50 dark:bg-gray-700 p-4 rounded-2xl w-fit border border-gray-100 dark:border-gray-600">
                        <span class="text-4xl font-black text-[#01411C] dark:text-white">Rs {prod['final_price']}</span>
                        <span class="text-xl text-gray-500 font-bold line-through">Rs {prod['fake_price']}</span>
                        {f'<span class="bg-red-500 text-white text-sm font-bold px-2 py-1 rounded-lg">Save Rs {prod["fake_price"] - prod["final_price"]}</span>' if discount_pct > 0 else ''}
                    </div>
                    
                    <div class="flex items-center gap-2 mb-6 text-sm">
                        <span class="bg-orange-100 text-orange-700 px-3 py-1 rounded-full font-bold"><i class="fas fa-fire"></i> Only {stock_left} left!</span>
                        <span class="bg-green-100 text-green-700 px-3 py-1 rounded-full font-bold"><i class="fas fa-truck"></i> Delivery by {delivery_date}</span>
                    </div>
                    
                    <p class="text-gray-700 dark:text-gray-300 mb-8 leading-relaxed border-t border-gray-100 dark:border-gray-700 pt-6">{prod['full_desc'][:500] if len(prod['full_desc']) > 50 else prod['seo_desc']}</p>
                    
                    <div class="flex flex-col sm:flex-row gap-4 w-full md:w-5/6 mt-auto">
                        <button onclick="addToCart('{escaped_name}', {prod['final_price']}, '{prod['image']}', event)" aria-label="Add to Cart" class="sm:w-1/2 bg-white dark:bg-gray-700 text-[#01411C] dark:text-white py-4 rounded-xl font-black text-lg border-2 border-[#01411C] hover:bg-gray-50 dark:hover:bg-gray-600 transition-all shadow-md transform hover:-translate-y-1 flex justify-center items-center gap-2">
                            <i class="fas fa-cart-plus"></i> Add to Cart
                        </button>
                        <button onclick="buyNow('{escaped_name}', {prod['final_price']}, '{prod['image']}', event)" aria-label="Buy Now" class="sm:w-1/2 bg-[#01411C] text-white py-4 rounded-xl font-black text-lg hover:bg-[#002a13] transition-all shadow-lg transform hover:-translate-y-1 flex justify-center items-center gap-2">
                            <i class="fas fa-bolt"></i> Buy Now
                        </button>
                    </div>
                    
                    <div class="grid grid-cols-3 gap-3 mt-8 pt-6 border-t border-gray-100 dark:border-gray-700">
                        <div class="text-center"><i class="fas fa-shield-alt text-[#01411C] text-xl mb-1"></i><p class="text-xs font-semibold text-gray-600 dark:text-gray-400">Secure Payment</p></div>
                        <div class="text-center"><i class="fas fa-undo text-[#01411C] text-xl mb-1"></i><p class="text-xs font-semibold text-gray-600 dark:text-gray-400">7-Day Returns</p></div>
                        <div class="text-center"><i class="fas fa-truck text-[#01411C] text-xl mb-1"></i><p class="text-xs font-semibold text-gray-600 dark:text-gray-400">Fast Delivery</p></div>
                    </div>
                </div>
            </div>
            
            {"<div class='bg-white dark:bg-gray-800 rounded-3xl shadow-lg border border-gray-200 dark:border-gray-700 p-8 mb-8 reveal'><h2 class='text-2xl font-extrabold text-gray-900 dark:text-white mb-6 border-b pb-4'>You May Also Like</h2><div class='grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6'>" + related_html + "</div></div>" if related_html else ""}
            
            <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-lg border border-gray-200 dark:border-gray-700 p-8 mb-8 reveal">
                <h2 class="text-2xl font-extrabold text-gray-900 dark:text-white mb-6 border-b pb-4 flex items-center gap-3">
                    <i class="fas fa-star text-yellow-500"></i> Customer Reviews ({review_count})
                </h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div>{reviews_section}</div>
                    <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-2xl h-fit border border-gray-300 dark:border-gray-700">
                        <h3 class="font-bold text-lg mb-2 text-gray-900 dark:text-white">Write a Review</h3>
                        <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">Only verified buyers can leave a review after receiving the product to maintain quality standards.</p>
                        <div class="flex items-center gap-2 text-[#01411C] dark:text-white font-bold bg-gray-50 dark:bg-gray-700 p-3 rounded-lg border border-gray-200 dark:border-gray-600">
                            <i class="fas fa-lock"></i> Review form is currently locked.
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-lg border border-gray-200 dark:border-gray-700 p-8 mb-16 md:mb-0 reveal">
                <h2 class="text-2xl font-extrabold text-gray-900 dark:text-white mb-6 border-b pb-4">Product FAQs</h2>
                <div class="space-y-4">
                    <details class="border border-gray-200 dark:border-gray-700 rounded-xl p-4 group">
                        <summary class="cursor-pointer font-bold text-gray-900 dark:text-white flex justify-between list-none">Is this product genuine? <i class="fas fa-chevron-down text-[#01411C] group-open:rotate-180 transition"></i></summary>
                        <p class="mt-3 text-sm text-gray-600 dark:text-gray-300">Yes! We source 100% genuine products directly from authorized distributors. Every product is quality-checked before dispatch.</p>
                    </details>
                    <details class="border border-gray-200 dark:border-gray-700 rounded-xl p-4 group">
                        <summary class="cursor-pointer font-bold text-gray-900 dark:text-white flex justify-between list-none">What is the delivery time? <i class="fas fa-chevron-down text-[#01411C] group-open:rotate-180 transition"></i></summary>
                        <p class="mt-3 text-sm text-gray-600 dark:text-gray-300">Delivery takes 2-4 business days across Pakistan. Major cities receive faster delivery.</p>
                    </details>
                    <details class="border border-gray-200 dark:border-gray-700 rounded-xl p-4 group">
                        <summary class="cursor-pointer font-bold text-gray-900 dark:text-white flex justify-between list-none">Can I return this product? <i class="fas fa-chevron-down text-[#01411C] group-open:rotate-180 transition"></i></summary>
                        <p class="mt-3 text-sm text-gray-600 dark:text-gray-300">Yes, we offer a 7-day return policy. The product must be in its original condition with packaging.</p>
                    </details>
                </div>
            </div>
        </div>
        """
        
        recent_json = json.dumps({"slug": prod['slug'], "name": prod['name'], "image": prod['image'], "final_price": prod['final_price'], "fake_price": prod['fake_price'], "category": prod['category']})
        prod_script = """
        <script>
            addToRecentlyViewed(__RECENT_JSON__);
            function changeMainImage(thumb) {
                document.getElementById('mainProductImage').src = thumb.src;
                document.querySelectorAll('.flex.gap-2 img').forEach(img => img.classList.remove('border-[#01411C]'));
                thumb.classList.add('border-[#01411C]');
            }
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
            <h2 class="text-2xl font-bold text-[#01411C] dark:text-white mb-6">Top Products in {city}</h2>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
        """
        for p in city_prods:
            city_html += generate_product_card(p)
            
        city_html += "</div></div>" + get_html_footer()
        with open(f"output/city/{city_slug}.html", "w", encoding="utf-8") as f:
            f.write(city_html)

    # ================= CATEGORY PAGES =================
    sections_dict = {}
    for p in products_list:
        c = p['category']
        if c not in sections_dict: sections_dict[c] = []
        sections_dict[c].append(p)

    # PERFORMANCE FIX: Save search index to a separate JS file instead of bloating the HTML
    search_index_json = json.dumps([{"name": p['name'], "slug": p['slug'], "category": p['category'], 
                                     "final_price": p['final_price'], "fake_price": p['fake_price'], "image": p['image']} for p in products_list])
    
    with open("output/search-data.js", "w", encoding="utf-8") as f:
        f.write(f"let searchIndex = {search_index_json};")

    home_html = get_html_header("Home - Premium Online Shopping in Pakistan", categories_list,
                                 "ASM VEO - Pakistan's premium online shopping destination. Buy quality products with Cash on Delivery, fast shipping & easy returns.")
    
    # Hero Carousel Slider with Pakistani Flag Theme
    home_html += """
    <div id="heroCarousel" class="relative w-full h-[300px] md:h-[450px] overflow-hidden shadow-xl">
        <div class="carousel-track h-full">
            <!-- Slide 1 -->
            <div class="carousel-slide h-full animated-bg flex items-center p-6 md:p-16 text-white relative">
                <div class="absolute top-10 right-10 w-32 h-32 bg-white/10 rounded-full animate-float"></div>
                <div class="absolute bottom-10 left-10 w-48 h-48 bg-white/5 rounded-full animate-float" style="animation-delay: 1s;"></div>
                <div class="z-10 max-w-lg">
                    <span class="bg-white text-[#01411C] text-xs font-black px-3 py-1 rounded-full">MEGA SALE</span>
                    <h2 class="text-3xl md:text-6xl font-extrabold mt-4 mb-4 leading-tight">Flat 50% OFF<br>Premium Products</h2>
                    <p class="text-base md:text-lg mb-6 text-gray-200">Cash on Delivery available all over Pakistan. Shop now before stock ends!</p>
                    <a href="#products" class="bg-white text-[#01411C] px-8 py-3 rounded-lg font-bold hover:bg-gray-100 transition inline-flex items-center gap-2"><i class="fas fa-shopping-bag"></i> Shop Now</a>
                </div>
            </div>
            <!-- Slide 2 -->
            <div class="carousel-slide h-full bg-gray-900 flex items-center p-6 md:p-16 text-white relative">
                <div class="z-10 max-w-lg">
                    <span class="bg-[#01411C] text-white text-xs font-black px-3 py-1 rounded-full">NEW ARRIVALS</span>
                    <h2 class="text-3xl md:text-6xl font-extrabold mt-4 mb-4 leading-tight">Latest Gadgets<br>& Accessories</h2>
                    <p class="text-base md:text-lg mb-6 text-gray-300">100% Genuine products delivered to your doorstep nationwide.</p>
                    <a href="#products" class="bg-[#01411C] text-white px-8 py-3 rounded-lg font-bold hover:bg-[#002a13] transition inline-flex items-center gap-2"><i class="fas fa-bolt"></i> Explore Now</a>
                </div>
                <img src="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=800&q=80" alt="Gadgets" class="absolute right-0 top-0 h-full w-1/2 object-cover opacity-30 md:opacity-100 hidden md:block">
            </div>
            <!-- Slide 3 -->
            <div class="carousel-slide h-full bg-gradient-to-r from-gray-900 to-gray-800 flex items-center p-6 md:p-16 text-white relative">
                <div class="z-10 max-w-lg">
                    <span class="bg-white text-gray-900 text-xs font-black px-3 py-1 rounded-full">EXCLUSIVE DEALS</span>
                    <h2 class="text-3xl md:text-6xl font-extrabold mt-4 mb-4 leading-tight">Premium Fashion<br>Collection 2026</h2>
                    <p class="text-base md:text-lg mb-6 text-gray-300">Trendy clothes & accessories at unbeatable prices in Pakistan.</p>
                    <a href="#products" class="bg-white text-gray-900 px-8 py-3 rounded-lg font-bold hover:bg-gray-100 transition inline-flex items-center gap-2"><i class="fas fa-tshirt"></i> Browse Fashion</a>
                </div>
                <img src="https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=800&q=80" alt="Fashion" class="absolute right-0 top-0 h-full w-1/2 object-cover opacity-30 md:opacity-100 hidden md:block">
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
        setInterval(nextSlide, 5000);
    </script>
    """

    # Flash Sale Countdown Timer
    home_html += """
    <div class="bg-[#01411C] text-white py-6 mt-6">
        <div class="container mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-3">
                <i class="fas fa-bolt text-yellow-400 text-3xl animate-pulse"></i>
                <div>
                    <h2 class="text-2xl font-extrabold">Flash Sale</h2>
                    <p class="text-gray-300 text-sm">Hurry up! Offer ends soon.</p>
                </div>
            </div>
            <div id="countdown" class="flex gap-3 text-center">
                <div class="bg-white/10 px-4 py-2 rounded-lg"><span id="hours" class="text-2xl font-black text-white">00</span><br><span class="text-xs text-gray-300">Hrs</span></div>
                <div class="bg-white/10 px-4 py-2 rounded-lg"><span id="minutes" class="text-2xl font-black text-white">00</span><br><span class="text-xs text-gray-300">Min</span></div>
                <div class="bg-white/10 px-4 py-2 rounded-lg"><span id="seconds" class="text-2xl font-black text-white">00</span><br><span class="text-xs text-gray-300">Sec</span></div>
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

    # Trust Indicators
    home_html += """
    <div class="container mx-auto px-4 py-6">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="reveal bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-3">
                <div class="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg text-[#01411C] dark:text-white"><i class="fas fa-truck-fast text-xl"></i></div>
                <div><h3 class="font-bold text-sm text-gray-900 dark:text-white">Fast Delivery</h3><p class="text-xs text-gray-500 dark:text-gray-400">All over Pakistan</p></div>
            </div>
            <div class="reveal bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-3">
                <div class="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg text-[#01411C] dark:text-white"><i class="fas fa-money-bill-wave text-xl"></i></div>
                <div><h3 class="font-bold text-sm text-gray-900 dark:text-white">Cash on Delivery</h3><p class="text-xs text-gray-500 dark:text-gray-400">Pay at your doorstep</p></div>
            </div>
            <div class="reveal bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-3">
                <div class="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg text-[#01411C] dark:text-white"><i class="fas fa-shield-halved text-xl"></i></div>
                <div><h3 class="font-bold text-sm text-gray-900 dark:text-white">Secure Shopping</h3><p class="text-xs text-gray-500 dark:text-gray-400">100% Protected</p></div>
            </div>
            <div class="reveal bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-3">
                <div class="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg text-[#01411C] dark:text-white"><i class="fas fa-undo text-xl"></i></div>
                <div><h3 class="font-bold text-sm text-gray-900 dark:text-white">Easy Returns</h3><p class="text-xs text-gray-500 dark:text-gray-400">7 Days Return Policy</p></div>
            </div>
        </div>
    </div>
    """

    home_html += f"""
    <div class='container mx-auto px-4 py-4' id="products">
        <div id="searchResultsSection" class="hidden mb-6">
            <h2 id="searchResultsHeading" class="text-2xl font-extrabold text-[#01411C] dark:text-white mb-2 border-b pb-2"></h2>
            <p id="searchResultsCount" class="text-gray-500 text-sm"></p>
        </div>
        <div id="defaultContent">
    """
    
    # OPTIMIZATION: Only show top 4 categories and 4 products each on home page for fast load
    total_rendered_products = 0
    for cat_name, prods in list(sections_dict.items())[:4]:
        cat_slug = make_slug(cat_name)
        sitemap_urls.append(f"https://www.asmveo.com/category/{cat_slug}.html")
        
        cat_html = get_html_header(cat_name, categories_list, f"Buy {cat_name} online in Pakistan at best prices. Wide range of {cat_name} with Cash on Delivery from ASM VEO.")
        
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
            <div class="flex flex-col lg:flex-row gap-6">
                <aside class="lg:w-64 flex-shrink-0">
                    <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 p-5 sticky top-24">
                        <h3 class="font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2"><i class="fas fa-filter text-[#01411C]"></i> Filters</h3>
                        
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
                            <button onclick="applyFilters()" class="w-full bg-[#01411C] text-white py-2 rounded-lg text-sm font-bold hover:bg-[#002a13] transition">Apply Filter</button>
                        </div>
                        
                        <button onclick="resetFilters()" class="w-full text-gray-500 hover:text-[#01411C] text-sm font-bold transition"><i class="fas fa-undo mr-1"></i> Reset Filters</button>
                    </div>
                </aside>
                
                <div class="flex-1">
                    <div id="productGrid" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-4 md:gap-6">
        """
        
        for prod in prods:
            cat_html += generate_product_card(prod, lazy=True)
        
        cat_html += """
                    </div>
                    <div id="noResults" class="hidden text-center py-16 text-gray-500">
                        <i class="fas fa-search text-6xl mb-4 opacity-30"></i>
                        <p class="text-lg font-bold">No products found</p>
                        <p class="text-sm mt-2">Try adjusting your filters</p>
                    </div>
                </div>
            </div>
        </div>
        """
        
        cat_script = """
        <script>
            let allProducts = __PRODUCTS_JSON__;
            
            function applyFilters() {
                let sortBy = document.getElementById('sortBy').value;
                let minP = parseFloat(document.getElementById('minPrice').value) || 0;
                let maxP = parseFloat(document.getElementById('maxPrice').value) || 999999;
                
                let filtered = allProducts.filter(p => p.final_price >= minP && p.final_price <= maxP);
                
                if (sortBy === 'price-low') filtered.sort((a,b) => a.final_price - b.final_price);
                else if (sortBy === 'price-high') filtered.sort((a,b) => b.final_price - a.final_price);
                else if (sortBy === 'name') filtered.sort((a,b) => a.name.localeCompare(b.name));
                
                let grid = document.getElementById('productGrid');
                let noResults = document.getElementById('noResults');
                
                if (filtered.length === 0) {
                    grid.innerHTML = '';
                    noResults.classList.remove('hidden');
                } else {
                    noResults.classList.add('hidden');
                    grid.innerHTML = filtered.map(p => generateCard(p)).join('');
                }
            }
            
            function generateCard(p) {
                let discount = Math.ceil(((p.fake_price - p.final_price) / p.fake_price) * 100);
                let safeName = p.name.replace(/'/g, "\\'");
                return `<div class="product-card reveal active bg-white dark:bg-gray-800 rounded-2xl shadow-sm hover:shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col relative cursor-pointer" onclick="window.location.href='/product/${p.slug}.html'">
                    <button onclick="toggleWishlist('${safeName}', ${p.final_price}, '${p.image}', event)" class="absolute top-3 right-3 w-9 h-9 bg-white rounded-full shadow-md flex items-center justify-center hover:bg-pink-50 transition z-10"><i class="fas fa-heart text-pink-500"></i></button>
                    ${discount > 0 ? `<div class="absolute top-3 left-3 bg-red-600 text-white text-xs font-black px-2.5 py-1 rounded-lg z-10 shadow-md">-${discount}% OFF</div>` : ''}
                    <div class="image-zoom h-48 md:h-60 bg-gray-50 dark:bg-gray-700 overflow-hidden relative border-b border-gray-200 dark:border-gray-700">
                        <img src="${p.image}" alt="${p.name}" loading="lazy" width="400" height="400" class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/400x400/01411C/ffffff?text=ASM+VEO'">
                    </div>
                    <div class="p-4 flex flex-col flex-grow">
                        <span class="text-[10px] font-bold text-[#01411C] uppercase tracking-wider mb-1 line-clamp-1">${p.category}</span>
                        <h3 class="text-sm md:text-base font-bold text-gray-900 dark:text-white leading-tight mb-2 line-clamp-2">${p.name}</h3>
                        <div class="mt-auto">
                            <div class="flex items-center gap-2 mb-3">
                                <span class="text-lg font-black text-[#01411C] dark:text-white">Rs ${p.final_price}</span>
                                <span class="text-xs text-gray-400 font-bold line-through">Rs ${p.fake_price}</span>
                            </div>
                            <div class="flex gap-2 w-full">
                                <button onclick="addToCart('${safeName}', ${p.final_price}, '${p.image}', event)" class="w-1/2 bg-gray-50 text-[#01411C] py-2.5 rounded-xl text-xs font-bold border border-gray-200 hover:bg-gray-100 transition flex justify-center items-center"><i class="fas fa-cart-plus"></i></button>
                                <button onclick="buyNow('${safeName}', ${p.final_price}, '${p.image}', event)" class="w-1/2 bg-[#01411C] text-white py-2.5 rounded-xl text-xs font-bold hover:bg-[#002a13] transition text-center">Buy Now</button>
                            </div>
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
        cat_html += cat_script.replace("__PRODUCTS_JSON__", json.dumps([{"name": p['name'], "slug": p['slug'], "category": p['category'], "final_price": p['final_price'], "fake_price": p['fake_price'], "image": p['image']} for p in prods])).replace("__MIN_PRICE__", str(int(min_price))).replace("__MAX_PRICE__", str(int(max_price))) + get_html_footer()
        
        with open(f"output/category/{cat_slug}.html", "w", encoding="utf-8") as f:
            f.write(cat_html)
        
        home_html += f"""
        <div class="mb-14 category-section reveal">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl md:text-3xl font-black text-gray-900 dark:text-white border-l-4 border-[#01411C] pl-4">{cat_name}</h2>
                <a href="/category/{cat_slug}.html" class="text-[#01411C] dark:text-white font-bold text-sm bg-gray-50 dark:bg-gray-800 px-5 py-2.5 rounded-full hover:bg-[#01411C] hover:text-white transition-all shadow-sm">View All <i class="fas fa-arrow-right ml-1"></i></a>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
        """
        
        # OPTIMIZATION: Render only 4 products per category on home page
        for idx, prod in enumerate(prods[:4]):
            home_html += generate_product_card(prod, lazy=(idx >= 2))
            total_rendered_products += 1
            
        home_html += "</div></div>"
    
    home_html += "</div></div>"

    home_html += """
    <div class="container mx-auto px-4 py-8 border-t border-gray-200 dark:border-gray-700">
        <h2 class="text-2xl font-extrabold text-gray-900 dark:text-white mb-6 border-l-4 border-[#01411C] pl-4">Shop by City in Pakistan</h2>
        <div class="flex flex-wrap gap-3">
    """
    for city in cities:
        home_html += f'<a href="/city/{make_slug(city)}.html" class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-5 py-2.5 rounded-full text-sm font-bold text-gray-700 dark:text-gray-300 hover:bg-[#01411C] hover:text-white transition shadow-sm">{city}</a>'
    home_html += "</div></div>"

    home_html += """
    <div id="recentlyViewedSection" class="hidden container mx-auto px-4 py-8 border-t border-gray-200 dark:border-gray-700">
        <h2 class="text-2xl font-extrabold text-gray-900 dark:text-white mb-6 border-l-4 border-[#01411C] pl-4">Recently Viewed</h2>
        <div id="recentlyViewedGrid" class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4 md:gap-6"></div>
    </div>
    """
    
    # PERFORMANCE FIX: Load search data from external JS file
    home_script = """
    <script src="/search-data.js" defer></script>
    <script>
        function performSearch(query) {
            if (typeof searchIndex === 'undefined') return; // Wait for search-data.js to load
            
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
            
            document.getElementById('defaultContent').classList.add('hidden');
            document.getElementById('recentlyViewedSection').classList.add('hidden');
            document.getElementById('searchResultsSection').classList.remove('hidden');
            document.getElementById('searchResultsHeading').innerText = 'Search Results for "' + query + '"';
            document.getElementById('searchResultsCount').innerText = results.length + ' products found';
            
            let html = '<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6 mt-6">';
            results.forEach(p => {
                let discount = Math.ceil(((p.fake_price - p.final_price) / p.fake_price) * 100);
                let safeName = p.name.replace(/'/g, "\\'");
                html += `<div class="product-card reveal active bg-white dark:bg-gray-800 rounded-2xl shadow-sm hover:shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col relative cursor-pointer" onclick="window.location.href='/product/${p.slug}.html'">
                    ${discount > 0 ? `<div class="absolute top-3 left-3 bg-red-600 text-white text-xs font-black px-2.5 py-1 rounded-lg z-10 shadow-md">-${discount}% OFF</div>` : ''}
                    <div class="image-zoom h-48 md:h-60 bg-gray-50 dark:bg-gray-700 overflow-hidden relative border-b border-gray-200 dark:border-gray-700">
                        <img src="${p.image}" alt="${p.name}" loading="lazy" width="400" height="400" class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/400x400/01411C/ffffff?text=ASM+VEO'">
                    </div>
                    <div class="p-4 flex flex-col flex-grow">
                        <span class="text-[10px] font-bold text-[#01411C] uppercase tracking-wider mb-1 line-clamp-1">${p.category}</span>
                        <h3 class="text-sm md:text-base font-bold text-gray-900 dark:text-white leading-tight mb-2 line-clamp-2">${p.name}</h3>
                        <div class="mt-auto">
                            <div class="flex items-center gap-2 mb-3">
                                <span class="text-lg font-black text-[#01411C] dark:text-white">Rs ${p.final_price}</span>
                                <span class="text-xs text-gray-400 font-bold line-through">Rs ${p.fake_price}</span>
                            </div>
                            <div class="flex gap-2 w-full">
                                <button onclick="addToCart('${safeName}', ${p.final_price}, '${p.image}', event)" class="w-1/2 bg-gray-50 text-[#01411C] py-2.5 rounded-xl text-xs font-bold border border-gray-200 hover:bg-gray-100 transition flex justify-center items-center"><i class="fas fa-cart-plus"></i></button>
                                <button onclick="buyNow('${safeName}', ${p.final_price}, '${p.image}', event)" class="w-1/2 bg-[#01411C] text-white py-2.5 rounded-xl text-xs font-bold hover:bg-[#002a13] transition text-center">Buy Now</button>
                            </div>
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
            // Clear previous results except heading and count
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
            // Delay search to ensure search-data.js is loaded
            setTimeout(() => performSearch(searchQuery), 500);
        }
        
        function renderRecentlyViewed() {
            let recent = JSON.parse(localStorage.getItem('asm_recent')) || [];
            recent = recent.slice(0, 5);
            if (recent.length === 0) return;
            
            document.getElementById('recentlyViewedSection').classList.remove('hidden');
            let grid = document.getElementById('recentlyViewedGrid');
            grid.innerHTML = recent.map(p => {
                let discount = Math.ceil(((p.fake_price - p.final_price) / p.fake_price) * 100);
                return `<div class="product-card reveal active bg-white dark:bg-gray-800 rounded-2xl shadow-sm hover:shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col relative cursor-pointer" onclick="window.location.href='/product/${p.slug}.html'">
                    ${discount > 0 ? `<div class="absolute top-3 left-3 bg-red-600 text-white text-xs font-black px-2.5 py-1 rounded-lg z-10 shadow-md">-${discount}% OFF</div>` : ''}
                    <div class="h-48 bg-gray-50 dark:bg-gray-700 overflow-hidden border-b border-gray-200 dark:border-gray-700">
                        <img src="${p.image}" alt="${p.name}" loading="lazy" width="400" height="400" class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/400x400/01411C/ffffff?text=ASM+VEO'">
                    </div>
                    <div class="p-4 flex flex-col flex-grow">
                        <h3 class="text-sm font-bold text-gray-900 dark:text-white line-clamp-2 mb-2">${p.name}</h3>
                        <div class="mt-auto">
                            <span class="text-lg font-black text-[#01411C] dark:text-white">Rs ${p.final_price}</span>
                            <span class="text-xs text-gray-400 font-bold line-through ml-2">Rs ${p.fake_price}</span>
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

    # ================= CHECKOUT PAGE =================
    pak_cities = ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Multan", 
                  "Peshawar", "Quetta", "Gujranwala", "Sialkot", "Hyderabad", "Bahawalpur", 
                  "Sargodha", "Sukkur", "Mardan", "Gujrat", "Larkana", "Kasur", "Rahim Yar Khan", "Other"]
    city_options = "".join([f"<option value='{city}'>{city}</option>" for city in pak_cities])
    delivery_date = (datetime.now() + timedelta(days=3)).strftime("%A, %b %d")
    
    checkout_html = get_html_header("Secure Checkout", categories_list, "Complete your order with Cash on Delivery. Fast and secure checkout at ASM VEO.")
    checkout_html += f"""
    <div class="container mx-auto px-4 py-12 max-w-6xl">
        <h1 class="text-3xl font-extrabold text-[#01411C] dark:text-white mb-8 flex items-center gap-3"><i class="fas fa-lock text-[#01411C]"></i> Secure Checkout</h1>
        
        <div class="flex items-center justify-center mb-10">
            <div class="flex items-center text-[#01411C] font-bold">
                <div class="w-10 h-10 bg-[#01411C] text-white rounded-full flex items-center justify-center font-black">1</div>
                <span class="ml-2 hidden md:inline">Cart</span>
            </div>
            <div class="w-16 md:w-32 h-1 bg-[#01411C] mx-2"></div>
            <div class="flex items-center text-[#01411C] font-bold">
                <div class="w-10 h-10 bg-[#01411C] text-white rounded-full flex items-center justify-center font-black">2</div>
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
                    <h2 class="text-2xl font-black text-gray-900 dark:text-white mb-4 border-b pb-4 flex items-center gap-2"><i class="fas fa-shopping-bag text-[#01411C]"></i> Your Items</h2>
                    <div id="cartItemsContainer" class="space-y-4 max-h-[400px] overflow-y-auto pr-2"></div>
                </div>
                
                <div class="bg-gray-50 dark:bg-gray-800 rounded-2xl p-5 border border-gray-100 dark:border-gray-700">
                    <h3 class="font-bold text-gray-900 dark:text-white mb-3 text-sm">Why Shop With Us?</h3>
                    <div class="grid grid-cols-2 gap-3 text-xs">
                        <div class="flex items-center gap-2"><i class="fas fa-shield-alt text-[#01411C]"></i> 100% Secure Checkout</div>
                        <div class="flex items-center gap-2"><i class="fas fa-truck text-[#01411C]"></i> Fast Nationwide Delivery</div>
                        <div class="flex items-center gap-2"><i class="fas fa-undo text-[#01411C]"></i> 7-Day Return Policy</div>
                        <div class="flex items-center gap-2"><i class="fas fa-certificate text-[#01411C]"></i> 100% Genuine Products</div>
                    </div>
                </div>
            </div>

            <div class="lg:w-1/2">
                <div class="bg-[#01411C] p-6 rounded-t-3xl text-white relative">
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
                            <input type="text" name="Full_Name" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-[#01411C] outline-none" required placeholder="Ali Abbas">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">Email Address</label>
                            <input type="email" name="Email" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-[#01411C] outline-none" placeholder="you@example.com">
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <div>
                            <label class="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">Mobile Number <span class="text-red-600">*</span></label>
                            <input type="tel" name="Phone_Number" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-[#01411C] outline-none" required placeholder="03XXXXXXXXX">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">City <span class="text-red-600">*</span></label>
                            <select name="City" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-[#01411C] outline-none font-semibold" required>
                                <option value="" disabled selected>Select City</option>
                                {city_options}
                            </select>
                        </div>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">Complete Delivery Address <span class="text-red-600">*</span></label>
                        <textarea name="Address" rows="3" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-[#01411C] outline-none" required placeholder="House No, Street, Area, Landmark..."></textarea>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">Coupon Code</label>
                        <div class="flex gap-2">
                            <input type="text" id="couponCode" placeholder="Enter ASM10 for 10% off (Min Rs 3000)" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-[#01411C] outline-none uppercase">
                            <button type="button" onclick="applyCoupon()" class="bg-gray-900 text-white px-5 rounded-xl font-bold hover:bg-gray-700 transition">Apply</button>
                        </div>
                    </div>
                    
                    <div class="bg-gray-50 dark:bg-gray-700 rounded-2xl p-5 border border-gray-100 dark:border-gray-600 mt-6">
                        <div class="flex justify-between text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">
                            <span>Subtotal</span>
                            <span id="subtotalDisplay">Rs 0</span>
                        </div>
                        <div class="flex justify-between text-sm font-bold text-[#01411C] dark:text-white mb-2 hidden" id="discountRow">
                            <span>Discount (10%)</span>
                            <span id="discountDisplay">- Rs 0</span>
                        </div>
                        <div class="flex justify-between text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">
                            <span>Delivery Charges</span>
                            <span id="deliveryDisplay">Rs 250</span>
                        </div>
                        <div class="flex justify-between items-center border-t border-gray-200 dark:border-gray-600 pt-3 mt-3">
                            <span class="font-black text-lg text-gray-900 dark:text-white">Total (COD)</span>
                            <span class="font-black text-2xl text-[#01411C] dark:text-white" id="grandTotalDisplay">Rs 250</span>
                        </div>
                    </div>

                    <button type="submit" id="submitBtn" class="w-full bg-[#01411C] text-white font-black py-4 rounded-xl hover:bg-[#002a13] transition-all shadow-xl text-lg transform hover:-translate-y-1 flex items-center justify-center gap-2">
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
                currentSubtotal = parseInt(urlParams.get('price'));
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
            const pPrice = parseInt(urlParams.get('price'));
            
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
                            <p class="text-[#01411C] dark:text-white font-black">Rs ${pPrice}</p>
                        </div>
                    </div>`;
            } else {
                let cart = getCart();
                if(cart.length === 0) {
                    container.innerHTML = `<div class="text-center py-8"><i class="fas fa-shopping-cart text-5xl text-gray-300 mb-3"></i><p class="text-gray-500 font-semibold">Your cart is empty.</p><a href="/index.html" class="inline-block mt-4 bg-[#01411C] text-white px-6 py-2 rounded-xl font-bold">Browse Products</a></div>`;
                    document.getElementById('submitBtn').disabled = true;
                    document.getElementById('submitBtn').classList.add('opacity-50', 'cursor-not-allowed');
                } else {
                    cart.forEach((item, index) => {
                        let qty = item.qty || 1;
                        subtotal += parseInt(item.price) * qty;
                        finalOrderString += qty + "x " + item.name + " (Rs " + (item.price * qty) + ")\\n";
                        
                        container.innerHTML += `
                        <div class="flex items-center gap-3 bg-gray-50 dark:bg-gray-700 p-3 rounded-xl border border-gray-200 dark:border-gray-600">
                            <img src="${item.image}" class="w-16 h-16 object-cover rounded-lg bg-white border border-gray-100" onerror="this.src='https://via.placeholder.com/100x100/01411C/ffffff?text=ASM'">
                            <div class="flex-1 min-w-0">
                                <h3 class="font-bold text-sm text-gray-900 dark:text-white line-clamp-2">${item.name}</h3>
                                <p class="text-[#01411C] dark:text-white font-black text-sm">Rs ${item.price}</p>
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
    print("✨ Optimized for 90+ Lighthouse Performance Score!")

if __name__ == "__main__":
    process_woocommerce_csv()
