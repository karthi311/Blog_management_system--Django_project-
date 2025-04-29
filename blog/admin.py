from django.contrib import admin
from .models import Post, Category, aboutus
# Register your models here.
class post_admin(admin.ModelAdmin):
    list_display = ('title','content')
    search_fields = ('title','content')
    list_filter = ('category','created_at')

admin.site.register(Post,post_admin)
admin.site.register(Category)
admin.site.register(aboutus)





