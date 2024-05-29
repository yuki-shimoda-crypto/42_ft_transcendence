import os
import random

from django.conf import settings
from PIL import Image, ImageDraw


def get_random_color_pair():
    color_pairs = [
        # (背景色, テキスト色)
        ((173, 216, 230), (139, 0, 139)),  # 薄水色と紫
        ((255, 215, 0), (0, 0, 139)),  # 黄色と紺
        ((60, 179, 113), (255, 255, 255)),  # 緑と白
        ((70, 130, 180), (255, 255, 255)),  # 水色と白
        ((211, 211, 211), (47, 79, 79)),  # ライトグレーとダークグレー
        ((144, 238, 144), (0, 100, 0)),  # ダークグリーンとライトグリーン
        ((255, 165, 0), (0, 0, 128)),  # オレンジと紺色
        ((255, 255, 224), (139, 69, 19)),  # ペールイエローとブラウン
        ((64, 224, 208), (139, 0, 0)),  # ターコイズとダークレッド
        ((250, 204, 229), (204, 0, 102)),  # ライトピンクと朱色
    ]
    return random.choice(color_pairs)


def generate_default_profile_image(username, size=200):
    text = username[:2].upper()
    bg_color, text_color = get_random_color_pair()

    # 画像の作成
    image = Image.new("RGB", (size, size), bg_color)
    draw = ImageDraw.Draw(image)

    # テキストの描画
    draw.text(
        xy=(100, 100), text=text, fill=text_color, anchor="mm", font_size=size / 2
    )

    # 画像の保存先ディレクトリ
    image_path = os.path.join(settings.MEDIA_ROOT, "profile_images")
    os.makedirs(image_path, exist_ok=True)

    # ファイル名の生成
    image_filename = f"{username.lower()}.png"
    image_full_path = os.path.join(image_path, image_filename)

    # 画像の保存
    image.save(image_full_path)

    return f"profile_images/{image_filename}"
