from django.conf.urls import url
from . import views

app_name = 'games'

urlpatterns = [
    url(r'^$', views.library, name='library'),
    url(r'^signIn$', views.signIn, name='signIn'),
    url(r'^register$', views.register, name='register'),
    url(r'^game_[a-z]+$', views.game_canvas, name='games_game_canvas')
    ]
