from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from .models import *


# 127.0.0.1/events/win?winner_id=foo&loser_id=bar
def win(request):
    # Проверить токен \\\ Содержит заголовок token
    token = request.headers.get('token')
    if not check_token_in_db(token):
        return HttpResponseNotFound("No token header")

    # Распарсить атрибуты
    winner_id = request.GET.get('winner_id', '')
    loser_id = request.GET.get('loser_id', '')

    # Записать в бд
    change_score_points(winner_id, loser_id)
    r = create_new_event(winner_id, loser_id)
    resp = {
        'response': r,
        'wid': winner_id,
        'lid': loser_id,
    }
    return JsonResponse(resp)


#+POST 127.0.0.1/events/registration
def register_new(request):
    if request.method == 'POST':
        req_body = request.POST['ds_id']
        sha = get_sha_by_ds_id_or_create(req_body)
        resp = {
            'response': 'success',
            'sha': sha
        }
        return JsonResponse(resp)


# 127.0.0.1/events/stat?id=foo
def stat(request):
    param = request.GET.get('ds_id', '')
    try:
        user = get_user_obj_from_db_by_ds_id(param)
        resp = {
            'response': 'success',
            'user_name': user.user_name,
            'game_count': user.game_count,
            'score': user.user_score
        }
        return JsonResponse(resp)
    except:
        resp = {
            'response': 'id dont exist'
        }
        return JsonResponse(resp)


# 127.0.0.1/events/newevent
def new_events_for_bot(request):
    res = return_oldest_event()
    resp = {
        'response': 'success',
        'oldest_event': res
    }
    return JsonResponse(resp)


def wipe_rating(request):
    wipe_all()
    return HttpResponse('All players was wiped')


def leaderboard(request):
    dct = {
        'response': 'success',
        'items': top_50_players()
    }
    return JsonResponse(dct)