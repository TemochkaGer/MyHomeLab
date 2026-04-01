import matplotlib.pyplot as plt
import numpy as np
import math

Student_coefficient = {
    2: 12.71,
    3: 4.30,
    4: 3.188,
    5: 2.77,
    6: 2.57,
    7: 2.45,
    8: 2.36,
    9: 2.31,
    10: 2.26,
    12: 2.20,
    14: 2.16,
    16: 2.13,
    18: 2.11,
    20: 2.09,
    30: 2.04,
    40: 2.02,
    50: 2.01,
    60: 2.00,
    100: 1.96
}

def lin_mass():
    """Функция принимает линейный массив и тривиально его обрабатывает для дальнейшей работы"""
    
    edin_izm = input('Введите единицы измерения в которых вы работаете:')
    
    while True:
        try:
            err = float(input('Введите приборную погрешность (Если нет, ничего не вводите): '))
            break
        except ValueError:
            print('Вы веди не правильное значение приборной погрешности, использовано значение 0!')
            instrument_error = 0.0
            break
    
    instrument_error = err
    start_input = []
        
# Заполнение одномерного массива эксперементальных значений

    while True:
        a = input('Введите по очереди результаты вашего эксперемента, иначе напишите Стоп: ')
        try:
            if a != 'Стоп':
                start_input.append(float(a))
            else:
                break
        except ValueError:
            print('Пожалуйста вводите только числа')
            continue
        
    try:
        sredn_stat = sum(start_input) / len(start_input) #Среднестатистическое значение результатов измерения(одного и того же опыта)
    
    except ZeroDivisionError:
        print('Не, Мишаня, всё хуйня, давай по новой!')
        
    count = 0
    
    for i in range(len(start_input)):
        if start_input[i] == 0:
            count += 1
            
    if count == len(start_input):
        return 'Весь массив состоит из нулей!\nВсё заново!'
    else:
        return start_input, edin_izm, instrument_error, sredn_stat
    
def sredn_kvard(start_input, sredn_stat):
    """Подстчёт среднеквадратического отклонения результатов одного эксперемента"""
    
    chislit = 0
    for i in range(len(start_input)):
        chislit += (float(start_input[i]) - sredn_stat) ** 2
        
    if (chislit / (len(start_input) * (len(start_input) - 1))) > 0:
        return (chislit / (len(start_input) * (len(start_input) - 1))) ** 0.5
    else:
        return "Видимо где - то ошибка! Долбаёб..."
   
def random_error(start_input, sr_kv):
    """Расчёт случайной погрешности"""
    
    global Student_coefficient

    alfa = 0
    
    # Находжение коэффициента Стьюдента на основе одноименного глобального массива (Сто процентов есть ошибка -- нужно ужесточить условие выбора значение ключа)
    try:
        if len(start_input) <= 60 and len(start_input) >= 2:
            for i in Student_coefficient.keys():
                if len(start_input) == i:
                    alfa = Student_coefficient[len(start_input)]
                    break
        else: 
            alfa = Student_coefficient[100]
            
        return float(alfa * sr_kv)
    except TypeError:
        return 'Ошибка типизации. Скорее всего ты указал массив из одних и тех же чисел'

def error(instrument_error, rand_err):
    """Подсчёт полной погрешности измерений и вывод среднего значения с абсолютной погрешностью"""
    
    return (instrument_error ** 2 + rand_err ** 2) ** 0.5

def relative_error(err, sredn_stat):
    """Подсчёт отностительной погрешности и её возвращение"""
    
    return err / sredn_stat

