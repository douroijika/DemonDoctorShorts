print("★DEMON DOCTOR SHORT 01★")

import os
import pyttsx3
import moviepy as mp
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math

W, H = 1080, 1920
OUT_FILE = "demon_doctor_short_01.mp4"
VOICE_DIR = "voice_demon_doctor_01"
SPEECH_RATE = 165

def get_font(size):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", size)
    except:
        return ImageFont.load_default()

scenes = [
    ("s01", "将棋AIは、\n実は熱力学です。"),
    ("s02", "良い局面ほど、\n自由エネルギーが低い。"),
    ("s03", "AIは山を下りながら、\n勝ちへ近づく。"),
    ("s04", "Mesh AIは、\nその“流れ”を見ています。"),
    ("s05", "デーモン博士でした。")
]

def voice_text_fix(t):
    return (
        t.replace("将棋AI", "しょうぎエーアイ")
         .replace("熱力学", "ねつりきがく")
         .replace("自由エネルギー", "じゆうエネルギー")
         .replace("局面", "きょくめん")
         .replace("Mesh AI", "メッシュ エーアイ")
         .replace("流れ", "ながれ")
         .replace("博士", "はかせ")
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
    draw.ellipse([390, 260, 690, 560], fill=(220,220,230), outline=(255,255,255), width=5)

    # 角
    draw.polygon([(410,280),(350,150),(470,255)], fill=(120,0,0), outline=(255,255,255))
    draw.polygon([(670,280),(730,150),(610,255)], fill=(120,0,0), outline=(255,255,255))

    # 顔
    draw.ellipse([455,360,505,415], fill=(20,20,20))
    draw.ellipse([575,360,625,415], fill=(20,20,20))
    draw.arc([480,430,600,510], 10, 170, fill=(120,0,0), width=6)

    # 白衣
    draw.rectangle([355,560,725,1020], fill=(235,235,240), outline=(255,255,255), width=5)
    draw.line([540,560,540,1020], fill=(0,0,0), width=4)

    # ネクタイ
    draw.polygon([(510,580),(570,580),(555,780),(525,780)], fill=(80,0,120))

    # 黒板
    draw.rectangle([90, 1030, 990, 1320], fill=(15,70,45), outline=(255,255,255), width=5)
    font_formula = get_font(54)
    draw.text((130, 1080), "F = E - T S", font=font_formula, fill=(255,255,255))
    draw.text((130, 1160), "Shogi Space = Mountain", font=get_font(38), fill=(255,255,255))
    draw.text((130, 1230), "AI follows the flow", font=get_font(38), fill=(255,255,255))

def draw_mountain(draw):
    # 山並み
    points = []
    for x in range(0, W+1, 30):
        y = 1480 - int(120 * math.sin(x / 90.0)) - int(70 * math.sin(x / 37.0))
        points.append((x, y))
    poly = [(0, H)] + points + [(W, H)]
    draw.polygon(poly, fill=(50,70,95))

    # 流れ線
    for i in range(6):
        y = 1420 + i * 55
        draw.line([(120, y), (940, y + 80)], fill=(80,180,255), width=5)
        draw.polygon([(940,y+80),(900,y+55),(910,y+105)], fill=(80,180,255))

def draw_frame(text, scene_index):
    img = Image.new("RGB", (W, H), (12,12,18))
    draw = ImageDraw.Draw(img)

    font_title = get_font(72)
    font_text = get_font(84)
    font_small = get_font(44)

    # 背景 星
    for i in range(90):
        x = (i * 137) % W
        y = (i * 251) % H
        r = 2 if i % 3 else 3
        draw.ellipse([x, y, x+r, y+r], fill=(180,180,220))

    draw.text((55, 45), "デーモン博士の将棋AI講座", font=font_small, fill=(255,255,0))

    draw_demon_doctor(draw)
    draw_mountain(draw)

    # メインテロップ
    draw.rectangle([50, 1350, 1030, 1780], fill=(0,0,0), outline=(255,255,255), width=5)

    yy = 1400
    for line in text.split("\n"):
        use_font = font_text if len(line) <= 13 else font_title
        draw.text((85, yy), line, font=use_font, fill=(255,255,255))
        yy += 115

    # 下部
    draw.text((70, 1830), "#将棋AI #熱力学 #MeshAI", font=get_font(42), fill=(180,220,255))

    return np.array(img)

def main():
    make_voice_files()

    clips = []

    for idx, (key, text) in enumerate(scenes):
        audio = audio_clip_for(key)
        dur = max(4.0, audio.duration + 0.35 if audio else 4.0)

        frame = draw_frame(text, idx)
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