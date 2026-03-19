from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Belediyem Ulaşım Sistemi 🛸</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background: #121212; color: white; }
            header { background: #1f1f1f; padding: 20px; text-align: center; border-bottom: 3px solid #00ffcc; shadow: 0 4px 10px rgba(0,0,0,0.5); }
            #map { height: 500px; width: 90%; margin: 20px auto; border-radius: 15px; border: 2px solid #333; }
            .container { padding: 20px; text-align: center; }
            .info-card { background: #1e1e1e; padding: 15px; border-radius: 10px; display: inline-block; margin: 10px; border-left: 5px solid #00ffcc; }
            footer { text-align: center; padding: 20px; font-size: 0.8em; color: #666; }
            h1 { margin: 0; color: #00ffcc; text-transform: uppercase; letter-spacing: 2px; }
        </style>
    </head>
    <body>
        <header>
            <h1>Belediyem Akıllı Ulaşım 🛸</h1>
            <p>Canlı Durak ve Hat Takip Sistemi v1.0</p>
        </header>

        <div class="container">
            <div class="info-card"><strong>Aktif Hat Sayısı:</strong> 12</div>
            <div class="info-card"><strong>Çevrimiçi Otobüs:</strong> 45</div>
            <div class="info-card"><strong>Sistem Durumu:</strong> Stabil ✅</div>
        </div>

        <div id="map"></div>

        <div class="container">
            <h3>Durak Listesi ve Tahmini Varış</h3>
            <p>Harita üzerinden duraklara tıklayarak detaylı bilgi alabilirsiniz.</p>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            // Haritayı başlat (Örnek olarak Ankara/İstanbul civarı bir koordinat)
            var map = L.map('map').setView([39.9334, 32.8597], 12);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap'
            }).addTo(map);

            // Örnek Duraklar
            var duraklar = [
                {ad: "Merkez Durak", koordinat: [39.9334, 32.8597], info: "Gelen Otobüs: Hat 102 (2 dk)"},
                {ad: "Üniversite Meydanı", koordinat: [39.9450, 32.8650], info: "Gelen Otobüs: Hat 205 (5 dk)"},
                {ad: "Belediye Sarayı", koordinat: [39.9200, 32.8500], info: "Gelen Otobüs: Hat 301 (Yolda)"}
            ];

            duraklar.forEach(function(durak) {
                L.marker(durak.koordinat).addTo(map)
                    .bindPopup("<b>" + durak.ad + "</b><br>" + durak.info);
            });
        </script>

        <footer>
            © 2026 BELED-YEM Sistemleri | Mehmet Tahir Projesi
        </footer>
    </body>
    </html>
    """
