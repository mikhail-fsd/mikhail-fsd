class Rectangle:

    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def __str__(self):
        message = f'Rectangle(width={self.width}, height={self.height})'
        return message

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def get_area(self):
        area = self.width * self.height
        return area

    def get_perimeter(self):
        perimeter = 2 * self.width + 2 * self.height
        return perimeter

    def get_diagonal(self):
        diagonal = (self.width ** 2 + self.height ** 2) ** .5
        return diagonal

    def get_picture(self):
        if self.width > 50 or self.height > 50: return 'Too big for picture.'
        picture = '\n'.join([''.join(['*' for _ in range(self.width)]) for _ in range(self.height)]) + '\n'
        return picture

    def get_amount_inside(self, another_shape):
        amount = self.get_area() // another_shape.get_area()
        return amount
        
class Square(Rectangle):

    def __init__(self, side):
        self.set_side(side)

    def __str__(self):
        message = f'Square(side={self.side})'
        return message

    def set_side(self, side):
        self.height = self.width = self.side = side

    def set_width(self, side):
        self.set_side(side)

    def set_height(self, side):
        self.set_side(side)

rt = Rectangle(3,5)
print(rt.get_picture())

