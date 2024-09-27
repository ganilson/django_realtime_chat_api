from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

import uuid
# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    # foto = models.ImageField(verbose_name="", null=True, upload_to="images")
    genderChoices = [
        ('Masculino','Masculino'),
        ('Feminino','Feminino'),
    ]
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='auth_users',
        blank=True,
        verbose_name=('groups'),
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='auth_users',
        blank=True,
        verbose_name=('user permissions'),
        help_text=('Specific permissions for this user.'),
    )
    telefone = models.CharField(max_length=14, blank=True, unique=False)
    telefoneVerified = models.BooleanField(default=False)
    gender = models.CharField(choices= genderChoices , max_length=50)
    saldo = models.FloatField(default=0)
    yetucode = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(null=True,  max_length=254)
    endereco1 = models.CharField(max_length=50,blank=True)
    verificado = models.BooleanField(default=False)
    first_login = models.BooleanField(default=True)

class Message(models.Model):
    sender = models.ForeignKey(to=User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(to=User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username}: {self.content} [{self.timestamp}]'




class Room(models.Model):
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)
    mensagens = models.ManyToManyField(to=Message, blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'