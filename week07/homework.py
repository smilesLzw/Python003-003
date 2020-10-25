from abc import ABCMeta, abstractmethod
from enum import IntEnum


class Animal(metaclass=ABCMeta):
    class BodyShape(IntEnum):
        SMALL = 1
        MID = 2
        BIG = 3

    def __init__(self, type, body, character):
        self.type = type
        self.body = self.BodyShape(body)
        self.character = character

    @property
    def isFerocious(self):
        if self.body >= self.BodyShape.MID and self.type == '食肉' \
            and self.character == '凶猛':
            return True
        return False


class Dog(Animal):
    bark = 'Wang'

    def __init__(self, name, type, body, character):
        self.name = name
        super().__init__(type, body, character)

    @property
    def isPet(self):
        return False if self.isFerocious else True


class Cat(Animal):
    bark = 'Meow'

    def __init__(self, name, type, body, character):
        self.name = name
        super().__init__(type, body, character)

    @property
    def isPet(self):
        return False if self.isFerocious else True


class Zoo():
    def __init__(self, name):
        self.name = name
        self.animals = []

    def add_animal(self, animal):
        if animal not in self.animals:
            setattr(self, animal.__class__.__name__, None)
            self.animals.append(animal)


if __name__ == '__main__':
    z = Zoo('时间动物园')
    cat1 = Cat('大花猫1', '食肉', 1, '温顺')
    z.add_animal(cat1)
    have_cat = hasattr(z, 'Cat')
    print(have_cat)