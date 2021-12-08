# -*- coding: utf-8 -*-
from random import randint
from Node import Node
from Function import Function
import matplotlib.pyplot as plt
class ElasticEnergyModel:
    def __init__(self, nodes:list = [], l:float = 2, k:float=1):
        self.k = k
        self.l = l
        self.nodes = nodes
        self.function = None
        
    def setupSimulation(self, quantity=20, stop_multiplier=1.2, step=0.05):
        self._generateRandomNodes(quantity)
        self.function = Function(quantity, self.l, self.k)
        self.step = step
        self.stop_multiplier = stop_multiplier
        
    def initiateSimulation(self):
        while True:
            values = [(node.x, node.y) for node in self.nodes] #[(Vx0, Vy0), ... ,(Vxn, Vyn)]
            calculated_gradient = self.function.calculateGradient(values) #[x1,y2, ..., xn, yn]
            if self._hasFinished(calculated_gradient) is True:
                break
            self._moveNodes(calculated_gradient)
            self._showProgress(calculated_gradient)
        self._printResults()
        
    def _showProgress(self, calculated_gradient):
        progress = self.step/max(calculated_gradient)*100
        if progress > 100:
            progress = 99
        print(f"{progress: .2f}%...")
    
    def _printResults(self):
        for node in self.nodes:
            print(f"({node.x}, {node.y})")
            plt.scatter(node.x, node.y)
        plt.show()
    
    
    def _hasFinished(self, calculated_gradient):
        stop_condition = self.step * self.stop_multiplier
        stop_flags = []
        for value in calculated_gradient:
            if -stop_condition < value < stop_condition:
                stop_flags.append(True)
            else:
                stop_flags.append(False)
        return all(stop_flags)
    
    def _moveNodes(self, calculated_gradient):
        gradient_index = -1
        for node in self.nodes:
            gradient_index += 1
            node.x = node.x - self.step*calculated_gradient[gradient_index]
            gradient_index += 1
            node.y = node.y - self.step*calculated_gradient[gradient_index]
            
    
    def _generateRandomNodes(self, quantity):
        minimum = (self.l* self.k) * -1
        maximum = abs(self.l* self.k)
        for _ in range(quantity):
            x = randint(minimum, maximum)
            y = randint(minimum, maximum)
            
            node = Node(x, y)
            self.nodes.append(node)
        
    
