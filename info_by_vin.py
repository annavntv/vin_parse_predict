import re
import pickle
import pandas as pd

class AutoByVin:
    def __init__(self, vin_code):
        self.vin_code = vin_code
        with open('model.pkl', 'rb') as f:
            self.model_for_pred = pickle.load(f)

        with open(r'parsed_wiki_tables\year.pkl', 'rb') as f:
            self.year = pickle.load(f)

        with open(r'parsed_wiki_tables\wmi.pkl', 'rb') as f:
            self.wmi = pickle.load(f)
        
        with open(r'parsed_wiki_tables\restraints.pkl', 'rb') as f:
            self.restraints = pickle.load(f)

        with open(r'parsed_wiki_tables\models.pkl', 'rb') as f:
            self.models = pickle.load(f)

        with open(r'parsed_wiki_tables\engine.pkl', 'rb') as f:
            self.engine = pickle.load(f)

        with open(r'parsed_wiki_tables\brakes.pkl', 'rb') as f:
            self.brakes = pickle.load(f)
        
    def parse_vin(self):
        allowed = r'ABCDEFGHJKLMNPRSTUVWXYZ1234567890'
        wmi_re = f'(?P<wmi>[{allowed}]{{3}})'   #1-3
        brake_re = f'(?P<brake>[{allowed}]{{1}})' #4
        model_re = f'(?P<model>[{allowed}]{{3}})' #5-7
        engine_re = f'(?P<engine>[{allowed}]{{1}})' #8
        check_re = f'(?P<check>[{allowed}]{{1}})' #9
        year_re = f'(?P<year>[{allowed}]{{1}})' #10
        plant_re = f'(?P<plant>[{allowed}]{{1}})' #11
        series_re = f'(?P<series>[{allowed}]{{3}}\\d{{3}})' #12-17


        vin = f'({wmi_re}{brake_re}{model_re}{engine_re}{check_re}{year_re}{plant_re}{series_re})'
        vin_re = re.compile(vin, re.X)
        match = vin_re.match(self.vin_code)
        if not match:
            raise ValueError('Невалидный вин-код. Попробуйте еще раз.')
        return pd.DataFrame([x.groupdict() for x in vin_re.finditer(self.vin_code)])

    def get_auto_info(self):
        parsed = self.parse_vin()
        if parsed['wmi'].iloc[0] not in self.wmi['WMI'].unique():
            raise ValueError(f'{self.vin_code} не относится к бренду Ford. Не можем предоставить достоверную информацию.')

        auto_wmi = self.wmi[self.wmi['WMI'] == parsed['wmi'].iloc[0]]
        auto_model = self.models[self.models['VIN Code'] == parsed['model'].iloc[0]]
        auto_engine = self.engine[self.engine['VIN code'] == parsed['engine'].iloc[0]]
        auto_brakes = self.brakes[self.brakes['VIN  Code'] == parsed['brake'].iloc[0]]
        auto_restraints = self.restraints[self.restraints['VIN code'] == parsed['brake'].iloc[0]]


        info =  {
            "model": auto_model.iloc[0]['Model'] if not auto_model.empty else "Unknown",
            "engine": (auto_engine.iloc[0]['Power (hp)'], auto_engine.iloc[0]['Fuel']) if not auto_engine.empty else "Unknown", 
            "country": auto_wmi.iloc[0]['Country'] if not auto_wmi.empty else "Unknown",
            "description": auto_wmi.iloc[0]['Description'] if not auto_wmi.empty else "Unknown",
            "vehicle type": auto_wmi.iloc[0]['Vehicle types'] if not auto_wmi.empty else "Unknown",
            "brakes": auto_brakes.iloc[0]['Brake System'] if not auto_brakes.empty else "Unknown",
            "restraints": auto_restraints.iloc[0]['Description'] if not auto_restraints.empty else "Unknown",

        }
        return f'''Страна производства: {info["country"]}
Описание: {info["description"]}
Тип автомобиля: {info["vehicle type"]}
Модель: {info["model"]}
Характеристик мотора: {info["engine"][0]} лошадиных сил, топливо: {info["engine"][1]}
Тормозная система: {info["brakes"]}
Удерживающие устройства: {info["restraints"]}

'''

    def predict_price(self):
        parsed = self.parse_vin()
        if parsed['wmi'].iloc[0] not in self.wmi['WMI'].unique():
            raise ValueError(f'{self.vin_code} не относится к бренду Ford. Не можем предоставить достоверную информацию.')
        parsed = parsed.drop(columns=['series', 'check'])
        price = self.model_for_pred.predict(parsed)
        return price[0]

