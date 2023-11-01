# from django.contrib.auth.models import User
from datetime import datetime
import os
from .models import User
from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'id','username']



class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id', 'files', 'description']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['files'] = f'https://res.cloudinary.com/dug5dj4uz/{representation["files"]}'
        return representation


class ReadPostsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    class Meta:
        model = Posts
        fields = ['id', 'user','files', 'description', 'created', 'likes_count']

    def to_representation(self, instance):  
        representation = super().to_representation(instance)
        representation['files'] = f'https://res.cloudinary.com/dug5dj4uz/{representation["files"]}' #To be JSON Serializable
        return representation
    
    def get_likes_count(self, instance):
        return instance.likes.count()
    

    def get_user(self, instance):
        user_profile = UserProfile.objects.get(user=instance.user)
        user_id = instance.user
        profile_image = user_profile.profile_image  
        public_id = profile_image.public_id  # Extracting the public_id of the cloudinary pic
        version = profile_image.version 
        format = profile_image.format #(file extension)

        image_url = f'https://res.cloudinary.com/dug5dj4uz/image/upload/v{version}/{public_id}.{format}'

        user_data = {
            'user_id': user_id.id,
            'user': user_profile.user.username,
            'profile_image': image_url
        }
        return user_data
    
    def get_created(self, instance):
        '''Formatting the time to be more readable'''
        now = timezone.now()  # Get the current time in the current timezone
        created_date = instance.created  

        time_difference = now - created_date

        minutes = time_difference.total_seconds() / 60
        hours = minutes / 60
        days = hours / 24
        weeks = days/7
        months = weeks/4
        years = months / 12

        if years >= 1:
            return f"{int(years)}{'y' if int(years) == 1 else 'yrs'} ago"
        elif months >=1 :
            return f"{int(months)}{'mth' if int(months) == 1 else 'mths'} ago"
        elif weeks >=1:
            return f"{int(weeks)}{'wk' if int(weeks)== 1 else 'wks'} ago"
        elif days >= 1:
            return f"{int(days)}{'d' if int(days) == 1 else 'days'} ago"
        elif hours >= 1:
            return f"{int(hours)}{'hr' if int(hours) == 1 else 'hrs'} ago"
        elif minutes >= 1:
            return f"{int(minutes)}{'min' if int(minutes) == 1 else 'mins'} ago"
        else:
            return "Just now"


    


class UserProfileSerializerx(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta: 
        model = UserProfile
        fields = ['user', 'bio', 'profile_image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['profile_image'] = f'https://res.cloudinary.com/dug5dj4uz/{representation["profile_image"]}'
        return representation
    


class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializerx(read_only=True)
    created = serializers.SerializerMethodField()
    class Meta:
        model = PostComment
        fields = ['id','body', 'user', 'created']

    def get_created(self, instance):
        '''Formatting the time to be more readable'''
        now = timezone.now()  # Get the current time in the current timezone
        created_date = instance.created  

        time_difference = now - created_date

        minutes = time_difference.total_seconds() / 60
        hours = minutes / 60
        days = hours / 24
        weeks = days/7
        months = weeks/4
        years = months / 12

        if years >= 1:
            return f"{int(years)}{'y' if int(years) == 1 else 'yrs'} ago"
        elif months >=1 :
            return f"{int(months)}{'mth' if int(months) == 1 else 'mths'} ago"
        elif weeks >=1:
            return f"{int(weeks)}{'wk' if int(weeks)== 1 else 'wks'} ago"
        elif days >= 1:
            return f"{int(days)}{'d' if int(days) == 1 else 'days'} ago"
        elif hours >= 1:
            return f"{int(hours)}{'hr' if int(hours) == 1 else 'hrs'} ago"
        elif minutes >= 1:
            return f"{int(minutes)}{'min' if int(minutes) == 1 else 'mins'} ago"
        else:
            return "Just now"







    

# ----------------------------KNOX TOKEN AUTHENTICATION -------------------------------#

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], None, validated_data['password'])
        return user
    


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError("Invalid Details")
    
