class Cable():

    def __init__(self, house):
        self.x = house.x
        self.y = house.y
        self.path = [[self.x,self.y]]
        
    def up(self):
        self.y += 1
        self.path.append([self.x,self.y])
        
    def down(self):
        self.y -= 1
        self.path.append([self.x, self.y])
        
    def right(self):
        self.x += 1
        self.path.append([self.x,self.y])
        
    def left(self):
        self.x -= 1
        self.path.append([self.x, self.y])