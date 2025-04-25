from django.db import models


class Highlight(models.Model):
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='highlight_covers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class HighlightMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    highlight = models.ForeignKey(
        Highlight, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(
        max_length=10, choices=MEDIA_TYPE_CHOICES, null=True)
    media_file = models.FileField(upload_to='highlight_media/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "هایلایت"
        verbose_name_plural = "هایلایت ها"

    def __str__(self):
        return f"{self.media_type.capitalize()} for {self.highlight.title}"
