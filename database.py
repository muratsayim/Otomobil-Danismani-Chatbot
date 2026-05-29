import os
import re

# Türkçe karakter normalizasyonu ve küçük harf dönüşümü yapan yardımcı fonksiyon
def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    mapping = {
        "ı": "i", "ş": "s", "ç": "c", "ğ": "g", "ü": "u", "ö": "o",
        "İ": "i", "Ş": "s", "Ç": "c", "Ğ": "g", "Ü": "u", "Ö": "o"
    }
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text

# Yenilenmiş ve genişletilmiş 50 araçlık sıfırdan oluşturulan Türkiye Pazarı otomobil veritabanı
CAR_DATABASE = [
    {
        "id": 1,
        "brand": "Fiat",
        "model": "Egea Sedan",
        "segment": "C",
        "body_type": "Sedan",
        "fuel_type": "Benzin",
        "transmission": "Manuel",
        "price": 980000,
        "power": "95 BG",
        "consumption": "6.4 L/100km",
        "features": ["Geniş bagaj (520 lt)", "Ekonomik yedek parça", "Yaygın servis ağı"],
        "pros": ["Fiyat/performans oranı çok yüksek", "Bakım maliyetleri düşük", "İkinci el piyasası çok canlı"],
        "cons": ["Malzeme kalitesi ortalama", "Yüksek hızlarda içeri yol sesi alabiliyor"],
        "image_placeholder": "sedan_budget",
        "description": "Türkiye'nin en çok satan aile sedanı. Bütçe dostu, pratik ve yedek parçası son derece ucuz."
    },
    {
        "id": 2,
        "brand": "Renault",
        "model": "Clio",
        "segment": "B",
        "body_type": "Hatchback",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1150000,
        "power": "90 BG",
        "consumption": "5.3 L/100km",
        "features": ["Easy Link multimedya", "Full LED ön farlar", "Yokuş kalkış desteği"],
        "pros": ["Şehir içi manevra kabiliyeti", "Düşük yakıt tüketimi", "Şık ve modern dış tasarım"],
        "cons": ["Arka koltuk diz mesafesi dar", "Bagaj hacmi geniş aileler için yetersiz"],
        "image_placeholder": "hatchback_mid",
        "description": "Şehir içi pratikliği ve dinamik tasarımıyla Türkiye'nin en popüler B-hatchback modellerinden biri."
    },
    {
        "id": 3,
        "brand": "Toyota",
        "model": "Corolla Hybrid",
        "segment": "C",
        "body_type": "Sedan",
        "fuel_type": "Hibrit",
        "transmission": "Otomatik",
        "price": 1650000,
        "power": "140 BG",
        "consumption": "4.0 L/100km",
        "features": ["Toyota Safety Sense 3.0", "Kablosuz Apple CarPlay", "Adaptif Hız Kontrolü"],
        "pros": ["Şehir içi yakıt tüketimi olağanüstü düşük", "Sessiz ve pürüzsüz sürüş", "Çok yüksek marka güvenilirliği"],
        "cons": ["Otoyolda e-CVT şanzıman gürültülü çalışabiliyor", "Multimedya ekran grafikleri rakiplerine göre klasik"],
        "image_placeholder": "sedan_hybrid",
        "description": "Kendi kendini şarj eden hibrit motoruyla hem çevreci hem de yakıt tasarrufunda lider bir aile sedanı."
    },
    {
        "id": 4,
        "brand": "Volkswagen",
        "model": "Golf",
        "segment": "C",
        "body_type": "Hatchback",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1800000,
        "power": "116 BG",
        "consumption": "5.2 L/100km",
        "features": ["Dijital Kokpit Pro", "Kayar sinyalli LED farlar", "DSG şanzıman"],
        "pros": ["Üst düzey malzeme kalitesi ve yalıtım", "Mükemmel yol tutuş özellikleri", "Yüksek ikinci el değeri"],
        "cons": ["Dokunmatik kokpit kontrollerine alışmak zaman alıyor", "Fiyatı rakiplerine göre premium seviyede"],
        "image_placeholder": "hatchback_premium",
        "description": "Hatchback sınıfının dünya çapındaki referans modeli. Konfor, sürüş dinamikleri ve kaliteyi bir arada sunar."
    },
    {
        "id": 5,
        "brand": "Dacia",
        "model": "Duster",
        "segment": "C-SUV",
        "body_type": "SUV",
        "fuel_type": "LPG / Benzin",
        "transmission": "Manuel",
        "price": 1250000,
        "power": "100 BG",
        "consumption": "7.3 L/100km (LPG)",
        "features": ["Gelişmiş ECO-G fabrika çıkışlı LPG", "217 mm yerden yükseklik", "Modüler tavan barları"],
        "pros": ["LPG ile çok ekonomik seyahat", "Hafif arazi koşullarına tam uyum", "Yüksek sürüş pozisyonu ve geniş bagaj"],
        "cons": ["Kabinde sert plastik malzeme yoğunluğu", "Rüzgar ve yol sesi yalıtımı zayıf"],
        "image_placeholder": "suv_budget",
        "description": "Fiyat-performans odaklı SUV arayanların ilk tercihi. Hafif arazi şartlarında da son derece yeteneklidir."
    },
    {
        "id": 6,
        "brand": "Hyundai",
        "model": "Tucson",
        "segment": "C-SUV",
        "body_type": "SUV",
        "fuel_type": "Dizel",
        "transmission": "Otomatik",
        "price": 1950000,
        "power": "136 BG",
        "consumption": "5.7 L/100km",
        "features": ["Geniş panoramik cam tavan", "Kör nokta görüntüleme asistanı", "Parametrik gizli far tasarımı"],
        "pros": ["Fütüristik ve dikkat çekici dış görünüm", "Çok geniş iç hacim ve bagaj kapasitesi", "Zengin donanım paketleri"],
        "cons": ["Şehir içi dur-kalk trafiğinde yakıt tüketimi yükselebiliyor", "Süspansiyon yapısı sert kaçabiliyor"],
        "image_placeholder": "suv_mid",
        "description": "Göz alıcı tasarımı, geniş ailelere hitap eden iç mekanı ve gelişmiş teknolojik donanımlarıyla popüler bir SUV."
    },
    {
        "id": 7,
        "brand": "Tesla",
        "model": "Model Y",
        "segment": "D-SUV",
        "body_type": "SUV",
        "fuel_type": "Elektrik",
        "transmission": "Otomatik",
        "price": 2400000,
        "power": "299 BG (RWD)",
        "consumption": "15.7 kWh/100km",
        "features": ["Otopilot sistemi", "15 inç merkezi dokunmatik ekran", "Frunk (Ön bagaj) + Dev arka bagaj"],
        "pros": ["Müthiş hızlanma performansı", "Geniş Tesla Supercharger şarj altyapısı", "Kablosuz yazılım güncellemeleriyle sürekli güncellenmesi"],
        "cons": ["Fiziksel tuşların olmaması alışkanlık gerektirir", "Süspansiyonlar bozuk yollarda biraz sarsıntılı"],
        "image_placeholder": "suv_electric",
        "description": "Elektrikli araç devriminin öncülerinden. Devasa depolama alanları, teknolojik kokpiti ve yüksek performansı ile öne çıkar."
    },
    {
        "id": 8,
        "brand": "Chery",
        "model": "Tiggo 8 Pro",
        "segment": "D-SUV",
        "body_type": "SUV",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1780000,
        "power": "183 BG",
        "consumption": "8.1 L/100km",
        "features": ["7 koltuklu oturma düzeni", "Çift 12.3 inç bilgi-eğlence ekranı", "Isıtmalı ve havalandırmalı deri koltuklar"],
        "pros": ["Fiyatına göre olağanüstü zengin lüks donanım", "7 kişilik taşıma kapasitesi", "Güçlü turbo benzinli motor"],
        "cons": ["Rakiplerine göre yakıt tüketimi biraz yüksek", "Yazılım arayüzündeki Türkçe çevirilerde ufak hatalar mevcut"],
        "image_placeholder": "suv_7seater",
        "description": "Geniş aileler için tasarlanmış, sunduğu donanım listesiyle fiyatının çok ötesinde lüks hissettiren 7 kişilik SUV."
    },
    {
        "id": 9,
        "brand": "Peugeot",
        "model": "2008",
        "segment": "B-SUV",
        "body_type": "SUV",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1550000,
        "power": "130 BG",
        "consumption": "5.6 L/100km",
        "features": ["3D i-Cockpit gösterge paneli", "E-toggle şanzıman seçici", "LED pençe far tasarımı"],
        "pros": ["Agresif, modern ve son derece şık dış tasarım", "Kompakt boyutlarıyla kolay park ve manevra", "Küçük direksiyon ile eğlenceli sürüş"],
        "cons": ["Arka baş mesafesi uzun boylular için biraz kısıtlı", "i-Cockpit paneli bazı direksiyon pozisyonlarında perdelenebiliyor"],
        "image_placeholder": "suv_compact",
        "description": "Tasarımıyla dikkatleri üzerine çeken, şehir yaşamına mükemmel uyum sağlayan teknolojik ve dinamik kompakt SUV."
    },
    {
        "id": 10,
        "brand": "Honda",
        "model": "Civic Eco",
        "segment": "C",
        "body_type": "Sedan",
        "fuel_type": "LPG / Benzin",
        "transmission": "Otomatik",
        "price": 1720000,
        "power": "129 BG",
        "consumption": "6.8 L/100km (LPG)",
        "features": ["Fabrikasyon LPG kiti", "Honda SENSING güvenlik donanımları", "Ön koltuk ısıtma"],
        "pros": ["Fabrikasyon LPG sistemi ile bütçe dostu kullanım", "Mükemmel yol tutuş ve sürüş güvenliği", "Yüksek parça ömrü ve sorunsuz şanzıman"],
        "cons": ["Kabin yol sesi yalıtımı daha iyi olabilirdi", "Multimedya arayüzü rakiplerine kıyasla daha yavaş"],
        "image_placeholder": "sedan_lpg",
        "description": "Türkiye'de LPG ekonomisi ve Honda sürüş dinamiklerini bir arada arayan aileler için tasarlanmış klasik sedan."
    },
    {
        "id": 11,
        "brand": "Volvo",
        "model": "EX30",
        "segment": "B-SUV",
        "body_type": "SUV",
        "fuel_type": "Elektrik",
        "transmission": "Otomatik",
        "price": 2250000,
        "power": "272 BG",
        "consumption": "16.7 kWh/100km",
        "features": ["Harman Kardon ses sistemi", "Geri dönüştürülmüş ekolojik iç malzemeler", "Gelişmiş çarpışma önleme asistanları"],
        "pros": ["Üst düzey güvenlik teknolojileri", "Minimalist İskandinav tasarımı", "Çok seri ve performanslı sürüş karakteri"],
        "cons": ["Hız göstergesinin dahi sadece orta ekranda olması alışkanlık gerektirir", "Bagaj hacmi ve arka koltuk diz mesafesi dar"],
        "image_placeholder": "suv_premium_electric",
        "description": "Volvo'nun en çevreci ve en hızlı hızlanan kompakt elektrikli SUV modeli. Modern ve minimalist yaşamı sevenler için."
    },
    {
        "id": 12,
        "brand": "BMW",
        "model": "3 Serisi Sedan",
        "segment": "D",
        "body_type": "Sedan",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 3100000,
        "power": "170 BG",
        "consumption": "6.5 L/100km",
        "features": ["BMW Curved Display (Kavisli Ekran)", "M Sport sürüş dinamikleri paketleri", "Arkadan itişli sürüş mimarisi"],
        "pros": ["Sınıfının en iyi direksiyon hassasiyeti ve yol tutuşu", "Çok kaliteli malzeme ve lüks işçilik", "Karizmatik dış tasarım"],
        "cons": ["Satın alma, kasko ve servis maliyetleri çok yüksek", "Sert süspansiyonlar şehir içi çukurlarda sarsabiliyor"],
        "image_placeholder": "sedan_premium",
        "description": "Prestij ve sürüş keyfini bir arada sunan D segmenti ikonik spor sedan."
    },
    {
        "id": 13,
        "brand": "Cupra",
        "model": "Formentor",
        "segment": "C-SUV",
        "body_type": "SUV",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1980000,
        "power": "150 BG",
        "consumption": "6.2 L/100km",
        "features": ["Bakır detaylı spor iç mekan", "Kova tipi spor koltuklar", "Şerit takip ve adaptif hız asistanı"],
        "pros": ["SUV yüksekliği ile spor otomobil yol tutuş dengesi", "Sıra dışı ve son derece agresif tasarım", "Zengin standart donanım paketi"],
        "cons": ["Multimedya ekranı bazen yavaş çalışabiliyor", "Dar arka camlar nedeniyle geri görüş açıları biraz kısıtlı"],
        "image_placeholder": "suv_sporty",
        "description": "Geleneksel SUV tasarımlarından sıkılan, sportiflik ve performans hissiyatı arayan sürücülerin gözdesi Crossover SUV."
    },
    {
        "id": 14,
        "brand": "Ford",
        "model": "Focus",
        "segment": "C",
        "body_type": "Hatchback",
        "fuel_type": "Dizel",
        "transmission": "Otomatik",
        "price": 1580000,
        "power": "115 BG",
        "consumption": "4.8 L/100km",
        "features": ["Ford Co-Pilot360 sürüş destek sistemi", "8 ileri tork konvertörlü şanzıman", "13.2 inç dev multimedya ekranı"],
        "pros": ["Efsanevi yol tutuş ve sürüş güvenliği hissi", "Çok ekonomik dizel motor seçeneği", "Geniş iç mekan ve ergonomik koltuklar"],
        "cons": ["Kokpit tasarımı rakiplerine göre biraz sade ve geleneksel", "Dizel motorun ilk hızlanma performansı sınırlı"],
        "image_placeholder": "hatchback_diesel",
        "description": "Yol tutuş karakteriyle bilinen, hem yakıtta cimri hem de uzun yolda son derece güvenli hissettiren dizel otomatik hatchback."
    },
    {
        "id": 15,
        "brand": "Hyundai",
        "model": "Ioniq 5",
        "segment": "D-SUV",
        "body_type": "SUV",
        "fuel_type": "Elektrik",
        "transmission": "Otomatik",
        "price": 2150000,
        "power": "229 BG",
        "consumption": "16.8 kWh/100km",
        "features": ["800V ultra hızlı şarj mimarisi", "V2L (Araçtan dış cihazlara elektrik sağlama)", "İleri-geri kayabilen orta konsol"],
        "pros": ["Benzersiz piksel tasarımlı retro-fütüristik görünüm", "Düz zemin sayesinde oturma odası gibi ferah kabin", "Çok hızlı şarj olabilme (18 dakikada %10'dan %80'e)"],
        "cons": ["Arka cam sileceğinin olmaması yağışlı havalarda görüşü azaltıyor", "Geniş gövdesi dar şehir içi sokaklarında manevrayı zorlaştırabiliyor"],
        "image_placeholder": "suv_future_electric",
        "description": "Retro esintili tasarımı, devrim niteliğindeki şarj hızı ve modüler yaşam alanı sunan yeni nesil elektrikli SUV."
    },
    {
        "id": 16,
        "brand": "TOGG",
        "model": "T10X",
        "segment": "C-SUV",
        "body_type": "SUV",
        "fuel_type": "Elektrik",
        "transmission": "Otomatik",
        "price": 1450000,
        "power": "218 BG",
        "consumption": "16.9 kWh/100km",
        "features": ["Boydan boya uzanan 29 inç akıllı ekran", "Yerli Truemore dijital ekosistemi", "Cam tavan ve 360 kamera"],
        "pros": ["Fiyatına göre çok yüksek menzil ve performans", "Çok geniş ve heybetli iç mekan", "Sürekli güncellenen zengin dijital servisler"],
        "cons": ["Yazılım kararlılığında nadiren ufak tefek takılmalar olabiliyor", "Servis ağı diğer köklü markalara göre gelişim aşamasında"],
        "image_placeholder": "suv_togg",
        "description": "Türkiye'nin yerli ve milli akıllı cihazı. Geniş iç hacmi, muazzam akıllı ekranı ve elektrikli motoruyla çok popüler."
    },
    {
        "id": 17,
        "brand": "Opel",
        "model": "Corsa",
        "segment": "B",
        "body_type": "Hatchback",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1050000,
        "power": "100 BG",
        "consumption": "5.4 L/100km",
        "features": ["Opel Vizör ön panel tasarımı", "Intelli-Lux LED Matrix farlar", "Dijital gösterge paneli"],
        "pros": ["Şık, modern ve sportif Alman tasarımı", "EAT8 otomatik şanzımanın pürüzsüz geçişleri", "Yüksek yakıt tasarrufu"],
        "cons": ["Kabinde sert plastik kullanımı yaygın", "Arka koltuk diz mesafesi uzun boylular için kısıtlı"],
        "image_placeholder": "hatchback_corsa",
        "description": "Şehir içi pratikliği Alman teknolojisi ve modern vizör tasarımıyla birleştiren, yakıt tüketimi düşük popüler hatchback."
    },
    {
        "id": 18,
        "brand": "Peugeot",
        "model": "3008 Hybrid",
        "segment": "C-SUV",
        "body_type": "SUV",
        "fuel_type": "Hibrit",
        "transmission": "Otomatik",
        "price": 2100000,
        "power": "136 BG",
        "consumption": "5.1 L/100km",
        "features": ["21 inç panoramik kavisli ekran", "i-Toggles kişiselleştirilebilir kısayol tuşları", "Gelişmiş sürüş destek paketi"],
        "pros": ["Sınıfının en fütüristik kokpit tasarımı", "Yeni nesil 48V hibrit motor ile düşük tüketim", "Mükemmel sürüş konforu ve yalıtım"],
        "cons": ["Fiyatı segmentinin üst sınırlarında", "Yenilenen gövde tasarımı nedeniyle bagaj yüksekliği biraz azalmış"],
        "image_placeholder": "suv_3008",
        "description": "Fütüristik panoramik kokpiti, verimli hibrit motoru ve yeni nesil tasarımıyla SUV sınıfında standartları belirleyen model."
    },
    {
        "id": 19,
        "brand": "Volkswagen",
        "model": "Polo",
        "segment": "B",
        "body_type": "Hatchback",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1150000,
        "power": "95 BG",
        "consumption": "5.2 L/100km",
        "features": ["LED farlar ve stoplar", "Dijital Gösterge Paneli 'Digital Cockpit'", "Çift bölgeli otomatik klima"],
        "pros": ["Küçük Golf hissi veren yalıtım ve konfor", "Çok yüksek malzeme ve montaj kalitesi", "İkinci el piyasasında altın değerinde olması"],
        "cons": ["Tasarımı rakiplerine göre oldukça muhafazakar", "Standart donanım listesi bazı rakiplerine göre boş"],
        "image_placeholder": "hatchback_polo",
        "description": "Konforu, yalıtımı ve tok sürüş hissiyle B segmentinin en olgun ve en çok güvenilen hatchback modellerinden biri."
    },
    {
        "id": 20,
        "brand": "Skoda",
        "model": "Octavia",
        "segment": "C",
        "body_type": "Sedan",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1650000,
        "power": "150 BG",
        "consumption": "5.0 L/100km",
        "features": ["600 litrelik devasa bagaj hacmi", "Elektrikli bagaj kapağı", "Shift-by-wire vites sistemi"],
        "pros": ["D segmentine göz kırpan muazzam arka diz mesafesi", "Liftback bagaj kapağı ile inanılmaz yükleme kolaylığı", "Mild-hybrid e-Tec motorun yüksek ekonomisi"],
        "cons": ["Multimedya sisteminde bazen yazılımsal sıfırlanmalar olabiliyor", "Süspansiyonlar arkada yarı bağımsız olduğu için yol dalgalanmalarını kabine iletebilir"],
        "image_placeholder": "sedan_octavia",
        "description": "Geniş bagajı ve arka diz mesafesiyle Türk ailelerinin en sevdiği, konfor odaklı efsanevi C-Sedan/Liftback modeli."
    },
    {
        "id": 21,
        "brand": "Nissan",
        "model": "Qashqai",
        "segment": "C-SUV",
        "body_type": "SUV",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1850000,
        "power": "158 BG",
        "consumption": "6.2 L/100km",
        "features": ["ProPILOT Sürüş Asistanı", "Nappa deri koltuklar ve masaj fonksiyonu", "12.3 inç dokunmatik ekran"],
        "pros": ["Zengin güvenlik donanımları ve asistanları", "Çok konforlu koltuklar ve sürüş pozisyonu", "Türkiye'de çok güçlü bir marka imajı"],
        "cons": ["Kabindeki eşya gözlerinin sayısı az", "X-Tronic şanzıman ani hızlanmalarda motor sesini kabine alabiliyor"],
        "image_placeholder": "suv_qashqai",
        "description": "Türkiye'de SUV akımını başlatan model. Gelişmiş güvenlik asistanları ve konforlu sürüşüyle crossover liderlerinden."
    },
    {
        "id": 22,
        "brand": "Seat",
        "model": "Leon",
        "segment": "C",
        "body_type": "Hatchback",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1480000,
        "power": "110 BG",
        "consumption": "5.3 L/100km",
        "features": ["Infinite LED stop tasarımı", "10.25 inç dijital gösterge paneli", "Üç bölgeli otomatik klima"],
        "pros": ["Genç ve son derece sportif dış görünüm", "İç mekan genişliği rakiplerine göre gayet iyi", "Ekonomik ve sessiz TSI motor"],
        "cons": ["Sert süspansiyon yapısı bozuk yollarda konforu azaltıyor", "Kabinde neredeyse hiç fiziksel tuş yok, her şey ekrandan yönetiliyor"],
        "image_placeholder": "hatchback_leon",
        "description": "Dinamik tasarımı, sportif kokpiti ve zengin donanımıyla özellikle genç sürücülerin en çok tercih ettiği C-Hatchback."
    },
    {
        "id": 23,
        "brand": "Kia",
        "model": "Sportage",
        "segment": "C-SUV",
        "body_type": "SUV",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1900000,
        "power": "150 BG",
        "consumption": "6.7 L/100km",
        "features": ["Kavisli çift ekran tasarımı", "Kör nokta izleme ekranı (kadran içi)", "Isıtmalı arka koltuklar"],
        "pros": ["Ezber bozan çok cesur ve teknolojik tasarım", "Çok geniş ve ferah arka yaşam alanı", "Zengin konfor donanımları"],
        "cons": ["Yakıt tüketimi şehir içi trafikte biraz yüksek", "Otoyol hızlarında dikiz aynalarından rüzgar sesi alabiliyor"],
        "image_placeholder": "suv_sportage",
        "description": "Sıra dışı tasarımı, modern kavisli paneli ve zengin donanımıyla son dönemin en popüler aile SUV'larından biri."
    },
    {
        "id": 24,
        "brand": "Hyundai",
        "model": "i20",
        "segment": "B",
        "body_type": "Hatchback",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 980000,
        "power": "100 BG",
        "consumption": "5.7 L/100km",
        "features": ["10.25 inç multimedya ekranı", "Şerit takip asistanı", "Geri görüş kamerası"],
        "pros": ["Türkiye'de üretilmesi sebebiyle uygun servis ve yedek parça", "B segmenti standartlarına göre geniş bagaj ve iç hacim", "Hafif direksiyonu ile kolay şehir içi sürüş"],
        "cons": ["Yüksek hızlarda kabine yol sesi alabiliyor", "Atmosferik motor seçeneğinde performans oldukça zayıf (Turbo motor tercih edilmeli)"],
        "image_placeholder": "hatchback_i20",
        "description": "Türkiye'de üretilen, geniş kabin hacmi ve modern tasarımıyla öne çıkan şehir içi dostu B-hatchback."
    },
    {
        "id": 25,
        "brand": "Dacia",
        "model": "Sandero Stepway",
        "segment": "B",
        "body_type": "SUV",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1080000,
        "power": "90 BG",
        "consumption": "5.6 L/100km",
        "features": ["Modüler tavan barları", "Media Display multimedya sistemi", "Yüksek sürüş pozisyonu"],
        "pros": ["Otomatik şanzımanlı en uygun fiyatlı crossover modellerinden biri", "Yüksek yapısı sayesinde kaldırım ve çukurlarda rahatlık", "Bakım maliyetlerinin düşüklüğü"],
        "cons": ["Ses yalıtımı zayıf", "Kabin içi malzeme kalitesi sert plastik ağırlıklı"],
        "image_placeholder": "crossover_stepway",
        "description": "Ekonomik, yüksek ve otomatik vitesli bir şehir aracı arayanlar için en mantıklı crossover seçeneklerinden."
    },
    {
        "id": 26,
        "brand": "Renault",
        "model": "Megane Sedan",
        "segment": "C",
        "body_type": "Sedan",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1250000,
        "power": "140 BG",
        "consumption": "5.9 L/100km",
        "features": ["Dikey Tesla tipi ekran", "Panoramik açılır cam tavan", "Eller serbest kart sistemi"],
        "pros": ["1.3 TCe motorun mükemmel performansı ve makul tüketimi", "Büyük bagaj hacmi (503 lt)", "Çok yaygın servis ağı ve yedek parça bulunabilirliği"],
        "cons": ["Arka baş mesafesi tavan eğimi nedeniyle kısıtlı", "İç mekan malzeme kalitesi yaşını belli ediyor"],
        "image_placeholder": "sedan_megane",
        "description": "Türkiye'de hem bireysel hem filo pazarının gözbebeği. Güçlü motoru ve sedan pratikliğiyle klasikleşmiş bir model."
    },
    {
        "id": 27,
        "brand": "Opel",
        "model": "Astra",
        "segment": "C",
        "body_type": "Hatchback",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1550000,
        "power": "130 BG",
        "consumption": "5.6 L/100km",
        "features": ["Pure Panel dijital kokpit", "Intelli-Lux LED Pixel farlar", "Ergonomik AGR onaylı koltuklar"],
        "pros": ["Keskin, modern ve dikkat çekici Alman tasarımı", "Uzun yolda yormayan ortopedik koltuklar", "Çok kararlı ve sessiz otoban sürüşü"],
        "cons": ["Arka koltuk diz mesafesi sınıf liderlerinin gerisinde", "Piyano siyahı iç kaplamalar çok çabuk çizilebiliyor"],
        "image_placeholder": "hatchback_astra",
        "description": "Tasarım dili tamamen yenilenen, sportif ruhu ve Alman sürüş disiplinini yaşatan şık C-hatchback."
    },
    {
        "id": 28,
        "brand": "Chery",
        "model": "Omoda 5",
        "segment": "C-SUV",
        "body_type": "SUV",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1420000,
        "power": "183 BG",
        "consumption": "7.5 L/100km",
        "features": ["Çift kavisli ekran", "Sesli komut asistanı", "Sportif entegre ön koltuklar"],
        "pros": ["Sıra dışı fütüristik tasarım", "Fiyatına göre muhteşem motor gücü ve donanım", "Zengin güvenlik ekipmanları"],
        "cons": ["Yakıt tüketimi şehir içinde rahatlıkla 9-10 litrelere çıkabiliyor", "Süspansiyonlar yüksek hız virajlarında gövdeyi çok yatırabiliyor"],
        "image_placeholder": "suv_omoda5",
        "description": "Gençleri ve teknoloji meraklılarını hedefleyen, fütüristik tasarımı ve zengin donanımıyla pazar payını hızla artıran SUV."
    },
    {
        "id": 29,
        "brand": "MG",
        "model": "MG4 Electric",
        "segment": "C",
        "body_type": "Hatchback",
        "fuel_type": "Elektrik",
        "transmission": "Otomatik",
        "price": 1390000,
        "power": "170 BG",
        "consumption": "16.0 kWh/100km",
        "features": ["Arkadan itişli sürüş karakteri", "350 km WLTP menzili", "Aktif hava ızgarası"],
        "pros": ["Türkiye'de satın alınabilecek en uygun fiyatlı elektrikli C segmenti araçlardan biri", "Arkadan itiş sayesinde çok keyifli yol tutuş", "Geniş iç kabin"],
        "cons": ["Yazılım arayüzü bazen yavaş tepki veriyor", "Plastik malzeme kalitesi bazı noktalarda basit kalıyor"],
        "image_placeholder": "hatchback_mg4",
        "description": "Elektrikli otomobil dünyasına adım atmak isteyenler için fiyat, performans ve menzili mükemmel dengeleyen hatchback."
    },
    {
        "id": 30,
        "brand": "Citroen",
        "model": "C3",
        "segment": "B",
        "body_type": "Hatchback",
        "fuel_type": "Benzin",
        "transmission": "Manuel",
        "price": 920000,
        "power": "83 BG",
        "consumption": "5.5 L/100km",
        "features": ["Airbump yan korumalar", "Citroen Advanced Comfort koltuklar", "Çift renk tavan kombinasyonu"],
        "pros": ["Sınıfının en konforlu ve yumuşak süspansiyon sistemi", "Özgün ve sevimli dış tasarım", "Bütçe dostu satın alma fiyatı"],
        "cons": ["Motor gücü düşük, rampalarda vites düşürmek gerekiyor", "Otomatik şanzıman olmaması yoğun trafikte yorucu olabilir"],
        "image_placeholder": "hatchback_c3",
        "description": "Sürüş konforu ve yumuşak koltuklarıyla bilinen, renkli tasarımıyla tarz sahibi, bütçe dostu hatchback."
    },
    {
        "id": 31,
        "brand": "Ford",
        "model": "Puma",
        "segment": "B",
        "body_type": "SUV",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1450000,
        "power": "125 BG",
        "consumption": "5.4 L/100km",
        "features": ["MegaBox bagaj altı saklama alanı (yıkanabilir)", "Seçilebilir sürüş modları", "Şerit takip sistemi"],
        "pros": ["Sınıfının en eğlenceli ve dinamik sürüş karakteri", "Mild-hybrid desteğiyle düşük yakıt tüketimi", "Megabox ile çok pratik bagaj çözümü"],
        "cons": ["Arka koltuk baş ve diz mesafesi rakiplerine göre biraz dar", "Süspansiyonlar sportiflik uğruna konfordan ödün veriyor"],
        "image_placeholder": "crossover_puma",
        "description": "Sportif sürüşü ve sevimli tasarımıyla öne çıkan, yenilikçi bagaj çözümleri sunan eğlenceli bir şehir crossoverı."
    },
    {
        "id": 32,
        "brand": "Audi",
        "model": "A3 Sportback",
        "segment": "C",
        "body_type": "Hatchback",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 2100000,
        "power": "150 BG",
        "consumption": "5.2 L/100km",
        "features": ["Audi Sanal Kokpit Plus", "Matrix LED farlar", "Panoramik cam tavan"],
        "pros": ["Üst düzey premium marka imajı", "Sarsıntısız çalışan şanzıman ve motor uyumu", "Kusursuz ses yalıtımı"],
        "cons": ["Ekstra donanımlar satın alma fiyatını aşırı yükseltiyor", "Servis ve bakım giderleri yüksek"],
        "image_placeholder": "hatchback_a3",
        "description": "Premium kompakt sınıfta kalitesi, prestiji ve sürüş olgunluğuyla fark yaratan lüks hatchback."
    },
    {
        "id": 33,
        "brand": "Mercedes-Benz",
        "model": "C-Serisi",
        "segment": "D",
        "body_type": "Sedan",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 3250000,
        "power": "204 BG",
        "consumption": "6.6 L/100km",
        "features": ["MBUX dikey dev multimedya paneli", "Arka aks yönlendirme sistemi (isteğe bağlı)", "Dijital Işık far teknolojisi"],
        "pros": ["Küçük S-Serisi hissi veren muazzam teknoloji ve lüks", "Harika sürüş konforu ve sessizlik", "Çok güçlü performans"],
        "cons": ["Fiyatı oldukça yüksek", "Arka koltuk yaşam alanı boyutlarına göre beklenenden biraz daha dar"],
        "image_placeholder": "sedan_cclass",
        "description": "Lüks ve prestij denildiğinde akla ilk gelen, konforu ve teknolojiyi en üst seviyede sunan premium sedan."
    },
    {
        "id": 34,
        "brand": "Skoda",
        "model": "Superb",
        "segment": "D",
        "body_type": "Sedan",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 2350000,
        "power": "150 BG",
        "consumption": "5.8 L/100km",
        "features": ["Simply Clever pratik çözümler (şemsiye, buz kazıyıcı)", "Masajlı ve havalandırmalı koltuklar", "Geri çekilebilir arka makam perdeleri"],
        "pros": ["Neredeyse limuzin seviyesinde arka diz mesafesi", "Muazzam bagaj hacmi ve yükleme alanı", "Yumuşacık sürüş konforu"],
        "cons": ["Devasa boyutları şehir içinde park etmeyi zorlaştırıyor", "Tasarımı bazı sürücüler için fazla klasik bulunabilir"],
        "image_placeholder": "sedan_superb",
        "description": "Genişlik, konfor ve fonksiyonellikte sınırları zorlayan, makam aracı olarak dahi kullanılan devasa sedan."
    },
    {
        "id": 35,
        "brand": "Volkswagen",
        "model": "Tiguan",
        "segment": "C-SUV",
        "body_type": "SUV",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 2250000,
        "power": "150 BG",
        "consumption": "6.5 L/100km",
        "features": ["IQ.LIGHT HD Matrix farlar", "OLED ekranlı sürüş deneyim kumandası", "Dinamik Şasi Kontrolü DCC Pro"],
        "pros": ["Kusursuza yakın süspansiyon ve konfor dengesi", "Çok yüksek malzeme kalitesi ve yalıtım", "Geniş ve kızaklı arka koltuklar sayesinde esnek bagaj"],
        "cons": ["Rakiplerine göre yüksek fiyat etiketi", "Tasarımı yenilense de hala sade kalıyor"],
        "image_placeholder": "suv_tiguan",
        "description": "C-SUV sınıfının referans aile modellerinden biri. Konforu, pratikliği ve yüksek kalitesiyle ailelerin favorisi."
    },
    {
        "id": 36,
        "brand": "Suzuki",
        "model": "Vitara Hybrid",
        "segment": "B",
        "body_type": "SUV",
        "fuel_type": "Hibrit",
        "transmission": "Otomatik",
        "price": 1390000,
        "power": "129 BG",
        "consumption": "5.4 L/100km",
        "features": ["AllGrip 4x4 sürüş sistemi seçeneği", "Çift kademeli panoramik tavan", "Kör nokta uyarı sistemi"],
        "pros": ["Kendi sınıfında gerçek 4x4 yeteneği sunabilen ender modellerden", "Japon sorunsuzluğu ve yüksek güvenilirlik", "Hafif hibrit ile ekonomik yakıt sarfiyatı"],
        "cons": ["İç mekan tasarımı ve ekran teknolojisi eski kalıyor", "Kabin içi sert plastik yoğunluğu yüksek"],
        "image_placeholder": "suv_vitara",
        "description": "Hem şehir içinde pratik ve ekonomik, hem de zorlu yol şartlarında 4x4 çekiş sistemiyle güven veren dayanıklı SUV."
    },
    {
        "id": 37,
        "brand": "Peugeot",
        "model": "408",
        "segment": "C",
        "body_type": "SUV",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1950000,
        "power": "130 BG",
        "consumption": "6.0 L/100km",
        "features": ["Aslan dişi farlar ve 3D stoplar", "i-Cockpit 3D gösterge paneli", "Geniş bagaj (536 lt)"],
        "pros": ["Göz alıcı Fastback (eğimli tavan) tasarım", "Yüksek sürüş pozisyonu ile sedan konforu harmanı", "Çok geniş diz mesafesi"],
        "cons": ["Arka eğimli tavan uzun boylular için iniş binişte dikkat gerektiriyor", "Arka cam silecek donanımı yok"],
        "image_placeholder": "crossover_408",
        "description": "Sedan, hatchback ve SUV hatlarını birleştiren, dinamik hatlarıyla yolda tüm bakışları üzerine toplayan yenilikçi Fastback."
    },
    {
        "id": 38,
        "brand": "Fiat",
        "model": "Egea Cross",
        "segment": "C",
        "body_type": "SUV",
        "fuel_type": "Benzin",
        "transmission": "Manuel",
        "price": 1050000,
        "power": "95 BG",
        "consumption": "6.5 L/100km",
        "features": ["10 inç tablet ekran", "Cross gövde koruma plastikleri", "LED ön farlar"],
        "pros": ["Türkiye'nin en uygun fiyatlı sıfır SUV/Crossover seçeneği", "Bakım ve yedek parça maliyetlerinin çok ucuz olması", "Geniş servis ağı"],
        "cons": ["Rüzgar ve yol sesi yalıtımı zayıf", "Motor performansı yüklü durumlarda sınırlı"],
        "image_placeholder": "crossover_egeacross",
        "description": "Egea ailesinin crossover üyesi. Yüksek yapısı, crossover detayları ve bütçe dostu fiyatıyla çok tercih ediliyor."
    },
    {
        "id": 39,
        "brand": "BYD",
        "model": "Atto 3",
        "segment": "C-SUV",
        "body_type": "SUV",
        "fuel_type": "Elektrik",
        "transmission": "Otomatik",
        "price": 1790000,
        "power": "204 BG",
        "consumption": "15.6 kWh/100km",
        "features": ["Dönebilen 15.6 inç ekran", "Güvenli Blade batarya teknolojisi", "Elektrikli bagaj kapısı"],
        "pros": ["Çok zengin güvenlik ve teknoloji donanımı", "Blade pil teknolojisi ile yüksek güvenlik ve uzun ömür", "Performans ve menzil dengesi"],
        "cons": ["İç tasarımdaki spor salonu temalı detaylar (gitar telleri vb.) herkesin beğenisine uymayabilir", "Maksimum şarj hızı rakiplerinin biraz gerisinde"],
        "image_placeholder": "suv_atto3",
        "description": "Dünya devi BYD'nin Türkiye'ye getirdiği ilk tamamen elektrikli SUV modeli. Yenilikçi pili ve dönebilen ekranıyla dikkat çeker."
    },
    {
        "id": 40,
        "brand": "Toyota",
        "model": "Yaris Cross Hybrid",
        "segment": "B",
        "body_type": "SUV",
        "fuel_type": "Hibrit",
        "transmission": "Otomatik",
        "price": 1420000,
        "power": "116 BG",
        "consumption": "4.4 L/100km",
        "features": ["Toyota Safety Sense", "Kendi kendini şarj eden 1.5 hibrit motor", "Kablosuz akıllı telefon bağlantısı"],
        "pros": ["Şehir içinde koklayarak yakıt tüketen motor", "Yüksek sürüş pozisyonu ve kolay park", "Çok canlı ikinci el pazarı"],
        "cons": ["Arka koltuk diz mesafesi oldukça dar", "Otoyol hızlarında kabin içine tekerlek sesi alabiliyor"],
        "image_placeholder": "suv_yaris_cross",
        "description": "Şehir hayatı için optimize edilmiş, yüksek yapılı, manevra kabiliyeti yüksek ve yakıt cimrisi B-SUV."
    },
    {
        "id": 41,
        "brand": "Renault",
        "model": "Austral Hybrid",
        "segment": "C-SUV",
        "body_type": "SUV",
        "fuel_type": "Hibrit",
        "transmission": "Otomatik",
        "price": 2050000,
        "power": "200 BG",
        "consumption": "4.8 L/100km",
        "features": ["OpenR Link 12 inç ekran (Google entegreli)", "4Control (Arka tekerlekten yönlendirme)", "Kızaklı arka koltuklar"],
        "pros": ["Tam hibrit motorun 200 beygirlik gücü ve inanılmaz ekonomisi", "Arka aks yönlendirme ile hatchback pratikliğinde dönüş çapı", "Çok modern kokpit"],
        "cons": ["Sert süspansiyon yapısı bazı durumlarda konforu baltalayabiliyor", "Fiyatı benzinli C-SUV rakiplerinden daha yukarıda"],
        "image_placeholder": "suv_austral",
        "description": "Renault'nun yeni nesil teknolojik SUV'u. Tam hibrit sistemi ve 4Control teknolojisiyle sınıfının en gelişmiş modellerinden."
    },
    {
        "id": 42,
        "brand": "Cupra",
        "model": "Leon",
        "segment": "C",
        "body_type": "Hatchback",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1720000,
        "power": "150 BG",
        "consumption": "5.6 L/100km",
        "features": ["Bakır detaylı spor gövde", "Full LED mercekli ön farlar", "F1 vites kulakçıkları"],
        "pros": ["Sportif sürüş dinamikleri ve çok şık duruş", "Zengin standart donanım", "Hızlı vites geçişleri sunan DSG şanzıman"],
        "cons": ["Normal Seat Leon'a göre daha sert süspansiyonlar", "Alçak yapısı nedeniyle iniş binişler klasik araçlara göre daha dik duruş gerektirir"],
        "image_placeholder": "hatchback_cupraleon",
        "description": "Seat'ın performans markası Cupra imzalı, sportif ruhlu, tasarımı ve sesiyle adrenalin arayanların hatchbacki."
    },
    {
        "id": 43,
        "brand": "Jeep",
        "model": "Renegade Hybrid",
        "segment": "B",
        "body_type": "SUV",
        "fuel_type": "Hibrit",
        "transmission": "Otomatik",
        "price": 1690000,
        "power": "130 BG",
        "consumption": "5.1 L/100km",
        "features": ["Karakteristik 7 gözlü Jeep ızgarası", "Uconnect multimedya sistemi", "Şeritten ayrılma ikazı"],
        "pros": ["Kutusal retro tasarımı ile çok karakteristik görünüm", "Yüksek tavan yapısı sayesinde çok ferah baş mesafesi", "E-Hybrid motorun şehir içi ekonomisi"],
        "cons": ["Köşeli tasarımı nedeniyle yüksek hızlarda rüzgar sesi alabiliyor", "Bagaj hacmi rakiplerinin gerisinde (351 lt)"],
        "image_placeholder": "suv_renegade",
        "description": "Karakterli köşeli hatları ve Jeep genlerini taşıyan tasarımıyla şehir içi macera severlerin tercihi hibrit SUV."
    },
    {
        "id": 44,
        "brand": "Volvo",
        "model": "XC40",
        "segment": "C-SUV",
        "body_type": "SUV",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 2750000,
        "power": "197 BG",
        "consumption": "6.9 L/100km",
        "features": ["City Safety güvenlik sistemi", "Panoramik açılır cam tavan", "Kablosuz telefon şarjı"],
        "pros": ["Sınıfının en güvenli gövde yapılarından biri", "İskandinav sade şıklığı ve premium malzeme kalitesi", "Çok yüksek sürüş hakimiyeti"],
        "cons": ["Şehir içi yakıt tüketimi 8-9 litrelere yaklaşabiliyor", "Multimedya ekranı dikey yapısıyla alışkanlık gerektirir"],
        "image_placeholder": "suv_xc40",
        "description": "Volvo güvenliğini ve premium konforu aile boyutlarında sunan, zamansız tasarıma sahip lüks SUV."
    },
    {
        "id": 45,
        "brand": "Kia",
        "model": "Picanto",
        "segment": "A",
        "body_type": "Hatchback",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 890000,
        "power": "67 BG",
        "consumption": "5.3 L/100km",
        "features": ["8 inç dokunmatik ekran", "Geri görüş kamerası", "Kompakt boyutlar"],
        "pros": ["Şehir içi park yeri bulma derdine son veren boyutlar", "Çok kolay kullanım ve hafif direksiyon", "Ekonomik bakım giderleri"],
        "cons": ["Bagaj hacmi çok dar (255 lt)", "Otoyol sürüşlerinde ve rampalarda motor gücü yetersiz kalabiliyor"],
        "image_placeholder": "hatchback_picanto",
        "description": "Şehir içi yoğun trafikte pratik kullanım, kolay park imkanı ve sevimli tasarımıyla öne çıkan A segmenti mini hatchback."
    },
    {
        "id": 46,
        "brand": "Hyundai",
        "model": "Bayon",
        "segment": "B",
        "body_type": "SUV",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1080000,
        "power": "100 BG",
        "consumption": "6.1 L/100km",
        "features": ["10.25 inç dijital gösterge", "Ok şeklinde arka stop tasarımı", "Geri görüş kamerası"],
        "pros": ["Türkiye'de üretilme avantajıyla uygun fiyat ve bol parça", "Geniş bagaj (411 lt) ve hatchback pratikliği", "Sorunsuz şanzıman"],
        "cons": ["Kabin içi plastik kalitesi ortalama", "Yüksek hızlarda yol sesi yalıtımı geliştirilebilir"],
        "image_placeholder": "suv_bayon",
        "description": "Türkiye'de üretilen, hatchback boyutlarında SUV pratikliği ve sıra dışı tasarım detayları sunan kompakt crossover."
    },
    {
        "id": 47,
        "brand": "Opel",
        "model": "Mokka",
        "segment": "B",
        "body_type": "SUV",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1520000,
        "power": "130 BG",
        "consumption": "5.9 L/100km",
        "features": ["Opel Vizör ön panel", "Pure Panel kokpit ekranları", "18 inç alaşımlı jantlar"],
        "pros": ["Çok şık, dikkat çekici ve modern dış tasarım", "Kompakt boyutlarına göre geniş ön yaşam alanı", "Verimli turbo motor performansı"],
        "cons": ["Arka koltuk alanı tavan çizgisi nedeniyle karanlık ve dar hissettirebilir", "Bagaj hacmi rakiplerine kıyasla ortalama seviyede (350 lt)"],
        "image_placeholder": "suv_mokka",
        "description": "Opel Vizör tasarımıyla tamamen kabuk değiştiren, şehirli, son derece tarz sahibi ve modern B-SUV."
    },
    {
        "id": 48,
        "brand": "BMW",
        "model": "iX3",
        "segment": "D-SUV",
        "body_type": "SUV",
        "fuel_type": "Elektrik",
        "transmission": "Otomatik",
        "price": 3850000,
        "power": "286 BG",
        "consumption": "18.5 kWh/100km",
        "features": ["Harman Kardon ses sistemi", "BMW Live Cockpit Professional", "Adaptif M Süspansiyon"],
        "pros": ["Geleneksel BMW sürüş kalitesi ve lüks hissinin korunması", "Çok verimli elektrik tüketimi ve 460 km menzil", "Kusursuz sessizlik ve konfor"],
        "cons": ["Elektrikli araç için tasarlanmış özel bir platform olmadığından şaft tüneli kabinde yer kaplıyor", "Fiyatı yüksek vergi dilimlerinden etkileniyor"],
        "image_placeholder": "suv_ix3",
        "description": "BMW X3'ün tamamen elektrikli versiyonu. BMW kalitesini sıfır emisyon ve yüksek elektrik performansı ile birleştirir."
    },
    {
        "id": 49,
        "brand": "Citroen",
        "model": "C5 Aircross",
        "segment": "C-SUV",
        "body_type": "SUV",
        "fuel_type": "Benzin",
        "transmission": "Otomatik",
        "price": 1820000,
        "power": "130 BG",
        "consumption": "6.2 L/100km",
        "features": ["Kademeli Hidrolik Destekli Süspansiyon", "3 adet bağımsız arka koltuk", "Geniş panoramik cam tavan"],
        "pros": ["Uçan halı hissi veren sınıf lideri sürüş konforu", "Bağımsız arka koltuklar sayesinde muazzam esneklik", "Çok geniş bagaj (580 lt)"],
        "cons": ["Yumuşak süspansiyonlar nedeniyle virajlarda yatma eğilimi gösterebilir", "Multimedya arayüzü biraz eski tip"],
        "image_placeholder": "suv_c5",
        "description": "Konfor odaklı ailelerin C-SUV segmentindeki bir numaralı tercihi. Benzersiz süspansiyon sistemiyle donatılmıştır."
    },
    {
        "id": 50,
        "brand": "Fiat",
        "model": "Panda Hybrid",
        "segment": "A",
        "body_type": "Hatchback",
        "fuel_type": "Hibrit",
        "transmission": "Manuel",
        "price": 850000,
        "power": "70 BG",
        "consumption": "4.1 L/100km",
        "features": ["Uconnect bluetooth radyo", "City modu (ekstra yumuşak direksiyon)", "Tavan rayları"],
        "pros": ["Türkiye'de satın alınabilecek en ucuz hibrit sıfır otomobil", "İnanılmaz düşük yakıt tüketimi", "Yoğun şehir trafiğinde kolay kullanım"],
        "cons": ["Donanım listesi oldukça kısıtlı", "Güvenlik teknolojileri ve otoyol performansı zayıf"],
        "image_placeholder": "hatchback_panda",
        "description": "Şehir içi ulaşıma en ucuz ve en ekonomik yoldan çözüm arayanların gözdesi ikonik mini şehir otomobili."
    }
]

