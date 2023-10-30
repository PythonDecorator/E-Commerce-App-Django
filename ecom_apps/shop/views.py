"""
Shop Views
"""
from django.shortcuts import render
# from django.views import generic

from core.models import Product, Order
# from .forms import CreateProductForm


def index(request):
    """Home page view."""
    new = Product.objects.order_by("-id")[:7]
    featured = Product.objects.order_by("-id")[5:]
    bestseller = Product.objects.order_by("-rating")[:7]
    context = {"new": new,
               "featured": featured,
               "bestseller": bestseller,
               }

    return render(request, "home/index.html", context)


def checkout(request):
    """Checkout page view."""
    if request.method == "POST":
        items = request.POST.get('items', '')
        name = request.POST.get('name', "")
        email = request.POST.get('email', "")
        address = request.POST.get('address', "")
        city = request.POST.get('city', "")
        state = request.POST.get('state', "")
        zipcode = request.POST.get('zipcode', "")
        total = request.POST.get('total', "")
        order = Order(items=items, name=name, email=email, address=address,
                      city=city, state=state, zipcode=zipcode, total=total)
        order.save()

    return render(request, 'home/checkout.html')


# class CreateView(generic.CreateView):
#     """View for creating a food menu selected."""
#     model = Order
#     template_name = "checkout.html"
#     fields = ["name", "description", "time_minutes", "price", "link"]
#
#     def form_valid(self, form):
#         """Validate creating a new menu."""
#         form.instance.user = self.request.user
#
#         return super().form_valid(form)


# class DetailView(generic.DetailView):
#     """View for the food menu selected."""
#     model = Menu
#     template_name = "menu_detail.html"
