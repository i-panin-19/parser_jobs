Курсовая работа "Парсер вакансий".

Принцип работы программы:
1. Запустите main.py.
2. Следуйте запросам программы (возможны ошибки, обработчик исключений в разработке).
3. Фильтрация производится по двум параметрам: from >= зп; to <= зп.
4. Результат выполнения запросов отображается в консоли.
5. Есть возможность сохранения и очистки справочников.
6. Парсер закольцован в цикл.

>apy_classes.py содержит все классы для работы с api сервисов!
> 
>parser_class.py содержит класс для работы со справочниками
> 
>funcs.py необходимые функции для работы с классами и их экземплярами
> 
>main.py утилита и главный файл (дальнейшее наращивание функционала позволит создать отдельный файлы с функциями)
> 
>HH_docs, SJ_docs каталоги для хранения справочников json, создаются самостоятельно