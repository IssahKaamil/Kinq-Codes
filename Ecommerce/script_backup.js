// Product data with international designs
const products = [
    // DRESSES - International Designs
    {
        id: 1,
        name: "Parisian Floral Summer Dress",
        price: 129.99,
        category: "dresses",
        image: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Elegant French-inspired floral dress with romantic details and perfect fit."
    },
    {
        id: 2,
        name: "Italian Silk Evening Gown",
        price: 299.99,
        category: "dresses",
        image: "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Luxurious Italian silk evening gown with sophisticated Italian tailoring."
    },
    {
        id: 17,
        name: "Japanese Kimono-Inspired Dress",
        price: 159.99,
        category: "dresses",
        image: "https://images.unsplash.com/photo-1551028719-00167b16eac5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Modern kimono-inspired dress with traditional Japanese aesthetics and contemporary style."
    },
    {
        id: 18,
        name: "Moroccan Boho Maxi Dress",
        price: 89.99,
        category: "dresses",
        image: "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Bohemian maxi dress inspired by Moroccan culture with vibrant patterns and flowing design."
    },
    {
        id: 19,
        name: "Scandinavian Minimalist Dress",
        price: 149.99,
        category: "dresses",
        image: "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=705&q=80",
        description: "Clean Scandinavian design with minimalist aesthetics and functional elegance."
    },
    {
        id: 20,
        name: "Indian Sari-Inspired Gown",
        price: 199.99,
        category: "dresses",
        image: "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Elegant gown inspired by traditional Indian sari with modern Western adaptations."
    },

    // TOPS - International Designs
    {
        id: 3,
        name: "French Breton Striped Top",
        price: 69.99,
        category: "tops",
        image: "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=705&q=80",
        description: "Classic French Breton striped top with authentic Parisian style and comfort."
    },
    {
        id: 4,
        name: "Italian Silk Blouse",
        price: 119.99,
        category: "tops",
        image: "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Premium Italian silk blouse with exquisite craftsmanship and luxurious feel."
    },
    {
        id: 21,
        name: "Japanese Origami-Inspired Top",
        price: 89.99,
        category: "tops",
        image: "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2080&q=80",
        description: "Innovative top with origami-inspired pleats and Japanese design philosophy."
    },
    {
        id: 22,
        name: "Mexican Embroidered Blouse",
        price: 79.99,
        category: "tops",
        image: "https://images.unsplash.com/photo-1584917865442-de89df76afd3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2025&q=80",
        description: "Vibrant Mexican embroidered blouse with traditional patterns and modern fit."
    },
    {
        id: 23,
        name: "Nordic Wool Sweater",
        price: 139.99,
        category: "tops",
        image: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Cozy Nordic wool sweater with traditional Scandinavian patterns and warmth."
    },

    // BOTTOMS - International Designs
    {
        id: 5,
        name: "Italian Leather Pants",
        price: 189.99,
        category: "bottoms",
        image: "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Premium Italian leather pants with superior craftsmanship and timeless style."
    },
    {
        id: 6,
        name: "French A-Line Skirt",
        price: 89.99,
        category: "bottoms",
        image: "https://images.unsplash.com/photo-1551028719-00167b16eac5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Classic French A-line skirt with Parisian elegance and perfect proportions."
    },
    {
        id: 24,
        name: "Japanese Denim Jeans",
        price: 159.99,
        category: "bottoms",
        image: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Premium Japanese denim jeans with exceptional quality and perfect fit."
    },
    {
        id: 25,
        name: "Moroccan Palazzo Pants",
        price: 99.99,
        category: "bottoms",
        image: "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Flowing Moroccan palazzo pants with exotic patterns and comfortable fit."
    },

    // LINGERIE - International Designs
    {
        id: 9,
        name: "French Silk Lingerie Set",
        price: 149.99,
        category: "lingerie",
        image: "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Luxurious French silk lingerie set with Parisian sophistication and elegance."
    },
    {
        id: 10,
        name: "Italian Lace Bodysuit",
        price: 119.99,
        category: "lingerie",
        image: "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=705&q=80",
        description: "Exquisite Italian lace bodysuit with premium craftsmanship and romantic design."
    },
    {
        id: 26,
        name: "Japanese Silk Kimono Robe",
        price: 179.99,
        category: "lingerie",
        image: "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2080&q=80",
        description: "Traditional Japanese silk kimono robe with modern comfort and authentic design."
    },
    {
        id: 27,
        name: "Brazilian Lace Teddy",
        price: 89.99,
        category: "lingerie",
        image: "https://images.unsplash.com/photo-1584917865442-de89df76afd3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2025&q=80",
        description: "Sensual Brazilian lace teddy with vibrant energy and flattering fit."
    },

    // BRAS - International Designs
    {
        id: 11,
        name: "French Push-Up Bra",
        price: 69.99,
        category: "bras",
        image: "https://images.unsplash.com/photo-1551028719-00167b16eac5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Sophisticated French push-up bra with perfect support and elegant design."
    },
    {
        id: 12,
        name: "Italian Wireless Bra",
        price: 59.99,
        category: "bras",
        image: "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Comfortable Italian wireless bra with premium materials and superior comfort."
    },
    {
        id: 28,
        name: "Japanese Seamless Bra",
        price: 79.99,
        category: "bras",
        image: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Innovative Japanese seamless bra with advanced technology and invisible comfort."
    },
    {
        id: 29,
        name: "Swiss Cotton Bra",
        price: 49.99,
        category: "bras",
        image: "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Premium Swiss cotton bra with natural materials and breathable comfort."
    },

    // PANTIES - International Designs
    {
        id: 13,
        name: "French Lace Panties",
        price: 39.99,
        category: "panties",
        image: "https://images.unsplash.com/photo-1584917865442-de89df76afd3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2025&q=80",
        description: "Elegant French lace panties with sophisticated design and feminine charm."
    },
    {
        id: 14,
        name: "Italian Cotton Panties Set",
        price: 44.99,
        category: "panties",
        image: "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Comfortable Italian cotton panties set with premium quality and daily comfort."
    },
    {
        id: 30,
        name: "Japanese Silk Panties",
        price: 59.99,
        category: "panties",
        image: "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2080&q=80",
        description: "Luxurious Japanese silk panties with exceptional softness and elegant design."
    },
    {
        id: 31,
        name: "Brazilian Cut Panties",
        price: 34.99,
        category: "panties",
        image: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Sensual Brazilian cut panties with flattering fit and vibrant energy."
    },

    // BIKINI - International Designs
    {
        id: 15,
        name: "French Riviera Bikini",
        price: 89.99,
        category: "bikini",
        image: "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2080&q=80",
        description: "Elegant French Riviera bikini with sophisticated style and beach glamour."
    },
    {
        id: 16,
        name: "Italian Designer Bikini",
        price: 129.99,
        category: "bikini",
        image: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Premium Italian designer bikini with luxury materials and perfect fit."
    },
    {
        id: 32,
        name: "Brazilian Bikini Set",
        price: 79.99,
        category: "bikini",
        image: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Sensual Brazilian bikini set with vibrant colors and flattering cut."
    },
    {
        id: 33,
        name: "Australian Beach Bikini",
        price: 69.99,
        category: "bikini",
        image: "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Relaxed Australian beach bikini with natural materials and coastal style."
    },

    // ACCESSORIES - International Designs
    {
        id: 7,
        name: "French Pearl Necklace",
        price: 89.99,
        category: "accessories",
        image: "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2080&q=80",
        description: "Elegant French pearl necklace with classic Parisian sophistication."
    },
    {
        id: 8,
        name: "Italian Leather Handbag",
        price: 199.99,
        category: "accessories",
        image: "https://images.unsplash.com/photo-1584917865442-de89df76afd3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2025&q=80",
        description: "Premium Italian leather handbag with superior craftsmanship and timeless design."
    },
    {
        id: 34,
        name: "Japanese Silk Scarf",
        price: 69.99,
        category: "accessories",
        image: "https://images.unsplash.com/photo-1551028719-00167b16eac5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Exquisite Japanese silk scarf with traditional patterns and luxurious feel."
    },
    {
        id: 35,
        name: "Moroccan Jewelry Set",
        price: 119.99,
        category: "accessories",
        image: "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        description: "Vibrant Moroccan jewelry set with exotic designs and cultural authenticity."
    },
    {
        id: 36,
        name: "Swiss Watch",
        price: 299.99,
        category: "accessories",
        image: "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=705&q=80",
        description: "Precision Swiss watch with exceptional craftsmanship and timeless elegance."
    }
];

