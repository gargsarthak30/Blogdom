from django.shortcuts import  HttpResponseRedirect, render, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, UpdateView
from . models import Post, UserBlogdom, UpvoteDetail
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from . forms import UserBlogdomForm, PostForm
from django.contrib.auth import logout
from rest_framework import generics
from .serializer import UserBlogdomSerializer, PostSerializer
from django.contrib.auth.models import User
import cloudinary
import cloudinary.uploader
import os


class IndexView(TemplateView):
    template_name = 'blogs/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['top_posts'] = Post.objects.order_by('-upvotes')
        context['recent_posts'] = Post.objects.order_by('-time')[:5]
        top_bloggers = sorted(UserBlogdom.objects.all(), key=lambda a: a.get_rating(), reverse=True)
        context['best_bloggers'] = top_bloggers
        return context


def UserProfile(request, pk):
    u = UserBlogdom.objects.get(user__username=pk)
    posts = u.post_set.all().order_by('-time')
    return render(request, 'blogs/user_profile.html', {'user': u, 'posts': posts})


@login_required
def UserBlogdomUpdate(request):
    if request.method == 'POST':
        form = UserBlogdomForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile_pic = request.FILES.get('profile_picture')
            profile_pic_public_id = content_profile_picture(request.user.profile, str(profile_pic))
            cover_pic = request.FILES.get('cover_picture')
            cover_pic_public_id = content_cover_picture(request.user.profile, str(cover_pic))
            if profile_pic is not None:
                cloudinary.uploader.upload(profile_pic, public_id = profile_pic_public_id)
            if cover_pic is not None:
                cloudinary.uploader.upload(cover_pic, public_id = cover_pic_public_id)
            user_profile_image = os.path.splitext(str(profile_pic))
            form.profile_picture = user_profile_image[0]
            form.save(commit=True)
            return HttpResponseRedirect(reverse('user_profile', kwargs={'pk': request.user.username}))
    else:
        user = request.user
        profile = user.profile
        form = UserBlogdomForm(instance=profile)

    args = {}
    args['form'] = form
    return render(request, 'blogs/profile_edit.html', args)


def content_profile_picture(instance, filename):
    filename = os.path.splitext(filename)[0]
    return 'user_{0}-profile_picture-{1}'.format(instance.user, filename)


def content_cover_picture(instance, filename):
    filename = os.path.splitext(filename)[0]
    return 'user_{0}-cover_picture-{1}'.format(instance.user, filename)


def content_post_image(instance, filename):
    filename = os.path.splitext(filename)[0]
    # dirname = instance.time.strftime('%Y.%m.%d.%H.%M.%S')
    return 'user_{0}-posts-{1}'.format(instance.blogger, filename)


@login_required
def DeleteUser(request):
    user = request.user
    record = UserBlogdom.objects.get(user = user)
    recordMain = User.objects.get(username = user)
    record.delete()
    recordMain.delete()
    return HttpResponseRedirect(reverse('index'))


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blogs/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.blogger = UserBlogdom.objects.get(user=self.request.user)
        post_image = os.path.splitext(str(post.image))
        print(post.image)
        post_pic_public_id = content_post_image(post, str(post.image))
        if str(post.image) != '':
            cloudinary.uploader.upload(post.image, public_id = post_pic_public_id)
        post.image = post_image[0]
        return super(PostCreateView, self).form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    fields = ['heading', 'blog_content', 'image']
    template_name = 'blogs/post_create.html'

    def form_valid(self, form):
        object = form.save(commit=False)
        post_pic = object.image
        post_pic_public_id = content_post_image(object, str(post_pic))
        if str(object.image) != '':
            cloudinary.uploader.upload(object.image, public_id=post_pic_public_id)
        if (str(object.blogger) == str(self.request.user)):
             return super(PostUpdate, self).form_valid(form)
        else:
            return HttpResponseRedirect(reverse('user_profile', kwargs={'pk': self.request.user.username}))


def load_blog_content(request, id):
    content = Post.objects.get(id=id)
    content = content.blog_content
    return HttpResponse(content)


def rating_user(request, username):
    user_rating = UserBlogdom.objects.get(user__username=username).get_rating()
    return HttpResponse(user_rating)


@login_required
def post_upvote(request, post_id):
    post = Post.objects.get(pk=post_id)
    upvoted_by = UserBlogdom.objects.get(user=request.user)
    ud_object, created = UpvoteDetail.objects.get_or_create(postid=post, userid=upvoted_by)

    if(ud_object.upvoted):
        ud_object.upvoted = False
        ud_object.save()
        post.upvotes = post.upvotes -1
        post.save()

    else:
        ud_object.upvoted = True
        ud_object.save()
        post.upvotes = post.upvotes + 1
        post.save()

    return HttpResponse(post.upvotes)


def LogoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


class Post_List(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class Post_Detail(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        blog_by = self.kwargs['username']
        user = UserBlogdom.objects.get(user__username = blog_by)
        return Post.objects.filter(blogger=user.id)


class UserBlogdom_List(generics.ListAPIView):
    queryset = UserBlogdom.objects.all()
    serializer_class = UserBlogdomSerializer


class UserBlogdom_Detail(generics.RetrieveAPIView):
    lookup_field = 'user__username'
    queryset = UserBlogdom.objects.all()
    serializer_class = UserBlogdomSerializer


