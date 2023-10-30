"""
URL mappings for the user views.
"""

from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from ecom_apps.user.views import register, login_view, ProfileDetailView, ProfileUpdateView

app_name = "user"

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', login_view, name="login"),
    path("logout/", login_required(LogoutView.as_view(template_name="authentication/logout.html")), name="logout"),
    path('profile/<str:email>/', login_required(ProfileDetailView.as_view()), name='profile'),
    path('profile/<str:email>/update/', login_required(ProfileUpdateView.as_view()), name='profile-update'),
]
