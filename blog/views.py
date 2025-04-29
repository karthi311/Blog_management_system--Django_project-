from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
import logging
from .models import Category, Post,aboutus
from django.core.paginator import Paginator
from .forms import Contactform, Forgotpassword, Loginform, NewpostForm, RegisterForm, ResetpasswordForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import Group


def index(request):
    blog_title = "Latest Posts"
    query = request.GET.get("q")
    #getting data from post model
    all_post = Post.objects.filter(is_published=True)
    
    if query:
        all_post = all_post.filter(title__icontains=query)
    # Debug: Print the filtered posts
        print("Filtered posts:", [post.title for post in all_post])
        
    #pagination
    paginator = Paginator(all_post, 5)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    
    return render(request,"blog/index.html", {'blog_title': blog_title, 'posts':page_object,'query':query})

def detail(request, slug):
    if  request.user and not request.user.has_perm('blog.view_post'):
        messages.error(request,"You have no permission to view any Posts")
        return redirect('blog:index')
        
    #getting static data
    #post = next((item for item in post if item['id'] == int(post_id)), None)
    
    try:
        #getting data by post id
        post = Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(category = post.category).exclude(pk=post.id)
        # print("printing post",post)
        # print("printing:",related_posts)
     
    except Post.DoesNotExist:
        raise Http404("Post Does Not Exist")
        
    # logger = logging.getLogger("testing")
    # logger.debug(f'post variable is {post}')
    return render(request, "blog/detail.html",{'post': post,'related_posts': related_posts})


def old_url_redirect(request):
    return redirect(reverse("blog:new_url_page"))

def new_url_view(request):
    return HttpResponse("This is the new url")

def contact(request):
    if request.method == "POST":
        form = Contactform(request.POST)
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        
        logger = logging.getLogger("testing")
        if form.is_valid():
            
            logger.debug(f'post data is {form.cleaned_data["name"]} {form.cleaned_data["email"]} {form.cleaned_data["message"]}')
            #send email or save in database
            success_message = 'Your Email Sent Successfully'
            return render(request, "blog/contact.html",{'form':form,'success':success_message})
            
                
        else:
                
                logger.debug("Form validation failure")
            
        return render(request, "blog/contact.html",{'form':form, 'name':name,'email':email,'message':message})    
    return render(request, "blog/contact.html")#,{'post': post,'related_posts': related_posts})
    
    
def about(request):
    about_content = aboutus.objects.first()
    if about_content is None or not about_content.content:
        about_content = 'Sorry there is no Content to Show'
    else:
        about_content = about_content.content       
        
    return render(request, "blog/about.html",{'content':about_content})
        

def register(request):
    if request.method == 'POST':
       
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Extract cleaned data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create the user
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password)  # Hash the password
            )
            
            user.save()
            # add user  to readers group
            readers_group,created = Group.objects.get_or_create(name="Readers")
            user.groups.add(readers_group)
            messages.success(request,"Registraiton Successfully Finished, You can Log-in")
            return redirect("blog:login")  # redirect to login page
        else:
            print("Form is invalid:", form.errors)
    else:
        form = RegisterForm()
      
    return render(request, "blog/register.html", {'form': form})   


def login(request):
    if request.method == 'POST':
        # Assuming Loginform is defined elsewhere
        form = Loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                auth_login(request,user)
                
                return redirect("blog:dashboard") #redirect to dashboard 
            
        else:
            print("Form errors:", form.errors)
            print("unsuccessful")
    else:
        print("form invalid")
        form = Loginform()
        print("GET request form:", form)
        
    # Ensure the context is a dictionary
    return render(request, "blog/login.html", {'form': form}) 


def dashboard(request):
    blog_title = 'My Posts'
    # getting user posts
    all_posts = Post.objects.filter(user=request.user)
    
    #pagination
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    
    return render(request, "blog/dashboard.html", {'blog_title': blog_title,'page_object':page_object}) 


def logout(request):
    auth_logout(request)
    return redirect("blog:index")

def forgotpassword(request):
    form = Forgotpassword()
    if request.method == "POST":
        # form for forgotpassword
        form = Forgotpassword(request.POST)
        
        if form.is_valid():
            
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            #sending email to reset password
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request) 
            domain = current_site.domain
            subject = "Reset Password Requested"
            message = render_to_string("blog/resetpasswordemail.html", {'domain':domain, 'uid':uid,'token':token})
            send_mail(subject,message, 'noreply@gmail.com',[email])
            messages.success(request,"Success mail has been sent")
            
            
                  
    return render(request, 'blog/forgotpassword.html',{'form':form})



def password_reset_confirm(request,uidb64,token):
    form = ResetpasswordForm()
    
    if request.method == 'POST':
        ## form
        form = ResetpasswordForm( request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except(TypeError,ValueError,OverflowError,User.DoesNotExist):
                user = None
                
            if user is not None and default_token_generator.check_token(user,token):
                user.set_password(new_password)
                user.save()
                messages.success(request,'Your password reset successfully')
                return redirect('blog:login')
            
            else:
                messages.error(request,'The password reset link is Invalid')
    
    return render(request,'blog/reset_password.html', {'form':form})
    
@login_required
@permission_required('blog.add_post', raise_exception=True)
def new_post(request):
    categories = Category.objects.all()
    form = NewpostForm()
    if request.method == 'POST':
        # form
        form = NewpostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('blog:dashboard')
    return render(request,'blog/new_post.html',{'categories':categories,'form': form}) 


@login_required
@permission_required('blog.change_post',raise_exception=True)
def edit_post(request, post_id):
    categories = Category.objects.all()
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = NewpostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save()
            if updated_post:  # Ensure save was successful
                messages.success(request, "Post updated successfully.")
                return redirect('blog:dashboard')  # Adjust redirect as needed
            else:
                messages.error(request, "An error occurred while saving the post.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = NewpostForm(instance=post)

    return render(request, 'blog/edit_post.html', {
        'categories': categories,
        'post': post,
        'form': form
    })

@login_required
@permission_required('blog.delete_post',raise_exception=True)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":  # Ensure deletion only happens on POST requests
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('blog:dashboard')  # Redirect to the dashboard URL
    else:
        # If the request method is GET, show a confirmation page (optional)
        return render(request, 'blog/dashboard.html', {'post': post})
    
    
@login_required
@permission_required('blog.can_publish',raise_exception=True)
def publish_post (request,post_id):
    post = get_object_or_404(Post, id=post_id)
    post.is_published = True
    post.save()
    messages.success(request,"Post Published successfully.")
    
    return redirect ('blog:dashboard')