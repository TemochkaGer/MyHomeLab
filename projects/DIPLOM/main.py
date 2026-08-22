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
        Функция, редактирует и отрисовывает граффик на основе полученных данных (x, y и названия графика - graf_name) и сохраняет их в папку ./graf в формате png
        """

        x_min = input("Введите нижний порог значений по по оси X: ").strip()
        if len(x_min) == 0:
            x_min = min(x)
        else:
            x_min = float(x_min)

        x_max = input("Введите верхний порог значений по по оси X: ").strip()
        if len(x_max) == 0:
            x_max = max(x)
        else:
            x_max = float(x_max)

        new_x = []
        new_y = []

        for i, j in zip(x, y):
            if i >= x_min and i <= x_max:
                new_x.append(i)
                new_y.append(j)

        if not new_x or not new_y:
            return
        
        graf_name = input("Введите имя графика: ")
        scatter_color = {
            1 : {"ru" : "Красный", "en" : "red"},
            2 : {"ru" : "Синий", "en" : "blue"},
            3 : {"ru" : "Зеленый", "en" : "green"},
            4 : {"ru" : "Оранжевый", "en" : "orange"}, 
            5 : {"ru" : "Черный", "en" : "black"},
            6 : {"ru" : "Желтый", "en" : "yellow"},
        }
        scatter_keys = list(scatter_color.keys())

        for i, j in enumerate(scatter_keys, start = 1):
            print(f"Индекс цвета: {i}, соответствующий ему цвет: {j}")
        print("Нажмите Enter, чтобы использовать цвет по усолчанию")

        while True:
            index = input(f"Введите номер цвета для точек из списка: ")
            if len(index) == 0:
                index = 5
                break
            elif int(index) > 0 and int(index) <= len(scatter_color):
                index = int(index)
                break
            else:
                continue

        plt.scatter(new_x, new_y,
                    color = scatter_color[scatter_keys[index-1]]
                    )
        plt.xlabel(input("Введите подпись к оси X: "), fontsize=12)
        plt.ylabel(input("Введите подпись к оси Y: "), fontsize=12)

        if not os.path.exists(f"{WORK_DIR}/graf"):
            self.make_dir(name_dir = "graf")
        plt.savefig(f"{WORK_DIR}/graf/{graf_name}.png")
        plt.close()
        return
    
    def make_dir(self, name_dir):
        try:
            print(f"Директории с названием {name_dir} не было найдено, выполняется подготовка окружения!")
            os.mkdir(f"{WORK_DIR}\{name_dir}")
            print(f"Директрория {WORK_DIR}/{name_dir} создана успешно!")
            return
        except Exception as e:
            print(f"Возникла ошибка при создании директории {WORK_DIR}/{name_dir}:\n{e}")
            return

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
