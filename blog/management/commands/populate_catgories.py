from blog.models import Category
from django.core.management.base import BaseCommand


    
class Command(BaseCommand):
    help = "This command inserts category data"
    
    def handle(self, *args, **options):
        
        #deleting existing data
        Category.objects.all().delete()
        # Titles for the blog posts
        categories = ['Sports','Technology','Science','Art','Food']
        
        
        for category in (categories):
            Category.objects.create(name =category)
        self.stdout.write(self.style.SUCCESS("completed inserting data!"))
          