import os

from redis import StrictRedis


class RedisDB:
    """
    Сервис для удобного взаимодействия с базой данных Redis
    """
    def __init__(self):
        self.store = StrictRedis(
            host=os.getenv('REDIS_HOST', '127.0.0.1'),
            port=os.getenv('REDIS_PORT', '6379')
        )

    def _get_unix_time(self) -> int:
        """
        Метод, возвращающий текущее время в unix формате (количество секунд)
        :return: unix time (int format)
        """
        return self.store.execute_command('TIME')[0]

    def zadd_with_unix_time(self, key: str, values: list) -> int:
        """
        Модифицированный метод zadd для удобного хранения ссылок под одним ключом, но с разными значениями (value)
        и информацией о времени в формате unix в виде score
        :param key: Ключ
        :param values: Значения
        :return: Количество добавленных значений
        """
        score = self._get_unix_time()
        values_score = {value: score for value in values}
        return self.store.zadd(key, values_score)

    def zrangebyscore_by_unix_time(self, key: str, from_unix_time: int, to_unix_time: int) -> list:
        """
        Модифицированный метод zrangebyscore, который преобрзаует байтовые строки в обычные и производит фильтрацию
        по unix времени, который хранится в score
        :param key: Ключ
        :param from_unix_time: Начало указанного промежутка времени
        :param to_unix_time: Конец указанного промежутка времени
        :return: Отфильтрованный список с обыными строками
        """
        links = self.store.zrangebyscore(key, from_unix_time, to_unix_time)
        decoded_links = []
        for link in links:
            decoded_links.append(link.decode('UTF-8'))
        return decoded_links
