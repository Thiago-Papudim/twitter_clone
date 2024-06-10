from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, ("O seu tweet foi postado!"))
                return redirect('home')

        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweets":tweets, "form":form})
    
    else:
        messages.success(request, ("Você precisa Logar!"))
        return render(request, 'login.html', {})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    
    else:
        messages.success(request, ("Você precisa estar logado para ver essa Página ..."))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")
        # Lógica do formulário de Postagem
        if request.method == "POST":
            # Pegar o Usuário
            current_user_profile = request.user.profile
            # Pegar os dados do Formulário
            action = request.POST['follow']
            # Decidir seguir ou deixar de seguir
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            
            elif action == "follow":
                current_user_profile.follows.add(profile)
            
            # Salvar o perfil
            current_user_profile.save()

        return render(request, "profile.html", {"profile":profile, "tweets":tweets})
    
    else:
        messages.success(request, ("Você precisa estar logado para ver essa Página ..."))
        return redirect('home')
    
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Você efetuou seu Login."))
            return redirect('home')
        else:
            messages.success(request, ("Aconteceu um erro, tente novamente ..."))
            return redirect('login')
    else:
        return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Você deslogou. Entre novamente."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
            # Logar o Usuário
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ("O usuário foi criado corretamente."))
            return redirect('home')
    return render(request, "register.html", {'form':form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        # Pegar formulários
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, ("Você atualizou seu perfil."))
            return redirect('home')     
        return render(request, "update_user.html", {'user_form':user_form, 'profile_form':profile_form})
    else:
        messages.success(request, ("Você tem que logar primeiro ..."))
        return redirect('home')
    
def tweet_like(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        return redirect('home')
    else:
        messages.success(request, ("Você tem que logar primeiro ..."))
        return redirect('home')