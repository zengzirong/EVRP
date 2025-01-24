from readData import getcli
import math
from travel_time import ttTao
speedMatrix,pickup,delivery,dis ,num_pair = [],[],[],[],0
arf1, arf2 = 0.05, 0.02
a1,a2,a3 = 0.02,0.05,0.3
CL,CL1,CL2 = [],[],[]

def init():
    global speedMatrix,pickup,dis ,num_pair,arf1,CL,CL1,CL2
    speedMatrix, pickup,  dis, num_pair,arf1 = getcli()
    CL = [[1000000 for i in range(num_pair + 1)] for j in range(num_pair + 1)]

    for i in range(1,num_pair+1):
        for j in range(1,num_pair+1):
            if i == j:
                continue
            CL[i][j] = arf1*(math.fabs(pickup[i]["load"]- pickup[j]["load"] ) )+\
                         (math.fabs(pickup[i]["x"] - pickup[j]["x"])+math.fabs(pickup[i]["y"] - pickup[j]["y"]))



def getcl():
    global CL
    return CL
if __name__=='__main__':
    print("")
