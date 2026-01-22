# Читает все непустые строки из текстового файла, удаляя символы новой строки
def read_file(name):
    try:
        with open(name, 'r', encoding='utf-8') as f:
            return [line.rstrip('\n') for line in f if line.strip()]
    except:
        return None


# Разбивает строку по запятым
def split_line(s):
    return s.split(',')


# Преобразует строку в целое число. Возвращает None при ошибке или пустой строке
def to_int(s):
    s = s.strip()
    if not s:
        return None
    try:
        return int(s)
    except ValueError:
        return None


# Переводит строку в нижний регистр (русский и английский).
def lower_str(s):
    return s.lower()


# Форматирует ФИО: с отчеством — "Иванов И.И.", без — "Петрова А."
def format_fio(a):
    fio = a['fam'] + " " + a['im'][0] + "."
    if a['otch'].strip():
        fio += a['otch'][0] + "."
    return fio


# Шейкерная сортировка списка по ключу
def shaker_sort(arr, key_func):
    n = len(arr)
    if n <= 1:
        return

    left = 0
    right = n - 1
    swapped = True

    while swapped:
        swapped = False
        for i in range(left, right):
            if key_func(arr[i]) > key_func(arr[i + 1]):
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        if not swapped:
            break

        right -= 1

        for i in range(right, left, -1):
            if key_func(arr[i]) < key_func(arr[i - 1]):
                arr[i], arr[i - 1] = arr[i - 1], arr[i]
                swapped = True

        left += 1


# Проверка даты

# Проверяет, является ли год високосным.
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


# Возвращает количество дней в месяце (с учётом високосного года)
def days_in_month(month, year):
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif month in (4, 6, 9, 11):
        return 30
    elif month == 2:
        return 29 if is_leap_year(year) else 28
    else:
        return 0  # недопустимый месяц


# Проверяет корректность даты
def is_valid_date(year, month, day):
    if not (1900 <= year <= 2025):
        return False
    if not (1 <= month <= 12):
        return False
    if not (1 <= day <= days_in_month(month, year)):
        return False
    return True


# Загрузка и сохранение файла

# Проверяет корректность данных одного соискателя. Возвращает словарь или None.
def validate_applicant(data, line_num):
    if len(data) != 11:
        print(f"Строка {line_num}: должно быть 11 полей")
        return None

    fam, im, otch, pol, y, m, d, spec, staj, lang, oklad = data

    if not fam.strip() or not im.strip():
        print(f"Строка {line_num}: фамилия и имя обязательны")
        return None

    if pol not in ('М', 'Ж'):
        print(f"Строка {line_num}: пол должен быть 'М' или 'Ж'")
        return None

    year = to_int(y)
    month = to_int(m)
    day = to_int(d)
    exp = to_int(staj)
    salary = to_int(oklad)

    if None in (year, month, day, exp, salary):
        print(f"Строка {line_num}: ошибка в числовых данных")
        return None

    if exp < 0 or salary < 0:
        print(f"Строка {line_num}: стаж и оклад не могут быть отрицательными")
        return None

    if not is_valid_date(year, month, day):
        print(f"Строка {line_num}: некорректная дата рождения")
        return None

    return {
        'fam': fam,
        'im': im,
        'otch': otch,  # может быть пустой строкой
        'pol': pol,
        'year': year,
        'month': month,
        'day': day,
        'spec': lower_str(spec),
        'staj': exp,
        'lang': lang,
        'oklad': salary
    }


# Загружает соискателей из файла со всей информацией
def load_from_file(filename):
    lines = read_file(filename)
    if lines is None:
        print(f"Файл '{filename}' не найден. База будет пустой.")
        return []

    people = []
    for i, line in enumerate(lines, start=1):
        parts = split_line(line)
        applicant = validate_applicant(parts, i)
        if applicant is not None:
            people.append(applicant)
    return people


# Сохраняет текущую базу в файл
def save_to_file(filename, applicants):
    fields = ['fam', 'im', 'otch', 'pol', 'year', 'month', 'day', 'spec', 'staj', 'lang', 'oklad']
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for a in applicants:
                line = ','.join(str(a[key]) for key in fields)
                f.write(line + '\n')
        print(f"Данные сохранены в '{filename}'.")
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")


# Функции для управления базой данных

applicants = []


