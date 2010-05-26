class Dave:
    x = 1
    def __init__(self, y):
        self.y = y


monkey = Dave(5)
bob = Dave(100)

print monkey.x, monkey.y
print bob.x, bob.y

monkey.x = 2
monkey.y = 3

print monkey.x, monkey.y
print bob.x, bob.y

bob.x = 1001
bob.y = 1002

print monkey.x, monkey.y
print bob.x, bob.y
