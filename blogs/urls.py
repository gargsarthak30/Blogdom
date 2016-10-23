from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^logout_user/', views.LogoutUser, name='logout'),
    url(r'delete/user', views.DeleteUser, name = 'deleteUser'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^new_post/$', login_required(views.PostCreateView.as_view()), name='new_post'),
    url(r'^content/(?P<id>[0-9]+)', views.load_blog_content, name= "load_blog_content"),
    url(r'^(?P<pk>[-\w.]+)/$', views.UserProfile, name='user_profile'),
    url(r'^profile/edit/', views.UserBlogdomUpdate, name='user_profile_edit'),
    url(r'^post/edit/(?P<pk>[0-9]+)/', login_required(views.PostUpdate.as_view()), name="post_edit"),
    url(r'upvote/(?P<post_id>[0-9]+)/', views.post_upvote, name='post_upvote'),
    url(r'rating/(?P<username>[\w-]+)/', views.rating_user, name='UserRating'),
    url(r'^data/users/$', views.UserBlogdom_List.as_view(), name="users-api"),
    url(r'^data/posts/$', views.Post_List.as_view(), name="posts-api"),
    url(r'^data/posts/(?P<username>[\w-]+)/$', views.Post_Detail.as_view(), name="posts-api-specific"),
    url(r'^data/users/(?P<user__username>[\w-]+)/$', views.UserBlogdom_Detail.as_view(), name="users-api-specific"),
]

urlpatterns = format_suffix_patterns(urlpatterns)