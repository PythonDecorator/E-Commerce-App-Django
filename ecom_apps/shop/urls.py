"""
URL mappings for the shop views.
"""

from django.urls import path
from ecom_apps.shop import views

app_name = "shop"

urlpatterns = [
    path("", views.index, name="index"),
    path("checkout/", views.checkout, name="checkout"),
    # path("detail/<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("delete/<int:pk>/", views.DeleteView.as_view(), name="delete"),
]
