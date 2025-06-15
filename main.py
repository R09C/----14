import tkinter as tk
from tkinter import ttk
import math
import random
import threading
import time


class QueueSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа 14 - Симуляция очереди")
        self.root.geometry("800x600")

        self.lambda_rate = 0.0
        self.mu_rate = 0.0
        self.n_consultants = 0
        self.queue = 0
        self.busy = 0
        self.served = 0
        self.current_time = 0.0

        self.is_running = False
        self.simulation_thread = None

        self.setup_ui()

    def setup_ui(self):

        settings_frame = ttk.LabelFrame(
            self.root, text="Настройки симуляции", padding="10"
        )
        settings_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(settings_frame, text="Интенсивность потока клиентов (λ):").grid(
            row=0, column=0, sticky="w", padx=5, pady=2
        )
        self.client_flow = tk.DoubleVar(value=1.0)
        client_flow_spinbox = ttk.Spinbox(
            settings_frame,
            from_=0.1,
            to=10.0,
            increment=0.1,
            textvariable=self.client_flow,
            width=10,
        )
        client_flow_spinbox.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(settings_frame, text="Интенсивность обслуживания (μ):").grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        self.service_intensity = tk.DoubleVar(value=1.5)
        service_intensity_spinbox = ttk.Spinbox(
            settings_frame,
            from_=0.1,
            to=10.0,
            increment=0.1,
            textvariable=self.service_intensity,
            width=10,
        )
        service_intensity_spinbox.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(settings_frame, text="Количество консультантов:").grid(
            row=2, column=0, sticky="w", padx=5, pady=2
        )
        self.num_consultants = tk.IntVar(value=2)
        consultants_spinbox = ttk.Spinbox(
            settings_frame, from_=1, to=10, textvariable=self.num_consultants, width=10
        )
        consultants_spinbox.grid(row=2, column=1, padx=5, pady=2)

        self.start_button = ttk.Button(
            settings_frame, text="Старт", command=self.toggle_simulation
        )
        self.start_button.grid(row=3, column=0, columnspan=2, pady=10)

        stats_frame = ttk.LabelFrame(self.root, text="Статистика", padding="10")
        stats_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(stats_frame, text="Обслужено клиентов:").grid(
            row=0, column=0, sticky="w", padx=5, pady=2
        )
        self.served_label = ttk.Label(stats_frame, text="0")
        self.served_label.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(stats_frame, text="Клиентов в очереди:").grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        self.queued_label = ttk.Label(stats_frame, text="0")
        self.queued_label.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(stats_frame, text="Время симуляции:").grid(
            row=2, column=0, sticky="w", padx=5, pady=2
        )
        self.time_label = ttk.Label(stats_frame, text="0.00")
        self.time_label.grid(row=2, column=1, padx=5, pady=2)

        table_frame = ttk.LabelFrame(
            self.root, text="Состояние консультантов и очереди", padding="10"
        )
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("Консультант", "Статус")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=15
        )

        self.tree.heading("Консультант", text="Консультант")
        self.tree.heading("Статус", text="Статус")

        self.tree.column("Консультант", width=200)
        self.tree.column("Статус", width=200)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def exp_random_value(self, rate):

        return -math.log(random.random()) / rate

    def next_event_time(self, current_time):

        arrival_time = self.exp_random_value(self.lambda_rate)

        if self.busy > 0:
            service_time = self.exp_random_value(self.mu_rate * self.busy)
        else:
            service_time = float("inf")

        if arrival_time < service_time:

            if self.busy < self.n_consultants:
                self.busy += 1
            else:
                self.queue += 1
            return current_time + arrival_time
        else:

            if self.queue > 0:
                self.queue -= 1
            else:
                self.busy -= 1
            self.served += 1
            return current_time + service_time

    def update_display(self):

        self.served_label.config(text=str(self.served))
        self.queued_label.config(text=str(self.queue))
        self.time_label.config(text=f"{self.current_time:.2f}")

        for item in self.tree.get_children():
            self.tree.delete(item)

        for i in range(self.n_consultants):
            consultant_name = f"Консультант {i + 1}"
            status = "Занят" if i < self.busy else "Свободен"
            self.tree.insert("", "end", values=(consultant_name, status))

        for i in range(self.queue):
            self.tree.insert("", "end", values=(f"Клиент {i + 1}", "В очереди"))

    def simulation_loop(self):

        while self.is_running:
            self.current_time = self.next_event_time(self.current_time)

            self.root.after(0, self.update_display)

            time.sleep(0.1)

    def toggle_simulation(self):

        if self.is_running:

            self.is_running = False
            if self.simulation_thread and self.simulation_thread.is_alive():
                self.simulation_thread.join()
            self.start_button.config(text="Старт")
        else:

            self.lambda_rate = self.client_flow.get()
            self.mu_rate = self.service_intensity.get()
            self.n_consultants = self.num_consultants.get()

            self.queue = 0
            self.busy = 0
            self.served = 0
            self.current_time = 0.0

            self.is_running = True
            self.simulation_thread = threading.Thread(target=self.simulation_loop)
            self.simulation_thread.daemon = True
            self.simulation_thread.start()

            self.start_button.config(text="Стоп")

    def on_closing(self):

        self.is_running = False
        if self.simulation_thread and self.simulation_thread.is_alive():
            self.simulation_thread.join()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = QueueSimulation(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
