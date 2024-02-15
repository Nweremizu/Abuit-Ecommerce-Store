from django.urls import path
from abuit_user import views

app_name = "abuit_user"
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.redirect_entry, name='entry')

]