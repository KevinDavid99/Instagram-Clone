from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import *
from.serializers import*
from rest_framework .views import APIView
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework import filters
from.permissions import IsAuthorOrReadOnly, IsUserProfile
from rest_framework import viewsets
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
import cloudinary
from cloudinary.uploader import destroy
from rest_framework import status


class PostComments(generics.ListCreateAPIView):
    permission_classes = (IsAuthorOrReadOnly, )
    authentication_classes = (TokenAuthentication, )
    serializer_class = CommentSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile, post_id=self.kwargs['post_id']) # Get and saving the specific user/profile of who made the comment

    def list(self, request, *args, **kwargs):
        '''Using the specific post id in the url to access the comments related to it'''
        post_id = self.kwargs['post_id']
        post = Posts.objects.get(id=post_id)
        comments = PostComment.objects.filter(post_id=post_id)
        post_serializer = ReadPostsSerializer(post) 
        comment_serializer = CommentSerializer(comments, many=True)
        
        response_data = {
            'post': post_serializer.data,
            'comments': comment_serializer.data,
        }
        return Response(response_data)


class PostCommentsDelete(generics.DestroyAPIView):
    permission_classes = (IsUserProfile, )
    authentication_classes = (TokenAuthentication, )
    queryset = PostComment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "id"


class PostCommentGet(generics.RetrieveAPIView):
    permission_classes = (IsUserProfile, )
    authentication_classes = (TokenAuthentication, )
    queryset = PostComment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "id"



class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthorOrReadOnly, )
    authentication_classes = (TokenAuthentication, )
    queryset = Posts.objects.all()
    serializer_class = ReadPostsSerializer


    def post(self, request, *args, **kwargs):
        serializer = PostsSerializer(data=request.data)

        if serializer.is_valid():
            # This line checks if the user is authorized to make a post
            serializer.validated_data['user'] = request.user
            post = serializer.save()

            # Getting the auther of the post
            user_serializer = UserSerializer(request.user)


            post.save()
            data = {
                'user': user_serializer.data,
                'id': post.id,
                'description': post.description,
                'files': f'https://res.cloudinary.com/dug5dj4uz/{post.files}',
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PostDetailView(generics.RetrieveAPIView):
    """Allows authenticated users to get specific post,
    and also get a specific post to update or delete"""
    permission_classes = (IsAuthorOrReadOnly, )
    authentication_classes = (TokenAuthentication,)
    queryset = Posts.objects.all()
    serializer_class = ReadPostsSerializer
    lookup_field = "id"


class PostUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthorOrReadOnly, )
    authentication_classes = (TokenAuthentication,)
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    lookup_field = 'id'

    def patch(self, request, id):
        post = Posts.objects.get(id=id)
        serializer = PostsSerializer(post, data=request.data, partial=True)
        
        # if the new serialized post is valid, then save
        if serializer.is_valid():

            post = serializer.save()

            user_serializer = UserSerializer(request.user)

            post.save()
            data = {
                'user': user_serializer.data,
                'id': post.id,
                'description': post.description,
               'files': f'https://res.cloudinary.com/dug5dj4uz/{post.files}',
            }

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PostDelete(generics.DestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly, )
    authentication_classes = (TokenAuthentication,)
    queryset = Posts.objects.all()
    serializer_class = ReadPostsSerializer
    lookup_field = "id"


    def delete(self, request, id, *args, **kwargs):
        '''deleting both the post file from cloudinary'''
        postfile = self.get_object()
        if postfile.user.id == request.user.id:
            cloudinary_file = postfile.files.public_id
            destroy(cloudinary_file)
            postfile.delete()
            return Response({ "success": True, "message": "post deleted" })




class SearchAnything(generics.ListAPIView):
    """The PostSearch allows for searching names and description relating to the Posts instance"""
    permission_classes = (IsAuthorOrReadOnly,)
    authentication_classes = (TokenAuthentication, )
    queryset = Posts.objects.all()
    serializer_class = ReadPostsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['description', 'user__username']



class LikeAndUnlikeView(APIView):
    '''Handles the like and unlike functionality'''
    permission_classes = (IsAuthorOrReadOnly, )
    authentication_classes = (TokenAuthentication, )
    
    def post(self, request, uuid):
        posts = Posts.objects.get(pk=uuid) 
        serialized_post = PostsSerializer(posts, data=request.data)
        user = (request.user.username) #The user who currently like or unlike the post
        if serialized_post.is_valid():
            serialized_post.save()

        liked = False
        # checking the user who likes the current post exist so that he can be removed
        if posts.likes.filter(pk=request.user.pk).exists():
            posts.likes.remove(request.user)
        else:
            posts.likes.add(request.user)
            liked = True

        likes_count = posts.number_of_likes #property gotten from the models to count the likes by different users
        return Response(
            { 
                'liked_post' : serialized_post.data, 
                'user_who_liked_it' : user ,
                'liked': liked, 
                'likes_count': likes_count
            }
        )
    





#---------------USER AUTHENTICATION----------------------#


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            return Response({
                'user': UserSerializer(user, context=self.get_serializer_context()).data,
                'token': AuthToken.objects.create(user)[1]
            })

class LoginView(KnoxLoginView):
    permission_classes = ()
    
    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class UserApi(generics.RetrieveAPIView):
    permission_classes = (IsAuthorOrReadOnly, )
    authentication_classes = (TokenAuthentication, )
    serializer_class = AuthUserSerializer

    def get_object(self):
        return self.request.user
