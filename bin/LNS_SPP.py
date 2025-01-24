from readData import getalns, getread
from clinitial import getcl
from feasiblity import check,final,final_ini
from local_search import LS
import heapq
import time
from SCP import solve_scp_model
import math
import random




dict_removal = {0: "Random_Rev", 1: "dis_Rev", 2: "CL_Rev(shaw)", 3: "Worst_W_Rev", 4: "Worst_W_Rev", 5: "large_cap_Rev"}





# check,tmpsol可能false，但仍返回已经removal过了的sol。
def Random_Rev(S, num_removel, num_pair):
    global T0, q, armax, armin, arRate, gamma, rou1, rou2, rou3
    global CL
    global pickup,Cap, speedMatrix, dis, speed
    #global depature, num_destroy, num_repair, w_reinsert, pr_reinsert, w_removal, pr_removal, pi_removal, theta_removal, cp_removal, cp_reinsert, pi_reinsert, theta_reinsert, Pro, Spend, MaxI, sco_i

    M, k, tmpsol = [], [], []
    for i in range(1, len(S) - 1):
        if S[i] <= num_pair:
            M.append(S[i])
    slice = random.sample(M, num_removel)  # random delete num_removal pickup node
    for i in range(len(slice)):
        k.append(slice[i])
    for i in range(len(S)):
        if S[i] in k:
            continue
        tmpsol.append(S[i])
    # #print("random   tmpsol  = ",tmpsol,'\n',S,k)
    return tmpsol


# check, greddy，有没有这对点的duration差排序。
def Load_Rev(S, num_removal, num_pair, dur_S):
    global T0, q, armax, armin, arRate, gamma, rou1, rou2, rou3
    global pickup, delivery, Cap, speedMatrix, dis, speed
    #global depature, num_destroy, num_repair, w_reinsert, pr_reinsert, w_removal, pr_removal, pi_removal, theta_removal, cp_removal, cp_reinsert, pi_reinsert, theta_reinsert, Pro, Spend, MaxI, sco_i

    p = 20  # random parameter ???????
    Q, k = [], []
    cost = [-100000000000 for i in range(num_pair + 1)]

    for i in range(1, len(S) - 1):
        cost[S[i]] = (i+1)*pickup[S[i]]["load"]
        Q.append([-cost[S[i]], S[i]])

    Q.sort()
    i = 0
    while num_removal > 0 and len(Q) != 0:
        k.append(Q[i][1])
        num_removal -= 1
        i += 1
    tmpsol = []
    for i in range(len(S)):
        if S[i] in k:
            continue
        tmpsol.append(S[i])
    # #print("dur   tmpsol  = ", tmpsol, '\n',S, k)
    # print("tmpsol : ",tmpsol,k)
    return tmpsol

# WR
def Worst_W_Rev(S, num_removal, num_pair, pro_S,routes_pool,pre_wt):
    global T0, q, armax, armin, arRate, gamma, rou1, rou2, rou3
    global pickup,Cap, speedMatrix, dis, speed
    #global num_destroy, num_repair, w_reinsert, pr_reinsert, w_removal, pr_removal, pi_removal, theta_removal, cp_removal, cp_reinsert, pi_reinsert, theta_reinsert, Pro, Spend, MaxI, sco_i

    Q, k = [], []
    cost = [-100000000000 for i in range(num_pair + 1)]
    for i in range(1, len(S) - 1):
        tmpsol = S[:i] + S[i + 1:]
        pro,routes_pool = check(tmpsol,routes_pool,pre_wt)
        cost[S[i]] = pro- pro_S
        Q.append([cost[S[i]], S[i]])

    Q.sort(reverse=True)
    #print(Q)
    i = 0
    while num_removal > 0 and len(Q) != 0:
        k.append(Q[i][1])
        num_removal -= 1
        i += 1
    tmpsol = []
    for i in range(len(S)):
        if S[i] in k:
            continue
        tmpsol.append(S[i])
    return tmpsol,routes_pool


# LRP
def Least_pro_Rev(S, num_removal, num_pair,routes_pool,pre_wt):
    global T0, q, armax, armin, arRate, gamma, rou1, rou2, rou3
    global pickup, delivery, Cap, speedMatrix, dis, speed
    #global depature, num_destroy, num_repair, w_reinsert, pr_reinsert, w_removal, pr_removal, pi_removal, theta_removal, cp_removal, cp_reinsert, pi_reinsert, theta_reinsert, Pro, Spend, MaxI, sco_i

    Q, k = [], []
    cost = [-100000000000 for i in range(num_pair + 1)]
    for i in range(1, len(S) - 1):
        cost[S[i]],routes_pool = check(S[:i]+S[i+1:],routes_pool,pre_wt)
        Q.append([cost[S[i]], S[i]])

    Q.sort()
    i = 0
    while num_removal > 0 and len(Q) != 0:
        k.append(Q[i][1])
        num_removal -= 1
        i += 1
    tmpsol = []
    for i in range(len(S)):
        if S[i] in k:
            continue
        tmpsol.append(S[i])
    return tmpsol,routes_pool



