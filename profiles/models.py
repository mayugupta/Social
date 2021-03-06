from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Class to manage user creation"""

    def create_user(self, email, name, password=None):
        """Creates a new user with the given details"""

        #Checking user has provided an email
        if not email:
            return ValueError("Must have an email")

        #Creating a new user object
        user = self.model(email=self.normalize_email(email), name=name)

        #Hashing the password instead of saving it as plaintext
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Creating a superuser(admin) using the provided details"""

        user = self.create_user(email, name, password)

        #Making the user admin
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """User profile for the social network"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Function to let django know what is user full name"""

        return self.name

    def __str__(self):
        """To show on output of an object as string"""

        return self.email


class ProfileFeedItem(models.Model):
    """Profile status update for feed"""

    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status_text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return model as string"""
        return self.status_text

class Messaging(models.Model):
    """Message from user to user"""

    sent_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='message_sender',
        on_delete=models.SET_NULL,
        null=True
    )
    message_text = models.TextField()
    sent_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='message_receiver',
        on_delete=models.SET_NULL,
        null=True
    )
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return message as string"""

        return self.message_text

class FriendRequest(models.Model):
    """Friend request from one user to another"""

    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='to_user',
        on_delete=models.CASCADE
    )
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='from_user',
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the request"""

        return "From {}, to {}".format(
            self.from_user.username,
            self.to_user.username
        )
