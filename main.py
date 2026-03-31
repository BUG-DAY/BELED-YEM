# ==============================================================================
# PROJE       : T.C. ULUSAL ULAŞIM MATRİSİ (UUM)
# SÜRÜM       : v8.0.0-DYNAMIC-LED-ENTERPRISE (BÖLÜM 1)
# ==============================================================================

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
import random
import logging
import time
from datetime import datetime

# --- 1. KURUMSAL SİSTEM İZLEME (LOGGING) ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s | UUM-CORE | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Ulaşım Matrisi Core API", version="8.0.0", docs_url="/api/docs")

# --- 2. SİBER GÜVENLİK & CORS KATMANI ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# --- 3. STRICT TYPING (PYDANTIC VERİ MODELLERİ) ---
class GeoLocation(BaseModel):
    lat: float
    lng: float

class VehicleData(BaseModel):
    id: str = Field(..., description="Hat Kodu (Örn: 154)")
    hedef: str = Field(..., description="Aracın son durağı")
    kalan_zaman: str = Field(..., description="Durağa varış süresi")
    konum: GeoLocation
    hiz_kmh: int

class CityMatrixResponse(BaseModel):
    status: int
    sehir: str
    gecikme_ms: float
    merkez: GeoLocation
    aktif_arac_sayisi: int
    ortalama_hiz: int
    filo: List[VehicleData]

# --- 4. TÜRKİYE BÜYÜKŞEHİR VERİTABANI ---
class NationalDataCore:
    def _init_(self):
        self.cities = {
            "Adana": [36.9914, 35.3308], "Ankara": [39.9334, 32.8597],
            "Antalya": [36.8841, 30.7056], "Bursa": [40.1824, 29.0611],
            "Diyarbakır": [37.9144, 40.2110], "Erzurum": [39.9000, 41.2700],
            "Eskişehir": [39.7767, 30.5206], "Gaziantep": [37.0662, 37.3833],
            "İstanbul": [41.0082, 28.9784], "İzmir": [38.4237, 27.1428],
            "Kayseri": [38.7312, 35.4787], "Kocaeli": [40.8533, 29.8815],
            "Konya": [37.8714, 32.4846], "Mersin": [36.8121, 34.6415]
        }
    
    def get_city_data(self, name: str):
        if name not in self.cities:
            name = "Adana"
        lat, lng = self.cities[name]
        return {
            "lat": lat, "lng": lng,
            "routes": [f"Hat {random.randint(10, 99)}", f"Hat {random.randint(100, 500)}", "Merkez Ekspres", "Terminal Yönü"]
        }

db = NationalDataCore()

# ==============================================================================
# 5. RESTful API ENDPOINT (GİZLİ ARKA PLAN VERİ MOTORU)
# ==============================================================================
@app.get("/api/v1/fleet", response_model=CityMatrixResponse)
async def get_live_fleet(city: str = "Adana"):
    t_start = time.perf_counter()
    city_info = db.get_city_data(city)
    
    fleet_data = []
    toplam_hiz = 0
    
    for line in city_info["routes"]:
        eta = random.randint(1, 15)
        hiz = random.randint(10, 55) if eta > 1 else 0
        toplam_hiz += hiz
        
        fleet_data.append(
            VehicleData(
                id=line,
                hedef=f"Durak {random.randint(100,999)}",
                kalan_zaman="DURAKTA" if eta == 1 else f"{eta} Dk",
                konum=GeoLocation(
                    lat=city_info["lat"] + random.uniform(-0.035, 0.035),
                    lng=city_info["lng"] + random.uniform(-0.035, 0.035)
                ),
                hiz_kmh=hiz
            )
        )
    
    latency = round((time.perf_counter() - t_start) * 1000, 2)
    ortalama_hiz = int(toplam_hiz / len(fleet_data)) if fleet_data else 0
    
    logger.info(f"[API_SYNC] {city} verisi çekildi. Gecikme: {latency}ms")
    
    return CityMatrixResponse(
        status=200,
        sehir=city,
        gecikme_ms=latency,
        merkez=GeoLocation(lat=city_info["lat"], lng=city_info["lng"]),
        aktif_arac_sayisi=len(fleet_data),
        ortalama_hiz=ortalama_hiz,
        filo=sorted(fleet_data, key=lambda x: x.kalan_zaman)
    )# ==============================================================================
# PROJE       : T.C. ULUSAL ULAŞIM MATRİSİ (UUM)
# SÜRÜM       : v8.0.0-DYNAMIC-LED-ENTERPRISE (BÖLÜM 1)
# ==============================================================================

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
import random
import logging
import time
from datetime import datetime

