import kivy
from kivy.uix.floatlayout import FloatLayout
kivy.require('1.7.0')

from kivy.app import App
from kivy.lang import Builder   
from kivy.event import EventDispatcher
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty

class DataModel(object):
    def __init__(self):
        self.a = 'An quod ita callida est, ut optime possit architectari voluptates? Quodsi ipsam honestatem undique pertectam atque absolutam. Paria sunt igitur. Quorum sine causa fieri nihil putandum est. Ad corpus diceres pertinere-, sed ea, quae dixi, ad corpusne refers? Quis est, qui non oderit libidinosam, protervam adolescentiam? Illa tamen simplicia, vestra versuta. Non igitur potestis voluptate omnia dirigentes aut tueri aut retinere virtutem. \n\nQuid enim tanto opus est instrumento in optimis artibus comparandis? Graccho, eius fere, aequal? Ergo instituto veterum, quo etiam Stoici utuntur, hinc capiamus exordium. Hoc loco tenere se Triarius non potuit. Perturbationes autem nulla naturae vi commoventur, omniaque ea sunt opiniones ac iudicia levitatis.'
        self.b = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quantum Aristoxeni ingenium consumptum videmus in musicis? Nam quid possumus facere melius? Laboro autem non sine causa; Apud ceteros autem philosophos, qui quaesivit aliquid, tacet; Duo Reges: constructio interrete. Sed nimis multa. Quo modo autem optimum, si bonum praeterea nullum est? Compensabatur, inquit, cum summis doloribus laetitia.'

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
        common_data_model.a = 'A'

    @ui_data_model.update
    def button_press2(self, *args):
        common_data_model.b = 'B'

class TestApp(App):
    def build(self):
        return RootWidget()

app = TestApp()
app.run()