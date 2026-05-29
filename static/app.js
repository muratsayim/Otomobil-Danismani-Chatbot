// State Management
const state = {
    budget: null,
    bodyType: null,
    fuelType: null,
    transmission: null,
    priorities: [],
    chatHistory: [],
    comparedCars: [], // Array of car objects
    allCars: [],      // Cached list of all cars
    apiKey: null,     // Gemini API Key entered in UI
    hasEnvKey: false, // Gemini API Key defined in server environment
    userId: sessionStorage.getItem('chatbot_user_id'),
    userName: sessionStorage.getItem('chatbot_user_name')
};

// DOM Elements
const elements = {
    budgetSlider: document.getElementById('input-budget'),
    budgetValue: document.getElementById('budget-value'),
    btnFindCars: document.getElementById('btn-find-cars'),
    btnShowAll: document.getElementById('btn-show-all-cars'),
    carsGrid: document.getElementById('cars-grid'),
    resultsCount: document.getElementById('results-count'),
    chatTextarea: document.getElementById('chat-textarea'),
    btnSend: document.getElementById('btn-send'),
    chatMessagesBox: document.getElementById('chat-messages-box'),
    btnClearChat: document.getElementById('btn-clear-chat'),
    compDrawer: document.getElementById('comp-drawer'),
    compList: document.getElementById('comp-list'),
    compCount: document.getElementById('comp-count'),
    btnCompareNow: document.getElementById('btn-compare-now'),
    carDetailModal: document.getElementById('car-detail-modal'),
    carDetailContent: document.getElementById('car-detail-content'),
    comparisonModal: document.getElementById('comparison-modal'),
    comparisonTableContent: document.getElementById('comparison-table-content'),
    inputApiKey: document.getElementById('input-api-key'),
    apiStatusDot: document.getElementById('api-status-dot'),
    apiStatusText: document.getElementById('api-status-text')
};

// ==========================================================================
// Initialization & Event Listeners
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
    initFilters();
    initChat();
    initComparison();
    initApiKey();
    
    // Check if user is authenticated
    checkAuthStatus();
});

// Authentication Status Checker
function checkAuthStatus() {
    state.userId = sessionStorage.getItem('chatbot_user_id');
    state.userName = sessionStorage.getItem('chatbot_user_name');

    if (!state.userId) {
        // Clear input fields to keep them empty on load/logout
        document.getElementById('loginEmail').value = '';
        document.getElementById('loginPassword').value = '';
        document.getElementById('registerName').value = '';
        document.getElementById('registerEmail').value = '';
        document.getElementById('registerPassword').value = '';
        document.getElementById('registerPasswordConfirm').value = '';

        // Show login screen, hide dashboard
        document.getElementById('authContainer').style.display = 'flex';
        document.querySelector('.app-container').style.display = 'none';
    } else {
        // Hide login screen, show dashboard
        document.getElementById('authContainer').style.display = 'none';
        document.querySelector('.app-container').style.display = 'flex';
        document.getElementById('welcomeUserName').textContent = state.userName;
        
        // Load server data
        checkServerStatus();
        fetchCachedCars();
    }
}

// Switch between login and register forms
window.switchAuthMode = function(mode) {
    if (mode === 'register') {
        document.getElementById('loginFormContainer').classList.remove('active');
        document.getElementById('registerFormContainer').classList.add('active');
    } else {
        document.getElementById('registerFormContainer').classList.remove('active');
        document.getElementById('loginFormContainer').classList.add('active');
    }
};

// Toggle password input visibility
window.togglePasswordVisibility = function(inputId, icon) {
    const input = document.getElementById(inputId);
    if (input.type === 'password') {
        input.type = 'text';
        icon.className = 'fa-solid fa-eye-slash toggle-password';
    } else {
        input.type = 'password';
        icon.className = 'fa-solid fa-eye toggle-password';
    }
};

