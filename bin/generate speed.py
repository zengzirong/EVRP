import numpy as np

# 生成100x100的数组，初始值全部为0
n = int(input())
arr = np.zeros((n+2, n+2), dtype=int)

# 设置边界值为4
arr[:, [0, -1]] = 4
arr[[0, -1], :] = 4

# 在除了边界之外的位置上随机填充0到4之间的整数
arr[1:-1, 1:-1] = np.random.randint(0, 5, (n, n))

# 将生成的数组输出到文件中
np.savetxt('output.txt', arr, fmt='%d')
