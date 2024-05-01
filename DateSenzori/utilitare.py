
def adauga_element_lista_fixa(lista, element):
        if len(lista) > 5:
               lista.pop(0)
        lista.append(element)

def medie_ignora_none(data):
    data = [x for x in data if x is not None]
    return sum(data) / len(data) if data else 0