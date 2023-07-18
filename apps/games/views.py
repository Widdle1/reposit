# Django
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.db.models.query import QuerySet
from django.db.models.functions import Lower
from django.views import View

# Local
from .models import Game, Genre, Company, Comment, User

#Other
import datetime


class MainView(View):
    
    def get(self, request: HttpRequest) -> HttpResponse:
        template_name: str = 'games/index.html'
        return render(
            request=request,
            template_name=template_name,
            context={}
        )


class GameListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        template_name: str = 'games/video.html'
        queryset: QuerySet[Game] = Game.objects.all().order_by('-id')
        genres: QuerySet[Genre] = Genre.objects.all()
        return render(
            request=request,
            template_name=template_name,
            context={
                'games': queryset,
                'genres': genres
            }
        )
    
    def post(self, request: HttpRequest) -> HttpResponse:
        data: dict = request.POST
        try:
            company: Company = Company.objects.annotate(
                lower_name=Lower('name')
            ).get(
                lower_name=data.get('company').lower()
            )
        except Company.DoesNotExist:
            return HttpResponse(
                f"Company {data.get('company')} doesn`t exists"
            )
        game: Game = Game.objects.create(
            name=data.get('name'),
            price=float(data.get('price')),
            datetime_created=data.get('datetime_created'),
            company=company
        )

        key: str
        for key in data:
            if 'genre_' in key:
                genre: Genre = Genre.objects.get(
                    id=int(key.strip('genre_'))
                )
                game.genres.add(genre)
        game.save()

        return HttpResponse("Hello!")


class GameView(View):
    def get(self, request: HttpRequest, game_id: int) -> HttpResponse:
        try:
            game: Game = Game.objects.get(id=game_id)
            comments: Comment = game.game_comments.all()
        except Game.DoesNotExist as e:
            return HttpResponse(
                f'<h1>Игры с id {game_id} не существует!</h1>'
            )
        return render(
            request=request,
            template_name='games/store-product.html',
            context={
                'igor': game,
                'comments': comments,
                'sum_comments': len(comments) 
            }
    )

    def post(self, request: HttpRequest, game_id: int) -> HttpResponse:
        data: dict = request.POST
        game: Game = Game.objects.get(id=game_id)
        comment: Comment = Comment.objects.create(
            user=User.objects.all()[0],
            text=data.get('text'),
            rate=float(data.get('rate')),
            datetime_created=datetime.datetime.now(),
            game=game
        )
        comment.save()

        return redirect(f"/games/list/{game_id}")
    

def about(request: HttpRequest) -> HttpResponse:
    template_name: str = 'games/about.html'
    return render(
        request=request,
        template_name=template_name,
        context={}
    )
