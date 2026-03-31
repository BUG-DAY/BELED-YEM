from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datetime

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root(sehir: str = "Adana"):
    simdi = datetime.datetime.now().strftime("%H:%M")
    
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Belediyem Live & Game 🛸</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{ --tr-mavi: #1e3a8a; --tr-altin: #c5a059; --tr-kirmizi: #e11d48; }}
            * {{ box-sizing: border-box; font-family: 'Inter', sans-serif; }}
            
            body {{ 
                margin: 0; height: 100vh; display: flex; align-items: center; justify-content: center;
                background: #f1f5f9; background-image: url('https://www.transparenttextures.com/patterns/az-subtle.png');
            }}

            .terminal-square {{
                width: 95vw; height: 95vw; max-width: 500px; max-height: 500px;
                background: white; border-radius: 40px; overflow: hidden;
                position: relative; display: flex; flex-direction: column;
                box-shadow: 0 30px 60px rgba(0,0,0,0.2); border: 4px solid var(--tr-mavi);
            }}

            .tv-strip {{ background: #000; padding: 10px; border-bottom: 3px solid var(--tr-altin); z-index: 100; }}
            .scroll {{ color: var(--tr-kirmizi); font-weight: 900; white-space: nowrap; animation: scroll 12s linear infinite; font-family: monospace; font-size: 13px; }}

            .content {{ flex: 1; position: relative; display: flex; }}
            #map {{ flex: 1; z-index: 1; }}

            .left-dock {{
                position: absolute; left: 0; top: 0; bottom: 0; width: 45px;
                background: rgba(30, 58, 138, 0.9); backdrop-filter: blur(8px);
                z-index: 100; display: flex; flex-direction: column; align-items: center; gap: 25px; padding-top: 20px;
                transition: width 0.3s; overflow: hidden;
            }}
            .left-dock:hover {{ width: 120px; }}
            .icon {{ color: white; font-size: 22px; cursor: pointer; display: flex; align-items: center; gap: 10px; }}
            .label {{ display: none; font-size: 10px; font-weight: bold; }}
            .left-dock:hover .label {{ display: block; }}

            #game-modal {{
                display: none; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                width: 200px; background: white; padding: 15px; border-radius: 20px; 
                box-shadow: 0 10px 40px rgba(0,0,0,0.5); z-index: 2000; border: 3px solid var(--tr-mavi);
            }}
            .xox-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; margin-top: 10px; }}
            .cell {{ width: 50px; height: 50px; background: #eee; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: 900; cursor: pointer; }}

            .footer-bar {{ background: white; padding: 8px; text-align: center; border-top: 1.5px solid #eee; }}
            .clock {{ font-size: 18px; font-weight: 900; color: var(--tr-mavi); }}

            @keyframes scroll {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        </style>
    </head>
    <body>
        <div class="terminal-square">
            <div class="tv-strip">
                <div class="scroll">🚀 MEHMET TAHİR TERMİNAL: OTOBÜSLER YOLA ÇIKTI | XOX TURNUVASI BAŞLADI...</div>
            </div>
            <div class="content">
                <div class="left-dock">
                    <div class="icon" onclick="toggleGame()">🎮 <span class="label">XOX OYNA</span></div>
                </div>
                <div id="map"></div>
                <div id="game-modal">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:12px; font-weight:bold;">XOX MOLA</span>
                        <span onclick="toggleGame()" style="cursor:pointer;">✖️</span>
                    </div>
                    <div class="xox-grid" id="board">
                        <div class="cell" onclick="play(0)"></div><div class="cell" onclick="play(1)"></div><div class="cell" onclick="play(2)"></div>
                        <div class="cell" onclick="play(3)"></div><div class="cell" onclick="play(4)"></div><div class="cell" onclick="play(5)"></div>
                        <div class="cell" onclick="play(6)"></div><div class="cell" onclick="play(7)"></div><div class="cell" onclick="play(8)"></div>
                    </div>
                    <button onclick="resetGame()" style="width:100%; margin-top:10px; border-radius:10px; border:none; background:var(--tr-mavi); color:white; padding:5px; font-size:10px;">YENİLE</button>
                </div>
            </div>
            <div class="footer-bar">
                <div class="clock" id="clock">{simdi}</div>
            </div>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            setInterval(() => {{ document.getElementById('clock').textContent = new Date().toLocaleTimeString('tr-TR', {{hour:'2-digit', minute:'2-digit'}}); }}, 1000);

            var map = L.map('map', {{zoomControl: false}}).setView([36.9914, 35.3308], 14);
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);

            var busIcon = L.divIcon({{
                html: '<div style="background: #1e3a8a; border: 2px solid white; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items:center; justify-content:center; color:white; font-size:12px;">🚌</div>',
                className: 'dummy-bus'
            }});
            var busMarker = L.marker([36.9914, 35.3308], {{icon: busIcon}}).addTo(map);

            let angle = 0;
            setInterval(() => {{
                angle += 0.005;
                let newLat = 36.9914 + Math.sin(angle) * 0.005;
                let newLon = 35.3308 + Math.cos(angle) * 0.005;
                busMarker.setLatLng([newLat, newLon]);
            }}, 100);

            function toggleGame() {{
                const modal = document.getElementById('game-modal');
                modal.style.display = (modal.style.display === 'block') ? 'none' : 'block';
            }}

            let currentPlayer = "X";
            let gameState = ["", "", "", "", "", "", "", "", ""];
            function play(idx) {{
                if (gameState[idx] === "") {{
                    gameState[idx] = currentPlayer;
                    document.getElementById('board').children[idx].innerText = currentPlayer;
                    currentPlayer = (currentPlayer === "X") ? "O" : "X";
                }}
            }}
            function resetGame() {{
                gameState = ["", "", "", "", "", "", "", "", ""];
                Array.from(document.getElementById('board').children).forEach(c => c.innerText = "");
                currentPlayer = "X";
            }}
        </script>
    </body>
    </html>
    """
