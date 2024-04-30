from django.contrib import admin
from django.core.mail import send_mail

from .models import User, Post, Comment, Contact, Ticket
from django.contrib.auth.admin import UserAdmin


# Register your models here.


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'phone', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Fields', {'fields': ('phone', 'job', 'bio', 'photo', 'date_of_birth')}),
    )


def email_activation(modeladmin, request, queryset):
    count_of_posts = 0
    for obj in queryset:
        if obj.active is False:
            send_mail(
                'post_status',
                f'hello {obj.auther} your post is deactivated',
                'davodrashiworking@gmail.com',
                [obj.auther.email],
            )
            count_of_posts += 1
    modeladmin.message_user(request, f'{count_of_posts} email send.')


email_activation.short_description = 'email activation'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['auther', 'create', 'active']
    search_fields = ['author', 'caption']
    actions = [email_activation]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['auther', 'text', 'create', 'status']
    ordering = ['create']
    list_filter = ['post', 'status']
    search_fields = ['text', 'auther']
    raw_id_fields = ['post']
    date_hierarchy = 'create'
    list_editable = ['status']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to', 'created']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['subject', 'email', 'phone']
