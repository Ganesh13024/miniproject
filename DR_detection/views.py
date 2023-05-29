from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .models import Datas
from django.contrib import messages
from DR_detection.forms import DatasetForm
from DR_detection.functions.function import handle_file_upload,send_email_da
from DR_detection.project.DeepRetinopathy.retinopathy2 import predection
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags 
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa   

ss,mailid,uname=[None,None,None]
def home(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        address = request.POST['address']
        contact= request.POST['contact']
        mail = request.POST['mail']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        errors = []
        if not name:
            errors.append('Name is required.')
        if not age:
            errors.append('Age is required.')
        elif not age.isdigit():
            errors.append('Age must be a number.')
        elif int(age) < 18 or int(age) > 99:
            errors.append('Age must be between 18 and 99.')
        if not address:
            errors.append('Address is required.')
        if not contact:
            errors.append('Contact is required.')
        if not mail:
            errors.append('Email is required.')
        if not password:
            errors.append('Password is required.')
        if password != cpassword:
            errors.append('Passwords do not match.')
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'home.html')
        messages.success(request, 'Registration successful!')
        obj = Datas()
        obj.Name = name
        obj.Age = age
        obj.Address = address
        obj.Contact = contact
        obj.Mail = mail
        obj.Password = password
        obj.Cpassword = cpassword
        obj.save()
        return render(request, 'login.html')
    return render(request, 'home.html')

def login(request):
    # messages.clear()  
    return render(request,'login.html')

def main(request):
    global uname,mailid
    if request.method == 'POST':
        
        uname = request.POST['uname']
        password = request.POST['password']
        mydata = Datas.objects.all()
        for data in mydata:
            if (uname == data.Name and password == data.Password):
                
                mailid = data.Mail
                gk = DatasetForm()
                return render(request,'main.html',{'forms':gk})  
    return render(request,'login.html')

def fileupload(request):
    global ss
    if request.method == 'POST':  
        f = DatasetForm(request.POST, request.FILES) 
        if f.is_valid():  
            handle_file_upload(request.FILES['file1'])
            
            ss = predection()
            return render(request,"temp.html",{'output':ss}) 
    return render(request,"main.html")

def moveon(request):
    return redirect('home')

def moveback(request):
    return render(request, "login.html")

def send_email(request):
    template = get_template('email_template.html')
    print(uname,ss)
    context = {'uname':uname,'result':ss}
    rendered_template = template.render(context)
    pdf = HttpResponse(content_type='application/pdf')
    pdf['Content-Disposition'] = 'attachment; filename="report.pdf"'
    pisa.CreatePDF(
        rendered_template,
        dest=pdf,
        encoding='utf-8'
    )
    return pdf
    return render(request, 'temp.html',{'msg1':'Successfully created report'})