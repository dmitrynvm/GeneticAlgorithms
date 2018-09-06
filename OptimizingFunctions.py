def QuadraticFunction(self):
    x = (self.grid[self.sign])[0]
    return x**2 - 31*x      


def QuadraticFunction2d(self):
    x = (self.grid[self.sign])[0]
    y = (self.grid[self.sign])[1]
    return -x**2 + 31*x - y**2 + 31*y
        
    
def RosenbrokFunction(self):
    x1 = (self.grid[self.sign])[0]
    x2 = (self.grid[self.sign])[1]
    return 100*(x2-x1**2)**2 + (1-x1)**2
    
    
def MatyasFunction(self):
    x1 = (self.grid[self.sign])[0]
    x2 = (self.grid[self.sign])[1]
    return 0.26 * (x1**2 + x2**2) - 0.48 * x1 * x2