# Добавляет новую запись о соискателе с проверкой всех полей, включая дату рождения.
def add_record():
    print("\n Добавление нового соискателя:")
    fam = input("Фамилия: ").strip()
    im = input("Имя: ").strip()
    otch = input("Отчество (если есть): ").strip()

    while not (fam and im):
        print("Фамилия и имя обязательны.")
        fam = input("Фамилия: ").strip()
        im = input("Имя: ").strip()
        if not otch:
            otch = input("Отчество (если есть): ").strip()

    pol = input("Пол (М/Ж): ").strip()
    while pol not in ('М', 'Ж'):
        print("Только 'М' или 'Ж'")
        pol = input("Пол (М/Ж): ").strip()

    # Ввод даты с проверкой
    while True:
        y = input("Год рождения: ").strip()
        m = input("Месяц рождения: ").strip()
        d = input("День рождения: ").strip()

        year = to_int(y)
        month = to_int(m)
        day = to_int(d)

        if None in (year, month, day):
            print("Ошибка: все части даты должны быть целыми числами.")
            continue

        if is_valid_date(year, month, day):
            break
        else:
            print("Некорректная дата! Проверьте:")
            print("Год: 1900–2025")
            print("Месяц: 1–12")
            print("День: не больше количества дней в месяце (февраль — 28/29)")

    spec = input("Специальность: ").strip()
    while not spec:
        spec = input("Специальность (обязательно): ").strip()
    spec = lower_str(spec)

    staj = input("Стаж (лет): ").strip()
    lang = input("Языки (через пробел): ").strip() or "—"
    oklad = input("Ожидаемый оклад: ").strip()

    exp = to_int(staj)
    salary = to_int(oklad)

    if None in (exp, salary) or exp < 0 or salary < 0:
        print("Стаж и оклад должны быть неотрицательными целыми числами.")
        return

    applicants.append({
        'fam': fam,
        'im': im,
        'otch': otch,
        'pol': pol,
        'year': year,
        'month': month,
        'day': day,
        'spec': spec,
        'staj': exp,
        'lang': lang,
        'oklad': salary
    })
    fio_display = format_fio(applicants[-1])
    print(f"Добавлен: {fio_display} ({day:02d}.{month:02d}.{year})")


# Печатает отчёт в компактном формате (без даты рождения) с нумерацией.
def print_report(lst):
    if not lst:
        print("Нет данных")
        return
    print("-" * 90)
    print(f"{'№':<3} {'ФИО':<20} {'Пол':<4} {'Специальность':<15} {'Стаж':<6} {'Оклад':<10} {'Языки'}")
    print("-" * 90)
    for idx, a in enumerate(lst, start=1):
        fio = format_fio(a)
        print(f"{idx:<3} {fio:<20} {a['pol']:<4} {a['spec']:<15} {a['staj']:<6} {a['oklad']:<10} {a['lang']}")


# Отображает всю базу соискателей в табличном виде с нумерацией.
def show_all():
    if not applicants:
        print("База пуста.")
        return
    print("\n Вся база:")
    print("-" * 100)
    print(f"{'№':<3} {'ФИО':<20} {'Пол':<4} {'Дата рожд.':<12} {'Специальность':<15} {'Стаж':<6} {'Оклад':<10} {'Языки'}")
    print("-" * 100)
    for idx, a in enumerate(applicants, start=1):
        fio = format_fio(a)
        birth = f"{a['day']:02d}.{a['month']:02d}.{a['year']}"
        print(f"{idx:<3} {fio:<20} {a['pol']:<4} {birth:<12} {a['spec']:<15} {a['staj']:<6} {a['oklad']:<10} {a['lang']}")


# Удаляет запись по фамилии или по номеру в списке
def delete_record():
    if not applicants:
        print("База пуста.")
        return
    show_all()
    choice = input("Введите номер записи или фамилию для удаления: ").strip()
    
    # Попробуем интерпретировать как номер
    idx = to_int(choice)
    if idx is not None and 1 <= idx <= len(applicants):
        deleted = applicants.pop(idx - 1)
        fio_display = format_fio(deleted)
        print(f"Удалён: {fio_display}")
        return

    # Иначе — ищем по фамилии
    for i, a in enumerate(applicants):
        if a['fam'] == choice:
            deleted = applicants.pop(i)
            fio_display = format_fio(deleted)
            print(f"Удалён: {fio_display}")
            return

    print("Запись не найдена.")


