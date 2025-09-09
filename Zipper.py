import matplotlib.pyplot as plt

class Tube:

    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

        self.num_sections = 1
        self.sections = []


    def add_joint(self, parameters):
        pass

    def visualize(self):
        