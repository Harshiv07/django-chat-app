from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Message(models.Model):

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='sender_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
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

class UserManager(BaseUserManager):
    def create_user(self, email, u_type, password="Klaasx2020"):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email ')

        user = self.model(
            email=email,
        )

        user.password = "Klaasx2020"
        user.activated = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, u_type, password):
        """
         Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, u_type=u_type,
                                password=password
                                )
        user.is_admin = True
        user.activated = True
        user.u_type = u_type
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # objects = models.Manager()
    objects = UserManager()
    mobile_no = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=75, null=True, blank=True, unique=True)
    password = models.CharField(max_length=50, null=True, blank=True, default="Klaasx2020")
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=70, null=True, blank=True)
    u_type = models.CharField(max_length=70, null=True, blank=True)
    location = models.CharField(max_length=70, null=True, blank=True)
    date_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    activated = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True, null=True, blank=True)
    institute_id = models.CharField(max_length=70, null=True, blank=True)
    batch_id = models.CharField(max_length=70, null=True, blank=True)

    def __unicode__(self):
        return str(self.mobile_no)

    def __str__(self):
        return str(self.mobile_no)

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    class Meta:
        ordering = ['-id']

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['u_type']
