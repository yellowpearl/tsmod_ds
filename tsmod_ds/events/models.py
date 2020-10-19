from django.db import models
import hashlib


def get_user_obj_from_db(name):
    """return user obj from db where user_name=name"""
    user = UserScore.objects.get(hash_id=name)
    return user


def check_token_in_db(token):
    """check token name in db and return True or False"""
    try:
        true_or_false = Token.objects.get(token_name=token)
        return True
    except:
        return False


def plus_score_points(user):

    game_counter = user.game_count
    if game_counter <= 10:
        score = user.user_score
        user.user_score = score + 100
        user.save()
        return 0
    else:
        score = user.user_score
        first_player = UserScore.objects.order_by('-user_score')[0]
        last_player = UserScore.objects.order_by('user_score')[0]
        difference = (first_player.user_score - last_player.user_score) // 100
        if first_player.hash_id == id:
            user.user_score = score + 25 - difference
            user.save()
            return 0
        user.user_score = score + 25 + difference
        user.save()
        return 0


def minus_score_points(user):
    game_counter = user.game_count
    if game_counter <= 10:
        score = user.user_score
        user.user_score = score - 100
        user.save()
        return 0
    else:
        score = user.user_score
        first_player = UserScore.objects.order_by('-user_score')[0]
        last_player = UserScore.objects.order_by('user_score')[0]
        difference = (first_player.user_score - last_player.user_score) // 100
        if last_player.hash_id == id:
            user.user_score = score - 25 + difference
            user.save()
            return 0
        user.user_score = score - 25 - difference
        user.save()
        return 0


def change_score_points(w_id, l_id):
    try:
        user_w = get_user_obj_from_db(w_id)
        user_l = get_user_obj_from_db(l_id)
        plus_score_points(user_w)
        minus_score_points(user_l)
        return
    except:
        return


def create_new_event(w_id, l_id):
    try:
        user_w = get_user_obj_from_db(w_id)
        user_l = get_user_obj_from_db(l_id)
        new_string = f'{user_w.user_name} победил {user_l.user_name}'
        NewEvents.objects.create(new_string=new_string)
        return new_string
    except:
        return


def return_oldest_event():
    last = NewEvents.objects.order_by('pk')[0]
    event_string = last.news_string
    last.delete()
    return event_string


def get_ds_id_or_create_sha(ds_id):
    try:
        user = UserScore.objects.get(user_name=ds_id)
        return user.hash_id
    except:
        return hash_ds_id(ds_id)


def hash_ds_id(ds_id):
    while True:
        sha_obj = hashlib.sha1(ds_id.encode('utf-8'))
        sha = sha_obj.hexdigest()[-12:]
        try:
            user = UserScore.objects.get(hash_id=sha)
        except:
            UserScore.objects.create(user_name=ds_id, hash_id=sha, game_count=0, user_score=1500)
            return sha


class UserScore(models.Model):
    user_name = models.CharField(max_length=64, unique=True, blank=False)
    hash_id = models.CharField(max_length=64, unique=True, blank=False)
    game_count = models.IntegerField(default=0)
    user_score = models.IntegerField(default=1500)

    def __str__(self):
        return self.user_name


class Token(models.Model):
    token_name = models.CharField(max_length=2048)

    def __str__(self):
        return self.token_name[:8]


class NewEvents(models.Model):
    news_string = models.CharField(max_length=64)
