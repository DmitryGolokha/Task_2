# Задание:
Необходимо написать универсальную основу для представления ненаправленных связных графов и поиска в них кратчайших маршрутов. Далее, этот алгоритм предполагается применять для прокладки маршрутов: на картах, в метро и так далее.
<img width="1087" alt="1" src="https://github.com/user-attachments/assets/8337e469-2d88-4986-88d1-8d8a0891a039">
Для универсального описания графов, вам требуется объявить в программе следующие классы:

Vertex - для представления вершин графа (на карте это могут быть: здания, остановки, достопримечательности и т.п.); Link - для описания связи между двумя произвольными вершинами графа (на карте: маршруты, время в пути и т.п.); LinkedGraph - для представления связного графа в целом (карта целиком).
<img width="952" alt="2" src="https://github.com/user-attachments/assets/a9c27931-7030-4d88-8009-4e86ae6c431e">
Объекты класса Vertex должны создаваться командой:
```python
v = Vertex()
```
и содержать локальный атрибут: _links - список связей с другими вершинами графа (список объектов класса Link).

Также в этом классе должно быть объект-свойство (property): links - для получения ссылки на список _links.

Объекты следующего класса Link должны создаваться командой:
```python
link = Link(v1, v2)
```
где v1, v2 - объекты класса Vertex (вершины графа). Внутри каждого объекта класса Link должны формироваться следующие локальные атрибуты: _v1, _v2 - ссылки на объекты класса Vertex, которые соединяются данной связью; _dist - длина связи (по умолчанию 1); это может быть длина пути, время в пути и др.

В классе Link должны быть объявлены следующие объекты-свойства: v1 - для получения ссылки на вершину v1; v2 - для получения ссылки на вершину v2; dist - для изменения и считывания значения атрибута _dist.

Наконец, объекты третьего класса LinkedGraph должны создаваться командой:
```python
map_graph = LinkedGraph()
```
В каждом объекте класса LinkedGraph должны формироваться локальные атрибуты: _links - список из всех связей графа (из объектов класса Link); _vertex - список из всех вершин графа (из объектов класса Vertex).

В самом классе LinkedGraph необходимо объявить (как минимум) следующие методы:

def add_vertex(self, v): ... - для добавления новой вершины v в список _vertex (если она там отсутствует); def add_link(self, link): ... - для добавления новой связи link в список _links (если объект link с указанными вершинами в списке отсутствует); def find_path(self, start_v, stop_v): ... - для поиска кратчайшего маршрута из вершины start_v в вершину stop_v.

Метод find_path() должен возвращать список из вершин кратчайшего маршрута и список из связей этого же маршрута в виде кортежа: ([вершины кратчайшего пути], [связи между вершинами]) Поиск кратчайшего маршрута необходимо реализовать через алгоритм Дейкстры поиска кратчайшего пути в связном взвешенном графе. В методе add_link() при добавлении новой связи следует автоматически добавлять вершины этой связи в список _vertex, если они там отсутствуют.

Проверку наличия связи в списке _links следует определять по вершинам этой связи. Например, если в списке имеется объект: _links = [Link(v1, v2)] то добавлять в него новые объекты Link(v2, v1) или Link(v1, v2) нельзя (обратите внимание у всех трех объектов будут разные id, т.е. по id определять вхождение в список нельзя).

Подсказка: проверку на наличие существующей связи можно выполнить с использованием функции filter() и указанием нужного условия для отбора объектов.

Однако, в таком виде применять классы для схемы карты метро не очень удобно. Например, здесь нет указаний названий станций, а также длина каждого сегмента равна 1, что не соответствует действительности.

Чтобы поправить этот момент и реализовать программу поиска кратчайшего пути в метро между двумя произвольными станциями, объявите еще два дочерних класса:

class Station(Vertex): ... - для описания станций метро; class LinkMetro(Link): ... - для описания связей между станциями метро.

Объекты класса Station должны создаваться командой:
```python
st = Station(name)
```
где name - название станции (строка). В каждом объекте класса Station должен дополнительно формироваться локальный атрибут:

name - название станции метро. (Не забудьте в инициализаторе дочернего класса вызывать инициализатор базового класса).

В самом классе Station переопределите магические методы str() и repr(), чтобы они возвращали название станции метро (локальный атрибут name).

