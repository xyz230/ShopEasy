import os
import logging
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# In-memory product database
with open('models.py', 'r') as f:
    # This will execute the models.py file which includes our product data
    pass

from models import products, categories

# Routes
@app.route('/')
def index():
    """Home page route"""
    featured_products = products[:4]  # First 4 products as featured
    return render_template('index.html', 
                          featured_products=featured_products,
                          categories=categories)

@app.route('/products')
def product_list():
    """Products page route"""
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    filtered_products = products
    
    # Filter by category if provided
    if category:
        filtered_products = [p for p in filtered_products if p['category'] == category]
    
    # Filter by search term if provided
    if search:
        search = search.lower()
        filtered_products = [p for p in filtered_products if search in p['name'].lower() or search in p['description'].lower()]
    
    return render_template('products.html', 
                          products=filtered_products,
                          categories=categories,
                          current_category=category,
                          search_term=search)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page route"""
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        # Get related products (same category)
        related = [p for p in products if p['category'] == product['category'] and p['id'] != product_id][:4]
        return render_template('product_detail.html', product=product, related_products=related)
    return redirect(url_for('product_list'))

@app.route('/cart')
def cart():
    """Shopping cart page route"""
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    """Checkout page route"""
    return render_template('checkout.html')

# API endpoints
@app.route('/api/products')
def api_products():
    """API endpoint to get all products"""
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    filtered_products = products
    
    # Filter by category if provided
    if category:
        filtered_products = [p for p in filtered_products if p['category'] == category]
    
    # Filter by search term if provided
    if search:
        search = search.lower()
        filtered_products = [p for p in filtered_products if search in p['name'].lower() or search in p['description'].lower()]
    
    return jsonify(filtered_products)

@app.route('/api/product/<int:product_id>')
def api_product_detail(product_id):
    """API endpoint to get a single product"""
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
