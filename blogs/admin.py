from django.contrib import admin
from .models import Post, UserBlogdom, UpvoteDetail


class PostAdmin(admin.ModelAdmin):
    list_display = ('blogger', 'heading', 'time')
    search_fields = ('blogger', 'heading')
    readonly_fields = ('time',)


class UserBlogdomAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')


class UpvoteDetailAdmin(admin.ModelAdmin):
    list_display = ('postid', 'userid', 'upvoted')


admin.site.register(Post, PostAdmin)
admin.site.register(UserBlogdom, UserBlogdomAdmin)
admin.site.register(UpvoteDetail, UpvoteDetailAdmin)