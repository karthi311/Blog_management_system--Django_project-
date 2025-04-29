from blog.models import Post,Category
from django.core.management.base import BaseCommand
import random

    
class Command(BaseCommand):
    help = "This command inserts post data"
    
    def handle(self, *args, **options):
        
        #deleting existing data
        Post.objects.all().delete()
        # Titles for the blog posts
        titles = [
            "The Rise of Artificial Intelligence in Everyday Life",
            "10 Easy Tips for Healthy Eating",
            "The History of the Internet: From ARPANET to Web 3.0",
            "How to Start a Small Business from Scratch",
            "Exploring the World’s Most Stunning Natural Wonders",
            "The Benefits of Practicing Mindfulness Daily",
            "Top 5 Books Every Aspiring Leader Should Read",
            "The Evolution of Social Media: Connecting a Global Audience",
            "DIY Projects to Beautify Your Home on a Budget",
            "The Science Behind a Good Night’s Sleep",
            "Fitness for Beginners: Your Ultimate Guide to Getting Started",
            "A Traveler’s Guide to the Hidden Gems of Europe",
            "How to Stay Productive While Working from Home",
            "The Art of Brewing the Perfect Cup of Coffee",
            "Breaking Down Cryptocurrency for Beginners",
            "The Joy of Gardening: Tips for Growing Your First Plant",
            "5 Life Lessons We Can Learn from Nature",
            "The Future of Electric Vehicles: What to Expect",
            "Mastering the Art of Cooking: Essential Tips for Beginners",
            "The Power of Gratitude: How It Can Transform Your Life"
        ]

        # Content for the blog posts
        contents = [
            "Artificial Intelligence (AI) is transforming how we live, work, and interact. From virtual assistants like Siri and Alexa to advanced robotics, AI has become an integral part of our daily routines. In this post, we explore the growing impact of AI across industries.",
            "Healthy eating doesn't have to be complicated. Focus on whole, unprocessed foods, drink plenty of water, and avoid sugary snacks. Discover how small dietary changes can have a big impact on your overall health.",
            "The internet has come a long way since its inception as ARPANET in the 1960s. Learn how it evolved into the global network we rely on today and what Web 3.0 promises for the future. This post takes a deep dive into its fascinating history.",
            "Starting a small business can be daunting but rewarding. Begin with a solid business plan, focus on solving real-world problems, and remain persistent. This guide offers actionable tips for turning your dream into reality.",
            "Our planet is home to breathtaking natural wonders, from the Grand Canyon to the Northern Lights. In this post, we journey through some of the most awe-inspiring locations on Earth and what makes them unique.",
            "Mindfulness can improve mental clarity, reduce stress, and enhance overall well-being. Learn simple techniques to incorporate mindfulness into your daily routine and start experiencing its benefits today.",
            "Leadership is a skill that can be cultivated through knowledge and practice. This post highlights five influential books that provide timeless wisdom for aspiring leaders looking to make an impact.",
            "Social media platforms have revolutionized how we communicate and share information. This post examines the rise of platforms like Facebook, Instagram, and TikTok, and their role in shaping modern society.",
            "Transform your living space without breaking the bank! From upcycling furniture to creating wall art, this post offers creative DIY ideas to give your home a fresh look.",
            "Sleep is essential for physical and mental health, yet many struggle to get enough. Learn about the science of sleep, tips for improving sleep quality, and why it's so crucial for overall well-being.",
            "Embarking on a fitness journey can be intimidating, but it doesn’t have to be. This post provides a beginner-friendly guide to exercise, including tips on setting realistic goals and staying motivated.",
            "Beyond the popular tourist destinations, Europe is full of hidden gems waiting to be discovered. This post uncovers lesser-known spots that are rich in history, culture, and beauty.",
            "Remote work has become the new normal for many. This post shares strategies for staying productive, maintaining a work-life balance, and creating a comfortable home office.",
            "Coffee lovers know there’s more to a great cup than just brewing. This post explores different brewing techniques, the importance of fresh beans, and tips for achieving coffee perfection.",
            "Cryptocurrencies like Bitcoin and Ethereum are making headlines, but they can be confusing. This post explains the basics of cryptocurrency, blockchain technology, and how to get started safely.",
            "Gardening is a relaxing and rewarding hobby. Learn how to start with easy-to-grow plants, care for them properly, and enjoy the therapeutic benefits of nurturing greenery.",
            "Nature offers valuable lessons on patience, resilience, and adaptability. This post explores the wisdom we can gain by observing the natural world and applying it to our lives.",
            "Electric vehicles (EVs) are reshaping the automotive industry. Discover the latest trends in EV technology, sustainability benefits, and how they’re set to change transportation.",
            "Cooking can be intimidating, but it’s a skill anyone can learn. From basic knife skills to understanding flavors, this post equips beginners with the knowledge they need to cook with confidence.",
            "Gratitude has been scientifically proven to boost happiness and improve mental health. Learn simple ways to practice gratitude daily and experience its transformative effects."
        ]

        image_urls = [
             "https://picsum.photos/300/300",  # AI in everyday life
             "https://picsum.photos/300/300",  # Healthy eating
             "https://picsum.photos/300/300",  # Internet history
             "https://picsum.photos/300/300",  # Starting a business
             "https://picsum.photos/300/300",  # Stunning natural wonders
             "https://picsum.photos/300/300",  # Mindfulness
             "https://picsum.photos/300/300",  # Books for leaders
             "https://picsum.photos/300/300",  # Social media evolution
             "https://picsum.photos/300/300",  # DIY projects
             "https://picsum.photos/300/300",  # Sleep science
             "https://picsum.photos/300/300",  # Fitness for beginners
             "https://picsum.photos/300/300",  # Hidden gems of Europe
             "https://picsum.photos/300/300",  # Productivity from home
             "https://picsum.photos/300/300",  # Brewing coffee
             "https://picsum.photos/300/300",  # Cryptocurrency basics
             "https://picsum.photos/300/300",  # Gardening
             "https://picsum.photos/300/300",  # Life lessons from nature
             "https://picsum.photos/300/300",  # Electric vehicles
             "https://picsum.photos/300/300",  # Cooking tips
             "https://picsum.photos/300/300",  # Gratitude power
        ]
 
        categories = Category.objects.all()

        for title, content, image_url in zip(titles,contents,image_urls):
            category = random.choice(categories)
            Post.objects.create(title=title, content=content,image_url=image_url,category=category)
        self.stdout.write(self.style.SUCCESS("completed inserting data!"))
          