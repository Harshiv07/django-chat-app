from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.base_user import BaseUserManager

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()
    email = models.EmailField(max_length=75, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=70, null=True, blank=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    u_type = models.CharField(max_length=70, null=True, blank=True)
    location = models.CharField(max_length=70, null=True, blank=True)
    date_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    activated = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True, null=True, blank=True)
    institute_id = models.CharField(max_length=70, null=True, blank=True)
    batch_id = models.CharField(max_length=70, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['u_type']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Message(models.Model):

    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='sender_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='receiver_messages')
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} to {}'.format(self.sender.username, self.receiver.username)

class Institute(models.Model):
    institute_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    mobile = models.IntegerField(default=1, validators=[MaxValueValidator(9999999999), MinValueValidator(1)])
    contact = models.IntegerField(default=1, validators=[MaxValueValidator(9999999999), MinValueValidator(1)])
    person = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50)

class Classes(models.Model):
    class_id = models.AutoField(primary_key=True)
    institute = models.CharField(max_length=50)
    classname = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    subject = models.CharField(max_length=50, null=True, blank=True)


class Batch(models.Model):
    batch_id = models.AutoField(primary_key=True)
    institute = models.CharField(max_length=50)
    subject = models.CharField(max_length=50, null=True, blank=True)
    batchname = models.CharField(max_length=50)


class BatchDetails(models.Model):
    batchdetails_id = models.AutoField(primary_key=True)
    institute = models.CharField(max_length=50, null=True, blank=True)
    batch_id = models.CharField(max_length=50, null=True, blank=True)
    student = models.CharField(max_length=50, null=True, blank=True)
    subject = models.CharField(max_length=50, null=True, blank=True)

class ClassesDetails(models.Model):
    classdetails_id = models.AutoField(primary_key=True)
    institute = models.CharField(max_length=50)
    class_id = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    subject = models.CharField(max_length=50, null=True, blank=True)
    student = models.CharField(max_length=50, null=True, blank=True)

class SubjectClassTeacherDetails(models.Model):
    subteacher_id = models.AutoField(primary_key=True)
    institute = models.CharField(max_length=50)
    classid = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    subject = models.CharField(max_length=50, null=True, blank=True)
    teacher = models.CharField(max_length=50, null=True, blank=True)

class SubjectBatchTeacherDetails(models.Model):
    subteacher_id = models.AutoField(primary_key=True)
    institute = models.CharField(max_length=50)
    batchid = models.CharField(max_length=50)
    subject = models.CharField(max_length=50, null=True, blank=True)
    teacher = models.CharField(max_length=50, null=True, blank=True)