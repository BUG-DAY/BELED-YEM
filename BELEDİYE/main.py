from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def ana_sayfa():
    # Burası senin o "roman" dediğin uzun HTML kodunun geleceği yer
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Belediye Akıllı Durak Sistemi</title>
        <style>
            body { background: #1a1a1a; color: #facc15; text-align: center; font-family: sans-serif; padding-top: 100px; }
            .container { border: 2px solid #facc15; display: inline-block; padding: 50px; border-radius: 15px; }
            .ufo { font-size: 80px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛸 BELEDİYE SİSTEMİ BAŞLATILDI</h1>
            <p>Sıfırdan kurulum başarıyla tamamlandı.</p>
            <div class="ufo">🛸</div>
            <p>Şimdi bu siteyi internete bağlayacağız.</p>
        </div>
    </body>
    </html>
    """