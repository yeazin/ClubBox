from django.contrib import admin
from .models import User, Gender, Admin, Member

admin.site.register(User)
admin.site.register(Gender)
admin.site.register(Admin)
admin.site.register(Member)
