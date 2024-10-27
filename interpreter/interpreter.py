# MEMBUAT TOKEN
class token:
    def __init__(self, type_,value):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.tpe}:{self.value}'
        return f'{self.type}'
        