print("★DEMON DOCTOR SHORT 02 MOUNTAIN★")

import os
import math
import pyttsx3
import moviepy as mp
from PIL import Image, ImageDraw, ImageFont
import numpy as np

W, H = 1080, 1920
OUT_FILE = "demon_doctor_short_02_mountain.mp4"
VOICE_DIR = "voice_demon_doctor_02"
SPEECH_RATE = 165

def get_font(size):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", size)
    except:
        return ImageFont.load_default()

scenes = [
    ("s01", "将棋空間には、\n山脈があります。"),
    ("s02", "局面は、\n孤立していません。"),
    ("s03", "良い局面は山頂、\n悪い局面は谷。"),
    ("s04", "AIは、\nその地形を移動しています。"),
    ("s05", "Mesh AIは、\nその“流れ”を見ています。"),
    ("s06", "将棋空間は、\n巨大な地形なのかもしれません。")
]

def voice_text_fix(t):
    return (
        t.replace("将棋空間", "しょうぎくうかん")
         .replace("将棋", "しょうぎ")
         .replace("局面", "きょくめん")
         .replace("山脈", "さんみゃく")
         .replace("山頂", "さんちょう")
         .replace("谷", "たに")
         .replace("地形", "ちけい")
         .replace("AI", "エーアイ")
         .replace("Mesh AI", "メッシュ エーアイ")
         .replace("流れ", "ながれ")
    )

def make_voice_files():
    os.makedirs(VOICE_DIR, exist_ok=True)
    engine = pyttsx3.init()
    engine.setProperty("rate", SPEECH_RATE)
    engine.setProperty("volume", 1.0)

    for key, text in scenes:
        path = os.path.join(VOICE_DIR, f"{key}.wav")
        if not os.path.exists(path):
            print("音声生成:", key)
            engine.save_to_file(voice_text_fix(text), path)

    engine.runAndWait()

def audio_clip_for(key):
    path = os.path.join(VOICE_DIR, f"{key}.wav")
    if os.path.exists(path):
        return mp.AudioFileClip(path)
    return None

def draw_demon_doctor(draw):
    # 頭
    draw.ellipse([390, 250, 690, 550], fill=(220,220,230), outline=(255,255,255), width=5)

    # 角
    draw.polygon([(410,280),(350,140),(470,250)], fill=(120,0,0), outline=(255,255,255))
    draw.polygon([(670,280),(730,140),(610,250)], fill=(120,0,0), outline=(255,255,255))

    # 目と口
    draw.ellipse([455,350,505,405], fill=(20,20,20))
    draw.ellipse([575,350,625,405], fill=(20,20,20))
    draw.arc([480,420,600,500], 10, 170, fill=(120,0,0), width=6)

    # 白衣
    draw.rectangle([355,550,725,1000], fill=(235,235,240), outline=(255,255,255), width=5)
    draw.line([540,550,540,1000], fill=(0,0,0), width=4)

    # ネクタイ
    draw.polygon([(510,570),(570,570),(555,770),(525,770)], fill=(80,0,120))

def draw_mountain_map(draw):
    # 背景の山脈
    for layer in range(3):
        points = []
        base = 1200 + layer * 130
        amp1 = 130 - layer * 25
        amp2 = 70 - layer * 15
        for x in range(0, W + 1, 20):
            y = base - int(amp1 * math.sin(x / (85 + layer * 30))) - int(amp2 * math.sin(x / (37 + layer * 18)))
            points.append((x, y))
        poly = [(0, H)] + points + [(W, H)]
        fill = [(45,70,105), (38,58,88), (30,45,70)][layer]
        draw.polygon(poly, fill=fill)

    # 流れの矢印
    for i in range(5):
        x1 = 130 + i * 120
        y1 = 1260 + i * 65
        x2 = x1 + 250
        y2 = y1 + 80
        draw.line([(x1, y1), (x2, y2)], fill=(90,200,255), width=7)
        draw.polygon([(x2,y2),(x2-45,y2-30),(x2-25,y2+35)], fill=(90,200,255))

    # 山頂・谷ラベル
    font = get_font(42)
    draw.text((120, 1110), "山頂 = 良い局面", font=font, fill=(255,255,0))
    draw.text((600, 1420), "谷 = 悪い局面", font=font, fill=(255,210,210))

def draw_board_hologram(draw):
    ox, oy = 115, 980
    size = 260
    cell = size // 9

    draw.rectangle([ox-10, oy-10, ox+size+10, oy+size+10], outline=(80,220,255), width=4)

    for i in range(10):
        x = ox + i * cell
        y = oy + i * cell
        draw.line([(x, oy), (x, oy+size)], fill=(80,220,255), width=2)
        draw.line([(ox, y), (ox+size, y)], fill=(80,220,255), width=2)

    draw.text((ox + 35, oy + 100), "局面空間", font=get_font(42), fill=(180,240,255))

def draw_frame(text):
    img = Image.new("RGB", (W, H), (10,10,18))
    draw = ImageDraw.Draw(img)

    font_top = get_font(44)
    font_text = get_font(78)
    font_text_small = get_font(62)

    # 星
    for i in range(100):
        x = (i * 137) % W
        y = (i * 251) % H
        r = 2 if i % 3 else 3
        draw.ellipse([x, y, x+r, y+r], fill=(180,180,230))

    draw.text((55, 45), "デーモン博士の将棋AI講座", font=font_top, fill=(255,255,0))

    draw_demon_doctor(draw)
    draw_board_hologram(draw)
    draw_mountain_map(draw)

    # テロップ
    draw.rectangle([50, 1450, 1030, 1810], fill=(0,0,0), outline=(255,255,255), width=5)

    yy = 1500
    for line in text.split("\n"):
        use_font = font_text if len(line) <= 13 else font_text_small
        draw.text((85, yy), line, font=use_font, fill=(255,255,255))
        yy += 110

    draw.text((70, 1840), "#将棋AI #MeshAI #将棋空間", font=get_font(40), fill=(180,220,255))

    return np.array(img)

def main():
    make_voice_files()

    clips = []

    for key, text in scenes:
        audio = audio_clip_for(key)
        dur = max(4.0, audio.duration + 0.35 if audio else 4.0)

        frame = draw_frame(text)
        clip = mp.ImageClip(frame).with_duration(dur)

        if audio:
            clip = clip.with_audio(audio)

        clips.append(clip)

    video = mp.concatenate_videoclips(clips, method="compose")

    video.write_videofile(
        OUT_FILE,
        fps=30,
        codec="libx264",
        audio_codec="aac"
    )

    print("完成:", OUT_FILE)

if __name__ == "__main__":
    main()