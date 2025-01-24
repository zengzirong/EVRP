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
plt.figure(figsize=(9,9))
plt.subplot(334)
plt.xlabel("t:[0,90)")
plt.plot(x[:int(90/e)], y[:int(90/e)], color='black', linestyle='-', label='ALNS_LS')

plt.subplot(335)
plt.xlabel("t:[90,136)")
plt.plot(x[int(90/e):int(136/e)], y[int(90/e):int(136/e)], color='black', linestyle='-', label='ALNS_LS')

plt.subplot(336)
plt.xlabel("t:[136,180)")
plt.plot(x[int(136/e):int(180/e)], y[int(136/e):int(180/e)], color='black', linestyle='-', label='ALNS_LS')

plt.subplot(337)
plt.xlabel("t:[180,540)")
plt.plot(x[int(180/e):int(540/e)], y[int(180/e):int(540/e)], color='black', linestyle='-', label='ALNS_LS')


plt.subplot(338)
plt.xlabel("t:[540,690)")
plt.plot(x[int(540/e):int(690/e)], y[int(540/e):int(690/e)], color='black', linestyle='-', label='ALNS_LS')


plt.subplot(339)
plt.xlabel("t:[690,840)")
plt.plot(x[int(690/e):int(840/e)], y[int(690/e):int(840/e)], color='black', linestyle='-', label='ALNS_LS')

plt.subplot(311)
plt.plot(x[:], y[:], color='black', linestyle='-')
plt.xlabel('Departure time')
plt.ylabel('Travel Time')
plt.subplots_adjust(left=0.1,bottom=0.05,top=0.95,right=0.9,hspace=0.25,wspace=0.25)
plt.show()
