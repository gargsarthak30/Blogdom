from django.shortcuts import  HttpResponseRedirect, render
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, UpdateView
from . models import Post, UserBlogdom, UpvoteDetail
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from . forms import UserBlogdomForm, PostForm
from django.contrib.auth import logout
from rest_framework import generics
from .serializer import UserBlogdomSerializer, PostSerializer


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
            form.save(commit=True)
            return HttpResponseRedirect(reverse('user_profile', kwargs={'pk': request.user.username}))
    else:
        user = request.user
        profile = user.profile
        form = UserBlogdomForm(instance=profile)

    args = {}
    args['form'] = form
    return render(request, 'blogs/profile_edit.html', args)


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blogs/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.blogger = UserBlogdom.objects.get(user=self.request.user)
        return super(PostCreateView, self).form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    fields = ['heading', 'blog_content', 'public', 'image']
    template_name = 'blogs/post_create.html'

    def form_valid(self, form):
        object = form.save(commit=False)
        if (str(object.blogger) == str(self.request.user)):
             return super(PostUpdate, self).form_valid(form)
        else:
            return HttpResponseRedirect(reverse('user_profile', kwargs={'pk': self.request.user.username}))


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

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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