Объекты второго класса LinkMetro должны создаваться командой:
```python
link = LinkMetro(v1, v2, dist)
```
где v1, v2 - вершины (станции метро); dist - расстояние между станциями (любое положительное число). (Также не забывайте в инициализаторе этого дочернего класса вызывать инициализатор базового класса). В результате, эти классы должны совместно работать.
# Листинг
```python
import sys
import tkinter as tk
from tkinter import ttk

class Vertex:
    def __init__(self):
        self._links = []

    @property
    def links(self):
        return self._links

class Link:
    def __init__(self, v1, v2, dist=1):
        self._v1 = v1
        self._v2 = v2
        self._dist = dist

    @property
    def v1(self):
        return self._v1

    @property
    def v2(self):
        return self._v2

    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, value):
        self._dist = value

class LinkedGraph:
    def __init__(self):
        self._links = []
        self._vertices = []

    def add_vertex(self, v):
        if v not in self._vertices:
            self._vertices.append(v)

    def add_link(self, link):
        if link not in self._links:
            self._links.append(link)
            self.add_vertex(link.v1)
            self.add_vertex(link.v2)

    def find_path(self, start_v, stop_v):
        if start_v not in self._vertices or stop_v not in self._vertices:
            return None, None

        distances = {v: sys.maxsize for v in self._vertices}
        distances[start_v] = 0
        prev_vertices = {v: None for v in self._vertices}
        queue = [start_v]

        while queue:
            current_v = queue.pop(0)
            if current_v == stop_v:
                break

            for link in current_v.links:
                neighbor_v = link.v1 if link.v1 != current_v else link.v2
                new_distance = distances[current_v] + link.dist
                if new_distance < distances[neighbor_v]:
                    distances[neighbor_v] = new_distance
                    prev_vertices[neighbor_v] = current_v
                    if neighbor_v not in queue:
                        queue.append(neighbor_v)

        path_vertices = []
        path_links = []
        current_v = stop_v
        while current_v is not None:
            path_vertices.insert(0, current_v)
            for link in self._links:
                if link.v1 == current_v or link.v2 == current_v:
                    path_links.insert(0, link)
                    break
            current_v = prev_vertices[current_v]

        return path_vertices, path_links

class Station(Vertex):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class LinkMetro(Link):
    def __init__(self, v1, v2, dist):
        super().__init__(v1, v2, dist)

class MetroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Metro Route Planner")
        self.geometry("400x300")

        # Создание поля ввода для начальной и конечной станций
        self.start_station_var = tk.StringVar()
        self.end_station_var = tk.StringVar()
        start_label = ttk.Label(self, text="Start Station:")
        start_label.grid(row=0, column=0, padx=10, pady=10)
        start_entry = ttk.Entry(self, textvariable=self.start_station_var)
        start_entry.grid(row=0, column=1, padx=10, pady=10)
        end_label = ttk.Label(self, text="End Station:")
        end_label.grid(row=1, column=0, padx=10, pady=10)
        end_entry = ttk.Entry(self, textvariable=self.end_station_var)
        end_entry.grid(row=1, column=1, padx=10, pady=10)

        # Создание кнопки для поиска кратчайшего пути
        find_path_button = ttk.Button(self, text="Find Path", command=self.find_path)
        find_path_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Создание текстовой области для отображения результата
        self.result_text = tk.Text(self, height=5, width=40)
        self.result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Создание метро графа
        self.metro_graph = LinkedGraph()
        self.create_metro_graph()

    def create_metro_graph(self):
        station_a = Station("Station A")
        station_b = Station("Station B")
        station_c = Station("Station C")
        station_d = Station("Station D")

        link_ab = LinkMetro(station_a, station_b, 2.5)
        link_bc = LinkMetro(station_b, station_c, 1.8)
        link_cd = LinkMetro(station_c, station_d, 3.1)

        self.metro_graph.add_link(link_ab)
        self.metro_graph.add_link(link_bc)
        self.metro_graph.add_link(link_cd)

    def find_path(self):
        start_station = next((s for s in self.metro_graph._vertices if str(s) == self.start_station_var.get()), None)
        end_station = next((s for s in self.metro_graph._vertices if str(s) == self.end_station_var.get()), None)

        if start_station and end_station:
            path_vertices, path_links = self.metro_graph.find_path(start_station, end_station)
            if path_vertices and path_links:
                result = "Shortest Path:\n"
                result += " -> ".join(str(v) for v in path_vertices)
                result += "\nDistance: {:.2f}".format(sum(link.dist for link in path_links))
            else:
                result = "Path not found."
        else:
            result = "Invalid start or end station."

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result)

if __name__ == "__main__":
    app = MetroApp()
    app.mainloop()
```
# Вывод
![Граф метро](https://github.com/user-attachments/assets/42633601-5b61-45d6-904f-f9cea6d94a96)


