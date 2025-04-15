from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle
from converter_logic import convert
from kivy.uix.image import Image
Window.size = (360, 640)


# --- Главный экран со списком категорий ---
class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Цвета
        bg_color = get_color_from_hex("#2e003e")
        button_color = get_color_from_hex("#9b5de5")
        text_color = (1, 1, 1, 1)

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        with self.layout.canvas.before:
            Color(*bg_color)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=lambda *_: setattr(self.bg_rect, 'size', self.size))
            self.bind(pos=lambda *_: setattr(self.bg_rect, 'pos', self.pos))

        img = Image(source="pointers.jpg", size_hint=(1, 0.3), allow_stretch=True, keep_ratio=True)
        self.layout.add_widget(img)

        categories = ["Длина", "Масса", "Температура", "Площадь", "Валюта"]
        for category in categories:
            btn = Button(text=category, size_hint=(1, None), height=60,
                         background_color=button_color, color=text_color)
            btn.bind(on_press=self.open_converter)
            self.layout.add_widget(btn)

        self.add_widget(self.layout)

    def open_converter(self, instance):
        converter_screen = self.manager.get_screen("converter")
        converter_screen.category = instance.text
        converter_screen.on_pre_enter()
        self.manager.transition.direction = "left"
        self.manager.current = "converter"


# --- Экран конвертации ---
class ConverterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category = ""

        # Цвета
        bg_color = get_color_from_hex("#2e003e")
        button_color = get_color_from_hex("#9b5de5")
        accent_color = get_color_from_hex("#c77dff")
        text_color = (1, 1, 1, 1)

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        with self.layout.canvas.before:
            Color(*bg_color)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=lambda *_: setattr(self.bg_rect, 'size', self.size))
            self.bind(pos=lambda *_: setattr(self.bg_rect, 'pos', self.pos))

        self.title_label = Label(text="Конвертация", font_size=24, size_hint=(1, None), height=40, color=text_color)

        self.input_value = TextInput(hint_text="Введите значение", multiline=False,
                                     size_hint=(1, None), height=50, input_filter='float',
                                     foreground_color=text_color,
                                     background_color=(0.2, 0.2, 0.2, 1),
                                     cursor_color=text_color)

        self.unit_from = Spinner(text="Выбрать из", size_hint=(1, None), height=50,
                                 background_color=(0.2, 0.2, 0.2, 1), color=text_color)

        self.unit_to = Spinner(text="Конвертировать в", size_hint=(1, None), height=50,
                               background_color=(0.2, 0.2, 0.2, 1), color=text_color)

        self.swap_button = Button(text="⇄ Поменять", size_hint=(1, None), height=50,
                                  background_color=accent_color, color=text_color)
        self.swap_button.bind(on_press=self.swap_units)

        self.result_label = Label(text="Результат: ", font_size=20, size_hint=(1, None), height=40, color=text_color)

        self.back_button = Button(text="← Назад", size_hint=(1, None), height=50,
                                  background_color=button_color, color=text_color)
        self.back_button.bind(on_press=self.go_back)

        # Автоконвертация
        self.input_value.bind(text=self.perform_conversion)
        self.unit_from.bind(text=self.perform_conversion)
        self.unit_to.bind(text=self.perform_conversion)

        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.input_value)
        self.layout.add_widget(Label(text="Из", font_size=18, size_hint=(1, None), height=30, color=text_color))
        self.layout.add_widget(self.unit_from)
        self.layout.add_widget(Label(text="В", font_size=18, size_hint=(1, None), height=30, color=text_color))
        self.layout.add_widget(self.unit_to)

        self.layout.add_widget(self.swap_button)
        self.layout.add_widget(self.result_label)
        self.layout.add_widget(self.back_button)
        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        self.title_label.text = f"Конвертация: {self.category}"

        units = {
            "Длина": ["Миллиметры", "Сантиметры", "Метры"],
            "Масса": ["Граммы", "Килограммы", "Тонны"],
            "Температура": ["Цельсий", "Фаренгейт", "Кельвин"],
            "Площадь": ["м²", "см²", "га"],
            "Валюта": ["Рубли", "Доллары", "Евро"]
        }

        selected_units = units.get(self.category, [])
        self.unit_from.values = selected_units
        self.unit_to.values = selected_units
        if selected_units:
            self.unit_from.text = selected_units[0]
            self.unit_to.text = selected_units[1]

        self.perform_conversion()

    def swap_units(self, _):
        self.unit_from.text, self.unit_to.text = self.unit_to.text, self.unit_from.text

    def go_back(self, _):
        self.manager.transition.direction = "right"
        self.manager.current = "main"

    def perform_conversion(self, *args):
        try:
            from_unit = self.unit_from.text
            to_unit = self.unit_to.text
            value_text = self.input_value.text

            result = convert(self.category, value_text, from_unit, to_unit)
            self.result_label.text = f"Результат: {result}"

        except Exception as e:
            self.result_label.text = f"Ошибка: {e}"


# --- Само приложение ---
class ConverterApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name="main"))
        sm.add_widget(ConverterScreen(name="converter"))
        return sm


if __name__ == "__main__":
    ConverterApp().run()
