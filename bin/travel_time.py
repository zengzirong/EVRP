from  readData import gettraveltime
from readData import getW_a123
import math
speedMatrix,dis ,speed,t_table = [],[],[],[]

def get_work(v_bar,t_dur,a,load):
    #Pdt = t_dur*v_bar*(479.1+math.fabs(a)*(1507))
    #Pdt = t_dur * v_bar * (479.1 + math.fabs(a) * (1507+load))
    
    
    return Pdt

def ttTao(i,j,t0,load):
    #print(i,j,t0)
    global speedMatrix,dis ,speed,t_table
    speedMatrix, dis, speed,t_table = gettraveltime()
    global a1, a2, a3, mu, vehm
    a1, a2, a3, mu, vehm = getW_a123()

    W = 0
    t = t0
    #print("i,j",i,j)
    c = speedMatrix[i][j]
    d = dis[i][j]
    timezone = -1
    #print(i, "->", j, t0,d,c)

    for kk in range(len(t_table)-1):
        if t >= t_table[kk] and t < t_table[kk + 1]:
            timezone = kk
            break
    #print("tmpezone = ",t,t_table,timezone,speed[c])
    if timezone == -1:

        return 10000000,1000000000
    if timezone == 0 :
        v0_cur = speed[c][0]["v0"]
        a_cur = speed[c][1]["a"]
        #print("a_cur:",a_cur)
        v = v0_cur+a_cur*t
        t_remain = speed[c][1]["start"]-t
        S_fwr = v*t_remain + 0.5*a_cur*(t_remain**2)
        #print("remain:",t_remain,load,( v+  v+a_cur*t_remain ) / 2,a_cur)
        tmp_W = get_work(( v+  v+a_cur*t_remain ) / 2, t_remain, a_cur, load)

    elif timezone%2 == 1: #platform
        v = speed[c][int((timezone+1)//2)]["speed"]
        a_cur = 0
        S_fwr = v*(speed[c][int(timezone//2+1)]["end"]-t)
        tmp_W = get_work( v, speed[c][int(timezone//2+1)]["end"]-t,0, load )
        #4Aif j == 5: print(tmp_W,S_fwr,d)

    else:
        past_time = t-speed[c][int(timezone//2)]["end"]
        v0_cur = speed[c][int(timezone//2)]["speed"]
        a_cur = speed[c][int(timezone//2+1)]["a"]
        v = v0_cur+a_cur*past_time
        t_remain = speed[c][int(timezone//2+1)]["start"]-t
        S_fwr = v*t_remain + 0.5*a_cur*(t_remain**2)
        tmp_W = get_work((v+speed[c][int(timezone//2+1)]["speed"])/2,t_remain,a_cur,load)

    #print(i,"->",j,"d",S_fwr,d,tmp_W)
    while d > S_fwr:
        d = d - S_fwr
        t = t_table[timezone + 1]
        timezone += 1
        W = W+tmp_W
        #print("W = ",W)
        if timezone+1 == len(t_table):
            #print(i, "->", j, t0, d, c)
            return 10000000, 1000000000
        #print(t_table,timezone+1)
        dur = t_table[timezone+1]-t
        #print("time",timezone,t_table[timezone+1],t)
        if timezone%2 == 1: #platform
            v = speed[c][int((timezone+1)//2)]["speed"] #//???
            S_fwr = v*dur
            #print("1:",v,dur,0,load)
            tmp_W = get_work(v,dur,0,load)
        else:
            #print("time",timezone,t_table,speed[c])
            v0_cur = speed[c][int((timezone)//2)]['speed']
            a_cur = speed[c][int(timezone//2+1)]["a"]
            S_fwr = v0_cur*dur + 0.5*a_cur*(dur**2)
            vbar =(v0_cur+ speed[c][int(timezone//2+1)]['speed'])/2
            #print("2:",vbar,dur,a_cur,load)

            tmp_W = get_work(vbar,dur,a_cur,load)
            #if j == 5: print(tmp_W, S_fwr, d)

    #if j == 5: print(W, timezone,d)
    if timezone == 0:
        v0_cur = speed[c][0]["v0"]
        a_cur = speed[c][1]["a"]
        v_ini = v0_cur + a_cur * t
        t_dur =  (-v_ini + math.sqrt(v_ini ** 2 + 2 * a_cur * d)) / a_cur
        t = t + t_dur

        v_after = v_ini + a_cur*t_dur
        #print("3:",(v_ini+v_after)/2, t_dur, a_cur, load)
        W = W + get_work((v_ini+v_after)/2, t_dur, a_cur, load)
        #if i == 0 and j == 2 and t0 == 0:
         #   print("??",a_cur,t_dur,v_ini, v_after)
    elif timezone%2 == 1: #platform
        v = speed[c][int((timezone+1)//2)]["speed"]
        t = t + d/v
        #print("4:", v, t-t_remain ,0, load )
        W = W+get_work( v, d/v ,0, load )#(a1*v)*()
    else:
        past_time = t - speed[c][int(timezone // 2)]["end"]
        v0_cur = speed[c][int(timezone // 2)]["speed"]
        a_cur = speed[c][int(timezone // 2 + 1)]["a"]
        v_ini = v0_cur + a_cur * past_time
        t_dur =  ( -v_ini+ math.sqrt(v_ini**2+2*a_cur*d) ) / a_cur
        #print("t,t_dur",t,t_dur)
        t = t+ t_dur
        v_after = math.sqrt(v_ini**2 + 2*a_cur*d)

        #if j == 5: print(W, "v0 = ",v_ini, "a = ",a_cur,"t = ",t_dur,"vend = ",v_after,load,v_ini+a_cur*t_dur)
        W =W+get_work((v_after+v0_cur)/2,t_dur,a_cur,load)
        #if j == 5: print(W, t_dur)
    #print(">>>>>>>>W,t = ",W,t-t0)
    #print(i,"->",j,"t0 = ",t0,"trvt:",t-t0)
    return t - t0,W
    #return round(t - t0,3)

def tt_W(i,j,t0,load):
    #print(i,j,t0)
    global speedMatrix,dis ,speed,t_table
    speedMatrix, dis, speed,t_table = gettraveltime()
    global a1, a2, a3, mu, vehm
    a1, a2, a3, mu, vehm = getW_a123()

    W = 0
    t = t0
    c = speedMatrix[i][j]
    d = dis[i][j]
    timezone = -1
    #print(i, "->", j, t0,d,c)

    for kk in range(len(t_table)-1):
        if t >= t_table[kk] and t < t_table[kk + 1]:
            timezone = kk
            break
    #print("tmpezone = ",t,t_table,timezone,speed[c])
    if timezone == -1:

        return 10000000,1000000000
    if timezone == 0 :
        v0_cur = speed[c][0]["v0"]
        a_cur = speed[c][1]["a"]
        #print("a_cur:",a_cur)
        v = v0_cur+a_cur*t
        t_remain = speed[c][1]["start"]-t
        S_fwr = v*t_remain + 0.5*a_cur*(t_remain**2)
        #print("remain:",t_remain,load,( v+  v+a_cur*t_remain ) / 2,a_cur)
        tmp_W = get_work(( v+  v+a_cur*t_remain ) / 2, t_remain, a_cur, load)

    elif timezone%2 == 1: #platform
        v = speed[c][int((timezone+1)//2)]["speed"]
        a_cur = 0
        S_fwr = v*(speed[c][int(timezone//2+1)]["end"]-t)
        tmp_W = get_work( v, speed[c][int(timezone//2+1)]["end"]-t,0, load )
        #4Aif j == 5: print(tmp_W,S_fwr,d)

    else:
        past_time = t-speed[c][int(timezone//2)]["end"]
        v0_cur = speed[c][int(timezone//2)]["speed"]
        a_cur = speed[c][int(timezone//2+1)]["a"]
        v = v0_cur+a_cur*past_time
        t_remain = speed[c][int(timezone//2+1)]["start"]-t
        S_fwr = v*t_remain + 0.5*a_cur*(t_remain**2)
        tmp_W = get_work((v+speed[c][int(timezone//2+1)]["speed"])/2,t_remain,a_cur,load)

    #print(i,"->",j,"d",S_fwr,d,tmp_W)
    while d > S_fwr:
        d = d - S_fwr
        t = t_table[timezone + 1]
        timezone += 1
        W = W+tmp_W
        #print("W = ",W)
        if timezone+1 == len(t_table):
            #print(i, "->", j, t0, d, c)
            return 10000000, 1000000000
        #print(t_table,timezone+1)
        dur = t_table[timezone+1]-t
        #print("time",timezone,t_table[timezone+1],t)
        if timezone%2 == 1: #platform
            v = speed[c][int((timezone+1)//2)]["speed"] #//???
            S_fwr = v*dur
            #print("1:",v,dur,0,load)
            tmp_W = get_work(v,dur,0,load)
        else:
            #print("time",timezone,t_table,speed[c])
            v0_cur = speed[c][int((timezone)//2)]['speed']
            a_cur = speed[c][int(timezone//2+1)]["a"]
            S_fwr = v0_cur*dur + 0.5*a_cur*(dur**2)
            vbar =(v0_cur+ speed[c][int(timezone//2+1)]['speed'])/2
            #print("2:",vbar,dur,a_cur,load)

            tmp_W = get_work(vbar,dur,a_cur,load)
            #if j == 5: print(tmp_W, S_fwr, d)

    #if j == 5: print(W, timezone,d)
    if timezone == 0:
        v0_cur = speed[c][0]["v0"]
        a_cur = speed[c][1]["a"]
        v_ini = v0_cur + a_cur * t
        t_dur =  (-v_ini + math.sqrt(v_ini ** 2 + 2 * a_cur * d)) / a_cur
        t = t + t_dur

        v_after = v_ini + a_cur*t_dur
        #print("3:",(v_ini+v_after)/2, t_dur, a_cur, load)
        W = W + get_work((v_ini+v_after)/2, t_dur, a_cur, load)
        #if i == 0 and j == 2 and t0 == 0:
         #   print("??",a_cur,t_dur,v_ini, v_after)
    elif timezone%2 == 1: #platform
        v = speed[c][int((timezone+1)//2)]["speed"]
        t = t + d/v
        #print("4:", v, t-t_remain ,0, load )
        W = W+get_work( v, d/v ,0, load )#(a1*v)*()
    else:
        past_time = t - speed[c][int(timezone // 2)]["end"]
        v0_cur = speed[c][int(timezone // 2)]["speed"]
        a_cur = speed[c][int(timezone // 2 + 1)]["a"]
        v_ini = v0_cur + a_cur * past_time
        t_dur =  ( -v_ini+ math.sqrt(v_ini**2+2*a_cur*d) ) / a_cur
        #print("t,t_dur",t,t_dur)
        t = t+ t_dur
        v_after = math.sqrt(v_ini**2 + 2*a_cur*d)

        #if j == 5: print(W, "v0 = ",v_ini, "a = ",a_cur,"t = ",t_dur,"vend = ",v_after,load,v_ini+a_cur*t_dur)
        W =W+get_work((v_after+v0_cur)/2,t_dur,a_cur,load)
        #if j == 5: print(W, t_dur)
    #print(">>>>>>>>W,t = ",W,t-t0)
    #print(i,"->",j,"t0 = ",t0,"trvt:",t-t0)
    return W
    #return round(t - t0,3)