# check, greddy，有没有这对点的差distance和排序。
def dis_Rev(S, num_removal, num_pair):
    global T0, q, armax, armin, arRate, gamma, rou1, rou2, rou3
    global pickup, Cap, speedMatrix, dis, speed

    cost = [-100000000000 for _ in range(num_pair + 1)]
    Q, k = [], []

    for i in range(1, len(S) - 1):
        cost[S[i]] = dis[S[i]][S[i + 1]]+ dis[S[i-1]][S[i]]
        Q.append([-cost[S[i]], S[i]])

    Q.sort()
    i = 0
    while num_removal > 0 and len(Q) != 0:
        k.append(Q[i][1])
        num_removal -= 1
        i += 1
        #print("Qpop = ",r)
    tmpsol = []
    for i in range(len(S)):
        if S[i] in k:
            continue
        tmpsol.append(S[i])
    return tmpsol


def shaw_Rev(S, num_removal, num_pair):
    global T0, q, armax, armin, arRate, gamma, rou1, rou2, rou3
    global CL
    global pickup, Cap, speedMatrix, dis, speed
    #global depature, num_destroy, num_repair, w_reinsert, pr_reinsert, w_removal, pr_removal, pi_removal, theta_removal, cp_removal, cp_reinsert, pi_reinsert, theta_reinsert, Pro, Spend, MaxI, sco_i

    Q, rev, vis = [], [], [0 for _ in range(num_pair + 1)]
    num = 0
    rn = random.sample(S[1:-1], 1)
    # print(rn,S)

    po = rn[0]
    heapq.heappush(Q, (0, po))
    # print("now:",S)
    while len(Q) != 0:
        # print("Q,S",Q,'\n',S)
        tmp = heapq.heappop(Q)
        if vis[tmp[1]] == 1: continue
        vis[tmp[1]] == 1
        rev.append(tmp[1])
        num += 1
        # print("S:",S)
        if num == num_removal: break
        for i in range(1, len(S)-1):
            if S[i] not in rev:
                heapq.heappush(Q, (CL[tmp[1]][S[i]], S[i]))

    tmpsol = []
    # print("S = ",S,"\nrev = ",rev)
    for i in range(len(S)):
        if S[i] in rev:
            continue
        tmpsol.append(S[i])
    # print("tmosol????",tmpsol,S)
    # print(S)
    return tmpsol



dict_reinsert = {0: "Random", 1: "Greedy", 2: "regret-2", 3:  "reget_3"}


# 随机插入位置，失败返回原始
def Random_Ins(tmpsol, bank,routes_pool,pre_wt):
    global T0, q, armax, armin, arRate, gamma, rou1, rou2, rou3
    global pickup, delivery, Cap, speedMatrix, dis, speed
    #global depature, num_destroy, num_repair, w_reinsert, pr_reinsert, w_removal, pr_removal, pi_removal, theta_removal, cp_removal, cp_reinsert, pi_reinsert, theta_reinsert, Pro, Spend, MaxI, sco_i

    pos = random.randint(1, len(tmpsol) - 1)  # ,,,pos
    # #print("random insert position delivery: ", pos + 1, len(tmpsol) - 1)
    for i in range(len(bank)):
        tmpsol = tmpsol[:pos] + [bank[i]] + tmpsol[pos:]

    # print("newsol:",newsol)
    pro,routes_pool= check(tmpsol,routes_pool,pre_wt)
    return pro,tmpsol,routes_pool


# 插入最好的位置，失败返回原始
def Greedy_Ins(tmpsol, num_pair, ins_id,routes_pool,pre_wt):
    cur_best = -10000000000
    global pickup
    curpi, curde = ins_id, ins_id + num_pair
    # print("curpi,curde",curpi,curde)
    init_sol, solo = tmpsol, tmpsol

    for i in range(0, len(tmpsol) - 1):
        # insert pi and de as neighbor
        tmp_sol = init_sol[0:i + 1] + [curpi] +  init_sol[i + 1:]
        tmpans,routes_pool= check(tmp_sol,routes_pool,pre_wt)

        # print("tmpsol is : ", tmp_sol, tmpans)
        if  tmpans > cur_best:
            cur_best = tmpans
            cur_sol = tmp_sol

    return cur_sol,routes_pool


