import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pylab import mpl
from matplotlib.pyplot import MultipleLocator

file_path = '../result_spp.xlsx'
no_spp = pd.read_excel(file_path,usecols=[1])
no_spp_li = no_spp.values.tolist()
#print(":",no_spp_li)
spp = pd.read_excel (file_path,usecols=[2])
spp_li = spp.values.tolist()

result_no_spp,result_spp = [],[]
#a = input()
'''
for no_li in no_spp_li:
    result_no_spp.append(no_li[0]/1e6)
for li in spp_li:
    result_spp .append(li[0]/1e6)
'''
for i in range(0,len(no_spp_li)):
    v1,v2 = no_spp_li[i][0] ,spp_li[i][0]
    if v2 > 1e6:
        k1 = v1-min(v1//1e6,v2//1e6)*1e6
        k2 = v2 - min(v1 // 1e6, v2 // 1e6) * 1e6
    else:
        k1 = v1 - min(v1 // 1e5, v2 // 1e5) * 1e5
        k2 = v2 - min(v1 // 1e5, v2 // 1e5) * 1e5
    result_no_spp.append(k1)
    result_spp.append(k2)
fig = plt.figure()
# 画图区域分成1行1列。选择第一块区域。
ax1 = fig.add_subplot(1,1, 1)
# 标题
ax1.set_title("Best Solution Quality Comparison")
# 横轴名称。
ax1.set_xlabel("The minimum W obtained by LNS-SPP")
# 纵轴名称。
ax1.set_ylabel("The minimum W obtained by LNS (without SPP)")
x=np.arange(0,1.01*1e6,1e5)
y=x
plt.plot(x,y,color="red",marker = '*',ls = ':',label='45° Line')
plt.scatter(result_spp,result_no_spp, color = '#88c999',cmap='viridis')
plt.legend(prop = {'size':13})
plt.show()