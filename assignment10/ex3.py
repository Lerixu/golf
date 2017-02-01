"""
Introduction to Web Science
Assignment 10
exercise 3
Team : golf

"""

import numpy as np

height_ehrenbreitstein=[150,180,220]

print("** Results for the Ehrenbreitstein Fortress")
print("Mean : %s "%np.mean(height_ehrenbreitstein))
print("Standard deviation : %s "%np.std(height_ehrenbreitstein))
print("Variance : %s "%np.var(height_ehrenbreitstein))
print()
height_fernmeldeturm=[350,300,450]
print("** Results for the Fernmeldeturm Koblenz")
print("Mean : %s "%np.mean(height_fernmeldeturm))
print("Standard deviation : %s "%np.std(height_fernmeldeturm))
print("Variance : %s "%np.var(height_fernmeldeturm))