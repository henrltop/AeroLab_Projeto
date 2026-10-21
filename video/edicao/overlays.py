"""Gera PNGs de sobreposição usados na montagem (painel lateral da demo e cartão do repositório)."""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = "/home/claude/edit/src/ov"
os.makedirs(OUT, exist_ok=True)
F = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
TXT, CINZA = (27, 42, 65), (91, 107, 128)
LAR, AZU, ROX = (198, 106, 22), (36, 120, 200), (134, 86, 185)


def font(w, s):
    return ImageFont.truetype(F % w, s)


# Painel lateral da demonstração (camada RGBA 1920x1080; vídeo de tela fica em x24..1504, y40..873; PiP em x1528..1896, y40..316)
im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
d.text((1528, 330), "Ventoinha no", font=font("SemiBold", 30), fill=CINZA)
d.text((1528, 366), "mesmo instante", font=font("SemiBold", 30), fill=CINZA)
y = 470
d.text((1528, y), "No gráfico", font=font("Bold", 34), fill=TXT)
itens = [(LAR, "contínua", "RPM desejado"), (AZU, "contínua", "RPM medido"), (ROX, "pontilhada", "PWM (eixo dir.)")]
for i, (cor, est, nome) in enumerate(itens):
    yy = y + 70 + i * 84
    if est == "pontilhada":
        for x in range(1530, 1600, 14):
            d.line([(x, yy + 20), (x + 7, yy + 20)], fill=cor, width=6)
    else:
        d.line([(1530, yy + 20), (1600, yy + 20)], fill=cor, width=9 if i == 0 else 6)
    d.text((1616, yy), nome, font=font("SemiBold", 32), fill=cor)
im.save(f"{OUT}/demo_lateral.png")

# Cartão do repositório (sem URL até ser publicada)
im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
d.rounded_rectangle([1060, 300, 1840, 700], radius=28, fill=(255, 255, 255, 240), outline=(213, 220, 230, 255), width=3)
d.text((1110, 345), "No repositório", font=font("Bold", 56), fill=TXT)
for i, t in enumerate(["Firmware do ESP32", "Painel (interface)", "Modelo 3D do suporte"]):
    d.ellipse([1112, 462 + i * 66, 1130, 480 + i * 66], fill=LAR)
    d.text((1150, 450 + i * 66), t, font=font("Regular", 40), fill=TXT)
d.text((1110, 650), "Link na descrição do vídeo", font=font("SemiBold", 30), fill=CINZA)
im.save(f"{OUT}/repo_card.png")
print("ok")
