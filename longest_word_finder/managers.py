import redis
from django.db import models
from django.apps import apps
from wordfinder.utils import GeneralUtils


class ActionManager(models.Manager):
    def get_user_points(self, user):
        user_actions = self.get_all_user_actions(user)
        point_sum = 0
        for action in user_actions:
            point_sum += action.type.points_gained_per_action

        return point_sum

    def get_all_user_actions(self, user):
        return super(ActionManager, self).get_queryset().filter(user=user)

    def add_words(self, user, words):
        unique_words = []
        text = words.split()

        for word in text:
            if word.isalpha() and word not in unique_words:
                unique_words.append(word.lower())

        redis_conn = redis.Redis()
        for word in unique_words:
            redis_conn.rpush(GeneralUtils.REDIS_DB_NAME, word)

        super(ActionManager, self).get_queryset()


class WordManager(models.Manager):
    def find_longest_word_optimal(self, word_pool, wild_cards, indexes, chars):
        wild_counter = 0
        redis_conn = redis.Redis()
        to_return = []
        max_len = len(word_pool) + wild_cards + len(indexes)

        for coded_word in redis_conn.lrange(GeneralUtils.REDIS_DB_NAME, 0, -1):
            word = coded_word.decode()
            if self.__is_word_correct_length__(len(word), max_len, indexes) \
                    and self.__is_word_within_constraints__(word, indexes, chars):

                is_valid = True
                holder = word_pool
                for letter in word:
                    if letter not in holder and letter not in chars:
                        wild_counter += 1
                        if wild_counter > wild_cards:
                            is_valid = False
                            break
                    else:
                        holder = holder.replace(letter, "", 1)

                if is_valid:
                    to_return.append(word)

        return to_return

    def __is_word_correct_length__(self, len_word, max_len, constraint_indexes):
        is_longer_than_constraint = (len(constraint_indexes) == 0 or max(constraint_indexes) < len_word)

        is_shorter_or_equal_to_pool = len_word <= max_len

        return is_shorter_or_equal_to_pool and is_longer_than_constraint

    def __is_word_within_constraints__(self, word, indexes, chars):
        if len(indexes) > 0:
            for index, char in zip(indexes, chars):
                if word[index] is not char:
                    return False

        return True


@staticmethod
def get_user_rank(points):
    ranks = Rank.objects.filter(points__lte=points)

    # Last rank is users rank
    return ranks[len(ranks) - 1]


@staticmethod
def get_user_next_rank(points):
    return Rank.objects.filter(points__gte=points)[0]


@staticmethod
def get_all_user_actions_of_type(user, action_type):
    return Action.objects.filter(user_id=user.id, type=action_type)


@staticmethod
def get_actions_for_word(word):
    return Action.objects.filter(word=word)


@staticmethod
def get_actions_of_type_for_word(word, action_type):
    return Action.objects.filter(word=word, type=action_type)


@staticmethod
def get_all_action_types():
    return ActionType.objects.all()


@staticmethod
def get_longest_words(pool, wild_amount, constraint_indexes, constraint_chars):
    longest_word = ""
    Word.objects.filter()
