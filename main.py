import tkinter as tk
from tkinter import ttk
import math
import random
import threading
import time
from queue import PriorityQueue
from enum import Enum


# Типы событий в системе
class TipSobytiya(Enum):
    PRISHEL = 1
    OBSLUJEN = 2


# Базовый класс агентов
class Uchastnik:
    def __init__(self, sistema):
        self.sistema = sistema

    def obrabotka_sobytiya(self, sobitie):
        pass


# Клиент банка
class Klient(Uchastnik):
    schetchik = 0

    def __init__(self, sistema, vremya_prihoda):
        super().__init__(sistema)
        Klient.schetchik += 1
        self.nomer = Klient.schetchik
        self.vremya_prihoda = vremya_prihoda
        self.vremya_v_ocheredi = vremya_prihoda

    def obrabotka_sobytiya(self, sobitie):
        # Обработка через консультанта
        pass


# Консультант
class Sotrudnik(Uchastnik):
    def __init__(self, sistema, nomer):
        super().__init__(sistema)
        self.nomer = nomer
        self.zaniat = False

    def obrabotka_sobytiya(self, sobitie):
        if sobitie.tip == TipSobytiya.OBSLUJEN:
            self.sistema.zaversheniye_obslujivaniya(self, sobitie.vremya)


# Генератор клиентов
class Generator(Uchastnik):
    def __init__(self, sistema, chastota):
        super().__init__(sistema)
        self.chastota = chastota

    def sled_klient(self, tek_vremya):
        if self.chastota <= 0:
            return
        interval = self.sistema.sluch_interval(self.chastota)
        vremya_sobitiya = tek_vremya + interval
        self.sistema.dobavit_sobitie(
            Sobitie(vremya_sobitiya, TipSobytiya.PRISHEL, self)
        )

    def obrabotka_sobytiya(self, sobitie):
        vremya = sobitie.vremya
        klient = Klient(self.sistema, vremya)
        self.sistema.noviy_klient(klient, vremya)
        self.sled_klient(vremya)


# Событие в симуляции
class Sobitie:
    def __init__(self, vremya, tip, agent):
        self.vremya = vremya
        self.tip = tip
        self.agent = agent

    def __lt__(self, drugoe):
        return self.vremya < drugoe.vremya


# Сбор статистики
class Statistika:
    def __init__(self):
        self.ochistit()

    def ochistit(self):
        self.vsego_obsluzheno = 0
        self.vsego_prishlo = 0
        self.sum_vremya_ozhidaniya = 0
        self.tek_vremya = 0

    def noviy_klient(self):
        self.vsego_prishlo += 1

    def klient_obslujen(self):
        self.vsego_obsluzheno += 1

    def dobavit_ozhidanie(self, ozhidanie):
        self.sum_vremya_ozhidaniya += ozhidanie

    def update_vremya(self, vremya):
        self.tek_vremya = vremya

    @property
    def sred_vremya_ozhid(self):
        if self.vsego_prishlo > 0:
            return self.sum_vremya_ozhidaniya / self.vsego_prishlo
        return 0


