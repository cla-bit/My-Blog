from django.db.models import Count
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailShareForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.views.decorators.http import require_POST

# Create your views here.


def home(request, tag_slug=None):
    context = {}
    post_link = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, tag=tag_slug)
        post_link = post_link.filter(tags__in=[tag])
    # pagination for load more
    paginator = Paginator(post_link, 2)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    context['posts'] = posts
    context['tag'] = tag
    return render(request, 'posts.html', context)


def post_detail(request, year, month, day, pk, slug):
    context = {}
    comment_form = CommentForm()
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             date_published__year=year,
                             date_published__month=month,
                             date_published__day=day,
                             id=pk,
                             blog_slug_title=slug,)
    # similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_post = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags', '-date_published')[:5]
    comments = post.comment_posts.filter(active=True)

    context['post'] = post
    context['comments'] = comments
    context['comment_form'] = comment_form
    context['similar'] = similar_post
    return render(request, 'post-detail.html', context)


def post_share(request, post_id):
    context = {}
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    share_form = EmailShareForm()
    sent = False
    if request.method == "POST":
        share_form = EmailShareForm(request.POST)
        if share_form.is_valid():
            share_form_bound = share_form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())  # getting a post url from the detail page
            subject = f"{share_form_bound['name']} recommends you read {post.blog_title}"
            message = f"Read {post.blog_title} at {post_url}\n\n {share_form_bound['name']}'s comments: {share_form_bound['comments']}"
            send_mail(
                subject=subject,
                message=message,
                from_email='admin@glog.com',
                recipient_list=[share_form_bound['to_receiver']],
                fail_silently=False
            )
            sent = True
        else:
            share_form = EmailShareForm()

    context["post"] = post
    context['sent'] = sent
    context['share_form'] = share_form
    return render(request, "share.html", context)


@require_POST
def post_comment(request, post_id):
    context = {}
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    """
    When not using if request.method == POST, i am using @require_POST,
    comment is set to None which means no comment has been donw,
    comment_form is receiving a comment
    """
    comment = None
    comment_form = CommentForm(data=request.POST, files=request.FILES)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)  # Create a Comment object without saving it to the database
        '''
        comment is my object it has the post, name, body and user image and some others,
        this is gotten from the comment_form.save which i commit is False
        '''
        comment.post = post  # i am assigning the post commented on to the exact comment made on it
        comment.save()  # now i am saving the comment to database

    context['comment_form'] = comment_form
    context['post'] = post
    context['comment'] = comment
    return render(request, 'comment.html', context)


def get_post_comments(request, post_id):
    context = {}
    post = get_list_or_404(Comment, post=post_id, active=True)
    context['posts'] = post
    return render(request, 'post_comments.html', context)