// Handle Login Submission
window.handleLoginSubmit = async function(e) {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value.trim();
    const sifre = document.getElementById('loginPassword').value;
    const btn = document.getElementById('btnLoginSubmit');

    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Giriş Yapılıyor...';

    try {
        const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, sifre })
        });

        const data = await res.json();
        if (res.ok) {
            sessionStorage.setItem('chatbot_user_id', data.id);
            sessionStorage.setItem('chatbot_user_name', data.adSoyad);
            showToast("Başarıyla giriş yapıldı.", "success");
            
            // Reset forms
            document.getElementById('loginForm').reset();
            
            // Transition to dashboard
            checkAuthStatus();
        } else {
            showToast(data.detail || "Giriş başarısız. Bilgilerinizi kontrol edin.", "error");
        }
    } catch (err) {
        showToast("Sunucu ile bağlantı kurulamadı.", "error");
    } finally {
        btn.disabled = false;
        btn.innerHTML = 'Giriş Yap';
    }
};

// Handle Registration Submission
window.handleRegisterSubmit = async function(e) {
    e.preventDefault();
    const adSoyad = document.getElementById('registerName').value.trim();
    const email = document.getElementById('registerEmail').value.trim();
    const sifre = document.getElementById('registerPassword').value;
    const sifreTekrar = document.getElementById('registerPasswordConfirm').value;
    const btn = document.getElementById('btnRegisterSubmit');

    if (sifre !== sifreTekrar) {
        showToast("Şifreler uyuşmuyor.", "error");
        return;
    }

    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Kaydediliyor...';

    try {
        const res = await fetch('/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ adSoyad, email, sifre })
        });

        const data = await res.json();
        if (res.ok) {
            showToast("Kayıt başarıyla tamamlandı! Giriş yapabilirsiniz.", "success");
            document.getElementById('registerForm').reset();
            switchAuthMode('login');
        } else {
            showToast(data.detail || "Kayıt başarısız.", "error");
        }
    } catch (err) {
        showToast("Sunucu ile bağlantı kurulamadı.", "error");
    } finally {
        btn.disabled = false;
        btn.innerHTML = 'Kayıt Ol ve Başla';
    }
};

// Handle Logout Action
window.handleLogout = function() {
    if (!confirm("Oturumu kapatmak istediğinize emin misiniz?")) return;
    
    // Clear session storage
    sessionStorage.removeItem('chatbot_user_id');
    sessionStorage.removeItem('chatbot_user_name');
    sessionStorage.removeItem('chatbot_session_state');
    
    showToast("Başarıyla çıkış yapıldı.", "success");
    
    // Clear state
    state.chatHistory = [];
    state.comparedCars = [];
    
    // Reset filters
    state.budget = null;
    state.bodyType = null;
    state.fuelType = null;
    state.transmission = null;
    state.priorities = [];
    
    // Clear chat UI
    elements.chatMessagesBox.innerHTML = `
        <div class="message bot-message">
            <div class="msg-avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="msg-body">
                <p>Merhaba! Ben sizin kişisel Otomobil Danışmanınızım. 🚗</p>
                <p>Size en uygun otomobili seçmek, bütçenizi değerlendirmek veya aklınızdaki modelleri karşılaştırmak için buradayyim.</p>
            </div>
        </div>
    `;
    
    restoreUiFromState();
    checkAuthStatus();
};

