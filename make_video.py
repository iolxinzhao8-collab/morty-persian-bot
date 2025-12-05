import os, sys, requests
from moviepy.editor import *
from gtts import gTTS

topic = sys.argv[1]
folder = sys.argv[2]

script = [
    f"ریک: بورپ! مورتی بیا بریم {topic}",
    "مورتی: اوه خدای من ریک نه دوباره!",
    "ریک: ساکت باش فقط بیا… بورپ!",
    "مورتی: وااا این کجاست؟ همه دارن نوروز جشن گرفتن!",
    "ریک: رسیدیم ایران ۱۴۰۴… بورپ جالب شد",
    "مورتی: ولی ما هدیه نیاوردیم ریک!",
    "ریک: من دستگاه هفت‌سین‌ساز دارم… نگاه کن بورپ!"
]

clips = []
for i, line in enumerate(script):
    speaker = "rick" if "ریک" in line else "morty"
    text = line.split(":", 1)[1] if ":" in line else line

    # صدا
    tts = gTTS(text, lang='fa')
    audio = f"{folder}/a{i}.mp3"
    tts.save(audio)

    # تصویر
    url = f"https://image.pollinations.ai/prompt/{text} rick and morty style vibrant cartoon?width=1280&height=720&nologo"
    img = f"{folder}/i}.jpg"
    open(img, "wb").write(requests.get(url).content)

    duration = AudioFileClip(audio).duration + 1.5
    clip = ImageClip(img).set_duration(duration).resize(lambda t: 1 + 0.04*t)
    txt = TextClip(text, fontsize=50, color="lime" if speaker=="rick" else "yellow",
                   font="Arial-Bold", stroke_color="black", stroke_width=3)\
          .set_pos(('center','bottom')).set_duration(duration)
    final_clip = CompositeVideoClip([clip, txt]).set_audio(AudioFileClip(audio))
    clips.append(final_clip)

video = concatenate_videoclips(clips)
video.write_videofile(f"{folder}/final.mp4", fps=24, preset="ultrafast", threads=4)
print("ویدیو آماده شد")
