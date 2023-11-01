from instaclone .models import UserProfile, User
from rest_framework import serializers
from instaclone.models import UserFollowing

# class UserProfileSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.username')
#     class Meta: 
#         model = UserProfile
#         fields = ['user', 'bio', 'profile_image']

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['profile_image'] = f'https://res.cloudinary.com/dug5dj4uz/{representation["profile_image"]}'
#         return representation


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta: 
        model = UserProfile
        fields = ['user_id', 'username', 'bio', 'profile_image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['profile_image'] = f'https://res.cloudinary.com/dug5dj4uz/{representation["profile_image"]}'
        return representation
    
    def get_username(self, instance):
        user_profile_name = UserProfile.objects.get(user=instance.user)
        return user_profile_name.user.username
        


    


class FollowAndUnfollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = "__all__"

class ReadUserFollowingSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source='follower.username')
    following = serializers.ReadOnlyField(source='following.username')
    class Meta:
        model = UserFollowing
        fields = ['follower', 'following']

    