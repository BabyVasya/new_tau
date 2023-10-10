import matplotlib.pyplot as pyplot
import control.matlab as matlab
import numpy
import math
import colorama

INERTIALESS_UNIT_NAME = 'Безынерционное звено'
APERIODIC_UNIT_NAME = 'Апериодическое звено'
INTEGRATING_UNIT_NAME = 'Интегрирующее звено'
IDEAL_DIFFERENTIATING_UNIT_NAME = 'Идеальное дифференцирующее звено'
REAL_DIFFERENTIATING_UNIT_NAME = 'Реальное дифференцирующее звено'
def choice():
    need_new_choice = True
    while need_new_choice:
        print(colorama.Style.RESET_ALL)
        user_input = input('Введите номер команды: \n'
                           '1 - ' + INERTIALESS_UNIT_NAME + ';\n'
                           '2 - ' + APERIODIC_UNIT_NAME + ';\n'
                           '3 - ' + INTEGRATING_UNIT_NAME + ';\n'
                           '4 - ' + IDEAL_DIFFERENTIATING_UNIT_NAME + ';\n'
                           '5 - ' + REAL_DIFFERENTIATING_UNIT_NAME + ';\n')
        if user_input.isdigit():
            need_new_choice = False
            user_input = int(user_input)
            if user_input == 1:
                name = INERTIALESS_UNIT_NAME
            elif user_input == 2:
                name = APERIODIC_UNIT_NAME
            elif user_input == 3:
                name = INTEGRATING_UNIT_NAME
            elif user_input == 4:
                name = IDEAL_DIFFERENTIATING_UNIT_NAME
            elif user_input == 5:
                name = REAL_DIFFERENTIATING_UNIT_NAME
            else:
                need_new_choice = True
                print(colorama.Fore.RED + '\nТакого звена не предусмотрено, либо значение не корректно')
        else:
            print(colorama.Fore.RED + '\nПожалуйста, введите числовое значение!')
    return name

def get_unit(unit_name):
    need_new_choice = True
    while need_new_choice:
        print(colorama.Style.RESET_ALL)
        need_new_choice = False
        if unit_name == INERTIALESS_UNIT_NAME:
            k = input('Введите коэффициент передачи звена (k): ')
            if k.isdigit():
                k = int(k)
                unit = matlab.tf([k], [1])
            else:
                print(colorama.Fore.RED + '\nПожалуйста, введите числовое значение!')
                need_new_choice = True

        elif unit_name == APERIODIC_UNIT_NAME:
            k = input('Введите коэффициент передачи звена (k): ')
            t = input('Введите постаянная времени звена (T): ')
            if k.isdigit() and t.isdigit():
                k = int(k)
                t = int(t)
                unit = matlab.tf([k], [t, 1])
            else:
                print(colorama.Fore.RED + '\nПожалуйста, введите числовое значение!')
                need_new_choice = True

        elif unit_name == INTEGRATING_UNIT_NAME:
            k = input('Введите коэффициент передачи звена (k): ')
            if k.isdigit() :
                k = int(k)
                unit = matlab.tf([k], [1])
            else:
                print(colorama.Fore.RED + '\nПожалуйста, введите числовое значение!')
                need_new_choice = True

        elif unit_name == IDEAL_DIFFERENTIATING_UNIT_NAME:
            k = input('Введите коэффициент передачи звена (k): ')
            if k.isdigit():
                k = int(k)
                unit = matlab.tf([k], [0.0000000000000001])
            else:
                print(colorama.Fore.RED + '\nПожалуйста, введите числовое значение!')
                need_new_choice = True

        elif unit_name == REAL_DIFFERENTIATING_UNIT_NAME:
            k = input('Введите коэффициент передачи звена (k): ')
            t = input('Введите постаянная времени звена (T): ')
            if k.isdigit() and t.isdigit():
                k = int(k)
                t = int(t)
                unit = matlab.tf([k, 0.0000000000000000001], [t, 1])
            else:
                print(colorama.Fore.RED + '\nПожалуйста, введите числовое значение!')
                need_new_choice = True
        else:
            print(colorama.Fore.YELLOW + '\nНедопустимое звено!')
            need_new_choice = True
    return unit

def graph(num, title, y, x ):
    pyplot.subplot(2, 4, num)
    pyplot.grid(True)
    if title == 'Переходная характеристика':
        pyplot.plot(x, y, 'red')
        pyplot.xlabel('Время, с')
        pyplot.ylabel('Амплитуда')
    elif title == 'Импульсная характеристика':
        pyplot.plot(x, y, 'black')
        pyplot.xlabel('Время, с')
        pyplot.ylabel('Амплитуда')
    elif title == 'АЧХ':
        pyplot.plot(omega, mag, 'blue')
        pyplot.xlabel('Частота, рад/с')
        pyplot.ylabel('Амплитуда')
    elif title == 'фЧХ':
        pyplot.plot(omega, phase, 'yellow')
        pyplot.xlabel('Частота, рад/с')
        pyplot.ylabel('Фаза')
    elif title == 'ЛАЧХ':
        pyplot.plot(omega, mag, 'blue')
        pyplot.xlabel('Частота, Дб')
        pyplot.ylabel('Амплитуда')
    elif title == 'ЛфЧХ':
        pyplot.plot(omega, phase, 'yellow')
        pyplot.xlabel('Частота, Дб')
        pyplot.ylabel('Фаза')
    elif title == 'АФХ':
        pyplot.plot(omega, phase, 'pink')
        pyplot.xlabel('Частота, Дб')
        pyplot.ylabel('Фаза')
    pyplot.title(title)

unit_name = choice()
unit = get_unit(unit_name)
print(unit)

time_line = []
for i in range(0, 10000):
    time_line.append(i/1000)

frequencies = []
for i in range(0, 100):
    frequencies.append(i)


[y, x] = matlab.step(unit, time_line)
graph(1, 'Переходная характеристика', y, x)
[y, x] = matlab.impulse(unit, time_line)
graph(2, 'Импульсная характеристика', y, x)
mag, phase, omega = matlab.freqresp(unit, frequencies)
graph(3, 'АЧХ', mag, omega)
graph(4, 'ФЧХ', mag, phase)
mag1, phase1, omega1 = matlab.bode(unit, frequencies)
graph(5, 'ЛАЧХ', mag1, omega1)
graph(6, 'ЛФЧХ', mag1, phase1)
mag1, phase1, omega1 = matlab.nyquist(unit)
graph(7,'АФХ', mag1, phase1)


pyplot.show()

