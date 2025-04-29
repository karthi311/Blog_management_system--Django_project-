# myapp/management/commands/update_slugs.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Post

class Command(BaseCommand):
    help = 'Update slugs for posts to ensure uniqueness'

    def handle(self, *args, **kwargs):
        for post in Post.objects.all():
            post.slug = slugify(post.title)[:50]  # Ensure slug is within 50 characters
            post.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated slugs'))
