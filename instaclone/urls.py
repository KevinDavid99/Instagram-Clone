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








