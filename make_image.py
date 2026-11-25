"""Render the 25 November 2026 world-news front page to assets/entry.png.

Run once at build time; main.py only copies the stored PNG so both runs
write identical bytes with no network.
"""
from PIL import Image, ImageDraw, ImageFont

F = "/usr/share/fonts/truetype/noto/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

W = H = 1024
NAVY = (16, 28, 52)
PAPER = (247, 243, 234)
INK = (24, 24, 28)
GREY = (92, 92, 100)
RED = (196, 38, 38)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def block(x, y, text, fnt, width, fill, gap=4):
    for line in wrap(text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + gap
    return y

# ---- masthead
d.rectangle([0, 0, W, 104], fill=NAVY)
d.text((32, 16), "THE WORLD IN ONE PAGE", font=font("NotoSans-Bold.ttf", 18), fill=(230, 196, 120))
d.text((32, 40), "Wednesday, 25 November 2026", font=font("NotoSerif-Black.ttf", 44), fill=(255, 255, 255))
d.text((W - 32, 22), "Daily world news", font=font("NotoSans-Medium.ttf", 16), fill=(190, 200, 220), anchor="ra")

# ---- lead story
d.rectangle([24, 120, W - 24, 372], fill=(255, 255, 255), outline=(220, 214, 200))
d.rectangle([24, 120, 32, 372], fill=RED)
d.text((52, 134), "TOP STORY  ·  MIDDLE EAST", font=font("NotoSans-Bold.ttf", 16), fill=RED)
y = block(52, 160, "Iran war widens: Saudi-led strikes hit Yemen's Hodeidah port as Houthis threaten Jeddah",
          font("NotoSerif-Black.ttf", 34), 640, INK, gap=2)
bul = font("NotoSans-Regular.ttf", 17)
for t in ["Houthi drone hits Riyadh financial tower, 11 injured",
          "Tehran warns ships in Hormuz after vessels reportedly hit mines",
          "Ukraine's strikes on Russian ships in Benghazi pull Libya in"]:
    d.ellipse([54, y + 10, 62, y + 18], fill=RED)
    d.text((72, y + 2), t, font=bul, fill=GREY)
    y += 26

# lead pictogram: target over sea with ship
cx, cy = 862, 246
d.ellipse([cx - 104, cy - 104, cx + 104, cy + 104], fill=(232, 240, 248))
for i in range(4):
    yy = cy + 30 + i * 16
    d.arc([cx - 90, yy - 8, cx - 30, yy + 8], 0, 180, fill=(70, 120, 170), width=3)
    d.arc([cx - 30, yy - 8, cx + 30, yy + 8], 0, 180, fill=(70, 120, 170), width=3)
    d.arc([cx + 30, yy - 8, cx + 90, yy + 8], 0, 180, fill=(70, 120, 170), width=3)
d.polygon([(cx - 60, cy + 10), (cx + 60, cy + 10), (cx + 44, cy + 34), (cx - 44, cy + 34)], fill=NAVY)
d.rectangle([cx - 20, cy - 16, cx + 18, cy + 10], fill=NAVY)
d.rectangle([cx - 4, cy - 40, cx + 2, cy - 16], fill=NAVY)
for r in (70, 46):
    d.ellipse([cx - r, cy - 12 - r, cx + r, cy - 12 + r], outline=RED, width=4)
d.line([cx - 92, cy - 12, cx + 92, cy - 12], fill=RED, width=3)
d.line([cx, cy - 104, cx, cy + 80], fill=RED, width=3)

# ---- story grid
stories = [
    ("SPACE", (88, 60, 160), "Pakistan's first astronaut reaches China's Tiangong",
     "Zeeshan Ali, first foreigner ever to board the station"),
    ("JUSTICE", (140, 30, 60), "World Court rules Myanmar committed genocide",
     "First state held directly responsible over the Rohingya"),
    ("MARKETS", (20, 110, 80), "AI doubts sink Asian tech: Nikkei -2.8%",
     "Seoul falls over 6%; Nvidia drops 7% amid probe questions"),
    ("US / CHINA", (180, 90, 20), "US jury convicts Huawei of trade-secret theft",
     "Bank-fraud guilty verdict after an 11-week New York trial"),
    ("PACIFIC", (20, 100, 150), "Solomon Islands picks Australia for security",
     "New treaty bars foreign bases, curbing China's reach"),
    ("AMERICAS", (150, 60, 40), "Cartagena siege ends, all hostages freed",
     "Colombian forces storm supermarket held since Tuesday"),
    ("LABOUR", (90, 110, 30), "Bangladesh garment wage rises 36%",
     "Gain follows weeks of protests over living costs"),
    ("TRADE", (60, 70, 90), "US readies new tariffs on 16 trading partners",
     "Duties to stack on top of existing levies"),
]
col_w, x0, y0, row_h = 476, 24, 388, 124
hf = font("NotoSerif-Bold.ttf", 21)
sf = font("NotoSans-Regular.ttf", 15)
tf = font("NotoSans-Bold.ttf", 13)
for i, (tag, colr, head, sub) in enumerate(stories):
    x = x0 + (i % 2) * (col_w + 24)
    y = y0 + (i // 2) * row_h
    d.rectangle([x, y, x + col_w, y + row_h - 12], fill=(255, 255, 255), outline=(220, 214, 200))
    tw = d.textlength(tag, font=tf)
    d.rectangle([x + 14, y + 12, x + 26 + tw, y + 32], fill=colr)
    d.text((x + 20, y + 14), tag, font=tf, fill=(255, 255, 255))
    yy = block(x + 14, y + 38, head, hf, col_w - 28, INK, gap=1)
    block(x + 14, yy + 2, sub, sf, col_w - 28, GREY, gap=2)

# ---- markets strip
my = 888
d.rectangle([0, my, W, my + 52], fill=NAVY)
mk = font("NotoSans-SemiBold.ttf", 16)
items = [("Nikkei", "-2.78%"), ("Nasdaq", "-1.48%"), ("S&P 500", "-0.50%"),
         ("Brent", "$87.41 -4.4%"), ("Gold", "$3,516 -1.3%"), ("Nat gas", "+9.6%")]
x = 24
for name, val in items:
    d.text((x, my + 15), name, font=mk, fill=(190, 200, 220))
    x += d.textlength(name, font=mk) + 6
    colv = (120, 220, 150) if val.startswith("+") else (255, 130, 120)
    d.text((x, my + 15), val, font=mk, fill=colv)
    x += d.textlength(val, font=mk) + 22

# ---- footer
ff = font("NotoSans-Regular.ttf", 13)
d.text((24, 954), "Also today: Ebola toll in DR Congo passes 5,800 · WHO urges end to US fuel blockade on Cuba ·",
       font=ff, fill=GREY)
d.text((24, 972), "dozens of miners trapped in Indonesia", font=ff, fill=GREY)
d.text((24, 996), "Sources: Horizon daily brief, Gulf News, CuriousCats, The Daily Edition (25 Nov 2026).  Image: Alenus",
       font=font("NotoSans-Medium.ttf", 12), fill=(130, 130, 140))

img.save("assets/entry.png", optimize=True)
print("ok")
