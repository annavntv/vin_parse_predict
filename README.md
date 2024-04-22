# Предсказание стоимости автомобилей марки Ford

**Описание**

Единственный источник информации об автомобилях - VIN-код. VIN-код можно декодировать и получить гораздо больше информации, чем просто набор знаков. VIN-код содержит информацию о стране, названии производителя, характеристиках авто (модель, двигатель, тип кузова), типе топлива, годе выпуска и сборочном заводе. Вся эта информация хранится в 17 числовых и буквенных знаках.

*Цель - обучить модель, предсказывающую стоимость автомобилей, основываясь на признаках зашифрованных в VIN-коде.*

В этом исследовании я создала модель, которая предсказывает стоимость автомобиля марки Ford по составляющим ВИН-кода. При подготовки данных для обучения модели я распарсила ВИН-коды в датасет с помощью определенного регулярного выражения, включающего паттерны ВИН-кодов.В качестве модели использовала градиентный бустинг Catboost (100 итераций, глубина деревьев - 3, скорость обучения - 0.1). Получили адекватное качество (лучше чем у константной модели).

Заключающим этап работы был подготовлен класс, который на вход принимает vin-код автомобиля (один) и выдает информацию об автомобиле и предсказанную стоимость.

Исследование можно посмотреть в файле `notebook.ipynb`
Класс, предоставляющий инфо по ВИН-коду, лежит в `info_by_vin.py`
Пример работы в `run_vin.py`


