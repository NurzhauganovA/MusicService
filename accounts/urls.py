from django.urls import path
from . import views

urlpatterns = [
    path("register/artist", views.CreateArtistProfileView.as_view(), name="register_artist"),
    path("register", views.register, name="register"),
    path("login", views.signin, name="login"),
    path("logout", views.logout, name='logout'),

]