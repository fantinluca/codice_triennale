class test:
    def __init__(self, id = 0):
        self.id = id

    def __hash__(self):
        return hash(repr(self))
    
a = test(1)
b = test(2)

c = {a: 2, b: 55}

for a,b in c.items():
    print(str(a.id) + " " + str(b))