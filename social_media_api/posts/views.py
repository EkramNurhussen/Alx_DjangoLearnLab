# posts/views.py
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import action
from .models import Like
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class StandardPagination(PageNumberPagination):
    page_size = 10

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('search', None)
        if query:
            queryset = queryset.filter(title__icontains=query) | queryset.filter(content__icontains=query)
        return queryset

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
# posts/views.py
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardPagination

    def get_queryset(self):
        followed_users = self.request.user.following.all()
        return Post.objects.filter(author__in=followed_users).order_by('-created_at')
    # posts/views.py

class PostViewSet(viewsets.ModelViewSet):
    # ... Existing code ...
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if not Like.objects.filter(post=post, user=user).exists():
            Like.objects.create(post=post, user=user)
            if post.author != user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=user,
                    verb="liked your post",
                    target_content_type=ContentType.objects.get_for_model(Post),
                    target_object_id=post.id
                )
            return Response({'status': 'Post liked'})
        return Response({'error': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        Like.objects.filter(post=post, user=user).delete()
        return Response({'status': 'Post unliked'})