// Toast Notifications helper
function showToast(msg, type = 'success') {
    const toast = document.getElementById('toast');
    const icon = document.getElementById('toastIcon');
    const msgEl = document.getElementById('toastMsg');

    msgEl.innerText = msg;
    toast.className = `toast-notification ${type} show`;

    if (type === 'success') {
        icon.className = 'fa-solid fa-circle-check';
    } else if (type === 'error') {
        icon.className = 'fa-solid fa-circle-exclamation';
    } else {
        icon.className = 'fa-solid fa-circle-info';
    }

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

async function checkServerStatus() {
    try {
        const response = await fetch('/api/status');
        if (response.ok) {
            const data = await response.json();
            state.hasEnvKey = data.has_env_key;
            updateApiStatus(!!state.apiKey || state.hasEnvKey);
        }
    } catch (e) {
        console.error("Durum kontrolü hatası:", e);
    }
}

function initApiKey() {
    let savedKey = null;
    try {
        savedKey = sessionStorage.getItem('gemini_api_key');
    } catch (e) {
        console.warn("sessionStorage okuma engellendi (Muhtemelen iframe veya gizlilik ayarı kaynaklı):", e);
    }

    if (savedKey) {
        elements.inputApiKey.value = savedKey;
        state.apiKey = savedKey;
    }

    elements.inputApiKey.addEventListener('input', (e) => {
        const key = e.target.value.trim();
        state.apiKey = key || null;
        updateApiStatus(!!key || state.hasEnvKey);
        
        try {
            if (key) {
                sessionStorage.setItem('gemini_api_key', key);
            } else {
                sessionStorage.removeItem('gemini_api_key');
            }
        } catch (err) {
            console.warn("sessionStorage yazma engellendi:", err);
        }
    });
}

function updateApiStatus(isActive) {
    if (isActive) {
        elements.apiStatusDot.className = 'status-dot green';
        if (state.apiKey) {
            elements.apiStatusText.innerText = 'Yapay Zeka Modu';
        } else if (state.hasEnvKey) {
            elements.apiStatusText.innerText = 'Yapay Zeka Modu (Sistem)';
        } else {
            elements.apiStatusText.innerText = 'Yapay Zeka Modu';
        }
    } else {
        elements.apiStatusDot.className = 'status-dot yellow';
        elements.apiStatusText.innerText = 'Yerel Mod';
    }
}

// Cache all cars for fast reference in comparison/detail lookups
async function fetchCachedCars() {
    try {
        const response = await fetch('/api/cars', {
            headers: { 'X-User-Id': state.userId }
        });
        if (response.ok) {
            state.allCars = await response.json();
            loadSessionState();
        }
    } catch (e) {
        console.error("Araçlar yüklenirken hata oluştu:", e);
    }
}

// Setup Filters Interactivity
function initFilters() {
    // Budget Slider
    elements.budgetSlider.addEventListener('input', (e) => {
        const val = parseInt(e.target.value);
        if (val === parseInt(elements.budgetSlider.max)) {
            elements.budgetValue.innerText = 'Limitsiz';
            state.budget = null;
        } else {
            elements.budgetValue.innerText = `${(val / 1000000).toFixed(2)} Milyon TL`;
            state.budget = val;
        }
        saveSessionState();
    });

    // Body Type Cards (Single Select)
    document.querySelectorAll('.body-card').forEach(card => {
        card.addEventListener('click', () => {
            const val = card.dataset.val;
            if (state.bodyType === val) {
                state.bodyType = null;
                card.classList.remove('active');
            } else {
                document.querySelectorAll('.body-card').forEach(c => c.classList.remove('active'));
                state.bodyType = val;
                card.classList.add('active');
            }
            saveSessionState();
        });
    });

    // Fuel Pills (Single Select)
    document.querySelectorAll('#fuel-pills .pill').forEach(pill => {
        pill.addEventListener('click', () => {
            const val = pill.dataset.val;
            if (state.fuelType === val) {
                state.fuelType = null;
                pill.classList.remove('active');
            } else {
                document.querySelectorAll('#fuel-pills .pill').forEach(p => p.classList.remove('active'));
                state.fuelType = val;
                pill.classList.add('active');
            }
            saveSessionState();
        });
    });

    // Transmission Pills (Single Select)
    document.querySelectorAll('#trans-pills .pill').forEach(pill => {
        pill.addEventListener('click', () => {
            const val = pill.dataset.val;
            if (state.transmission === val) {
                state.transmission = null;
                pill.classList.remove('active');
            } else {
                document.querySelectorAll('#trans-pills .pill').forEach(p => p.classList.remove('active'));
                state.transmission = val;
                pill.classList.add('active');
            }
            saveSessionState();
        });
    });

    // Priority Pills (Multi Select)
    document.querySelectorAll('#priority-pills .pill').forEach(pill => {
        pill.addEventListener('click', () => {
            const val = pill.dataset.val;
            const index = state.priorities.indexOf(val);
            if (index > -1) {
                state.priorities.splice(index, 1);
                pill.classList.remove('active');
            } else {
                state.priorities.push(val);
                pill.classList.add('active');
            }
            saveSessionState();
        });
    });

    // Submit Filter Search
    elements.btnFindCars.addEventListener('click', handleFilterSearch);
    elements.btnShowAll.addEventListener('click', handleShowAllCars);
}

// ==========================================================================
// Car Search & Render Operations
// ==========================================================================
async function handleFilterSearch() {
    elements.btnFindCars.disabled = true;
    elements.btnFindCars.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Aranıyor...';

    const payload = {
        budget: state.budget,
        body_types: state.bodyType ? [state.bodyType] : null,
        fuel_types: state.fuelType ? [state.fuelType] : null,
        transmissions: state.transmission ? [state.transmission] : null,
        priorities: state.priorities.length > 0 ? state.priorities : null
    };

    try {
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-User-Id': state.userId
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            const cars = await response.json();
            renderCarCards(cars);
            // Scroll to results area smoothly
            document.getElementById('results-area').scrollIntoView({ behavior: 'smooth' });
        } else {
            showErrorCard("Sonuçlar alınamadı.");
        }
    } catch (e) {
        showErrorCard("Bağlantı hatası oluştu.");
    } finally {
        elements.btnFindCars.disabled = false;
        elements.btnFindCars.innerHTML = '<i class="fa-solid fa-magnifying-glass"></i> Uygun Modelleri Ara';
    }
}

