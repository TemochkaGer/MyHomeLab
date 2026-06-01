import math
import sys
import os
import matplotlib.pyplot as plt

WORK_DIR = os.path.dirname(os.path.abspath(__file__))

class CompositionCalculation:

    def composition_lo(self, w, a, b, c):
        """
        Расчет квадратного уравнения вида ax^2 + bx + c = w
        Возвращает список положительных решений в диапазоне от 0 до 1
        """
        try:
            cont = []

            if type(w) is list:
                if len(w) != 0:
                    for i in w:
                        new_c = c - i
                        diskr = b**2 - 4 * a * new_c
                        if diskr > 0:
                            x_1 = (-b + math.sqrt(diskr)) / (2 * a)
                            x_2 = (-b - math.sqrt(diskr)) / (2 * a)

                            if x_1 >= 0 and x_1 <= 1:
                                cont.append(f"Для значения {i} корень, удовлетворяющий условию - {x_1}")
                            elif x_2 >= 0 and x_2 <= 1:
                                cont.append(f"Для значения {i} корень, удовлетворяющий условию - {x_2}")
                            else:
                                cont.append(f"Для значения {i} корень, удовлетворяюзий условию - {None}")

                        elif diskr == 0:
                            x = (-b) / (2 * a)
                            cont.append(x)
                        else:
                            cont.append(None)
                    return cont
                else:
                    return cont
        except Exception as e:
            return f"Возникла ошибка в коде - {e}"
        
    def take_file(self):
        """
        Функция читает файлы из папки data формата .txt
        Возвращает список файлов для обработки
        """

        data = os.listdir(f"{WORK_DIR}/data")
        txt_data = []
        for i in data:
            if ".txt" in i:
                txt_data.append(i)


        return txt_data
    
    def take_data(self, txt_files):
        """
        Функция, через переменную txt_files(Список файлов директории с данными data, выводит список файлов для чтения, по выбранному файлу читает данные и делит их на x и y 
        Возвращает два списка x и y
        """

        x = []
        y = []
        
        print(txt_files)
        index_file = int(input("Введите номер файла, который надо обработать: "))

        with open(f"{WORK_DIR}/data/{txt_files[index_file - 1]}", "r") as f:
            data = f.read().splitlines()

        for i in data:
            point = i.split("\t")
            x.append(float(point[0].replace(",", ".")))
            y.append(float(point[1].replace(",", ".")))

        return x, y
    
    def plot_graf(self, x, y):
        """
        Функция отрисовывает граффик на основе полученных данных (x, y и названия графика - graf_name) и сохраняет их в папку ./graf в формате png
        """

        graf_name = input("Введите имя графика: ")
        plt.scatter(x, y)
        plt.savefig(f"{WORK_DIR}/graf/{graf_name}.png")
            
if __name__ == "__main__":
    calc = CompositionCalculation()
    do = int(input(
        """Введите действие, которое хотите сделать:\n1 - Посчитать содержание In исходя из частоты пика продольной моды Al\n2 - Посчитать содержание In исходя из частоты пика продольной моды In
3 - Посчитать содержание In исходя из частоты пика поперечной моды Al\n4 - Нарисовать график исходя из данных\n"""
    ))
    if do == 1:
        print("Введите значение чатсоты пика продольной моды (если значения закончились, введите '0')")
        input_data = []
        while True:
            count = float(input())
            if count != 0:
                input_data.append(count)
            else:
                break
        print(calc.composition_lo(w = input_data, a = -20, b = -55, c = 403))
    elif do == 2:
        print("Введите значение чатсоты пика продольной моды (если значения закончились, введите '0')")
        input_data = []
        while True:
            count = float(input())
            if count != 0:
                input_data.append(count)
            else:
                break
        print(calc.composition_lo(w = input_data, a = -13, b = 22, c = 229))
    elif do == 3:
        print("Введите значение чатсоты пика продольной моды (если значения закончились, введите '0')")
        input_data = []
        while True:
            count = float(input())
            if count != 0:
                input_data.append(count)
            else:
                break
        print(calc.composition_lo(w = input_data, a = -9.5, b = -24, c = 361.5))
    elif do == 4:
        list_files = calc.take_file()
        x, y = calc.take_data(list_files)
        calc.plot_graf(x, y)

    else:
        print("Введено некорректное значение номера действия")
        sys.exit()
