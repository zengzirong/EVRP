import math
arf1,T0,q,armax,armin,arRate,gamma,rou1,rou2,rou3,instance = 1.2 ,187, 0.88    , 0.7  ,0.4   ,0.51  ,0.86  , 14  ,  7  ,  4 ,""
NumVechicle=0
capacityVechicle=0
Depots=[]
pickups=[]
num_pair = 0
speedprofile = []
speedMatrix = []
dis = []
t_table = []

def readmain(arf11,T01,q1,armax1,armin1,arRate1,gamma1,rou11,rou21,rou31,instance1):
    global arf1,T0,q,armax,armin,arRate,gamma,rou1,rou2,rou3,instance,mu,Electric
    arf1,T0,q,armax,armin,arRate,gamma,rou1,rou2,rou3,instance = arf11,T01,q1,armax1,armin1,arRate1,gamma1,rou11,rou21,rou31,instance1
    global pickups,speedMatrix,dis,num_pair,NumVechicle,capacityVechicle,Depots,t_table
    t_table = [0,30,60,90,150,300,540,570,630,660,720,750,840]

    with open(instance, 'r', encoding='utf8') as f:
        cont = True
        c = 0
        sumq = 0
        li = []
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
                    #Vechicleweight = float(li[2][0])
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
                        sumq += float(i[2])
                        # print(int(i[1])),
                        pickups.append(({
                            "idx": int(i[0]),
                            "ID": int(i[1]),
                            "load": float(i[2]),
                            #"servtime": float(i[3])
                        }))
                    # print("pickups",pickups)


                elif li[0][0] == "[Speed":
                    speed_num = int(li[0][1][:-1])
                    speedprofile.append([])
                    speedprofile[speed_num].append(({"v0":float(li[1][0])}))
                    last_speed = float(li[1][0])
                    last_time = 0
                    for i in li[2:]:         
                        speedprofile[speed_num].append(({
                            "start": float(i[0]),
                            "end": float(i[1]),
                            "speed": float(i[-1]),
                            "a": (float(i[-1])-last_speed)/(float(i[0])-last_time)
                            }))
                        if i == li[-1]:
                            speedprofile[speed_num][4]["end"] = 100000
                        #print("st,en,a", float(i[-1]),last_speed,float(i[0]),last_time,
                              #(float(i[-1]) - last_speed) / (float(i[0]) - last_time))
                        last_speed = float(i[-1])
                        last_time = float(i[1])    
                    #print(speedprofile[speed_num][2]["start"])
                    #print("\n")

                elif li[0][1] == "choose":
                    for i in li[1:]:
                        speedMatrix.append([int(s) for s in i])
                li = []
    mp = {}
    #capacityVechicle = sumq
    with open('../cola_new/Customer2ID.txt', 'r', encoding='utf8') as f:
        cont = True
        li = []
        while cont:
            cont = f.readline()
            li = []
            li.append(cont.split())
            li = [x for x in li if x != []]
            if li != []:
                mp[int(li[0][0])] = int(li[0][1])
    DisT = [[0 for _ in range(2000)] for i in range(2000)]
    # print(len(DisT[1]))
    with open('../cola_new/ODMatrix.txt', 'r', encoding='utf8') as f:
        cont = True
        li = []
        while cont:
            cont = f.readline()
            li = []
            li.append(cont.split())
            li = [x for x in li if x != []]
            if li != []:
                DisT[int(li[0][0])][int(li[0][1])] = float(li[0][2])
    # print("dd", DisT[1][7])
    # print("dd",DisT[1][7])
    # global dis
    dis = [[0 for i in range(num_pair + 2)] for j in range(num_pair + 2)]
    # print(mp[504558778],mp[504557490],DisT[1184] [1180])
    for i in range(0, num_pair + 2):
        if i == 0 or i == num_pair + 1:
            idx = 1
        else:
            idx = mp[pickups[i]["ID"]]
        for j in range(0, num_pair + 2):
            if j == 0 or j == num_pair + 1:
                jdx = 1
            else:
                jdx = mp[pickups[j]["ID"]]
            # if idx == 1 and jdx == 7: print(i,j,idx,jdx,DisT[1][7])
            dis[i][j] = max(DisT[idx][jdx], 0.0000000001)
            # if dis[i][j] == 0.0000000001:
            # print(i,j)

    # print(dis[1])
    long = {}
    with open('../cola_new/long', 'r', encoding='utf8') as f:
        cont = True
        li = []
        while cont:
            cont = f.readline()
            li = []
            li.append(cont.split())
            li = [x for x in li if x != []]
            if li != []:
                long[int(li[0][0])] = [float(li[0][-2]), float(li[0][-1])]
    for i in range(1, len(pickups)):
        pickups[i]["x"] = long[pickups[i]["ID"]][0]
        pickups[i]["y"] = long[pickups[i]["ID"]][1]

    #print(speedprofile)
def getbp():
    global  speedMatrix,pickups,dis,speedprofile,num_pair
    return speedMatrix,pickups,dis,speedprofile,num_pair
def get_para():
    global arf1,  T0, q, armax, armin, arRate, gamma, rou1, rou2, rou3
    return arf1,  T0, q, armax, armin, arRate, gamma, rou1, rou2, rou3
def gettraveltime():
    global speedMatrix, dis, speedprofile, t_table
    return speedMatrix,dis,speedprofile,t_table
def getcli():
    global speedMatrix,pickups,dis,num_pair,arf1
    return speedMatrix,pickups,dis,num_pair,arf1
def gettestini():
    global pickups, num_pair, capacityVechicle
    return pickups,num_pair,capacityVechicle
def feas():
    global pickups, num_pair, capacityVechicle,Electric
    #print("?>",pickups)
    return pickups,num_pair,capacityVechicle,Electric
def seginit():
    global pickups,dis,num_pair
    return pickups,dis,num_pair

def getalns():
    global T0,q,armax, armin, arRate,gamma, rou1, rou2, rou3
    return T0,q,armax, armin, arRate,gamma, rou1, rou2, rou3
def getread():
    global pickups, capacityVechicle, speedMatrix, dis, speedprofile,num_pair
    return pickups,  capacityVechicle, speedMatrix, dis, speedprofile,num_pair
def getls():
    global pickups,num_pair
    return pickups,num_pair
def getW_a123():
    global a1,a2,a3,mu
    a1, a2, a3,mu,vehm = 479.1,-18.93,0.7876,1,1507
    return a1,a2,a3,mu,vehm
def getclu():
    global num_pair,pickups
    #print(pickups)
    return num_pair,pickups[1:],3
if __name__ == "__main__":
    print("")