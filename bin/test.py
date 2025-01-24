import random
from local_search import LS
from collections import Counter
from cluster import OPTICS_construction,Agglomerative_construction,Spectral_construction,Birch_construction,MeanShift_construction,KMeans_construction
from feasiblity import check
from travel_time import ttTao
from feasiblity import final
from clinitial import init
from readData import readmain,gettestini
from LNS_SPP import LNS
arf1,arf2,a1,a2,a3,T0,q,armax,armin,arRate,gamma,rou1,rou2,rou3=0.05,0.02,0.02,0.05,0.3,200,0.95,0.6,0.3,0.45,0.1,10,3,1
instance= ""
pickup,delivery ,num_pair,Cap = [],[],0,0
rank = []
dict = {}
inf = float(1 << 30)
depature,glo_depa = [],[]
Vehicle_dep, Vehicle_end, Profit, ini_len, Spend = 0, 0, 40, inf, 1
init_sol = []



def swap(init_sol,cur_best,num_pair,routes_pool,pre_wt):
    len_ro,cur_sol = len(init_sol),init_sol
    for i in range(1,len_ro-1):
        for j in range(i+1,len_ro-1):   # ...i-1 -> j-> i+1 ->......-> j-1 -> i -> j+1
                tmp_sol = init_sol[0:i] + init_sol[j:j+1]  +init_sol[i + 1:j] + init_sol[i:i+1] + init_sol[j+1:]
                #print(init_sol,"aaaa",tmp_sol)
                tmpans,routes_pool= check(tmp_sol,routes_pool,pre_wt)
                if tmpans > cur_best:
                    #print("_swap",tmp_sol,tmpans)
                    cur_sol = tmp_sol
                    cur_best = tmpans
    return cur_sol,cur_best,routes_pool

def relocate(init_sol, cur_best,num_pair,routes_pool,pre_wt):
    len_ro,cur_sol = len(init_sol),init_sol
    for i in range(1,len_ro-1):
        for j in range(i+1,len_ro-1):   # ...i-1 -> i+1 ->......-> j -> i -> j+1
            tmp_sol = init_sol[0:i] + init_sol[i + 1:j+1] + init_sol[i:i+1] + init_sol[j+1:]

            tmpans,routes_pool = check(tmp_sol,routes_pool,pre_wt)
            #print("aaaa", i, j, init_sol, tmp_sol, tmpans,cur_best)
            if tmpans > cur_best:
                #print("_relocate", tmp_sol,tmpans)
                cur_sol = tmp_sol
                cur_best = tmpans

        for j in range(1,i):  # ...j-1,i,j,.....->i-1->i+1->....
            tmp_sol = init_sol[0:j] + init_sol[i:i+1] + init_sol[j:i] + init_sol[i+1:]
            tmpans ,routes_pool= check(tmp_sol,routes_pool,pre_wt)
            if tmpans > cur_best:
                #print("_relocate", tmp_sol)
                cur_sol = tmp_sol
                cur_best = tmpans
    return cur_sol,cur_best,routes_pool

def Heuris(init_sol, cur_pro,num_pair,routes_pool,pre_wt):
    init_sol, cur_pro,routes_pool = swap(init_sol, cur_pro,num_pair,routes_pool,pre_wt)
    init_sol, cur_pro,routes_pool = relocate(init_sol, cur_pro,num_pair,routes_pool,pre_wt)
    init_sol,cur_pro,routes_pool = LS(init_sol,cur_pro,routes_pool,pre_wt)
    return init_sol, cur_pro,routes_pool

def regret2_Ins(new_node,pro_tmp,init_sol, pro,routes_pool,pre_wt):
    ini_sol,ini_pro = init_sol,pro
    cur_best, cur_second = -1000000000, -1000000000

    for i in range(0, len(ini_sol) - 1):
        tmp_sol = init_sol[0:i + 1] + [new_node] + init_sol[i + 1:]
        tmpans,routes_pool = check(tmp_sol,routes_pool,pre_wt)
        #print("haha", tmp_sol,tmpans)
        if tmpans >= cur_best:
            #print("cur_best",cur_best)
            cur_second = cur_best
            cur_best = tmpans
            solo = tmp_sol
        elif tmpans > cur_second or i == 1:
            cur_second = tmpans
    return cur_best - cur_second, solo,routes_pool


