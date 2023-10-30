"""
User views
"""

from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm, LoginForm, EditProfileForm
from core.models import User, Profile


def register(request):
    msg = None

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            authenticate(username=username, password=raw_password)

            msg = 'Your account was created successfully.'
            messages.success(request, msg)

            return redirect("user:login")

        else:
            msg = 'Form is not valid'
            messages.error(request, msg)
    else:
        form = SignUpForm()

    return render(request, "authentication/register.html", {"form": form, "msg": msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    context = {"form": form}

    if request.method == "POST":

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                msg = f'Hello {email}.'
                messages.success(request, msg)
                return redirect("shop:index")
        else:
            msg = 'Error validating the form'
            messages.error(request, msg)

    return render(request, "authentication/login.html", context)


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    """Views for the profile page."""
    model = User

    slug_url_kwarg = "email"
    slug_field = "email"
    template_name = "home/profile.html"
    context_object_name = "object"


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Views for the profile page."""
    model = Profile
    slug_url_kwarg = "email"
    slug_field = "email"

    form_class = EditProfileForm
    template_name = 'home/profile_update.html'

    def get_success_url(self):
        return reverse('user:profile', kwargs={'email': self.get_object().user.email})

    def get_object(self, **kwargs):
        """Get the object specific to the user."""
        email = self.kwargs.get("email")
        if email is None:
            raise Http404
        return get_object_or_404(Profile, user__email__iexact=email)

    def get_context_data(self, **kwargs):
        """Set the form values before rendering on the page"""
        context = super().get_context_data(**kwargs)
        profile = self.get_object()  # -> returns a customer object

        # accessing the user information on the profile
        data = {
            'country': profile.country,
            'address': profile.address,
            'state': profile.state,
        }

        form = self.form_class(initial=data, instance=profile.user)

        context['form'] = form  # -> updating the class view context dictionary
        return context
