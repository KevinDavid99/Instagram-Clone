from django.contrib import admin
from .models import Posts, PostComment, UserProfile, User, UserFollowing



admin.site.register(Posts)
admin.site.register(UserProfile)
admin.site.register(PostComment)
admin.site.register(User)
admin.site.register(UserFollowing)


