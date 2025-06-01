def strict(func):
    def wrapper(*args, **kwargs):
        # Получаем аннотации типов из функции
        type_hints = func.__annotations__

        # Получаем имена аргументов функции
        arg_names = func.__code__.co_varnames[: func.__code__.co_argcount]

        # Проверяем позиционные аргументы
        for i, arg in enumerate(args):
            arg_name = arg_names[i]

            # Если для этого аргумента есть аннотация типа
            if arg_name in type_hints:
                expected_type = type_hints[arg_name]

                # Проверяем тип аргумента
                if not isinstance(arg, expected_type):
                    actual_type = type(arg).__name__
                    raise TypeError(
                        f"Argument '{arg_name}' must be {expected_type.__name__}, "
                        f"not {actual_type}"
                    )

        # Проверяем именованные аргументы
        for arg_name, arg_value in kwargs.items():
            # Пропускаем 'return' так как это аннотация возвращаемого значения
            if arg_name == "return":
                continue

            if arg_name in type_hints:
                expected_type = type_hints[arg_name]
                if not isinstance(arg_value, expected_type):
                    actual_type = type(arg_value).__name__
                    raise TypeError(
                        f"Argument '{arg_name}' must be {expected_type.__name__},"
                        f"not {actual_type}"
                    )

        # Если все проверки пройдены, вызываем оригинальную функцию
        return func(*args, **kwargs)

    return wrapper
