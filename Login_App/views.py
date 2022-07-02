from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import UserCreateForm, UserUpdateForm, ProfilePicture, PasswordCheck
from django.contrib.auth.models import User
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import check_password


def register(request):

    form = UserCreateForm()
    registered = False
    if request.method == 'POST':
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True
    data = {'form': form, 'registered': registered}
    return render(request, 'Login_App/register.html', context=data)


def user_login(request):

    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    data = {'form': form}
    return render(request, 'Login_App/login.html', context=data)


@login_required
def user_logout(request):

    logout(request)
    return HttpResponseRedirect(reverse('Login_App:user_login'))


@login_required
def user_profile(request):

    return render(request, 'Login_App/profile.html', context={})


@login_required
def user_info_update(request):

    form = UserUpdateForm(instance=request.user)
    if request.method == 'POST':
        form = UserUpdateForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('Login_App:user_profile'))
    data = {'form': form}
    return render(request, 'Login_App/user_info_update.html', context=data)


@login_required
def user_password_change(request):

    user = request.user
    form = PasswordChangeForm(user=user)
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('Login_App:user_login'))
    data = {'form': form}
    return render(request, 'Login_App/user_password_change.html', context=data)


@login_required
def add_profile_picture(request):

    form = ProfilePicture()
    data = {'form': form}
    if request.method == 'POST':
        form = ProfilePicture(request.POST, request.FILES)
        if form.is_valid():
            pic = form.save(commit=False)
            pic.user = request.user
            pic.save()
            return HttpResponseRedirect(reverse('Login_App:user_profile'))
    return render(request, 'Login_App/change_picture.html', context=data)


@login_required
def change_picture(request):

    form = ProfilePicture(instance=request.user.user_profile)
    data = {'form': form}
    if request.method == 'POST':
        form = ProfilePicture(request.POST, request.FILES, instance=request.user.user_profile)
        if form.is_valid():
            pic = form.save(commit=False)
            pic.save()
            return HttpResponseRedirect(reverse('Login_App:user_profile'))

    return render(request, 'Login_App/change_picture.html', context=data)


@login_required
def public_user_info(request, user):

    user_to_display = User.objects.get(username=user)
    context = {'user_info': user_to_display}
    return render(request, 'Login_App/public_user_info.html', context)


@login_required()
def password_check(request):

    user_password = request.user.password
    form = PasswordCheck()
    if request.method == 'POST':
        form = PasswordCheck(data=request.POST)
        if form.is_valid():
            password_to_check = form.cleaned_data['password']
            if check_password(password_to_check, user_password):
                return HttpResponseRedirect(reverse('Login_App:user_delete', kwargs={'pk': request.user.pk}))
            else:
                error = True
                return render(request, 'Login_App/profile.html', context={'error': error})
    context = {'form': form}
    return render(request, 'Login_App/password_check.html', context)


class UserDelete(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'Login_App/user_delete.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('Login_App:register')
