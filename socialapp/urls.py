from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'social'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.log_out, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>', views.profile, name='profile_visit'),
    path('register/', views.register, name='register'),
    path('edit-user/', views.edit_user, name='edit_user'),
    path('ticket/', views.ticket, name='ticket'),

    path('password-reset/', auth_views.PasswordResetView.as_view(success_url='done'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url='/password-reset/complete'),
         name="password_reset_confirm"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('password-change/', auth_views.PasswordChangeView.as_view(success_url='done'), name="password_change"),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('post_search/', views.search_post, name="search_post"),
    path('posts/post_detail/<int:id>/', views.post_detail, name="post_detail"),
    path('', views.post_list, name='post_list'),
    path('posts/tags/<slug:slug>/', views.post_list, name='post_tags'),
    path('post/add_comment/', views.add_comment, name='add_comment'),
    path('add_post/', views.add_post, name='add_post'),
    path('posts/post_detail/<int:post_id>/edit_post', views.edit_post, name="edit_post"),
    path('posts/post_detail/<int:post_id>/delete_post', views.delete_post, name="delete_post"),
    path('posts/like_post/', views.like_post, name='like_post'),
    path('posts/save_post/', views.save_post, name='save_post'),
    path('follow_user/', views.follow_user, name='follow_user'),
    path('followers/<int:id>/', views.followers_list, name='followers_list'),
]
