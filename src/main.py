import os
import csv
import math
import re
import shutil
import random

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
        return desc[:120] + "..."
    return f"Buy {name} online in Pakistan at the best price. Premium quality with Cash on Delivery."

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
    for _ in range(random.randint(3, 7)): # ہر پروڈکٹ پر 3 سے 7 ریویوز
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
        .product-card:hover {{ transform: translateY(-8px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }}
        .image-zoom img {{ transition: transform 0.5s ease; }}
        .product-card:hover .image-zoom img {{ transform: scale(1.1); }}
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
                <input type="text" id="searchInput" onkeyup="searchProducts()" placeholder="Search products..." class="w-full bg-gray-100 border border-gray-200 focus:border-teal-500 rounded-full py-2.5 px-6 outline-none transition-all">
                <button class="absolute right-4 top-2.5 text-gray-500 hover:text-teal-600"><i class="fas fa-search text-lg"></i></button>
            </div>
            
            <a href="/checkout.html" class="bg-gray-900 text-white px-5 py-2.5 rounded-full font-bold hover:bg-teal-600 transition-colors shadow-lg flex items-center gap-2 whitespace-nowrap">
                <i class="fas fa-truck-fast"></i> <span class="hidden md:inline">Track Order</span>
            </a>
        </div>
    </header>
    
    <script>
    function searchProducts() {{
        let input = document.getElementById('searchInput').value.toLowerCase();
        let cards = document.getElementsByClassName('product-card');
        for (let i = 0; i < cards.length; i++) {{
            let title = cards[i].querySelector('h3').innerText.toLowerCase();
            if (title.includes(input)) {{
                cards[i].style.display = "";
            }} else {{
                cards[i].style.display = "none";
            }}
        }}
    }}
    </script>
"""

def get_html_footer():
    return """
    <!-- Footer -->
    <footer class="bg-gray-900 text-white mt-16 pt-12 pb-6 border-t-4 border-teal-500">
        <div class="container mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            <div>
                <h3 class="text-xl font-bold mb-4 flex items-center gap-2"><i class="fas fa-shopping-bag text-teal-400"></i> ASM VEO</h3>
                <p class="text-gray-400 text-sm leading-relaxed">Your premium destination for high-quality products. Nationwide Cash on Delivery with a secure shopping experience.</p>
            </div>
            <div>
                <h3 class="text-lg font-bold mb-4">Management & Contact</h3>
                <ul class="space-y-3 text-gray-400 text-sm">
                    <li class="flex items-center gap-2"><i class="fas fa-user-tie text-teal-400"></i> CEO: Ali Abbas</li>
                    <li class="flex items-center gap-2"><i class="fas fa-building text-teal-400"></i> ASM Digital Solutions</li>
                    <li class="flex items-center gap-2"><i class="fab fa-whatsapp text-green-500 text-lg"></i> <a href="https://wa.me/923425478683" class="hover:text-white transition">0342 54 786 83</a></li>
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

def process_woocommerce_csv():
    file_path = "woocommerce-products-export.csv"
    if not os.path.exists(file_path):
        print("❌ CSV File Not Found!")
        return
        
    print("🚀 سکرپٹ شروع ہو گئی ہے! پرانا ڈیٹا ڈیلیٹ کیا جا رہا ہے...")
    
    # 1. پرانی فائلز کو جڑ سے ختم کرنا
    if os.path.exists("output"):
        shutil.rmtree("output")
    os.makedirs("output/category", exist_ok=True)
    os.makedirs("output/product", exist_ok=True)
    
    with open("output/CNAME", "w") as f:
        f.write("www.asmveo.com")
    
    products_list = []
    categories_set = set()
    
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            if not name: continue
                
            base_price = get_price(row.get('Sale price', '') or row.get('Regular price', ''))
            if base_price == 0: continue
            final_price = math.ceil(base_price * 1.30)
            
            cat_raw = row.get('Categories', 'Uncategorized')
            category = cat_raw.split(',')[0].strip() if cat_raw else 'Hot Items'
            categories_set.add(category)
            
            images_raw = row.get('Images', '')
            image = images_raw.split(',')[0].strip() if images_raw else 'https://via.placeholder.com/500'
            
            desc_raw = row.get('Short description', '') or row.get('Description', '')
            clean_description = clean_html(desc_raw)
            seo_desc = local_seo_desc(name, clean_description)
            
            product_id = row.get('ID', str(len(products_list)+1))
            slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-') + f"-{product_id}"
            
            products_list.append({
                'id': product_id,
                'slug': slug,
                'name': name,
                'category': category,
                'base_price': int(base_price),
                'final_price': final_price,
                'image': image,
                'seo_desc': seo_desc,
                'full_desc': clean_description
            })

    print(f"✔ کل {len(products_list)} پروڈکٹس پراسیس ہو رہی ہیں...")
    
    # ================= 2. GENERATE PRODUCT PAGES =================
    for prod in products_list:
        prod_html = get_html_header(prod['name'])
        reviews_section = generate_reviews(prod['name'])
        
        prod_html += f"""
        <div class="container mx-auto px-4 py-10">
            <nav class="text-sm text-gray-500 mb-6">
                <a href="/index.html" class="hover:text-teal-600">Home</a> &gt; 
                <a href="/category/{re.sub(r'[^a-z0-9]+', '-', prod['category'].lower())}.html" class="hover:text-teal-600">{prod['category']}</a> &gt; 
                <span class="text-gray-800">{prod['name']}</span>
            </nav>
            
            <div class="bg-white rounded-3xl shadow-lg border border-gray-100 overflow-hidden flex flex-col md:flex-row mb-12">
                <div class="md:w-1/2 p-6 flex justify-center items-center bg-gray-50">
                    <img src="{prod['image']}" alt="{prod['name']}" class="max-h-[500px] object-contain rounded-xl hover:scale-105 transition duration-500">
                </div>
                <div class="md:w-1/2 p-8 md:p-12 flex flex-col justify-center">
                    <span class="text-xs font-bold uppercase tracking-widest text-teal-600 mb-2">{prod['category']}</span>
                    <h1 class="text-3xl md:text-4xl font-extrabold text-gray-900 mb-4">{prod['name']}</h1>
                    
                    <div class="flex items-center gap-3 mb-6">
                        <div class="text-yellow-400 text-sm"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star-half-alt"></i></div>
                        <span class="text-sm text-gray-500">(Multiple Customer Reviews)</span>
                    </div>

                    <div class="flex items-center gap-4 mb-6">
                        <span class="text-4xl font-black text-gray-900">Rs {prod['final_price']}</span>
                        <span class="text-xl text-gray-400 line-through">Rs {prod['base_price']}</span>
                    </div>
                    
                    <div class="mb-6">
                        <label class="block text-sm font-bold text-gray-700 mb-2">Select Size / Variation (If Applicable)</label>
                        <select class="w-full md:w-2/3 border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-teal-500">
                            <option>Standard / Free Size</option>
                            <option>Small (S)</option>
                            <option>Medium (M)</option>
                            <option>Large (L)</option>
                        </select>
                    </div>

                    <p class="text-gray-600 mb-8 leading-relaxed">{prod['full_desc'][:300] if len(prod['full_desc']) > 50 else prod['seo_desc']}</p>
                    
                    <a href="/checkout.html?product={prod['name'].replace(' ', '%20')}&price={prod['final_price']}" class="bg-teal-600 text-white text-center py-4 rounded-xl font-bold text-lg hover:bg-gray-900 transition shadow-lg w-full md:w-2/3 transform hover:-translate-y-1">
                        <i class="fas fa-shopping-cart mr-2"></i> Order Now (COD)
                    </a>
                </div>
            </div>
            
            <!-- Reviews Section -->
            <div class="bg-white rounded-3xl shadow-lg border border-gray-100 p-8">
                <h2 class="text-2xl font-extrabold text-gray-900 mb-6 border-b pb-4">Customer Reviews for {prod['name']}</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div>
                        {reviews_section}
                    </div>
                    <div class="bg-gray-50 p-6 rounded-2xl h-fit border border-gray-200">
                        <h3 class="font-bold text-lg mb-2">Write a Review</h3>
                        <p class="text-sm text-gray-500 mb-4">Only verified buyers can leave a review after receiving the product.</p>
                        <div class="flex items-center gap-2 text-teal-600 font-bold">
                            <i class="fas fa-lock"></i> Review form is currently locked.
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """ + get_html_footer()
        
        with open(f"output/product/{prod['slug']}.html", "w", encoding="utf-8") as f:
            f.write(prod_html)

    # ================= 3. GENERATE HOME & CATEGORY PAGES =================
    sections_dict = {}
    for p in products_list:
        c = p['category']
        if c not in sections_dict: sections_dict[c] = []
        sections_dict[c].append(p)

    home_html = get_html_header("Home")
    home_html += "<div class='container mx-auto px-4 py-8'>"
    
    for cat_name, prods in sections_dict.items():
        cat_slug = re.sub(r'[^a-z0-9]+', '-', cat_name.lower())
        
        # Category Page Build
        cat_html = get_html_header(cat_name)
        cat_html += f"""
        <div class="bg-gray-100 py-8 mb-8 border-b border-gray-200">
            <div class="container mx-auto px-4">
                <h1 class="text-3xl font-extrabold text-gray-900">{cat_name}</h1>
                <p class="text-gray-500 mt-2 font-medium">{len(prods)} Products Found</p>
            </div>
        </div>
        <div class="container mx-auto px-4 pb-12"><div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
        """
        
        home_html += f"""
        <div class="mb-12">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl font-extrabold text-gray-800 border-l-4 border-teal-500 pl-3">{cat_name}</h2>
                <a href="/category/{cat_slug}.html" class="text-teal-600 font-bold text-sm bg-teal-50 px-4 py-2 rounded-full hover:bg-teal-100 transition">See All <i class="fas fa-chevron-right ml-1"></i></a>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
        """
        
        for idx, prod in enumerate(prods):
            card_ui = f"""
                <div class="product-card bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col relative cursor-pointer" onclick="window.location.href='/product/{prod['slug']}.html'">
                    <div class="absolute top-3 right-3 bg-red-500 text-white text-[10px] font-black px-2 py-1 rounded-md z-10 shadow-md">30% OFF</div>
                    <div class="image-zoom h-48 md:h-60 bg-gray-100 overflow-hidden relative">
                        <img src="{prod['image']}" alt="{prod['name']}" class="w-full h-full object-cover" loading="lazy">
                    </div>
                    <div class="p-4 flex flex-col flex-grow">
                        <h3 class="text-sm md:text-base font-bold text-gray-900 leading-tight mb-2 line-clamp-2">{prod['name']}</h3>
                        <div class="mt-auto">
                            <div class="flex items-center gap-2 mb-3">
                                <span class="text-lg md:text-xl font-extrabold text-gray-900">Rs {prod['final_price']}</span>
                                <span class="text-xs text-gray-400 line-through">Rs {prod['base_price']}</span>
                            </div>
                            <button class="block text-center bg-teal-600 text-white py-2 rounded-xl text-sm font-bold hover:bg-gray-900 transition-colors w-full">
                                View Details
                            </button>
                        </div>
                    </div>
                </div>
            """
            cat_html += card_ui
            if idx < 8: home_html += card_ui # Home page par sirf 8 products per category
            
        cat_html += "</div></div>" + get_html_footer()
        with open(f"output/category/{cat_slug}.html", "w", encoding="utf-8") as f:
            f.write(cat_html)
            
        home_html += "</div></div>"
    
    home_html += "</div>" + get_html_footer()
    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(home_html)

    # ================= 4. GENERATE CHECKOUT PAGE (Formspree + Notifications) =================
    pak_cities = ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Multan", "Peshawar", "Quetta", "Gujranwala", "Sialkot", "Hyderabad", "Bahawalpur", "Sargodha", "Other"]
    city_options = "".join([f"<option value='{city}'>{city}</option>" for city in pak_cities])
    
    checkout_html = get_html_header("Secure Checkout")
    checkout_html += f"""
    <div class="container mx-auto px-4 py-12 max-w-3xl">
        <div class="bg-white rounded-3xl shadow-2xl overflow-hidden border border-gray-100">
            <div class="bg-gray-900 p-8 text-center text-white relative">
                <div class="absolute top-0 left-0 w-full h-1 bg-teal-500"></div>
                <h1 class="text-3xl font-extrabold"><i class="fas fa-box-open mr-2 text-teal-400"></i> Cash on Delivery Checkout</h1>
                <p class="text-gray-400 mt-2 text-sm font-medium">Please fill in your details to confirm the order.</p>
            </div>
            
            <form id="checkoutForm" class="p-6 md:p-10 space-y-6">
                <!-- Hidden subject field for Formspree Email Subject -->
                <input type="hidden" name="_subject" value="New Order Received on ASM VEO!">
                <input type="hidden" name="Product_Ordered" id="productField" value="Direct Checkout">
                <input type="hidden" name="Total_Price" id="priceField" value="">

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-2">Full Name <span class="text-red-500">*</span></label>
                        <input type="text" name="Full_Name" class="w-full border-2 border-gray-200 p-3.5 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-500 outline-none" required placeholder="e.g. Ali Abbas">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-2">Email Address (Optional)</label>
                        <input type="email" name="Email" class="w-full border-2 border-gray-200 p-3.5 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-500 outline-none" placeholder="you@example.com">
                    </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-2">Mobile Number <span class="text-red-500">*</span></label>
                        <input type="tel" name="Phone_Number" class="w-full border-2 border-gray-200 p-3.5 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-500 outline-none" required placeholder="0300-XXXXXXX">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-2">City <span class="text-red-500">*</span></label>
                        <select name="City" class="w-full border-2 border-gray-200 p-3.5 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-500 outline-none" required>
                            <option value="" disabled selected>Select your City</option>
                            {city_options}
                        </select>
                    </div>
                </div>
                
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-2">Complete Delivery Address <span class="text-red-500">*</span></label>
                    <textarea name="Address" rows="3" class="w-full border-2 border-gray-200 p-3.5 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-500 outline-none" required placeholder="House No, Street Name, Area..."></textarea>
                </div>
                
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-2">Nearest Landmark (Famous Place)</label>
                    <input type="text" name="Landmark" class="w-full border-2 border-gray-200 p-3.5 rounded-xl bg-gray-50 focus:bg-white focus:border-teal-500 outline-none" placeholder="e.g. Near HBL Bank / Masjid">
                </div>
                
                <div class="mt-8 bg-teal-50 p-5 rounded-2xl border border-teal-100 flex flex-col gap-3">
                    <div class="flex justify-between items-center border-b border-teal-200 pb-3">
                        <span class="font-bold text-gray-700">Subtotal:</span>
                        <span class="font-bold text-gray-900" id="subtotalDisplay">Rs 0</span>
                    </div>
                    <div class="flex justify-between items-center border-b border-teal-200 pb-3">
                        <div class="flex items-center gap-2 text-teal-700">
                            <i class="fas fa-truck-fast"></i> <span class="font-bold">Delivery Charges:</span>
                        </div>
                        <span class="font-bold text-teal-700">Rs 250</span>
                    </div>
                    <div class="flex justify-between items-center pt-2">
                        <span class="font-black text-xl text-gray-900">Total to Pay (COD):</span>
                        <span class="font-black text-2xl text-teal-700" id="grandTotalDisplay">Rs 250</span>
                    </div>
                </div>

                <button type="submit" id="submitBtn" class="w-full bg-teal-600 text-white font-black py-4 px-4 rounded-2xl hover:bg-gray-900 transition-all duration-300 shadow-xl text-lg mt-6 transform hover:-translate-y-1">
                    Confirm Order Now
                </button>
            </form>
        </div>
    </div>
    
    <script>
        // URL se product aur price nikal kar form mein dalna
        const urlParams = new URLSearchParams(window.location.search);
        const productName = urlParams.get('product');
        const productPrice = urlParams.get('price');
        
        if(productName && productPrice) {{
            document.getElementById('productField').value = productName;
            document.getElementById('priceField').value = productPrice;
            document.getElementById('subtotalDisplay').innerText = "Rs " + productPrice;
            document.getElementById('grandTotalDisplay').innerText = "Rs " + (parseInt(productPrice) + 250);
        }}

        // Formspree AJAX Submission Logic
        document.getElementById('checkoutForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            const btn = document.getElementById('submitBtn');
            btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Processing Order...';
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
                    btn.innerHTML = 'Confirm Order Now';
                    btn.disabled = false;
                }}
            }}).catch(error => {{
                alert('Network Error! Please try again.');
                btn.innerHTML = 'Confirm Order Now';
                btn.disabled = false;
            }});
        }});
    </script>
    """
    checkout_html += get_html_footer()
    with open("output/checkout.html", "w", encoding="utf-8") as f:
        f.write(checkout_html)
        
    print("🎉 تمام فائلز اور پیجز کامیابی کے ساتھ نئے سرے سے بن چکے ہیں!")

if __name__ == "__main__":
    process_woocommerce_csv()
