from django import template

register = template.Library()

symbols = ['.', ',', '/', ' ', '!', '?'] # символы для которых не нужно учитывать регистр

@register.filter()
def censor(value):

    # проверяем является ли значение строковым типом

    if isinstance(value, str):
        b = 0
        value1 = ''
        for i in range(len(value)):
            if b == 0:
                if value[i].isupper():
                    b = 1
                    value1 = value1 + value[i]

                else:
                    value1 = value1 + value[i]

            elif value[i] in symbols:
                b = 0
                value1 = value1 + value[i]

            else:
                value1 = value1 + '*'

        value = value1
        return f'{value}'
    else:
        print('Значение не является строковым')




