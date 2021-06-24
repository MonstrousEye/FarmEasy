from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Contact
from django.conf import settings
from django.core import mail
from django.core.mail.message import EmailMessage



# Create your views here.
def index(request):

    return render(request,'index.html')


def handleSignup(request):
    if request.method == 'POST':

        # TAKE THE PARAMETERS FROM THE POP UP FORM
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if len(fname)<2 or len(email)<3 or len(username)<5:
            messages.error(request,"  please fill the valid details") 


        if len(username)>15:
            messages.error(request,"username should be less than 15 characters")
            return redirect('/')

        

        if User.objects.filter(username=username).exists():
            messages.error(request,"username already taken")
            return redirect('/')


          
       
        if User.objects.filter(email=email).exists():
            messages.error(request,"email already taken")
            return redirect('/')


            

        if not username.isalnum():
            messages.error(request,"username should contain only letters and there should be no space")
            return redirect('/')

        if pass1 != pass2:
            messages.error(request,"invali passoword")
            return redirect('/')


           
            
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Successfully Signed  In")
        return redirect('/')
        
 
def handleLogin(request):

    if request.method == "POST":

        # GET PARAMETERS
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user=authenticate(username=loginusername,password=loginpassword)
        if user is not None:

            login(request,user)
            messages.success(request,"Successfully Logged In")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials")
           
            return redirect('/')




def contact(request):
    if not request.user.is_authenticated:
             messages.error(request,"Please login")
             return render(request,'index.html') 
    if  request.method == "POST": 
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        pin=request.POST.get('pin')
        desc=request.POST.get('desc')
        files=request.FILES.get('files')
        from_email=settings.EMAIL_HOST_USER

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(desc)<5 or len(address)<20 or len(pin)<6:
            messages.error(request,"  please fill the valid details")

        

        else:
            connection=mail.get_connection()
            connection.open()
            emaill=mail.EmailMessage(name  ,desc + "\n email adress of user:"+ email + "\n Phone : " + phone ,from_email,['manjunathgowda7826@gmail.com'],connection=connection)
            connection.send_messages([emaill])
            connection.close()
            contact=Contact(name=name,email=email,phone=phone,address=address,pin=pin,desc=desc,files=files)
            contact.save()
            messages.success(request,"Your Message Has Been Recorded")
            messages.success(request,"Your Problems Will be Verified And We Will Contact You Shortly")     


    return render(request,'contact.html') 


def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('/')


def about(request):
        if not request.user.is_authenticated:
             messages.error(request,"Please login")
             return render(request,'index.html') 

        else:

            return render(request,'about.html') 




def blog(request):
        
        if not request.user.is_authenticated:
             messages.error(request,"Please login")
             return render(request,'index.html') 

        else:
            allPosts=Contact.objects.all()
            context={'allPosts':allPosts}
        return render(request,'blog.html',context) 


def search(request):

    query=request.GET['search']

    if not request.user.is_authenticated:
             messages.error(request,"Please login")
             return render(request,'index.html') 

    if len(query)>78:
        allPosts=Contact.objects.none()

    else:
         allPostsTitle=Contact.objects.filter(name__icontains=query)
         allPostsContent=Contact.objects.filter(desc__icontains=query)
         allPostsAuthor=Contact.objects.filter(phone__icontains=query)
         allPosts=allPostsTitle.union(allPostsContent,allPostsAuthor)    

    if allPosts.count() == 0:
        messages.warning(request,"No Search Results")

    params={'allPosts':allPosts,'query':query}
    return render(request,'search.html',params)
 
 