def main(k,instance):
    global pickup,num_pair,Cap
    global  Profit, ini_len, Spend, init_sol
    pickup,  num_pair, Cap = gettestini()
    init_sol = [0,num_pair+1]
    map, bank = {}, []
    routes_pool = []
    pre_wt = [0 for i in range(num_pair + 1)]

    for i in range(1, num_pair + 1):  # [0,1,3,5,0]  numnode = 5
        # a = input()
        # print(tmp_sol[i])
        t1, w1 = ttTao(0, i, 0, pickup[i]["load"])
        #print("num:",num_pair)
        t2, w2 = ttTao(i, num_pair + 1, t1, 0)
        pre_wt[i] = [w1 + w2, t1 + t2]
    ##########################################################################
    #init_sol =[0, 80, 156, 41, 92, 154, 27, 116, 152, 136, 62, 77, 70, 9, 25, 165, 164, 163, 162, 161, 160, 159, 38, 134, 141, 157, 98, 89, 101, 145, 2, 30, 49, 124, 53, 68, 112, 129, 51, 94, 117, 5, 131, 26, 115, 64, 55, 105, 48, 106, 128, 57, 158, 71, 69, 153, 37, 147, 125, 22, 81, 58, 150, 119, 74, 12, 31, 65, 67, 82, 90, 151, 50, 15, 138, 78, 75, 73, 42, 122, 20, 32, 140, 6, 121, 46, 139, 45, 56, 40, 148, 84, 1, 111, 34, 93, 135, 149, 110, 28, 23, 97, 120, 137, 144, 133, 7, 59, 19, 10, 14, 102, 43, 4, 118, 66, 8, 60, 113, 143, 24, 76, 18, 146, 95, 127, 88, 54, 16, 61, 87, 130, 107, 108, 47, 52, 13, 72, 63, 36, 99, 35, 86, 11, 104, 3, 96, 109, 103, 91, 123, 29, 132, 114, 44, 100, 21, 126, 17, 79, 33, 142, 85, 39, 155, 83, 166]

    #final(init_sol, instance, pre_wt)
    #a = input()
    ########################################################################################################
    
    if k%2 == 0:
        for i in range(1, num_pair + 1):
            bank.append(i)

        pro_tmp = 0
        while len(bank) != 0:
            cur_max = -1000000000
            for i in range(len(bank)):
                dif, solo,routes_pool = regret2_Ins(bank[i], pro_tmp, init_sol, num_pair,routes_pool,pre_wt)
                # print("dif:",dif,solo)
                if dif > cur_max:
                    cur_max = dif
                    cur_sol = solo
                    id = i
            if cur_max != -1000000000:
                init_sol = cur_sol
                bank.pop(id)
            # print("cur:",cur_sol)
    else:
        a = Agglomerative_construction()
        for ele in a: bank.append(int(ele))
        init_sol = [0] + bank + [num_pair + 1]


    '''
    a = input()
    init_sol = [int(x) for x in a.split(",")]

    '''
    fi_cost, routes_pool = check(init_sol, routes_pool, pre_wt)
    print("ini:", init_sol,fi_cost,routes_pool)
    #print("heu start")
    #init_sol, fi_cost, routes_pool = Heuris(init_sol, fi_cost, num_pair, routes_pool, pre_wt)
    print("LNS start")
    init_sol, fi_cost =  LNS( init_sol,fi_cost,routes_pool,instance,pre_wt)

    return fi_cost

def evaluate(arf11,T01,q1,armax1,armin1,arRate1,gamma1,rou11,rou21,rou31,instance1,a,k):
    global arf1,T0,q,armax,armin,arRate,gamma,rou1,rou2,rou3,instance
    arf1,T0,q,armax,armin,arRate,gamma,rou1,rou2,rou3,instance = arf11,T01,q1,armax1,armin1,arRate1,gamma1,rou11,rou21,rou31,instance1

    random.seed(k)
    readmain(arf1,T0,q,armax,armin,arRate,gamma,rou1,rou2,rou3,instance)
    init()
    #get_abc(3, 5, 1)
    return main(k,a)

if __name__ == "__main__":
    print("")