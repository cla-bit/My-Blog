from django import template
from ..models import Post


register = template.Library()


@register.simple_tag()
def total_posts():
    count = Post.published.count()
    return count


'''
Each module that contains template tags needs to define a variable called register to be a valid tag 
library. This variable is an instance of template.Library, and it’s used to register the template tags 
and filters of the application.

In the preceding code, I have defined a tag called total_posts with a simple Python function. I 
have added the @register.simple_tag decorator to the function, to register it as a simple tag. Django 
will use the function’s name as the tag name. If you want to register it using a different name, you can 
do so by specifying a name attribute, such as  @register.simple_tag(name='my_tag').
'''


@register.inclusion_tag('trend.html')
def trend(count=1):
    context = {}
    trending = Post.published.filter(is_trending=True).order_by('-date_published')[:count]
    context['trending'] = trending
    return context


@register.inclusion_tag('recent.html')
def recent(count=2):
    context = {}
    recent_blog = Post.published.filter(is_recent=True).order_by('-date_published')[:count]
    context['recent'] = recent_blog
    return context

