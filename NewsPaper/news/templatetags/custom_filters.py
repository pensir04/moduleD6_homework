from django import template

register = template.Library()  # если мы не зарегестрируем наши фильтры, то django никогда не узнает где именно их искать и фильтры потеряются :(

@register.filter(name='multiply') # регистрируем наш фильтр под именем multiply, чтоб django понимал, что это именно фильтр, а не простая функция
def multiply(value, arg): # первый аргумент здесь — это то значение, к которому надо применить фильтр,
                          # второй аргумент — это аргумент фильтра, т.е. примерно следующее будет в шаблоне value|multiply:arg
    return str(value) * arg # возвращаемое функцией значение — это то значение, которое подставится к нам в шаблон

@register.filter(name='censor')
def censor(value, arg):
    list_bad_words = ['черт', 'блин', 'капец']
    value_edited = value
    value_final = ''
    for word in list_bad_words:
        value_edited = value_edited.lower()
        value_temp = value_edited.replace(word, arg * len(word))
        value_edited = value_temp

    for i in range(0, len(value)):
        if (value[i] != value_edited[i]) & (value_edited[i].isalpha()):
            temp = value_edited[i].upper()
            value_final += temp
        else:
            value_final += value_edited[i]
    return value_final
