from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.conf import settings

def upload_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.userProfile.id) + str(instance.nickName) + str('.') + str(ext)])

class UserManager(BaseUserManager):
    # 通常のユーザーを作成するメソッド
    def create_user(self, email, password=None):
        # メールアドレスが提供されていない場合はエラーをスロー
        if not email:
            raise ValueError('The Email field must be set')

        # modelメソッドを使用してユーザーオブジェクトを作成
        # この時、normalize_emailメソッドを使用してメールアドレスを正規化
        user = self.model(email=self.normalize_email(email))
        # set_passwordメソッドを使用することで、パスワードをハッシュ化して設定
        user.set_password(password)
        # saveメソッドの引数にusing=self._dbを指定することで、デフォルトのデータベースを使用
        user.save(using=self._db)

        return user

    # スーパーユーザー（管理者）を作成するメソッド
    def create_superuser(self, email, password):
        # 通常のユーザー作成メソッドを使用してユーザーを作成
        user = self.create_user(email, password=password)
        # 管理者権限を与えるためにフラグを設定
        user.is_staff = True
        user.is_superuser = True
        # 変更をデータベースに保存
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # カスタムユーザーマネージャーを使用
    objects = UserManager()

    # ユーザー名として使用するフィールド
    USERNAME_FIELD = 'email'

    # ユーザーオブジェクトを文字列で表現した際の挙動を定義
    def __str__(self):
        return self.email

class Profile(models.Model):
    nickName = models.CharField(max_length=20)
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userProfile', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to=upload_avatar_path, blank=True, null=True)

    def __str__(self):
        return self.nickName