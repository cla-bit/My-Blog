from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import validate_image_file_extension
from taggit.managers import TaggableManager

# Create your models here.


class PublishedManager(models.Manager):  # my custom manager to retrieve all posts that are published
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status=Post.Status.PUBLISHED)


class DraftManager(models.Manager):  # my custom manager to retrieve all posts that are published
    def get_queryset(self):
        return super(DraftManager, self).get_queryset().filter(status=Post.Status.DRAFT)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    blog_title = models.CharField(null=True, blank=True, max_length=200)
    blog_slug_title = models.SlugField(unique=True, max_length=200, unique_for_date='date_published')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    blog_img = models.ImageField(upload_to='blog/post/%Y%m%d', blank=True, null=False, default='blog/post/default.jpg', validators=[validate_image_file_extension])
    is_recent = models.BooleanField(default=False)
    recent_img = models.ImageField(upload_to='blog/recent/%Y%m%d', blank=True, null=False, default='blog/recent/default.jpg', validators=[validate_image_file_extension])
    is_trending = models.BooleanField(default=False)
    trend_img = models.ImageField(upload_to='blog/trends/%Y%m%d', blank=True, null=False, default='blog/trends/default.jpg', validators=[validate_image_file_extension])
    body = models.TextField()
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    date_published = models.DateTimeField(default=now())
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    published = PublishedManager()  # my custom manager
    drafted = DraftManager()

    class Meta:
        ordering = ['-date_published']
        indexes = [
            models.Index(fields=['blog_title', 'blog_slug_title']),
            models.Index(fields=['body']),
            models.Index(fields=['status']),
            models.Index(fields=['date_published', 'date_created']),
        ]
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.blog_title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[
            self.date_published.year,
            self.date_published.month,
            self.date_published.day,
            self.pk,
            self.blog_slug_title
        ])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_posts')
    user_img = models.ImageField(upload_to='blog/comment/%Y%m%d',
                                 default='blog/comment/recent-commnet-img.jpg',
                                 blank=True, null=False, validators=[validate_image_file_extension])
    name = models.CharField(max_length=30, null=True)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
            models.Index(fields=['body']),
            models.Index(fields=['created', 'active'])
        ]
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'{self.name} comment on {self.post}'