def miss(start_input):
    """Анализ промахов с использованием критерия Стьюдента"""
    global Student_coefficient
    
    try:
        doubtful = float(input('Введите число для проверки на промах: '))
        if doubtful not in start_input:
            return start_input, "Указанное значение отсутствует в данных"
            
        # Создаем копию без проверяемого значения
        filtered_data = [x for x in start_input if x != doubtful]
        if not filtered_data:
            return start_input, "Нельзя удалить все значения"
            
        mean_filtered = sum(filtered_data) / len(filtered_data)
        n = len(start_input)
        
        # Вычисляем коэффициент Стьюдента
        degrees_of_freedom = n - 2  # Число степеней свободы
        alfa = Student_coefficient.get(degrees_of_freedom, Student_coefficient[100])
        
        # Вычисляем дисперсию
        variance = sum((x - mean_filtered)**2 for x in filtered_data)
        
        # Критическое отклонение
        critical_deviation = alfa * (n * variance / ((n - 1) * (n - 2)))**0.5
        
        if abs(mean_filtered - doubtful) > critical_deviation:
            return filtered_data, f"Значение {doubtful} является промахом и было удалено"
        else:
            return start_input, f"Значение {doubtful} находится в допустимых пределах"
            
    except ValueError:
        return start_input, "Ошибка: введите корректное число"
    except Exception as e:
        return start_input, f"Произошла ошибка: {str(e)}"
        
# Косвеные измерения

def mass():
    """Заполнение двумерного массива эксперементальных значений"""
    
    massive = []
    
    n = int(input('Введите количество точек, которые вы измерили - это характеризует количество строк в матрице: '))
    m = int(input('Введите количество значений в строке:'))
    
    for i in range(n):
        a = []
        for j in range(m):
            a.append(0)
        massive.append(a)
    
    for i in range(n):
        for j in range(m):
            try:
                massive[i][j] = float(input('Введите Ваши значенния:'))
            except ValueError:
                massive[i][j] = float(input('Введите корректные значения:'))
            
    return massive

def sredn(start_input):
    """Функция возвращает среднее значение массива"""
    return sum(start_input) / len(start_input)

def mass_from_aprox():
    """Функция заполнения значений X и Y для дальнейшей работы апроксимаций"""
    
    x = []
    y = []
    
    while True:
        x_i = input('Введите значения для оси X, иначе Стоп или Stop: ')
        try:
            if x_i not in ['Стоп', 'Stop']:
                x.append(float(x_i))
                continue
            else:
                break
        except ValueError:
            print('Пожалуйста, вводите корректные значения!')
            continue
        
    while True:
        y_i = input('Введите значения для оси Y, иначе Стоп или Stop: ')
        try:
            if y_i not in ['Стоп', 'Stop']:
                y.append(float(y_i))
                continue
            else:
                break
        except ValueError:
            print('Пожалуйста, вводите корректные значения!')
            continue
    
    if len(x) == len(y):
        counter_x = 0
        counter_y = 0
        
        for i in range(len(x)):
            if x[i] == 0:
                counter_x += 1
        for j in range(len(y)):
            if y[j] == 0:
                counter_y += 1
        
        if len(x) == 0 or len(y) == 0:
            return 'Вы задали один из списков пустым, придётся начать всё занво!'
        
        elif counter_x == len(x) or counter_y == len(y):
            return 'Все значения x или y - нули, не издевайся!'
        
        else:
            x = np.array(x)
            y = np.array(y)
            return x, y
    elif len(y) > len(x):
        return 'Массив значений y больше чем x!'
    elif len(x) > len(y):
        return 'Массив значений x больше y!'

def kvadr_aprox(x, y):
    """Функция возвращает коэффициенты для квадротичной апроксимации"""
    
    n = len(x)
    Sx = np.sum(x)
    Sy = np.sum(y)
    Sxx = np.sum(x**2)
    Sxy = np.sum(x*y)
    Sxxx = np.sum(x**3)
    Sxxxx = np.sum(x**4)
    Sxxy = np.sum(x**2 * y)

    det = n * (Sxx * Sxxxx - Sxxx**2) - Sx * (Sx * Sxxxx - Sxx * Sxxx) + Sxx * (Sx * Sxxx - Sxx**2)

    det1 = np.array([[Sy, Sxy, Sxxy], [Sx, Sxx, Sxxx], [Sxx, Sxxx, Sxxxx]])
    det2 = np.array([[n, Sx, Sxx], [Sy, Sxy, Sxxy], [Sxx, Sxxx, Sxxxx]])
    det3 = np.array([[n, Sx, Sxx], [Sx, Sxx, Sxxx], [Sy, Sxy, Sxxy]])

    a0 = np.linalg.det(det1) / det
    a1 = np.linalg.det(det2) / det
    a2 = np.linalg.det(det3) / det
    
    return a0, a1, a2

