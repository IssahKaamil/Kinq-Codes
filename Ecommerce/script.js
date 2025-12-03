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

// Category default images (curated Unsplash)
const CATEGORY_IMAGES = {
    dresses: 'https://images.unsplash.com/photo-1520975922284-9d06c6a2c88c?auto=format&fit=crop&w=1200&q=80',
    tops: 'https://images.unsplash.com/photo-1503342217505-b0a15cf70489?auto=format&fit=crop&w=1200&q=80',
    bottoms: 'https://images.unsplash.com/photo-1503342394121-0253b602a485?auto=format&fit=crop&w=1200&q=80',
    lingerie: 'https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?auto=format&fit=crop&w=1200&q=80',
    bras: 'https://images.unsplash.com/photo-1586074292901-795f6b3aef6d?auto=format&fit=crop&w=1200&q=80',
    panties: 'https://images.unsplash.com/photo-1592878904946-b3cd4df8d8b2?auto=format&fit=crop&w=1200&q=80',
    bikini: 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=1200&q=80',
    accessories: 'https://images.unsplash.com/photo-1520975916090-3105956dac38?auto=format&fit=crop&w=1200&q=80'
};
const IMAGE_PLACEHOLDER = 'https://via.placeholder.com/800x1000?text=Image+Unavailable';

function getProductImage(product) {
    return product.image || CATEGORY_IMAGES[product.category] || IMAGE_PLACEHOLDER;
}

function onImgErrorSetFallback(imgEl, category) {
    if (!imgEl || imgEl.dataset.fallbackApplied === '1') return;
    imgEl.dataset.fallbackApplied = '1';
    imgEl.src = CATEGORY_IMAGES[category] || IMAGE_PLACEHOLDER;
}

// Cart functionality
let cart = [];
let currentFilter = 'all';
let currentProduct = null;
let selectedSize = null;
let selectedColor = null;
let selectedDesign = null;
let modalQuantity = 1;
let selectedDelivery = 'standard';
// Loyalty tracking (demo via localStorage)
const LOYALTY_KEY = 'heba_loyalty_completed_orders';
const NEW_USER_USED_KEY = 'heba_new_user_discount_used';
function getCompletedOrders() { return parseInt(localStorage.getItem(LOYALTY_KEY) || '0', 10); }
function incrementCompletedOrders() { localStorage.setItem(LOYALTY_KEY, String(getCompletedOrders() + 1)); }
function hasUsedNewUserDiscount() { return localStorage.getItem(NEW_USER_USED_KEY) === '1'; }
function markUsedNewUserDiscount() { localStorage.setItem(NEW_USER_USED_KEY, '1'); }

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

    // Make category tiles scroll and filter products
    document.querySelectorAll('.category-card').forEach(card => {
        card.addEventListener('click', (e) => {
            const onclick = card.getAttribute('onclick');
            // Parse category from existing onclick or fallback to data attr later if needed
            const match = onclick && onclick.match(/filterProducts\('(.+?)'\)/);
            const category = match ? match[1] : null;
            if (category) {
                filterProducts(category);
            }
            const productsSection = document.getElementById('products');
            if (productsSection) productsSection.scrollIntoView({ behavior: 'smooth' });
        });
    });

    // Payment method switching
    const methodContainer = document.getElementById('paymentMethods');
    if (methodContainer) {
        methodContainer.addEventListener('click', function(e) {
            const btn = e.target.closest('.method-btn');
            if (!btn) return;
            document.querySelectorAll('.method-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            renderPaymentFields(btn.dataset.method);
        });
    }

    // Delivery selection
    const deliveryContainer = document.getElementById('deliveryOptions');
    if (deliveryContainer) {
        deliveryContainer.addEventListener('click', function(e) {
            const btn = e.target.closest('.delivery-btn');
            if (!btn) return;
            document.querySelectorAll('.delivery-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            selectedDelivery = btn.dataset.delivery;
            // Re-render summary totals with shipping
            openPaymentModal();
        });
    }

    // Payment form submit
    const paymentForm = document.getElementById('paymentForm');
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            simulatePayment();
        });
    }
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
                <img src="${getProductImage(product)}" alt="${product.name}" onerror="onImgErrorSetFallback(this, '${product.category}')">
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

    // Smooth scroll to products
    const productsSection = document.getElementById('products');
    if (productsSection) {
        productsSection.scrollIntoView({ behavior: 'smooth' });
    }
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
    const modalImg = document.getElementById('modalProductImage');
    modalImg.src = getProductImage(product);
    modalImg.onerror = () => onImgErrorSetFallback(modalImg, product.category);
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