async function handleShowAllCars() {
    try {
        elements.btnShowAll.disabled = true;
        const response = await fetch('/api/cars', {
            headers: { 'X-User-Id': state.userId }
        });
        if (response.ok) {
            const cars = await response.json();
            renderCarCards(cars, false); // Do not show match scores for general list
            document.getElementById('results-area').scrollIntoView({ behavior: 'smooth' });
        }
    } catch (e) {
        showErrorCard("Araçlar yüklenemedi.");
    } finally {
        elements.btnShowAll.disabled = false;
    }
}

function renderCarCards(cars, showScore = true) {
    elements.carsGrid.innerHTML = '';
    elements.resultsCount.innerText = `${cars.length} Araç Listelendi`;

    if (cars.length === 0) {
        elements.carsGrid.innerHTML = `
            <div class="initial-results-placeholder">
                <i class="fa-solid fa-face-frown-open"></i>
                <p>Kriterlerinize uygun otomobil bulunamadı. Lütfen filtrelerinizi gevşetip tekrar deneyin.</p>
            </div>
        `;
        return;
    }

    cars.forEach(car => {
        const isCompared = state.comparedCars.some(c => c.id === car.id);
        const card = document.createElement('article');
        card.className = 'car-card';

        // Styling tags for icons
        let carIcon = 'fa-car-side';
        if (car.body_type === 'SUV') carIcon = 'fa-truck-monster';
        if (car.body_type === 'Hatchback') carIcon = 'fa-car-rear';

        let fuelIcon = 'fa-gas-pump';
        if (car.fuel_type === 'Elektrik') fuelIcon = 'fa-plug-circle-bolt';
        if (car.fuel_type === 'Hibrit') fuelIcon = 'fa-leaf';

        const scoreBadge = (showScore && car.score && car.score > 0) ? 
            `<div class="card-header-badge"><span class="match-score-badge">%${Math.min(100, 60 + car.score * 10)} Uyumluluk</span></div>` : '';

        card.innerHTML = `
            ${scoreBadge}
            <button class="car-compare-btn ${isCompared ? 'active' : ''}" data-id="${car.id}" title="Karşılaştırmaya Ekle">
                <i class="fa-solid fa-scale-balanced"></i>
            </button>
            <div class="car-image-area">
                <div class="car-silhouette"></div>
                <i class="fa-solid ${carIcon} bg-car-icon"></i>
                <div class="car-visual-tag">${car.brand}</div>
            </div>
            <div class="car-info-area">
                <h4 class="car-title">${car.brand} ${car.model}</h4>
                <div class="car-segment-pills">
                    <span class="car-tag highlight">${car.body_type}</span>
                    <span class="car-tag">${car.segment} Segment</span>
                </div>
                <div class="car-specs">
                    <div class="car-spec-item"><i class="fa-solid ${fuelIcon}"></i> <span>${car.fuel_type}</span></div>
                    <div class="car-spec-item"><i class="fa-solid fa-gears"></i> <span>${car.transmission}</span></div>
                    <div class="car-spec-item"><i class="fa-solid fa-gauge-high"></i> <span>${car.power}</span></div>
                    <div class="car-spec-item"><i class="fa-solid fa-droplet"></i> <span>${car.consumption}</span></div>
                </div>
                <div class="car-price-row">
                    <span class="car-price">${car.price.toLocaleString('tr-TR')} TL</span>
                    <button class="car-card-action" onclick="showCarDetails(${car.id})">Detaylar <i class="fa-solid fa-arrow-right"></i></button>
                </div>
            </div>
        `;

        // Bind compare button click inside loop
        card.querySelector('.car-compare-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            toggleComparison(car);
        });

        elements.carsGrid.appendChild(card);
    });
}

