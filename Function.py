# -*- coding: utf-8 -*-
from math import isnan
from sympy import sqrt, symbols
class Function:
    def __init__(self, n , l, k):
        self.n = n
        self.l = l
        self.k = k
        self.variables = None
        self.function = self._generateFunction()
        self.gradient = self._generateGradient()
        
    def calculateGradient(self, values):
        # values = [(Vx0, Vy0), ... ,(Vxn, Vyn)]
        calculated_gradient = []
        substitutions = {}
        
        for i in range(len(self.variables)):
            substitutions[self.variables[i][0]] = values[i][0]
            substitutions[self.variables[i][1]] = values[i][1]
            
        for component in self.gradient:
            component = component.evalf(4, subs=substitutions,chop=True)
            
            if isnan(component):
                component = 0
            calculated_gradient.append(component)
        return calculated_gradient
        
        
    def _generateFunction(self):
        constant_term = (self.k/2)
        function_terms = [] # list of sqrt's times first_term 
        xs = symbols(f"x:{self.n}")
        ys = symbols(f"y:{self.n}")
        self.variables = [(xs[i], ys[i]) for i in range(self.n)]
        #[(xi, yi), (xi+1, yi+1), ...]
        
        for i in range(self.n):
            for j in range(i + 1, self.n):# Para pegar todo j > i para todo i 
                # Assim toda tupla será (i,j>i)
                function_terms.append(
                    (self._generateNthSqrt(i, j) - self.l)**2)
                
        return constant_term * sum(function_terms)
        
    def _generateNthSqrt(self, i, j):
        x_variables = (self.variables[i][0], self.variables[j][0])
        y_variables = (self.variables[i][1], self.variables[j][1])
        nth_sqrt = sqrt((x_variables[0]- x_variables[1])**2 + 
                        (y_variables[0]- y_variables[1])**2)
        return nth_sqrt
        
    def _generateGradient(self):
        gradient = [] # [x1,y2, ..., xn, yn]
        for variable_tuple in self.variables:
            for i in range(2):
                variable = variable_tuple[i]
                gradient.append(self.function.diff(variable))
        return gradient
        