# Belirtilen id'ye göre araç detayını getirir
def get_car_by_id(car_id):
    for car in CAR_DATABASE:
        if car["id"] == car_id:
            return car
    return None

# Kriterlere göre araç filtreleme ve puanlama algoritması
def filter_cars(budget=None, body_types=None, fuel_types=None, transmissions=None, priorities=None):
    filtered = []
    
    for car in CAR_DATABASE:
        # Bütçe filtresi
        if budget is not None and car["price"] > budget:
            continue
            
        # Kasa Tipi filtresi
        if body_types:
            if isinstance(body_types, str) and car["body_type"].lower() != body_types.lower():
                continue
            elif isinstance(body_types, list) and car["body_type"].lower() not in [b.lower() for b in body_types]:
                continue
                
        # Yakıt Tipi filtresi
        if fuel_types:
            # Örneğin "Hibrit" arandığında veritabanındaki "Hibrit" veya "LPG / Benzin" eşleşebilir
            # Normalizasyon yapıp içerip içermediğine bakalım
            car_fuel_norm = normalize_text(car["fuel_type"])
            if isinstance(fuel_types, str):
                fuel_norm = normalize_text(fuel_types)
                if fuel_norm not in car_fuel_norm:
                    continue
            elif isinstance(fuel_types, list):
                match_any = False
                for f in fuel_types:
                    if normalize_text(f) in car_fuel_norm:
                        match_any = True
                        break
                if not match_any:
                    continue
                
        # Şanzıman filtresi
        if transmissions:
            if isinstance(transmissions, str) and car["transmission"].lower() != transmissions.lower():
                continue
            elif isinstance(transmissions, list) and car["transmission"].lower() not in [t.lower() for t in transmissions]:
                continue

        # Zeki Puanlama Motoru
        score = 0
        
        # Önceliklere göre puan artırma
        if priorities:
            priorities_lower = [p.lower() for p in priorities]
            
            # 1. Ekonomi & Yakıt Tasarrufu
            if any(x in priorities_lower for x in ["ekonomi", "tasarruf", "ucuz", "yakit"]):
                # Hibrit, Elektrik veya LPG en ekonomik kabul edilir
                if any(f in car["fuel_type"] for f in ["Hibrit", "Elektrik", "LPG"]):
                    score += 3
                
                # Tüketim sayısal değerini parse et
                try:
                    consumption_match = re.search(r'[\d\.]+', car["consumption"].replace(',', '.'))
                    if consumption_match:
                        consumption_val = float(consumption_match.group())
                        # Elektrikli araç tüketimi kwh/100km olduğu için 15-18 arası düşüktür
                        if "kwh" in car["consumption"].lower():
                            score += 3
                        elif consumption_val < 5.0:
                            score += 3
                        elif consumption_val < 6.0:
                            score += 1
                except Exception:
                    pass
                
                # Fiyat avantajı
                if car["price"] < 1200000:
                    score += 2
                elif car["price"] < 1800000:
                    score += 1
                    
            # 2. Hız & Yüksek Performans
            if any(x in priorities_lower for x in ["performans", "hiz", "guc", "seri"]):
                try:
                    power_match = re.search(r'\d+', car["power"])
                    if power_match:
                        power_val = int(power_match.group())
                        if power_val > 200:
                            score += 4
                        elif power_val >= 140:
                            score += 2
                except Exception:
                    pass
                # Spor donanım veya özel modeller
                if any(x in car["model"].lower() or x in "".join(car["features"]).lower() for x in ["sport", "m sport", "cupra", "gt"]):
                    score += 2

            # 3. Konfor & Premium Hissiyat
            if any(x in priorities_lower for x in ["konfor", "rahat", "sessiz", "kalite", "premium", "prestij"]):
                if car["brand"] in ["BMW", "Mercedes-Benz", "Volvo", "Audi", "Tesla"]:
                    score += 3
                if any(x in "".join(car["pros"]).lower() or x in car["description"].lower() for x in ["sessiz", "konfor", "premium", "kalite", "luks"]):
                    score += 2
                    
            # 4. Geniş Aile & Bagaj Hacmi
            if any(x in priorities_lower for x in ["aile", "genis", "bagaj", "cocuk"]):
                if car["body_type"] == "SUV":
                    score += 2
                if car["segment"] in ["C-SUV", "D-SUV", "D"]:
                    score += 2
                if any(x in "".join(car["features"]).lower() or x in "".join(car["pros"]).lower() for x in ["bagaj", "genis", "7 koltuk", "hacim"]):
                    score += 3
                    
            # 5. Teknoloji & Akıllı Ekranlar
            if any(x in priorities_lower for x in ["teknoloji", "ekran", "akilli", "yazilim"]):
                if car["fuel_type"] == "Elektrik" or car["brand"] in ["Tesla", "TOGG"]:
                    score += 3
                if any(x in "".join(car["features"]).lower() for x in ["ekran", "otopilot", "multimedya", "truemore"]):
                    score += 2

        car_copy = car.copy()
        car_copy["score"] = score
        filtered.append(car_copy)
        
    # Puanı yüksek olanları en başa getir
    filtered.sort(key=lambda x: x["score"], reverse=True)
    return filtered