function showErrorCard(msg) {
    elements.carsGrid.innerHTML = `
        <div class="initial-results-placeholder" style="color: var(--danger)">
            <i class="fa-solid fa-triangle-exclamation"></i>
            <p>${msg}</p>
        </div>
    `;
}

// ==========================================================================
// Car Details & Comparison Logic
// ==========================================================================
async function showCarDetails(carId) {
    const car = state.allCars.find(c => c.id === carId) || await fetchCarById(carId);
    if (!car) return;

    elements.carDetailContent.innerHTML = `
        <div class="detail-header">
            <div>
                <h2>${car.brand} ${car.model}</h2>
                <div class="car-segment-pills" style="margin-top: 8px;">
                    <span class="car-tag highlight">${car.body_type}</span>
                    <span class="car-tag">${car.segment} Segment</span>
                    <span class="car-tag">${car.transmission}</span>
                </div>
            </div>
            <span class="price-tag">${car.price.toLocaleString('tr-TR')} TL</span>
        </div>
        <p class="detail-desc">${car.description}</p>
        
        <div class="detail-specs-grid">
            <div class="detail-spec-card">
                <span class="label"><i class="fa-solid fa-gauge-high"></i> Güç</span>
                <span class="value">${car.power}</span>
            </div>
            <div class="detail-spec-card">
                <span class="label"><i class="fa-solid fa-gas-pump"></i> Yakıt Türü</span>
                <span class="value">${car.fuel_type}</span>
            </div>
            <div class="detail-spec-card">
                <span class="label"><i class="fa-solid fa-droplet"></i> Tüketim</span>
                <span class="value">${car.consumption}</span>
            </div>
        </div>

        <div class="pros-cons-container">
            <div class="pros-column">
                <h4><i class="fa-solid fa-circle-check"></i> Artıları</h4>
                <ul class="bullets-list">
                    ${car.pros.map(pro => `<li>${pro}</li>`).join('')}
                </ul>
            </div>
            <div class="cons-column">
                <h4><i class="fa-solid fa-circle-xmark"></i> Eksileri</h4>
                <ul class="bullets-list">
                    ${car.cons.map(con => `<li>${con}</li>`).join('')}
                </ul>
            </div>
        </div>

        <div class="features-list">
            <h4>Öne Çıkan Özellikler</h4>
            <div class="features-grid">
                ${car.features.map(f => `<span class="car-tag">${f}</span>`).join('')}
            </div>
        </div>
    `;

    openModal('car-detail-modal');
}

async function fetchCarById(id) {
    try {
        const res = await fetch(`/api/cars/${id}`, {
            headers: { 'X-User-Id': state.userId }
        });
        if (res.ok) return await res.json();
    } catch (e) {
        console.error(e);
    }
    return null;
}

// Comparison Desk Logic
function initComparison() {
    elements.btnCompareNow.addEventListener('click', showComparisonModal);
}

function toggleComparison(car) {
    const idx = state.comparedCars.findIndex(c => c.id === car.id);
    const btns = document.querySelectorAll(`.car-compare-btn[data-id="${car.id}"]`);

    if (idx > -1) {
        // Remove
        state.comparedCars.splice(idx, 1);
        btns.forEach(b => b.classList.remove('active'));
    } else {
        // Add (max 3 cars limit)
        if (state.comparedCars.length >= 3) {
            alert("Aynı anda en fazla 3 aracı karşılaştırabilirsiniz.");
            return;
        }
        state.comparedCars.push(car);
        btns.forEach(b => b.classList.add('active'));
    }

    renderComparisonDrawer();
    saveSessionState();
}

function renderComparisonDrawer() {
    const count = state.comparedCars.length;
    elements.compCount.innerText = count;

    if (count > 0) {
        elements.compDrawer.classList.add('active');
        elements.compList.innerHTML = '';
        state.comparedCars.forEach(car => {
            const item = document.createElement('div');
            item.className = 'comp-item';
            item.innerHTML = `
                <span class="comp-item-name">${car.brand} ${car.model}</span>
                <button class="comp-item-remove" onclick="removeComparedCar(${car.id})">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            `;
            elements.compList.appendChild(item);
        });
    } else {
        elements.compDrawer.classList.remove('active');
        elements.compList.innerHTML = '<p class="empty-text">Karşılaştırmak için en az 2 araç ekleyin.</p>';
    }

    elements.btnCompareNow.disabled = count < 2;
}

