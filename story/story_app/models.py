from django.db import models

from story_auth.models import Writer, UserProfile


class Story(models.Model):
    FUN = 'FN'
    LOVE = 'LV'
    UNEXPECTED_END = 'UE'
    MYSTERY = 'MY'
    FAIRY_TAIL = 'FT'
    FANTASY = 'FA'

    CATEGORY_CHOICES = (
        (FUN, 'fun'),
        (LOVE, 'love'),
        (UNEXPECTED_END, 'unexpected-end'),
        (MYSTERY, 'mystery'),
        (FAIRY_TAIL, 'fairy-tail'),
        (FANTASY, 'fantasy'),
    )

    writer = models.ForeignKey(Writer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='story_images')
    date = models.DateField(auto_now_add=True)
    published = models.BooleanField(default=False)
    favorites = models.ManyToManyField(UserProfile, related_name='favorites', blank=True)
    likes = models.ManyToManyField(UserProfile, related_name='likes', blank=True)

    def __str__(self):
        return f'{self.title} --by {self.writer.user_profile.user.first_name} {self.writer.user_profile.user.last_name}'


class Comment(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Comment for {self.story.title}'

