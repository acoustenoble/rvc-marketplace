from PIL import Image, ImageDraw, ImageFont

NAVY = (27, 42, 74, 255)
GOLD = (184, 151, 90, 255)
WHITE = (255, 255, 255, 255)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def make(path, textcolor, bar=GOLD, scale=6):
    W, H = 900*scale//6, 460*scale//6
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = scale/6
    # gold vertical bar on the left
    bar_w = int(46*s)
    bar_x = int(40*s)
    d.rectangle([bar_x, int(30*s), bar_x+bar_w, int(300*s)], fill=bar)
    # RVC
    f_rvc = ImageFont.truetype(SERIF, int(230*s))
    rvc_x = bar_x + bar_w + int(28*s)
    d.text((rvc_x, int(8*s)), "RVC", font=f_rvc, fill=textcolor)
    # IMMOBILIER with letter spacing
    f_imm = ImageFont.truetype(SANS, int(70*s))
    txt = "IMMOBILIER"
    spacing = int(14*s)
    x = rvc_x + int(6*s)
    y = int(330*s)
    for ch in txt:
        d.text((x, y), ch, font=f_imm, fill=textcolor)
        bbox = d.textbbox((0, 0), ch, font=f_imm)
        x += (bbox[2]-bbox[0]) + spacing
    # crop to content
    bbox = img.getbbox()
    img = img.crop(bbox)
    img.save(path)
    print("saved", path, img.size)

make("/sessions/fervent-pensive-hypatia/mnt/outputs/mandat-gestion/assets/logo-rvc-color.png", NAVY)
make("/sessions/fervent-pensive-hypatia/mnt/outputs/mandat-gestion/assets/logo-rvc-white.png", WHITE)
