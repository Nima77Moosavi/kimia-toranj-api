from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import Post, PostImage
from .serializers import PostSerializer


class PostViewSet(ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
