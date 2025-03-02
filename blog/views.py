from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, PostImage
from .serializers import PostSerializer, PostImageSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)  # Handle file uploads

    def perform_create(self, serializer):
        serializer.save()


class PostImageViewSet(viewsets.ModelViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
    parser_classes = (MultiPartParser, FormParser)  # Handle file uploads


class WYSIWYGImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            return Response({"error": "No image provided."}, status=400)

        post_image = PostImage.objects.create(image=image)
        serializer = PostImageSerializer(post_image)
        return Response(serializer.data, status=201)
