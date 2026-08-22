

scatter_color = {
    1 : {"ru" : "Красный", "en" : "red"},
    2 : {"ru" : "Синий", "en" : "blue"},
    3 : {"ru" : "Зеленый", "en" : "green"},
    4 : {"ru" : "Оранжевый", "en" : "orange"}, 
    5 : {"ru" : "Черный", "en" : "black"},
    6 : {"ru" : "Желтый", "en" : "yellow"},
}
scatter_keys = list(scatter_color)

print(scatter_color.items("ru"))

for i, j in enumerate(scatter_keys, start = 1):
    print(f"Индекс цвета: {i}, соответствующий ему цвет: {j}")


