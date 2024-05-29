from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings


def generate_profile_image(username, size=200):
    text = username[:2].upper()
    bg_color = (173, 216, 230)  # 背景色 (ライトブルー)
    text_color = (139, 0, 139)  # テキスト色 (ダークマゼンタ)

    # 画像の作成
    image = Image.new('RGB', (size, size), bg_color)
    draw = ImageDraw.Draw(image)

    # フォントの設定
    font_size = int(size * 0.5)
    try:
        font = ImageFont.truetype("arial", font_size)
    except IOError:
        font = ImageFont.load_default()

    # テキストの位置計算
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) / 2
    text_y = (size - text_height) / 2

    # テキストの描画
    draw.text((text_x, text_y), text, font=font, fill=text_color)

    # 画像の保存先ディレクトリ
    image_path = os.path.join(settings.MEDIA_ROOT, 'profile_images')
    os.makedirs(image_path, exist_ok=True)

    # ファイル名の生成
    image_filename = f"{username.lower()}.png"
    image_full_path = os.path.join(image_path, image_filename)

    # 画像の保存
    image.save(image_full_path)

    return f"profile_images/{image_filename}"
