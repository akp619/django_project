from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

# to fetch the room and user table columns and use columns in views.
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ('host', 'participants')

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        exclude = ('password', 'last_login', 'is_superuser', 'groups', 'user_permissions', 'username', 'is_staff', 'is_active', 'date_joined')