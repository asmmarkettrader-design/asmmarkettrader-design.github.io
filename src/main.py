import os
import csv
import math
import re
import shutil
import random
import json
from datetime import datetime, timedelta

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
    names = ["Ali Raza", "Ayesha Khan", "Usman Tariq", "Fatima Noor", "Bilal Ahmed", 
             "Zainab Ali", "Hassan Raza", "Maryam S.", "Ahmad Malik", "Sana Javed", 
             "Zohaib Hassan", "Iqra Baig", "Hamza Sheikh", "Anum Khalid"]
    
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
        reviewer = random.choice(names)
        comment = random.choice(templates).format(name=product_name)
        stars = random.randint(4, 5)
        days_ago = random.randint(1, 60)
        
        reviews_html += f"""
        <div class="border-b border-gray-100 dark:border-gray-700 py-4 last:border-0">
            <div class="flex items-center gap-2 mb-2">
                <div class="w-9 h-9 rounded-full bg-gradient-to-br from-emerald-400 to-emerald-700 text-white flex items-center justify-center font-bold text-sm" aria-hidden="true">{reviewer[0]}</div>
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
                    product_data=None, breadcrumb_data=None, og_image=None, global_search_json="[]"):
    
    cat_links = ""
    for cat in categories_list:
        c_slug = make_slug(cat)
        cat_links += f'<a href="/category/{c_slug}.html" class="block px-4 py-2.5 text-sm text-gray-700 hover:bg-emerald-50 hover:text-emerald-700 transition-colors">{cat}</a>\n'

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
    
    <!-- Local Pakistan SEO -->
    <meta name="title" content="{title} | Buy Online in Pakistan | ASM VEO">
    <meta name="description" content="Buy {title} online in Pakistan at best price. Cash on Delivery available all over Pakistan. Shop premium quality products with fast shipping & easy returns at ASM VEO.">
    <meta name="keywords" content="buy {title} in Pakistan, {title} price in Pakistan, online shopping Pakistan, cash on delivery, ASM VEO, best online store Pakistan, Karachi, Lahore, Islamabad">
    <meta name="author" content="ASM Digital Solutions">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta name="theme-color" content="#047857">
    <link rel="canonical" href="https://www.asmveo.com/">
    
    <!-- Geo Tags for Local SEO -->
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
                    colors: {{ brand: {{ 50: '#ecfdf5', 500: '#10b981', 600: '#059669', 700: '#047857', 800: '#065f46', 900: '#064e3b' }} }}
                }}
            }}
        }}
    </script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; transition: background-color 0.3s; padding-bottom: 70px; md:padding-bottom: 0; }}
        .dark body {{ background-color: #0f172a; color: #e2e8f0; }}
        .product-card {{ transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }}
        .product-card:hover {{ transform: translateY(-8px); box-shadow: 0 20px 40px -10px rgba(0,0,0,0.15); }}
        .image-zoom img {{ transition: transform 0.5s ease; }}
        .product-card:hover .image-zoom img {{ transform: scale(1.1); }}
        .dropdown:hover .dropdown-menu {{ display: block; }}
        
        ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
        ::-webkit-scrollbar-track {{ background: #f1f5f9; }}
        ::-webkit-scrollbar-thumb {{ background: #047857; border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #065f46; }}
        
        .skeleton {{ background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; }}
        @keyframes shimmer {{ 0% {{ background-position: 200% 0; }} 100% {{ background-position: -200% 0; }} }}
        
        .line-clamp-1 {{ display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden; }}
        .line-clamp-2 {{ display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
        .line-clamp-3 {{ display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
        
        @keyframes slideIn {{ from {{ transform: translateY(20px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}
        .slide-in {{ animation: slideIn 0.4s ease-out; }}
        
        .carousel-track {{ display: flex; transition: transform 0.8s cubic-bezier(0.65, 0, 0.35, 1); }}
        .carousel-slide {{ min-width: 100%; box-sizing: border-box; }}
        
        .glass {{ background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); }}
        .dark .glass {{ background: rgba(15, 23, 42, 0.85); }}
        
        /* Advanced Search Suggestion Scrollbar */
        #searchSuggestions::-webkit-scrollbar {{ width: 6px; }}
        #searchSuggestions::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 10px; }}
        
        /* Magnifier Effect */
        .zoom-magnifier {{ overflow: hidden; cursor: crosshair; }}
        .zoom-magnifier img {{ transition: transform 0.1s ease; }}
    </style>
    {structured_data}

    <script>
        // GLOBAL DATA FOR AUTO-SUGGEST
        window.GLOBAL_SEARCH_INDEX = {global_search_json};

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
            showToast('Added to Cart!', 'fa-cart-plus', 'emerald');
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

        // RECENTLY VIEWED
        function addToRecentlyViewed(product) {{
            let recent = JSON.parse(localStorage.getItem('asm_recent')) || [];
            recent = recent.filter(p => p.slug !== product.slug);
            recent.unshift(product);
            recent = recent.slice(0, 10);
            localStorage.setItem('asm_recent', JSON.stringify(recent));
        }}

        // TOAST NOTIFICATIONS
        function showToast(msg, icon='fa-check-circle', color='emerald') {{
            const colors = {{ emerald: 'bg-emerald-600', red: 'bg-red-500', gray: 'bg-gray-600', green: 'bg-green-500', blue: 'bg-blue-600' }};
            const toast = document.createElement('div');
            toast.className = `fixed bottom-24 md:bottom-4 right-4 ${{colors[color]}} text-white px-6 py-3 rounded-xl shadow-2xl z-[9999] transform transition-all duration-300 translate-y-0 opacity-100 flex items-center gap-3 font-bold slide-in border border-white/20`;
            toast.innerHTML = `<i class="fas ${{icon}} text-xl"></i> ${{msg}}`;
            document.body.appendChild(toast);
            setTimeout(() => {{ toast.style.opacity = '0'; toast.style.transform = 'translateY(20px)'; setTimeout(() => toast.remove(), 300); }}, 2500);
        }}

        function pulseCartIcon() {{
            let cartIcon = document.querySelector('.cart-icon-pulse');
            if (cartIcon) {{ cartIcon.classList.add('scale-125'); setTimeout(() => cartIcon.classList.remove('scale-125'), 200); }}
        }}

        // ADVANCED LIVE SEARCH SYSTEM
        function liveSearch(query) {{
            let suggestionsDiv = document.getElementById('searchSuggestions');
            if(!query || query.length < 2) {{ suggestionsDiv.classList.add('hidden'); return; }}
            
            query = query.toLowerCase();
            let results = window.GLOBAL_SEARCH_INDEX.filter(p => 
                p.name.toLowerCase().includes(query) || p.category.toLowerCase().includes(query)
            ).slice(0, 6); // Max 6 results
            
            if(results.length > 0) {{
                let html = results.map(p => `
                    <a href="/product/${{p.slug}}.html" class="flex items-center gap-3 p-3 hover:bg-emerald-50 dark:hover:bg-emerald-900/30 border-b border-gray-100 dark:border-gray-700 transition">
                        <img src="${{p.image}}" class="w-12 h-12 object-cover rounded bg-white">
                        <div class="flex-1 min-w-0">
                            <h4 class="text-sm font-bold text-gray-900 dark:text-white line-clamp-1">${{p.name}}</h4>
                            <p class="text-xs font-black text-emerald-600 dark:text-emerald-400">Rs ${{p.final_price}}</p>
                        </div>
                    </a>
                `).join('');
                
                html += `<div class="p-2 text-center bg-gray-50 dark:bg-gray-800"><button onclick="executeSearch()" class="text-xs font-bold text-emerald-600 hover:text-emerald-700">View all results <i class="fas fa-arrow-right"></i></button></div>`;
                
                suggestionsDiv.innerHTML = html;
                suggestionsDiv.classList.remove('hidden');
            }} else {{
                suggestionsDiv.innerHTML = `<div class="p-4 text-center text-sm text-gray-500">No products found</div>`;
                suggestionsDiv.classList.remove('hidden');
            }}
        }}

        function executeSearch() {{
            let val = document.getElementById('searchInput').value;
            if(val.trim() !== "") window.location.href = '/index.html?search=' + encodeURIComponent(val);
        }}
        function handleSearch(e) {{ if (e.key === 'Enter') executeSearch(); }}
        
        // Hide suggestions when clicking outside
        document.addEventListener('click', function(e) {{
            let searchDiv = document.getElementById('searchInput');
            let suggestDiv = document.getElementById('searchSuggestions');
            if(suggestDiv && e.target !== searchDiv && !suggestDiv.contains(e.target)) {{
                suggestDiv.classList.add('hidden');
            }}
        }});

        // DARK MODE
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
            
            // Sticky Cart / Back to Top Logic
            window.addEventListener('scroll', function() {{
                let btn = document.getElementById('backToTop');
                if (btn) btn.style.display = window.scrollY > 400 ? 'flex' : 'none';
                
                let stickyCart = document.getElementById('stickyCart');
                if(stickyCart) {{
                    if(window.scrollY > 600) stickyCart.classList.remove('translate-y-full');
                    else stickyCart.classList.add('translate-y-full');
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
    <header class="glass shadow-md sticky top-0 z-50 transition-colors border-b border-gray-100 dark:border-gray-800">
        <div class="bg-gray-900 text-white text-xs md:text-sm py-2">
            <div class="container mx-auto px-4 flex justify-between items-center">
                <div class="flex space-x-4 items-center">
                    <a href="/index.html" class="hover:text-emerald-400 transition font-semibold"><i class="fas fa-home mr-1"></i> Home</a>
                    <div class="relative dropdown z-50 hidden md:block">
                        <button class="hover:text-emerald-400 transition font-semibold focus:outline-none"><i class="fas fa-list mr-1"></i> Categories <i class="fas fa-chevron-down text-[10px] ml-1"></i></button>
                        <div class="dropdown-menu absolute hidden text-gray-700 bg-white dark:bg-gray-800 dark:text-gray-200 shadow-2xl rounded-xl mt-1 w-56 py-2 border border-gray-100 dark:border-gray-700 max-h-96 overflow-y-auto">
                            {cat_links}
                        </div>
                    </div>
                    <a href="/about.html" class="hover:text-emerald-400 transition font-semibold"><i class="fas fa-info-circle mr-1"></i> About</a>
                    <a href="/contact.html" class="hover:text-emerald-400 transition font-semibold"><i class="fas fa-envelope mr-1"></i> Contact</a>
                </div>
                <div class="flex items-center gap-3">
                    <button onclick="toggleDarkMode()" class="hover:text-emerald-400 transition" aria-label="Toggle Dark Mode"><i class="fas fa-moon dark-mode-icon"></i></button>
                    <div class="hidden md:block text-emerald-400 font-bold"><i class="fas fa-truck-fast"></i> Cash on Delivery</div>
                </div>
            </div>
        </div>

        <div class="container mx-auto px-4 py-4 flex flex-wrap justify-between items-center gap-4">
            <a href="/index.html" class="text-2xl md:text-3xl font-extrabold text-emerald-800 dark:text-emerald-400 tracking-tight flex items-center gap-2" aria-label="ASM VEO Home">
                <div class="bg-gradient-to-br from-emerald-600 to-emerald-800 text-white p-2 rounded-lg shadow-md" aria-hidden="true"><i class="fas fa-shopping-bag"></i></div>
                ASM VEO
            </a>
            
            <div class="flex-1 min-w-[200px] max-w-xl mx-0 md:mx-8 relative">
                <label for="searchInput" class="sr-only">Search products in Pakistan</label>
                <input type="text" id="searchInput" onkeyup="liveSearch(this.value)" onfocus="liveSearch(this.value)" onkeypress="handleSearch(event)" placeholder="Search products, brands, categories..." autocomplete="off" class="w-full bg-gray-50 dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 focus:bg-white dark:focus:bg-gray-700 focus:border-emerald-600 rounded-xl py-3 px-6 outline-none transition-all text-gray-800 dark:text-gray-100 font-semibold shadow-sm">
                <button onclick="executeSearch()" aria-label="Search" class="absolute right-4 top-3 text-gray-500 hover:text-emerald-700"><i class="fas fa-search text-xl" aria-hidden="true"></i></button>
                
                <!-- Live Search Auto-Suggest Dropdown -->
                <div id="searchSuggestions" class="absolute top-full left-0 w-full mt-2 bg-white dark:bg-gray-800 rounded-xl shadow-2xl border border-gray-200 dark:border-gray-700 hidden max-h-80 overflow-y-auto z-[60]"></div>
            </div>
            
            <div class="flex items-center gap-3">
                <a href="/wishlist.html" class="relative bg-pink-50 text-pink-600 p-3 rounded-xl hover:bg-pink-600 hover:text-white transition-colors border border-pink-200" aria-label="Wishlist">
                    <i class="fas fa-heart"></i>
                    <span class="wishlist-badge absolute -top-2 -right-2 bg-pink-500 text-white text-xs font-black px-1.5 py-0.5 rounded-full shadow min-w-[20px] text-center">0</span>
                </a>
                <a href="/checkout.html" class="cart-icon-pulse relative bg-emerald-50 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200 px-5 py-3 rounded-xl font-bold hover:bg-emerald-700 hover:text-white transition-colors border border-emerald-200 dark:border-emerald-700 shadow-sm flex items-center gap-2" aria-label="Go to Cart">
                    <i class="fas fa-shopping-cart text-xl" aria-hidden="true"></i>
                    <span class="hidden md:inline">Cart</span>
                    <span class="cart-badge absolute -top-2 -right-2 bg-red-500 text-white text-xs font-black px-1.5 py-0.5 rounded-full shadow min-w-[20px] text-center">0</span>
                </a>
            </div>
        </div>
    </header>

    <!-- Cookie Consent -->
    <div id="cookieConsent" class="hidden fixed bottom-20 md:bottom-0 left-0 right-0 bg-gray-900 text-white p-4 z-[9998] shadow-2xl">
        <div class="container mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-3">
                <i class="fas fa-cookie-bite text-2xl text-emerald-400"></i>
                <p class="text-sm">We use cookies to improve your experience. By continuing to browse, you agree to our use of cookies.</p>
            </div>
            <div class="flex gap-3">
                <a href="/privacy.html" class="text-emerald-400 hover:text-emerald-300 text-sm font-bold mt-2">Privacy Policy</a>
                <button onclick="acceptCookies()" class="bg-emerald-600 hover:bg-emerald-700 px-6 py-2 rounded-lg font-bold text-sm transition">Accept</button>
            </div>
        </div>
    </div>

    <!-- Mobile Bottom Navigation -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-900 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)] border-t border-gray-100 dark:border-gray-800 flex justify-around py-2 md:hidden z-[90]">
        <a href="/index.html" class="flex flex-col items-center text-emerald-600 text-xs font-bold"><i class="fas fa-home text-lg mb-1"></i> Home</a>
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

    <!-- WhatsApp & Back To Top -->
    <a href="https://wa.me/923425478683?text=Hi,%20I%20want%20to%20know%20about%20your%20products" target="_blank" 
       class="fixed bottom-24 right-4 bg-green-500 text-white w-14 h-14 rounded-full shadow-2xl flex items-center justify-center hover:bg-green-600 transition-all z-50 hover:scale-110" 
       aria-label="Chat on WhatsApp">
        <i class="fab fa-whatsapp text-3xl"></i>
        <span class="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full animate-ping"></span>
        <span class="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full"></span>
    </a>

    <button id="backToTop" onclick="scrollTop()" class="hidden fixed bottom-40 md:bottom-24 left-4 bg-emerald-600 text-white w-12 h-12 rounded-full shadow-2xl items-center justify-center hover:bg-emerald-700 transition z-50" aria-label="Back to top">
        <i class="fas fa-arrow-up text-xl"></i>
    </button>

    <main id="main-content">
"""