// Cart functionality
let cart = [];
let currentFilter = 'all';
let currentProduct = null;
let selectedSize = null;
let selectedColor = null;
let selectedDesign = null;
let modalQuantity = 1;

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    displayProducts();
    updateCartCount();
    
    // Add event listeners for option buttons
    document.querySelectorAll('.size-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            selectSize(this.dataset.size);
        });
    });
    
    document.querySelectorAll('.color-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            selectColor(this.dataset.color);
        });
    });
    
    document.querySelectorAll('.design-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            selectDesign(this.dataset.design);
        });
    });
    
    // Close modal when clicking outside
    document.getElementById('productModal').addEventListener('click', function(e) {
        if (e.target === this) {
            closeProductModal();
        }
    });
});

// Display products
function displayProducts(filter = 'all') {
    const productsGrid = document.getElementById('productsGrid');
    const filteredProducts = filter === 'all' ? products : products.filter(product => product.category === filter);
    
    productsGrid.innerHTML = '';
    
    filteredProducts.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';
        productCard.innerHTML = `
            <div class="product-image" onclick="openProductModal(${product.id})">
                <img src="${product.image}" alt="${product.name}">
            </div>
            <div class="product-info">
                <h3 class="product-title" onclick="openProductModal(${product.id})">${product.name}</h3>
                <p class="product-price">$${product.price.toFixed(2)}</p>
                <button class="add-to-cart" onclick="openProductModal(${product.id})">View Details</button>
            </div>
        `;
        productsGrid.appendChild(productCard);
    });
}