// Buy Now from modal: validates options, ensures address present, opens payment modal directly
function buyNowFromModal() {
    if (!selectedSize) { showNotification('Please select a size!'); return; }
    if (!selectedColor) { showNotification('Please select a color!'); return; }
    if (!selectedDesign) { showNotification('Please select a design!'); return; }

    // Add the item to cart first (so summary reflects it)
    const productWithOptions = {
        ...currentProduct,
        size: selectedSize,
        color: selectedColor,
        design: selectedDesign,
        quantity: modalQuantity
    };
    const existingItem = cart.find(item => 
        item.id === currentProduct.id && item.size === selectedSize && item.color === selectedColor && item.design === selectedDesign
    );
    if (existingItem) existingItem.quantity += modalQuantity; else cart.push(productWithOptions);

    updateCartCount();
    updateCartDisplay();
    closeProductModal();
    // Jump directly to checkout
    openPaymentModal();
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
            <img src="${getProductImage(item)}" alt="${item.name}" onerror="onImgErrorSetFallback(this, '${item.category}')">
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
    
    // Compute promotional discounts preview
    const promo = computePromotions(cart);
    const finalTotal = Math.max(0, total - promo.totalDiscount);
    cartTotal.textContent = finalTotal.toFixed(2);
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
    // Populate and open payment modal
    openPaymentModal();
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

// Payment modal helpers
function openPaymentModal() {
    // Build summary
    const summaryItems = document.getElementById('summaryItems');
    const summaryTotal = document.getElementById('summaryTotal');
    if (summaryItems && summaryTotal) {
        summaryItems.innerHTML = '';
        let total = 0;
        cart.forEach(item => {
            const div = document.createElement('div');
            div.className = 'summary-item';
            const options = item.size && item.color && item.design ? ` | ${item.size} · ${item.color} · ${item.design}` : '';
            div.innerHTML = `
                <img src="${getProductImage(item)}" alt="${item.name}" onerror="onImgErrorSetFallback(this, '${item.category}')">
                <div class="summary-item-info">
                    <div class="summary-item-title">${item.name}</div>
                    <div class="summary-item-meta">$${item.price.toFixed(2)}${options}</div>
                </div>
                <div class="summary-item-qty">x${item.quantity}</div>
            `;
            summaryItems.appendChild(div);
            total += item.price * item.quantity;
        });
        // Apply promotions and show line items
        const promo = computePromotions(cart);
        // Append discount lines
        if (promo.bogoDiscount > 0) {
            const d = document.createElement('div');
            d.className = 'summary-item';
            d.innerHTML = `<div class="summary-item-info"><div class="summary-item-title">BOGO Discount</div><div class="summary-item-meta">- $${promo.bogoDiscount.toFixed(2)}</div></div>`;
            summaryItems.appendChild(d);
        }
        if (promo.loyaltyDiscount > 0) {
            const d = document.createElement('div');
            d.className = 'summary-item';
            d.innerHTML = `<div class="summary-item-info"><div class="summary-item-title">Loyalty Discount (10%)</div><div class="summary-item-meta">- $${promo.loyaltyDiscount.toFixed(2)}</div></div>`;
            summaryItems.appendChild(d);
        }
        if (promo.newUserDiscount > 0) {
            const d = document.createElement('div');
            d.className = 'summary-item';
            d.innerHTML = `<div class="summary-item-info"><div class="summary-item-title">New User Discount (15%)</div><div class="summary-item-meta">- $${promo.newUserDiscount.toFixed(2)}</div></div>`;
            summaryItems.appendChild(d);
        }
        // Shipping based on selectedDelivery
        const shipping = getShippingCost(selectedDelivery);
        if (shipping > 0) {
            const ship = document.createElement('div');
            ship.className = 'summary-item';
            ship.innerHTML = `<div class="summary-item-info"><div class="summary-item-title">Shipping (${formatDelivery(selectedDelivery)})</div><div class="summary-item-meta">$${shipping.toFixed(2)}</div></div>`;
            summaryItems.appendChild(ship);
        }
        const finalTotal = Math.max(0, total - promo.totalDiscount + shipping);
        summaryTotal.textContent = finalTotal.toFixed(2);
    }

    // Default to card fields
    renderPaymentFields('card');

    document.getElementById('paymentModal').classList.add('open');
}

function closePaymentModal() {
    document.getElementById('paymentModal').classList.remove('open');
}

function renderPaymentFields(method) {
    const title = document.getElementById('paymentFormTitle');
    const fields = document.getElementById('paymentFields');
    if (!fields || !title) return;
    const commonBilling = `
        <div class="row">
            <div class="field">
                <label>First Name</label>
                <input type="text" required>
            </div>
            <div class="field">
                <label>Last Name</label>
                <input type="text" required>
            </div>
        </div>
        <div class="field">
            <label>Email</label>
            <input type="email" required>
        </div>
        <div class="field">
            <label>Address</label>
            <input type="text" required>
        </div>
        <div class="row">
            <div class="field">
                <label>City</label>
                <input type="text" required>
            </div>
            <div class="field">
                <label>Country</label>
                <input type="text" required>
            </div>
        </div>
    `;

    if (method === 'card') {
        title.textContent = 'Card Details';
        fields.innerHTML = `
            ${commonBilling}
            <div class="field">
                <label>Cardholder Name</label>
                <input type="text" required>
            </div>
            <div class="field">
                <label>Card Number</label>
                <input type="text" inputmode="numeric" pattern="[0-9\\s]{12,19}" placeholder="1234 5678 9012 3456" required>
            </div>
            <div class="row">
                <div class="field">
                    <label>Expiry</label>
                    <input type="text" placeholder="MM/YY" required>
                </div>
                <div class="field">
                    <label>CVC</label>
                    <input type="text" inputmode="numeric" placeholder="123" required>
                </div>
            </div>
        `;
    } else if (method === 'mobile') {
        title.textContent = 'Mobile Money Details';
        fields.innerHTML = `
            ${commonBilling}
            <div class="field">
                <label>Provider</label>
                <select required>
                    <option value="">Select</option>
                    <option>M-Pesa</option>
                    <option>MTN Mobile Money</option>
                    <option>Airtel Money</option>
                </select>
            </div>
            <div class="field">
                <label>Phone Number</label>
                <input type="tel" required>
            </div>
        `;
    } else if (method === 'paypal') {
        title.textContent = 'PayPal';
        fields.innerHTML = `
            ${commonBilling}
            <div class="field">
                <label>PayPal Email</label>
                <input type="email" required>
            </div>
        `;
    } else if (method === 'applepay') {
        title.textContent = 'Apple Pay';
        fields.innerHTML = `
            ${commonBilling}
            <div class="field">
                <label>Apple ID Email</label>
                <input type="email" required>
            </div>
        `;
    } else if (method === 'crypto') {
        title.textContent = 'Crypto Payment';
        fields.innerHTML = `
            ${commonBilling}
            <div class="field">
                <label>Currency</label>
                <select required>
                    <option value="">Select</option>
                    <option>Bitcoin (BTC)</option>
                    <option>Ethereum (ETH)</option>
                    <option>USDT (Tether)</option>
                    <option>Solana (SOL)</option>
                </select>
            </div>
            <div class="field">
                <label>Wallet Address</label>
                <input type="text" required>
            </div>
        `;
    }
}

function simulatePayment() {
    // Simulate processing
    const payBtn = document.querySelector('.pay-btn');
    if (!payBtn) return;
    payBtn.disabled = true;
    const original = payBtn.innerHTML;
    payBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    setTimeout(() => {
        payBtn.disabled = false;
        payBtn.innerHTML = original;
        // Validate delivery address
        const address = collectDeliveryAddress();
        if (!address) {
            showNotification('Please complete delivery address.');
            return;
        }
        // Calculate promotions for final charge
        const rawTotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const promo = computePromotions(cart);
    const shipping = getShippingCost(selectedDelivery);
    const finalCharge = Math.max(0, rawTotal - promo.totalDiscount + shipping);
        closePaymentModal();
        toggleCart();
        showNotification(`Payment successful! Charged $${finalCharge.toFixed(2)}. Shipping to ${address.city}, ${address.country}.`);
        // Persist loyalty state
        incrementCompletedOrders();
        if (promo.newUserDiscount > 0) { markUsedNewUserDiscount(); }
        // Clear cart
        cart = [];
        updateCartCount();
        updateCartDisplay();
    }, 1500);
}

// Promotions engine
function computePromotions(items) {
    let bogoDiscount = 0;
    // BOGO: for every two of the same product, one free (price of one)
    const grouped = new Map();
    items.forEach(i => {
        const key = `${i.id}|${i.size||''}|${i.color||''}|${i.design||''}`; // exact variant
        const prev = grouped.get(key) || { item: i, qty: 0 };
        prev.qty += i.quantity;
        prev.item = i;
        grouped.set(key, prev);
    });
    grouped.forEach(({ item, qty }) => {
        const freeUnits = Math.floor(qty / 2); // buy 1 get 1 free per pair
        bogoDiscount += freeUnits * item.price;
    });

    const rawTotal = items.reduce((s, it) => s + it.price * it.quantity, 0);
    const postBogoSubtotal = Math.max(0, rawTotal - bogoDiscount);

    // Loyalty: 10% off after 5 completed orders on device
    const isLoyal = getCompletedOrders() >= 5;
    let loyaltyDiscount = isLoyal ? postBogoSubtotal * 0.10 : 0;

    // New user: 15% off first order over $1000, cannot combine with loyalty
    let newUserDiscount = 0;
    if (!hasUsedNewUserDiscount() && !isLoyal && postBogoSubtotal > 1000) {
        newUserDiscount = postBogoSubtotal * 0.15;
    } else {
        newUserDiscount = 0;
    }

    // Apply the better of loyalty vs new user (not both)
    if (newUserDiscount > 0 && loyaltyDiscount > 0) {
        if (newUserDiscount >= loyaltyDiscount) loyaltyDiscount = 0; else newUserDiscount = 0;
    }

    const totalDiscount = bogoDiscount + loyaltyDiscount + newUserDiscount;
    return { bogoDiscount, loyaltyDiscount, newUserDiscount, totalDiscount };
}

function getShippingCost(method) {
    switch (method) {
        case 'express': return 15;
        case 'sameday': return 25;
        case 'international': return 30;
        case 'standard':
        default: return 5;
    }
}

function formatDelivery(method) {
    switch (method) {
        case 'express': return 'Express 1-2 days';
        case 'sameday': return 'Same-day';
        case 'international': return 'International 5-10 days';
        case 'standard':
        default: return 'Standard 3-5 days';
    }
}

// Delivery helpers
function collectDeliveryAddress() {
    const fullName = document.getElementById('del_fullname')?.value?.trim();
    const phone = document.getElementById('del_phone')?.value?.trim();
    const addr1 = document.getElementById('del_addr1')?.value?.trim();
    const city = document.getElementById('del_city')?.value?.trim();
    const country = document.getElementById('del_country')?.value?.trim();
    if (!fullName || !phone || !addr1 || !city || !country) return null;
    const addr2 = document.getElementById('del_addr2')?.value?.trim() || '';
    const state = document.getElementById('del_state')?.value?.trim() || '';
    const postal = document.getElementById('del_postal')?.value?.trim() || '';
    const instructions = document.getElementById('del_instructions')?.value?.trim() || '';
    const address = { fullName, phone, addr1, addr2, city, state, postal, country, instructions };
    // Persist last used address to localStorage
    localStorage.setItem('heba_last_address', JSON.stringify(address));
    return address;
}

function preloadDeliveryAddress() {
    try {
        const raw = localStorage.getItem('heba_last_address');
        if (!raw) return;
        const a = JSON.parse(raw);
        const set = (id, val) => { const el = document.getElementById(id); if (el && val) el.value = val; };
        set('del_fullname', a.fullName);
        set('del_phone', a.phone);
        set('del_addr1', a.addr1);
        set('del_addr2', a.addr2);
        set('del_city', a.city);
        set('del_state', a.state);
        set('del_postal', a.postal);
        set('del_country', a.country);
        set('del_instructions', a.instructions);
    } catch (e) {}
}

function useCurrentLocation() {
    if (!navigator.geolocation) {
        showNotification('Geolocation not supported on this device.');
        return;
    }
    navigator.geolocation.getCurrentPosition(async (pos) => {
        const { latitude, longitude } = pos.coords;
        try {
            // Try reverse geocoding via OpenStreetMap Nominatim (no API key). For demo only.
            const resp = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`);
            const data = await resp.json();
            const addr = data.address || {};
            const set = (id, val) => { const el = document.getElementById(id); if (el && val) el.value = val; };
            set('del_city', addr.city || addr.town || addr.village || '');
            set('del_state', addr.state || '');
            set('del_postal', addr.postcode || '');
            set('del_country', addr.country || '');
            showNotification('Location filled from your current position.');
        } catch (e) {
            showNotification('Could not fetch address from location.');
        }
    }, () => showNotification('Unable to get current location.'));
}

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
