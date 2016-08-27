from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^logout_user/', views.LogoutUser, name='logout'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^new_post/$', login_required(views.PostCreateView.as_view()), name='new_post'),
    url(r'^(?P<pk>[\w-]+)/$', views.UserProfile, name='user_profile'),
    url(r'^profile/edit/', views.UserBlogdomUpdate, name='user_profile_edit'),
    url(r'^post/edit/(?P<pk>[0-9]+)/', login_required(views.PostUpdate.as_view()), name="post_edit"),
    url(r'upvote/(?P<post_id>[0-9]+)/', views.post_upvote, name='post_upvote'),
]