// Filter products
function filterProducts(category) {
    currentFilter = category;
    displayProducts(category);
    
    // Update active filter button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}

// Open product modal
function openProductModal(productId) {
    const product = products.find(p => p.id === productId);
    currentProduct = product;
    selectedSize = null;
    selectedColor = null;
    selectedDesign = null;
    modalQuantity = 1;
    
    // Update modal content
    document.getElementById('modalProductName').textContent = product.name;
    document.getElementById('modalProductTitle').textContent = product.name;
    document.getElementById('modalProductDescription').textContent = product.description;
    document.getElementById('modalProductPrice').textContent = `$${product.price.toFixed(2)}`;
    document.getElementById('modalProductImage').src = product.image;
    document.getElementById('modalQuantity').textContent = modalQuantity;
    
    // Reset selections
    document.querySelectorAll('.size-btn').forEach(btn => btn.classList.remove('selected'));
    document.querySelectorAll('.color-btn').forEach(btn => btn.classList.remove('selected'));
    document.querySelectorAll('.design-btn').forEach(btn => btn.classList.remove('selected'));
    
    // Show modal
    document.getElementById('productModal').classList.add('open');
}

// Close product modal
function closeProductModal() {
    document.getElementById('productModal').classList.remove('open');
    currentProduct = null;
}

// Handle size selection
function selectSize(size) {
    selectedSize = size;
    document.querySelectorAll('.size-btn').forEach(btn => {
        btn.classList.remove('selected');
        if (btn.dataset.size === size) {
            btn.classList.add('selected');
        }
    });
}

// Handle color selection
function selectColor(color) {
    selectedColor = color;
    document.querySelectorAll('.color-btn').forEach(btn => {
        btn.classList.remove('selected');
        if (btn.dataset.color === color) {
            btn.classList.add('selected');
        }
    });
}

// Handle design selection
function selectDesign(design) {
    selectedDesign = design;
    document.querySelectorAll('.design-btn').forEach(btn => {
        btn.classList.remove('selected');
        if (btn.dataset.design === design) {
            btn.classList.add('selected');
        }
    });
}

// Change quantity in modal
function changeQuantity(change) {
    modalQuantity = Math.max(1, modalQuantity + change);
    document.getElementById('modalQuantity').textContent = modalQuantity;
}

// Add to cart from modal
function addToCartFromModal() {
    if (!selectedSize) {
        showNotification('Please select a size!');
        return;
    }
    if (!selectedColor) {
        showNotification('Please select a color!');
        return;
    }
    if (!selectedDesign) {
        showNotification('Please select a design!');
        return;
    }
    
    const productWithOptions = {
        ...currentProduct,
        size: selectedSize,
        color: selectedColor,
        design: selectedDesign,
        quantity: modalQuantity
    };
    
    // Check if same product with same options already exists
    const existingItem = cart.find(item => 
        item.id === currentProduct.id && 
        item.size === selectedSize && 
        item.color === selectedColor && 
        item.design === selectedDesign
    );
    
    if (existingItem) {
        existingItem.quantity += modalQuantity;
    } else {
        cart.push(productWithOptions);
    }
    
    updateCartCount();
    updateCartDisplay();
    closeProductModal();
    
    showNotification('Product added to cart!');
}

// Add to cart (legacy function for direct add)
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            ...product,
            quantity: 1
        });
    }
    
    updateCartCount();
    updateCartDisplay();
    
    // Show success message
    showNotification('Product added to cart!');
}