# Среда моделирования
class BankSistem:
    def __init__(self, chastota_klientov, skorost_obsluzhivaniya, kol_sotrudnikov):
        self.chastota_klientov = chastota_klientov
        self.skorost_obsluzhivaniya = skorost_obsluzhivaniya
        self.ochered_sobitiy = PriorityQueue()
        self.stats = Statistika()
        self.tek_vremya = 0.0
        self.ochered = []
        self.sotrudniki = [Sotrudnik(self, i + 1) for i in range(kol_sotrudnikov)]
        self.generator = Generator(self, chastota_klientov)

    def zapusk(self):
        self.sbros()
        self.generator.sled_klient(self.tek_vremya)

    def sbros(self):
        while not self.ochered_sobitiy.empty():
            self.ochered_sobitiy.get()
        self.stats.ochistit()
        self.tek_vremya = 0.0
        self.ochered = []
        for s in self.sotrudniki:
            s.zaniat = False

    def dobavit_sobitie(self, sobitie):
        self.ochered_sobitiy.put(sobitie)

    def sluch_interval(self, lambda_param):
        if lambda_param <= 0:
            return float("inf")
        return -math.log(random.random()) / lambda_param

    def sled_shag(self):
        if self.ochered_sobitiy.empty():
            return None

        sobitie = self.ochered_sobitiy.get()
        self.tek_vremya = sobitie.vremya
        self.stats.update_vremya(self.tek_vremya)
        sobitie.agent.obrabotka_sobytiya(sobitie)
        return sobitie

    def noviy_klient(self, klient, vremya):
        self.stats.noviy_klient()
        klient.vremya_v_ocheredi = vremya

        svobod_sotr = self.naiti_svobodnogo()
        if svobod_sotr:
            self.nachat_obsluzhivanie(svobod_sotr, klient, vremya)
        else:
            self.ochered.append(klient)

    def naiti_svobodnogo(self):
        for s in self.sotrudniki:
            if not s.zaniat:
                return s
        return None

    def nachat_obsluzhivanie(self, sotrudnik, klient, vremya):
        sotrudnik.zaniat = True
        vremya_ozhid = vremya - klient.vremya_v_ocheredi
        self.stats.dobavit_ozhidanie(vremya_ozhid)

        interval = self.sluch_interval(self.skorost_obsluzhivaniya)
        vremya_zaversheniya = vremya + interval

        self.dobavit_sobitie(
            Sobitie(vremya_zaversheniya, TipSobytiya.OBSLUJEN, sotrudnik)
        )

    def zaversheniye_obslujivaniya(self, sotrudnik, vremya):
        self.stats.klient_obslujen()
        sotrudnik.zaniat = False

        if self.ochered:
            sled_klient = self.ochered.pop(0)
            self.nachat_obsluzhivanie(sotrudnik, sled_klient, vremya)

    @property
    def dlina_ocheredi(self):
        return len(self.ochered)

    @property
    def zagruzka_sistemy(self):
        zan_count = sum(1 for s in self.sotrudniki if s.zaniat)
        vsego = len(self.sotrudniki)
        return (zan_count / vsego * 100.0) if vsego > 0 else 0.0


