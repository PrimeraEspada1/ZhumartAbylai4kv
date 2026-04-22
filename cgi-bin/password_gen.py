import cgi
import html
import random
import string
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

print("Content-type: text/html; charset=utf-8\n")

form = cgi.FieldStorage()

length = int(form.getvalue("length", 12))
use_digits = form.getvalue("use_digits")
use_upper = form.getvalue("use_upper")
use_special = form.getvalue("use_special")


def generate_password(password_length, digits, upper, special):
    chars = string.ascii_lowercase
    if digits:
        chars += string.digits
    if upper:
        chars += string.ascii_uppercase
    if special:
        chars += "!@#$%^&*()_+-="
    return "".join(random.choice(chars) for _ in range(password_length))


def get_complexity_label(password):
    if len(password) >= 12 and any(c.isdigit() for c in password) and any(c.isupper() for c in password):
        return "Высокая"
    if len(password) >= 8:
        return "Средняя"
    return "Низкая"


new_password = generate_password(length, use_digits, use_upper, use_special)
safe_password = html.escape(new_password)
complexity = get_complexity_label(new_password)

print(
    f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Генератор паролей</title>
    <style>
        body {{
            margin: 0;
            min-height: 100vh;
            display: grid;
            place-items: center;
            font-family: "Trebuchet MS", "Segoe UI", sans-serif;
            background: linear-gradient(180deg, #fff8ec 0%, #f4ecdd 100%);
            color: #1f2933;
        }}
        .card {{
            width: min(560px, calc(100% - 32px));
            padding: 32px;
            border-radius: 28px;
            background: rgba(255, 251, 245, 0.92);
            border: 1px solid rgba(104, 84, 55, 0.16);
            box-shadow: 0 22px 50px rgba(76, 53, 31, 0.14);
            text-align: center;
        }}
        .eyebrow {{
            margin: 0 0 8px;
            color: #b95c2e;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 0.75rem;
            font-weight: 700;
        }}
        .password {{
            margin: 18px 0;
            padding: 18px;
            border-radius: 18px;
            background: #fffdfa;
            border: 1px dashed rgba(185, 92, 46, 0.35);
            font-family: Consolas, monospace;
            font-size: 1.3rem;
        }}
        p {{ color: #5d6a74; line-height: 1.6; }}
        a {{
            display: inline-block;
            margin-top: 16px;
            padding: 12px 18px;
            border-radius: 16px;
            background: linear-gradient(135deg, #b95c2e, #d18147);
            color: #fff;
            text-decoration: none;
            font-weight: 700;
        }}
    </style>
</head>
<body>
    <div class="card">
        <p class="eyebrow">Новый пароль</p>
        <h1>Генерация завершена</h1>
        <div class="password">{safe_password}</div>
        <p>Оценка сложности: {complexity}.</p>
        <a href="/auth.html">Вернуться в кабинет</a>
    </div>
</body>
</html>"""
)
