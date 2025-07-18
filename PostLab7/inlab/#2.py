import numpy as np
import matplotlib.pyplot as plt

# Define the cubic function
def cubic_function(x):
    return x**3 + 53 * x**2 - 400 * x + 25

# Generate x values from -30 to 30 with integer steps
x = np.arange(-30, 31)  # Integer arguments
y = cubic_function(x)    # Compute y values for the cubic function

# Plot the data
plt.plot(x, y, 'go-', label='cubic polynomial')  
plt.xlabel('x value')
plt.ylabel('y value')
plt.title("Cubic Polynomial Plot")
plt.grid(True)  # Include the grid
plt.legend()

# Annotate the graph
plt.annotate('cubic polynomial', xy=(0, 25), xytext=(10, 10000),
             arrowprops=dict(facecolor='black', shrink=0.05))

# Display the plot
plt.show()
