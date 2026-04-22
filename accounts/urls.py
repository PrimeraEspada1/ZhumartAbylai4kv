from django.urls import path

from .views import (
    UserLoginView,
    home,
    logout_view,
    profile_view,
    register_view,
    service_request_detail,
    service_request_list,
    blog_view,
    practice3_view,
    submit_request,
    chatbot_view,
)


urlpatterns = [
    path("", home, name="home"),
    path("blog/", blog_view, name="blog"),
    path("practice3/", practice3_view, name="practice3"),
    path("submit-request/", submit_request, name="submit_request"),
    path("chatbot/", chatbot_view, name="chatbot"),
    path("register/", register_view, name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("requests/", service_request_list, name="service_requests"),
    path("requests/<int:request_id>/", service_request_detail, name="service_request_detail"),
]
