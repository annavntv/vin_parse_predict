from info_by_vin import AutoByVin

vin_sample = input('Введите один вин-код машины марки Ford:')
auto = AutoByVin(vin_sample)
print(auto.get_auto_info())
print("Прогнозируемая стоимость, у.е.:", round(auto.predict_price()))

