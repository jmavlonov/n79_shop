from django.shortcuts import render,redirect
from users.forms import LoginForm, RegistrationUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('app:home')
            else:
                messages.error(request, 'Username yoki parol noto‘g‘ri')

    else:
        form = LoginForm()
    return render(request,'users/login.html')



def register_view(request):
    if request.method == 'POST':
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user.set_password(form.cleaned_data['password'])
            # user.save()
            login(request, user)
            messages.success(request, 'Ro‘yxatdan muvaffaqiyatli o‘tdingiz')
            return redirect('app:home')
    else:
        form = RegistrationUserForm()
    return render(request, 'users/register.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.success(request, 'Tizimdan muvaffaqiyatli chiqdingiz')
    return redirect('app:home')
    