def lin_aprox(x, y):
    """Функция возвращает коэффициенты для линейной апроксимации"""
    Sx = sum(x)
    Sy = sum(y)
    Sxy = sum(x*y)
    Sxx = sum(x*x)

    Zn = len(x)*Sxx-Sx**2
    a = (Sxy * len(x)-Sx*Sy)/Zn
    b = (Sxx*Sy-Sx*Sxy)/Zn

    print("Sx=",Sx)
    print("Sy=",Sy)
    print("Sxy=",Sxy)
    print("Sxx=",Sxx)

    return a, b

def exp_aprox(x, y):
    """Функция возвращает коэффициенты для эксподенциальной апроксимации"""
    Sx = Sy = Sxy = Sxx = 0
    lnY = []

    for i in range(len(y)):
        lnY.append(math.log( y[i] ))
        
    print(lnY) 

    Sx = sum(x)
    Sy = sum(lnY)
    Sxy = sum(x * lnY)
    Sxx = sum(x * x)
    Zn = len(x) * Sxx - Sx ** 2

    print("Sx = ",Sx)
    print("Sy = ",Sy)
    print("Sxy = ",Sxy)
    print("Sxx = ",Sxx)

    a = (Sxy * len(x) - Sx * Sy) / Zn
    b = (Sxx*Sy-Sx*Sxy)/Zn

    A = (math.e) ** b
    B = a

    return A, B

def graf_kvadr_aprox(x, a0, a1, a2):
    """Функция возвращает график квадротичной апроксимации"""
    return a2 * (x**2) + a1 * x + a0

def graf_lin_aprox(a, b, x):
    """Функция возвращает график линейной апроксимации"""
    return a*x+b

def graf_exp_aprox(a, b, x):
    """Функция возвращает график експоденциальной апроксимации"""
    return a * (math.e) ** (b * x)

# Выполнение простейших консольных комманд

