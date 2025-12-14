import random

def versiculo_del_dia(data):
    cap = random.choice(list(data['chapters'].keys()))
    ver = random.choice(list(data['chapters'][cap].keys()))
    return data['chapters'][cap][ver]