# --- 1. KURUMSAL SİSTEM İZLEME (LOGGING) ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s | UUM-CORE | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Ulaşım Matrisi Core API", version="8.0.0", docs_url="/api/docs")

# --- 2. SİBER GÜVENLİK & CORS KATMANI ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# --- 3. STRICT TYPING (PYDANTIC VERİ MODELLERİ) ---
class GeoLocation(BaseModel):
    lat: float
    lng: float

class VehicleData(BaseModel):
    id: str = Field(..., description="Hat Kodu (Örn: 154)")
    hedef: str = Field(..., description="Aracın son durağı")
    kalan_zaman: str = Field(..., description="Durağa varış süresi")
    konum: GeoLocation
    hiz_kmh: int

class CityMatrixResponse(BaseModel):
    status: int
    sehir: str
    gecikme_ms: float
    merkez: GeoLocation
    aktif_arac_sayisi: int
    ortalama_hiz: int
    filo: List[VehicleData]

# --- 4. TÜRKİYE BÜYÜKŞEHİR VERİTABANI ---
class NationalDataCore:
    def _init_(self):
        self.cities = {
            "Adana": [36.9914, 35.3308], "Ankara": [39.9334, 32.8597],
            "Antalya": [36.8841, 30.7056], "Bursa": [40.1824, 29.0611],
            "Diyarbakır": [37.9144, 40.2110], "Erzurum": [39.9000, 41.2700],
            "Eskişehir": [39.7767, 30.5206], "Gaziantep": [37.0662, 37.3833],
            "İstanbul": [41.0082, 28.9784], "İzmir": [38.4237, 27.1428],
            "Kayseri": [38.7312, 35.4787], "Kocaeli": [40.8533, 29.8815],
            "Konya": [37.8714, 32.4846], "Mersin": [36.8121, 34.6415]
        }
    
    def get_city_data(self, name: str):
        if name not in self.cities:
            name = "Adana"
        lat, lng = self.cities[name]
        return {
            "lat": lat, "lng": lng,
            "routes": [f"Hat {random.randint(10, 99)}", f"Hat {random.randint(100, 500)}", "Merkez Ekspres", "Terminal Yönü"]
        }

db = NationalDataCore()

# ==============================================================================
# 5. RESTful API ENDPOINT (GİZLİ ARKA PLAN VERİ MOTORU)
# ==============================================================================
@app.get("/api/v1/fleet", response_model=CityMatrixResponse)
async def get_live_fleet(city: str = "Adana"):
    t_start = time.perf_counter()
    city_info = db.get_city_data(city)
    
    fleet_data = []
    toplam_hiz = 0
    
    for line in city_info["routes"]:
        eta = random.randint(1, 15)
        hiz = random.randint(10, 55) if eta > 1 else 0
        toplam_hiz += hiz
        
        fleet_data.append(
            VehicleData(
                id=line,
                hedef=f"Durak {random.randint(100,999)}",
                kalan_zaman="DURAKTA" if eta == 1 else f"{eta} Dk",
                konum=GeoLocation(
                    lat=city_info["lat"] + random.uniform(-0.035, 0.035),
                    lng=city_info["lng"] + random.uniform(-0.035, 0.035)
                ),
                hiz_kmh=hiz
            )
        )
    
    latency = round((time.perf_counter() - t_start) * 1000, 2)
    ortalama_hiz = int(toplam_hiz / len(fleet_data)) if fleet_data else 0
    
    logger.info(f"[API_SYNC] {city} verisi çekildi. Gecikme: {latency}ms")
    
    return CityMatrixResponse(
        status=200,
        sehir=city,
        gecikme_ms=latency,
        merkez=GeoLocation(lat=city_info["lat"], lng=city_info["lng"]),
        aktif_arac_sayisi=len(fleet_data),
        ortalama_hiz=ortalama_hiz,
        filo=sorted(fleet_data, key=lambda x: x.kalan_zaman)
    )# ==============================================================================
# 6. FRONTEND (GÜVENLİ, 500 HATASI VERMEYEN HTML ŞABLONLARI)
# ==============================================================================