window.removeComparedCar = function(carId) {
    const car = state.comparedCars.find(c => c.id === carId);
    if (car) toggleComparison(car);
};

function showComparisonModal() {
    if (state.comparedCars.length < 2) return;

    const cars = state.comparedCars;
    
    let tableHtml = `
        <table class="comparison-table">
            <thead>
                <tr>
                    <th>Özellik</th>
                    ${cars.map(c => `
                        <th>
                            <div class="comp-header-cell">
                                <span class="brand">${c.brand}</span>
                                <span class="model">${c.model}</span>
                            </div>
                        </th>
                    `).join('')}
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="feature-name">Fiyat</td>
                    ${cars.map(c => `<td><strong>${c.price.toLocaleString('tr-TR')} TL</strong></td>`).join('')}
                </tr>
                <tr>
                    <td class="feature-name">Kasa Tipi / Segment</td>
                    ${cars.map(c => `<td>${c.body_type} (${c.segment})</td>`).join('')}
                </tr>
                <tr>
                    <td class="feature-name">Yakıt Türü</td>
                    ${cars.map(c => `<td>${c.fuel_type}</td>`).join('')}
                </tr>
                <tr>
                    <td class="feature-name">Şanzıman</td>
                    ${cars.map(c => `<td>${c.transmission}</td>`).join('')}
                </tr>
                <tr>
                    <td class="feature-name">Motor Gücü</td>
                    ${cars.map(c => `<td>${c.power}</td>`).join('')}
                </tr>
                <tr>
                    <td class="feature-name">Yakıt Tüketimi</td>
                    ${cars.map(c => `<td>${c.consumption}</td>`).join('')}
                </tr>
                <tr>
                    <td class="feature-name">Öne Çıkan Özellikler</td>
                    ${cars.map(c => `<td>${c.features.join(', ')}</td>`).join('')}
                </tr>
                <tr>
                    <td class="feature-name" style="color: var(--accent)">Artıları (Pros)</td>
                    ${cars.map(c => `
                        <td>
                            <ul class="bullets-list" style="padding-left: 0;">
                                ${c.pros.map(p => `<li>${p}</li>`).join('')}
                            </ul>
                        </td>
                    `).join('')}
                </tr>
                <tr>
                    <td class="feature-name" style="color: var(--danger)">Eksileri (Cons)</td>
                    ${cars.map(c => `
                        <td>
                            <ul class="bullets-list" style="padding-left: 0;">
                                ${c.cons.map(p => `<li>${p}</li>`).join('')}
                            </ul>
                        </td>
                    `).join('')}
                </tr>
            </tbody>
        </table>
    `;

    elements.comparisonTableContent.innerHTML = tableHtml;
    openModal('comparison-modal');
}

// Modal Helpers
function openModal(id) {
    document.getElementById(id).classList.add('active');
}

window.closeModal = function(id) {
    document.getElementById(id).classList.remove('active');
};

// ==========================================================================
// Chatbot Interface Logic
// ==========================================================================
function initChat() {
    elements.btnSend.addEventListener('click', handleSendMessage);
    elements.chatTextarea.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });

    elements.btnClearChat.addEventListener('click', () => {
        state.chatHistory = [];
        elements.chatMessagesBox.innerHTML = `
            <div class="message bot-message">
                <div class="msg-avatar"><i class="fa-solid fa-robot"></i></div>
                <div class="msg-body">
                    <p>Sohbet geçmişi temizlendi. Yeniden yardımcı olmak için buradayım!</p>
                </div>
            </div>
        `;
        saveSessionState();
    });

    // Quick Suggestions buttons
    document.querySelectorAll('.suggest-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const query = btn.dataset.query;
            elements.chatTextarea.value = query;
            handleSendMessage();
        });
    });
}

