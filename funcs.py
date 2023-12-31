from api_classes import *
from parser_class import *
import os

def create_folders():
    """
    Функция создания директорий для справочников
    :return:
    """

    if not os.path.isdir("HH_docs"):
        os.mkdir("HH_docs")
    if not os.path.isdir("SJ_docs"):
        os.mkdir("SJ_docs")

def user_input():

    #пользователь вводит ключевое слово
    vacancy = input('\nВведите ключевое слово:\n').lower()
    #vacancy = 'Python'
    while vacancy != 'выход':
        hh_data = GetApiHH(vacancy)
        sj_data = GetApiSJ(vacancy)

        hh_data.get_vacancy()
        sj_data.get_vacancy()

        base_obj_hh = VacancyParser()
        base_obj_hh.create_obj_hh()
        base_obj_sj = VacancyParser()
        base_obj_sj.create_obj_sj()

        hh_input = input('\nВывести результаты поиска HeadHunter.ru? Да/Нет\n').lower()
        if hh_input == 'да':
            base_obj_hh.print_obj(0)

        sj_input = input('\nВывести результаты поиска SuperJob.ru? Да/Нет\n').lower()
        if sj_input == 'да':
            base_obj_sj.print_obj(1)

        salary_filt = input('\nПроизвести фильтрацию данных по ЗП? Да/Нет\n')
        if salary_filt == 'да':
            s_from = int(input('\nВведите сумму "от":\n'))
            s_to = int(input('\nВведите сумму "до":\n'))
            base_obj_hh.user_salary_filt(s_from, s_to, 0)
            base_obj_sj.user_salary_filt(s_from, s_to, 1)

        del_base = input('\nОчистить базу данных? Да/Нет\n').lower()
        if del_base == 'да':
            hh_data.clear_base()
            sj_data.clear_base()
            print('\nБаза данных удалена.\n')

        vacancy = input('\nВведите ключевое слово ("выход" - завершить работу программы):\n').lower()
