from readData import getls
from feasiblity import check
import random
pickup = []
num_pair = 0

def operator1(init_sol,cur_best,routes_pool,pre_wt):  #swap
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
                    return cur_sol, cur_best, routes_pool
    return cur_sol,cur_best,routes_pool

def operator2(init_sol,cur_best,routes_pool,pre_wt):  #relocate
    global pickup, num_pair
    len_ro, cur_sol = len(init_sol), init_sol
    for i in range(1, len_ro - 1):
        for j in range(i + 1, len_ro - 1):  # ...i-1 -> i+1 ->......-> j -> i -> j+1
            tmp_sol = init_sol[0:i] + init_sol[i + 1:j + 1] + init_sol[i:i + 1] + init_sol[j + 1:]

            tmpans,routes_pool = check(tmp_sol,routes_pool,pre_wt)
            # print("aaaa", i, j, init_sol, tmp_sol, tmpans,cur_best)
            if tmpans > cur_best:
                #print("_relocate", tmp_sol, tmpans)
                cur_sol = tmp_sol
                cur_best = tmpans
                return cur_sol, cur_best, routes_pool
        for j in range(1, i):  # ...j-1,i,j,.....->i-1->i+1->....
            tmp_sol = init_sol[0:j] + init_sol[i:i + 1] + init_sol[j:i] + init_sol[i + 1:]
            tmpans,routes_pool = check(tmp_sol,routes_pool,pre_wt)
            if tmpans > cur_best:
                #print("_relocate", tmp_sol)
                cur_sol = tmp_sol
                cur_best = tmpans
                return cur_sol, cur_best, routes_pool
    return cur_sol,cur_best,routes_pool



def operator3(init_sol,cur_best,routes_pool,pre_wt):  #nmswap

    len_ro,cur_sol = len(init_sol),init_sol
    n = random.randint(1, len_ro-4)
    m = random.randint (1,len_ro-n-1)

    for i in range(1,len_ro-m-n):
        for j in range(i+n,len_ro-m):
                tmp_sol = init_sol[0:i] + init_sol[j:j+m]  +init_sol[i + n:j] + init_sol[i:i+n] + init_sol[j+m:]
                #print(init_sol,"aaaa",tmp_sol)
                tmpans,routes_pool= check(tmp_sol,routes_pool,pre_wt)
                if tmpans > cur_best:
                    #print("_nmswap",tmp_sol,tmpans)
                    cur_sol = tmp_sol
                    cur_best = tmpans
                    return cur_sol, cur_best, routes_pool
    return cur_sol,cur_best,routes_pool


def operator4(init_sol,cur_best,routes_pool,pre_wt):  #nmRex

    len_ro,cur_sol = len(init_sol),init_sol
    n = random.randint(1, len_ro-4)
    m = random.randint (1,len_ro-n-1)

    for i in range(1,len_ro-m-n):
        for j in range(i+n,len_ro-m):
                tmp_sol = init_sol[0:i] + init_sol[j+m-1:j-1:-1]  +init_sol[i + n:j] + init_sol[i:i+n] + init_sol[j+m:]
                #print(init_sol,"aaaa",tmp_sol)
                tmpans,routes_pool= check(tmp_sol,routes_pool,pre_wt)
                if tmpans > cur_best:
                    #print("_nmswap",tmp_sol,tmpans)
                    cur_sol = tmp_sol
                    cur_best = tmpans
                    return cur_sol, cur_best, routes_pool
    return cur_sol,cur_best,routes_pool

def operator5(init_sol,cur_best,routes_pool,pre_wt):  #TWOPT

    len_ro,cur_sol = len(init_sol),init_sol
    n = random.randint(1, len_ro-2)
    m = random.randint (n,len_ro-1)

    for i in range(1,len_ro-m-n):
        for j in range(i+n,len_ro-m):
                tmp_sol = init_sol[0:i+1] + init_sol[j:i:-1]  +init_sol[j+1:]
                #print(init_sol,"aaaa",tmp_sol)
                tmpans,routes_pool= check(tmp_sol,routes_pool,pre_wt)
                if tmpans > cur_best:
                    #print("_nmswap",tmp_sol,tmpans)
                    cur_sol = tmp_sol
                    cur_best = tmpans
                    return cur_sol, cur_best, routes_pool
    return cur_sol,cur_best,routes_pool

def operator0(init_sol,cur_best,routes_pool,pre_wt):  #nmRex*

    len_ro,cur_sol = len(init_sol),init_sol
    n = random.randint(1, len_ro-4)
    m = random.randint (1,len_ro-n-1)

    for i in range(1,len_ro-m-n):
        for j in range(i+n,len_ro-m):
                tmp_sol = init_sol[0:i] + init_sol[j+m-1:j-1:-1]  +init_sol[i + n:j] + init_sol[i+n-1:i-1:-1] + init_sol[j+m:]
                #print(init_sol,"aaaa",tmp_sol)
                tmpans,routes_pool= check(tmp_sol,routes_pool,pre_wt)
                if tmpans > cur_best:
                    #print("_nmswap",tmp_sol,tmpans)
                    cur_sol = tmp_sol
                    cur_best = tmpans
                    return cur_sol, cur_best, routes_pool
    return cur_sol,cur_best,routes_pool

def LS(S,W_S,routes_pool,pre_wt):
    print("ls start: ",W_S)
    global pickup,num_pair
    pickup,num_pair = getls()

    e,c = 0,0
    num_opt = 5
    num = 0
    while 1:
        num += 1
        S_new, W_new,routes_pool = eval('operator'+str(c))(S,W_S,routes_pool,pre_wt)
        if W_new > W_S:
            #print('operator'+str(c))
            S = S_new[:]
            W_S= W_new
            e = c
        c = (c+1)%num_opt
        if c == e:
            break
    #print(num)
    print("ls end: ", W_S)
    return S,W_S,routes_pool


#init_sol = [0, 10, 4, 9, 6, 1, 7, 8, 3, 2, 5, 11]
#n,m = 3,2
#i,j = 3,7
#print(init_sol[0:i] + init_sol[j:j+1]  +init_sol[i + 1:j] + init_sol[i:i+1] + init_sol[j+1:])
#print(S, LS(S))
# ck, pro_Snew, dur_Snew = check(S)
#two_insert(S,num_pair,pro_Snew,dur_Snew)
if __name__ == "__main__":
    print("")