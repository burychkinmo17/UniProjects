from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '340')
Config.set('graphics', 'height', '575')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation


class CircularButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.original_color = kwargs.get('background_color', (0.3, 0.3, 0.3, 1))
        self.background_color = self.original_color
        self.bind(pos=self.update_shape, size=self.update_shape)
        self.bind(on_press=self.animate_press)
        self.bind(on_release=self.animate_release)

    def update_shape(self, *args):
        self.draw_button(self.background_color)

    def draw_button(self, color):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.height / 2])

    def animate_press(self, *args):
        lighter = [min(c + 0.2, 1) for c in self.original_color[:3]] + [1]
        anim = Animation(background_color=lighter, d=0.1)
        anim.bind(on_progress=lambda a, w, p: self.draw_button(self.background_color))
        anim.start(self)

    def animate_release(self, *args):
        anim = Animation(background_color=self.original_color, d=0.1)
        anim.bind(on_progress=lambda a, w, p: self.draw_button(self.background_color))
        anim.start(self)


class Calculator(GridLayout):
    theme = StringProperty("dark")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 2
        self.padding = 10
        self.spacing = 10
        self.expression = ""

        self.themes = {
            "dark": {
                "bg": (0.1, 0.1, 0.1, 1),
                "text": (1, 1, 1, 1),
                "digit": (0.2, 0.2, 0.2, 1),
                "op": (0.4, 0.2, 0.1, 1)
            },
            "light": {
                "bg": (1, 1, 1, 1),
                "text": (0, 0, 0, 1),
                "digit": (0.9, 0.9, 0.9, 1),
                "op": (1, 0.8, 0.4, 1)
            }
        }

        self.result_input = TextInput(
            multiline=False,
            readonly=True,
            halign="right",
            font_size=48,
            background_color=self.themes[self.theme]["bg"],
            foreground_color=self.themes[self.theme]["text"],
            size_hint=(1, 0.2)
        )
        self.add_widget(self.result_input)

        # Обёртка для центрирования кнопок
        buttons_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.8), padding=[0, 0, 0, 0])
        self.buttons_grid = GridLayout(cols=4, spacing=10, size_hint=(None, 1))
        self.buttons_grid.width = 320  # Ширина сетки фиксированная
        buttons_box.add_widget(self.buttons_grid)
        self.add_widget(buttons_box)

        self.create_buttons()

    def create_buttons(self):
        self.buttons_grid.clear_widgets()
        current_theme = self.themes[self.theme]

        buttons = [
            ("7", self.add_char), ("8", self.add_char), ("9", self.add_char), ("/", self.add_char),
            ("4", self.add_char), ("5", self.add_char), ("6", self.add_char), ("*", self.add_char),
            ("1", self.add_char), ("2", self.add_char), ("3", self.add_char), ("-", self.add_char),
            ("0", self.add_char), (".", self.add_char), ("^", self.add_char), ("+", self.add_char),
            ("C", self.clear), ("BS", self.backspace), ("=", self.calculate), ("Theme", self.toggle_theme)
        ]

        digit_labels = set("0123456789")

        for label, callback in buttons:
            bg_color = current_theme["digit"] if label in digit_labels else current_theme["op"]

            btn = CircularButton(
                text=label,
                font_size=22,
                background_color=bg_color,
                color=current_theme["text"],
                size_hint=(1, None),
                height=80
            )
            btn.bind(on_press=callback)
            self.buttons_grid.add_widget(btn)

    def toggle_theme(self, _):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.result_input.background_color = self.themes[self.theme]["bg"]
        self.result_input.foreground_color = self.themes[self.theme]["text"]
        self.create_buttons()

    def add_char(self, instance):
        self.expression += "^" if instance.text == "^" else instance.text
        self.result_input.text = self.expression

    def clear(self, _):
        self.expression = ""
        self.result_input.text = ""

    def backspace(self, _):
        self.expression = self.expression[:-1]
        self.result_input.text = self.expression

    def calculate(self, _):
        try:
            expr = self.expression.replace("^", "**")
            value = eval(expr)
            if isinstance(value, float) and value.is_integer():
                result = str(int(value))
            else:
                result = str(value)
        except ZeroDivisionError:
            result = "Ошибка: деление на 0"
        except Exception:
            result = "Ошибка"
        self.expression = result if result.replace('.', '', 1).isdigit() else ""
        self.result_input.text = result


class CalculatorApp(App):
    def build(self):
        self.title = "Calculator"
        return Calculator()


if __name__ == "__main__":
    CalculatorApp().run()