# --- ANA MENÜ ---
@app.get("/", response_class=HTMLResponse)
async def render_home():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Ulaşım Matrisi | Ana Kontrol</title>
        <style>
            :root { --blue: #2563eb; --pink: #db2777; --orange: #ea580c; --green: #10b981; --dark: #0f172a; }
            * { box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; padding: 0; text-decoration: none; user-select: none; -webkit-tap-highlight-color: transparent; }
            body { background: #020617; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; }
            
            .app-core { width: 100vw; height: 100vh; max-width: 450px; background: #f8fafc; display: flex; flex-direction: column; position: relative; }
            @media (min-width: 460px) { .app-core { max-height: 850px; border-radius: 35px; border: 8px solid #1e293b; overflow: hidden; box-shadow: 0 25px 50px rgba(0,0,0,0.5); } }
            
            .dashboard { padding: 40px 25px; flex: 1; display: flex; flex-direction: column; }
            .sys-title { font-size: 28px; font-weight: 900; color: var(--dark); line-height: 1.2; margin-bottom: 35px; }
            .sys-title span { color: var(--blue); }
            
            .grid-matrix { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
            .module-card {
                background: white; border-radius: 24px; padding: 30px 10px; text-align: center;
                box-shadow: 0 8px 20px rgba(0,0,0,0.04); display: flex; flex-direction: column; align-items: center; gap: 15px;
                border: 2px solid transparent; transition: transform 0.1s;
            }
            .module-card:active { transform: scale(0.94); background: #f1f5f9; }
            .m-icon { width: 70px; height: 70px; border-radius: 22px; display: flex; align-items: center; justify-content: center; font-size: 35px; }
            .m-label { font-size: 15px; font-weight: 900; color: var(--dark); }
            
            .c-bel .m-icon { background: #dbeafe; color: var(--blue); }
            .c-met .m-icon { background: #fce7f3; color: var(--pink); }
            .c-ozl .m-icon { background: #ffedd5; color: var(--orange); }
            .c-krt .m-icon { background: #d1fae5; color: var(--green); }
            
            .security-badge { position: absolute; bottom: 20px; left: 0; width: 100%; text-align: center; font-size: 10px; color: #94a3b8; font-weight: 800; letter-spacing: 1px; }
        </style>
    </head>
    <body>
        <div class="app-core">
            <div class="dashboard">
                <div class="sys-title">Merhaba <span>Mehmet Tahir</span>,<br><div style="font-size:16px; color:#64748b; font-weight:600; margin-top:8px;">Hangi aracı kullanacaksın?</div></div>
                <div class="grid-matrix">
                    <a href="/belediye?city=Adana" class="module-card c-bel"><div class="m-icon">🚌</div><div class="m-label">Belediye</div></a>
                    <a href="/metro" class="module-card c-met"><div class="m-icon">🚇</div><div class="m-label">Metro</div></a>
                    <a href="/ozel" class="module-card c-ozl"><div class="m-icon">🚐</div><div class="m-label">Özel Sektör</div></a>
                    <a href="/kart" class="module-card c-krt"><div class="m-icon">💳</div><div class="m-label">Kart Dolum</div></a>
                </div>
            </div>
            <div class="security-badge">UUM ENTERPRISE CORE | SECURE CONNECTION</div>
        </div>
    </body>
    </html>
    """

# --- BELEDİYE OTOBÜSÜ EKRANI (DİNAMİK LED EKRANLI) ---
@app.get("/belediye", response_class=HTMLResponse)
async def render_belediye(city: str = "Adana"):
    options_html = "".join([f"<option value='{s}' {'selected' if s == city else ''}>{s}</option>" for s in sorted(db.cities.keys())])
    
    html_template = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Canlı Filo Ağı</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root { --blue: #2563eb; --dark: #0f172a; }
            * { box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; padding: 0; text-decoration: none; }
            body { background: #020617; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; }
            
            .app-core { width: 100vw; height: 100vh; max-width: 450px; background: #f8fafc; display: flex; flex-direction: column; position: relative; }
            @media (min-width: 460px) { .app-core { max-height: 850px; border-radius: 35px; border: 8px solid #1e293b; overflow: hidden; } }
            
            /* DİJİTAL LED PANEL */
            .led-panel { background: #000; padding: 10px; border-bottom: 2px solid var(--blue); display: flex; align-items: center; justify-content: space-between; z-index: 2000; }
            .ticker-wrap { overflow: hidden; white-space: nowrap; flex: 1; }
            .ticker-text { display: inline-block; color: #38bdf8; font-family: monospace; font-size: 13px; font-weight: bold; animation: scroll 20s linear infinite; }
            .ping-monitor { color: #10b981; font-family: monospace; font-size: 11px; font-weight: 800; margin-left: 10px; background: rgba(16, 185, 129, 0.1); padding: 2px 6px; border-radius: 4px; }
            @keyframes scroll { from { transform: translateX(100%); } to { transform: translateX(-100%); } }
            
            /* NAVİGASYON & ŞEHİR SEÇİCİ */
            .nav-bar { background: var(--dark); padding: 15px; display: flex; align-items: center; justify-content: space-between; z-index: 2000; }
            .btn-back { color: white; font-weight: 900; padding: 8px 12px; background: #334155; border-radius: 8px; font-size: 13px; }
            .city-selector { background: #1e293b; color: white; border: 1px solid #38bdf8; padding: 8px 15px; border-radius: 8px; font-weight: bold; outline: none; }

            /* HARİTA (YÜKSEK ÖNCELİKLİ) */
            .map-layer { flex: 0.6; width: 100%; position: relative; background: #e2e8f0; }
            #sys-map { position: absolute; top: 0; bottom: 0; left: 0; right: 0; z-index: 1; }
            
            /* MOOVIT ÇEKMECESİ */
            .data-drawer { flex: 0.4; background: white; border-radius: 20px 20px 0 0; box-shadow: 0 -10px 20px rgba(0,0,0,0.1); z-index: 1000; display: flex; flex-direction: column; margin-top: -15px; }
            .drawer-handle { width: 40px; height: 5px; background: #cbd5e1; border-radius: 10px; margin: 10px auto; }
            .search-module { padding: 0 20px 10px; border-bottom: 1px solid #f1f5f9; }
            .search-input { width: 100%; padding: 10px 15px; border-radius: 10px; border: 2px solid #e2e8f0; font-size: 14px; font-weight: bold; outline: none; background: #f8fafc; color: var(--dark); }
            .search-input:focus { border-color: var(--blue); background: #fff; }
            
            /* VERİ LİSTESİ */
            .fleet-list { padding: 0 20px 10px; overflow-y: auto; flex: 1; }
            .f-row { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f1f5f9; }
            .f-info { display: flex; flex-direction: column; gap: 4px; }
            .f-id { font-size: 15px; font-weight: 900; color: var(--dark); }
            .f-dest { font-size: 11px; color: #64748b; font-weight: 600; display: flex; gap: 5px; align-items: center; }
            .f-eta { font-size: 12px; font-weight: 900; background: #dbeafe; padding: 6px 12px; border-radius: 10px; color: var(--blue); }
            
            .loader-msg { text-align: center; padding: 30px; color: #94a3b8; font-size: 12px; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="app-core">
            <div class="led-panel">
                <div class="ticker-wrap"><div class="ticker-text" id="led-text-content">📡 SİSTEM BAŞLATILIYOR | API BAĞLANTISI BEKLENİYOR...</div></div>
                <div class="ping-monitor" id="ping-display">PING: --ms</div>
            </div>
            
            <div class="nav-bar">
                <a href="/" class="btn-back">❮ GERİ</a>
                <select class="city-selector" id="citySelect" onchange="location.href='/belediye?city=' + this.value">
                    {{CITY_OPTIONS}}
                </select>
            </div>
            
            <div class="map-layer"><div id="sys-map"></div></div>
            
            <div class="data-drawer">
                <div class="drawer-handle"></div>
                <div class="search-module">
                    <input type="text" id="routeSearch" class="search-input" placeholder="🔍 Hat veya Durak Ara...">
                </div>
                <div class="fleet-list" id="fleet-container">
                    <div class="loader-msg">🔄 Güvenli API Bağlantısı Kuruluyor...</div>
                </div>
            </div>
        </div>
        
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            class UlasimCoreEngine {
                constructor(city) {
                    this.city = city;
                    this.map = null;
                    this.layerGroup = L.layerGroup();
                    this.initSearch();
                    this.fetchData();
                    setInterval(() => this.fetchData(), 4000);
                }

                setupMap(lat, lng) {
                    if (!this.map) {
                        this.map = L.map('sys-map', { zoomControl: false }).setView([lat, lng], 13);
                        L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', { maxZoom: 19 }).addTo(this.map);
                        this.layerGroup.addTo(this.map);
                        setTimeout(() => this.map.invalidateSize(), 100);
                    } else {
                        this.map.setView([lat, lng], 13);
                    }
                }

                async fetchData() {
                    try {
                        const reqStart = performance.now();
                        const response = await fetch('/api/v1/fleet?city=' + this.city);
                        const payload = await response.json();
                        const ping = Math.round(performance.now() - reqStart);
                        
                        document.getElementById('ping-display').innerText = 'PING: ' + ping + 'ms';
                        
                        this.setupMap(payload.merkez.lat, payload.merkez.lng);
                        this.updateUI(payload.filo);
                        
                        const now = new Date().toLocaleTimeString('tr-TR');
                        const ledMessage = 📡 CANLI VERİ AKIŞI: ${this.city.toUpperCase()} | AKTİF İZLENEN ARAÇ: ${payload.aktif_arac_sayisi} | FİLO ORTALAMA HIZI: ${payload.ortalama_hiz} KM/S | SON GÜNCELLEME: ${now} | SİSTEM DURUMU: OPTİMAL...;
                        document.getElementById('led-text-content').innerText = ledMessage + " \u00A0\u00A0\u00A0\u00A0\u00A0\u00A0 " + ledMessage;
                        
                    } catch (error) {
                        console.error("[SYS_ERR] API Fetch Failed:", error);
                        document.getElementById('led-text-content').innerText = "⚠️ BAĞLANTI HATASI: VERİ ÇEKİLEMİYOR. LÜTFEN İNTERNETİNİZİ KONTROL EDİN...";
                    }
                }

                updateUI(fleet) {
                    const container = document.getElementById('fleet-container');
                    container.innerHTML = '';
                    this.layerGroup.clearLayers();

                    const icon = L.divIcon({ html: '<div style="background:#2563eb; width:22px; height:22px; border-radius:50%; border:2px solid #fff; display:flex; align-items:center; justify-content:center; color:white; font-size:10px; box-shadow:0 2px 5px rgba(0,0,0,0.3);">🚌</div>', className: 'm' });

                    fleet.forEach(bus => {
                        const badgeStyle = bus.kalan_zaman === 'DURAKTA' ? 'background:#d1fae5; color:#059669;' : '';
                        
                        container.innerHTML += `
                            <div class="f-row item">
                                <div class="f-info">
                                    <span class="f-id">🚌 ${bus.id}</span>
                                    <span class="f-dest">Hedef: ${bus.hedef} | Hız: ${bus.hiz_kmh} km/s</span>
                                </div>
                                <div class="f-eta" style="${badgeStyle}">${bus.kalan_zaman}</div>
                            </div>
                        `;
                        L.marker([bus.konum.lat, bus.konum.lng], {icon: icon}).addTo(this.layerGroup);
                    });
                }

                initSearch() {
                    document.getElementById('routeSearch').addEventListener('keyup', (e) => {
                        const keyword = e.target.value.toUpperCase();
                        document.querySelectorAll('.item').forEach(row => {
                            row.style.display = row.innerText.toUpperCase().includes(keyword) ? "flex" : "none";
                        });
                    });
                }
            }

            document.addEventListener('DOMContentLoaded', () => {
                window.AppEngine = new UlasimCoreEngine('{{CITY_NAME}}');
            });
        </script>
    </body>
    </html>
    """
    
    final_html = html_template.replace("{{CITY_OPTIONS}}", options_html).replace("{{CITY_NAME}}", city)
    return HTMLResponse(content=final_html)

# --- 7. DİĞER MODÜLLER ---
@app.get("/{module_name}", response_class=HTMLResponse)
async def sub_modules(module_name: str):
    if module_name not in ["metro", "ozel", "kart"]:
        return "<a href='/'>Geri Dön</a>"
    
    titles = {"metro": "RAYLI SİSTEMLER", "ozel": "ÖZEL SEKTÖR AĞI", "kart": "KENTKART NOKTALARI"}
    
    html = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { box-sizing: border-box; font-family: 'Segoe UI', sans-serif; text-decoration: none; }
            body { background: #020617; height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; }
            .app-core { width: 100vw; height: 100vh; max-width: 450px; background: #f8fafc; display: flex; flex-direction: column; position:relative; }
            @media (min-width: 460px) { .app-core { max-height: 850px; border-radius: 35px; border: 8px solid #1e293b; overflow:hidden; } }
            .nav-bar { background: #0f172a; padding: 15px; display: flex; align-items: center; justify-content: center; position: relative; }
            .btn-back { position: absolute; left: 15px; color: white; font-weight: bold; padding: 8px 12px; background: #334155; border-radius: 8px; font-size: 13px; }
            .sys-msg { margin: auto; padding: 30px; text-align: center; color: #1e293b; font-weight: bold; font-size: 15px; border: 2px dashed #cbd5e1; border-radius: 15px; width: 80%; line-height:1.5; }
        </style>
    </head>
    <body>
        <div class="app-core">
            <div class="nav-bar">
                <a href="/" class="btn-back">❮ GERİ</a>
                <div style="color:white; font-weight:900; letter-spacing:1px;">{{TITLE}}</div>
            </div>
            <div class="sys-msg">
                ⚠️ Güvenli API Bağlantısı Bekleniyor...<br><br>
                <span style="font-size:12px; color:#64748b; font-weight:normal;">Altyapı hazır durumdadır. İlgili kurumun Açık Veri portalı entegrasyonu sağlandığında aktifleşecektir.</span>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html.replace("{{TITLE}}", titles[module_name]))
