
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView
urlpatterns = [
    path('', views.home, name='home'),
    path('categories/<str:category>/', views.category_view, name='category_view'),
    path('create/', views.create_vacation, name='create_vacation'),
    path('vacation/<int:id>', views.vacation_detail, name='vacation_detail'),
    path('comment/upvote/<int:comment_id>/', views.upvote_comment, name='upvote_comment'),
    path('search/', views.search, name='search'),
    path('login/', CustomLoginView.as_view(template_name='vacations/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('comment/add/<int:vacation_id>/', views.add_comment, name='add_comment'),
    path('comment/upvote/<int:comment_id>/', views.upvote_comment, name='upvote_comment'),
    path('toggle-favorite/<int:vacation_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites, name='favorites'),
    path('dynamic-search/', views.dynamic_search, name='dynamic_search'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('get-user-theme/', views.get_user_theme, name='get_user_theme'),
    path('check-logged-in/', views.check_logged_in, name='check_logged_in'),
]
