from django.urls import path
from .views import home, post_detail, post_share, post_comment, get_post_comments

app_name = 'blog'

urlpatterns = [
    path('', home, name='home'),
    path('tag/<slug:tag_slug>/', home, name='post_tag'),
    path('article/<int:year>/<int:month>/<int:day>/<int:pk>/<slug:slug>/', post_detail, name='post_detail'),
    path('article/<int:post_id>/share/', post_share, name='share'),
    path('article/<int:post_id>/comment/', post_comment, name='comment'),
    path('article/<int:post_id>/comments', get_post_comments, name='comments'),
]
