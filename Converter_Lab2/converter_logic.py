def convert(category, value, from_unit, to_unit):
    try:
        value = float(value)

        if category == "Температура":
            return convert_temperature(value, from_unit, to_unit)

        conversion_table = {
            "Длина": {
                "Миллиметры": 0.001,
                "Сантиметры": 0.01,
                "Метры": 1.0
            },
            "Масса": {
                "Граммы": 0.001,
                "Килограммы": 1.0,
                "Тонны": 1000.0
            },
            "Площадь": {
                "см²": 0.0001,
                "м²": 1.0,
                "га": 10000.0
            },
            "Валюта": {
                "Рубли": 1.0,
                "Доллары": 0.011,
                "Евро": 0.01
            }
        }

        units = conversion_table.get(category, {})
        if from_unit not in units or to_unit not in units:
            return "Ошибка: неизвестные единицы"

        # Переводим всё в базовую единицу (например, метры)
        base_value = value * units[from_unit]
        result = base_value / units[to_unit]
        return round(result, 4)

    except Exception as e:
        return f"Ошибка: {e}"


def convert_temperature(value, from_unit, to_unit):
    # Сначала переводим в цельсии
    if from_unit == "Фаренгейт":
        value = (value - 32) * 5/9
    elif from_unit == "Кельвин":
        value = value - 273.15

    # Теперь из цельсия в нужную
    if to_unit == "Фаренгейт":
        return round(value * 9/5 + 32, 2)
    elif to_unit == "Кельвин":
        return round(value + 273.15, 2)
    else:
        return round(value, 2)
