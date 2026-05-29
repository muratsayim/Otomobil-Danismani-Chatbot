# 🚗 Otomobil Danışmanı Chatbot

Bu proje, kullanıcılara bütçe, kasa tipi, yakıt türü ve şanzıman tercihlerine göre en uygun araç önerilerini sunan, araçları yan yana detaylı bir şekilde karşılaştıran ve otomobiller hakkında merak edilen soruları yanıtlayan **modern, premium tasarımlı ve çift modlu (Yapay Zeka / Yerel Mod)** bir web uygulamasıdır.

---

## ✨ Özellikler

*   **Hızlı Tercih Sihirbazı:** Sol panelden bütçenizi, kasa tipinizi, şanzıman ve sürüş önceliklerinizi (ekonomi, konfor, performans vb.) belirleyerek sizinle en uyumlu araçları saniyeler içinde listeleyebilirsiniz.
*   **Detaylı Karşılaştırma Havuzu:** Seçtiğiniz araçları "Karşılaştırma Masası"na ekleyerek fiyat, motor gücü, yakıt tüketimi, segment, artı ve eksi yönlerini yan yana şık bir Markdown tablosunda kıyaslayabilirsiniz.
*   **İkili Yapay Zeka Modu:**
    *   **Gemini AI Modu:** Web arayüzü üzerinden geçerli bir Gemini API anahtarı girdiğinizde, chatbot **Gemini 2.5 Flash** aklıyla 50 araçlık veritabanını analiz ederek sorularınızı yanıtlar.
    *   **Yerel Mod (Çevrimdışı):** API anahtarı girilmediğinde sistem kesintisiz çalışmaya devam eder. Kendi yazdığımız akıllı yerel kural motoru; Türkçe normalizasyonu, regex bütçe yakalama ve otomatik karşılaştırma analizi yaparak yerel veritabanından cevaplar üretir.
*   **Premium Karanlık Mod Tasarımı:** Glassmorphism (cam efekti), canlı neon geçişleri, pürüzsüz animasyonlar ve tamamen duyarlı (mobil uyumlu) modern arayüz tasarımı.
*   **Üye Kayıt & Giriş:** SQLite altyapısı ve güvenli şifreleme (password hashing) kullanan üyelik sistemi.

---

## 📁 Proje Yapısı

```text
automobile-advisor-chatbot/
├── main.py                # FastAPI sunucusu ve API uç noktaları
├── database.py            # 50 araçlık yerel veritabanı ve dinamik arama algoritması
├── user_db.py             # SQLite kullanıcı kayıt ve giriş yönetimi
├── requirements.txt       # Python bağımlılıkları (FastAPI, uvicorn, vb.)
├── run.bat                # Sunucuyu tek tıkla başlatan komut dosyası
├── .gitignore             # GitHub'a gitmeyecek gizli dosyaların listesi
├── README.md              # Proje dökümantasyonu (Bu dosya)
└── static/                # Ön yüz (Frontend) dosyaları
    ├── index.html         # Arayüz iskeleti
    ├── style.css          # Neon ve glassmorphism CSS stilleri
    └── app.js             # API bağlantıları ve dinamik UI yönetimi
```

---

## 🛠️ Kurulum ve Çalıştırma

### Gereksinimler
*   Python 3.8 veya üzeri sürüm bilgisayarınızda yüklü olmalıdır.

### Adımlar

1.  **Bağımlılıkları Yükleyin:**
    Proje klasörünün içinde terminali açarak gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Uygulamayı Başlatın:**
    *   **Windows'ta:** Klasörün içindeki `run.bat` dosyasına çift tıklayarak sunucuyu başlatabilirsiniz.
    *   **Alternatif Terminal Komutu:**
        ```bash
        python main.py
        ```

3.  **Tarayıcıda Açın:**
    Sunucu başladıktan sonra tarayıcınızdan aşağıdaki adresi açarak uygulamayı kullanmaya başlayabilirsiniz:
    👉 **[http://localhost:8000](http://localhost:8000)**

---

## 🔒 Güvenlik Uyarıları

*   Proje klasöründeki `.env` (varsa) ve `users.db` dosyaları, API anahtarı ve kullanıcı şifreleri gibi hassas bilgiler içerdiğinden `.gitignore` dosyası aracılığıyla GitHub'a **yüklenmeyecek şekilde** korunmaktadır.
