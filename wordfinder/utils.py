import redis


class GeneralUtils:
    REDIS_DB_NAME = 'words'


    # Maybe add types of action to DB
    @staticmethod
    def get_all_action_types():
        from longest_word_finder.models import ActionType

        pass


class StartUp:
    @staticmethod
    def start_up_code():
        from longest_word_finder.models import Word

        redis_conn = redis.Redis()
        coded_words = redis_conn.lrange(GeneralUtils.REDIS_DB_NAME, 0, -1)
        existing_words = []

        for coded_word in coded_words:
            existing_words.append(coded_word.decode())

        for word in Word.objects.all():
            if word.word not in existing_words:
                redis_conn.lpush(GeneralUtils.REDIS_DB_NAME, word.word.lower())
