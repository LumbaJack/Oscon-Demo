import kivy
kivy.require('1.7.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.event import EventDispatcher
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty

class DataModel(object):
    def __init__(self):
        self.a = 'This is a'
        self.b = 'This is b'

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

Builder.load_string("""
<RootWidget>:
    cols: 1
    Label:
        text: root.ui_data_model.a
    Label:
        text: root.ui_data_model.b
    Button:
        size_hint: .2, .2
        text: "Start"
        on_press: root.button_press()
    Button:
        size_hint: .2, .2
        text: "Stop"
        on_press: root.button_press2()
""")

class RootWidget(GridLayout):
    ui_data_model = UI_DataModel()

    @ui_data_model.update
    def button_press(self, *args):
        common_data_model.a = 'A'

    @ui_data_model.update
    def button_press2(self, *args):
        common_data_model.b = 'B'

class TestApp(App):
    def build(self):
        return RootWidget()

app = TestApp()
app.run()