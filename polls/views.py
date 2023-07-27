from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Question,Choice
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def loginPage(request):
    page= 'login'
    if request.method=='POST':
        username = request.POST['unsername']
        password = request.POST['password']

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('polls:index')
        else:
            return redirect('polls:login')

    return render(request, 'login_register.html', {'page':page})

def logoutPage(request):
    logout(request)
    return redirect('polls:login')

def registrationPage(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user = authenticate(request, username=user.username,password=request.POST['password1'])

            if user is not None:
                login(request,user)
                return redirect('polls:index')

    context={'form':form, 'page':page}
    return render(request, 'login_register.html', context)

@login_required(login_url='polls:login')
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:3]
    context = {'latest_question_list': latest_question_list}
    return render(request, "index.html", context)

@login_required(login_url='polls:login')
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'detail.html', {'question': question})

@login_required(login_url='polls:login')
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question': question})

@login_required(login_url='polls:login')
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(
        pk=request.POST['choice']
        )
    except (KeyError, Choice.DoesNotExist):
    # Redisplay the question voting form
        return render(request, 'detail.html', {'question': question,'error_message': "You didn't select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
    # Always return an HttpResponseRedirect after successfully
    # dealing with POST data. This prevents data from being
    # posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:results', args=(question_id,))
)