# Редактирует запись по фамилии или по номеру в списке
def edit_record():
    if not applicants:
        print("База пуста.")
        return
    show_all()
    choice = input("Введите номер записи или фамилию для редактирования: ").strip()

    # Попробуем интерпретировать как номер
    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(applicants):
            a = applicants[idx - 1]
            print(f"\nРедактирование записи №{idx}: {format_fio(a)}")
        else:
            print("Номер вне диапазона.")
            return
    else:
        # Ищем по фамилии
        a = None
        for applicant in applicants:
            if applicant['fam'] == choice:
                a = applicant
                break
        if a is None:
            print("Запись не найдена.")
            return
        print(f"\nРедактирование: {format_fio(a)}")

    # Редактируем запись `a`
    a['fam'] = input(f"Новая фамилия ({a['fam']}): ").strip() or a['fam']
    a['im'] = input(f"Новое имя ({a['im']}): ").strip() or a['im']
    new_otch = input(f"Новое отчество ({a['otch']}): ").strip()
    if new_otch != "":
        a['otch'] = new_otch

    new_pol = input(f"Новый пол ({a['pol']}): ").strip()
    if new_pol in ('М', 'Ж'):
        a['pol'] = new_pol

    # Редактирование даты с проверкой
    print(f"\nТекущая дата: {a['day']:02d}.{a['month']:02d}.{a['year']}")
    while True:
        new_y = input(f"Новый год ({a['year']}): ").strip()
        new_m = input(f"Новый месяц ({a['month']}): ").strip()
        new_d = input(f"Новый день ({a['day']}): ").strip()

        year = to_int(new_y) if new_y else a['year']
        month = to_int(new_m) if new_m else a['month']
        day = to_int(new_d) if new_d else a['day']

        if None in (year, month, day):
            print("Все части даты должны быть целыми числами.")
            continue

        if is_valid_date(year, month, day):
            a['year'], a['month'], a['day'] = year, month, day
            break
        else:
            print("Некорректная дата! Попробуйте снова.")

    new_spec = input(f"Новая специальность ({a['spec']}): ").strip()
    if new_spec:
        a['spec'] = lower_str(new_spec)

    new_staj = input(f"Новый стаж ({a['staj']}): ").strip()
    if new_staj:
        val = to_int(new_staj)
        if val is not None and val >= 0:
            a['staj'] = val

    new_oklad = input(f"Новый оклад ({a['oklad']}): ").strip()
    if new_oklad:
        val = to_int(new_oklad)
        if val is not None and val >= 0:
            a['oklad'] = val

    a['lang'] = input(f"Новые языки ({a['lang']}): ").strip() or a['lang']
    print("Запись обновлена.")


# Отчёты
def generate_reports():
    if not applicants:
        print("База пуста.")
        return

    # Отчёт 1
    r1 = [x.copy() for x in applicants]
    shaker_sort(r1, lambda x: (x['spec'], x['fam']))
    print("\n[1] Полный список (спец ↑, фам ↑)")
    print_report(r1)

    # Отчёт 2
    specs = list(set(a['spec'] for a in applicants))
    print("\nДоступные специальности:", ", ".join(sorted(specs)))
    s = input("Введите специальность: ").strip()
    s = lower_str(s)
    if s not in specs:
        print("Такой специальности нет.")
        return
    r2 = [x for x in applicants if x['spec'] == s]
    def key2(x):
        g = 1 if x['pol'] == 'М' else 0
        return (-x['staj'], -g, x['fam'])
    shaker_sort(r2, key2)
    print(f"\n[2] По специальности '{s}'")
    print_report(r2)

    # Отчёт 3
    n1 = input_num("Мин. оклад: ")
    n2 = input_num("Макс. оклад: ")
    if n1 > n2:
        n1, n2 = n2, n1
    r3 = [x for x in applicants if n1 <= x['oklad'] <= n2]
    shaker_sort(r3, lambda x: (-x['oklad'], x['fam']))
    print(f"\n[3] Оклад от {n1} до {n2}")
    print_report(r3)


# Ввод неотрицательного целого числа с повторным запросом при ошибке.
def input_num(prompt):
    while True:
        val = to_int(input(prompt).strip())
        if val is not None and val >= 0:
            return val
        print("Введите целое неотрицательное число.")


# Меню программы
def main_menu():
    print("=" * 60)
    print("КАДРОВОЕ АГЕНТСТВО")
    print("=" * 60)
    print("1. Показать всю базу")
    print("2. Добавить запись")
    print("3. Удалить запись")
    print("4. Изменить запись")
    print("5. Сформировать отчёты")
    print("6. Сохранить изменения в файл")
    print("0. Выход")

    while True:
        choice = input("\nВыбор: ").strip()
        if choice == '1':
            show_all()
        elif choice == '2':
            add_record()
        elif choice == '3':
            delete_record()
        elif choice == '4':
            edit_record()
        elif choice == '5':
            generate_reports()
        elif choice == '6':
            save_to_file("soiskateli.txt", applicants)
        elif choice == '0':
            if input("Сохранить изменения перед выходом? (д/н): ").strip().lower() in ('д', 'y', 'yes', ''):
                save_to_file("soiskateli.txt", applicants)
            print("До свидания!")
            break
        else:
            print("Неверный выбор.")


# Загрузка данных и запуск меню
if __name__ == "__main__":
    applicants = load_from_file("soiskateli.txt")
    print(f"Загружено {len(applicants)} записей из файла 'soiskateli.txt'.")
    main_menu()
