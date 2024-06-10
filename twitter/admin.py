from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Tweet

# Register your models here.
# Retirar o Group do registro.
admin.site.unregister(Group)

# Mesclar o Perfil com o Usuário.
class ProfileInline(admin.StackedInline):
    model = Profile

# Expandir o User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    #Só mostrar os campos de username na página de admin.
    fields = ["username"]
    inlines = [ProfileInline]

# Apagar o registro do usuário inicial.
admin.site.unregister(User)
# Registrar novamente o usuário e o Perfil.
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)

# Registrando Tweets
admin.site.register(Tweet)