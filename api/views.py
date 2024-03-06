from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Profile, Post, Comment

# ユーザー作成のためのビュー
class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer  # 使用するシリアライザーを指定
    permission_classes = (AllowAny,)  # どのユーザーでもアクセス可能に設定

# プロフィールに関するCRUD操作を行うためのビューセット
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()  # 使用するクエリセットを指定
    serializer_class = serializers.ProfileSerializer  # 使用するシリアライザーを指定

    # プロフィール作成時に実行されるメソッド
    def perform_create(self, serializer):
        serializer.save(userProfile=self.request.user)  # リクエストユーザーをプロフィールのユーザーとして保存

# 自分のプロフィールをリスト表示するためのビュー
class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()  # 使用するクエリセットを指定
    serializer_class = serializers.ProfileSerializer  # 使用するシリアライザーを指定

    # クエリセットをフィルタリングするメソッド
    def get_queryset(self):
        return self.queryset.filter(userProfile=self.request.user)  # リクエストユーザーのプロフィールのみを返す

# 投稿に関するCRUD操作を行うためのビューセット
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()  # 使用するクエリセットを指定
    serializer_class = serializers.PostSerializer  # 使用するシリアライザーを指定

    # 投稿作成時に実行されるメソッド
    def perform_create(self, serializer):
        serializer.save(userPost=self.request.user)  # リクエストユーザーを投稿のユーザーとして保存

# コメントに関するCRUD操作を行うためのビューセット
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()  # 使用するクエリセットを指定
    serializer_class = serializers.CommentSerializer  # 使用するシリアライザーを指定

    # コメント作成時に実行されるメソッド
    def perform_create(self, serializer):
        serializer.save(userComment=self.request.user)  # リクエストユーザーをコメントのユーザーとして保存