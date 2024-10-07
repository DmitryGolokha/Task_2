import tkinter as tk
from tkinter import ttk, messagebox
import psutil
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class ProcessManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Диспетчер задач")
        self.geometry("1000x600")

        # Treeview для отображения списка процессов
        self.process_tree = ttk.Treeview(self, columns=("PID", "Name", "CPU", "Memory"), show="headings")
        self.process_tree.heading("PID", text="PID", command=lambda: self.sort_column("PID", False))
        self.process_tree.heading("Name", text="Name", command=lambda: self.sort_column("Name", False))
        self.process_tree.heading("CPU", text="CPU (%)", command=lambda: self.sort_column("CPU", False))
        self.process_tree.heading("Memory", text="Memory (MB)", command=lambda: self.sort_column("Memory", False))

        self.process_tree.column("PID", width=50)
        self.process_tree.column("Name", width=200)
        self.process_tree.column("CPU", width=80)
        self.process_tree.column("Memory", width=80)

        self.process_tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Scrollbar для списка процессов
        process_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.process_tree.yview)
        process_scrollbar.grid(row=0, column=1, sticky="ns")
        self.process_tree.configure(yscrollcommand=process_scrollbar.set)

        # Кнопка обновления списка процессов
        refresh_button = ttk.Button(self, text="Обновить процессы", command=self.refresh_processes)
        refresh_button.grid(row=1, column=0, pady=10)

        # Кнопка завершения выбранного процесса
        kill_button = ttk.Button(self, text="Завершить процесс", command=self.kill_selected_process)
        kill_button.grid(row=1, column=1, pady=10)

        # Информационная панель
        self.info_label = tk.Label(self, text="")
        self.info_label.grid(row=2, column=0, columnspan=2, pady=10)

        # Выбор интервала обновления
        self.update_interval_label = tk.Label(self, text="Интервал обновления:")
        self.update_interval_label.grid(row=3, column=0, pady=10)

        self.update_interval_values = [1, 2, 5, 10, 30]  # Возможные значения интервала в секундах
        self.update_interval_var = tk.StringVar(value=self.update_interval_values[0])
        self.update_interval_combobox = ttk.Combobox(self, values=self.update_interval_values,
                                                     textvariable=self.update_interval_var)
        self.update_interval_combobox.grid(row=3, column=1, pady=10)
        self.update_interval_combobox.bind("<<ComboboxSelected>>", self.update_interval_changed)

        # Поле ввода для поиска процессов по имени
        self.search_entry = ttk.Entry(self)
        self.search_entry.grid(row=4, column=0, pady=10, padx=10, sticky="ew")

        # Кнопка выполнения поиска
        search_button = ttk.Button(self, text="Поиск", command=self.search_process)
        search_button.grid(row=4, column=1, pady=10)

        # Графики для информационной панели
        self.fig, self.ax = plt.subplots(2, 2, figsize=(8, 6))
        self.fig.subplots_adjust(hspace=0.5)  # Увеличиваем расстояние между графиками
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=3, padx=10, pady=10)

        # Переменные для графиков
        self.cpu_data = []
        self.memory_data = []
        self.disk_data = []
        self.network_data = []

        # Интервал обновления информации в миллисекундах
        self.update_interval = 1000  # Значение по умолчанию

        # Запуск обновления информации
        self.after(0, self.update_info)

        # Задаем вес столбцов и строк
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def refresh_processes(self):
        """Обновляет список процессов в Treeview."""
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                mem_usage = proc.info['memory_info'].rss / (1024 * 1024)  # Конвертация в МБ
                self.process_tree.insert("", "end", values=(
                proc.info['pid'], proc.info['name'], proc.info['cpu_percent'], mem_usage))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def kill_selected_process(self):
        """Завершает выбранный процесс."""
        selected_item = self.process_tree.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите процесс для завершения.")
            return

        pid = int(self.process_tree.item(selected_item)['values'][0])

        try:
            proc = psutil.Process(pid)
            proc.terminate()  # Завершение процесса
            messagebox.showinfo("Информация", f"Процесс {pid} завершен.")
            self.refresh_processes()  # Обновляем список после завершения процесса

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def sort_column(self, col, reverse):
        """Сортирует столбец в Treeview."""
        items = [(self.process_tree.set(k, col), k) for k in self.process_tree.get_children('')]
        items.sort(reverse=reverse)

        for index, (val, k) in enumerate(items):
            self.process_tree.move(k, '', index)

        # Смена направления сортировки
        self.process_tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def update_interval_changed(self, event):
        """Обрабатывает изменение интервала обновления."""
        selected_value = int(self.update_interval_var.get())
        self.update_interval = selected_value * 1000  # Конвертация в миллисекунды

    def search_process(self):
        """Ищет процесс по имени."""
        search_term = self.search_entry.get().lower()

        for item in self.process_tree.get_children():
            if search_term in str(self.process_tree.item(item)['values']):
                self.process_tree.selection_set(item)
                break

    def update_info(self):
        """Обновляет информацию о системе и графики."""
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()

        disk = psutil.disk_usage('/')

        net_io = psutil.net_io_counters()

        # Обновление графиков
        if len(self.cpu_data) >= 10:
            self.cpu_data.pop(0)
            self.memory_data.pop(0)
            self.disk_data.pop(0)
            self.network_data.pop(0)

        self.cpu_data.append(cpu_percent)
        self.memory_data.append(memory.percent)

        # Обновляем графики
        for a in self.ax.flatten():
            a.clear()

        self.ax[0, 0].plot(self.cpu_data, label='Использование ЦП (%)')
        self.ax[0, 0].set_title('Использование ЦП')

        self.ax[0, 1].plot(self.memory_data, label='Использование памяти (%)', color='orange')
        self.ax[0, 1].set_title('Использование памяти')

        network_data = [net_io.bytes_sent / (1024 * 1024), net_io.bytes_recv / (1024 * 1024)]

        labels = ['Отправлено (МБ)', 'Получено (МБ)']

        for i in range(len(network_data)):
            if len(self.network_data) <= i:
                self.network_data.append([])
            if len(self.network_data[i]) >= 10:
                self.network_data[i].pop(0)
            self.network_data[i].append(network_data[i])

            if i == 0:
                self.ax[1, 0].bar(labels[i], network_data[i])
                self.ax[1, 0].set_title('Сеть (Отправлено)')
            else:
                self.ax[1, 1].bar(labels[i], network_data[i])
                self.ax[1, 1].set_title('Сеть (Получено)')
                # Обновляем графики на экране
                self.canvas.draw()

                # Запланировать следующий вызов
                self.after(self.update_interval, self.update_info)

        if __name__ == "__main__":
            app = ProcessManagerApp()
            app.mainloop()
