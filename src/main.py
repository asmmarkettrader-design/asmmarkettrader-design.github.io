import os
import json
import requests
from google import genai
from google.genai import errors
from jinja2 import Template

# 1. Gemini API Initialization with Error Handling
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        client = genai.Client(api_key=api_key)
    else:
        print("Warning: GEMINI_API_KEY not found. Script will run without SEO content generation.")
        client = None
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    client = None

def scrape_markaz():
    print("Starting data scraping...")
    try:
        # Yahan Markaz API / scraping ka logic aayega (China items filter, etc.)
        # Abhi ke liye hum dummy data pass kar rahe hain taake script kabhi fail na ho
        dummy_data = {
            "categories": ["Cosmetics", "Womens Fashion", "Mens Fashion", "Home Decor"],
            "products": [
                {"id": 1, "name": "Premium Handbag", "category": "Womens Fashion", "desc": "High quality leather handbag.", "price": "3500"},
                {"id": 2, "name": "Mens Casual Watch", "category": "Mens Fashion", "desc": "Waterproof analog watch.", "price": "1500"}
            ]
        }
        return dummy_data
    except Exception as e:
        print(f"Error during scraping: {e}")
        # Agar scrape fail ho jaye tab bhi khali data bhej do taake site deploy ho jaye
        return {"categories": [], "products": []}

def generate_seo_content(product_name, description):
    if not client:
        return description # Agar API key nahi hai to normal description use karega
    
    try:
        prompt = f"Generate a highly SEO-friendly, fast-loading, short description for an online store named ASM VEO for this product: {product_name} - {description}. Return only plain text, no markdown."
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except errors.APIError as e:
        print(f"Gemini API error for {product_name}: {e}")
        return description
    except Exception as e:
        print(f"Unexpected API error for {product_name}: {e}")
        return description

def build_store(data):
    print("Building static files for ASM VEO store...")
    try:
        # 1. Output aur Categories ke sub-folders khud banaye ga (Error #128 ka permanently khatma)
        os.makedirs("output", exist_ok=True)
        os.makedirs("output/categories", exist_ok=True)
        os.makedirs("output/products", exist_ok=True)

        # 2. CNAME file banaye ga custom domain ke liye
        with open("output/CNAME", "w") as f:
            f.write("www.asmveo.com")

        # 3. Main Index (Home) Page generate karega
        index_html = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ASM VEO Online Store</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f8f9fa; }
                header { background-color: #333; color: white; padding: 10px 20px; text-align: center; }
                .product-list { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; margin-top: 20px;}
                .product-card { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); max-width: 300px;}
            </style>
        </head>
        <body>
            <header>
                <h1>Welcome to ASM VEO Store</h1>
                <p>Premium Products, Delivered Fast</p>
            </header>
            <div class="product-list">
        """

        # API se SEO content la kar products add karega
        if data and data.get("products"):
            for prod in data["products"]:
                seo_desc = generate_seo_content(prod['name'], prod['desc'])
                index_html += f"""
                <div class="product-card">
                    <h3>{prod['name']}</h3>
                    <p><strong>Category:</strong> {prod['category']}</p>
                    <p>{seo_desc}</p>
                    <p style="color: green; font-weight: bold;">Rs {prod['price']}</p>
                    <button style="width: 100%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 5px;">Order via COD</button>
                </div>
                """
        
        index_html += "</div></body></html>"
        
        with open("output/index.html", "w", encoding="utf-8") as f:
            f.write(index_html)

        # 4. Sitemap (SEO aur Crawling ke liye)
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        sitemap += '  <url>\n    <loc>https://www.asmveo.com/</loc>\n  </url>\n'
        
        if data and data.get("categories"):
            for cat in data["categories"]:
                cat_slug = cat.lower().replace(" ", "-").replace("'", "")
                sitemap += f'  <url>\n    <loc>https://www.asmveo.com/categories/{cat_slug}.html</loc>\n  </url>\n'
                
                # Sath hi Category page ki empty/dummy file bhi bana dega taake 404 error na aye
                with open(f"output/categories/{cat_slug}.html", "w", encoding="utf-8") as f:
                    f.write(f"<html><head><title>{cat} - ASM VEO</title></head><body><h1>{cat} Collection</h1><a href='../index.html'>Back to Home</a></body></html>")

        sitemap += '</urlset>'
        
        with open("output/sitemap.xml", "w", encoding="utf-8") as f:
            f.write(sitemap)

        print("✔ Store built successfully! All files are in the 'output' directory.")
        
    except Exception as e:
        print(f"Critical error while building the store: {e}")

def handle_cod_orders():
    print("Checking COD systems...")
    try:
        # COD form submissions ya external order management ka logic yahan hoga
        pass
    except Exception as e:
        print(f"Error handling COD: {e}")

if __name__ == "__main__":
    print("--- ASM VEO Automation Script Started ---")
    scraped_data = scrape_markaz()
    build_store(scraped_data)
    handle_cod_orders()
    print("--- ASM VEO Automation Script Finished ---")
