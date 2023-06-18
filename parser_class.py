import json
import os


class VacancyParser:
    """
    Класс для работы со справочниками.
    Объекты класса помещаются во внутренние списки
    """


    base_obj_hh = []
    base_obj_sj = []
    def __init__(self):
        self.vacancy = None
        self.url = None
        self.salary = None
        self.experience = None
        self.id = None

    def create_obj_hh(self):
        """
        Создание экземпляров класса.
        Считывание страницы из папки.
        Обработка строки, преобразование в читаемый вид.
        Создание объекта и помещение его во внутренний список класса
        :return:
        """

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
        """
        Печать справочников.
        Получение на вход номера справочника (0 для hh и 1 для sj)
        :param num_base:
        Преобразование данных в читаемые строки
        :return:
        """

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
        """
        Небольшой фильтро по ЗП
        Получение на вход ЗП от и до. А так же номера справочника.
        :param s_from:
        :param s_to:
        :param num_base:
        :return:
        """

        if num_base == 0:
            obj_base = self.base_obj_hh
        else:
            obj_base = self.base_obj_sj
        num = 0
        for obj in obj_base:

            #условие учитывает только полные данные по ЗП, 0 пропускается
            if (int(obj.salary[0]) != 0 and int(obj.salary[0]) >= s_from) and (int(obj.salary[1]) != 0 and int(obj.salary[1] <= s_to)):
                tmp_str = f'от {obj.salary[0]} до {obj.salary[1]} {obj.salary[2]}'
                num += 1

                #вывод на экран прошедших условие данных
                print(
                    f'{num} >>> {obj.vacancy}. -|- '
                    f'Опыт: {obj.experience}. -|- '
                    f'Зарплата: {tmp_str} -|- '
                    f'ID: {obj.id} -|- '
                    f'URL: {obj.url}'
                )

    def __repr__(self):
        return f"{self.__class__}: {self.vacancy}"

    def __str__(self):
        return f'{self.id}, {self.url}'