# 找到第一好和第二好的位置，做差，返回差值到主函数，主函数排序，找到差最大的num_removal个
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
        elif tmpans >  cur_second or i == 1:
            cur_second = tmpans

    return cur_best - cur_second, solo,routes_pool

def regret3_Ins( W_tmp, tmpsol, num_pair, ins_id,routes_pool,pre_wt):
    global T0, q, armax, armin, arRate, gamma, rou1, rou2, rou3
    global CL, CL1, CL2
    global pickup, delivery, Cap, speedMatrix, dis, speed
    #global depature, num_destroy, num_repair, w_reinsert, pr_reinsert, w_removal, pr_removal, pi_removal, theta_removal, cp_removal, cp_reinsert, pi_reinsert, theta_reinsert, Pro, Spend, MaxI, sco_i

    cur_best, cur_second, cur_third = -100000000000, -100000000000, -100000000000
    curpi, curde = ins_id, ins_id + num_pair
    init_sol, solo = tmpsol, tmpsol

    for i in range(0, len(tmpsol) - 1):
        # insert pi and de as neighbor
        tmp_sol = init_sol[0:i + 1] + [curpi]  + init_sol[i + 1:]
        tmpans,routes_pool= check(tmp_sol,routes_pool,pre_wt)
        if tmpans >= cur_best:
            cur_third = cur_second
            cur_second = cur_best
            cur_best = tmpans
            solo = tmp_sol
        elif tmpans >= cur_second:
            cur_third = cur_second
            cur_second = tmpans
        elif tmpans > cur_third:
            cur_third = tmpans

    if cur_best == -100000000000:
        return -100000000000, init_sol
    return cur_best - cur_second + cur_best - cur_third, solo,routes_pool


# roulette_wheel select reinsert operator reg-k(1,2)+random





def Distroy_and_Repair(SS_cur, num_removal, num_pair, pro_S, Removal_id, Reinsert_id,routes_pool,pre_wt):
    global T0, q, armax, armin, arRate, gamma, rou1, rou2, rou3
    global CL
    global pickup, Cap, speedMatrix, dis, speed
    #global depature, num_destroy, num_repair, w_reinsert, pr_reinsert, w_removal, pr_removal, pi_removal, theta_removal, cp_removal, cp_reinsert, pi_reinsert, theta_reinsert, Pro, Spend, MaxI, sco_i

    if Removal_id ==2:
        tmpsol = Random_Rev(SS_cur, num_removal, num_pair)
    elif Removal_id == 4:
        tmpsol = dis_Rev(SS_cur, num_removal, num_pair)
    elif Removal_id == 1:
        tmpsol = shaw_Rev(SS_cur, num_removal, num_pair)
    elif Removal_id == 3:
        tmpsol,routes_pool = Worst_W_Rev(SS_cur, num_removal, num_pair, pro_S,routes_pool,pre_wt)
    elif Removal_id == 0:
        tmpsol = Load_Rev(SS_cur, num_removal, num_pair, pro_S)
    #print("id",Removal_id, Reinsert_id)
    #print("ramoval,", tmpsol)
    M, bank = [], []
    for i in range(1, len(tmpsol) - 1):
        M.append(tmpsol[i])
    for i in range(1, num_pair + 1):
        if i not in M:
            bank.append(i)
    # random insert
    W_tmp = -100000000000
    if Reinsert_id == 1:
        proo, solo =  W_tmp, tmpsol
        random.shuffle(bank)
        proo,solo,routes_pool = Random_Ins(solo, bank,routes_pool,pre_wt)
        tmpsol, W_tmp =  solo, proo

    # greedy insert
    elif Reinsert_id == 0:
        proo, solo = W_tmp, tmpsol
        random.shuffle(bank)
        for i in range(len(bank)):
            solo,routes_pool= Greedy_Ins(solo, num_pair, bank[i],routes_pool,pre_wt)
        tmpsol, W_tmp = solo, proo

    # regret_2，加入num_removal个
    elif Reinsert_id == 2:  # reget_2
        W_tmp,routes_pool = check(tmpsol,routes_pool,pre_wt)
        while len(bank) != 0:
            cur_max = -100000000000
            #print("ccc",bank)
            for i in range(len(bank)):
                dif, solo,routes_pool = regret2_Ins(bank[i], W_tmp, tmpsol,num_pair,routes_pool,pre_wt)
                #print("dif:",dif,solo)
                if dif > cur_max:
                    cur_max = dif
                    cur_sol = solo
                    id = i
            if cur_max != -100000000000:
                W_tmp,routes_pool = check(cur_sol,routes_pool,pre_wt)
                tmpsol = cur_sol
                bank.pop(id)

    # reget_3
    elif Reinsert_id == 3:
        W_tmp,routes_pool = check(tmpsol,routes_pool,pre_wt)
        while len(bank) != 0:
            cur_max = -100000000000
            for i in range(len(bank)):
                dif, solo ,routes_pool= regret3_Ins( W_tmp, tmpsol, num_pair, bank[i],routes_pool,pre_wt)
                if dif > cur_max:
                    cur_max = dif
                    cur_sol = solo
                    id = i
            if cur_max != -100000000000:
                W_tmp,routes_pool = check(cur_sol,routes_pool,pre_wt)
                tmpsol = cur_sol
                bank.pop(id)

    #print("after insert: ",tmpsol,W_tmp)
    return tmpsol,W_tmp,routes_pool


