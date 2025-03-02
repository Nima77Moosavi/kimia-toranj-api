from rest_framework import serializers
from .models import Highlight, HighlightMedia


class HighlightMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HighlightMedia
        fields = ['id', 'media_type', 'media_file', 'created_at']


class HighlightSerializer(serializers.ModelSerializer):
    media = HighlightMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Highlight
        fields = ['id', 'title', 'cover_image', 'created_at', 'media']
