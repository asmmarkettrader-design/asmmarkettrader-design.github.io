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
    if not text: return "uncategorized"
    slug = re.sub(r'[^a-z0-9]+', '-', str(text).lower()).strip('-')
    return slug if slug else "uncategorized"

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
        "Bahut khush hoon is product se. ASM VEO is trustworthy.",
        "Paisa wasool hai. Delivery thodi slow thi par product mast hai.",
        "Main is product se bohat khush hoon. High quality material."
    ]
    
    reviews_html = ""
    num_reviews = random.randint(4, 8)
    for i in range(num_reviews):
        reviewer = random.choice(names)
        comment = random.choice(templates).format(name=product_name)
        stars = random.randint(4, 5)
        days_ago = random.randint(1, 60)
        
        reviews_html += f"""
        <div class="border-b border-gray-100 dark:border-gray-700 py-4 last:border-0 reveal">
            <div class="flex items-center gap-2 mb-2">
                <div class="w-9 h-9 rounded-full bg-emerald-600 text-white flex items-center justify-center font-bold text-sm" aria-hidden="true">{reviewer[0]}</div>
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

# HTML Minifier for Fast Loading
def minify_html(html_content):
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
    html_content = re.sub(r'>\s+<', '><', html_content)
    html_content = re.sub(r'\s{2,}', ' ', html_content)
    return html_content.strip()

# ==================== HTML HEADER ====================

def get_html_header(title, cat_slug_map={}, seo_desc="ASM VEO - Premium Online Shopping in Pakistan", 
                    product_data=None, breadcrumb_data=None, og_image=None):
    
    cat_links = ""
    for cat, slug in cat_slug_map.items():
        cat_links += f'<a href="/category/{slug}.html" class="block px-4 py-2.5 text-sm text-gray-700 hover:bg-emerald-50 hover:text-emerald-700 transition-colors">{cat}</a>\n'

    structured_data = ""
    if product_data:
        structured_data = f"""
    <script type="application/ld+json">
    {{"@context":"https://schema.org/","@type":"Product","name":"{product_data['name']}","image":["{product_data['image']}"],"description":"{product_data.get('seo_desc', '')}","brand":{{"@type":"Brand","name":"ASM VEO"}},"offers":{{"@type":"Offer","priceCurrency":"PKR","price":"{product_data['final_price']}","availability":"https://schema.org/InStock"}},"aggregateRating":{{"@type":"AggregateRating","ratingValue":"{product_data.get('rating', 4.5)}","reviewCount":"{product_data.get('review_count', 10)}"}}}}
    </script>"""
    
    if breadcrumb_data:
        c_slug = cat_slug_map.get(breadcrumb_data['category'], make_slug(breadcrumb_data['category']))
        structured_data += f"""
    <script type="application/ld+json">
    {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://www.asmveo.com/"}},{{"@type":"ListItem","position":2,"name":"{breadcrumb_data['category']}","item":"https://www.asmveo.com/category/{c_slug}.html"}},{{"@type":"ListItem","position":3,"name":"{breadcrumb_data['name']}","item":"https://www.asmveo.com/product/{breadcrumb_data['slug']}.html"}}]}}
    </script>"""

    og_image_final = og_image or "https://www.asmveo.com/assets/og-image.jpg"
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <title>{title} | Buy Online in Pakistan | ASM VEO</title>
    
    <meta name="title" content="{title} | Buy Online in Pakistan | ASM VEO">
    <meta name="description" content="{seo_desc}">
    <meta name="keywords" content="buy {title} in Pakistan, online shopping Pakistan, cash on delivery, ASM VEO, Karachi, Lahore, Islamabad">
    <meta name="author" content="ASM Digital Solutions">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta name="theme-color" content="#047857">
    <link rel="canonical" href="https://www.asmveo.com/">
    
    <meta name="geo.region" content="PK" />
    <meta name="geo.placename" content="Pakistan" />
    
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://www.asmveo.com/">
    <meta property="og:title" content="{title} | ASM VEO">
    <meta property="og:description" content="{seo_desc}">
    <meta property="og:image" content="{og_image_final}">
    
    <link rel="manifest" href="/manifest.json">
    <link rel="preconnect" href="https://cdn.tailwindcss.com">
    <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{colors:{{pk:{{green:'#047857',light:'#ecfdf5',dark:'#065f46'}}}}}}}}}}</script>
    
    <link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"></noscript>
    
    <style>
        body{{font-family:'Plus Jakarta Sans',sans-serif;background-color:#f8fafc;transition:background-color .3s;padding-bottom:70px}}
        .dark body{{background-color:#0f172a;color:#e2e8f0}}
        .product-card{{transition:all .3s cubic-bezier(.4,0,.2,1);content-visibility:auto;contain-intrinsic-size:300px}}
        .product-card:hover{{transform:translateY(-5px);box-shadow:0 15px 30px -10px rgba(0,0,0,.15)}}
        .image-zoom img{{transition:transform .5s ease}}
        .product-card:hover .image-zoom img{{transform:scale(1.08)}}
        .dropdown:hover .dropdown-menu{{display:block}}
        ::-webkit-scrollbar{{width:8px;height:8px}}
        ::-webkit-scrollbar-track{{background:#f1f5f9}}
        ::-webkit-scrollbar-thumb{{background:#047857;border-radius:4px}}
        .skeleton{{background:linear-gradient(90deg,#f0f0f0 25%,#e0e0e0 50%,#f0f0f0 75%);background-size:200% 100%;animation:shimmer 1.5s infinite}}
        @keyframes shimmer{{0%{{background-position:200% 0}}100%{{background-position:-200% 0}}}}
        .line-clamp-1{{display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;overflow:hidden}}
        .line-clamp-2{{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
        @keyframes slideIn{{from{{transform:translateY(20px);opacity:0}}to{{transform:translateY(0);opacity:1}}}}
        .slide-in{{animation:slideIn .4s ease-out}}
        .carousel-track{{display:flex;transition:transform .8s cubic-bezier(.65,0,.35,1)}}
        .carousel-slide{{min-width:100%;box-sizing:border-box}}
        .glass{{background:rgba(255,255,255,.95);backdrop-filter:blur(10px)}}
        .dark .glass{{background:rgba(15,23,42,.95)}}
    </style>
    {structured_data}

    <script>
        function getCart(){{return JSON.parse(localStorage.getItem('asm_cart'))||[]}}
        function saveCart(cart){{localStorage.setItem('asm_cart',JSON.stringify(cart));updateCartBadge()}}
        function updateCartBadge(){{let cart=getCart();let cc=cart.reduce((s,i)=>s+(i.qty||1),0);document.querySelectorAll('.cart-badge').forEach(el=>el.innerText=cc)}}
        function addToCart(name,price,image,event){{if(event)event.stopPropagation();let cart=getCart();let ex=cart.find(i=>i.name===name);if(ex){ex.qty=(ex.qty||1)+1}else{cart.push({{name,price:parseFloat(price),image,qty:1}})}saveCart(cart);showToast('Added to Cart!','fa-cart-plus','emerald');pulseCartIcon()}}
        function removeFromCart(index){{let cart=getCart();cart.splice(index,1);saveCart(cart);if(typeof renderCart==='function')renderCart()}}
        function updateQty(index,delta){{let cart=getCart();if(!cart[index])return;cart[index].qty=(cart[index].qty||1)+delta;if(cart[index].qty<1){cart.splice(index,1)}saveCart(cart);if(typeof renderCart==='function')renderCart()}}
        function buyNow(name,price,image,event){{if(event)event.stopPropagation();window.location.href='/checkout.html?buy_now=true&product='+encodeURIComponent(name)+'&price='+price}}
        function toggleWishlist(name,price,image,event){{if(event)event.stopPropagation();let wl=JSON.parse(localStorage.getItem('asm_wishlist'))||[];let idx=wl.findIndex(i=>i.name===name);if(idx>-1){wl.splice(idx,1);showToast('Removed from Wishlist','fa-heart-broken','gray')}else{wl.push({{name,price,image}});showToast('Added to Wishlist!','fa-heart','red')}localStorage.setItem('asm_wishlist',JSON.stringify(wl));updateWishlistBadge()}}
        function updateWishlistBadge(){{let wl=JSON.parse(localStorage.getItem('asm_wishlist'))||[];document.querySelectorAll('.wishlist-badge').forEach(el=>el.innerText=wl.length)}}
        function addToRecentlyViewed(p){{let r=JSON.parse(localStorage.getItem('asm_recent'))||[];r=r.filter(i=>i.slug!==p.slug);r.unshift(p);r=r.slice(0,10);localStorage.setItem('asm_recent',JSON.stringify(r))}}
        function showToast(msg,icon='fa-check-circle',color='emerald'){{const c={{emerald:'bg-emerald-600',red:'bg-red-500',gray:'bg-gray-600',green:'bg-green-500'}};const t=document.createElement('div');t.className=`fixed bottom-20 md:bottom-4 right-4 ${{c[color]}} text-white px-6 py-3 rounded-xl shadow-2xl z-[9999] transform transition-all duration-300 translate-y-0 opacity-100 flex items-center gap-3 font-bold slide-in`;t.innerHTML=`<i class="fas ${{icon}} text-xl"></i> ${{msg}}`;document.body.appendChild(t);setTimeout(()=>{{t.style.opacity='0';t.style.transform='translateY(20px)';setTimeout(()=>t.remove(),300)}},2500)}}
        function pulseCartIcon(){{let c=document.querySelector('.cart-icon-pulse');if(c){c.classList.add('scale-125');setTimeout(()=>c.classList.remove('scale-125'),200)}}}
        function executeSearch(){{let v=document.getElementById('searchInput').value;if(v.trim()!=="")window.location.href='/index.html?search='+encodeURIComponent(v)}}
        function handleSearch(e){{if(e.key==='Enter')executeSearch()}}
        function toggleDarkMode(){{document.documentElement.classList.toggle('dark');localStorage.setItem('asm_dark',document.documentElement.classList.contains('dark'));updateDarkModeIcon()}}
        function updateDarkModeIcon(){{let d=document.documentElement.classList.contains('dark');document.querySelectorAll('.dark-mode-icon').forEach(el=>{el.className=`fas ${{d?'fa-sun':'fa-moon'}} dark-mode-icon`})}}
        function scrollTop(){{window.scrollTo({{top:0,behavior:'smooth'}})}}
        window.onload=function(){{updateCartBadge();updateWishlistBadge();if(localStorage.getItem('asm_dark')==='true'){document.documentElement.classList.add('dark');updateDarkModeIcon()}if(!localStorage.getItem('asm_cookie_consent')){document.getElementById('cookieConsent').classList.remove('hidden')}window.addEventListener('scroll',function(){{let b=document.getElementById('backToTop');if(b)b.style.display=window.scrollY>400?'flex':'none'}});let r=document.querySelectorAll('.reveal');function cR(){{r.forEach(e=>{{let t=e.getBoundingClientRect().top;if(t<window.innerHeight-50)e.classList.add('active')}})}}window.addEventListener('scroll',cR);cR();let s=document.getElementById('searchInput');if(s){s.addEventListener('focus',loadSearchData)}}};
        function acceptCookies(){{localStorage.setItem('asm_cookie_consent','true');document.getElementById('cookieConsent').classList.add('hidden')}}
        let searchLoaded=false;function loadSearchData(){{if(searchLoaded)return;searchLoaded=true;let s=document.createElement('script');s.src='/search-data.js';document.head.appendChild(s)}}
    </script>
</head>
<body class="text-gray-900 dark:text-gray-100">
    <header class="glass shadow-md sticky top-0 z-50 border-b border-gray-100 dark:border-gray-800">
        <div class="bg-gray-900 text-white text-xs md:text-sm py-2">
            <div class="container mx-auto px-4 flex justify-between items-center">
                <div class="flex space-x-4 items-center">
                    <a href="/index.html" class="hover:text-emerald-400 font-semibold"><i class="fas fa-home mr-1"></i> Home</a>
                    <div class="relative dropdown z-50 hidden md:block">
                        <button class="hover:text-emerald-400 font-semibold focus:outline-none"><i class="fas fa-list mr-1"></i> Categories <i class="fas fa-chevron-down text-[10px] ml-1"></i></button>
                        <div class="dropdown-menu absolute hidden text-gray-700 bg-white dark:bg-gray-800 dark:text-gray-200 shadow-2xl rounded-xl mt-1 w-56 py-2 border border-gray-100 dark:border-gray-700 max-h-96 overflow-y-auto">{cat_links}</div>
                    </div>
                    <a href="/about.html" class="hover:text-emerald-400 font-semibold hidden md:inline"><i class="fas fa-info-circle mr-1"></i> About</a>
                    <a href="/contact.html" class="hover:text-emerald-400 font-semibold hidden md:inline"><i class="fas fa-envelope mr-1"></i> Contact</a>
                    <a href="/faq.html" class="hover:text-emerald-400 font-semibold hidden md:inline"><i class="fas fa-question-circle mr-1"></i> FAQ</a>
                    <a href="/track-order.html" class="hover:text-emerald-400 font-semibold hidden md:inline"><i class="fas fa-truck-fast mr-1"></i> Track Order</a>
                </div>
                <div class="flex items-center gap-3">
                    <button onclick="toggleDarkMode()" class="hover:text-emerald-400" aria-label="Toggle Dark Mode"><i class="fas fa-moon dark-mode-icon"></i></button>
                    <div class="hidden md:block text-emerald-400 font-bold"><i class="fas fa-truck-fast"></i> Cash on Delivery</div>
                </div>
            </div>
        </div>
        <div class="container mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-4">
            <a href="/index.html" class="text-2xl font-extrabold text-emerald-800 dark:text-emerald-400 flex items-center gap-2">
                <div class="bg-emerald-600 text-white p-2 rounded-lg"><i class="fas fa-shopping-bag"></i></div>
                ASM VEO
            </a>
            <div class="flex-1 min-w-[200px] max-w-xl mx-0 md:mx-8 relative">
                <input type="text" id="searchInput" onkeypress="handleSearch(event)" placeholder="Search products..." class="w-full bg-gray-50 dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 focus:bg-white dark:focus:bg-gray-700 focus:border-emerald-600 rounded-xl py-2.5 px-6 outline-none text-sm shadow-sm">
                <button onclick="executeSearch()" class="absolute right-4 top-2.5 text-gray-500 hover:text-emerald-700"><i class="fas fa-search text-lg"></i></button>
            </div>
            <div class="flex items-center gap-3">
                <a href="/wishlist.html" class="relative bg-pink-50 text-pink-600 p-2.5 rounded-xl hover:bg-pink-600 hover:text-white border border-pink-200"><i class="fas fa-heart"></i><span class="wishlist-badge absolute -top-2 -right-2 bg-pink-500 text-white text-xs font-black px-1.5 py-0.5 rounded-full">0</span></a>
                <a href="/checkout.html" class="cart-icon-pulse relative bg-emerald-50 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200 px-4 py-2.5 rounded-xl font-bold hover:bg-emerald-700 hover:text-white border border-emerald-200 shadow-sm flex items-center gap-2 text-sm"><i class="fas fa-shopping-cart text-lg"></i><span class="hidden md:inline">Cart</span><span class="cart-badge absolute -top-2 -right-2 bg-red-500 text-white text-xs font-black px-1.5 py-0.5 rounded-full">0</span></a>
            </div>
        </div>
    </header>
    <div id="cookieConsent" class="hidden fixed bottom-20 md:bottom-0 left-0 right-0 bg-gray-900 text-white p-4 z-[9998] shadow-2xl"><div class="container mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4"><div class="flex items-center gap-3"><i class="fas fa-cookie-bite text-2xl text-emerald-400"></i><p class="text-sm">We use cookies to improve your experience.</p></div><div class="flex gap-3"><a href="/privacy.html" class="text-emerald-400 text-sm font-bold">Privacy Policy</a><button onclick="acceptCookies()" class="bg-emerald-600 px-6 py-2 rounded-lg font-bold text-sm">Accept</button></div></div></div>
    <nav class="fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-900 shadow-2xl border-t border-gray-100 dark:border-gray-800 flex justify-around py-2 md:hidden z-50"><a href="/index.html" class="flex flex-col items-center text-emerald-600 text-xs font-bold"><i class="fas fa-home text-lg mb-1"></i> Home</a><a href="/index.html#products" class="flex flex-col items-center text-gray-500 text-xs font-bold"><i class="fas fa-th-large text-lg mb-1"></i> Categories</a><a href="/checkout.html" class="flex flex-col items-center text-gray-500 text-xs font-bold relative"><i class="fas fa-shopping-cart text-lg mb-1"></i> Cart<span class="cart-badge absolute -top-1 right-2 bg-red-500 text-white text-[8px] font-black px-1 py-0.5 rounded-full">0</span></a><a href="/wishlist.html" class="flex flex-col items-center text-gray-500 text-xs font-bold relative"><i class="fas fa-heart text-lg mb-1"></i> Wishlist<span class="wishlist-badge absolute -top-1 right-2 bg-pink-500 text-white text-[8px] font-black px-1 py-0.5 rounded-full">0</span></a></nav>
    <a href="https://wa.me/923425478683" target="_blank" class="fixed bottom-24 right-4 bg-green-500 text-white w-14 h-14 rounded-full shadow-2xl flex items-center justify-center hover:bg-green-600 z-50 hover:scale-110"><i class="fab fa-whatsapp text-3xl"></i></a>
    <button id="backToTop" onclick="scrollTop()" class="hidden fixed bottom-24 left-4 bg-emerald-600 text-white w-12 h-12 rounded-full shadow-2xl items-center justify-center hover:bg-emerald-700 z-50"><i class="fas fa-arrow-up text-xl"></i></button>
    <main id="main-content" class="bg-white dark:bg-gray-900 shadow-2xl">
"""

# ==================== HTML FOOTER ====================

def get_html_footer(cat_slug_map={}):
    return f"""
    </main>
    <footer class="bg-gray-900 text-white mt-16 pt-16 pb-20 md:pb-8 border-t-4 border-emerald-600">
        <div class="container mx-auto px-4 grid grid-cols-1 md:grid-cols-4 gap-10 mb-10">
            <div class="col-span-1 md:col-span-2">
                <h3 class="text-3xl font-extrabold mb-4 flex items-center gap-2"><i class="fas fa-shopping-bag text-emerald-400"></i> ASM VEO</h3>
                <p class="text-gray-400 text-sm leading-relaxed mb-6 pr-4">ASM VEO is Pakistan's premium online shopping platform by <strong class="text-emerald-400">ASM Digital Solutions</strong>. Enjoy premium quality products, nationwide Cash on Delivery, 7-day return policy, and a 100% secure shopping experience.</p>
                <div class="flex gap-4 mb-6">
                    <a href="#" class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-blue-600 transition"><i class="fab fa-facebook-f"></i></a>
                    <a href="#" class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-pink-600 transition"><i class="fab fa-instagram"></i></a>
                    <a href="https://wa.me/923425478683" class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-green-600 transition"><i class="fab fa-whatsapp"></i></a>
                </div>
            </div>
            <div>
                <h3 class="text-xl font-bold mb-5 border-b border-gray-700 pb-2">Quick Links</h3>
                <ul class="space-y-3 text-gray-400 text-sm font-semibold">
                    <li><a href="/index.html" class="hover:text-emerald-400"><i class="fas fa-angle-right mr-2 text-emerald-600"></i> Home</a></li>
                    <li><a href="/about.html" class="hover:text-emerald-400"><i class="fas fa-angle-right mr-2 text-emerald-600"></i> About Us</a></li>
                    <li><a href="/contact.html" class="hover:text-emerald-400"><i class="fas fa-angle-right mr-2 text-emerald-600"></i> Contact Us</a></li>
                    <li><a href="/track-order.html" class="hover:text-emerald-400"><i class="fas fa-angle-right mr-2 text-emerald-600"></i> Track Order</a></li>
                    <li><a href="/shipping-policy.html" class="hover:text-emerald-400"><i class="fas fa-angle-right mr-2 text-emerald-600"></i> Shipping Policy</a></li>
                    <li><a href="/return-policy.html" class="hover:text-emerald-400"><i class="fas fa-angle-right mr-2 text-emerald-600"></i> Return Policy</a></li>
                    <li><a href="/sitemap.xml" class="hover:text-emerald-400"><i class="fas fa-angle-right mr-2 text-emerald-600"></i> Sitemap</a></li>
                </ul>
            </div>
            <div>
                <h3 class="text-xl font-bold mb-5 border-b border-gray-700 pb-2">Get in Touch</h3>
                <ul class="space-y-4 text-gray-400 text-sm">
                    <li class="flex items-center gap-3"><div class="bg-gray-800 p-2 rounded text-emerald-400"><i class="fas fa-user-tie"></i></div> CEO: Ali Abbas</li>
                    <li class="flex items-center gap-3"><div class="bg-green-500 p-2 rounded text-white"><i class="fab fa-whatsapp text-lg"></i></div> <a href="https://wa.me/923425478683" class="hover:text-white font-bold text-base">0342 54 786 83</a></li>
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

# ==================== SITEMAP & ROBOTS ====================

def generate_sitemap(urls):
    urls = list(set(urls))
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls: xml += f"  <url><loc>{u}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>\n"
    xml += '</urlset>'
    with open("output/sitemap.xml", "w", encoding="utf-8") as f: f.write(xml)

def generate_robots_txt():
    with open("output/robots.txt", "w") as f: f.write("User-agent: *\nAllow: /\nDisallow: /checkout.html\n\nSitemap: https://www.asmveo.com/sitemap.xml")

def generate_manifest():
    with open("output/manifest.json", "w") as f: json.dump({"name":"ASM VEO","short_name":"ASM VEO","start_url":"/index.html","display":"standalone","background_color":"#ffffff","theme_color":"#047857"}, f)

# ==================== PRODUCT CARD GENERATOR ====================

def generate_product_card(prod, lazy=True, show_wishlist=True):
    discount = math.ceil(((prod['fake_price'] - prod['final_price']) / prod['fake_price']) * 100) if prod['fake_price'] > 0 and prod['fake_price'] > prod['final_price'] else 0
    img_loading = 'loading="lazy"' if lazy else 'fetchpriority="high"'
    escaped_name = prod['name'].replace("'", "\\'")
    
    wishlist_btn = f"""<button onclick="toggleWishlist('{escaped_name}', {prod['final_price']}, '{prod['image']}', event)" class="absolute top-2 right-2 w-8 h-8 bg-white rounded-full shadow-md flex items-center justify-center hover:bg-pink-50 z-10"><i class="fas fa-heart text-pink-500 text-sm"></i></button>""" if show_wishlist else ""
    
    return f"""
    <div class="product-card reveal bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col relative cursor-pointer" onclick="window.location.href='/product/{prod['slug']}.html'">
        {wishlist_btn}
        {f'<div class="absolute top-2 left-2 bg-red-600 text-white text-[10px] font-black px-1.5 py-0.5 rounded z-10">-{discount}% OFF</div>' if discount > 0 else ''}
        <div class="image-zoom h-40 skeleton overflow-hidden relative border-b border-gray-200 dark:border-gray-700 flex justify-center items-center">
            <img src="{prod['image']}" alt="{prod['name']}" {img_loading} class="w-full h-full object-contain p-1 opacity-0 transition-opacity duration-500" onload="this.style.opacity=1;this.parentElement.classList.remove('skeleton')" onerror="this.src='https://via.placeholder.com/200/047857/ffffff?text=ASM+VEO'">
        </div>
        <div class="p-2 flex flex-col flex-grow">
            <span class="text-[9px] font-bold text-emerald-700 dark:text-emerald-400 uppercase mb-1 line-clamp-1">{prod['category']}</span>
            <h3 class="text-[10px] md:text-xs font-bold text-gray-900 dark:text-gray-100 mb-1 line-clamp-2">{prod['name']}</h3>
            <div class="mt-auto">
                <div class="flex items-center gap-1 mb-1"><span class="text-xs md:text-sm font-black text-emerald-800 dark:text-white">Rs {prod['final_price']}</span><span class="text-[9px] text-gray-400 line-through">Rs {prod['fake_price']}</span></div>
                <button onclick="addToCart('{escaped_name}', {prod['final_price']}, '{prod['image']}', event)" class="w-full bg-gray-50 text-emerald-700 py-1.5 rounded-md text-[10px] font-bold border border-gray-200 hover:bg-emerald-100 transition flex justify-center items-center"><i class="fas fa-cart-plus"></i></button>
            </div>
        </div>
    </div>
    """

# ==================== STATIC PAGES ====================

def generate_static_pages(cat_slug_map, sitemap_urls):
    static_pages = {
        "about.html": ("About Us", "About ASM VEO - Pakistan's premium online shopping platform.", "<div class='container mx-auto px-4 py-16'><h1 class='text-4xl font-extrabold text-center mb-8'>About ASM VEO</h1><p class='text-lg text-gray-600 text-center'>Your trusted shopping partner in Pakistan.</p></div>"),
        "contact.html": ("Contact Us", "Contact ASM VEO for queries and support.", "<div class='container mx-auto px-4 py-16 text-center'><h1 class='text-4xl font-extrabold mb-8'>Contact Us</h1><a href='https://wa.me/923425478683' class='bg-green-500 text-white px-8 py-4 rounded-xl font-bold'>WhatsApp: 0342 54 786 83</a></div>"),
        "faq.html": ("FAQ", "Frequently Asked Questions.", "<div class='container mx-auto px-4 py-16'><h1 class='text-4xl font-extrabold mb-8 text-center'>FAQ</h1><p class='text-center text-gray-600'>Delivery takes 2-4 days. COD available.</p></div>"),
        "privacy.html": ("Privacy Policy", "Privacy Policy.", "<div class='container mx-auto px-4 py-16'><h1 class='text-4xl font-extrabold mb-8'>Privacy Policy</h1><p class='text-gray-600'>We protect your data.</p></div>"),
        "terms.html": ("Terms & Conditions", "Terms.", "<div class='container mx-auto px-4 py-16'><h1 class='text-4xl font-extrabold mb-8'>Terms</h1><p class='text-gray-600'>All sales subject to availability.</p></div>"),
        "shipping-policy.html": ("Shipping Policy", "Fast delivery across Pakistan.", "<div class='container mx-auto px-4 py-16'><h1 class='text-4xl font-extrabold mb-8'>Shipping Policy</h1><p class='text-gray-600'>2-4 business days delivery.</p></div>"),
        "return-policy.html": ("Return Policy", "7-day easy returns.", "<div class='container mx-auto px-4 py-16'><h1 class='text-4xl font-extrabold mb-8'>Return Policy</h1><p class='text-gray-600'>7-day return policy.</p></div>"),
        "track-order.html": ("Track Order", "Track your order.", "<div class='container mx-auto px-4 py-16 text-center'><h1 class='text-4xl font-extrabold mb-8'>Track Order</h1><a href='https://wa.me/923425478683' class='bg-green-500 text-white px-8 py-4 rounded-xl font-bold'>Track via WhatsApp</a></div>"),
        "404.html": ("404", "Page not found.", "<div class='container mx-auto px-4 py-20 text-center'><div class='text-9xl font-black text-emerald-600'>404</div><h1 class='text-3xl font-bold my-4'>Page Not Found</h1><a href='/index.html' class='bg-emerald-600 text-white px-8 py-3 rounded-xl font-bold'>Go Home</a></div>"),
        "wishlist.html": ("Wishlist", "My Wishlist.", "<div class='container mx-auto px-4 py-12'><h1 class='text-3xl font-extrabold mb-8'>My Wishlist</h1><div id='wishlistContainer' class='grid grid-cols-3 md:grid-cols-6 gap-3'></div></div><script>function renderWishlist(){let wl=JSON.parse(localStorage.getItem('asm_wishlist'))||[];let c=document.getElementById('wishlistContainer');if(wl.length===0)return;c.innerHTML='';wl.forEach((item,i)=>{let sN=item.name.split(\"'\").join(\"\\\\'\");c.innerHTML+=`<div class='bg-white rounded-lg border p-2'><h3 class='text-xs font-bold mb-2'>${item.name}</h3><p class='text-sm font-black text-emerald-800 mb-2'>Rs ${item.price}</p><div class='flex gap-1'><button onclick=\"addToCart('${sN}', ${item.price}, '${item.image}')\" class='flex-1 bg-emerald-600 text-white py-1.5 rounded-md text-xs'>Add</button><button onclick=\"removeWishlistItem(${i})\" class='flex-1 bg-red-50 text-red-600 py-1.5 rounded-md text-xs'>Remove</button></div></div>`})}function removeWishlistItem(i){let wl=JSON.parse(localStorage.getItem('asm_wishlist'))||[];wl.splice(i,1);localStorage.setItem('asm_wishlist',JSON.stringify(wl));updateWishlistBadge();renderWishlist()}window.addEventListener('load',renderWishlist)</script>"),
        "order-success.html": ("Order Confirmed", "Order successful.", "<div class='container mx-auto px-4 py-20 text-center'><div class='w-24 h-24 mx-auto bg-green-100 rounded-full flex items-center justify-center mb-6'><i class='fas fa-check text-5xl text-green-600'></i></div><h1 class='text-3xl font-extrabold mb-4'>Order Confirmed!</h1><p>Order ID: <span id='orderId' class='font-bold text-emerald-600'>ASM-XXXX</span></p><a href='/index.html' class='mt-8 inline-block bg-emerald-600 text-white px-8 py-3 rounded-xl font-bold'>Continue Shopping</a></div><script>document.getElementById('orderId').innerText='ASM-'+Math.floor(100000+Math.random()*900000);localStorage.removeItem('asm_cart');updateCartBadge()</script>"),
    }

    for filename, (title, desc, content) in static_pages.items():
        sitemap_urls.append(f"https://www.asmveo.com/{filename}")
        html = get_html_header(title, cat_slug_map, desc) + content + get_html_footer(cat_slug_map)
        with open(f"output/{filename}", "w", encoding="utf-8") as f: f.write(minify_html(html))

# ==================== MAIN PROCESSOR ====================

def process_woocommerce_csv():
    file_path = "woocommerce-products-export.csv"
    if not os.path.exists(file_path): return
        
    if os.path.exists("output"): shutil.rmtree("output")
    os.makedirs("output/category", exist_ok=True)
    os.makedirs("output/product", exist_ok=True)
    
    with open("output/CNAME", "w") as f: f.write("www.asmveo.com")
    
    products_list, categories_set = [], set()
    sitemap_urls = ["https://www.asmveo.com/", "https://www.asmveo.com/checkout.html"]
    
    with open(file_path, mode='r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            name = row.get('Name', '').strip()
            images_raw = row.get('Images', '').strip()
            if not name or not images_raw: continue 
            images = [img.strip() for img in images_raw.split(',') if img.strip()]
            base_price = get_price(row.get('Sale price', '') or row.get('Regular price', ''))
            if base_price == 0: continue
            
            final_price = math.ceil(base_price * 1.30)
            fake_regular_price = math.ceil(final_price * 1.61) 
            cat_raw = row.get('Categories', 'Uncategorized')
            category = cat_raw.split(',')[0].strip() if cat_raw else 'Exclusive Collection'
            categories_set.add(category)
            
            slug = make_slug(name) + f"-{row.get('ID', str(len(products_list)+1))}"
            sitemap_urls.append(f"https://www.asmveo.com/product/{slug}.html")
            products_list.append({'slug': slug, 'name': name, 'category': category, 'fake_price': fake_regular_price, 'final_price': final_price, 'image': images[0], 'images': images, 'seo_desc': local_seo_desc(name, clean_html(row.get('Short description', ''))), 'full_desc': clean_html(row.get('Short description', ''))})

    cat_slug_map = {cat: make_slug(cat) for cat in sorted(list(categories_set))}
    print(f"✔ Total {len(products_list)} products being processed...")
    
    generate_static_pages(cat_slug_map, sitemap_urls)
    generate_robots_txt()
    generate_manifest()
    
    # PRODUCT PAGES
    for i, prod in enumerate(products_list):
        reviews_section, avg_rating, review_count = generate_reviews(prod['name'])
        related_html = "".join([generate_product_card(p, lazy=True) for p in [p for p in products_list if p['category'] == prod['category'] and p['slug'] != prod['slug']][:4]])
        
        prod_html = get_html_header(prod['name'], cat_slug_map, prod['seo_desc'], product_data={**prod, 'rating': avg_rating, 'review_count': review_count}, breadcrumb_data={'category': prod['category'], 'name': prod['name'], 'slug': prod['slug']}, og_image=prod['image'])
        
        discount_pct = math.ceil(((prod['fake_price'] - prod['final_price']) / prod['fake_price']) * 100) if prod['fake_price'] > 0 and prod['fake_price'] > prod['final_price'] else 0
        escaped_name = prod['name'].replace("'", "\\'")
        
        prod_html += f"""
        <div class="container mx-auto px-4 py-10">
            <nav class="text-sm text-gray-600 mb-6 bg-gray-100 p-3 rounded-lg inline-block"><a href="/index.html">Home</a> &gt; <a href="/category/{cat_slug_map[prod['category']]}.html">{prod['category']}</a> &gt; <span class="text-emerald-800">{prod['name']}</span></nav>
            <div class="bg-white rounded-3xl shadow-xl border overflow-hidden flex flex-col md:flex-row mb-12 reveal">
                <div class="md:w-1/2 p-6 flex flex-col justify-center items-center bg-gray-50 relative">
                    {f'<div class="absolute top-4 left-4 bg-red-600 text-white text-sm font-black px-3 py-1.5 rounded-lg z-10">-{discount_pct}% OFF</div>' if discount_pct > 0 else ''}
                    <img src="{prod['image']}" alt="{prod['name']}" class="max-h-[500px] object-contain rounded-xl">
                </div>
                <div class="md:w-1/2 p-8 md:p-12 flex flex-col justify-center">
                    <h1 class="text-3xl font-extrabold mb-4">{prod['name']}</h1>
                    <div class="flex items-center gap-4 mb-4 bg-gray-50 p-4 rounded-2xl w-fit"><span class="text-4xl font-black text-emerald-800">Rs {prod['final_price']}</span><span class="text-xl text-gray-500 line-through">Rs {prod['fake_price']}</span></div>
                    <p class="text-gray-700 mb-8 border-t pt-6">{prod['full_desc'][:500]}</p>
                    <div class="flex gap-4 w-full md:w-5/6 mt-auto main-product-actions">
                        <button onclick="addToCart('{escaped_name}', {prod['final_price']}, '{prod['image']}', event)" class="sm:w-1/2 bg-white text-emerald-700 py-4 rounded-xl font-black text-lg border-2 border-emerald-600 hover:bg-emerald-50">Add to Cart</button>
                        <button onclick="buyNow('{escaped_name}', {prod['final_price']}, '{prod['image']}', event)" class="sm:w-1/2 bg-emerald-600 text-white py-4 rounded-xl font-black text-lg hover:bg-emerald-700">Buy Now</button>
                    </div>
                </div>
            </div>
            {"<div class='bg-white rounded-3xl shadow-lg p-8 mb-8'><h2 class='text-2xl font-extrabold mb-6'>You May Also Like</h2><div class='grid grid-cols-2 md:grid-cols-4 gap-4'>" + related_html + "</div></div>" if related_html else ""}
            <div class="bg-white rounded-3xl shadow-lg p-8 mb-8"><h2 class="text-2xl font-extrabold mb-6">Customer Reviews ({review_count})</h2><div>{reviews_section}</div></div>
        </div>
        <div id="stickyAddToCart" class="hidden fixed bottom-16 left-0 right-0 bg-white shadow-2xl p-3 z-40 flex items-center justify-between md:hidden">
            <span class="text-lg font-black text-emerald-800">Rs {prod['final_price']}</span>
            <button onclick="addToCart('{escaped_name}', {prod['final_price']}, '{prod['image']}', event)" class="bg-emerald-600 text-white px-4 py-2.5 rounded-lg font-bold text-sm">Add to Cart</button>
        </div>
        <script>
            let stickyBar = document.getElementById('stickyAddToCart');
            let mainActions = document.querySelector('.main-product-actions');
            window.addEventListener('scroll', () => {{ if (mainActions) {{ let rect = mainActions.getBoundingClientRect(); if (rect.bottom < 0) stickyBar.classList.remove('hidden'); else stickyBar.classList.add('hidden'); }} }});
        </script>
        """
        with open(f"output/product/{prod['slug']}.html", "w", encoding="utf-8") as f: f.write(minify_html(prod_html + get_html_footer(cat_slug_map)))

    # CATEGORY PAGES (WITH LOAD MORE FEATURE)
    sections_dict = {}
    for p in products_list:
        if p['category'] not in sections_dict: sections_dict[p['category']] = []
        sections_dict[p['category']].append(p)

    search_index_json = json.dumps([{"name": p['name'], "slug": p['slug'], "category": p['category'], "final_price": p['final_price'], "fake_price": p['fake_price'], "image": p['image']} for p in products_list])
    with open("output/search-data.js", "w", encoding="utf-8") as f: f.write(f"let searchIndex = {search_index_json};")

    home_html = get_html_header("Home - Premium Online Shopping in Pakistan", cat_slug_map)
    home_html += """
    <div id="heroCarousel" class="relative w-full h-[250px] md:h-[350px] overflow-hidden shadow-xl">
        <div class="carousel-track h-full">
            <div class="carousel-slide h-full bg-emerald-700 flex items-center p-6 md:p-16 text-white"><div class="z-10"><span class="bg-yellow-400 text-black text-xs px-3 py-1 rounded-full">MEGA SALE</span><h2 class="text-2xl md:text-4xl font-extrabold mt-3">Flat 50% OFF</h2><a href="#products" class="inline-block mt-4 bg-white text-emerald-700 px-6 py-2 rounded-lg font-bold">Shop Now</a></div></div>
            <div class="carousel-slide h-full bg-gray-900 flex items-center p-6 md:p-16 text-white"><div class="z-10"><span class="bg-emerald-500 text-xs px-3 py-1 rounded-full">NEW ARRIVALS</span><h2 class="text-2xl md:text-4xl font-extrabold mt-3">Latest Gadgets</h2><a href="#products" class="inline-block mt-4 bg-emerald-600 px-6 py-2 rounded-lg font-bold">Explore</a></div></div>
        </div>
        <button onclick="prevSlide()" class="absolute left-2 top-1/2 -translate-y-1/2 bg-black/40 text-white w-10 h-10 rounded-full z-20">&lt;</button>
        <button onclick="nextSlide()" class="absolute right-2 top-1/2 -translate-y-1/2 bg-black/40 text-white w-10 h-10 rounded-full z-20">&gt;</button>
    </div>
    <script>let si=0;const s=document.querySelectorAll('.carousel-slide');function uC(){{document.querySelector('.carousel-track').style.transform=`translateX(-${{si*100}}%)`}}function nextSlide(){{si=(si+1)%s.length;uC()}}function prevSlide(){{si=(si-1+s.length)%s.length;uC()}}setInterval(nextSlide,3000)</script>
    """
    home_html += f"""
    <div class='container mx-auto px-4 py-4' id="products">
        <div id="searchResultsSection" class="hidden mb-6"><h2 id="searchResultsHeading" class="text-2xl font-extrabold text-emerald-800 mb-2"></h2><p id="searchResultsCount" class="text-gray-500 text-sm"></p></div>
        <div id="defaultContent">
    """
    
    for cat_name, prods in list(sections_dict.items())[:6]:
        cat_slug = cat_slug_map[cat_name]
        sitemap_urls.append(f"https://www.asmveo.com/category/{cat_slug}.html")
        
        cat_html = get_html_header(cat_name, cat_slug_map, f"Buy {cat_name} online in Pakistan at best prices. Wide range of {cat_name} with Cash on Delivery.")
        cat_html += f"""
        <div class="bg-emerald-600 py-12 mb-8 text-center text-white"><h1 class="text-3xl font-black">{cat_name}</h1><p class="mt-3 font-bold">{len(prods)} Products Available</p></div>
        <div class="container mx-auto px-4 pb-12">
            <div id="productGrid" class="grid grid-cols-3 md:grid-cols-6 gap-3 md:gap-4">
        """
        for prod in prods[:12]: cat_html += generate_product_card(prod, lazy=False)
        cat_html += "</div>"
        
        if len(prods) > 12:
            all_prods_json = json.dumps([{"name": p['name'], "slug": p['slug'], "category": p['category'], "final_price": p['final_price'], "fake_price": p['fake_price'], "image": p['image']} for p in prods[12:]])
            cat_html += f"""
                <div class="text-center mt-8"><button id="loadMoreBtn" onclick="loadMore()" class="bg-gray-100 text-emerald-700 px-8 py-3 rounded-xl font-bold hover:bg-gray-200">Load More Products</button></div>
                <script>
                    let remainingProducts = {all_prods_json};
                    let isLoading = false;
                    function loadMore() {{
                        if (isLoading || remainingProducts.length === 0) return;
                        isLoading = true;
                        let btn = document.getElementById('loadMoreBtn');
                        btn.innerText = 'Loading...';
                        
                        let batch = remainingProducts.splice(0, 12);
                        let grid = document.getElementById('productGrid');
                        
                        batch.forEach(p => {{
                            let discount = Math.ceil(((p.fake_price - p.final_price) / p.fake_price) * 100);
                            let safeName = p.name.split("'").join("\\'");
                            grid.insertAdjacentHTML('beforeend', `<div class="product-card reveal active bg-white rounded-lg shadow-sm border overflow-hidden flex flex-col relative cursor-pointer" onclick="window.location.href='/product/${{p.slug}}.html'"><div class="image-zoom h-40 skeleton overflow-hidden border-b flex items-center justify-center"><img src="${{p.image}}" alt="${{p.name}}" loading="lazy" class="w-full h-full object-contain p-1 opacity-0" onload="this.style.opacity=1;this.parentElement.classList.remove('skeleton')" onerror="this.src='https://via.placeholder.com/200/047857/ffffff?text=ASM'"></div><div class="p-2 flex flex-col flex-grow"><span class="text-[9px] font-bold text-emerald-700 uppercase mb-1">${{p.category}}</span><h3 class="text-[10px] font-bold mb-1 line-clamp-2">${{p.name}}</h3><div class="mt-auto"><div class="flex items-center gap-1 mb-1"><span class="text-xs font-black text-emerald-800">Rs ${{p.final_price}}</span><span class="text-[9px] text-gray-400 line-through">Rs ${{p.fake_price}}</span></div><button onclick="addToCart('${{safeName}}', ${{p.final_price}}, '${{p.image}}', event)" class="w-full bg-gray-50 text-emerald-700 py-1.5 rounded-md text-[10px] font-bold border hover:bg-emerald-100">Add to Cart</button></div></div></div>`);
                        }});
                        
                        if (remainingProducts.length === 0) btn.style.display = 'none';
                        else btn.innerText = 'Load More Products';
                        isLoading = false;
                    }}
                </script>
            """
        
        cat_html += "</div>" + get_html_footer(cat_slug_map)
        with open(f"output/category/{cat_slug}.html", "w", encoding="utf-8") as f: f.write(minify_html(cat_html))
        
        home_html += f"""
        <div class="mb-14 category-section reveal">
            <div class="flex justify-between items-center mb-6"><h2 class="text-2xl font-black border-l-4 border-emerald-600 pl-4">{cat_name}</h2><a href="/category/{cat_slug}.html" class="text-emerald-700 font-bold text-sm bg-gray-50 px-5 py-2.5 rounded-full hover:bg-emerald-700 hover:text-white">View All</a></div>
            <div class="grid grid-cols-3 md:grid-cols-6 gap-3 md:gap-4">
        """
        for prod in prods[:6]: home_html += generate_product_card(prod, lazy=True)
        home_html += "</div></div>"
    
    home_html += "</div></div>"
    
    home_script = """
    <script>
        function performSearch(query) {
            if (typeof searchIndex === 'undefined') { loadSearchData(); setTimeout(() => performSearch(query), 500); return; }
            query = query.toLowerCase().trim();
            if (!query) { document.getElementById('defaultContent').classList.remove('hidden'); document.getElementById('searchResultsSection').classList.add('hidden'); return; }
            let results = searchIndex.filter(p => p.name.toLowerCase().includes(query) || p.category.toLowerCase().includes(query));
            document.getElementById('defaultContent').classList.add('hidden');
            document.getElementById('searchResultsSection').classList.remove('hidden');
            document.getElementById('searchResultsHeading').innerText = 'Search Results for "' + query + '"';
            document.getElementById('searchResultsCount').innerText = results.length + ' products found';
            let html = '<div class="grid grid-cols-3 md:grid-cols-6 gap-3 md:gap-4 mt-6">';
            results.forEach(p => {
                let safeName = p.name.split("'").join("\\'");
                html += `<div class="product-card reveal active bg-white rounded-lg shadow-sm border overflow-hidden flex flex-col relative cursor-pointer" onclick="window.location.href='/product/${p.slug}.html'"><div class="image-zoom h-40 skeleton overflow-hidden border-b flex items-center justify-center"><img src="${p.image}" alt="${p.name}" loading="lazy" class="w-full h-full object-contain p-1 opacity-0" onload="this.style.opacity=1;this.parentElement.classList.remove('skeleton')" onerror="this.src='https://via.placeholder.com/200/047857/ffffff?text=ASM'"></div><div class="p-2 flex flex-col flex-grow"><span class="text-[9px] font-bold text-emerald-700 uppercase mb-1">${p.category}</span><h3 class="text-[10px] font-bold mb-1 line-clamp-2">${p.name}</h3><div class="mt-auto"><div class="flex items-center gap-1 mb-1"><span class="text-xs font-black text-emerald-800">Rs ${p.final_price}</span></div><button onclick="addToCart('${safeName}', ${p.final_price}, '${p.image}', event)" class="w-full bg-gray-50 text-emerald-700 py-1.5 rounded-md text-[10px] font-bold border hover:bg-emerald-100">Add to Cart</button></div></div></div>`;
            });
            document.getElementById('searchResultsSection').innerHTML += html;
        }
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('search')) { document.getElementById('searchInput').value = urlParams.get('search'); loadSearchData(); setTimeout(() => performSearch(urlParams.get('search')), 1000); }
    </script>
    """
    home_html += home_script + get_html_footer(cat_slug_map)
    with open("output/index.html", "w", encoding="utf-8") as f: f.write(minify_html(home_html))

    # CHECKOUT PAGE
    checkout_html = get_html_header("Secure Checkout", cat_slug_map)
    checkout_html += """
    <div class="container mx-auto px-4 py-12 max-w-6xl">
        <h1 class="text-3xl font-extrabold mb-8">Secure Checkout</h1>
        <div class="flex flex-col lg:flex-row gap-8">
            <div class="lg:w-1/2"><div class="bg-white rounded-3xl shadow-xl p-6 border mb-6"><h2 class="text-2xl font-black mb-4 border-b pb-4">Your Items</h2><div id="cartItemsContainer" class="space-y-4 max-h-[400px] overflow-y-auto pr-2"></div></div></div>
            <div class="lg:w-1/2">
                <div class="bg-emerald-600 p-6 rounded-t-3xl text-white"><h1 class="text-2xl font-extrabold">Shipping Details</h1></div>
                <form id="checkoutForm" class="bg-white p-6 md:p-8 rounded-b-3xl shadow-xl border space-y-5">
                    <input type="hidden" name="_subject" value="New Order!"><input type="hidden" name="Product_Ordered" id="productField" value=""><input type="hidden" name="Order_Total" id="totalField" value="">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <div><label class="block text-sm font-bold mb-2">Full Name</label><input type="text" name="Full_Name" class="w-full border-2 p-3 rounded-xl bg-gray-50 focus:border-emerald-600 outline-none" required></div>
                        <div><label class="block text-sm font-bold mb-2">Mobile Number</label><input type="tel" name="Phone_Number" class="w-full border-2 p-3 rounded-xl bg-gray-50 focus:border-emerald-600 outline-none" required></div>
                    </div>
                    <div><label class="block text-sm font-bold mb-2">Address</label><textarea name="Address" rows="3" class="w-full border-2 p-3 rounded-xl bg-gray-50 focus:border-emerald-600 outline-none" required></textarea></div>
                    <div class="bg-gray-50 rounded-2xl p-5 border mt-6">
                        <div class="flex justify-between text-sm font-bold mb-2"><span>Subtotal</span><span id="subtotalDisplay">Rs 0</span></div>
                        <div class="flex justify-between text-sm font-bold mb-2"><span>Delivery</span><span id="deliveryDisplay">Rs 250</span></div>
                        <div class="flex justify-between items-center border-t pt-3 mt-3"><span class="font-black text-lg">Total (COD)</span><span class="font-black text-2xl text-emerald-800" id="grandTotalDisplay">Rs 250</span></div>
                    </div>
                    <button type="submit" id="submitBtn" class="w-full bg-emerald-600 text-white font-black py-4 rounded-xl hover:bg-emerald-700 transition-all shadow-xl text-lg">Confirm Order</button>
                </form>
            </div>
        </div>
    </div>
    <script>
        function renderCart() {
            const urlParams = new URLSearchParams(window.location.search);
            const isBuyNow = urlParams.get('buy_now') === 'true';
            const pName = urlParams.get('product');
            const pPrice = parseInt(urlParams.get('price')) || 0;
            let subtotal = 0; let finalOrderString = ""; let container = document.getElementById('cartItemsContainer'); container.innerHTML = '';
            if (isBuyNow && pName && pPrice) {
                subtotal = pPrice; finalOrderString = "1x " + pName + " (Rs " + pPrice + ")";
                container.innerHTML = `<div class="flex items-center gap-4 bg-gray-50 p-3 rounded-xl border"><div class="flex-1"><h3 class="font-bold line-clamp-1">${pName}</h3><p class="text-emerald-700 font-black">Rs ${pPrice}</p></div></div>`;
            } else {
                let cart = getCart();
                if(cart.length === 0) { container.innerHTML = `<p class='text-center py-8 text-gray-500'>Cart is empty.</p>`; document.getElementById('submitBtn').disabled = true; }
                else { cart.forEach((item, index) => { let qty = item.qty || 1; subtotal += parseInt(item.price) * qty; finalOrderString += qty + "x " + item.name + " (Rs " + (item.price * qty) + ")\\n"; container.innerHTML += `<div class="flex items-center gap-3 bg-gray-50 p-3 rounded-xl border"><img src="${item.image}" class="w-16 h-16 object-contain rounded-lg bg-white p-1"><div class="flex-1"><h3 class="font-bold text-sm line-clamp-2">${item.name}</h3><p class="text-emerald-700 font-black text-sm">Rs ${item.price}</p><div class="flex items-center gap-2 mt-1"><button onclick="updateQty(${index}, -1)" class="w-6 h-6 bg-gray-200 rounded font-bold">-</button><span class="font-bold text-sm">${qty}</span><button onclick="updateQty(${index}, 1)" class="w-6 h-6 bg-gray-200 rounded font-bold">+</button><button onclick="removeFromCart(${index})" class="ml-2 text-red-500 text-xs"><i class="fas fa-trash"></i></button></div></div></div>`; }); }
            }
            let delivery = subtotal >= 5000 ? 0 : 250; let grandTotal = subtotal + delivery;
            document.getElementById('subtotalDisplay').innerText = "Rs " + subtotal;
            document.getElementById('deliveryDisplay').innerText = delivery === 0 ? "FREE" : "Rs " + delivery;
            document.getElementById('grandTotalDisplay').innerText = "Rs " + grandTotal;
            document.getElementById('productField').value = finalOrderString + "\\nDelivery: Rs " + delivery + "\\nGrand Total: Rs " + grandTotal;
        }
        document.getElementById('checkoutForm').addEventListener('submit', function(e) {
            e.preventDefault(); const btn = document.getElementById('submitBtn'); btn.innerHTML = 'Processing...'; btn.disabled = true;
            fetch('https://formspree.io/f/xjgnlgpw', { method: 'POST', body: new FormData(this), headers: { 'Accept': 'application/json' } })
            .then(r => { if (r.ok) { if(new URLSearchParams(window.location.search).get('buy_now') !== 'true') localStorage.removeItem('asm_cart'); updateCartBadge(); window.location.href = '/order-success.html'; } else { btn.innerHTML = 'Confirm Order'; btn.disabled = false; } })
            .catch(e => { btn.innerHTML = 'Confirm Order'; btn.disabled = false; });
        });
        window.addEventListener('load', renderCart);
    </script>
    """
    with open("output/checkout.html", "w", encoding="utf-8") as f: f.write(minify_html(checkout_html + get_html_footer(cat_slug_map)))
        
    generate_sitemap(sitemap_urls)
    print("🎉 Website generated successfully with Load More Feature & Extreme Minification!")

if __name__ == "__main__":
    process_woocommerce_csv()
