from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash, logout
from django.views.generic import FormView, RedirectView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, ChangeUserData

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        user = form.instance
        login(self.request, user)
        messages.success(self.request, f'Account created for {username} successfully.')
        return super().form_valid(form)


    def form_invalid(self, form):
        for field in form.errors:
            for error in form.errors[field]:
                messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, 'Logged in successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)
    
    
    
class LogoutView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('user_login')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been logged out successfully!')
        return super().get(request, *args, **kwargs)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = ChangeUserData(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile information updated successfully.')
            return redirect('profile_views')
        else:
            for field in profile_form.errors:
                for error in profile_form.errors[field]:
                    messages.error(request, f"{field}: {error}")
    else:
        profile_form = ChangeUserData(instance=request.user)
    return render(request, 'update_profile.html', {'form': profile_form})


@login_required
def pass_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your password has been changed successfully.')
            update_session_auth_hash(request, form.user)
            return redirect('profile_views')
        else:
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})
