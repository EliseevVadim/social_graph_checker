import vk_api
from vk_api import VkApi

from constants import *
from core.tools import create_dataframe


def auth():
    token = API_KEY
    session = vk_api.VkApi(token=token)
    api = session.get_api()
    return api


def get_friends_list(api: VkApi, return_as_dataframe=False):
    result = api.friends.get(
        user_id=ID,
        fields='nickname'
    )
    friends = result['items']
    friends = [friend for friend in friends if 'deactivated' not in friend]
    if return_as_dataframe:
        df = create_dataframe(friends, keys=['id', 'first_name', 'last_name'])
        return df
    return friends


def calculate_mean_path_length(friends: list[dict]):
    calculating_friends = friends.copy()
    calculating_friends.append({
        'id': ID,
        'mutual_count': 0
    })
    friends_count = len(calculating_friends)
    mean_path_length = sum(
        calculate_friend_path_rating(friend=friend, friends_count=len(friends))
        for friend in calculating_friends
    )
    mean_path_length /= (friends_count * (friends_count - 1))
    return mean_path_length


def calculate_friend_path_rating(friend, friends_count: int):
    mutual_count = friend['mutual_count']
    rating = mutual_count + (friends_count - mutual_count) * 2
    return rating


def get_farthest_connection(friends: list[dict]):
    min_mutual_friends_count = min(friend['mutual_count'] for friend in friends)
    required_friends_count_for_full_connection = len(friends)
    farthest_connection = 2 if min_mutual_friends_count < required_friends_count_for_full_connection else 1
    return farthest_connection


def get_mutual_count_with(api: VkApi, user_id):
    result = api.friends.getMutual(
        source_uid=ID,
        target_uid=user_id
    )
    return len(result)


def get_friends_count(api: VkApi, user_id):
    result = api.friends.get(
        user_id=user_id
    )
    return result['count']
