# ==============================================================================
# PROJE       : T.C. ULUSAL ULAŞIM MATRİSİ (UUM)
# SÜRÜM       : v11.0.0-NATIONAL-INFRASTRUCTURE (BÖLÜM 1)
# MİMARİ      : %100 SPA (Single Page Application) - SIFIR SAYFA YENİLEME
# ÖZELLİK     : 81 İl Koordinatları, Devlet İzni Bekleme Modülü
# ==============================================================================

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random
import time

app = FastAPI(title="UUM National API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

class GeoLocation(BaseModel):
    lat: float
    lng: float

class Vehicle(BaseModel):
    id: str
    hedef: str
    kalan: str
    konum: GeoLocation
    hiz: int

class FleetResponse(BaseModel):
    sehir: str
    durum: str  # "ACTIVE" veya "AWAITING_API"
    gecikme_ms: float
    merkez: GeoLocation
    arac_sayisi: int
    ortalama_hiz: int
    filo: List[Vehicle]

class NationalCore:
    def _init_(self):
        # Pilot Şehirler (Açık Verisi Aktif Olanlar)
        self.active_cities = ["Adana", "Ankara", "İstanbul", "İzmir", "Bursa"]
        
        # Türkiye 81 İl Merkez Koordinatları (Milli Altyapı)
        self.cities = {
            "Adana": [36.99, 35.33], "Adıyaman": [37.76, 38.27], "Afyon": [38.75, 30.55], "Ağrı": [39.71, 43.05],
            "Aksaray": [38.36, 33.99], "Amasya": [40.65, 35.83], "Ankara": [39.93, 32.85], "Antalya": [36.88, 30.70],
            "Ardahan": [41.11, 42.70], "Artvin": [41.18, 41.81], "Aydın": [37.83, 27.84], "Balıkesir": [39.65, 27.89],
            "Bartın": [41.63, 32.33], "Batman": [37.88, 41.13], "Bayburt": [40.26, 40.22], "Bilecik": [40.14, 29.97],
            "Bingöl": [38.88, 40.49], "Bitlis": [38.40, 42.10], "Bolu": [40.73, 31.60], "Burdur": [37.71, 30.28],
            "Bursa": [40.18, 29.06], "Çanakkale": [40.15, 26.41], "Çankırı": [40.60, 33.61], "Çorum": [40.54, 34.95],
            "Denizli": [37.78, 29.09], "Diyarbakır": [37.91, 40.21], "Düzce": [40.83, 31.15], "Edirne": [41.67, 26.55],
            "Elazığ": [38.67, 39.22], "Erzincan": [39.73, 39.48], "Erzurum": [39.90, 41.27], "Eskişehir": [39.77, 30.52],
            "Gaziantep": [37.06, 37.38], "Giresun": [40.91, 38.38], "Gümüşhane": [40.46, 39.48], "Hakkari": [37.57, 43.73],
            "Hatay": [36.20, 36.16], "Iğdır": [39.92, 44.04], "Isparta": [37.76, 30.55], "İstanbul": [41.00, 28.97],
            "İzmir": [38.42, 27.14], "K.Maraş": [37.57, 36.92], "Karabük": [41.19, 32.62], "Karaman": [37.18, 33.22],
            "Kars": [40.60, 43.09], "Kastamonu": [41.37, 33.77], "Kayseri": [38.73, 35.47], "Kırıkkale": [39.83, 33.50],
            "Kırklareli": [41.73, 27.22], "Kırşehir": [39.14, 34.16], "Kilis": [36.71, 37.11], "Kocaeli": [40.85, 29.88],
            "Konya": [37.87, 32.48], "Kütahya": [39.42, 29.98], "Malatya": [38.35, 38.30], "Manisa": [38.61, 27.42],
            "Mardin": [37.31, 40.73], "Mersin": [36.81, 34.64], "Muğla": [37.21, 28.36], "Muş": [38.73, 41.49],
            "Nevşehir": [38.62, 34.71], "Niğde": [37.96, 34.67], "Ordu": [40.98, 37.87], "Osmaniye": [37.07, 36.24],
            "Rize": [41.02, 40.52], "Sakarya": [40.75, 30.37], "Samsun": [41.28, 36.33], "Siirt": [37.92, 41.94],
            "Sinop": [42.02, 35.15], "Sivas": [39.74, 37.01], "Şanlıurfa": [37.15, 38.79], "Şırnak": [37.51, 42.45],
            "Tekirdağ": [40.97, 27.50], "Tokat": [40.32, 36.55], "Trabzon": [41.00, 39.71], "Tunceli": [39.10, 39.54],
            "Uşak": [38.67, 29.40], "Van": [38.48, 43.38], "Yalova": [40.65, 29.26], "Yozgat": [39.82, 34.80], "Zonguldak": [41.45, 31.79]
        }
    
    def get_info(self, name: str):
        if name not in self.cities: name = "Adana"
        status = "ACTIVE" if name in self.active_cities else "AWAITING_API"
        return {"name": name, "lat": self.cities[name][0], "lng": self.cities[name][1], "status": status}

db = NationalCore()

@app.get("/api/v1/cities")
async def get_all_cities():
    return sorted(list(db.cities.keys()))

@app.get("/api/v1/fleet", response_model=FleetResponse)
async def get_fleet(city: str = "Adana"):
    t_start = time.perf_counter()
    info = db.get_info(city)
    latency = round((time.perf_counter() - t_start) * 1000, 2)
    
    if info["status"] == "AWAITING_API":
        return FleetResponse(sehir=info["name"], durum="AWAITING_API", gecikme_ms=latency, merkez=GeoLocation(lat=info["lat"], lng=info["lng"]), arac_sayisi=0, ortalama_hiz=0, filo=[])
    
    fleet = []
    tot_spd = 0
    routes = [f"Hat {random.randint(10,99)}", f"Hat {random.randint(100,500)}", "Ekspres Hat", "Ring"]
    for r in routes:
        eta = random.randint(1, 15)
        spd = random.randint(10, 55) if eta > 1 else 0
        tot_spd += spd
        fleet.append(Vehicle(id=r, hedef=f"Durak {random.randint(100,999)}", kalan="DURAKTA" if eta == 1 else f"{eta} Dk", konum=GeoLocation(lat=info["lat"] + random.uniform(-0.03, 0.03), lng=info["lng"] + random.uniform(-0.03, 0.03)), hiz=spd))
        
    return FleetResponse(sehir=info["name"], durum="ACTIVE", gecikme_ms=latency, merkez=GeoLocation(lat=info["lat"], lng=info["lng"]), arac_sayisi=len(fleet), ortalama_hiz=int(tot_spd/len(fleet)) if fleet else 0, filo=sorted(fleet, key=lambda x: 0 if x.kalan == "DURAKTA" else int(x.kalan.split()[0])))# ==============================================================================
# ÖN YÜZ (FRONTEND) - SAYFA YENİLEMESİZ JET GİBİ GEÇİŞ MİMARİSİ
# ==============================================================================

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <title>Ulaşım Matrisi</title>
        <style>
            * { box-sizing: border-box; font-family: 'Segoe UI', sans-serif; text-decoration: none; user-select: none; -webkit-tap-highlight-color: transparent; }
            body { background: #020617; height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; }
            .app { width: 100vw; height: 100vh; max-width: 450px; background: #f8fafc; display: flex; flex-direction: column; position: relative; }
            @media (min-width: 460px) { .app { max-height: 850px; border-radius: 35px; border: 8px solid #1e293b; overflow: hidden; box-shadow: 0 25px 50px rgba(0,0,0,0.5); } }
            .dash { padding: 40px 25px; flex: 1; display: flex; flex-direction: column; }
            .title { font-size: 28px; font-weight: 900; color: #0f172a; line-height: 1.2; margin-bottom: 35px; }
            .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
            .card { background: white; border-radius: 24px; padding: 30px 10px; text-align: center; box-shadow: 0 8px 20px rgba(0,0,0,0.04); display: flex; flex-direction: column; align-items: center; gap: 15px; border: 2px solid transparent; transition: 0.1s; }
            .card:active { transform: scale(0.94); background: #f1f5f9; }
            .ic { width: 70px; height: 70px; border-radius: 22px; display: flex; align-items: center; justify-content: center; font-size: 35px; }
            .lb { font-size: 15px; font-weight: 900; color: #0f172a; }
            .badge { position: absolute; bottom: 20px; left: 0; width: 100%; text-align: center; font-size: 10px; color: #94a3b8; font-weight: 800; letter-spacing: 1px; }
        </style>
    </head>
    <body>
        <div class="app">
            <div class="dash">
                <div class="title">Ulaşım Matrisine <span style="color:#2563eb;">Hoş Geldin</span>,<br><div style="font-size:15px; color:#64748b; font-weight:600; margin-top:8px;">Türkiye'nin akıllı ulaşım ağına bağlandın. Bugün rotamız neresi?</div></div>
                <div class="grid">
                    <a href="/belediye" class="card"><div class="ic" style="background:#dbeafe; color:#2563eb;">🚌</div><div class="lb">Belediye</div></a>
                    <a href="/metro" class="card"><div class="ic" style="background:#fce7f3; color:#db2777;">🚇</div><div class="lb">Metro</div></a>
                    <a href="/ozel" class="card"><div class="ic" style="background:#ffedd5; color:#ea580c;">🚐</div><div class="lb">Özel Sektör</div></a>
                    <a href="/kart" class="card"><div class="ic" style="background:#d1fae5; color:#10b981;">💳</div><div class="lb">Kart Dolum</div></a>
                </div>
            </div>
            <div class="badge">T.C. ULAŞIM MATRİSİ | MİLLİ ALTYAPI HAZIR</div>
        </div>
    </body>
    </html>
    """

@app.get("/belediye", response_class=HTMLResponse)
async def belediye_app():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <title>Canlı Filo Ağı</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            * { box-sizing: border-box; font-family: 'Segoe UI', sans-serif; text-decoration: none; -webkit-tap-highlight-color: transparent; }
            body { background: #020617; height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; }
            .app { width: 100vw; height: 100vh; max-width: 450px; background: #f8fafc; display: flex; flex-direction: column; position: relative; }
            @media (min-width: 460px) { .app { max-height: 850px; border-radius: 35px; border: 8px solid #1e293b; overflow: hidden; box-shadow: 0 25px 50px rgba(0,0,0,0.5); } }
            
            .led { background: #000; padding: 10px; border-bottom: 2px solid #2563eb; display: flex; align-items: center; }
            .tk-wrap { overflow: hidden; white-space: nowrap; flex: 1; }
            .tk-text { display: inline-block; color: #38bdf8; font-family: monospace; font-size: 13px; font-weight: bold; animation: scroll 20s linear infinite; }
            @keyframes scroll { from { transform: translateX(100%); } to { transform: translateX(-100%); } }
            
            .nav { background: #0f172a; padding: 15px; display: flex; align-items: center; justify-content: space-between; z-index: 2000; }
            .bck { color: white; font-weight: 900; padding: 8px 12px; background: #334155; border-radius: 8px; font-size: 13px; }
            .sel { background: #1e293b; color: white; border: 1px solid #38bdf8; padding: 8px 15px; border-radius: 8px; font-weight: bold; outline: none; }
            
            .map-box { flex: 0.6; width: 100%; position: relative; background: #e2e8f0; }
            #map { position: absolute; top: 0; bottom: 0; left: 0; right: 0; z-index: 1; }
            
            .drw { flex: 0.4; background: white; border-radius: 20px 20px 0 0; box-shadow: 0 -10px 20px rgba(0,0,0,0.1); z-index: 1000; display: flex; flex-direction: column; margin-top: -15px; }
            .hnd { width: 40px; height: 5px; background: #cbd5e1; border-radius: 10px; margin: 10px auto; }
            .src-box { padding: 0 20px 10px; border-bottom: 1px solid #f1f5f9; }
            .src { width: 100%; padding: 10px 15px; border-radius: 10px; border: 2px solid #e2e8f0; font-size: 14px; font-weight: bold; outline: none; background: #f8fafc; }
            .src:focus { border-color: #2563eb; background: #fff; }
            
            .list { padding: 0 20px 10px; overflow-y: auto; flex: 1; }
            .row { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f1f5f9; }
            .info { display: flex; flex-direction: column; gap: 4px; }
            .id { font-size: 15px; font-weight: 900; color: #0f172a; }
            .dst { font-size: 11px; color: #64748b; font-weight: 600; }
            .eta { font-size: 12px; font-weight: 900; background: #dbeafe; padding: 6px 12px; border-radius: 10px; color: #2563eb; }
        </style>
    </head>
    <body>
        <div class="app">
            <div class="led" id="led-bar"><div class="tk-wrap"><div class="tk-text" id="led">📡 MİLLİ ALTYAPI BAŞLATILIYOR | API BAĞLANTISI BEKLENİYOR...</div></div></div>
            <div class="nav">
                <a href="/" class="bck">❮ GERİ</a>
                <select class="sel" id="citySelect"></select>
            </div>
            <div class="map-box"><div id="map"></div></div>
            <div class="drw">
                <div class="hnd"></div>
                <div class="src-box"><input type="text" id="src" class="src" placeholder="🔍 Hat veya Durak Ara..."></div>
                <div class="list" id="fleet"><div style="text-align:center; padding:30px; color:#94a3b8; font-size:12px; font-weight:bold;">🔄 Ağ Bağlantısı Kuruluyor...</div></div>
            </div>
        </div>
        
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            class NationalEngine {
                constructor() {
                    this.city = 'Adana';
                    this.map = null;
                    this.layer = L.layerGroup();
                    this.initCities();
                    
                    document.getElementById('src').addEventListener('keyup', (e) => {
                        let val = e.target.value.toUpperCase();
                        document.querySelectorAll('.item').forEach(r => {
                            r.style.display = r.innerText.toUpperCase().includes(val) ? "flex" : "none";
                        });
                    });
                }
                
                async initCities() {
                    try {
                        const res = await fetch('/api/v1/cities');
                        const cities = await res.json();
                        const sel = document.getElementById('citySelect');
                        cities.forEach(c => {
                            let opt = document.createElement('option');
                            opt.value = c; opt.innerText = c;
                            if(c === this.city) opt.selected = true;
                            sel.appendChild(opt);
                        });
                        
                        sel.addEventListener('change', (e) => {
                            this.city = e.target.value;
                            this.fetchData();
                        });
                        
                        this.fetchData();
                        setInterval(() => this.fetchData(), 4000);
                    } catch(e) { console.error(e); }
                }
                
                async fetchData() {
                    try {
                        const res = await fetch('/api/v1/fleet?city=' + this.city);
                        const data = await res.json();
                        
                        if (!this.map) {
                            this.map = L.map('map', { zoomControl: false }).setView([data.merkez.lat, data.merkez.lng], 13);
                            L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {maxZoom: 19}).addTo(this.map);
                            this.layer.addTo(this.map);
                            setTimeout(() => { if(this.map) this.map.invalidateSize(); }, 300);
                        } else {
                            this.map.setView([data.merkez.lat, data.merkez.lng], 13);
                        }
                        
                        const cont = document.getElementById('fleet');
                        const led = document.getElementById('led');
                        const ledBar = document.getElementById('led-bar');
                        cont.innerHTML = '';
                        this.layer.clearLayers();
                        
                        if (data.durum === "AWAITING_API") {
                            ledBar.style.borderBottom = "2px solid #eab308";
                            led.style.color = "#facc15";
                            led.innerText = 🟡 MİLLİ ALTYAPI HAZIR | ${data.sehir.toUpperCase()} İÇİN DEVLET AÇIK VERİ İZNİ BEKLENİYOR... \u00A0\u00A0\u00A0\u00A0 🟡 MİLLİ ALTYAPI HAZIR | ${data.sehir.toUpperCase()} İÇİN DEVLET AÇIK VERİ İZNİ BEKLENİYOR...;
                            
                            cont.innerHTML = `
                                <div style="text-align:center; padding:40px 20px; color:#475569; font-size:14px; line-height:1.6;">
                                    <b>Altyapı Entegrasyonu Tamamlandı!</b><br><br>
                                    ${data.sehir} ilinin coğrafi veri tabanı sisteme eklenmiştir. İlgili kurumun KVKK ve Açık Veri izinleri onaylandığında canlı takip başlayacaktır.
                                </div>
                            `;
                        } else {
                            ledBar.style.borderBottom = "2px solid #2563eb";
                            led.style.color = "#38bdf8";
                            const icon = L.divIcon({ html: '<div style="background:#2563eb; width:22px; height:22px; border-radius:50%; border:2px solid #fff; display:flex; align-items:center; justify-content:center; color:white; font-size:10px; box-shadow:0 2px 5px rgba(0,0,0,0.3);">🚌</div>', className: 'm' });

                            data.filo.forEach(b => {
                                const bg = b.kalan === 'DURAKTA' ? 'background:#d1fae5; color:#059669;' : '';
                                cont.innerHTML += `
                                    <div class="row item">
                                        <div class="info">
                                            <span class="id">🚌 ${b.id}</span>
                                            <span class="dst">Hedef: ${b.hedef} | Hız: ${b.hiz} km/s</span>
                                        </div>
                                        <div class="eta" style="${bg}">${b.kalan}</div>
                                    </div>`;
                                L.marker([b.konum.lat, b.konum.lng], {icon: icon}).addTo(this.layer);
                            });
                            
                            const now = new Date().toLocaleTimeString('tr-TR');
                            const msg = 🟢 BAĞLANTI: GÜVENLİ | ŞEHİR: ${data.sehir.toUpperCase()} | AKTİF ARAÇ: ${data.arac_sayisi} | ORT. HIZ: ${data.ortalama_hiz} KM/S | GECİKME: ${data.gecikme_ms}ms | SAAT: ${now}...;
                            led.innerText = msg + " \u00A0\u00A0\u00A0\u00A0 " + msg;
                        }
                    } catch (e) {
                        document.getElementById('led').innerText = "🔴 BAĞLANTI KOPTU: İNTERNET AĞINIZI KONTROL EDİN...";
                        document.getElementById('led').style.color = "#ef4444";
                    }
                }
            }

            document.addEventListener('DOMContentLoaded', () => { window.App = new NationalEngine(); });
        </script>
    </body>
    </html>
    """

@app.get("/{mod}", response_class=HTMLResponse)
async def mods(mod: str):
    if mod not in ["metro", "ozel", "kart"]: return "<a href='/'>Geri</a>"
    t = {"metro": "RAYLI SİSTEMLER", "ozel": "ÖZEL SEKTÖR", "kart": "KART DOLUM"}[mod]
    return f"""
    <!DOCTYPE html><html lang="tr"><head><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ box-sizing: border-box; font-family: sans-serif; text-decoration: none; }}
        body {{ background: #020617; height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; }}
        .app {{ width: 100vw; height: 100vh; max-width: 450px; background: #f8fafc; display: flex; flex-direction: column; position:relative; }}
        @media (min-width: 460px) {{ .app {{ max-height: 850px; border-radius: 35px; border: 8px solid #1e293b; overflow:hidden; }} }}
        .nav {{ background: #0f172a; padding: 15px; display: flex; align-items: center; justify-content: center; position: relative; }}
        .bck {{ position: absolute; left: 15px; color: white; font-weight: bold; padding: 8px 12px; background: #334155; border-radius: 8px; font-size: 13px; }}
        .msg {{ margin: auto; padding: 30px; text-align: center; color: #1e293b; font-weight: bold; font-size: 15px; border: 2px dashed #cbd5e1; border-radius: 15px; width: 80%; line-height:1.5; }}
    </style></head><body><div class="app"><div class="nav"><a href="/" class="bck">❮ GERİ</a>
    <div style="color:white; font-weight:900;">{t}</div></div>
    <div class="msg">⚠️ Güvenli API Bağlantısı Bekleniyor...<br><br><span style="font-size:12px; color:#64748b;">Altyapı hazır. İlgili açık veri sistemine bağlanıldığında aktifleşecektir.</span></div></div></body></html>
    """
