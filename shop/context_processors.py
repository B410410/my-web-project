from .models import Category

def category_list(request): 
    categories = Category.objects.all()
    # for category in categories: 
    #     print(f"Category ID: {category.id}, Name: {category.name}")
    return {'categories': categories}
