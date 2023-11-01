from django.urls import include, path
from instaclone import views
from knox import views as knox_views
# Autopep8 exension


urlpatterns = [
    path('api/auth/', include('knox.urls')),
    path('api/posts/search/', views.SearchAnything.as_view()),
    path('api/comments/<uuid:post_id>/', views.PostComments.as_view()),
    path('api/comments-delete/<int:id>/', views.PostCommentsDelete.as_view()),
    path('api/posts/', views.PostListCreateView.as_view()),
    path('api/get-posts/<uuid:id>/', views.PostDetailView.as_view()),
    path('api/post-update/<uuid:id>/',views.PostUpdateView.as_view()),
    path('api/posts/<uuid:id>/', views.PostDelete.as_view()),
    path('auth/register/', views.RegisterView.as_view()),
    path('auth/login/', views.LoginView.as_view()),
    path('auth/logout/', knox_views.LogoutView.as_view()),
    path('auth/user/', views.UserApi.as_view()),
    path('like/unlike/<uuid:uuid>/', views.LikeAndUnlikeView.as_view(), name='like_unlike'),
    path('api/comments/<int:id>/', views.PostCommentGet.as_view()),
] 












# It appears that you are trying to display the likes_count from the response in your React component, but you are not getting the desired result. Here's a possible issue and a suggestion on how to fix it:

# Issue:
# In your code, you are mapping through likeCount and trying to access the likes_count as if it's directly under the likeCount array. However, in your response, the likes_count is nested inside the liked_post object.

# Suggestion:
# You need to update your code to access likes_count from the liked_post object within the likeCount array. Here's how you can modify your code to achieve that:

# jsx
# Copy code
# {likeCount.map((likey) => (
#   <div className={s.postcard} key={post.id}>
#     {/* ... other code ... */}
#     <div className={s.likes}>{likey.liked_post.likes_count}</div>
#     {/* ... other code ... */}
#   </div>
# ))}