# Yenilenmiş, Sıfırdan Kodlanmış Yerel Yapay Zeka Motoru (Çevrimdışı ve Hızlı Fallback Modu)
def get_local_response(user_message: str) -> str:
    msg_normalized = normalize_text(user_message)
    
    # 1. KULLANICININ BELİRTTİĞİ ARAÇLARIN DİNAMİK OLARAK TESPİT EDİLMESİ
    matched_cars = []
    
    for car in CAR_DATABASE:
        brand_norm = normalize_text(car["brand"])
        model_norm = normalize_text(car["model"])
        
        # Sadeleştirilmiş model ismi (örneğin "Yaris Cross Hybrid" -> "yaris")
        clean_model = model_norm
        for word in ["sedan", "hybrid", "eco", "cross", "pro", "sportback", "stepway", "electric"]:
            clean_model = clean_model.replace(word, "")
        clean_model = clean_model.strip()
        
        # Arama kelimeleri varyasyonları
        keywords = [
            f"{brand_norm} {model_norm}",
            model_norm,
            f"{brand_norm} {clean_model}",
            clean_model
        ]
        # Kısa kelimeleri temizleyelim (örneğin "c" segmenti karışmasın diye 2 harften büyük olmalı)
        keywords = [kw for kw in keywords if len(kw) > 2]
        
        if any(kw in msg_normalized for kw in keywords):
            if car not in matched_cars:
                matched_cars.append(car)

    # Eğer marka bazında arama yapıldıysa ama spesifik model bulunamadıysa markaları eşleştir
    if not matched_cars:
        brands = list(set(normalize_text(car["brand"]) for car in CAR_DATABASE))
        matched_brands = [b for b in brands if b in msg_normalized]
        if matched_brands:
            for car in CAR_DATABASE:
                if normalize_text(car["brand"]) in matched_brands:
                    matched_cars.append(car)

    # 2. BULUNAN ARAÇLARIN SAYISINA GÖRE ANLAMLI YANITLAR ÜRETİLMESİ
    
    # TEK BİR ARAÇ EŞLEŞTİYSE: Detaylı Analiz Kartı ve Bilgisi
    if len(matched_cars) == 1:
        car = matched_cars[0]
        response_text = (
            f"Sorduğunuz **{car['brand']} {car['model']}** modelinin detaylı yerel analizi aşağıdadır:\n\n"
            f"🚗 **Kasa ve Sınıf**: {car['body_type']} ({car['segment']} Segmenti) | {car['transmission']} Şanzıman\n"
            f"🔌 **Motor ve Tüketim**: {car['power']} güç üreten {car['fuel_type']} motor. Ortalama Tüketim: **{car['consumption']}**\n"
            f"💰 **Yaklaşık Pazar Fiyatı**: **{car['price']:,} TL**\n\n"
            f"📝 **Özet Tanıtım**: {car['description']}\n\n"
            f"✅ **Artıları (Öne Çıkan Avantajlar)**:\n"
            + "\n".join([f"- {pro}" for pro in car["pros"]]) + "\n\n"
            f"❌ **Eksileri (Kullanıcı Şikayetleri/Dezavantajlar)**:\n"
            + "\n".join([f"- {con}" for con in car["cons"]]) + "\n\n"
            f"🌟 **Önemli Donanımlar**: {', '.join(car['features'])}\n\n"
            f"Dilerseniz bu aracı sol taraftaki listeden karşılaştırma havuzuna ekleyebilirsiniz!"
        )
        return response_text

    # BİRDEN ÇOK ARAÇ (2 VEYA 3 ARAÇ) EŞLEŞTİYSE: Yan Yana Tablosal Karşılaştırma Algoritması
    elif 1 < len(matched_cars) <= 3:
        cars = matched_cars
        response_text = f"Sorduğunuz **{', '.join([c['brand'] + ' ' + c['model'] for c in cars])}** modellerini sizin için karşılaştırdım:\n\n"
        
        # Dinamik Markdown Tablosu Oluşturma
        response_text += "| Teknik Özellik | " + " | ".join([f"**{c['brand']} {c['model']}**" for c in cars]) + " |\n"
        response_text += "| :--- | " + " | ".join([":---" for _ in cars]) + " |\n"
        
        response_text += f"| **Fiyat (TL)** | " + " | ".join([f"{c['price']:,} TL" for c in cars]) + " |\n"
        response_text += f"| **Kasa Tipi / Segment** | " + " | ".join([f"{c['body_type']} / {c['segment']}" for c in cars]) + " |\n"
        response_text += f"| **Yakıt / Şanzıman** | " + " | ".join([f"{c['fuel_type']} / {c['transmission']}" for c in cars]) + " |\n"
        response_text += f"| **Motor Gücü** | " + " | ".join([c['power'] for c in cars]) + " |\n"
        response_text += f"| **Tüketim** | " + " | ".join([c['consumption'] for c in cars]) + " |\n"
        response_text += f"| **En Büyük Artısı** | " + " | ".join([c['pros'][0] for c in cars]) + " |\n"
        response_text += f"| **En Belirgin Eksisi** | " + " | ".join([c['cons'][0] for c in cars]) + " |\n"
        
        response_text += "\n📊 **Akıllı Karşılaştırma Analizi**:\n"
        
        # En ucuz olanı belirle
        cheapest = min(cars, key=lambda x: x["price"])
        response_text += f"- **Bütçe Analizi**: En uygun fiyatlı seçenek yaklaşık **{cheapest['price']:,} TL** fiyatıyla **{cheapest['brand']} {cheapest['model']}**.\n"
        
        # En güçlü olanı belirle
        try:
            powers = []
            for c in cars:
                p_match = re.search(r'\d+', c["power"])
                powers.append((c, int(p_match.group()) if p_match else 0))
            most_powerful = max(powers, key=lambda x: x[1])[0]
            response_text += f"- **Performans Analizi**: En yüksek motor gücünü sunan model: **{most_powerful['brand']} {most_powerful['model']}** ({most_powerful['power']}).\n"
        except Exception:
            pass
            
        # En az yakanı belirle
        try:
            econ_list = []
            for c in cars:
                if "kwh" in c["consumption"].lower():
                    # Elektrikli araç tüketimini kabaca 3 L/100km'ye eşdeğer sayalım ekonomi puanında
                    val = 3.0
                else:
                    c_match = re.search(r'[\d\.]+', c["consumption"].replace(',', '.'))
                    val = float(c_match.group()) if c_match else 99.0
                econ_list.append((c, val))
            most_econ = min(econ_list, key=lambda x: x[1])[0]
            response_text += f"- **Yakıt Analizi**: Şehir içi ve karma kullanımda en tasarruflu araç: **{most_econ['brand']} {most_econ['model']}** (Ortalama: {most_econ['consumption']}).\n"
        except Exception:
            pass
            
        return response_text

    # ÇOK FAZLA ARAÇ EŞLEŞTİYSE: Seçenekleri listele ve daraltma iste
    elif len(matched_cars) > 3:
        response_text = f"Sorduğunuz kelimeyle eşleşen **{len(matched_cars)} adet** araç buldum. Karşılaştırma tablosu yapabilmem için lütfen aralarından en fazla 3 tanesini seçer misiniz?\n\n"
        for i, car in enumerate(matched_cars[:8], 1):
            response_text += f"{i}. **{car['brand']} {car['model']}** ({car['price']:,} TL - {car['fuel_type']})\n"
        if len(matched_cars) > 8:
            response_text += f"... ve {len(matched_cars) - 8} model daha var.\n"
        return response_text

    # 3. YEREL DOĞAL DİL KRİTER FİLTRELEME VE PUANLAMA MOTORU
    # Eğer direkt marka/model adı bulunamadıysa kullanıcının isteklerini analiz et
    budget = None
    # Düzenli ifadelerle bütçe tespiti (Örn: "1.5 milyon", "900 bin", "850000 tl", "1.200.000 TL")
    budget_match = re.search(r'(\d+[\d\s\.]*)\s*(?:tl|bin|milyon|lira)', msg_normalized)
    if budget_match:
        budget_str = re.sub(r'[\s\.]', '', budget_match.group(1))
        try:
            val = int(budget_str)
            if "milyon" in msg_normalized:
                # 1.5 gibi küsuratlı milyon durumları için
                float_val = float(budget_match.group(1).replace(',', '.').strip())
                budget = int(float_val * 1000000)
            elif val < 50:  # 1.5, 2 vb. milyon kısaltmaları
                budget = int(val * 1000000)
            elif val < 5000:  # 800, 1200 gibi bin kısaltmaları
                budget = val * 1000
            else:
                budget = val
        except ValueError:
            pass

    # Kasa Tipi Tespiti
    body_type = None
    if any(x in msg_normalized for x in ["suv", "arazi", "crossover", "jeep"]):
        body_type = "SUV"
    elif any(x in msg_normalized for x in ["sedan", "aile arabasi", "uc kutulu"]):
        body_type = "Sedan"
    elif any(x in msg_normalized for x in ["hatchback", "hb", "kucuk araba", "sehir ici arabasi"]):
        body_type = "Hatchback"

    # Yakıt Tipi Tespiti
    fuel_type = None
    if any(x in msg_normalized for x in ["elektrik", "pilli", "sarjli", "togg", "ev"]):
        fuel_type = "Elektrik"
    elif any(x in msg_normalized for x in ["hibrit", "hybrid", "yarim elektrik"]):
        fuel_type = "Hibrit"
    elif any(x in msg_normalized for x in ["dizel", "mazot", "motorin"]):
        fuel_type = "Dizel"
    elif any(x in msg_normalized for x in ["lpg", "gaz", "tuplu"]):
        fuel_type = "LPG / Benzin"
    elif any(x in msg_normalized for x in ["benzin", "kursunsuz"]):
        fuel_type = "Benzin"

    # Şanzıman Tespiti
    transmission = None
    if any(x in msg_normalized for x in ["otomatik", "vites yok", "otomatik vites"]):
        transmission = "Otomatik"
    elif any(x in msg_normalized for x in ["manuel", "duz vites", "vitesli"]):
        transmission = "Manuel"

    # Öncelik Tespiti
    priorities = []
    if any(x in msg_normalized for x in ["yakit", "tasarruf", "ekonomi", "ucuz", "az yakan", "fiyat"]):
        priorities.append("ekonomi")
    if any(x in msg_normalized for x in ["hiz", "performans", "seri", "guc", "beygir", "basmak", "tork"]):
        priorities.append("performans")
    if any(x in msg_normalized for x in ["konfor", "rahat", "sessiz", "yapit", "suspansiyon", "luks", "kalite"]):
        priorities.append("konfor")
    if any(x in msg_normalized for x in ["aile", "genis", "bagaj", "cocuk", "piknik", "tatil"]):
        priorities.append("aile")
    if any(x in msg_normalized for x in ["teknoloji", "ekran", "akilli", "yazilim", "multimedya"]):
        priorities.append("teknoloji")

    # Filtreleri Çalıştır
    recommendations = filter_cars(
        budget=budget, 
        body_types=body_type, 
        fuel_types=fuel_type, 
        transmissions=transmission,
        priorities=priorities
    )
    
    # Kullanıcı kriter girdiyse önerileri sun
    has_criteria = any([budget, body_type, fuel_type, transmission, priorities])
    if recommendations and has_criteria:
        top_cars = recommendations[:3]
        response_text = "Seçtiğiniz kriterlere en uygun yerel veritabanı önerilerim aşağıdadır:\n\n"
        for i, car in enumerate(top_cars, 1):
            response_text += f"{i}. **{car['brand']} {car['model']}** ({car['body_type']} - {car['segment']} Segment)\n"
            response_text += f"   - 💰 **Fiyat**: {car['price']:,} TL | 🔌 **Motor**: {car['power']} ({car['fuel_type']})\n"
            response_text += f"   - 📝 **Neden Seçildi?**: {car['description']}\n"
            response_text += f"   - 👍 **En Büyük Avantajı**: {car['pros'][0]}\n\n"
        response_text += "Daha fazla model görmek veya filtreleri daraltmak için bütçe, kasa tipi veya şanzıman tercihinizi değiştirebilirsiniz."
        return response_text

    # Standart ve Yardımcı Diyaloglar
    if any(x in msg_normalized for x in ["merhaba", "selam", "gunaydin", "iyi gunler"]):
        return "Merhaba! Ben yapay zeka destekli Otomobil Danışmanınızım. 50 araçlık yerel veritabanım üzerinden size en uygun aracı bulabilir, modelleri karşılaştırabilir ve bütçe/performans tavsiyesi verebilirim. Nasıl bir araç bakıyorsunuz?"
    
    elif any(x in msg_normalized for x in ["nasil calisir", "yardim", "ne yapabilirsin"]):
        return (
            "Bana şu konularda sorular sorabilirsiniz:\n"
            "- **Bütçe Odaklı**: '1.5 milyon TL bütçem var ne alabilirim?'\n"
            "- **Kasa & Amaç**: 'Geniş bagajlı aile SUV modelleri hangileri?'\n"
            "- **Teknik & Yakıt**: 'Düşük yakıtlı otomatik arabalar hangileri?'\n"
            "- **Karşılaştırma**: 'TOGG T10X ile Tesla Model Y karşılaştırır mısın?' veya 'Megane mı Corolla mı?'\n"
            "- **Detay Öğrenme**: 'Volvo EX30'un artıları ve eksileri nelerdir?'"
        )
        
    else:
        return (
            "Aradığınız kritere uygun bir eşleşme bulamadım. Ancak 50 araçlık veritabanımda arama yapabilmem için bana "
            "bütçenizden (örn: '1.2 milyon TL'), kasa tercihinizden (Sedan, Hatchback, SUV) veya yakıt tipinden (Hibrit, Elektrik, Dizel) "
            "bahsedebilirsiniz."
        )

