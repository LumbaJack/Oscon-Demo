import kivy
import json
import requests

kivy.require('1.7.0')
from kivy.app import App
from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout

class DataModel(object):
    def __init__(self):
        self.a = 'Press start to populate...'
        self.b = 'Press start to populate...'

common_data_model = DataModel()

class UI_DataModelMeta(type):
    def __new__(meta, name, bases, dct):
        added_attributes = []
        for attr in dir(common_data_model):
            if not attr.startswith('_'):
                assert attr not in dir(EventDispatcher())
                dct[attr] = StringProperty('INIT')
                added_attributes.append(attr)

        dct['_model_attr'] = added_attributes
        return super(UI_DataModelMeta, meta).__new__(meta, name, bases, dct)

class UI_DataModel(EventDispatcher):
    __metaclass__ = UI_DataModelMeta
    def __getattribute__(self, key):
        if key == '_model_attr':
            return object.__getattribute__(self, key)
        elif key in self._model_attr:
            val = str(getattr(common_data_model, key))
            setattr(self, key, val)
            return EventDispatcher.__getattribute__(self, key)
        else:
            return EventDispatcher.__getattribute__(self, key)

    def update(self, func):
        """Decorator to put around any UI function that update the common
           data model"""
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            for attr in self._model_attr:
                getattr(self, attr)
            return ret
        return wrapper

class RootWidget(FloatLayout):
    ui_data_model = UI_DataModel()

    @ui_data_model.update
    def button_press(self, *args):
        output = json.loads(requests.get('https://70.138.100.58:4443/redfish/' \
                                         'v1/Telemetry/1/', verify=False).text)
        output = json.dumps(output, indent=4, sort_keys=True)
        common_data_model.a = output

    @ui_data_model.update
    def button_press2(self, *args):
        output = json.loads(requests.get('https://70.138.100.58:4443/redfish/' \
                                         'v1/Telemetry/2/', verify=False).text)
        output = json.dumps(output, indent=4, sort_keys=True)
        common_data_model.b = output

class TestApp(App):
    def build(self):
        return RootWidget()

app = TestApp()
app.run()

