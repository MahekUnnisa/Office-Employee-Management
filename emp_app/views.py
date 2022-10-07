from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Employee
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request, 'index.html')
# all theemployees
def manage(request):
    if  not request.user.is_authenticated:
        return HttpResponse('Login required')
    else:
        return render(request,'manage.html')
        
def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST.get('loginusername', False)
        loginpassword = request.POST.get('loginpassword', False)

        user = authenticate(username = loginusername, password = loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request, "Successfully logged in")
            return redirect('/')
        else:
            messages.success(request, 'Invalid Credentials, please try again')
            return redirect('/')
    return HttpResponse('404 - Not Found')

def handleRegister(request):
    if request.method=='POST':
        
        username = request.POST.get('username', False)
        fname  = request.POST.get('fname', False)
        lname  = request.POST.get('lname',False)
        email  = request.POST.get('email',False)
        pass1  = request.POST.get('pass1',False)
        pass2  = request.POST.get('pass2',False)
        # Create the user
        # get the post parameter
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('/')
        if pass1 != pass2:
            messages.error(request,"Passwords do not match")
            return redirect('/')
        if not username.isalnum():
            messages.error(request,"Username should only contain letters and numbers")
            return redirect('/')
        # myuser = User(email=email, username = username, password=pass1)
        myuser = User.objects.create_user(username=username,email=email,password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "You are registered successfully") 
        return redirect('/')
    else:
        return HttpResponse('404 - Not Found')



def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')
        
def viewallemployees(request):
    emps = Employee.objects.all()
    context = {
        'emps' : emps
    }
    return render(request,'viewallemployees.html', context)

def addanemployee(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        role = int(request.POST['role'])
        dept = int(request.POST['dept'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        new_emp = Employee(first_name = first_name, last_name = last_name, salary = salary, bonus = bonus, phone=phone, dept_id = dept, role_id = role)
        new_emp.save()
        return HttpResponse("employee added successfully",'addanemployee.html')

    elif request.method == 'GET':
        return render(request,'addanemployee.html')
    else:
        return HttpResponse("An Exception Occured Employee has not been added")

def removeanemployee(request, emp_id = 0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id = emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee removed successfully")
        except:
            return HttpResponse("Please enter a valid emp_id")
    emps = Employee.objects.all()
    context = {
        'emps':emps
    }
    return render(request,'removeanemployee.html',context)

def filterallemployees(request):
    if request.method=='POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps  = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains = dept)
        if role:
            emps = emps.filter(role__name__icontains = role)

        context = {
            'emps':emps
        }
        return render(request, 'viewallemployees.html', context)
    elif request.method == 'GET':
        return render(request, 'filterallemployees.html')
    else:
        return HttpResponse('An error occured')
