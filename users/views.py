from django.shortcuts import get_object_or_404, render
from .serializers import *
from rest_framework import filters
from instaclone .serializers import *
from rest_framework.response import Response
from instaclone .permissions import IsAuthorOrReadOnly
from knox.auth import TokenAuthentication
from rest_framework import generics
from rest_framework import status
from rest_framework .views import APIView
from instaclone.models import UserProfile, UserFollowing, User, Posts




class AllUsers(generics.ListAPIView):
    permission_classes = (IsAuthorOrReadOnly, )
    authentication_classes = (TokenAuthentication, )
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ['user', 'user__username']




class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthorOrReadOnly, )
    authentication_classes = (TokenAuthentication, )
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


    def get_object(self):
        '''using the username of the user in the url to access his profile'''
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return user.userprofile
    
    def get_user_posts(self):
        '''Filters the posts created by the user'''
        user_profile = self.get_object()
        user_posts = Posts.objects.filter(user=user_profile.user)
        post_serializer = PostsSerializer(user_posts, many=True) 
        return post_serializer.data
    

    def get(self, request, *args, **kwargs):
        user_profile = self.get_object()
        user_profile_data = UserProfileSerializer(user_profile).data
        user_posts = self.get_user_posts()  # Get the user's posts
        number_of_user_posts = Posts.objects.filter(user=user_profile.user).count()
        user_profile_data['posts'] = user_posts  # Adding the posts to the user profile data
        user_profile_data['number_of_user_post'] = number_of_user_posts # Adding the number of posts to the user profile data
        return Response(user_profile_data)
    


    def partial_update(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile, data=request.data, partial=True)
        
        if request.method == 'PATCH':
            if serializer.is_valid():

                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error', 'invalid'})

            

class FollowAndUnfollow(APIView):
    permission_classes = (IsAuthorOrReadOnly, )
    authentication_classes = (TokenAuthentication, )
    queryset = UserFollowing.objects.all()
    serializer_class = FollowAndUnfollowSerializer

    def get_object(self):
        '''using the id of the user in the url to access his followers and who he is following'''
        user_id = self.kwargs.get('uuid')
        user = get_object_or_404(User, id=user_id)
        return user

    def get(self, request, uuid):
        userobj = self.get_object()
        #user
        following = UserFollowing.objects.filter(follower = userobj)
        #follows
        followers = UserFollowing.objects.filter(following = userobj)

        following_serializer = ReadUserFollowingSerializer(following, many=True)
        followers_serializer = ReadUserFollowingSerializer(followers, many=True)
        return Response(
            { 
                "success": True, 
                "following": following_serializer.data, 
                "followers": followers_serializer.data, 
                "num_of_users_following" : following.count(), 
                "num_of_followers" : followers.count()
            }
        )

    def post(self, request, uuid):
        following_user = User.objects.get(pk=uuid)
        if request.user == following_user:
            return Response({'You cant follow yourself'})
        follow_user = UserFollowing.objects.get_or_create(follower=request.user, following = following_user)
        if not follow_user[1]:
            follow_user[0].delete()
            # follow_user.count_followers
            return Response({ "Followed": False, "message": "unfollowed user" })
        else:
            return Response({ "Followed": True, "message": "followed user" })