// Update cart count
function updateCartCount() {
    const cartCount = document.querySelector('.cart-count');
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
}

// Update cart display
function updateCartDisplay() {
    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');
    
    cartItems.innerHTML = '';
    
    if (cart.length === 0) {
        cartItems.innerHTML = '<p>Your cart is empty</p>';
        cartTotal.textContent = '0.00';
        return;
    }
    
    let total = 0;
    
    cart.forEach((item, index) => {
        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        
        // Show options if they exist
        const optionsText = item.size && item.color && item.design 
            ? `<div class="cart-item-options">Size: ${item.size} | Color: ${item.color} | Design: ${item.design}</div>`
            : '';
        
        cartItem.innerHTML = `
            <img src="${item.image}" alt="${item.name}">
            <div class="cart-item-info">
                <div class="cart-item-title">${item.name}</div>
                <div class="cart-item-price">$${item.price.toFixed(2)}</div>
                ${optionsText}
                <div class="cart-item-quantity">
                    <button class="quantity-btn" onclick="updateQuantity(${index}, -1)">-</button>
                    <span>${item.quantity}</span>
                    <button class="quantity-btn" onclick="updateQuantity(${index}, 1)">+</button>
                </div>
            </div>
        `;
        cartItems.appendChild(cartItem);
        
        total += item.price * item.quantity;
    });
    
    cartTotal.textContent = total.toFixed(2);
}

// Update quantity
function updateQuantity(index, change) {
    if (index >= 0 && index < cart.length) {
        cart[index].quantity += change;
        
        if (cart[index].quantity <= 0) {
            cart.splice(index, 1);
        }
        
        updateCartCount();
        updateCartDisplay();
    }
}

// Toggle cart sidebar
function toggleCart() {
    const cartSidebar = document.getElementById('cartSidebar');
    cartSidebar.classList.toggle('open');
}

// Checkout function
function checkout() {
    if (cart.length === 0) {
        showNotification('Your cart is empty!');
        return;
    }
    
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    alert(`Thank you for your order! Total: $${total.toFixed(2)}\nThis is a demo - no actual payment will be processed.`);
    
    // Clear cart
    cart = [];
    updateCartCount();
    updateCartDisplay();
    toggleCart();
}

// Scroll to products
function scrollToProducts() {
    document.getElementById('products').scrollIntoView({
        behavior: 'smooth'
    });
}

// Show notification
function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: #ff6b9d;
        color: white;
        padding: 1rem 2rem;
        border-radius: 8px;
        z-index: 1002;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 2000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Search functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.search-box input');
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const filteredProducts = products.filter(product => 
            product.name.toLowerCase().includes(searchTerm) ||
            product.description.toLowerCase().includes(searchTerm)
        );
        
        const productsGrid = document.getElementById('productsGrid');
        productsGrid.innerHTML = '';
        
        filteredProducts.forEach(product => {
            const productCard = document.createElement('div');
            productCard.className = 'product-card';
            productCard.innerHTML = `
                <div class="product-image">
                    <img src="${product.image}" alt="${product.name}">
                </div>
                <div class="product-info">
                    <h3 class="product-title">${product.name}</h3>
                    <p class="product-price">$${product.price.toFixed(2)}</p>
                    <button class="add-to-cart" onclick="addToCart(${product.id})">Add to Cart</button>
                </div>
            `;
            productsGrid.appendChild(productCard);
        });
    });
});

// Contact form submission
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.querySelector('.contact-form');
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        showNotification('Thank you for your message! We\'ll get back to you soon.');
        contactForm.reset();
    });
});

// Smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});
