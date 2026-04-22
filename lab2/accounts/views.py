from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import urllib.request
import urllib.error
from .forms import LoginForm, ProfileAvatarForm, RegisterForm
from .models import ServiceRequest


def home(request):
    return render(request, "index.html")

@csrf_exempt
def chatbot_view(request):
    if request.method != "POST":
        return JsonResponse({"reply": "Only POST requests are allowed"}, status=405)
        
    GROQ_API_KEY = "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"
    api_key = os.environ.get("GROQ_API_KEY", "").strip() or GROQ_API_KEY
    if not api_key:
        return JsonResponse({"reply": "Чат-бот пока не настроен: не найден ключ для доступа к Groq API."}, status=500)

    try:
        request_data = json.loads(request.body)
    except json.JSONDecodeError:
        request_data = {}

    user_message = str(request_data.get("message", "")).strip()

    if not user_message:
        return JsonResponse({"reply": "Напишите вопрос о ремонте, диагностике или апгрейде компьютера."}, status=400)

    system_prompt = (
        "Ты полезный консультант сайта по ремонту и обслуживанию компьютеров. "
        "Отвечай на русском языке. Давай понятные, практичные и безопасные советы по темам: "
        "перегрев, шум, синий экран, медленная работа ПК, выбор SSD, RAM, блока питания, чистка, "
        "профилактика, диагностика ноутбуков и сборок. "
        "Если проблема может привести к потере данных или риску для электроники, сначала советуй резервную копию "
        "и безопасную диагностику. Не выдумывай выполненные действия. Не обещай точный ремонт без осмотра. "
        "Структурируй ответ кратко: причина, что проверить, что сделать дальше."
    )

    payload = {
        "model": "llama-3.1-8b-instant",
        "temperature": 0.4,
        "max_tokens": 500,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    }

    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            groq_data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="ignore")
        details = error_body[:400]
        try:
            parsed_error = json.loads(error_body)
            details = (
                parsed_error.get("error", {}).get("message")
                or parsed_error.get("message")
                or details
            )
        except json.JSONDecodeError:
            pass
        return JsonResponse(
            {
                "reply": "Не удалось получить ответ от AI-сервиса.",
                "details": details,
            },
            status=502,
        )
    except Exception as error:
        return JsonResponse(
            {
                "reply": "Ошибка подключения к AI-сервису.",
                "details": str(error),
            },
            status=502,
        )

    reply = (
        groq_data.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "Не удалось сформировать ответ.")
        .strip()
    )

    return JsonResponse({"reply": reply})

def blog_view(request):
    return render(request, "blog.html")

def practice3_view(request):
    return render(request, "practice3.html")

def submit_request(request):
    if request.method == "POST":
        title = request.POST.get("title")
        customer_name = request.POST.get("customer_name")
        device_type = request.POST.get("device_type")
        problem_description = request.POST.get("problem_description")
        service_action = request.POST.get("service_action")
        
        prices = {
            "diagnostics": 5000.00,
            "replacement": 8000.00,
            "os_install": 6000.00,
            "other": 0.00
        }
        estimated_price = prices.get(service_action, 0.00)

        action_names = {
            "diagnostics": "Очистка и диагностика",
            "replacement": "Замена комплектующих",
            "os_install": "Установка ОС и программ",
            "other": "Другое"
        }
        action_name = action_names.get(service_action, "Другое")
        
        if title and customer_name and device_type and problem_description:
            full_description = f"[{action_name}] {problem_description}"
            ServiceRequest.objects.create(
                title=title,
                customer_name=customer_name,
                device_type=device_type,
                problem_description=full_description,
                estimated_price=estimated_price
            )
            messages.success(request, "Ваша заявка успешно отправлена и добавлена в базу данных!")
        else:
            messages.error(request, "Пожалуйста, заполните все поля формы.")
            
    return redirect('home')

def service_request_list(request):
    requests = ServiceRequest.objects.all()
    return render(request, "accounts/service_requests.html", {"service_requests": requests})


def service_request_detail(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    return render(
        request,
        "accounts/service_request_detail.html",
        {"service_request": service_request},
    )


def register_view(request):
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно.")
            return redirect("profile")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = LoginForm


def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect("home")


@login_required
def profile_view(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileAvatarForm(request.POST, request.FILES)
        if form.is_valid():
            profile.avatar = form.cleaned_data["avatar"]
            profile.save()
            messages.success(request, "Фото профиля обновлено.")
            return redirect("profile")
    else:
        form = ProfileAvatarForm()

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
            "profile": profile,
        },
    )