def LNS(SS_cur, pro_S,routes_pool,instance,pre_wt):  # init_sol,num_pair,cur_best,ini_len
    #print("??")
    t, w = final_ini(SS_cur,instance,pre_wt)
    #return SS_cur,w
    #print("gujiguji",SS_cur, t, w )
    start = time.process_time()
    global T0, q, armax, armin, arRate, gamma, rou1, rou2, rou3
    global CL
    global pickup, delivery, Cap, speedMatrix, dis, speed, num_pair
    #global depature, num_destroy, num_repair, w_reinsert, pr_reinsert, w_removal, pr_removal, pi_removal, theta_removal, cp_removal, cp_reinsert, pi_reinsert, theta_reinsert, Pro, Spend, MaxI, sco_i
    T0, q, armax, armin, arRate, gamma, rou1, rou2, rou3 = getalns()
    CL= getcl()
    pickup,  Cap, speedMatrix, dis, speed, num_pair = getread()
    S_best, T, pro_Sbest = SS_cur, T0, pro_S
    NonImp, Terminal, cnt = 0, 1, 0

    num_destroy, num_repair = 5,4

    MaxI = num_pair*10 #0
    # 100, ALNS iterator,reinsert最多的迭代次数
    sco_i = [0 for i in range(7)]

    while Terminal < MaxI:
        #print("start ite")
        num_removal =  int(min(armax, armin + arRate * NonImp) * num_pair)

        #print ("num_des",num_destroy)
        Removal_id =random.randint(0, num_destroy-1)
        #print("id",Removal_id)

        Reinsert_id = random.randint(0,num_repair-1)
       # print("repa",Reinsert_id)


        S_new,pro_Snew,routes_pool = Distroy_and_Repair(SS_cur, num_removal, num_pair,pro_S, Removal_id,Reinsert_id,routes_pool,pre_wt)  # (S,num_removal,Removal_id,Reinsert_id)
        if pro_Snew/pro_Sbest<2: S_new, pro_Snew,routes_pool= LS(S_new,pro_Snew,routes_pool,pre_wt)
        T = T * q


        diff = pro_Snew - pro_S  #better than current: -99 +100  =  1

        if diff > 0:
            SS_cur = S_new
            #print("Yes, better than now",pro_S,'\n', S_new)
            pro_S = pro_Snew
        else:
            r = random.random()
            if T >= 0.01  and math.exp((diff) /(10000*T)) >= r:
                SS_cur = S_new
                #print("Yes,another chance",pro_S,'\n', S_new)
                pro_S =  pro_Snew


        if len(routes_pool)*(num_pair) >=30000:
            p,s = solve_scp_model(routes_pool, num_pair)
            routes_pool = []
            S_new,pro_Snew = s,-p

        if pro_Snew > pro_Sbest:  #-99  > -100
            NonImp = 0
            #print("LNS part:",S_new)
            t, w = final(S_new,instance,pre_wt)
            print("LNS found ", S_new,'\n',-pro_Snew,t,Terminal)
            #print("t0 = ", t)
            #a = input()
            S_best = S_new
            SS_cur = S_new
        else:
            NonImp += 1

        Terminal += 1
        end = time.process_time()
        print("start,end",start, end)
        #print("end iter")
    #print("@@Best one ", S_new, '\n', pro_Snew)
    return S_best, pro_Sbest


if __name__ == "__main__":
    print("")
