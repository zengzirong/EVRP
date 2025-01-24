import random
import math

# 设置正态分布的均值和标准差
mu = 250
sigma = 75
NumVechicle=0
capacityVechicle=0
Depots=[]
pickups=[]
num_pair = 0
with open('../cola_new/500.txt', 'r', encoding='utf8') as f:
    cont = True
    li = []
    c = 0
    pickups.append(({}))
    while cont:
        cont = f.readline()
        li.append(cont.split())
        li = [x for x in li if x != []]
        # print(li)
        if cont == '\n' and li != []:
            c = c + 1
            # print(li)
            # print(li[0])
            if c == 1:
                NumVechicle = int(li[0][0])
                capacityVechicle = float(li[1][0])
                # Vechicleweight = float(li[2][0])
                Electric = float(li[2][0])

            elif li[0][0] == "[Node]" or li[0][0] == "[Depot]":
                for i in li[1:]:
                    Depots.append(({
                        "idx": int(i[0]),
                        "x": 103.967432,
                        "y": 30.584035
                    }))
                # print("Depots",Depots)
            elif li[0][0] == "[pickup]" or li[0][0] == "[Pickup]":
                for i in li[1:]:
                    # print(i)
                    num_pair += 1
                    # print(int(i[1])),
                    pickups.append(({
                        "idx": num_pair,
                        "ID": int(i[0]),
                    # "servtime": float(i[3])
                    }))
            li = []

# 打开文件并准备写入数据
with open("../cola_new/random_numbers.txt", "w") as f:
    num = 0
    for i in range(1,502):
        num+=1
        while True:
            # 生成正态分布的随机数
            rand_num = round(random.normalvariate(mu, sigma))

            # 如果随机数在 10 到 500 的范围内，则返回该数
            if rand_num >= 10 and rand_num <= 500:
                break

        # 写入随机数到文件中
        f.write(str(num) +'  '+str(pickups[i]["ID"])+'  '+ str(rand_num) + "\n")
