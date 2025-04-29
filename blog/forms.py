from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from blog.models import Category, Post


class Contactform(forms.Form):
    name = forms.CharField(label="Name", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    message = forms.CharField(label="Message", required=True)
    
    
class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="Username", max_length=100, required=True)
    email = forms.EmailField(label="Email", max_length=100, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    confirm_pass = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_pass = cleaned_data.get("confirm_pass")

        if password and confirm_pass and password != confirm_pass:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data     

    
class Loginform(forms.Form):
    username = forms.CharField(label='username',max_length=100, required=True)
    password = forms.CharField(label='password',max_length=100, required=True)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username,password=password)
            if user is None:
                    raise forms.ValidationError("Invalid Username and Password ")
        
        
class Forgotpassword(forms.Form):
    email = forms.EmailField(label='Email', max_length=254, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user registered with this email.")
        return email
    
    
class ResetpasswordForm(forms.Form):
    new_password = forms.CharField(label="New Password", min_length=8)
    confirm_password = forms.CharField(label="Confirm Password", min_length=8)
    
    def clean(self):
        
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        
class NewpostForm(forms.ModelForm):
    title = forms.CharField(label='Title',max_length=200, required=True)
    content = forms.CharField(label='Content', required=True)
    category = forms.ModelChoiceField(label='Category',required=True, queryset=Category.objects.all())
    image_url = forms.ImageField(label="Image",required=False)
    
    class Meta:
        model = Post
        fields = ['title','content','category','image_url']
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        
        #custom validatoion
        if title and len(title) < 5:
            raise forms.ValidationError('Title must be atleast 5 characters')
        
        if content and len(content) < 10:
            raise forms.ValidationError('Content must be atleast 10 characters')
        
    def save(self, commit = ...):
        
        post = super().save(commit=False)
        cleaned_data = super().clean()
        
        if cleaned_data.get('image_url'):
            post.image_url = cleaned_data.get('image_url')
        
        else:
            img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/300px-No_image_available.svg.png"
            post.image_url = img_url
            
        if commit:
            post.save()
            
        return post
        
    