# Generated by Django 4.1.4 on 2023-09-15 19:47

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instaclone', '0005_alter_userprofile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/dug5dj4uz/image/upload/v1694778236/Insagram_User_Profile_Picture/default_fvxn5f.jpg', max_length=255, verbose_name='image'),
        ),
    ]
