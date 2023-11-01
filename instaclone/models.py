import uuid
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Posts(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    files = CloudinaryField(resource_type='auto', folder='Insagram_Posts', default='')
    description = models.TextField(blank=True)
    created = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    @property
    def number_of_likes(self):
        return self.likes.count()


    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return f"Post : {self.description}\n By {self.user}"
    








class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = CloudinaryField("image", folder='Insagram_User_Profile_Picture', default='v1694778236/Insagram_User_Profile_Picture/default_fvxn5f.jpg')
    bio = models.TextField(max_length=150, null=True, blank=True)
    website = models.CharField(max_length=90, null=True, blank=True)
    slug = models.SlugField(default='', null=False, unique=True)

    def __str__(self) -> str:
        name = str(self.user.username)
        if name.endswith('s'):
            return f"{self.user} Profile "
        else:
            return f"{self.user}'s Profile "
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)


    @property
    def image_url(self):
        return(
            f"https://res.cloudinary.com/dug5dj4uz/image/upload/v{self.profile_image.version}/{self.profile_image}"
        )
    

class UserFollowing(models.Model):
    # user
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    # follows
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    @property
    def count_followers(self):
        return User.objects.filter(following=self.following).count()
    
    def __str__(self):
        return f'{self.follower} is following {self.following}'

        

class PostComment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.user.username

    def __str__(self) -> str:
        return f'{self.user} commented on the post {self.post.description} : {self.body}'

