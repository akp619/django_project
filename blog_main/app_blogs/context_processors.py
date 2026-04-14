from .models import Category, SocialLinks



"""

    # context_processors is used to create a generic method which will provide data to every page
    
    # In this project scenerio "navbar categories" we need to render each time and for every page shows the same details. So, instead of
    # passing "categories = Category.objects.all()" we define a generic method "get_categories()" which will call by default a page loads

"""
def get_categories(request):
    categories = Category.objects.all()
    return dict(categories=categories)


def get_social_links(request):
    social_links = SocialLinks.objects.all()
    return dict(social_links=social_links)