async function handleSendMessage() {
    const text = elements.chatTextarea.value.trim();
    if (!text) return;

    // Clear Textarea
    elements.chatTextarea.value = '';

    // Add User Message to UI & State
    appendChatMessage('user', text);
    state.chatHistory.push({ role: 'user', content: text });
    saveSessionState();

    // Show Typing Indicator
    const typingId = showTypingIndicator();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-User-Id': state.userId
            },
            body: JSON.stringify({
                message: text,
                history: state.chatHistory.slice(0, -1), // exclude current message
                api_key: state.apiKey
            })
        });

        removeTypingIndicator(typingId);

        if (response.ok) {
            const data = await response.json();
            appendChatMessage('assistant', data.response);
            state.chatHistory.push({ role: 'assistant', content: data.response });
            saveSessionState();
        } else {
            appendChatMessage('assistant', "Üzgünüm, şu anda yanıt oluşturamıyorum. Lütfen daha sonra tekrar deneyin.");
        }
    } catch (e) {
        removeTypingIndicator(typingId);
        appendChatMessage('assistant', "Bir bağlantı hatası oluştu. Lütfen sunucunun çalıştığından emin olun.");
    }
}

function appendChatMessage(role, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role === 'user' ? 'user-message' : 'bot-message'}`;

    const avatarHtml = role === 'user' ? 
        `<div class="msg-avatar"><i class="fa-solid fa-user"></i></div>` : 
        `<div class="msg-avatar"><i class="fa-solid fa-robot"></i></div>`;

    const formattedText = parseMarkdown(text);

    msgDiv.innerHTML = `
        ${avatarHtml}
        <div class="msg-body">
            ${formattedText}
        </div>
    `;

    elements.chatMessagesBox.appendChild(msgDiv);
    scrollToBottom();
}

function showTypingIndicator() {
    const indicatorId = 'typing-' + Date.now();
    const indDiv = document.createElement('div');
    indDiv.className = 'message bot-message';
    indDiv.id = indicatorId;
    indDiv.innerHTML = `
        <div class="msg-avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="msg-body">
            <div class="typing-indicator">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        </div>
    `;
    elements.chatMessagesBox.appendChild(indDiv);
    scrollToBottom();
    return indicatorId;
}

function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function scrollToBottom() {
    elements.chatMessagesBox.scrollTop = elements.chatMessagesBox.scrollHeight;
}

// Simple Markdown parser to convert bold, italic, lines and lists into HTML
function parseMarkdown(text) {
    // Escape HTML to prevent XSS (only keep markup we generate)
    let html = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

    // Table Parsing
    const tableLines = html.split('\n');
    let inTable = false;
    let tableRows = [];
    let processedLines = [];

    for (let i = 0; i < tableLines.length; i++) {
        let line = tableLines[i].trim();
        if (line.startsWith('|') && line.endsWith('|')) {
            if (!inTable) {
                if (line.includes(':---') || line.includes('---')) {
                    inTable = true;
                    if (tableRows.length > 0) {
                        const headerRow = tableRows.pop();
                        const cols = headerRow.split('|').map(c => c.trim()).filter((c, idx, arr) => idx > 0 && idx < arr.length - 1);
                        tableRows.push('<thead><tr>' + cols.map(c => `<th>${c}</th>`).join('') + '</tr></thead><tbody>');
                    }
                    continue;
                }
                inTable = true;
                tableRows.push('<table><tbody>');
            }
            
            if (!line.includes(':---') && !line.includes('---')) {
                const cols = line.split('|').map(c => c.trim()).filter((c, idx, arr) => idx > 0 && idx < arr.length - 1);
                if (tableRows.length === 1 && tableRows[0] === '<table><tbody>') {
                    const nextLine = tableLines[i+1] ? tableLines[i+1].trim() : '';
                    if (nextLine.startsWith('|') && (nextLine.includes(':---') || nextLine.includes('---'))) {
                        tableRows.push(line);
                        continue;
                    }
                }
                tableRows.push('<tr>' + cols.map(c => `<td>${c}</td>`).join('') + '</tr>');
            }
        } else {
            if (inTable) {
                if (tableRows.length > 0) {
                    let tableStr = tableRows.join('\n');
                    tableStr += '</tbody></table>';
                    processedLines.push(tableStr);
                }
                tableRows = [];
                inTable = false;
            }
            processedLines.push(tableLines[i]);
        }
    }
    if (inTable && tableRows.length > 0) {
        let tableStr = tableRows.join('\n');
        tableStr += '</tbody></table>';
        processedLines.push(tableStr);
    }
    html = processedLines.join('\n');

    // Bold (**text** or __text__)
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/__(.*?)__/g, '<strong>$1</strong>');

    // Italic (*text* or _text_)
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    html = html.replace(/_(.*?)_/g, '<em>$1</em>');

    // Headers (### Header)
    html = html.replace(/^### (.*?)$/gm, '<h4>$1</h4>');
    html = html.replace(/^## (.*?)$/gm, '<h3>$1</h3>');

    // Bullet Lists (- item or * item)
    // Wrap consecutive bullet points in <ul>
    const lines = html.split('\n');
    let inList = false;
    let newLines = [];

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();
        if (line.startsWith('- ') || line.startsWith('* ')) {
            if (!inList) {
                newLines.push('<ul>');
                inList = true;
            }
            newLines.push(`<li>${line.substring(2)}</li>`);
        } else {
            if (inList) {
                newLines.push('</ul>');
                inList = false;
            }
            newLines.push(lines[i]);
        }
    }
    if (inList) {
        newLines.push('</ul>');
    }

    html = newLines.join('\n');

    // Paragraphs / Linebreaks
    html = html.split('\n').map(line => {
        if (line.trim() === '') return '';
        if (line.startsWith('<table') || line.startsWith('</table') || line.startsWith('<thead') || line.startsWith('</thead') || line.startsWith('<tbody') || line.startsWith('</tbody') || line.startsWith('<tr') || line.startsWith('</tr') || line.startsWith('<td') || line.startsWith('</td') || line.startsWith('<th') || line.startsWith('</th')) return line;
        if (line.startsWith('<ul') || line.startsWith('</ul') || line.startsWith('<li') || line.startsWith('<h')) return line;
        return `<p>${line}</p>`;
    }).join('\n');

    return html;
}

// Session State Persist Helpers
function saveSessionState() {
    try {
        const sessionData = {
            budget: state.budget,
            bodyType: state.bodyType,
            fuelType: state.fuelType,
            transmission: state.transmission,
            priorities: state.priorities,
            chatHistory: state.chatHistory,
            comparedCars: state.comparedCars
        };
        sessionStorage.setItem('chatbot_session_state', JSON.stringify(sessionData));
    } catch (e) {
        console.warn("Session state kaydedilemedi:", e);
    }
}

function loadSessionState() {
    try {
        const dataStr = sessionStorage.getItem('chatbot_session_state');
        if (dataStr) {
            const data = JSON.parse(dataStr);
            state.budget = data.budget;
            state.bodyType = data.bodyType;
            state.fuelType = data.fuelType;
            state.transmission = data.transmission;
            state.priorities = data.priorities || [];
            state.chatHistory = data.chatHistory || [];
            state.comparedCars = data.comparedCars || [];
            
            restoreUiFromState();
        }
    } catch (e) {
        console.warn("Session state yuklenemedi:", e);
    }
}

function restoreUiFromState() {
    // 1. Budget
    if (state.budget !== null) {
        elements.budgetSlider.value = state.budget;
        elements.budgetValue.innerText = `${(state.budget / 1000000).toFixed(2)} Milyon TL`;
    } else {
        elements.budgetSlider.value = elements.budgetSlider.max;
        elements.budgetValue.innerText = 'Limitsiz';
    }

    // 2. Body Type
    document.querySelectorAll('.body-card').forEach(card => {
        const val = card.dataset.val;
        if (state.bodyType === val) {
            card.classList.add('active');
        } else {
            card.classList.remove('active');
        }
    });

    // 3. Fuel Type
    document.querySelectorAll('#fuel-pills .pill').forEach(pill => {
        const val = pill.dataset.val;
        if (state.fuelType === val) {
            pill.classList.add('active');
        } else {
            pill.classList.remove('active');
        }
    });

    // 4. Transmission
    document.querySelectorAll('#trans-pills .pill').forEach(pill => {
        const val = pill.dataset.val;
        if (state.transmission === val) {
            pill.classList.add('active');
        } else {
            pill.classList.remove('active');
        }
    });

    // 5. Priorities
    document.querySelectorAll('#priority-pills .pill').forEach(pill => {
        const val = pill.dataset.val;
        if (state.priorities.includes(val)) {
            pill.classList.add('active');
        } else {
            pill.classList.remove('active');
        }
    });

    // 6. Comparisons
    renderComparisonDrawer();

    // 7. Chat History
    if (state.chatHistory.length > 0) {
        elements.chatMessagesBox.innerHTML = '';
        state.chatHistory.forEach(msg => {
            appendChatMessage(msg.role, msg.content);
        });
    }
}
