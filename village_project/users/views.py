from typing import ItemsView
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView, DetailView 
from django.urls import reverse
from users.forms import EmployeeForm, PanchayathForm, EndUserForm, NewsForm, SalaryForm,ComplaintForm
from users.models import Complaint, Employee, EndUser, Panchayath, News, Salary, Complaint
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q


class HomeView(TemplateView):
    template_name = 'home.html'


def index(request):
        current_user = request.user
        panchayath = None
        employee = None
        endusers = None
        # admin = None

        #check if current_user is panchayath

        try:
            panchayath = current_user.panchayath
        except:
            pass

        if panchayath:
        
            employees = Employee.objects.filter(panchayath_name= request.user.panchayath)
            endusers = EndUser.objects.filter(panchayath_name= request.user.panchayath)
            return render(request, 'index_panchayath.html', {'employees':employees,'endusers':endusers})

        #check if current_user is employee

        try:
            employee = current_user.employee
        except:
            pass

        if employee:
            print(request.user.employee.panchayath_name)
            endusers= EndUser.objects.filter(panchayath_name= request.user.employee.panchayath_name)
            return render(request,'index_employee.html', {'enduser': endusers})

         #check if current user is end user   
        try:
            endusers = current_user.enduser
        
        except:
            pass
        if endusers:
            return render(request, 'index_enduser.html')

        return redirect('users:home')

def employee_registrationview(request):
    register_url = reverse('users:employee_registration')
    if request.method=='POST':
        register_form =EmployeeForm(data= request.POST)

        if register_form.is_valid():
            register_form.cleaned_data.pop('confirm_password')
            item = Employee(**register_form.cleaned_data)
            item.panchayath_name = request.user.panchayath
            item.save()
            item.set_password(item.password)
            item.save()
            messages.success(request, 'successfully created an account')
            return redirect('users:index')
        else:
            return render(request, 'registration.html', {'register_form':register_form, 'register_url':register_url})
    
    else:
        register_form = EmployeeForm()
        return render(request, 'registration.html', {'register_form':register_form, 'register_url':register_url})


def panchayath_registrationview(request):
    register_url = reverse('users:panchayath_registration')
    if request.method=='POST':
        register_form =PanchayathForm(data= request.POST)

        if register_form.is_valid():
            register_form.cleaned_data.pop('confirm_password')
            item = register_form.save()
            item.set_password(item.password)
            item.save()
            messages.success(request, 'successfully created a pachayath account')
            return redirect('users:index')
        else:
            return render(request, 'registration.html', {'register_form':register_form, 'register_url':register_url})
    
    else:
        register_form = PanchayathForm()
        return render(request, 'registration.html', {'register_form':register_form, 'register_url':register_url})


def enduser_registrationview(request):
    register_url = reverse('users:enduser_registration')
    if request.method=='POST':
        register_form =EndUserForm(data= request.POST)

        if register_form.is_valid():
            register_form.cleaned_data.pop('confirm_password')
            item = register_form.save()
            item.set_password(item.password)
            item.save()
            messages.success(request, 'successfully created a enduser account')
            return redirect('users:index')
        else:
            return render(request, 'registration.html', {'register_form':register_form, 'register_url':register_url})
    
    else:
        register_form = EndUserForm()
        return render(request, 'registration.html', {'register_form':register_form, 'register_url':register_url})


