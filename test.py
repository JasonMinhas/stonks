import matplotlib.pyplot as plt
import numpy as np

x = np.arange(61).astype(float)
y1 = np.exp(0.1 * x)
y2 = np.exp(0.09 * x)

plt.plot(x, y1)
plt.plot(x, y2)

for var in (y1, y2):
    plt.annotate('%0.2f' % var.max(), xy=(1, var.max()), xytext=(8, 0),
                 xycoords=('axes fraction', 'data'), textcoords='offset points')

plt.show()