"""
Пробегаю кардон + находу скриптом записываю свою координату в игре
Сохраняю запись всех координат
Накладываю эти координаты на .dds файл
Получается отпечаток моего пути на минимапе


Запускаю бота и смотрю что произойдет
"""
from pymem import Pymem
import time


for i in range(5):
    print(i)
    time.sleep(1)
if "__main__" == __name__:
    pm = Pymem('XR_3DA.exe')
    module_offset = None
    for i in list(pm.list_modules()):
        if(i.name == "xrGame.dll"):
            module_offset = i.lpBaseOfDll
    holder = []
    plashka = False
    print("started")
    while not plashka:
        z = pm.read_float(pm.base_address+0x104944)
        x = pm.read_float(pm.base_address+0x10493C)
        plashka = pm.read_bool(module_offset+0x54C2F9)
        holder.append([x, z])
        time.sleep(0.5)
    with open("dataclean", mode="w") as file:
        file.write(str(holder))
