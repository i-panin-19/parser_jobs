from abc import ABC, abstractmethod
import requests
import json
import time
import os


class CoreClasses(ABC):

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancy(self):
        pass

    @abstractmethod
    def clear_base(self):
        pass


class GetApiHH(CoreClasses):
    """
    Класс для работы с API hh.ru
    """
    url = 'https://api.hh.ru/vacancies'
    page = 0

    def __init__(self, user_vacancy):
        self.params = {
            'text': f'NAME:{user_vacancy}',
            'page': self.page,
            'per_page': 100,
            'archived': False,
        }

    def get_request(self):
        """
        Внутренний метод создания страницы со списком вакансий. Осуществляет запрос и возвращает страницу из 100 вакансий
        :return:
        """

        req = requests.get(self.url, self.params)
        data = req.content.decode()
        req.close()
        self.params['page'] += 1

        return data

    def get_vacancy(self):
        """
        Метод преобразует первые 10 страниц в справочник.
        Каждая страница сохраняется под имененем текущей страницы в цикле.
        Создаем новый документ, записываем в него ответ запроса, после закрываем.
        :return:
        """

        for page in range(0, 10):
            jsObject = json.loads(self.get_request())
            FileName = './HH_docs/{}.json'.format(len(os.listdir('./HH_docs')))

            f = open(FileName, mode='w', encoding='utf8')
            f.write(json.dumps(jsObject, ensure_ascii=False))
            f.close()

            #проверка на последнюю страницу, когда вакансий меньше 1000
            if (jsObject['pages'] - page) <= 1:
                break

            #небольшая задержка, во избежании перегрузки сервера
            time.sleep(0.25)
        print('Файлы HeadHunter собраны!')

    def clear_base(self):
        """
        Очистка папок со справочниками
        :return:
        """

        dirHH = os.listdir('./HH_docs')
        for f in dirHH:
            os.remove(os.path.join('./HH_docs', f))


def sj_key_keeper():
    """
        Функция хранения ключа через строку или переменную среды
        :return:
        """

    sj_key = os.getenv('SJ_KEY')

    if sj_key == None:
        sj_key = 'v3.r.137590044.f2f7d5ef9df7fed349ce1169d6fe115e22285ff9.c727331886d1671df92bcc8579b84a5c801994b2'

    return sj_key


class GetApiSJ(CoreClasses):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    page = 0
    sj_key = sj_key_keeper()
    headers = {
        'X-Api-App-Id': sj_key
    }

    def __init__(self, user_vacancy):
        self.params = {
            #'profession' ???
            'keyword': user_vacancy,
            'page': self.page,
            'count': 100,
            'archived': False,
        }

    def get_request(self):
        req = requests.get(self.url, headers=self.headers, params=self.params)
        data = req.content.decode()
        req.close()
        self.params['page'] += 1

        return data

    def get_vacancy(self):
        for page in range(0, 10):
            jsObject = json.loads(self.get_request())
            FileName = './SJ_docs/{}.json'.format(len(os.listdir('./SJ_docs')))

            f = open(FileName, mode='w', encoding='utf8')
            f.write(json.dumps(jsObject, ensure_ascii=False))
            f.close()

            #остановка цикла с пустыми страницами
            if len(jsObject) == 0:
                break

            time.sleep(0.25)
        print('Файлы SuperJob собраны!')

    def clear_base(self):
        dirSJ = os.listdir('./SJ_docs')
        for f in dirSJ:
            os.remove(os.path.join('./SJ_docs', f))
