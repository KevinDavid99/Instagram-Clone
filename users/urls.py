from django .urls import path
from users import views

urlpatterns = [
    path('api/<str:username>-profile-settings/', views.UserProfileView.as_view()),
    path('api/users/', views.AllUsers.as_view()),
    path('user/follow/<uuid:uuid>/', views.FollowAndUnfollow.as_view()),
]




    # def post(self, request, uuid):
    #     following_user = User.objects.get(pk=uuid)
    #     if request.user == following_user:
    #         return Response({'You cant follow yourself'})
    #     follow_user, created = UserFollowing.objects.get_or_create(follower=request.user, following = following_user)
    #     if not created:
    #         follow_user[0].delete()
    #         # follow_user.count_followers
    #         return Response({ "Followed": False, "message": "unfollowed user" })
    #     else:
    #         return Response({ "Followed": True, "message": "followed user" })