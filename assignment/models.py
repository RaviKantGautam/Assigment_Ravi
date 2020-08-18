from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.exceptions import *
from django.core.validators import *
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User Must have email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.active = True
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user


def phn_no_validation(value):
    if str(value).isnumeric() == False:
        raise ValidationError('Invalid Mobile Number')
    elif len(str(value)) < 10:
        raise ValidationError('Mobile Number Should be 10 character')
    else:
        return value


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email")
    phn_no = models.CharField(max_length=12, verbose_name="Mobile No.", validators=[phn_no_validation])
    active = models.BooleanField(default=False)
    client = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_client(self):
        return self.client

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    objects = UserManager()


class Category_type(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    objects = models.Manager

    def __str__(self):
        return self.name


def validate_pin(pin):
    if str(pin).isnumeric() == False:
        print(pin)
        raise ValidationError('Invalid Pincode')
    if re.fullmatch("\d{4}|\d{6}", pin):
        return pin
    else:
        raise ValidationError('Pincode is of 6 integer character')


class Request_Table(models.Model):
    STATUS_CHOICE = [('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')]
    STATES_NAMES = [('Punjab', 'Punjab'), ('Delhi', 'Delhi'), ('Rajasthan', 'Rajasthan'), ('Maharastra', 'Maharastra'),
                    ('Utter Pradesh', 'Utter Pradesh'), ('Madhya Pradesh', 'Madhya Pradesh'),
                    ('Jammu Kashmir', 'Jammu Kashmir'), ('Gujrat', 'Gujrat'), ('Tamil Nadu', 'Tamil Nadu'),
                    ('Kerela', 'Kerela'), ('Karnatka', 'Karnatka'), ('Orissa', 'Orissa')]
    TYPE = [('Plumbing', 'Plumbing'), ('Electricity', 'Electricity'), ('Painting', 'Painting'),
            ('Deep Cleaning', 'Deep Cleaning')]
    request_type = models.ManyToManyField(Category_type, verbose_name='Request Type')
    request_desc = models.TextField(verbose_name='Request Desc')
    city = models.CharField(max_length=255, verbose_name='City')
    state = models.CharField(max_length=255, choices=STATES_NAMES)
    pincode = models.CharField(max_length=6, verbose_name='Pin Code', validators=[validate_pin])
    # country_code = models.CharField(max_length=3, verbose_name="Country Code")
    date = models.DateTimeField(verbose_name='Request Date', auto_now_add=True)
    mobile = PhoneNumberField()
    status = models.CharField(max_length=255, verbose_name="Status", choices=STATUS_CHOICE, default='Pending',
                              blank=True, null=True)
    remarks = models.TextField(verbose_name="Remarks", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User', blank=True,
                             null=True)
    objects = models.Manager

    def __str__(self):
        return str(self.id)
