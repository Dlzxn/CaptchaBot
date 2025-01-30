from PIL import Image, ImageDraw, ImageFont
import random
import os


def generate_image_captcha():
    # Создаем изображение
    img = Image.new('RGB', (200, 100), color=(255, 255, 255))
    d = ImageDraw.Draw(img)

    # Генерируем случайный текст (4 символа)
    captcha_text = ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', k=4))

    # Добавляем шум
    for _ in range(80):
        x = random.randint(0, 200)
        y = random.randint(0, 100)
        d.line([(x, y), (x + 10, y + 10)],
               fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), width=2)

    # Рисуем текст
    font = ImageFont.load_default()

    text_width= d.textbbox((0, 0), captcha_text)
    print(text_width)
    d.text(
        ((200 - text_width[0]) // 2, (100 - text_width[1]) // 2),
        captcha_text,
        font=font,
        fill=(0, 0, 0)
    )

    # Сохраняем в папку `captchas`
    os.makedirs('captchas', exist_ok=True)
    img_path = f'captchas/{captcha_text}.png'
    img.save(img_path)

    return captcha_text, img_path

def generate_math_image_captcha():
    """
    Создаем изображение капчу с мат выражением
    :return:
    """
    img = Image.new('RGB', (200, 100), color=(255, 255, 255))
    d = ImageDraw.Draw(img)

    rand = random.randint(1, 4)

    if rand == 1:
        a = random.randint(0, 100)
        b = random.randint(0, 100)
        captcha_text = f'{a} + {b}'
        answer: int = a + b

    if rand == 2:
        a = random.randint(0, 100)
        b = random.randint(0, 100)
        captcha_text = f'{a} - {b}'
        answer: int = a - b

    if rand == 3:
        a = random.randint(0, 100)
        b = random.randint(0, 100)
        captcha_text = f'{a} * {b}'
        answer: int = a * b

    if rand == 4:
        a = random.randint(0, 100)
        b = random.randint(0, 100)
        captcha_text = f'{a*b} % {b}'
        answer: int = a


    # Добавляем шум
    for _ in range(150):
        x = random.randint(0, 200)
        y = random.randint(0, 100)
        d.line([(x, y), (x + 10, y + 10)],
               fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), width=2)

    # Рисуем текст
    font = ImageFont.load_default()

    text_width= d.textbbox((0, 0), captcha_text)
    print(text_width)
    d.text(
        ((200 - text_width[0]) // 2, (100 - text_width[1]) // 2),
        captcha_text,
        font=font,
        fill=(0, 0, 0)
    )

    # Сохраняем в папку `captchas`
    os.makedirs('captchas', exist_ok=True)
    img_path = f'captchas/{captcha_text}.png'
    img.save(img_path)

    return answer, img_path


