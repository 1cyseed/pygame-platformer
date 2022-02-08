class Animal:
    def __init__(self, name, size, age, origin, food,  health = 'good' ):
        self.name =  name
        self.size = size
        self.age = age
        self.origin = origin
        self.food = food
        self.health = health

    def eat(self):
        print((f'{self.name} ate some food'))




class Dog(Animal):

    def __init__(self, name, size, age, origin, health = 'good'):
        super().__init__(self, name, size, age, origin, 'omnivore', health)


    def bark(self):
        print("WOOF!")

    def fetch(self):
        print((f'{self.name} got the stick'))


class GoldenRetriever(Dog):

    def __init__(self, name, color):
        super().__init__(self, name, 'black')

    def fetch(self):
        super().fetch()
        print(f'{self.name} is great and retrieving things!')


scrappy = Dog('Scrappy', 'small', 4)
scrappy.bark()



buddy = GoldenRetriever()
buddy.bark()

