from django.contrib import admin
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import get_object_or_404

from users.models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    search_fields = list_filter
    save_on_top = True

    def save_model(self, request, obj, form, change):
        user_database = get_object_or_404(User, pk=obj.pk)
        if not (check_password(form.data['password'], user_database.password)
                or user_database.password == form.data['password']):
            obj.password = make_password(obj.password)
        else:
            obj.password = user_database.password
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
