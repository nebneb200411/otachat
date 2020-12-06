from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    """ユーザーマネージャー"""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """ユーザーネーム，email, パスワードを入力し，ユーザーを作成し，それを保存する"""
        if not email:
            raise ValueError("Emailを入力してください。")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル"""
    username = models.CharField(
        _("username"), max_length=50, unique=True)  # uniqueは一意性を持たせること
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=50, blank=True)
    last_name = models.CharField(_("last name"), max_length=50, blank=True)
    gender = models.CharField(
        _("gender"), max_length=2, blank=False)

    is_staff = models.BooleanField(_("staff status"), default=False, help_text=_(
        'Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_("active"), default=True, help_text=_('Designates whether this user should be treated as active. '
                                                                           'Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """入力された苗字と名前の間に半角を入れ，戻り値とする"""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """ユーザーに名前を返す"""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ユーザーにemailを送る"""
        send_mail(subject, message, from_email, [self.email], **kwargs)

# Profileクラスの定義


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateTimeField(_("birth date"), null=True, blank=True)
    location = models.CharField(_("location"), max_length=50, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
