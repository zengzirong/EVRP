from readData import feas,seginit
from travel_time import ttTao
# coding=utf-8
import collections


pickup,num_pair ,Cap ,dep= [],0,0,[]
penalty = 10


def tandw(tmpsol,Cap,num_pair,pickup):
    #print(tmpsol,Cap)
    t0, W = ttTao(0, tmpsol[0], 0, Cap)
    #print(0, tmpsol[0], Cap)
    curload = Cap - pickup[tmpsol[0]]["load"]

    for i in range(1, len(tmpsol) ):
        #print(tmpsol[i-1]," ->  ",tmpsol[i], t0, curload)
        tmpt, tmpw = ttTao(tmpsol[i - 1], tmpsol[i], t0, Cap)
        #tmpt, tmpw = ttTao(tmpsol[i - 1], tmpsol[i], t0, curload)

        curload = curload - pickup[tmpsol[i]]["load"]

        W = W + tmpw
        t0 = tmpt + t0
        # print("W,t0 = ",W,t0)
    #print(tmpsol[-1]," ->  ",num_pair+1, t0, curload)
    #tmpt, tmpw = ttTao(tmpsol[-1], num_pair + 1, t0, 0)
    tmpt, tmpw = ttTao(tmpsol[-1], num_pair + 1, t0, Cap)

    W = W + tmpw
    t0 = t0 + tmpt
    #print("W,t0",W,t0)

    return W,t0


def split_out(tmp_sol,instance,pre_wt):
    #print("tmp:",tmp_sol)
    queue = collections.deque()
    queue.append(0)
    pickup, num_pair, Capacity, Electric = feas()
    sumq,dp,pre,detile = [0 for i in range(num_pair+2)],[[] for i in range(num_pair+2)],[0 for i in range(num_pair+2)],[[] for i in range(num_pair+2)]
    print(tmp_sol,num_pair) ####!!!!
    #print(pickup[tmp_sol[num_pair]])
    for i in range(1,num_pair+1):
        sumq[i] = sumq[i-1]+pickup[tmp_sol[i]]["load"]

    dp[0] = [0,0]
    pre[0] = -1
    detile[0] = [0,0]
    for i in range(1, num_pair+1):
        #print("i",i)
        w,t = pre_wt[tmp_sol[i]]
        dp[i] = [w+dp[i-1][0],t+dp[i-1][1]]
        pre[i] = i-1
        detile[i] = pre_wt[i]

        while(queue):
            p = queue[0]

            if(sumq[i] - sumq[p] > Capacity ):
                #print("cam", sumq[i] - sumq[p], "Cap", Capacity)
                queue.popleft()
            else:
                break
        for p in queue:
            if p+1 == i:break
            tmpw,tmpt0 = tandw(tmp_sol[p+1:i+1],sumq[i] - sumq[p],num_pair,pickup )
            #print(tmp_sol[p + 1:i + 1], ":", p,  sumq[i] - sumq[p], tmpw,tmpt0)
            tmpcost = dp[p][0] + tmpw
            tmptime = dp[p][1] + tmpt0
            #print("tmpcost,tmotime",tmpcost,tmptime)
            if tmpcost < dp[i][0]:
                #print("sti2", tmpcost, dp[i][0])
                dp[i] = [tmpcost,tmptime]
                pre[i] = p
                detile[i] = [tmpw,tmpt0]
                #print("pre",pre[i])

        queue.append(i)

    curnode = num_pair
    path,ans =[],[]
    #print("?")
    while(pre[curnode] != -1):
        lastpathnode = pre[curnode]
        #print("path",[tmp_sol[k] for k in range(lastpathnode+1,curnode+1)])
        path.append( [ [tmp_sol[k] for k in range(lastpathnode+1,curnode+1)],detile[curnode] ])
        curnode = pre[curnode]
    #print("hello")
    file = '../result/sol_'+ str(instance)+'.txt'
    with open(file, 'a') as f:
        f.write(str(tmp_sol))
        f.write('\n')
        k = 0
        for i in reversed(path):
            if i == []:break
            k += 1
            f.write(str(i))
            f.write('\n')
        f.write(str(dp[num_pair][0])+' '+str(dp[num_pair][1])+' '+str(k))
        f.write('\n')
    return dp[num_pair][1],dp[num_pair][0]
