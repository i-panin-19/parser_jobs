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
        req = requests.get(self.url, self.params)
        data = req.content.decode()
        req.close()
        self.params['page'] += 1

        return data

    def get_vacancy(self):
        for page in range(0, 10):
            jsObject = json.loads(self.get_request())
            FileName = './HH_docs/{}.json'.format(len(os.listdir('./HH_docs')))

            f = open(FileName, mode='w', encoding='utf8')
            f.write(json.dumps(jsObject, ensure_ascii=False))
            f.close()

            if (jsObject['pages'] - page) <= 1:
                break

            time.sleep(0.25)
        print('Файлы HeadHunter собраны!')

    def clear_base(self):
        dirHH = os.listdir('./HH_docs')
        for f in dirHH:
            os.remove(os.path.join('./HH_docs', f))


class GetApiSJ(CoreClasses):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    page = 0
    headers = {
        'X-Api-App-Id': 'v3.r.137590044.f2f7d5ef9df7fed349ce1169d6fe115e22285ff9.c727331886d1671df92bcc8579b84a5c801994b2'
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

            if len(jsObject) == 0:
                break

            time.sleep(0.25)
        print('Файлы SuperJob собраны!')

    def clear_base(self):
        dirSJ = os.listdir('./SJ_docs')
        for f in dirSJ:
            os.remove(os.path.join('./SJ_docs', f))


class VacancyParser:
    base_obj_hh = []
    base_obj_sj = []
    def __init__(self):
        self.vacancy = None
        self.url = None
        self.salary = None
        self.experience = None
        self.id = None

    def create_obj_hh(self):
        for fl in os.listdir('./HH_docs'):
            f = open('./HH_docs/{}'.format(fl), encoding='utf8')
            jsonText = f.read()
            f.close()

            json_obj = json.loads(jsonText)
            for v in json_obj['items']:

                # сохранение зп
                salary_temp = []
                salary_obj = v['salary']
                if salary_obj == None:
                    salary_temp = [0, 0, 0]
                else:
                    if salary_obj['from'] == None:
                        salary_temp.append(0)
                    else:
                        salary_temp.append(salary_obj['from'])
                    if salary_obj['to'] == None:
                        salary_temp.append(0)
                    else:
                        salary_temp.append(salary_obj['to'])
                    salary_temp.append(salary_obj['currency'])

                # сохранение опыта работы
                experience_temp = ''
                experience_obj = v['experience']
                if experience_obj == None:
                    experience_temp = '-'
                else:
                    experience_temp = experience_obj['name']

                # сохранение id
                id_temp = v['id']

                # сохранение url
                url_temp = v['alternate_url']

                # сохранение описания профессии
                name_temp = v['name']

                obj = VacancyParser()
                obj.vacancy = name_temp
                obj.url = url_temp
                obj.salary = salary_temp
                obj.experience = experience_temp
                obj.id = id_temp
                self.base_obj_hh.append(obj)

                #print(salary_temp, experience_temp, id_temp, url_temp, name_temp)

        return self.base_obj_hh

    def create_obj_sj(self):
        for fl in os.listdir('./SJ_docs'):
            f = open('./SJ_docs/{}'.format(fl), encoding='utf8')
            jsonText = f.read()
            f.close()

            json_obj = json.loads(jsonText)
            for v in json_obj['objects']:

                # сохранение зп
                salary_temp = []
                salary_temp.append(v['payment_from'])
                salary_temp.append(v['payment_to'])
                salary_temp.append(v['currency'])

                # сохранение опыта работы
                experience_temp = v['experience']['title']

                # сохранение id
                id_temp = v['id']

                # сохранение url
                url_temp = v['link']

                # сохранение описания профессии
                name_temp = v['profession']

                obj = VacancyParser()
                obj.vacancy = name_temp
                obj.url = url_temp
                obj.salary = salary_temp
                obj.experience = experience_temp
                obj.id = id_temp
                self.base_obj_sj.append(obj)

        return self.base_obj_sj

    def print_obj(self, num_base):
        if num_base == 0:
            obj_base = self.base_obj_hh
        else:
            obj_base = self.base_obj_sj
        num = 0
        for obj in obj_base:
            tmp_str = ''
            num += 1
            if obj.salary != [0, 0, 0]:
                if obj.salary[0] != 0:
                    tmp_str = f'от {obj.salary[0]} '
                if obj.salary[1] != 0:
                    tmp_str += f'до {obj.salary[1]} '
                tmp_str += f'{obj.salary[2]}'
            else:
                tmp_str = ' - '
            print(
                f'{num} >>> {obj.vacancy}. -|- '
                f'Опыт: {obj.experience}. -|- '
                f'Зарплата: {tmp_str} -|- '
                f'ID: {obj.id} -|- '
                f'URL: {obj.url}'
            )

    def user_salary_filt(self, s_from, s_to, num_base):
        if num_base == 0:
            obj_base = self.base_obj_hh
        else:
            obj_base = self.base_obj_sj
        num = 0
        for obj in obj_base:
            if (int(obj.salary[0]) != 0 and int(obj.salary[0]) >= s_from) and (int(obj.salary[1]) != 0 and int(obj.salary[1] <= s_to)):
                tmp_str = f'от {obj.salary[0]} до {obj.salary[1]} {obj.salary[2]}'
                num += 1

                print(
                    f'{num} >>> {obj.vacancy}. -|- '
                    f'Опыт: {obj.experience}. -|- '
                    f'Зарплата: {tmp_str} -|- '
                    f'ID: {obj.id} -|- '
                    f'URL: {obj.url}'
                )
