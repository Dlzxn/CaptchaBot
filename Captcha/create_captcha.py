from PIL import Image, ImageDraw, ImageFont
import random
import os


def generate_image_captcha():
    # Создаем изображение
    img = Image.new('RGB', (100, 15), color=(200, 200, 200))
    d = ImageDraw.Draw(img)

    # Генерируем случайный текст (4 символа)
    captcha_text = ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', k=4))

    # Добавляем шум
    # for _ in range(80):
    #     x = random.randint(0, 200)
    #     y = random.randint(0, 50)
    #     d.line([(x, y), (x + 10, y + 10)],
    #            fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), width=2)

    # Рисуем текст
    kaef_font: int = 2
    font = ImageFont.load_default()

    text_width= d.textbbox((0, 0), captcha_text)
    print(text_width)
    d.text(
        ((100 - text_width[0]*kaef_font) // 2, (15 - text_width[1]*kaef_font) // 2),
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
    img = Image.new('RGB', (100, 15), color=(200, 200, 200))
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
    # for _ in range(100):
    #     x = random.randint(0, 200)
    #     y = random.randint(0, 50)
    #     d.line([(x, y), (x + 10, y + 10)],
    #            fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), width=2)

    # Рисуем текст
    kaef_font: int = 2
    font = ImageFont.load_default()

    text_width= d.textbbox((0, 0), captcha_text)
    print(text_width)
    d.text(
        ((100 - text_width[0]*kaef_font) // 2, (15 - text_width[1]*kaef_font) // 2),
        captcha_text,
        font=font,
        fill=(0, 0, 0)
    )

    # Сохраняем в папку `captchas`
    os.makedirs('captchas', exist_ok=True)
    img_path = f'captchas/{captcha_text}.png'
    img.save(img_path)

    return answer, img_path

def generate_ariphmetic():
    rand = random.randint(1, 4)

    if rand == 1:
        a = random.randint(0, 10)
        b = random.randint(0, 10)
        captcha_text = f'{a} + {b}'
        answer: int = a + b

    if rand == 2:
        a = random.randint(0, 10)
        b = random.randint(0, 10)
        captcha_text = f'{a} - {b}'
        answer: int = a - b

    if rand == 3:
        a = random.randint(0, 10)
        b = random.randint(0, 10)
        captcha_text = f'{a} * {b}'
        answer: int = a * b

    if rand == 4:
        a = random.randint(0, 10)
        b = random.randint(0, 10)
        captcha_text = f'{a * b} % {b}'
        answer: int = a

    return answer, captcha_text