# Основной класс приложения
class BankApp:
    def __init__(self, okno):
        self.okno = okno
        self.okno.title("Лабораторная работа 14 - Моделирование банка")
        self.okno.geometry("800x600")

        self.rabotaet = False
        self.potok = None
        self.bank = None

        self.sozdat_interfeis()

    def sozdat_interfeis(self):
        # Настройки симуляции
        block_nastroiki = ttk.LabelFrame(
            self.okno, text="Параметры модели", padding="10"
        )
        block_nastroiki.pack(fill="x", padx=10, pady=5)

        ttk.Label(block_nastroiki, text="Частота прихода клиентов (λ):").grid(
            row=0, column=0, sticky="w", padx=5, pady=2
        )
        self.potok_klientov = tk.DoubleVar(value=1.0)
        potok_spin = ttk.Spinbox(
            block_nastroiki,
            from_=0.1,
            to=10.0,
            increment=0.1,
            textvariable=self.potok_klientov,
            width=10,
        )
        potok_spin.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(block_nastroiki, text="Скорость обслуживания (μ):").grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        self.skorost = tk.DoubleVar(value=1.5)
        skorost_spin = ttk.Spinbox(
            block_nastroiki,
            from_=0.1,
            to=10.0,
            increment=0.1,
            textvariable=self.skorost,
            width=10,
        )
        skorost_spin.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(block_nastroiki, text="Число консультантов:").grid(
            row=2, column=0, sticky="w", padx=5, pady=2
        )
        self.kol_sotrudnikov = tk.IntVar(value=2)
        sotr_spin = ttk.Spinbox(
            block_nastroiki, from_=1, to=10, textvariable=self.kol_sotrudnikov, width=10
        )
        sotr_spin.grid(row=2, column=1, padx=5, pady=2)

        self.knopka = ttk.Button(block_nastroiki, text="Старт", command=self.start_stop)
        self.knopka.grid(row=3, column=0, columnspan=2, pady=10)

        # Статистика
        block_stats = ttk.LabelFrame(self.okno, text="Показатели", padding="10")
        block_stats.pack(fill="x", padx=10, pady=5)

        ttk.Label(block_stats, text="Обслужено:").grid(
            row=0, column=0, sticky="w", padx=5, pady=2
        )
        self.lbl_obsluzheno = ttk.Label(block_stats, text="0")
        self.lbl_obsluzheno.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(block_stats, text="В очереди:").grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        self.lbl_v_ocheredi = ttk.Label(block_stats, text="0")
        self.lbl_v_ocheredi.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(block_stats, text="Загрузка системы:").grid(
            row=2, column=0, sticky="w", padx=5, pady=2
        )
        self.lbl_zagruzka = ttk.Label(block_stats, text="0%")
        self.lbl_zagruzka.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(block_stats, text="Среднее время ожидания:").grid(
            row=3, column=0, sticky="w", padx=5, pady=2
        )
        self.lbl_sredn_ozhid = ttk.Label(block_stats, text="0.00")
        self.lbl_sredn_ozhid.grid(row=3, column=1, padx=5, pady=2)

        ttk.Label(block_stats, text="Время:").grid(
            row=4, column=0, sticky="w", padx=5, pady=2
        )
        self.lbl_vremya = ttk.Label(block_stats, text="0.00")
        self.lbl_vremya.grid(row=4, column=1, padx=5, pady=2)

        # Таблица состояния
        block_table = ttk.LabelFrame(
            self.okno, text="Текущее состояние системы", padding="10"
        )
        block_table.pack(fill="both", expand=True, padx=10, pady=5)

        stolbci = ("Элемент", "Статус", "Инфо")
        self.tablica = ttk.Treeview(
            block_table, columns=stolbci, show="headings", height=15
        )

        self.tablica.heading("Элемент", text="Элемент")
        self.tablica.heading("Статус", text="Статус")
        self.tablica.heading("Инфо", text="Дополнительно")

        self.tablica.column("Элемент", width=150)
        self.tablica.column("Статус", width=100)
        self.tablica.column("Инфо", width=150)

        skrollbar = ttk.Scrollbar(
            block_table, orient="vertical", command=self.tablica.yview
        )
        self.tablica.configure(yscrollcommand=skrollbar.set)

        self.tablica.pack(side="left", fill="both", expand=True)
        skrollbar.pack(side="right", fill="y")

    def obnovit_ekran(self):
        if not self.bank:
            return

        stats = self.bank.stats

        self.lbl_obsluzheno.config(text=str(stats.vsego_obsluzheno))
        self.lbl_v_ocheredi.config(text=str(self.bank.dlina_ocheredi))
        self.lbl_zagruzka.config(text=f"{self.bank.zagruzka_sistemy:.1f}%")
        self.lbl_sredn_ozhid.config(text=f"{stats.sred_vremya_ozhid:.2f}")
        self.lbl_vremya.config(text=f"{stats.tek_vremya:.2f}")

        # Обновление таблицы
        for item in self.tablica.get_children():
            self.tablica.delete(item)

        # Консультанты
        for sotr in self.bank.sotrudniki:
            status = "Занят" if sotr.zaniat else "Свободен"
            info = "Обслуживает клиента" if sotr.zaniat else "Ожидает клиента"
            self.tablica.insert(
                "", "end", values=(f"Сотрудник {sotr.nomer}", status, info)
            )

        # Клиенты в очереди
        for i, klient in enumerate(self.bank.ochered):
            self.tablica.insert(
                "",
                "end",
                values=(
                    f"Клиент {klient.nomer}",
                    "Ждёт",
                    f"Время ожидания: {stats.tek_vremya - klient.vremya_v_ocheredi:.1f}",
                ),
            )

    def tsikl_modelirovaniya(self):
        while self.rabotaet:
            self.bank.sled_shag()

            # Обновляем интерфейс из основного потока
            self.okno.after(0, self.obnovit_ekran)

            # Пауза для наглядности
            time.sleep(0.1)

    def start_stop(self):
        if self.rabotaet:
            # Остановка
            self.rabotaet = False
            if self.potok and self.potok.is_alive():
                self.potok.join()
            self.knopka.config(text="Старт")
        else:
            # Запуск
            chastota = self.potok_klientov.get()
            skorost = self.skorost.get()
            kol_sotr = self.kol_sotrudnikov.get()

            self.bank = BankSistem(chastota, skorost, kol_sotr)
            self.bank.zapusk()

            self.rabotaet = True
            self.potok = threading.Thread(target=self.tsikl_modelirovaniya)
            self.potok.daemon = True
            self.potok.start()

            self.knopka.config(text="Стоп")

    def zakrytie(self):
        self.rabotaet = False
        if self.potok and self.potok.is_alive():
            self.potok.join()
        self.okno.destroy()


def main():
    okno = tk.Tk()
    app = BankApp(okno)
    okno.protocol("WM_DELETE_WINDOW", app.zakrytie)
    okno.mainloop()


if __name__ == "__main__":
    main()
