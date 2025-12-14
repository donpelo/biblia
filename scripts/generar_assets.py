from PIL import Image, ImageDraw, ImageFont
import os

BASE = "gui/assets"
os.makedirs(f"{BASE}/buttons", exist_ok=True)
os.makedirs(f"{BASE}/backgrounds", exist_ok=True)
os.makedirs(f"{BASE}/icons", exist_ok=True)

COLORS = {
    "gold": "#FFD700",
    "blue": "#65B5F6",
    "paper": "#F5F5DC",
    "ink": "#2B2B2B",
    "dark": "#2E2B59"
}

def boton(nombre, texto, color):
    img = Image.new("RGBA", (220, 60), color)
    d = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 26)
    except:
        font = ImageFont.load_default()

    bbox = d.textbbox((0, 0), texto, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    d.text(
        ((220 - w) / 2, (60 - h) / 2),
        texto,
        fill=COLORS["ink"],
        font=font
    )

    img.save(f"{BASE}/buttons/{nombre}.png")

def fondo():
    img = Image.new("RGB", (900, 600), COLORS["paper"])
    d = ImageDraw.Draw(img)

    for i in range(0, 600, 8):
        d.line((0, i, 900, i), fill="#E8E3C7")

    img.save(f"{BASE}/backgrounds/pergamino.png")

def icono():
    img = Image.new("RGBA", (256, 256), COLORS["dark"])
    d = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 90)
    except:
        font = ImageFont.load_default()

    d.text((70, 70), "✝", fill="white", font=font)
    img.save(f"{BASE}/icons/icon.png")

boton("leer", "Leer", COLORS["gold"])
boton("siguiente", "Siguiente", COLORS["blue"])
boton("play", "▶", COLORS["gold"])
boton("pause", "⏸", COLORS["blue"])
fondo()
icono()
