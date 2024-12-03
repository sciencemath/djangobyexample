from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class Profile(models.Model):
  user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
  )
  date_of_birth = models.DateField(blank=True, null=True)
  photo = models.ImageField(
    upload_to='users/%Y/%m/%d/',
    blank=True
  )

  def __str__(self):
    return f'Profile of {self.user.username}'

# An intermediate model is needed because we 
# dont want to modify the builtin User model `django.contrib.auth`
# instead we add dynamically (see below)
class Contact(models.Model):
  user_from = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='rel_from_set',
    on_delete=models.CASCADE
  )
  user_to = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='rel_to_set',
    on_delete=models.CASCADE
  )
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    indexes = [
      models.Index(fields=['-created']),
    ]
    ordering = ['-created']

  def __str__(self):
    return f'{self.user_from} follows {self.user_to}'
  
user_model = get_user_model()
user_model.add_to_class(
  'following',
  models.ManyToManyField(
    'self',
    through=Contact,
    related_name='followers', # if I follow you, it doesn't mean that you automatically follow me
    symmetrical=False
  )
)