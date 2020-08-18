from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, View
from django.core.mail import send_mail
from .decorator import unauthenticated_user
from .form import *
from django.contrib import messages
# Create your views here.

@unauthenticated_user
def user_Registration(request):
    if request.method == 'POST':
        next = QueryDict(request.META['QUERY_STRING']).get('next') or '/user_login'
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(next)
        else:
            return render(request, 'registration.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {'form': form})

@unauthenticated_user
def user_Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            next = QueryDict(request.META['QUERY_STRING']).get('next') or '/user_login'
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None and user.is_client and user.is_active:
                login(request, user)
                request.session['client'] = {'email': email}
                messages.success(request, 'Successfully Login')
                return HttpResponseRedirect(next)
            else:
                messages.error(request, 'Invalid Credentials')
        else:
            messages.error(request, 'Invalid Credentials')
    return render(request, 'login.html')

@login_required(login_url='user_login')
def user_logout(request):
    next = QueryDict(request.META['QUERY_STRING']).get('next') or '/user_login'
    if 'client' in request.session:
        request.session['client'] = ''
        del request.session['client']
    logout(request)
    return HttpResponseRedirect(next)

@method_decorator(login_required(login_url='/user_login'),name='dispatch')
class Request_view(ListView):
    model = Request_Table
    template_name = 'request_view.html'

@login_required(login_url='assignment:user_login')
def delete_request(request,pk):
    try:
        obj = Request_Table.objects.get(pk=pk)
        obj.delete()
    except Request_Table.DoesNotExist:
        raise ValidationError('No Record Found')
    return redirect('assignment:request')

@login_required(login_url='assignment:user_login')
def create_request(request):
    next = QueryDict(request.META['QUERY_STRING']).get('next') or '/user_login'
    if request.method=='POST':
        form = requestCreate(request.POST)
        code = form.data.get('code')
        mob = form.data.get('mobile')
        Request_Table.mobile = code+mob
        print(Request_Table.mobile)
        if form.is_valid():
            print(form.data)
            form.save(commit=False)
            Request_Table.mobile = code + mob
            Request_Table.user = request.user
            form.save()
            return redirect(next)
        else:
            return render(request,'request_create.html',{'form':form})
    else:
        form = requestCreate()
        return render(request,'request_create.html',{'form':form})

@login_required(login_url='assignment:user_login')
def update_request(request,pk):
    next = QueryDict(request.META['QUERY_STRING']).get('next') or '/user_login'
    data = Request_Table.objects.get(pk=pk)
    if request.method=='POST':
        form = requestUpdate(request.POST,instance=data)
        if form.is_valid():
            form.save(commit=False)
            Request_Table.user = request.user
            form.save()
            return HttpResponseRedirect(next)
    form = requestUpdate(instance=data)
    return render(request,'request_update.html',{'form':form,'object':data})

@method_decorator(login_required(login_url='/user_login'),name='dispatch')
class Detail_request(DetailView):
    model = Request_Table
    template_name = 'request_detail.html'


def forgetpassword(request):
    if request.method=='POST':
        email = request.POST['email']
        try:
            urs = User.objects.get(email=email)
            send_mail('Password Change','',settings.EMAIL_BACKEND,[urs],html_message=f'<h3>Click this link to change your password : <a href="http://127.0.0.1:8000/forgetPasswordPage?email={email}">Change Password Page</a></h3>')
            messages.success(request,'Password Change Link is share in your email')
            return redirect('assignment:user_login')
        except User.DoesNotExist:
            messages.error(request,'Email is not registered')
            return render(request,'forgetpassword.html')
    return render(request,'forgetpassword.html')


def forgetPasswordPage(request):
    email = request.GET.get('email')
    if request.method == 'POST':
        emailps = request.POST.get('emailps')
        changedone = True
        try:
            us = User.objects.get(email__iexact=emailps)
        except User.DoesNotExist:
            changedone = False
        if changedone == True:
            us.set_password(request.POST.get('password2'))
            us.save()
            messages.success(request, "Password Change Successfully. Now You Can login Using New Credentials")
        else:
            messages.error(request, 'Fail to Change Password')
        return redirect('assignment:user_login')
    return render(request, 'forgetchangepassword.html', {'email': email})