# ==================== HTML FOOTER ====================

def get_html_footer():
    return """
    </main>
    <footer class="bg-gray-900 text-white mt-16 pt-16 pb-20 md:pb-8 border-t-4 border-emerald-600">
        <div class="container mx-auto px-4 grid grid-cols-1 md:grid-cols-4 gap-10 mb-10">
            <div class="col-span-1 md:col-span-2">
                <h3 class="text-3xl font-extrabold mb-4 flex items-center gap-2 text-white"><i class="fas fa-shopping-bag text-emerald-400" aria-hidden="true"></i> ASM VEO</h3>
                <p class="text-gray-400 text-sm leading-relaxed mb-6 pr-4">ASM VEO is Pakistan's premium online shopping platform by <strong class="text-emerald-400">ASM Digital Solutions</strong>. Enjoy premium quality products, nationwide Cash on Delivery, 7-day return policy, and a 100% secure shopping experience.</p>
                <div class="flex gap-4 mb-6">
                    <a href="#" aria-label="Facebook" class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-blue-600 transition text-white"><i class="fab fa-facebook-f"></i></a>
                    <a href="#" aria-label="Instagram" class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-pink-600 transition text-white"><i class="fab fa-instagram"></i></a>
                    <a href="https://wa.me/923425478683" aria-label="WhatsApp" class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-green-600 transition text-white"><i class="fab fa-whatsapp"></i></a>
                    <a href="#" aria-label="YouTube" class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-red-600 transition text-white"><i class="fab fa-youtube"></i></a>
                </div>
                <div class="flex flex-wrap gap-3">
                    <div class="bg-gray-800 px-4 py-2 rounded-lg flex items-center gap-2 text-xs font-bold"><i class="fas fa-shield-alt text-emerald-400"></i> SSL Secure</div>
                    <div class="bg-gray-800 px-4 py-2 rounded-lg flex items-center gap-2 text-xs font-bold"><i class="fas fa-truck text-emerald-400"></i> Nationwide COD</div>
                    <div class="bg-gray-800 px-4 py-2 rounded-lg flex items-center gap-2 text-xs font-bold"><i class="fas fa-undo text-emerald-400"></i> 7-Day Returns</div>
                </div>
            </div>
            <div>
                <h3 class="text-xl font-bold mb-5 text-white border-b border-gray-700 pb-2">Quick Links</h3>
                <ul class="space-y-3 text-gray-400 text-sm font-semibold">
                    <li><a href="/index.html" class="hover:text-emerald-400 transition"><i class="fas fa-angle-right mr-2 text-emerald-600"></i> Home</a></li>
                    <li><a href="/about.html" class="hover:text-emerald-400 transition"><i class="fas fa-angle-right mr-2 text-emerald-600"></i> About Us</a></li>
                    <li><a href="/contact.html" class="hover:text-emerald-400 transition"><i class="fas fa-angle-right mr-2 text-emerald-600"></i> Contact Us</a></li>
                    <li><a href="/faq.html" class="hover:text-emerald-400 transition"><i class="fas fa-angle-right mr-2 text-emerald-600"></i> FAQ</a></li>
                    <li><a href="/checkout.html" class="hover:text-emerald-400 transition"><i class="fas fa-angle-right mr-2 text-emerald-600"></i> Cart / Checkout</a></li>
                    <li><a href="/privacy.html" class="hover:text-emerald-400 transition"><i class="fas fa-angle-right mr-2 text-emerald-600"></i> Privacy Policy</a></li>
                    <li><a href="/terms.html" class="hover:text-emerald-400 transition"><i class="fas fa-angle-right mr-2 text-emerald-600"></i> Terms & Conditions</a></li>
                </ul>
            </div>
            <div>
                <h3 class="text-xl font-bold mb-5 text-white border-b border-gray-700 pb-2">Get in Touch</h3>
                <ul class="space-y-4 text-gray-400 text-sm">
                    <li class="flex items-center gap-3"><div class="bg-gray-800 p-2 rounded text-emerald-400"><i class="fas fa-user-tie"></i></div> CEO: Ali Abbas</li>
                    <li class="flex items-center gap-3"><div class="bg-gray-800 p-2 rounded text-emerald-400"><i class="fas fa-building"></i></div> ASM Digital Solutions</li>
                    <li class="flex items-center gap-3"><div class="bg-green-500 p-2 rounded text-white"><i class="fab fa-whatsapp text-lg"></i></div> <a href="https://wa.me/923425478683" class="hover:text-white transition font-bold text-base">0342 54 786 83</a></li>
                    <li class="flex items-center gap-3"><div class="bg-gray-800 p-2 rounded text-emerald-400"><i class="fas fa-clock"></i></div> Mon-Sun: 9AM - 11PM</li>
                </ul>
            </div>
        </div>
        <div class="container mx-auto px-4 mb-8">
            <div class="bg-gray-800 rounded-2xl p-6 flex flex-col md:flex-row items-center justify-between gap-4">
                <div>
                    <h4 class="text-xl font-bold text-white mb-1">Subscribe to Our Newsletter</h4>
                    <p class="text-gray-400 text-sm">Get exclusive deals and new arrivals straight to your inbox.</p>
                </div>
                <form onsubmit="event.preventDefault(); showToast('Subscribed successfully!', 'fa-envelope', 'emerald'); this.reset();" class="flex gap-2 w-full md:w-auto">
                    <input type="email" required placeholder="Enter your email" class="bg-gray-700 text-white px-4 py-3 rounded-xl outline-none flex-1 md:w-64 border border-gray-600 focus:border-emerald-500">
                    <button type="submit" class="bg-emerald-600 hover:bg-emerald-700 px-6 py-3 rounded-xl font-bold transition">Subscribe</button>
                </form>
            </div>
        </div>
        <div class="border-t border-gray-800 text-center pt-8">
            <p class="text-gray-500 text-sm font-semibold">&copy; 2026 ASM Digital Solutions. All Rights Reserved. | Powered by ASM VEO</p>
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
        "background_color": "#f8fafc",
        "theme_color": "#047857",
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
    escaped_name = prod['name'].replace("'", "\\'")
    
    wishlist_btn = ""
    if show_wishlist:
        wishlist_btn = f"""
            <button onclick="toggleWishlist('{escaped_name}', {prod['final_price']}, '{prod['image']}', event)" 
                    class="wishlist-btn absolute top-3 right-3 w-9 h-9 bg-white rounded-full shadow-md flex items-center justify-center hover:bg-pink-50 transition z-10" 
                    aria-label="Add to Wishlist">
                <i class="fas fa-heart text-pink-500"></i>
            </button>"""
    
    return f"""
    <div class="product-card bg-white dark:bg-gray-800 rounded-2xl shadow-sm hover:shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col relative cursor-pointer group" onclick="window.location.href='/product/{prod['slug']}.html'">
        {wishlist_btn}
        {f'<div class="absolute top-3 left-3 bg-red-600 text-white text-xs font-black px-2.5 py-1 rounded-lg z-10 shadow-md">-{discount}% OFF</div>' if discount > 0 else ''}
        <div class="image-zoom h-48 md:h-60 bg-gray-50 dark:bg-gray-700 overflow-hidden relative border-b border-gray-200 dark:border-gray-700 flex justify-center items-center">
            <img src="{prod['image']}" alt="{prod['name']} buy online in Pakistan" {img_loading} class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/400x400/047857/ffffff?text=ASM+VEO'">
            <!-- Quick View Overlay overlay -->
            <div class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <span class="bg-white text-emerald-800 font-bold px-4 py-2 rounded-full text-sm shadow-lg transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300">View Product</span>
            </div>
        </div>
        <div class="p-4 flex flex-col flex-grow">
            <span class="text-[10px] font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider mb-1 line-clamp-1">{prod['category']}</span>
            <h3 class="prod-title text-sm md:text-base font-bold text-gray-900 dark:text-gray-100 leading-tight mb-2 line-clamp-2">{prod['name']}</h3>
            <div class="flex items-center gap-1 mb-2 text-yellow-500 text-xs">
                <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star-half-alt"></i>
                <span class="text-gray-400 ml-1">({random.randint(10, 200)})</span>
            </div>
            <div class="mt-auto">
                <div class="flex items-center gap-2 mb-1">
                    <span class="text-lg font-black text-emerald-800 dark:text-emerald-400">Rs {prod['final_price']}</span>
                    <span class="text-xs text-gray-400 font-bold line-through">Rs {prod['fake_price']}</span>
                </div>
                <div class="text-[10px] text-orange-600 font-bold mb-2"><i class="fas fa-fire"></i> Only {stock_left} left in stock!</div>
                <div class="flex gap-2 w-full">
                    <button onclick="addToCart('{escaped_name}', {prod['final_price']}, '{prod['image']}', event)" class="w-1/2 bg-emerald-50 dark:bg-emerald-900 text-emerald-800 dark:text-emerald-200 py-2.5 rounded-xl text-xs font-bold border border-emerald-200 dark:border-emerald-700 hover:bg-emerald-100 dark:hover:bg-emerald-800 transition flex justify-center items-center" aria-label="Add to Cart">
                        <i class="fas fa-cart-plus"></i>
                    </button>
                    <!-- BUG FIXED HERE: Removed extra quote -->
                    <button onclick="buyNow('{escaped_name}', {prod['final_price']}, '{prod['image']}', event)" class="w-1/2 bg-gray-900 dark:bg-emerald-600 text-white py-2.5 rounded-xl text-xs font-bold hover:bg-emerald-700 transition text-center" aria-label="Buy Now">
                        Buy Now
                    </button>
                </div>
            </div>
        </div>
    </div>
    """

# ==================== STATIC PAGES ====================

def generate_static_pages(categories_list, global_search_json):
    with open("output/about.html", "w", encoding="utf-8") as f:
        f.write(get_html_header("About Us", categories_list, global_search_json=global_search_json) + """
        <div class="container mx-auto px-4 py-16 max-w-4xl">
            <div class="text-center mb-12">
                <h1 class="text-4xl md:text-5xl font-extrabold text-gray-900 dark:text-white mb-6">About ASM VEO</h1>
                <p class="text-lg text-gray-600 dark:text-gray-300 leading-relaxed">Your trusted shopping partner in Pakistan</p>
            </div>
            <div class="grid md:grid-cols-2 gap-8 mb-12">
                <div class="bg-white dark:bg-gray-800 p-8 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-700">
                    <div class="w-14 h-14 bg-emerald-100 rounded-2xl flex items-center justify-center mb-4"><i class="fas fa-bullseye text-2xl text-emerald-700"></i></div>
                    <h3 class="text-xl font-bold mb-3 text-gray-900 dark:text-white">Our Mission</h3>
                    <p class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">To provide every Pakistani with access to premium quality products at affordable prices, delivered right to their doorstep with Cash on Delivery convenience.</p>
                </div>
                <div class="bg-white dark:bg-gray-800 p-8 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-700">
                    <div class="w-14 h-14 bg-emerald-100 rounded-2xl flex items-center justify-center mb-4"><i class="fas fa-eye text-2xl text-emerald-700"></i></div>
                    <h3 class="text-xl font-bold mb-3 text-gray-900 dark:text-white">Our Vision</h3>
                    <p class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">To become Pakistan's most trusted and loved e-commerce platform, known for quality, reliability, and exceptional customer service.</p>
                </div>
            </div>
            <div class="bg-gradient-to-r from-emerald-600 to-emerald-800 text-white rounded-3xl p-8 md:p-12">
                <h2 class="text-3xl font-bold mb-4">Why Choose ASM VEO?</h2>
                <div class="grid md:grid-cols-3 gap-6 mt-8">
                    <div><i class="fas fa-shield-alt text-4xl mb-3 text-emerald-300"></i><h4 class="font-bold text-lg mb-2">100% Secure</h4><p class="text-emerald-100 text-sm">SSL encrypted checkout with COD option</p></div>
                    <div><i class="fas fa-truck-fast text-4xl mb-3 text-emerald-300"></i><h4 class="font-bold text-lg mb-2">Fast Delivery</h4><p class="text-emerald-100 text-sm">Nationwide delivery in 2-4 business days</p></div>
                    <div><i class="fas fa-undo text-4xl mb-3 text-emerald-300"></i><h4 class="font-bold text-lg mb-2">Easy Returns</h4><p class="text-emerald-100 text-sm">7-day return policy, no questions asked</p></div>
                </div>
            </div>
        </div>
        """ + get_html_footer())

    with open("output/contact.html", "w", encoding="utf-8") as f:
        f.write(get_html_header("Contact Us", categories_list, global_search_json=global_search_json) + """
        <div class="container mx-auto px-4 py-16 max-w-4xl">
            <h1 class="text-4xl font-extrabold text-gray-900 dark:text-white mb-8 text-center">Contact Us</h1>
            <div class="grid md:grid-cols-2 gap-8">
                <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-xl p-8 border border-gray-100 dark:border-gray-700">
                    <i class="fab fa-whatsapp text-6xl text-green-500 mb-4"></i>
                    <h2 class="text-2xl font-bold mb-2 text-gray-900 dark:text-white">WhatsApp Support</h2>
                    <p class="text-gray-600 dark:text-gray-300 mb-6">Quick and instant support for all your queries. Message us anytime!</p>
                    <a href="https://wa.me/923425478683" class="inline-block bg-green-500 text-white font-black py-4 px-8 rounded-xl hover:bg-green-600 transition shadow-lg w-full text-center"><i class="fab fa-whatsapp mr-2"></i> 0342 54 786 83</a>
                </div>
                <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-xl p-8 border border-gray-100 dark:border-gray-700">
                    <i class="fas fa-headset text-6xl text-emerald-600 mb-4"></i>
                    <h2 class="text-2xl font-bold mb-2 text-gray-900 dark:text-white">Business Hours</h2>
                    <ul class="text-gray-600 dark:text-gray-300 space-y-2">
                        <li class="flex justify-between"><span>Monday - Friday</span><span class="font-bold">9AM - 11PM</span></li>
                        <li class="flex justify-between"><span>Saturday</span><span class="font-bold">10AM - 11PM</span></li>
                        <li class="flex justify-between"><span>Sunday</span><span class="font-bold">12PM - 10PM</span></li>
                    </ul>
                    <div class="mt-6 pt-6 border-t border-gray-100 dark:border-gray-700">
                        <p class="text-sm text-gray-500"><i class="fas fa-building mr-2 text-emerald-600"></i> ASM Digital Solutions</p>
                        <p class="text-sm text-gray-500 mt-1"><i class="fas fa-user-tie mr-2 text-emerald-600"></i> CEO: Ali Abbas</p>
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
    
    faq_html = get_html_header("Frequently Asked Questions", categories_list, global_search_json=global_search_json)
    faq_html += """
    <div class="container mx-auto px-4 py-16 max-w-3xl">
        <h1 class="text-4xl font-extrabold text-gray-900 dark:text-white mb-8 text-center">Frequently Asked Questions</h1>
        <div class="space-y-4">
    """
    for q, a in faqs:
        faq_html += f"""
            <details class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 group">
                <summary class="p-5 cursor-pointer font-bold text-gray-900 dark:text-white flex justify-between items-center list-none">
                    {q}
                    <i class="fas fa-chevron-down text-emerald-600 transition-transform group-open:rotate-180"></i>
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
        f.write(get_html_header("Privacy Policy", categories_list, global_search_json=global_search_json) + """
        <div class="container mx-auto px-4 py-16 max-w-4xl prose dark:prose-invert">
            <h1 class="text-4xl font-extrabold mb-8 text-gray-900 dark:text-white">Privacy Policy</h1>
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
        f.write(get_html_header("Terms & Conditions", categories_list, global_search_json=global_search_json) + """
        <div class="container mx-auto px-4 py-16 max-w-4xl">
            <h1 class="text-4xl font-extrabold mb-8 text-gray-900 dark:text-white">Terms & Conditions</h1>
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
        f.write(get_html_header("Page Not Found", categories_list, global_search_json=global_search_json) + """
        <div class="container mx-auto px-4 py-20 text-center">
            <div class="max-w-lg mx-auto">
                <div class="text-9xl font-black text-emerald-600 mb-4">404</div>
                <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">Oops! Page Not Found</h1>
                <p class="text-gray-500 dark:text-gray-400 mb-8">The page you're looking for doesn't exist or has been moved. Let's get you back on track!</p>
                <div class="flex gap-4 justify-center flex-wrap">
                    <a href="/index.html" class="bg-emerald-600 text-white px-8 py-3 rounded-xl font-bold hover:bg-emerald-700 transition shadow-lg"><i class="fas fa-home mr-2"></i> Go Home</a>
                    <a href="/contact.html" class="bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white px-8 py-3 rounded-xl font-bold hover:bg-gray-200 dark:hover:bg-gray-700 transition"><i class="fas fa-headset mr-2"></i> Contact Us</a>
                </div>
            </div>
        </div>
        """ + get_html_footer())

    with open("output/wishlist.html", "w", encoding="utf-8") as f:
        f.write(get_html_header("My Wishlist", categories_list, global_search_json=global_search_json) + """
        <div class="container mx-auto px-4 py-12 min-h-[50vh]">
            <h1 class="text-3xl font-extrabold text-gray-900 dark:text-white mb-8 flex items-center gap-3"><i class="fas fa-heart text-pink-500"></i> My Wishlist</h1>
            <div id="wishlistContainer" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
                <div class="col-span-full text-center py-16 text-gray-500 dark:text-gray-400">
                    <i class="fas fa-heart-broken text-6xl mb-4 opacity-30"></i>
                    <p class="text-lg font-bold">Your wishlist is empty</p>
                    <p class="text-sm mt-2">Start adding products you love!</p>
                    <a href="/index.html" class="inline-block mt-6 bg-emerald-600 text-white px-8 py-3 rounded-xl font-bold hover:bg-emerald-700 transition">Browse Products</a>
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
                                <img src="${item.image}" alt="${item.name}" class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/400x400/047857/ffffff?text=ASM+VEO'">
                            </div>
                            <div class="p-4 flex flex-col flex-grow">
                                <h3 class="text-sm font-bold text-gray-900 dark:text-white line-clamp-2 mb-2">${item.name}</h3>
                                <p class="text-lg font-black text-emerald-800 dark:text-emerald-400 mb-3">Rs ${item.price}</p>
                                <div class="flex gap-2 mt-auto">
                                    <button onclick="addToCart('${safeName}', ${item.price}, '${item.image}')" class="flex-1 bg-emerald-600 text-white py-2 rounded-lg text-xs font-bold hover:bg-emerald-700 transition"><i class="fas fa-cart-plus"></i></button>
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
        f.write(get_html_header("Order Confirmed!", categories_list, global_search_json=global_search_json) + """
        <div class="container mx-auto px-4 py-20 text-center">
            <div class="max-w-lg mx-auto">
                <div class="w-24 h-24 mx-auto bg-green-100 rounded-full flex items-center justify-center mb-6 animate-bounce">
                    <i class="fas fa-check text-5xl text-green-600"></i>
                </div>
                <h1 class="text-3xl font-extrabold text-gray-900 dark:text-white mb-4">Order Confirmed!</h1>
                <p class="text-gray-600 dark:text-gray-300 mb-2">Thank you for your purchase. Your order has been placed successfully.</p>
                <p class="text-gray-500 dark:text-gray-400 text-sm mb-8">Order ID: <span id="orderId" class="font-bold text-emerald-600">ASM-XXXXXX</span></p>
                <div class="bg-emerald-50 dark:bg-emerald-900/30 rounded-2xl p-6 mb-8 text-left">
                    <h3 class="font-bold text-gray-900 dark:text-white mb-3">What's Next?</h3>
                    <ol class="space-y-3 text-sm text-gray-600 dark:text-gray-300">
                        <li class="flex gap-3"><span class="w-6 h-6 bg-emerald-600 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">1</span> We'll confirm your order via WhatsApp shortly</li>
                        <li class="flex gap-3"><span class="w-6 h-6 bg-emerald-600 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">2</span> Your order will be dispatched within 24 hours</li>
                        <li class="flex gap-3"><span class="w-6 h-6 bg-emerald-600 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">3</span> Expected delivery: 2-4 business days</li>
                        <li class="flex gap-3"><span class="w-6 h-6 bg-emerald-600 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">4</span> Pay cash when you receive your order</li>
                    </ol>
                </div>
                <div class="flex gap-4 justify-center flex-wrap">
                    <a href="/index.html" class="bg-emerald-600 text-white px-8 py-3 rounded-xl font-bold hover:bg-emerald-700 transition shadow-lg"><i class="fas fa-shopping-bag mr-2"></i> Continue Shopping</a>
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
        
    print("🚀 Enterprise Script Started! Cleaning old data...")
    
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
            
            # BUG FIX: STRICT IMAGE VALIDATION
            if not name or not images_raw or 'http' not in images_raw.lower(): 
                continue 
                
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
    print(f"✔ Total {len(products_list)} valid products being processed...")
    
    # Generate Global Search JSON
    global_search_json = json.dumps([{"name": p['name'], "slug": p['slug'], "category": p['category'], 
                                      "final_price": p['final_price'], "image": p['image']} for p in products_list])
    
    generate_static_pages(categories_list, global_search_json)
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
                gallery_thumbs += f'<img src="{img}" alt="Thumbnail {idx+1}" onmouseover="changeMainImage(this)" onclick="changeMainImage(this)" class="w-16 h-16 object-cover rounded-lg cursor-pointer border-2 {"border-emerald-600" if idx == 0 else "border-gray-200"} hover:border-emerald-500 transition" onerror="this.style.display=\'none\'">'
            gallery_html = f'<div class="flex gap-2 mt-4 overflow-x-auto pb-2">{gallery_thumbs}</div>'
        
        breadcrumb_data = {'category': prod['category'], 'name': prod['name'], 'slug': prod['slug']}
        product_schema_data = {**prod, 'rating': avg_rating, 'review_count': review_count}
        
        prod_html = get_html_header(prod['name'], categories_list, prod['seo_desc'], 
                                     product_data=product_schema_data, breadcrumb_data=breadcrumb_data,
                                     og_image=prod['image'], global_search_json=global_search_json)
        
        discount_pct = math.ceil(((prod['fake_price'] - prod['final_price']) / prod['fake_price']) * 100) if prod['fake_price'] > prod['final_price'] else 0
        stock_left = random.randint(3, 15)
        delivery_date = (datetime.now() + timedelta(days=random.randint(2, 4))).strftime("%b %d, %Y")
        escaped_name = prod['name'].replace("'", "\\'")
        
        prod_html += f"""
        <!-- Floating Sticky Add to Cart Bar -->
        <div id="stickyCart" class="fixed bottom-0 left-0 w-full bg-white dark:bg-gray-900 shadow-[0_-4px_10px_rgba(0,0,0,0.1)] dark:shadow-[0_-4px_10px_rgba(0,0,0,0.4)] p-3 flex justify-between items-center z-50 transform translate-y-full transition-transform duration-300 border-t border-gray-200 dark:border-gray-800">
            <div class="flex items-center gap-3 w-1/2">
                <img src="{prod['image']}" class="w-12 h-12 object-cover rounded hidden sm:block">
                <div class="min-w-0">
                    <span class="font-bold text-sm text-gray-900 dark:text-white line-clamp-1">{prod['name']}</span>
                    <span class="font-black text-emerald-700 dark:text-emerald-400 text-xs">Rs {prod['final_price']}</span>
                </div>
            </div>
            <div class="flex items-center gap-2">
                <button onclick="addToCart('{escaped_name}', {prod['final_price']}, '{prod['image']}', event)" class="bg-emerald-600 text-white px-4 md:px-8 py-2.5 rounded-xl font-bold hover:bg-emerald-700 transition shadow-lg text-sm md:text-base">Add to Cart</button>
            </div>
        </div>

        <div class="container mx-auto px-4 py-10">
            <nav class="text-sm text-gray-600 dark:text-gray-400 mb-6 font-semibold bg-gray-100 dark:bg-gray-800 p-3 rounded-lg inline-block" aria-label="Breadcrumb">
                <a href="/index.html" class="hover:text-emerald-700 transition">Home</a> &gt; 
                <a href="/category/{make_slug(prod['category'])}.html" class="hover:text-emerald-700 transition">{prod['category']}</a> &gt; 
                <span class="text-emerald-800 dark:text-emerald-400" aria-current="page">{prod['name']}</span>
            </nav>
            
            <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col md:flex-row mb-12">
                <div class="md:w-1/2 p-6 flex flex-col justify-center items-center bg-gray-50 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 relative">
                    {f'<div class="absolute top-4 left-4 bg-red-600 text-white text-sm font-black px-3 py-1.5 rounded-lg z-10 shadow-md">-{discount_pct}% OFF</div>' if discount_pct > 0 else ''}
                    
                    <!-- Magnifying Zoom Image Container -->
                    <div class="zoom-magnifier w-full max-w-[500px] h-[300px] md:h-[500px] rounded-xl overflow-hidden relative shadow-sm bg-white" onmousemove="zoomImage(event)" onmouseleave="resetZoom(event)">
                        <img id="mainProductImage" src="{prod['image']}" alt="Image of {prod['name']}" fetchpriority="high" class="w-full h-full object-contain pointer-events-none" onerror="this.src='https://via.placeholder.com/600x600/047857/ffffff?text=ASM+VEO'">
                    </div>
                    {gallery_html}
                </div>
                <div class="md:w-1/2 p-8 md:p-12 flex flex-col justify-center">
                    <span class="text-xs font-bold uppercase tracking-widest text-emerald-700 dark:text-emerald-400 mb-2">{prod['category']}</span>
                    <h1 class="text-3xl md:text-4xl font-extrabold text-gray-900 dark:text-white mb-4">{prod['name']}</h1>
                    
                    <div class="flex items-center gap-3 mb-6" aria-label="Customer Rating">
                        <div class="text-yellow-500 text-sm">{"<i class='fas fa-star'></i>" * 5}</div>
                        <span class="text-sm font-semibold text-gray-600 dark:text-gray-300">{avg_rating} ({review_count} verified reviews)</span>
                    </div>

                    <div class="flex items-center gap-4 mb-4 bg-emerald-50 dark:bg-emerald-900/30 p-4 rounded-2xl w-fit border border-emerald-100 dark:border-emerald-800">
                        <span class="text-4xl font-black text-emerald-800 dark:text-emerald-400">Rs {prod['final_price']}</span>
                        <span class="text-xl text-gray-500 font-bold line-through">Rs {prod['fake_price']}</span>
                        {f'<span class="bg-red-500 text-white text-sm font-bold px-2 py-1 rounded-lg">Save Rs {prod["fake_price"] - prod["final_price"]}</span>' if discount_pct > 0 else ''}
                    </div>
                    
                    <div class="flex items-center gap-2 mb-6 text-sm">
                        <span class="bg-orange-100 text-orange-700 px-3 py-1 rounded-full font-bold"><i class="fas fa-fire"></i> Only {stock_left} left!</span>
                        <span class="bg-green-100 text-green-700 px-3 py-1 rounded-full font-bold"><i class="fas fa-truck"></i> Delivery by {delivery_date}</span>
                    </div>
                    
                    <p class="text-gray-700 dark:text-gray-300 mb-8 leading-relaxed border-t border-gray-100 dark:border-gray-700 pt-6">{prod['full_desc'][:500] if len(prod['full_desc']) > 50 else prod['seo_desc']}</p>
                    
                    <div class="flex flex-col sm:flex-row gap-4 w-full md:w-5/6 mt-auto">
                        <button onclick="addToCart('{escaped_name}', {prod['final_price']}, '{prod['image']}', event)" aria-label="Add to Cart" class="sm:w-1/2 bg-white dark:bg-gray-700 text-emerald-700 dark:text-emerald-300 py-4 rounded-xl font-black text-lg border-2 border-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-900 transition-all shadow-md transform hover:-translate-y-1 flex justify-center items-center gap-2">
                            <i class="fas fa-cart-plus"></i> Add to Cart
                        </button>
                        <!-- BUG FIX: Removed extra quote from buyNow -->
                        <button onclick="buyNow('{escaped_name}', {prod['final_price']}, '{prod['image']}', event)" aria-label="Buy Now" class="sm:w-1/2 bg-gray-900 dark:bg-emerald-600 text-white py-4 rounded-xl font-black text-lg hover:bg-emerald-700 transition-all shadow-lg transform hover:-translate-y-1 flex justify-center items-center gap-2">
                            <i class="fas fa-bolt"></i> Buy Now
                        </button>
                    </div>
                    
                    <div class="grid grid-cols-3 gap-3 mt-8 pt-6 border-t border-gray-100 dark:border-gray-700">
                        <div class="text-center"><i class="fas fa-shield-alt text-emerald-600 text-xl mb-1"></i><p class="text-xs font-semibold text-gray-600 dark:text-gray-400">Secure Payment</p></div>
                        <div class="text-center"><i class="fas fa-undo text-emerald-600 text-xl mb-1"></i><p class="text-xs font-semibold text-gray-600 dark:text-gray-400">7-Day Returns</p></div>
                        <div class="text-center"><i class="fas fa-truck text-emerald-600 text-xl mb-1"></i><p class="text-xs font-semibold text-gray-600 dark:text-gray-400">Fast Delivery</p></div>
                    </div>
                </div>
            </div>
            
            {"<div class='bg-white dark:bg-gray-800 rounded-3xl shadow-lg border border-gray-200 dark:border-gray-700 p-8 mb-8'><h2 class='text-2xl font-extrabold text-gray-900 dark:text-white mb-6 border-b pb-4'>You May Also Like</h2><div class='grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6'>" + related_html + "</div></div>" if related_html else ""}
            
            <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-lg border border-gray-200 dark:border-gray-700 p-8 mb-8">
                <h2 class="text-2xl font-extrabold text-gray-900 dark:text-white mb-6 border-b pb-4 flex items-center gap-3">
                    <i class="fas fa-star text-yellow-500"></i> Customer Reviews ({review_count})
                </h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div>{reviews_section}</div>
                    <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-2xl h-fit border border-gray-300 dark:border-gray-700">
                        <h3 class="font-bold text-lg mb-2 text-gray-900 dark:text-white">Write a Review</h3>
                        <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">You can submit a review to share your experience with others.</p>
                        
                        <!-- Mini Review Form (Simulated JS) -->
                        <form onsubmit="event.preventDefault(); showToast('Review submitted for moderation!', 'fa-check', 'emerald'); this.reset();" class="space-y-3">
                            <div class="flex gap-1 text-yellow-500 text-xl mb-2 cursor-pointer">
                                <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="far fa-star"></i>
                            </div>
                            <input type="text" required placeholder="Your Name" class="w-full bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 p-2 rounded-lg text-sm outline-none focus:border-emerald-500">
                            <textarea required placeholder="Write your review here..." rows="3" class="w-full bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 p-2 rounded-lg text-sm outline-none focus:border-emerald-500"></textarea>
                            <button type="submit" class="w-full bg-emerald-600 text-white font-bold py-2 rounded-lg hover:bg-emerald-700 transition text-sm">Submit Review</button>
                        </form>
                    </div>
                </div>
            </div>
            
            <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-lg border border-gray-200 dark:border-gray-700 p-8 mb-16 md:mb-0">
                <h2 class="text-2xl font-extrabold text-gray-900 dark:text-white mb-6 border-b pb-4">Product FAQs</h2>
                <div class="space-y-4">
                    <details class="border border-gray-200 dark:border-gray-700 rounded-xl p-4 group">
                        <summary class="cursor-pointer font-bold text-gray-900 dark:text-white flex justify-between list-none">Is this product genuine? <i class="fas fa-chevron-down text-emerald-600 group-open:rotate-180 transition"></i></summary>
                        <p class="mt-3 text-sm text-gray-600 dark:text-gray-300">Yes! We source 100% genuine products directly from authorized distributors. Every product is quality-checked before dispatch.</p>
                    </details>
                    <details class="border border-gray-200 dark:border-gray-700 rounded-xl p-4 group">
                        <summary class="cursor-pointer font-bold text-gray-900 dark:text-white flex justify-between list-none">What is the delivery time? <i class="fas fa-chevron-down text-emerald-600 group-open:rotate-180 transition"></i></summary>
                        <p class="mt-3 text-sm text-gray-600 dark:text-gray-300">Delivery takes 2-4 business days across Pakistan. Major cities receive faster delivery.</p>
                    </details>
                    <details class="border border-gray-200 dark:border-gray-700 rounded-xl p-4 group">
                        <summary class="cursor-pointer font-bold text-gray-900 dark:text-white flex justify-between list-none">Can I return this product? <i class="fas fa-chevron-down text-emerald-600 group-open:rotate-180 transition"></i></summary>
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
            
            // Thumbnail Switcher
            function changeMainImage(thumb) {
                let mainImg = document.getElementById('mainProductImage');
                mainImg.src = thumb.src;
                mainImg.style.transform = "scale(1)"; // Reset zoom on change
                document.querySelectorAll('.flex.gap-2 img').forEach(img => img.classList.remove('border-emerald-600'));
                thumb.classList.add('border-emerald-600');
            }

            // Image Zoom Logic
            function zoomImage(e) {
                let img = document.getElementById('mainProductImage');
                let rect = e.currentTarget.getBoundingClientRect();
                let x = ((e.clientX - rect.left) / rect.width) * 100;
                let y = ((e.clientY - rect.top) / rect.height) * 100;
                
                img.style.transformOrigin = `${x}% ${y}%`;
                img.style.transform = "scale(2.2)";
                img.style.objectFit = "cover";
            }
            function resetZoom(e) {
                let img = document.getElementById('mainProductImage');
                img.style.transformOrigin = "center center";
                img.style.transform = "scale(1)";
                img.style.objectFit = "contain";
            }
        </script>
        """
        prod_html += prod_script.replace("__RECENT_JSON__", recent_json) + get_html_footer()
        
        with open(f"output/product/{prod['slug']}.html", "w", encoding="utf-8") as f:
            f.write(prod_html)

    # ================= CATEGORY PAGES =================
    sections_dict = {}
    for p in products_list:
        c = p['category']
        if c not in sections_dict: sections_dict[c] = []
        sections_dict[c].append(p)

    search_index_json = json.dumps([{"name": p['name'], "slug": p['slug'], "category": p['category'], 
                                     "final_price": p['final_price'], "fake_price": p['fake_price'], "image": p['image']} for p in products_list])

    home_html = get_html_header("Home - Premium Online Shopping in Pakistan", categories_list,
                                 "ASM VEO - Pakistan's premium online shopping destination. Buy quality products with Cash on Delivery.",
                                 global_search_json=global_search_json)
    
    # Hero Carousel Slider
    home_html += """
    <div id="heroCarousel" class="relative w-full h-[300px] md:h-[450px] overflow-hidden shadow-xl">
        <div class="carousel-track h-full">
            <div class="carousel-slide h-full bg-gradient-to-r from-emerald-700 to-emerald-900 flex items-center p-6 md:p-16 text-white relative">
                <div class="z-10 max-w-lg">
                    <span class="bg-yellow-400 text-black text-xs font-black px-3 py-1 rounded-full animate-pulse">MEGA SALE</span>
                    <h2 class="text-3xl md:text-6xl font-extrabold mt-4 mb-4 leading-tight">Flat 50% OFF<br>Premium Products</h2>
                    <p class="text-base md:text-lg mb-6 text-emerald-100">Cash on Delivery available all over Pakistan. Shop now before stock ends!</p>
                    <a href="#products" class="bg-white text-emerald-700 px-8 py-3 rounded-lg font-bold hover:bg-gray-100 transition inline-flex items-center gap-2"><i class="fas fa-shopping-bag"></i> Shop Now</a>
                </div>
                <img src="https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?auto=format&fit=crop&w=800&q=80" alt="Sale" class="absolute right-0 top-0 h-full w-1/2 object-cover opacity-30 md:opacity-100 hidden md:block">
            </div>
            <div class="carousel-slide h-full bg-gradient-to-r from-gray-900 to-gray-800 flex items-center p-6 md:p-16 text-white relative">
                <div class="z-10 max-w-lg">
                    <span class="bg-emerald-500 text-white text-xs font-black px-3 py-1 rounded-full">NEW ARRIVALS</span>
                    <h2 class="text-3xl md:text-6xl font-extrabold mt-4 mb-4 leading-tight">Latest Gadgets<br>& Accessories</h2>
                    <p class="text-base md:text-lg mb-6 text-gray-300">100% Genuine products delivered to your doorstep nationwide.</p>
                    <a href="#products" class="bg-emerald-600 text-white px-8 py-3 rounded-lg font-bold hover:bg-emerald-700 transition inline-flex items-center gap-2"><i class="fas fa-bolt"></i> Explore Now</a>
                </div>
                <img src="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=800&q=80" alt="Gadgets" class="absolute right-0 top-0 h-full w-1/2 object-cover opacity-30 md:opacity-100 hidden md:block">
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
        slides.forEach((_, i) => { dotsContainer.innerHTML += `<button onclick="goToSlide(${i})" class="w-3 h-3 rounded-full bg-white/50 hover:bg-white transition"></button>`; });
        function updateCarousel() {
            document.querySelector('.carousel-track').style.transform = `translateX(-${slideIndex * 100}%)`;
            document.querySelectorAll('#carouselDots button').forEach((dot, i) => { dot.className = `w-3 h-3 rounded-full transition ${i === slideIndex ? 'bg-white scale-125' : 'bg-white/50 hover:bg-white'}`; });
        }
        function nextSlide() { slideIndex = (slideIndex + 1) % slides.length; updateCarousel(); }
        function prevSlide() { slideIndex = (slideIndex - 1 + slides.length) % slides.length; updateCarousel(); }
        function goToSlide(i) { slideIndex = i; updateCarousel(); }
        updateCarousel(); setInterval(nextSlide, 5000);
    </script>
    """

    home_html += """
    <div class="container mx-auto px-4 py-6">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-3">
                <div class="bg-emerald-100 dark:bg-emerald-900 p-3 rounded-lg text-emerald-600"><i class="fas fa-truck-fast text-xl"></i></div>
                <div><h3 class="font-bold text-sm text-gray-900 dark:text-white">Fast Delivery</h3><p class="text-xs text-gray-500 dark:text-gray-400">All over Pakistan</p></div>
            </div>
            <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-3">
                <div class="bg-emerald-100 dark:bg-emerald-900 p-3 rounded-lg text-emerald-600"><i class="fas fa-money-bill-wave text-xl"></i></div>
                <div><h3 class="font-bold text-sm text-gray-900 dark:text-white">Cash on Delivery</h3><p class="text-xs text-gray-500 dark:text-gray-400">Pay at your doorstep</p></div>
            </div>
            <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-3">
                <div class="bg-emerald-100 dark:bg-emerald-900 p-3 rounded-lg text-emerald-600"><i class="fas fa-shield-halved text-xl"></i></div>
                <div><h3 class="font-bold text-sm text-gray-900 dark:text-white">Secure Shopping</h3><p class="text-xs text-gray-500 dark:text-gray-400">100% Protected</p></div>
            </div>
            <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-3">
                <div class="bg-emerald-100 dark:bg-emerald-900 p-3 rounded-lg text-emerald-600"><i class="fas fa-undo text-xl"></i></div>
                <div><h3 class="font-bold text-sm text-gray-900 dark:text-white">Easy Returns</h3><p class="text-xs text-gray-500 dark:text-gray-400">7 Days Return Policy</p></div>
            </div>
        </div>
    </div>
    """

    home_html += f"""
    <div class='container mx-auto px-4 py-4' id="products">
        <div id="searchResultsSection" class="hidden mb-6">
            <h2 id="searchResultsHeading" class="text-2xl font-extrabold text-emerald-800 dark:text-emerald-400 mb-2 border-b pb-2"></h2>
            <p id="searchResultsCount" class="text-gray-500 text-sm"></p>
        </div>
        <div id="defaultContent">
    """
    
    total_rendered_products = 0
    for cat_name, prods in sections_dict.items():
        cat_slug = make_slug(cat_name)
        sitemap_urls.append(f"https://www.asmveo.com/category/{cat_slug}.html")
        
        cat_html = get_html_header(cat_name, categories_list, f"Buy {cat_name} online in Pakistan at best prices. Wide range of {cat_name} with Cash on Delivery from ASM VEO.", global_search_json=global_search_json)
        
        min_price = min(p['final_price'] for p in prods)
        max_price = max(p['final_price'] for p in prods)
        
        cat_html += f"""
        <div class="bg-gradient-to-r from-emerald-600 to-emerald-800 py-12 mb-8 relative overflow-hidden">
            <div class="absolute inset-0 opacity-10" style="background-image: url('data:image/svg+xml,%3Csvg width=\"60\" height=\"60\" viewBox=\"0 0 60 60\" xmlns=\"http://www.w3.org/2000/svg\"%3E%3Cg fill=\"none\" fill-rule=\"evenodd\"%3E%3Cg fill=\"%23ffffff\"%3E%3Cpath d=\"M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>
            <div class="container mx-auto px-4 text-center relative">
                <div class="w-16 h-16 mx-auto rounded-full bg-white/20 backdrop-blur flex items-center justify-center mb-4 text-white shadow-lg">
                    <i class="fas {get_category_icon(cat_name)} text-3xl"></i>
                </div>
                <h1 class="text-3xl md:text-5xl font-black text-white">{cat_name}</h1>
                <p class="text-emerald-100 mt-3 font-bold">{len(prods)} Products Available • Cash on Delivery</p>
            </div>
        </div>
        
        <div class="container mx-auto px-4 pb-12">
            <div class="flex flex-col lg:flex-row gap-6">
                <aside class="lg:w-64 flex-shrink-0">
                    <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 p-5 sticky top-24">
                        <h3 class="font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2"><i class="fas fa-filter text-emerald-600"></i> Filters</h3>
                        
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
                            <button onclick="applyFilters()" class="w-full bg-emerald-600 text-white py-2 rounded-lg text-sm font-bold hover:bg-emerald-700 transition">Apply Filter</button>
                        </div>
                        
                        <button onclick="resetFilters()" class="w-full text-gray-500 hover:text-emerald-600 text-sm font-bold transition"><i class="fas fa-undo mr-1"></i> Reset Filters</button>
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
                return `<div class="product-card bg-white dark:bg-gray-800 rounded-2xl shadow-sm hover:shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col relative cursor-pointer group" onclick="window.location.href='/product/${p.slug}.html'">
                    <button onclick="toggleWishlist('${safeName}', ${p.final_price}, '${p.image}', event)" class="absolute top-3 right-3 w-9 h-9 bg-white rounded-full shadow-md flex items-center justify-center hover:bg-pink-50 transition z-10"><i class="fas fa-heart text-pink-500"></i></button>
                    ${discount > 0 ? `<div class="absolute top-3 left-3 bg-red-600 text-white text-xs font-black px-2.5 py-1 rounded-lg z-10 shadow-md">-${discount}% OFF</div>` : ''}
                    <div class="image-zoom h-48 md:h-60 bg-gray-50 dark:bg-gray-700 overflow-hidden relative border-b border-gray-200 dark:border-gray-700 flex justify-center items-center">
                        <img src="${p.image}" alt="${p.name}" loading="lazy" class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/400x400/047857/ffffff?text=ASM+VEO'">
                        <div class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                            <span class="bg-white text-emerald-800 font-bold px-4 py-2 rounded-full text-sm shadow-lg transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300">View Product</span>
                        </div>
                    </div>
                    <div class="p-4 flex flex-col flex-grow">
                        <span class="text-[10px] font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider mb-1 line-clamp-1">${p.category}</span>
                        <h3 class="text-sm md:text-base font-bold text-gray-900 dark:text-white leading-tight mb-2 line-clamp-2">${p.name}</h3>
                        <div class="mt-auto">
                            <div class="flex items-center gap-2 mb-3">
                                <span class="text-lg font-black text-emerald-800 dark:text-emerald-400">Rs ${p.final_price}</span>
                                <span class="text-xs text-gray-400 font-bold line-through">Rs ${p.fake_price}</span>
                            </div>
                            <div class="flex gap-2 w-full">
                                <button onclick="addToCart('${safeName}', ${p.final_price}, '${p.image}', event)" class="w-1/2 bg-emerald-50 dark:bg-emerald-900 text-emerald-800 dark:text-emerald-200 py-2.5 rounded-xl text-xs font-bold border border-emerald-200 dark:border-emerald-700 hover:bg-emerald-100 transition flex justify-center items-center"><i class="fas fa-cart-plus"></i></button>
                                <button onclick="buyNow('${safeName}', ${p.final_price}, '${p.image}', event)" class="w-1/2 bg-gray-900 dark:bg-emerald-600 text-white py-2.5 rounded-xl text-xs font-bold hover:bg-emerald-700 transition text-center">Buy Now</button>
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
        <div class="mb-14 category-section">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl md:text-3xl font-black text-gray-900 dark:text-white border-l-4 border-emerald-600 pl-4">{cat_name}</h2>
                <a href="/category/{cat_slug}.html" class="text-emerald-700 dark:text-emerald-400 font-bold text-sm bg-emerald-50 dark:bg-emerald-900/30 px-5 py-2.5 rounded-full hover:bg-emerald-700 hover:text-white transition-all shadow-sm">View All <i class="fas fa-arrow-right ml-1"></i></a>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
        """
        
        for idx, prod in enumerate(prods[:10]):
            home_html += generate_product_card(prod, lazy=(idx >= 4))
            total_rendered_products += 1
            
        home_html += "</div></div>"
    
    home_html += "</div></div>"

    home_html += """
    <div id="recentlyViewedSection" class="hidden container mx-auto px-4 py-8 border-t border-gray-200 dark:border-gray-700">
        <h2 class="text-2xl font-extrabold text-gray-900 dark:text-white mb-6 border-l-4 border-emerald-600 pl-4">Recently Viewed</h2>
        <div id="recentlyViewedGrid" class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4 md:gap-6"></div>
    </div>
    """
    
    home_script = """
    <script>
        let searchIndex = __SEARCH_INDEX__;
        
        function performSearch(query) {
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
                html += `<div class="product-card bg-white dark:bg-gray-800 rounded-2xl shadow-sm hover:shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col relative cursor-pointer group" onclick="window.location.href='/product/${p.slug}.html'">
                    ${discount > 0 ? `<div class="absolute top-3 left-3 bg-red-600 text-white text-xs font-black px-2.5 py-1 rounded-lg z-10 shadow-md">-${discount}% OFF</div>` : ''}
                    <div class="image-zoom h-48 md:h-60 bg-gray-50 dark:bg-gray-700 overflow-hidden relative border-b border-gray-200 dark:border-gray-700 flex justify-center items-center">
                        <img src="${p.image}" alt="${p.name}" loading="lazy" class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/400x400/047857/ffffff?text=ASM+VEO'">
                        <div class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                            <span class="bg-white text-emerald-800 font-bold px-4 py-2 rounded-full text-sm shadow-lg transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300">View Product</span>
                        </div>
                    </div>
                    <div class="p-4 flex flex-col flex-grow">
                        <span class="text-[10px] font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider mb-1 line-clamp-1">${p.category}</span>
                        <h3 class="text-sm md:text-base font-bold text-gray-900 dark:text-white leading-tight mb-2 line-clamp-2">${p.name}</h3>
                        <div class="mt-auto">
                            <div class="flex items-center gap-2 mb-3">
                                <span class="text-lg font-black text-emerald-800 dark:text-emerald-400">Rs ${p.final_price}</span>
                                <span class="text-xs text-gray-400 font-bold line-through">Rs ${p.fake_price}</span>
                            </div>
                            <div class="flex gap-2 w-full">
                                <button onclick="addToCart('${safeName}', ${p.final_price}, '${p.image}', event)" class="w-1/2 bg-emerald-50 dark:bg-emerald-900 text-emerald-800 dark:text-emerald-200 py-2.5 rounded-xl text-xs font-bold border border-emerald-200 dark:border-emerald-700 hover:bg-emerald-100 transition flex justify-center items-center"><i class="fas fa-cart-plus"></i></button>
                                <button onclick="buyNow('${safeName}', ${p.final_price}, '${p.image}', event)" class="w-1/2 bg-gray-900 dark:bg-emerald-600 text-white py-2.5 rounded-xl text-xs font-bold hover:bg-emerald-700 transition text-center">Buy Now</button>
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
            document.getElementById('searchResultsSection').appendChild(resultsDiv);
        }
        
        const urlParams = new URLSearchParams(window.location.search);
        const searchQuery = urlParams.get('search');
        if (searchQuery) {
            document.getElementById('searchInput').value = searchQuery;
            performSearch(searchQuery);
        }
        
        function renderRecentlyViewed() {
            let recent = JSON.parse(localStorage.getItem('asm_recent')) || [];
            recent = recent.slice(0, 5);
            if (recent.length === 0) return;
            
            document.getElementById('recentlyViewedSection').classList.remove('hidden');
            let grid = document.getElementById('recentlyViewedGrid');
            grid.innerHTML = recent.map(p => {
                let discount = Math.ceil(((p.fake_price - p.final_price) / p.fake_price) * 100);
                return `<div class="product-card bg-white dark:bg-gray-800 rounded-2xl shadow-sm hover:shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col relative cursor-pointer" onclick="window.location.href='/product/${p.slug}.html'">
                    ${discount > 0 ? `<div class="absolute top-3 left-3 bg-red-600 text-white text-xs font-black px-2.5 py-1 rounded-lg z-10 shadow-md">-${discount}% OFF</div>` : ''}
                    <div class="h-48 bg-gray-50 dark:bg-gray-700 overflow-hidden border-b border-gray-200 dark:border-gray-700 flex justify-center items-center">
                        <img src="${p.image}" alt="${p.name}" loading="lazy" class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/400x400/047857/ffffff?text=ASM+VEO'">
                    </div>
                    <div class="p-4 flex flex-col flex-grow">
                        <h3 class="text-sm font-bold text-gray-900 dark:text-white line-clamp-2 mb-2">${p.name}</h3>
                        <div class="mt-auto">
                            <span class="text-lg font-black text-emerald-800 dark:text-emerald-400">Rs ${p.final_price}</span>
                            <span class="text-xs text-gray-400 font-bold line-through ml-2">Rs ${p.fake_price}</span>
                        </div>
                    </div>
                </div>`;
            }).join('');
        }
        window.addEventListener('load', renderRecentlyViewed);
    </script>
    """
    home_html += home_script.replace("__SEARCH_INDEX__", search_index_json) + get_html_footer()
    
    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(home_html)

    # ================= CHECKOUT PAGE =================
    pak_cities = ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Multan", 
                  "Peshawar", "Quetta", "Gujranwala", "Sialkot", "Hyderabad", "Bahawalpur", 
                  "Sargodha", "Sukkur", "Mardan", "Gujrat", "Larkana", "Kasur", "Rahim Yar Khan", "Other"]
    city_options = "".join([f"<option value='{city}'>{city}</option>" for city in pak_cities])
    delivery_date = (datetime.now() + timedelta(days=3)).strftime("%A, %b %d")
    
    checkout_html = get_html_header("Secure Checkout", categories_list, "Complete your order with Cash on Delivery. Fast and secure checkout at ASM VEO.", global_search_json=global_search_json)
    checkout_html += f"""
    <div class="container mx-auto px-4 py-12 max-w-6xl">
        <h1 class="text-3xl font-extrabold text-gray-900 dark:text-white mb-8 flex items-center gap-3"><i class="fas fa-lock text-emerald-600"></i> Secure Checkout</h1>
        
        <div class="flex items-center justify-center mb-10">
            <div class="flex items-center text-emerald-600 font-bold">
                <div class="w-10 h-10 bg-emerald-600 text-white rounded-full flex items-center justify-center font-black">1</div>
                <span class="ml-2 hidden md:inline">Cart</span>
            </div>
            <div class="w-16 md:w-32 h-1 bg-emerald-600 mx-2"></div>
            <div class="flex items-center text-emerald-600 font-bold">
                <div class="w-10 h-10 bg-emerald-600 text-white rounded-full flex items-center justify-center font-black">2</div>
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
                    <h2 class="text-2xl font-black text-gray-900 dark:text-white mb-4 border-b pb-4 flex items-center gap-2"><i class="fas fa-shopping-bag text-emerald-600"></i> Your Items</h2>
                    <div id="cartItemsContainer" class="space-y-4 max-h-[400px] overflow-y-auto pr-2"></div>
                </div>
                
                <!-- NEW PROMO CODE SECTION -->
                <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-xl p-6 border border-gray-200 dark:border-gray-700 mb-6">
                    <h3 class="font-bold text-gray-900 dark:text-white mb-3 text-sm flex items-center gap-2"><i class="fas fa-tag text-emerald-600"></i> Have a Promo Code?</h3>
                    <div class="flex gap-2">
                        <input type="text" id="promoCodeInput" placeholder="Enter code (e.g. ASM10)" class="flex-1 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg p-2.5 text-sm outline-none focus:border-emerald-500 uppercase">
                        <button type="button" onclick="applyPromoCode()" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2.5 rounded-lg transition text-sm">Apply</button>
                    </div>
                    <p id="promoMessage" class="text-xs font-bold mt-2 hidden"></p>
                </div>
                
                <div class="bg-emerald-50 dark:bg-emerald-900/30 rounded-2xl p-5 border border-emerald-100 dark:border-emerald-800">
                    <h3 class="font-bold text-gray-900 dark:text-white mb-3 text-sm">Why Shop With Us?</h3>
                    <div class="grid grid-cols-2 gap-3 text-xs">
                        <div class="flex items-center gap-2"><i class="fas fa-shield-alt text-emerald-600"></i> 100% Secure Checkout</div>
                        <div class="flex items-center gap-2"><i class="fas fa-truck text-emerald-600"></i> Fast Nationwide Delivery</div>
                        <div class="flex items-center gap-2"><i class="fas fa-undo text-emerald-600"></i> 7-Day Return Policy</div>
                        <div class="flex items-center gap-2"><i class="fas fa-certificate text-emerald-600"></i> 100% Genuine Products</div>
                    </div>
                </div>
            </div>

            <div class="lg:w-1/2">
                <div class="bg-gray-900 p-6 rounded-t-3xl text-white relative">
                    <div class="absolute top-0 left-0 w-full h-1 bg-emerald-500 rounded-t-3xl"></div>
                    <h1 class="text-2xl font-extrabold flex items-center gap-2"><i class="fas fa-map-marker-alt text-emerald-400"></i> Shipping Details</h1>
                    <p class="text-emerald-200 text-sm mt-1"><i class="fas fa-truck"></i> Expected delivery: {delivery_date}</p>
                </div>
                
                <form id="checkoutForm" class="bg-white dark:bg-gray-800 p-6 md:p-8 rounded-b-3xl shadow-xl border border-gray-200 dark:border-gray-700 border-t-0 space-y-5">
                    <input type="hidden" name="_subject" value="🛒 New Order on ASM VEO!">
                    <input type="hidden" name="Product_Ordered" id="productField" value="">
                    <input type="hidden" name="Order_Total" id="totalField" value="">
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <div>
                            <label class="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">Full Name <span class="text-red-600">*</span></label>
                            <input type="text" name="Full_Name" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-emerald-600 outline-none" required placeholder="Ali Abbas">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">Email Address</label>
                            <input type="email" name="Email" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-emerald-600 outline-none" placeholder="you@example.com">
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <div>
                            <label class="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">Mobile Number <span class="text-red-600">*</span></label>
                            <input type="tel" name="Phone_Number" pattern="03[0-9]{{2}}[0-9]{{7}}" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-emerald-600 outline-none" required placeholder="0300-XXXXXXX">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">City <span class="text-red-600">*</span></label>
                            <select name="City" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-emerald-600 outline-none font-semibold" required>
                                <option value="" disabled selected>Select City</option>
                                {city_options}
                            </select>
                        </div>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">Complete Delivery Address <span class="text-red-600">*</span></label>
                        <textarea name="Address" rows="3" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-emerald-600 outline-none" required placeholder="House No, Street, Area, Landmark..."></textarea>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">Order Notes (Optional)</label>
                        <textarea name="Order_Notes" rows="2" class="w-full border-2 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white p-3 rounded-xl bg-gray-50 focus:bg-white focus:border-emerald-600 outline-none" placeholder="Any special instructions..."></textarea>
                    </div>
                    
                    <div class="bg-emerald-50 dark:bg-emerald-900/30 rounded-2xl p-5 border border-emerald-100 dark:border-emerald-800 mt-6 relative overflow-hidden">
                        <div id="confetti" class="absolute inset-0 pointer-events-none hidden"></div>
                        <div class="flex justify-between text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">
                            <span>Subtotal</span>
                            <span id="subtotalDisplay">Rs 0</span>
                        </div>
                        <div id="discountRow" class="flex justify-between text-sm font-bold text-emerald-600 mb-2 hidden">
                            <span>Discount (Promo)</span>
                            <span id="discountDisplay">-Rs 0</span>
                        </div>
                        <div class="flex justify-between text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">
                            <span>Delivery Charges</span>
                            <span id="deliveryDisplay">Rs 250</span>
                        </div>
                        <div class="flex justify-between items-center border-t border-emerald-200 dark:border-emerald-800 pt-3 mt-3">
                            <span class="font-black text-lg text-gray-900 dark:text-white">Total (COD)</span>
                            <span class="font-black text-2xl text-emerald-800 dark:text-emerald-400" id="grandTotalDisplay">Rs 250</span>
                        </div>
                    </div>

                    <button type="submit" id="submitBtn" class="w-full bg-gray-900 dark:bg-emerald-600 text-white font-black py-4 rounded-xl hover:bg-emerald-700 transition-all shadow-xl text-lg transform hover:-translate-y-1 flex items-center justify-center gap-2">
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
        let currentDiscountPercentage = 0;

        function applyPromoCode() {
            let codeInput = document.getElementById('promoCodeInput');
            let msg = document.getElementById('promoMessage');
            let code = codeInput.value.trim().toUpperCase();
            
            if(code === 'ASM10') {
                currentDiscountPercentage = 10;
                msg.innerText = "Promo applied! 10% OFF.";
                msg.className = "text-xs font-bold mt-2 text-emerald-600 block";
                showToast('Promo Code Applied!', 'fa-tag', 'emerald');
                renderCart(); // Re-calculate
            } else {
                currentDiscountPercentage = 0;
                msg.innerText = "Invalid or expired promo code.";
                msg.className = "text-xs font-bold mt-2 text-red-500 block";
                renderCart(); // Re-calculate
            }
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
                            <p class="text-emerald-700 dark:text-emerald-400 font-black">Rs ${pPrice}</p>
                        </div>
                    </div>`;
            } else {
                let cart = getCart();
                if(cart.length === 0) {
                    container.innerHTML = `<div class="text-center py-8"><i class="fas fa-shopping-cart text-5xl text-gray-300 mb-3"></i><p class="text-gray-500 font-semibold">Your cart is empty.</p><a href="/index.html" class="inline-block mt-4 bg-emerald-600 text-white px-6 py-2 rounded-xl font-bold">Browse Products</a></div>`;
                    document.getElementById('submitBtn').disabled = true;
                    document.getElementById('submitBtn').classList.add('opacity-50', 'cursor-not-allowed');
                } else {
                    document.getElementById('submitBtn').disabled = false;
                    document.getElementById('submitBtn').classList.remove('opacity-50', 'cursor-not-allowed');
                    cart.forEach((item, index) => {
                        let qty = item.qty || 1;
                        subtotal += parseInt(item.price) * qty;
                        finalOrderString += qty + "x " + item.name + " (Rs " + (item.price * qty) + ")\\n";
                        
                        container.innerHTML += `
                        <div class="flex items-center gap-3 bg-gray-50 dark:bg-gray-700 p-3 rounded-xl border border-gray-200 dark:border-gray-600">
                            <img src="${item.image}" class="w-16 h-16 object-cover rounded-lg bg-white border border-gray-100" onerror="this.src='https://via.placeholder.com/100x100/047857/ffffff?text=ASM'">
                            <div class="flex-1 min-w-0">
                                <h3 class="font-bold text-sm text-gray-900 dark:text-white line-clamp-2">${item.name}</h3>
                                <p class="text-emerald-700 dark:text-emerald-400 font-black text-sm">Rs ${item.price}</p>
                                <div class="flex items-center gap-2 mt-1">
                                    <button onclick="updateQty(${index}, -1)" type="button" class="w-6 h-6 bg-gray-200 dark:bg-gray-600 rounded text-gray-700 dark:text-white font-bold hover:bg-gray-300">-</button>
                                    <span class="font-bold text-sm">${qty}</span>
                                    <button onclick="updateQty(${index}, 1)" type="button" class="w-6 h-6 bg-gray-200 dark:bg-gray-600 rounded text-gray-700 dark:text-white font-bold hover:bg-gray-300">+</button>
                                    <button onclick="removeFromCart(${index})" type="button" class="ml-2 text-red-500 hover:text-red-700 text-xs"><i class="fas fa-trash"></i></button>
                                </div>
                            </div>
                        </div>`;
                    });
                }
            }

            // Calculation with Discount
            let discountAmount = Math.floor((subtotal * currentDiscountPercentage) / 100);
            let afterDiscount = subtotal - discountAmount;
            let delivery = afterDiscount >= 5000 ? 0 : 250;
            let grandTotal = afterDiscount + delivery;
            
            document.getElementById('subtotalDisplay').innerText = "Rs " + subtotal;
            
            let discRow = document.getElementById('discountRow');
            if(discountAmount > 0) {
                discRow.classList.remove('hidden');
                document.getElementById('discountDisplay').innerText = "-Rs " + discountAmount;
                finalOrderString += "\\nDiscount (" + currentDiscountPercentage + "%): -Rs " + discountAmount;
            } else {
                discRow.classList.add('hidden');
            }

            document.getElementById('deliveryDisplay').innerText = delivery === 0 ? "FREE" : "Rs " + delivery;
            document.getElementById('grandTotalDisplay').innerText = "Rs " + grandTotal;
            document.getElementById('productField').value = finalOrderString + "\\nDelivery: Rs " + delivery + "\\nGrand Total: Rs " + grandTotal;
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
    print(f"📦 Products: {len(products_list)} | 📂 Categories: {len(categories_list)}")
    print("✨ Features added: Live Search, Zoom Magnifier, Sticky Add-to-Cart, Promo Code System!")

if __name__ == "__main__":
    process_woocommerce_csv()
