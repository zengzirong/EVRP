import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

x = []
y = []

with open('../Instances/out(3,5).txt', 'r') as fp:
    while True:
        str = fp.readline()
        if not str:
            break
        x.append(float(str.split(":")[0]))
        y.append(float(str.split(":")[-1])*10)

e = 0.05
plt.figure(figsize=(9,6))
plt.subplot(234)
plt.plot(x[int(510/e):int(525/e)], y[int(510/e):int(525/e)], color='black', linestyle='-', label='quadratic part',linewidth=2)
#plt.title("")
plt.legend()


plt.subplot(235)
#plt.xlabel("t:[560,562)")
plt.plot(x[int(560/e):int(562/e)], y[int(560/e):int(562/e)], color='black', linestyle='-', label='linear part',linewidth=2)
plt.legend()

plt.subplot(236)
#plt.xlabel("t:[590,610)")
plt.plot(x[int(590/e):int(610/e)], y[int(590/e):int(610/e)], color='black', linestyle='-', label='constant part',linewidth=2)
plt.legend()

plt.subplot(211)
plt.plot(x[:], y[:], color='black', linestyle='-',label='resultant travel time function',linewidth=2.5)
plt.xlabel('Departure time')
plt.ylabel('Travel Time')
plt.subplots_adjust(left=0.1,bottom=0.05,top=0.95,right=0.9,hspace=0.25,wspace=0.25)
plt.legend()

plt.show()
