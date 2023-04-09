import django.db.models
import xlsxwriter


class ReportWriter(type):
    """Writer обеспечивает всю работу с xlsxwriter,
    понимает, как мержить ячейки и на какой строке находится,
    ему нужно посылать сигнал перехода на следующую строку"""
    def __new__(cls, name, bases, attrs):
        print(name, bases, attrs)
        # Проверяем наличие атрибута 'fields' в определении класса
        if 'fields' in attrs and isinstance(attrs['fields'], str):
            attrs['fields'] = (attrs['fields'],)  # Преобразуем строку в кортеж
        # Создаем новый класс с помощью метакласса type
        return super().__new__(cls, name, bases, attrs)

    def write_row(self):
        pass

    def write_all(self):
        pass
