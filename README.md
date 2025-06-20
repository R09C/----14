# Лабораторная работа №14: Моделирование системы массового обслуживания

## Теоретические основы

### 1. Система массового обслуживания (СМО)

**Система массового обслуживания (СМО)** — это математическая модель, описывающая процесс обслуживания требований (клиентов, заявок), поступающих в систему и ожидающих обслуживания в очереди.

Основные компоненты СМО:

- **Входящий поток требований** — процесс поступления клиентов
- **Очередь** — место ожидания обслуживания
- **Каналы обслуживания** — обслуживающие устройства (в нашем случае — консультанты)
- **Выходящий поток** — обслуженные клиенты

### 2. Модель M/M/c

В нашей лабораторной работе рассматривается модель M/M/c:

- Первая буква M означает, что входящий поток подчиняется закону Пуассона (время между приходами распределено экспоненциально)
- Вторая буква M означает, что время обслуживания также распределено экспоненциально
- c — количество каналов обслуживания (количество консультантов)

### 3. Экспоненциальное распределение

**Экспоненциальное распределение** широко используется в теории массового обслуживания для моделирования времени между событиями в потоках событий.

Функция плотности вероятности экспоненциального распределения:

$f(x) = \lambda e^{-\lambda x}$ для $x \geq 0$

где $\lambda$ — интенсивность (параметр распределения).

Среднее значение (математическое ожидание) равно $1/\lambda$.

Для генерации случайной величины, распределенной экспоненциально с параметром $\lambda$, используется формула:

$X = -\frac{1}{\lambda} \ln(1 - U)$

где $U$ — случайное число, равномерно распределенное в интервале $(0,1)$.

Поскольку $1-U$ также равномерно распределено в $(0,1)$, часто используют более простую формулу:

$X = -\frac{1}{\lambda} \ln(U)$

### 4. Основные характеристики СМО

1. **Коэффициент загрузки системы** $\rho = \frac{\lambda}{c\mu}$, где:

   - $\lambda$ — интенсивность входящего потока
   - $\mu$ — интенсивность обслуживания одним каналом
   - $c$ — количество каналов обслуживания

   Система считается стабильной, если $\rho < 1$.

2. **Среднее время ожидания в очереди** $W_q$
3. **Среднее количество клиентов в очереди** $L_q$
4. **Среднее время нахождения в системе** $W = W_q + \frac{1}{\mu}$
5. **Среднее количество клиентов в системе** $L = L_q + \frac{\lambda}{\mu}$

### 5. Имитационное моделирование СМО

Имитационное моделирование — это метод исследования, при котором изучаемая система заменяется моделью, которая с достаточной точностью описывает реальную систему. С этой моделью проводятся эксперименты с целью получения информации о реальной системе.

Основные этапы имитационного моделирования:

1. **Формализация системы** — определение компонентов, характеристик и параметров
2. **Разработка алгоритма моделирования** — создание логики работы модели
3. **Программная реализация** — написание кода для выполнения моделирования
4. **Проведение экспериментов** — запуск модели с различными параметрами
5. **Анализ результатов** — интерпретация полученных данных

В нашей модели используется **дискретно-событийное моделирование**, при котором система изменяется только в момент наступления определенных событий (приход клиента, окончание обслуживания).

## Задания для лабораторной работы

1. **Изучение теоретических основ** — ознакомиться с принципами работы СМО типа M/M/c.

2. **Изучение программной реализации** — разобраться в структуре кода и логике работы модели.

3. **Проведение экспериментов** — запустить модель с различными параметрами и наблюдать за изменением характеристик системы:

   - Изменить интенсивность потока клиентов ($\lambda$)
   - Изменить интенсивность обслуживания ($\mu$)
   - Изменить количество консультантов (c)

4. **Анализ результатов** — для каждого эксперимента проанализировать:

   - Среднее время ожидания клиентов
   - Длину очереди
   - Загрузку системы

5. **Исследование предельных режимов**:

   - Изучить поведение системы при $\rho \approx 1$ (система на пределе стабильности)
   - Изучить поведение системы при $\rho > 1$ (перегруженная система)
   - Изучить поведение системы при $\rho \ll 1$ (недогруженная система)

6. **Оптимизация системы** — определить оптимальное количество консультантов для заданных интенсивностей потока клиентов и обслуживания.

## Теоретические вопросы для защиты

1. Что такое система массового обслуживания? Приведите примеры СМО в реальной жизни.
2. Почему в моделях СМО часто используется экспоненциальное распределение?
3. Как определить, стабильна ли система обслуживания?
4. Что произойдет, если коэффициент загрузки системы превысит единицу?
5. Какие метрики используются для оценки эффективности работы СМО?
6. В чем разница между детерминированной и стохастической моделью СМО?
7. Как влияет увеличение числа каналов обслуживания на характеристики системы?
8. Объясните принцип работы дискретно-событийного моделирования.
9. Какие законы распределения можно использовать для моделирования времени обслуживания?
10. Как связаны между собой средняя длина очереди и среднее время ожидания?

## Литература

1. Клейнрок Л. Теория массового обслуживания. — М.: Машиностроение, 1979.
2. Вентцель Е.С. Исследование операций. — М.: Советское радио, 1972.
3. Кельтон В., Лоу А. Имитационное моделирование. — СПб.: Питер, 2004.
4. Таха Х.А. Введение в исследование операций. — М.: Вильямс, 2005.
