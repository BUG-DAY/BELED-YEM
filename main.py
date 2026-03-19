from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datetime

app = FastAPI()

sehir_detaylari = {
    "Adana": {"duraklar": ["🚌 154 Hattı - 2 dk", "🚌 172 Hattı - Yakın", "🚌 İtimat 1 - 15 dk"], "koordinat": [36.9914, 35.3308], "zoom": 13},
    "İstanbul": {"duraklar": ["🚇 Metrobüs - 1 dk", "🚢 Vapur - Kalkıyor", "🚌 500T - Durakta"], "koordinat": [41.0082, 28.9784], "zoom": 11},
    "Ankara": {"duraklar": ["🚇 Ankaray - 3 dk", "🚌 EGO 413 - 12 dk"], "koordinat": [39.9334, 32.8597], "zoom": 12}
}

@app.get("/", response_class=HTMLResponse)
async def read_root(sehir: str = "Adana"):
    simdi = datetime.datetime.now().strftime("%H:%M:%S")
    detay = sehir_detaylari.get(sehir, sehir_detaylari["Adana"])
    otobus_listesi_html = "".join([f"<li>{hat}</li>" for hat in detay["duraklar"]])
    lat, lon, zoom = detay["koordinat"][0], detay["koordinat"][1], detay["zoom"]

    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Belediyem Terminal 🛸</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            * {{ box-sizing: border-box; }}
            body {{ background: #0f172a; color: white; font-family: sans-serif; margin: 0; padding: 10px; }}
            
            /* ÜST TV REKLAM BANDI */
            .tv-ads {{ background: #000; border: 2px solid #334155; padding: 10px; border-radius: 10px; overflow: hidden; margin-bottom: 10px; }}
            .scrolling-text {{ color: #fbbf24; white-space: nowrap; animation: scroll 15s linear infinite; font-weight: bold; }}
            
            /* ANA YAPI */
            .layout {{ display: flex; flex-direction: column; gap: 10px; }}
            
            /* AYARLAR VE SAAT (SOL PANEL) */
            .settings {{ background: rgba(30,41,59,0.8); padding: 15px; border-radius: 15px; border: 1px solid #334155; }}
            
            /* HARİTA (ORTA) */
            #map {{ height: 250px; width: 100%; border-radius: 15px; border: 2px solid #fbbf24; }}
            
            /* DURAK LİSTESİ (SAĞ) */
            .station {{ background: #1e293b; padding: 15px; border-radius: 15px; }}
            ul {{ list-style: none; padding: 0; }}
            li {{ background: #fff; color: #1e3a8a; padding: 12px; margin-bottom: 5px; border-radius: 8px; font-weight: bold; }}

            /* XOX OYUNU */
            .xox-container {{ background: #1e293b; padding: 15px; border-radius: 15px; text-align: center; border: 1px dashed #fbbf24; }}
            .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; width: 150px; margin: 10px auto; }}
            .cell {{ width: 45px; height: 45px; background: #334155; display: flex; align-items: center; justify-content: center; font-size: 20px; cursor: pointer; border-radius: 5px; font-weight: bold; }}

            select, button {{ width: 100%; padding: 12px; border-radius: 8px; border: none; background: #fbbf24; font-weight: bold; margin-top: 5px; }}
            @keyframes scroll {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>
        <div class="tv-ads"><div class="scrolling-text">📢 REKLAM: Adana'nın En İyi Şalgamı Yüreğir Terminali'nde! | Akıllı Durak Sistemi Devrede...</div></div>

        <div class="layout">
            <div class="settings">
                <h3 style="margin:0; color:#fbbf24;">⚙️ AYARLAR</h3>
                <select onchange="location.href='/?sehir=' + this.value">
                    <option value="Adana" {"selected" if sehir=="Adana" else ""}>Adana</option>
                    <option value="İstanbul" {"selected" if sehir=="İstanbul" else ""}>İstanbul</option>
                    <option value="Ankara" {"selected" if sehir=="Ankara" else ""}>Ankara</option>
                </select>
                <div style="text-align:center; font-size:1.5rem; margin-top:10px; color:#fbbf24;" id="clock">{simdi}</div>
            </div>

            <div id="map"></div>

            <div class="station">
                <h3 style="margin:0; color:#fbbf24;">⏳ DURAK</h3>
                <ul>{otobus_listesi_html}</ul>
            </div>

            <div class="xox-container">
                <h3 style="margin:0; color:#fbbf24;">🎮 OTOBÜS BEKLERKEN OYNA</h3>
                <div class="grid" id="grid">
                    <div class="cell" onclick="play(0)"></div><div class="cell" onclick="play(1)"></div><div class="cell" onclick="play(2)"></div>
                    <div class="cell" onclick="play(3)"></div><div class="cell" onclick="play(4)"></div><div class="cell" onclick="play(5)"></div>
                    <div class="cell" onclick="play(6)"></div><div class="cell" onclick="play(7)"></div><div class="cell" onclick="play(8)"></div>
                </div>
                <button onclick="resetGame()">Yeniden Başlat</button>
            </div>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            setInterval(() => {{ document.getElementById('clock').textContent = new Date().toLocaleTimeString('tr-TR'); }}, 1000);
            var map = L.map('map').setView([{lat}, {lon}], {zoom});
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
            L.marker([{lat}, {lon}]).addTo(map).bindPopup("<b>{sehir} Terminali</b>").openPopup();

            // XOX OYUN MANTIĞI
            let board = ["","","","","","","","",""];
            let currentPlayer = "X";
            function play(i) {{
                if (board[i] === "") {{
                    board[i] = currentPlayer;
                    document.getElementsByClassName('cell')[i].innerText = currentPlayer;
                    currentPlayer = currentPlayer === "X" ? "O" : "X";
                }}
            }}
            function resetGame() {{
                board = ["","","","","","","","",""];
                Array.from(document.getElementsByClassName('cell')).forEach(c => c.innerText = "");
                currentPlayer = "X";
            }}
        </script>
    </body>
    </html>
    """
