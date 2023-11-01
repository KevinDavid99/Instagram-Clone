# Generated by Django 4.1.4 on 2023-10-15 15:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('instaclone', '0010_userfollowing'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instaclone.posts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instaclone.userprofile')),
            ],
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
