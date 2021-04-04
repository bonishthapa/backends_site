from django.db import models
from django.db.models.deletion import SET_NULL
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_verified', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, first_name, password, **other_fields)

    def create_user(self, email, username, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name, **other_fields)
        user.set_password(make_password(password))
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'),unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=250)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name']

    def __str__(self):
        return self.username


class MainTitle(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user',blank=True,null=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True,blank=True,null=True)
    image = models.ImageField(upload_to='maintitle',blank=True,null=True)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_on']

    def get_absolute_url(self):
        return reverse("maintitle", kwargs={
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(MainTitle, self).save(*args, **kwargs)


class SubTitle(models.Model):
    maintitle = models.ManyToManyField(MainTitle, related_name='subtitle')
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True,blank=True,null=True)
    image = models.ImageField(upload_to='subtitle',blank=True,null=True)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    available_on = models.CharField(max_length=250)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_on']


    def get_absolute_url(self):
        return reverse("subtitle", kwargs={
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(SubTitle, self).save(*args, **kwargs)
