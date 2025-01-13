import math

class Shape:

    def area(self):
        pass

    def perimeter(self):
        pass



class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius 

    def area(self):
        return math.pi * (self.radius ** 2)
    
    def perimeter(self):
        return 2 * math.pi * self.radius 
    

class Rectangle(Shape):
    def __init__(self, height, width):
        self.height = height
        self.width = width 

    def area(self):
        return self.height * self.width
    
    def perimeter(self):
        return (self.height + self.width) * 2 
    