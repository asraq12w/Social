from django.contrib.auth import logout
from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from taggit.models import Tag

# Create your views here.


def log_out(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


def profile(request, user_id=None):
    if user_id:
        user = User.objects.prefetch_related('following', 'followers').get(id=user_id)
    else:
        user = request.user

    posts = Post.objects.filter(auther=user)
    saved_posts = Post.objects.filter(saves__in=[user])
    last_followers = user.followers.all()[:5]
    last_following = user.following.all()[:5]
    context = {
        'posts': posts,
        'saved_posts': saved_posts,
        'user': user,
        'last_followers': last_followers,
        'last_following': last_following,
    }
    return render(request, 'social/profile.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect('social:login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_user(request):
    user = request.user
    if request.method == "POST":
        form = EditUserForm(data=request.POST, instance=user, files=request.FILES)
        if form.is_valid():
            form.save(commit=False)
            return redirect('social:profile')
    else:
        form = EditUserForm(instance=user)
    return render(request, 'registration/edit_user.html', {'form': form})


@login_required()
def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = f" name:{cd['name']}\n phone:{cd['phone']}\n email:{cd['email']}\n\n {cd['message']}"
            send_mail(
                cd['subject'],
                message,
                'davodrashiworking@gmail.com',
                ['davod.q12w@gmail.com'],
                fail_silently=False
            )
            Ticket.objects.create(subject=cd['subject'], email=cd['email'], message=cd['message'], phone=cd['phone'],
                                  name=cd['name'],)
            return redirect('social:profile')
    else:
        form = TicketForm()
    return render(request, 'forms/ticket_form.html', {'form': form})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-create')

    context = {
        'post': post,
        'similar_posts': similar_posts
    }
    return render(request, 'social/post_detail.html', context)


def search_post(request):
    query = []
    posts_results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            ###
            results1 = Post.objects.annotate(similarity=TrigramSimilarity('tags__name', query)) \
                .filter(similarity__gt=0.1)
            ###
            results2 = Post.objects.annotate(similarity=TrigramSimilarity('caption', query)) \
                .filter(similarity__gt=0.1)
            posts_results_ = (results1 | results2).order_by('-similarity')
            for post in posts_results_:
                if post not in posts_results:
                    posts_results.append(post)

        context = {
            'query': query,
            'posts_results': posts_results,
        }
        return render(request, 'social/search_post.html', context)


def post_list(request, slug=None):
    tag = None
    posts = Post.objects.prefetch_related('auther').order_by('-total_likes')
    if slug:
        tag = get_object_or_404(Tag, slug=slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = []
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'social/list_ajax.html', {'posts': posts})
    context = {
        'posts': posts,
        'tag': tag,
    }
    return render(request, 'social/post_list.html', context)


# @login_required
# def add_comment(request, post_id):
#     if request.method == "POST":
#         post = get_object_or_404(Post, id=post_id)
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.auther = request.user.username
#             comment.save()
#             return redirect('social:post_detail', post_id)
#     else:
#         form = CommentForm()
#         context = {
#             'form': form,
#         }
#     return render(request, 'forms/add_comment.html', context)

@login_required
@require_POST
def add_comment(request):
    post_id = request.POST.get('post_id')
    post = Post.objects.get(id=post_id)
    text = request.POST.get('comment')
    if text:
        comment = Comment.objects.create(post=post, auther=request.user, text=text)
        comment.save()

        response_data = {
            'text': comment.text,
            'auther': comment.auther.username,
        }
        return JsonResponse(response_data)


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.auther = request.user
            post.save()
            form.save_m2m()
            return redirect('social:post_list')
    else:
        form = PostForm()
        context = {
            'form': form,
        }
    return render(request, 'forms/add_post.html', context)


@login_required()
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form.save_m2m()
            return redirect('social:post_detail', post_id)
    else:
        form = PostForm(instance=post)
        context = {
            'form': form,
        }
    return render(request, 'forms/add_post.html', context)


@login_required()
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.auther == request.user:
        post.delete()
    return redirect('social:profile')


@login_required
@require_POST
def like_post(request):
    post_id = request.POST.get('post_id')
    if post_id:
        post = Post.objects.get(id=post_id)
        user = request.user
        if user in post.likes.all():
            liked = False
            post.likes.remove(user)
        else:
            liked = True
            post.likes.add(user)

        post_likes_count = post.likes.count()
        response_data = {
            'liked': liked,
            'likes_count': post_likes_count
        }
    else:
        response_data = {
            'error': 'Invalid post id'
        }
    return JsonResponse(response_data)


@login_required
@require_POST
def save_post(request):
    post_id = request.POST.get('post_id')
    if post_id:
        post = Post.objects.get(id=post_id)
        user = request.user
        if user in post.saves.all():
            saved = False
            post.saves.remove(user)
        else:
            saved = True
            post.saves.add(user)

        response_data = {
            'saved': saved,
        }
    else:
        response_data = {
            'error': 'Invalid post id',
        }
    return JsonResponse(response_data)


@login_required
@require_POST
def follow_user(request):
    user_id = request.POST.get('user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            if request.user in user.followers.all():
                Contact.objects.get(user_from=request.user, user_to=user).delete()
                follow = False
            else:
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                follow = True
            followers_count = user.followers.count()
            following_count = user.following.count()
            return JsonResponse({'followers': followers_count, 'following': following_count, 'follow': follow, })
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'})
    else:
        return JsonResponse({'error': 'user not found'})


def followers_list(request, id):
    user = User.objects.get(id=id)
    return render(request, 'social/followers_list.html', {'user': user})


