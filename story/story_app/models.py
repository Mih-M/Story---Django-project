from django.db import models

from story_auth.models import Writer


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

    def __str__(self):
        return f'{self.title} --by {self.writer.user_profile.user.first_name} {self.writer.user_profile.user.last_name}'


class Like(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.story}'
