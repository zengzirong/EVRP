import numpy as np
import matplotlib.pyplot as plt

f = open("../para_result/0.01_0.50_0.01_new", "r")
lines=[]
for line in f:
    lines.append(line)
f.close()
x=[]
y=[]
iterations = 0
for i in range(len(lines)):
    words = lines[i].split(' ')
    if(len(words) == 4 and words[2] == 'iteration'):
        iterations += 1
        if(iterations > 1):
            x.append(iterations)
            words_nextline = lines[i+1].split(' ')
            y.append(float(words_nextline[3]))
for i in range(len(x)):
    x[i] /= iterations
plt.plot(x, y, label = '(0.01, 0.05, 0.01)')

f = open("../para_result/0.01_0.85_0.04_new", "r")
lines=[]
for line in f:
    lines.append(line)
f.close()
x=[]
y=[]
iterations = 0
for i in range(len(lines)):
    words = lines[i].split(' ')
    if(len(words) == 4 and words[2] == 'iteration'):
        iterations += 1
        if(iterations > 1):
            x.append(iterations)
            words_nextline = lines[i+1].split(' ')
            y.append(float(words_nextline[3]))
for i in range(len(x)):
    x[i] /= iterations
plt.plot(x, y, label = '(0.01, 0.85, 0.04)')

f = open("../para_result/0.05_0.75_0.03_new", "r")
lines=[]
for line in f:
    lines.append(line)
f.close()
x=[]
y=[]
iterations = 0
for i in range(len(lines)):
    words = lines[i].split(' ')
    if(len(words) == 4 and words[2] == 'iteration'):
        iterations += 1
        if(iterations > 1):
            x.append(iterations)
            words_nextline = lines[i+1].split(' ')
            y.append(float(words_nextline[3]))
for i in range(len(x)):
    x[i] /= iterations
plt.plot(x, y, label = '(0.05, 0.75, 0.03)')

f = open("../para_result/0.23_0.85_0.02_new", "r")
lines=[]
for line in f:
    lines.append(line)
f.close()
x=[]
y=[]
iterations = 0
for i in range(len(lines)):
    words = lines[i].split(' ')
    if(len(words) == 4 and words[2] == 'iteration'):
        iterations += 1
        if(iterations > 1):
            x.append(iterations)
            words_nextline = lines[i+1].split(' ')
            y.append(float(words_nextline[3]))
for i in range(len(x)):
    x[i] /= iterations
plt.plot(x, y, label = '(0.23, 0.85, 0.02)')

f = open("../para_result/0.25_0.75_0.02_new", "r")
lines=[]
for line in f:
    lines.append(line)
f.close()
x=[]
y=[]
iterations = 0
for i in range(len(lines)):
    words = lines[i].split(' ')
    if(len(words) == 4 and words[2] == 'iteration'):
        iterations += 1
        if(iterations > 1):
            x.append(iterations)
            words_nextline = lines[i+1].split(' ')
            y.append(float(words_nextline[3]))
for i in range(len(x)):
    x[i] /= iterations
plt.plot(x, y, label = '(0.25, 0.75, 0.02)')

plt.xlabel("Iteration Ratio")
plt.ylabel("energy consumption")
plt.legend()
plt.show()