def loginview(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
       
        if user:
            if user.is_active:
                
                login(request,user)
                return redirect('users:index')
            else:
                return HttpResponse(request, 'Your account is disabled')

        else:
            messages.error(request, 'Invalid login details')
            return render(request, 'login.html')

    else:
        return render(request, 'login.html')


@login_required
def logoutview(request):
    logout(request)

    return redirect('users:home')

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee_list.html'
    
    def get_queryset(self):
        current_user = self.request.user
        panchayath = current_user.panchayath
        return Employee.objects.filter(Q(panchayath_name=panchayath))

def AddNews(request):
    register_url = reverse('users:add_news')
    if request.method=='POST':
        register_form =NewsForm(data= request.POST)

        if register_form.is_valid():
            
            item = News(**register_form.cleaned_data)
            item.panchayath_name=request.user.panchayath
            item.save()
            messages.success(request, 'successfully created news')
            return redirect('users:index')
        else:
            return render(request, 'registration.html', {'register_form':register_form, 'register_url':register_url})
    
    else:
        register_form = NewsForm()
        return render(request, 'registration.html', {'register_form':register_form, 'register_url':register_url})

class ViewNews(ListView):
    model = News
    template_name = 'news_details.html'
    
    def get_queryset(self):
        current_user = self.request.user
        panchayath = current_user.panchayath
        return News.objects.filter(Q(panchayath_name =panchayath))

def salary_updation_view(request, employee_id):
    register_url = reverse('users:update_salary', kwargs={'employee_id':employee_id})
    employee = Employee.objects.get(id = employee_id)
    if  request.method == 'POST':
        register_form = SalaryForm(data=request.POST)
        if register_form.is_valid():
            item = Salary(**register_form.cleaned_data)
            item.panchayath_name = request.user.panchayath
            item.employee_name = employee
            item.save()
            return redirect('users:index')
        
        else:
            return render(request, 'registration.html', {'register_form':register_form, 'register_url':register_url})
    
    else:
        register_form = SalaryForm()
        return render(request, 'registration.html', {'register_form':register_form, 'register_url':register_url})


class SalaryDetailsView(DetailView):
    model = Salary
    template_name = 'salary_details.html'


class SalaryListView(ListView):
    model = Salary
    template_name = 'salary_list.html'
    
    def get_queryset(self):
        current_user = self.request.user
        employee = current_user.employee
        
        return Salary.objects.filter(employee_name=employee)

def register_complaint(request):
    register_url = reverse('users:complaint_registration')
    if request.method=='POST':
        register_form =ComplaintForm(data= request.POST)

        if register_form.is_valid():
            
            item = Complaint(**register_form.cleaned_data)
            item.panchayath_name=request.user.enduser.panchayath_name
            item.enduser = request.user.enduser
            item.save()
            messages.success(request, 'successfully created news')
            return redirect('users:index')
        else:
            return render(request, 'registration.html', {'register_form':register_form, 'register_url':register_url})
    
    else:
        register_form = ComplaintForm()
        return render(request, 'registration.html', {'register_form':register_form, 'register_url':register_url})


class ComplaintListView(ListView):
    model = Complaint
    template_name = 'complaint_list.html'

    def get_queryset(self):
        current_user =self.request.user
        
        try:
            if current_user.panchayath:
                panchayath =current_user.panchayath
        except:
            pass
        
        try:
            if current_user.employee:
                panchayath = current_user.employee.panchayath_name
        except:
            pass
        
        try:
            if current_user.enduser:
                panchayath =current_user.enduser.panchayath_name
        except:
            pass
        
        return Complaint.objects.filter(panchayath_name = panchayath, solved = False)

    
    def get_context_data(self,**kwargs):
        current_user = self.request.user
        try:
            if current_user.panchayath:
                panchayath =current_user.panchayath
        except:
            pass
        
        try:
            if current_user.employee:
                panchayath = current_user.employee.panchayath_name
        except:
            pass
        
        try:
            if current_user.enduser:
                panchayath =current_user.enduser.panchayath_name
        except:
            pass

        context = super(ComplaintListView,self).get_context_data(**kwargs)
        context['resolved_complaints'] = Complaint.objects.filter(panchayath_name=panchayath, solved=True)
        return context

class ComplaintDetailsView(DetailView):
    model = Complaint
    template_name = 'complaint_details.html'


def resolve_complaint(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    complaint.solved = True
    complaint.save()
    return HttpResponseRedirect(reverse('users:complaint_list'))

class EnduserProfileDetailsView(DetailView):
    model = EndUser
    template_name ='profile/enduser_profile.html'

class EmployeeProfileDetailsview(DetailView):
    model = Employee
    template_name ='profile/employee_profile.html'

class PanchayathProfileDetailsview(DetailView):
    model = Panchayath
    template_name ='profile/panchayath_profile.html'