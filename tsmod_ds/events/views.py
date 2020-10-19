from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
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
    return


# POST 127.0.0.1/events/registration
def register_new(request):
    if request.method == 'POST':
        req_body = request.body.decode()
        sha = get_ds_id_or_create_sha(req_body)
        resp = {
            'response': sha
        }
        return JsonResponse(resp)


# 127.0.0.1/events/stat?id=foo
def stat(request):
    param = request.GET.get('id', '')
    try:
        user = get_user_obj_from_db(param)
        resp = {
            'user_name': user.user_name,
            'game_count': user.game_count,
            'score': user.user_score
        }
        return JsonResponse(resp)
    except:
        resp = {
            'Error': 'id dont exist'
        }
        return JsonResponse(resp)


# 127.0.0.1/events/newevent
def new_events_for_bot(request):
    res = return_oldest_event()
    resp = {
        'oldest_event': res
    }
    return JsonResponse(resp)
