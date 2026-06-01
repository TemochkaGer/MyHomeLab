import os
import matplotlib.pyplot as plt

x = []
y = []

# with open("Tests_for_code.txt", "r") as f:
#     data = f.read().splitlines()

# for i in data:
#     point = i.split("\t")
#     x.append(float(point[0].replace(",", ".")))
#     y.append(float(point[1].replace(",", ".")))

# plt.scatter(x, y)
# plt.savefig("graf.png")

list_dir = os.listdir(f"{os.path.dirname(os.path.abspath(__file__))}/data")
print(list_dir)
for i in list_dir:
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/data/{i}") as f:
        print(f.read())