def split_out_ini(tmp_sol,instance,pre_wt):
    #print("tmp:",tmp_sol)
    queue = collections.deque()
    queue.append(0)
    pickup, num_pair, Capacity, Electric = feas()
    sumq,dp,pre,detile = [0 for i in range(num_pair+2)],[[] for i in range(num_pair+2)],[0 for i in range(num_pair+2)],[[] for i in range(num_pair+2)]
    #print(tmp_sol,num_pair)
    #print(pickup[tmp_sol[num_pair]])
    for i in range(1,num_pair+1):
        sumq[i] = sumq[i-1]+pickup[tmp_sol[i]]["load"]

    dp[0] = [0,0]
    pre[0] = -1
    detile[0] = [0,0]
    for i in range(1, num_pair+1):
        #print("i",i)
        w,t = pre_wt[tmp_sol[i]]
        dp[i] = [w+dp[i-1][0],t+dp[i-1][1]]
        pre[i] = i-1
        detile[i] = pre_wt[i]

        while(queue):
            p = queue[0]

            if(sumq[i] - sumq[p] > Capacity ):
                #print("cam", sumq[i] - sumq[p], "Cap", Capacity)
                queue.popleft()
            else:
                break
        for p in queue:
            if p+1 == i:break
            tmpw,tmpt0 = tandw(tmp_sol[p+1:i+1],sumq[i] - sumq[p],num_pair,pickup )
            #print(tmp_sol[p + 1:i + 1], ":", p,  sumq[i] - sumq[p], tmpw,tmpt0)
            tmpcost = dp[p][0] + tmpw
            tmptime = dp[p][1] + tmpt0
            #print("tmpcost,tmotime",tmpcost,tmptime)
            if tmpcost < dp[i][0]:
                #print("sti2", tmpcost, dp[i][0])
                dp[i] = [tmpcost,tmptime]
                pre[i] = p
                detile[i] = [tmpw,tmpt0]
                #print("pre",pre[i])

        queue.append(i)

    curnode = num_pair
    path,ans =[],[]
    #print("?")
    while(pre[curnode] != -1):
        lastpathnode = pre[curnode]
        #print("path",[tmp_sol[k] for k in range(lastpathnode+1,curnode+1)])
        path.append( [ [tmp_sol[k] for k in range(lastpathnode+1,curnode+1)],detile[curnode] ])
        curnode = pre[curnode]
    #print("hello")
    file = '../result/init_sol_'+ str(instance)+'.txt'
    with open(file, 'a') as f:
        f.write(str(tmp_sol))
        f.write('\n')
        k = 0
        for i in reversed(path):
            if i == []:break
            k += 1
            f.write(str(i))
            f.write('\n')
        f.write(str(dp[num_pair][0])+' '+str(dp[num_pair][1])+' '+str(k))
        f.write('\n')
    return dp[num_pair][1],dp[num_pair][0]
def split(tmp_sol,route_pool,pre_wt):
    #print("tmp",tmp_sol,route_pool)
    #a = input()
    pickup, num_pair, Capacity, Electric = feas()
    if num_pair == len(tmp_sol)-2:
        file = '../result/cnt_' + str(num_pair) + '.txt'
        with open(file, 'a') as f:
            f.write(str(1))
            f.write('\n')
    queue = collections.deque()
    queue.append(0)
    pickup, num_pair, Capacity, Electric = feas()
    num_node = len(tmp_sol)


    sumq,dp,pre,detile = [0 for i in range(num_node)],[[] for i in range(num_node)],[0 for i in range(num_node)],[[] for i in range(num_node)]
    for i in range(1,num_node-1):
        sumq[i] = sumq[i-1]+pickup[tmp_sol[i]]["load"]


    dp[0] = [0,0]
    pre[0] = -1
    detile[0] = [0,0]
    #print(tmp_sol)
    for i in range(1, num_node-1):  # [0,1,3,5,0]  numnode = 5
        w, t = pre_wt[tmp_sol[i]]
        dp[i] = [w + dp[i - 1][0], t + dp[i - 1][1]]
        pre[i] = i-1
        detile[i] = [w,t]

        while(queue):
            p = queue[0]

            if(sumq[i] - sumq[p] > Capacity ):
                #print("cam", sumq[i] - sumq[p], "Cap", Capacity)
                queue.popleft()
            else:
                break
        for p in queue:
            if p + 1 == i : break
            tmpw,tmpt0 = tandw(tmp_sol[p+1:i+1],sumq[i] - sumq[p],num_pair,pickup )
            #print(tmp_sol[p + 1:i + 1], ":", p,  sumq[i] - sumq[p], tmpw,tmpt0)
            tmpcost = dp[p][0] + tmpw
            tmptime = dp[p][1] + tmpt0
            #print("tmpcost,tmotime",tmpcost,tmptime)
            if tmpcost < dp[i][0]:
                #print("sti2", tmpcost, dp[i][0])
                dp[i] = [tmpcost,tmptime]
                pre[i] = p
                detile[i] = [tmpw,tmpt0]
                #print("pre",pre[i])

        queue.append(i)
    #print("befo",route_pool)
    curnode = num_node-2
    list_path = []
    flag_path = []
    while(pre[curnode] != -1):
        lastpathnode = pre[curnode]
        path = [ [tmp_sol[k] for k in range(lastpathnode+1,curnode+1)],detile[curnode] ]
        flag_path.append(0)
        list_path.append(path)
        curnode = pre[curnode]

    tmp_pool = []
    for rr in route_pool:
        flag = 0
        ind = 0
        for path in list_path:

            if set(rr[0]).issubset(set(path[0])) and rr[1][0] >= path[1][0]:  #被任何一个 path 所 dominate,一摸一样算在这里
                flag =1
            elif set(path[0]).issubset(set(rr[0])) and rr[1][0] <= path[1][0]: #path 被 donimate
                flag_path[ind] =1

            ind += 1
        if flag == 0:
            tmp_pool.append(rr)


    for i in range(0, len(list_path)):
        if flag_path[i] == 0:
            tmp_pool.append(list_path[i])

    return dp[num_node - 2][0], tmp_pool


def check(tmp_sol,routes_pool,pre_wt):
    #print(tmp_sol)
    W,routes_pool= split(tmp_sol,routes_pool,pre_wt)

    #print("t0,tmot", t0, W)
    #if len(tmp_sol) == num_pair+2:
        #a = input()
    return -W,routes_pool
def final(tmp_sol,instance,pre_wt):
    t0,W = split_out(tmp_sol,instance,pre_wt)
    return t0,-W

def final_ini(tmp_sol,instance,pre_wt):
    t0,W = split_out_ini(tmp_sol,instance,pre_wt)
    return t0,-W


if __name__=='__main__':
    print("")