# Gemini API anahtarı yükleme yardımı
def load_env():
    base_dir = os.path.dirname(__file__)
    env_path = os.path.join(base_dir, ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        os.environ[key.strip()] = val.strip()
        except Exception as e:
            try:
                print(f".env dosyası okunurken hata oluştu: {repr(e)}")
            except Exception:
                pass

# Proje başlarken .env dosyasını otomatik oku
load_env()

# Ana API endpoint'inin çağırdığı AI yönlendirici fonksiyonu
def get_ai_response(user_message: str, chat_history: list = None, api_key: str = None) -> str:
    active_key = api_key or os.environ.get("GEMINI_API_KEY")
    api_error = None
    
    if active_key:
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=active_key)
            
            # Sistem talimatı
            system_instruction = (
                "Sen uzman bir otomobil danışmanısın. Kullanıcıların bütçelerine, tercihlerine ve "
                "ihtiyaçlarına göre araba seçmelerine yardımcı oluyorsun. "
                "Cevaplarını Türkçe ver. Samimi, bilgilendirici, tarafsız ve profesyonel ol. "
                "Gerektiğinde araçların avantajlarından (artıları) ve dezavantajlarından (eksilerinden) bahset. "
                "Sana yardımcı olması için şu zenginleştirilmiş yerel otomobil veritabanına erişimin var:\n\n"
                f"{str(CAR_DATABASE)}\n\n"
                "Kullanıcıya önerilerde bulunurken bu veritabanındaki 50 aracı öncelikle öner, "
                "ancak veritabanında olmayan ama Türkiye pazarında satılan diğer popüler araçlardan da bahsedebilirsin. "
                "Eğer kullanıcı veritabanındaki bir aracı sorarsa, onun teknik verilerini (tüketim, motor gücü, "
                "artıları/eksileri) tam olarak yansıt ve Markdown biçiminde yanıt oluştur."
            )
            
            contents = []
            if chat_history:
                for msg in chat_history:
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append(types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg["content"])]
                    ))
            
            contents.append(types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_message)]
            ))
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7
                )
            )
            return response.text
        except Exception as e:
            try:
                print(f"Gemini API hatası oluştu, yerel yapay zeka motoruna dönülüyor: {repr(e)}")
            except Exception:
                pass
            api_error = repr(e)
            
    # Eğer API anahtarı yoksa veya hata oluştuysa yenilenen Yerel Yapay Zeka Motorunu çalıştır
    response_text = get_local_response(user_message)
    
    if api_error:
        error_msg = "Girdiğiniz API anahtarı çalışmadı."
        if "429" in api_error or "RESOURCE_EXHAUSTED" in api_error:
            error_msg = "API anahtarınızın ücretsiz kotası dolmuş (429 Rate Limit)."
        elif "API_KEY_INVALID" in api_error or "invalid" in api_error.lower():
            error_msg = "Girdiğiniz API anahtarı geçersiz."
            
        warning = f"\n\n*(⚠️ Uyarı: {error_msg} Bu nedenle geçici olarak Yerel Mod veritabanı yanıtı gösterilmektedir.)*"
        response_text += warning
        
    return response_text
