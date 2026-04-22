import cgi
import html
import re
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

print("Content-type: text/html; charset=utf-8\n")

form = cgi.FieldStorage()
username = html.escape(form.getvalue("username", "пользователь"))
password = form.getvalue("password", "")


def get_complexity(value):
    score = 0
    if len(value) >= 8:
        score += 1
    if re.search("[a-z]", value) and re.search("[A-Z]", value):
        score += 1
    if re.search("[0-9]", value):
        score += 1
    if re.search(r"[!@#$%^&*()_+\-=]", value):
        score += 1
    return score


score = get_complexity(password)

if score >= 3:
    status = "Пароль подходит"
    color = "#2f855a"
    message = f"Аккаунт для {username} можно считать созданным. Пароль имеет достаточную сложность."
    back_link = "/index.html"
    back_label = "Перейти на главную"
    redirect_tag = '<meta http-equiv="refresh" content="3;url=/index.html">'
else:
    status = "Пароль слишком слабый"
    color = "#c05645"
    message = "Используйте минимум 8 символов, добавьте цифры, буквы разного регистра и по возможности спецсимволы."
    back_link = "/auth.html"
    back_label = "Вернуться и исправить"
    redirect_tag = ""

print(
    f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    {redirect_tag}
    <title>Проверка пароля</title>
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
        }}
        .eyebrow {{
            margin: 0 0 8px;
            color: {color};
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 0.75rem;
            font-weight: 700;
        }}
        h1 {{ margin: 0 0 14px; }}
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
        <p class="eyebrow">{status}</p>
        <h1>Результат проверки</h1>
        <p>{message}</p>
        <a href="{back_link}">{back_label}</a>
    </div>
</body>
</html>"""
)
