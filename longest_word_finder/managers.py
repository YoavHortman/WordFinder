from django.db import models
from django.apps import apps


class ActionManager(models.Manager):
    def get_user_points(self, user):
        user_actions = self.get_all_user_actions(user)
        point_sum = 0
        for action in user_actions:
            point_sum += action.type.points_gained_per_action

        return point_sum

    def get_all_user_actions(self, user):
        return super(ActionManager, self).get_queryset().filter(user=user)



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

#
# def is_word_relevant(len_word, len_word_pool, amount_wild_cards, constraint_indexes, longest_word):
#     is_longer_than_constraint = True
#     if len(constraint_indexes) > 0:
#         is_longer_than_constraint = max(constraint_indexes) < len_word
#
#     is_as_long_as_last_longest = len_word >= len(longest_word)
#     is_shorter_or_equal_to_pool = len_word <= len_word_pool + amount_wild_cards + len(constraint_indexes)
#
#     return is_as_long_as_last_longest and is_shorter_or_equal_to_pool and is_longer_than_constraint
#
#
# def find_longest_word_optimal(word, word_pool, wild_cards, indexes, chars):
#     wild_counter = 0
#     is_valid = False
#
#     if is_word_relevant(len(word), len(word_pool), wild_cards, indexes) \
#             and is_word_within_constraints(word, indexes, chars):
#
#         is_valid = True
#         holder = word_pool
#         for letter in word:
#             if letter not in holder and letter not in chars:
#                 wild_counter += 1
#                 if wild_counter > wild_cards:
#                     is_valid = False
#                     break
#             else:
#                 holder = holder.replace(letter, "", 1)
#
#     return is_valid
#
#
# def is_word_within_constraints(word, indexes, chars):
#     if indexes is not None and chars is not None:
#         for index, char in zip(indexes, chars):
#             if word[index] is not char:
#                 return False
#
#     return True
