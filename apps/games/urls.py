from django.urls import path

# Local
from .views import GameView, about, GameListView, MainView


urlpatterns = [
    path('list/<int:game_id>/', GameView.as_view()),
    path('about/', about),
    path('', MainView.as_view()),
    path('list/', GameListView.as_view()),
]