def main():
    """Функция простейшего интерфейса"""
    do = int(input("""
               Пожалуйста, введите число-действие, которое хотите сделать:\n
               1 - Подсчёт среднего значения с погрешностью.\n
               2 - Подсчёт относительной погрешности.\n
               3 - Анализ промахов.\n
               4 - Обработка многомерных массивов.\n
               5 - Квадротичная апроксимация.\n
               6 - Линейная апроксимация.\n
               7 - Эксподенциальная апроксимация. 
               """))

    if do == 1:
        """Подсчёт среднего статистического и погрешности у линейного массива"""
        cort = lin_mass() #Выводит кортеж вида ([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0], 'метры', 0.1, 5.0)
        
        if type(cort) != str:
            sr_kv = sredn_kvard(cort[0], cort[-1])
            rand_err = random_error(cort[0], sr_kv)
            
            print(f'Подсчёт среднего значения составил: ({cort[-1]} ± {error(float(cort[2]), rand_err)}) {cort[1]}')
        else:
            print(cort)
    if do == 2:
        """Подсчёт отностительной погрешности"""
        
        cort = lin_mass()
        if type(cort) != str:
            sr_kv = sredn_kvard(cort[0], cort[-1])
            rand_err = random_error(cort[0], sr_kv)
            err = float(error(float(cort[2]), rand_err))
            
            print(f'Ваша отностительная погрешность составляет {relative_error(err, float(cort[-1]))} {cort[1]}')
        else:
            print(cort)
            
    if do == 3:
        """Анализ промахов"""
        
        cort = lin_mass()
        if type(cort) != str:
            start_input = cort[0]
            
            print(f'Конечный итог операции: {miss(start_input)}')
        else:
            print(cort)
    
    if do == 4:
        """Обработка многомерных массивов"""
        
        ed_izm = input('Введите единицы измерения, в которых работаете: ')
        
        while True:
            try:
                pr_pogr = float(input('Введите приборную погрешность: '))
                break
            except ValueError:
                pr_pogr = float(input('Вводите корректное значение: '))
                continue
            
        massive = mass()
        
        for i in range(len(massive)):
            cort_i = massive[i]
            sr = sredn(cort_i)
            sr_kv_mass = sredn_kvard(cort_i, sr)
            rand_err_mass = random_error(cort_i, sr_kv_mass)
            err_mass = error(pr_pogr, rand_err_mass)
            print(f'Подсчёт среднего значения составил: ({sr} ± {err_mass}) {ed_izm}')
            
    if do == 5:
        
        x_y = mass_from_aprox()
        if type(x_y) != str:
            x = x_y[0]
            y = x_y[1]
            mass_koef = kvadr_aprox(x, y)
            a0 = mass_koef[0]
            a1 = mass_koef[1]
            a2 = mass_koef[2]
            
            print(f'Формула квадратичной кривой:  {a2} * x^2 + {a1} * x + {a0}')
            
            plt.scatter(x, y, label='Данные', color = 'green')
            plt.plot(x, graf_kvadr_aprox(x, a0, a1, a2), label='Квадратичная аппроксимация', color='blue')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.legend()
            plt.grid(True)
            
            save = input('Хотите ли вы сохранить график?\n(y - yes, д - да, n - no, н - нет)')
            if save in ['y', 'д', 'n', 'н']:
                name = input('Введите название графика: ')
                name = name.strip()
                if len(name) != 0:
                    plt.savefig(f'{name}.pdf')
                else:
                    print('Ебать ты лох, ничего не сохранилось!')
            else:
                print('Ты не правильно ответил на вопрос!')
                
            plt.show()
        
        else:
            print(x_y)
            
        x_y = np.array([])
        
    if do == 6:
        x_y = mass_from_aprox()
        if type(x_y) != str:
            x = x_y[0]
            y = x_y[1]
            lin_koef = lin_aprox(x, y)
            a = lin_koef[0]
            b = lin_koef[1]
            
            print(f'Формула апроксимирующей прямой: {a} * x + {b}')
            
            plt.scatter(x, y, label='Данные', color='green')
            plt.plot(x, graf_lin_aprox(a, b, x), label='Линейная аппроксимация', color='blue')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend()
            plt.grid(True)
            
            save = input('Хотите ли вы сохранить график?\n(y - yes, д - да, n - no, н - нет)')
            if save in ['y', 'д', 'n', 'н']:
                name = input('Введите название графика: ')
                name = name.strip()
                if len(name) != 0:
                    plt.savefig(f'{name}.pdf')
                else:
                    print('Ебать ты лох, ничего не сохранилось!')
            else:
                print('Ты не правильно ответил на вопрос!')
                
            plt.show()
        
        else:
            print(x_y)
            
        x_y = np.array([])
            
    if do == 7:
        x_y = mass_from_aprox()
        if type(x_y) != str:
            x = x_y[0]
            y = x_y[1]
            exp_koef = exp_aprox(x, y)
            a = exp_koef[0]
            b = exp_koef[1]
            
            print(f'Формула експоденциальной кривой: {a} * e ** ({b} * x)')
            
            plt.scatter(x, y, label='Данные', color='green')
            plt.plot(x, graf_exp_aprox(a, b, x), label='Экспоненциальная аппроксимация', color='blue')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend()
            plt.grid(True)
            
            save = input('Хотите ли вы сохранить график?\n(y - yes, д - да, n - no, н - нет)')
            if save in ['y', 'д', 'n', 'н']:
                name = input('Введите название графика: ')
                name = name.strip()
                if len(name) != 0:
                    plt.savefig(f'{name}.pdf')
                else:
                    print('Ебать ты лох, ничего не сохранилось!')
            else:
                print('Ты не правильно ответил на вопрос!')
                
            plt.show()
        
        else:
            print(x_y)
            
        x_y = np.array([])
            
if __name__ == "__main__":
    main()