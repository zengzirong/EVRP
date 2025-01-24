import numpy as np
import math
import pyomo.environ as pyo
from sympy import symbols, Eq, solve
import pickle
import sys


def readData(instance, t_table):
    # global arf1, arf2, a1, a2, a3, T0, q, armax, armin, arRate, gamma, rou1, rou2, rou3, instance, mu, Electric
    # arf1, arf2, a1, a2, a3, T0, q, armax, armin, arRate, gamma, rou1, rou2, rou3, instance = arf11, arf21, a11, a21, a31, T01, q1, armax1, armin1, arRate1, gamma1, rou11, rou21, rou31, instance1
    # global pickups, speedMatrix, dis, num_pair, NumVechicle, capacityVechicle, Depots, t_table, speedprofile

    NumVechicle = 0
    capacityVechicle = 0
    Depots = []
    pickups = []
    num_pair = 0
    speedprofile = []
    speedMatrix = []
    with open(instance, 'r', encoding='utf8') as f:
        cont = True
        c = 0
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
                    # Vechicleweight = float(li[2][0])
                    Electric = float(li[2][0])

                elif li[0][0] == "[Node]" or li[0][0] == "[Depot]":
                    for i in li[1:]:
                        Depots.append(({
                            "idx": int(i[0]),
                            "x": float(i[1]),
                            "y": float(i[2])
                        }))
                    # print("Depots",Depots)
                elif li[0][0] == "[pickup]" or li[0][0] == "[Pickup]":
                    for i in li[1:]:
                        # print(i,i[4])
                        num_pair += 1
                        pickups.append(({
                            "rk": -float(i[4]),  # (float(i[7])-float(i[6]))*
                            "idx": int(i[0]),
                            "x": float(i[1]),
                            "y": float(i[2]),
                            "load": float(i[4])
                        }))
                    # print("pickups",pickups)


                elif li[0][0] == "[Speed":
                    speed_num = int(li[0][1][:-1])
                    speedprofile.append([])
                    speedprofile[speed_num].append(({"v0": float(li[1][0])}))
                    last_speed = float(li[1][0])
                    last_time = 0
                    for i in li[2:]:
                        speedprofile[speed_num].append(({
                            "start": float(i[0]),
                            "end": float(i[1]),
                            "speed": float(i[-1]),
                            "a": (float(i[-1]) - last_speed) / (float(i[0]) - last_time)
                        }))
                        # print("st,en,a", float(i[-1]),last_speed,float(i[0]),last_time,
                        # (float(i[-1]) - last_speed) / (float(i[0]) - last_time))
                        last_speed = float(i[-1])
                        last_time = float(i[1])
                        # print(speedprofile[speed_num][2]["start"])
                    # print("\n")

                elif li[0][1] == "choose":
                    for i in li[1:]:
                        speedMatrix.append([int(s) for s in i])
                li = []

    dis = [[0 for i in range(2 + num_pair)] for j in range(2 + num_pair)]
    for i in range(1, num_pair + 1):
        x1, y1 = pickups[i]["x"], pickups[i]["y"]
        x2, y2 = Depots[0]["x"], Depots[0]["y"]
        dis[0][i] = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)  # depot1 & pickup
        dis[i][num_pair + 1] = dis[0][i]
        dis[num_pair + 1][i] = dis[0][i]
        dis[i][0] = dis[0][i]
        for j in range(i + 1, num_pair + 1):
            x2, y2 = pickups[j]["x"], pickups[j]["y"]  # pickup &node
            dis[i][j] = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
            dis[j][i] = dis[i][j]
    # print(speedMatrix)
    # print(pickups)
    # for i in range(num_pair+1):
    # print(dis[i])
    return pickups, speedMatrix, dis, num_pair, NumVechicle, capacityVechicle, Depots, speedprofile


def get_ttTao(i, j, t0):
    a1, a2, a3, mu, vehm = 479.1, -18.93, 0.7876, 1.507, 1000
    W = 0
    t = t0
    c = speedMatrix[i][j]
    d = distMat[i][j]
    timezone = -1
    # print(i, "->", j, t0,d)
    tt_table = [0, 30, 90, 180, 540, 570, 690, 750, 840]
    for kk in range(len(tt_table) + 1):
        if t >= tt_table[kk] and t < tt_table[kk + 1]:
            timezone = kk
            break
    # print("tmpezone = ",timezone)
    if timezone == -1:
        return -1
    if timezone == 0:
        v0_cur = speedprofile[c][0]["v0"]
        a_cur = speedprofile[c][1]["a"]
        v = v0_cur + a_cur * t
        t_remain = speedprofile[c][1]["start"] - t
        S_fwr = v * t_remain + 0.5 * a_cur * (t_remain ** 2)

    elif timezone % 2 == 1:  # platform
        v = speedprofile[c][int((timezone + 1) // 2)]["speed"]
        a_cur = 0
        S_fwr = v * (speedprofile[c][int(timezone // 2 + 1)]["end"] - t)

    else:
        past_time = t - speedprofile[c][int(timezone // 2)]["end"]
        v0_cur = speedprofile[c][int(timezone // 2)]["speed"]
        a_cur = speedprofile[c][int(timezone // 2 + 1)]["a"]
        v = v0_cur + a_cur * past_time
        t_remain = speedprofile[c][int(timezone // 2 + 1)]["start"] - t
        S_fwr = v * t_remain + 0.5 * a_cur * (t_remain ** 2)
        # print("timsezone",v*t_remain,0.5*a_cur*(t_remain**2))
    # print(t0,a_cur,v,S_fwr)
    tmp_W = 0
    while S_fwr < d:
        d = d - S_fwr
        t = tt_table[timezone + 1]
        timezone += 1
        W = W + tmp_W
        # print("W = ",W)
        if timezone == len(tt_table):
            return -1

        dur = tt_table[timezone + 1] - t
        if timezone % 2 == 1:  # platform
            v = speedprofile[c][int((timezone + 1) // 2)]["speed"]
            S_fwr = v * dur
            tmp_W = (a1 * v) * dur
        else:
            v0_cur = speedprofile[c][int(timezone // 2)]["speed"]
            a_cur = speedprofile[c][int(timezone // 2 + 1)]["a"]
            S_fwr = v0_cur * dur + 0.5 * a_cur * (dur ** 2)
            vbar = (v0_cur + v0_cur + a_cur * dur) / 2
            # tmp_W = get_work(vbar, dur, a_cur, load)
            # if i == 3 and j == 5:
            # print("ha,",S_fwr ,v0_cur,a_cur,timezone)

    t_remain = t
    if timezone == 0:
        v0_cur = speedprofile[c][0]["v0"]
        a_cur = speedprofile[c][1]["a"]
        v_ini = v0_cur + a_cur * t
        t_dur = ((-v_ini + math.sqrt(v_ini ** 2 + 2 * a_cur * d)) / a_cur)
        t = t + t_dur
        v_after = math.sqrt(v_ini ** 2 + 2 * a_cur * d)
        # W = W + get_work((v_ini + v_after) / 2, t_dur, a_cur, load)
    elif timezone % 2 == 1:  # platform
        v = speedprofile[c][int((timezone + 1) // 2)]["speed"]
        t = t + d / v
        # W = W + (a1 * v) * (t - t_remain)
    else:
        past_time = t - speedprofile[c][int(timezone // 2)]["end"]
        v0_cur = speedprofile[c][int(timezone // 2)]["speed"]
        a_cur = speedprofile[c][int(timezone // 2 + 1)]["a"]
        v_ini = v0_cur + a_cur * past_time
        t_dur = ((-v_ini + math.sqrt(v_ini ** 2 + 2 * a_cur * d)) / a_cur)
        t = t + t_dur
        v_after = math.sqrt(v_ini ** 2 + 2 * a_cur * d)
        # print("dur",v_ini,t_remain,d)
        # W = W + get_work((v_after + v0_cur) / 2, t_dur, a_cur, load)
    # print(i,"->",j,t0,"W = ", W,"travel time",t-t0)
    return round(t - t0, 3)


# 解三元一次方程求abc
def get_abc(i, j, m):
    t0, t2 = get_tij(i, j, m - 1), get_tij(i, j, m)
    # np.random.seed(10)
    t1 = np.random.uniform(t0, t2)

    travel_t0, travel_t1, travel_t2 = get_ttTao(i, j, t0), get_ttTao(i, j, t1), get_ttTao(i, j, t2)
    # # 利用numpy解方程组
    # coeff_mat = np.mat([[t0 ** 2, t0, 1], [t1 ** 2, t1, 1], [t2 ** 2, t2, 1]])  # 系数矩阵
    # cons_mat = np.mat([travel_t0, travel_t1, travel_t2]).T  # 常数项列矩阵
    # res = solve(coeff_mat, cons_mat)
    # abc = []
    # for r in res:
    #     abc.append(r[0])
    # print(res)
    # 利用sympy求解三元一次方程组
    a, b, c = symbols('a,b,c')

    # defining equations
    eq1 = Eq(((t0 ** 2) * a + t0 * b + c), travel_t0)
    # print("Equation 1:")
    # print(eq1)

    eq2 = Eq(((t1 ** 2) * a + t1 * b + c), travel_t1)
    # print("Equation 2")
    # print(eq2)

    eq3 = Eq(((t2 ** 2) * a + t2 * b + c), travel_t2)
    # print("Equation 3")
    # print(eq3)

    # solving the equation and printing the
    # value of unknown variables
    # print("Values of 3 unknown variable are as follows:")
    res = solve((eq1, eq2, eq3), (a, b, c))
    # print("------------------->")
    # print("m:", m)
    # print("t_random:", t1)
    # print(solve((eq1, eq2, eq3), (a, b, c)))

    # return [res[a], res[b], res[c]], [t0, t1, t2], [travel_t0, travel_t1, travel_t2]
    return [float(res[a]), float(res[b]), float(res[c])]


def get_tot_abc():
    res = {}
    for i in range(num_node - 1):
        for j in range(1, num_node):
            if i == 0 and j == num_node - 1:
                continue
            # print(i, j)
            if i != j:
                res_abc = [[]]
                for m in range(1, max_m):
                    if m in col3:
                        res_abc.append([])
                        continue
                    res_abc.append(get_abc(i, j, m))
                # print(res_abc)
                res[(i, j)] = res_abc
    print("a,b,c complete!")
    return res


# 获取当前时刻
def get_tij(i, j, m):
    t_mij = 0
    if m in col1:
        t_mij = get_tij(i, j, m + 1) - (v[m + 1] - np.sqrt(pow(v[m + 1], 2) - 2 * a[m - 1] * distMat[i][j])) / a[m - 1]
    elif m in col3:
        t_mij = get_tij(i, j, m + 1) - distMat[i][j] / v[m - 1]
    else:
        t_mij = t_table[m]
    return t_mij


# 获取在第j个点的总做功
def get_tot_work(model, i, j, m):
    # tot_work = 0
    # for m in range(1, max_m):
    if m in col1:
        tot_work = (model.s[j] - model.s[i]) * (r + abs(a[m - 1]) * mu * M) * 0.5 * (
                    2 * v[m - 1] + a[m - 1] * (model.s[i] - get_tij(i, j, m - 1)) + a[m - 1] * (
                        model.s[j] - get_tij(i, j, m - 1)))
    elif m in col2:
        tot_work = (get_tij(i, j, m) - model.s[i]) * (r + abs(a[m - 2]) * mu * M) * 0.5 * (
                v[m - 2] + a[m - 2] * (model.s[i] - get_tij(i, j, m - 2)) + v[m]) + v[m] * r * (
                           model.s[j] - get_tij(i, j, m))
    elif m in col3:
        tot_work = v[m - 1] * r * (model.s[j] - get_tij(i, j, m))

    else:
        tot_work = (model.s[j] - get_tij(i, j, m)) * (
                r + mu * M * abs(a[m])) * 0.5 * (2 * v[m] + a[m] * (model.s[j] - get_tij(i, j, m))) + v[m] * r * (
                           get_tij(i, j, m) - model.s[i])
    return tot_work


# 约束（7）
def get_dist_balance(model, i, j):
    dist_time = 0
    for m in range(1, max_m):
        if m in col1:
            dist_time += model.x[i, j, m] * (
                    (v[m - 1] + a[m - 1] * (model.w[i, j, m] - get_tij(i, j, m - 1))) * (
                    model.s[j] - model.w[i, j, m]) + 0.5 * a[m - 1] * (
                            (model.s[j] - model.w[i, j, m]) ** 2))
        elif m in col2:
            dist_time += model.x[i, j, m] * ((v[m - 2] + a[m - 2] * (model.w[i, j, m] - get_tij(i, j, m - 2))) * (
                    get_tij(i, j, m) - model.w[i, j, m]) + 0.5 * a[m - 2] * (
                                                     (get_tij(i, j, m) - model.w[i, j, m]) ** 2) + (
                                                     model.s[j] - get_tij(i, j, m)) * v[m])
        elif m in col3:
            dist_time += model.x[i, j, m] * (model.s[j] - model.w[i, j, m]) * v[m - 1]
        else:
            dist_time += model.x[i, j, m] * (
                    (get_tij(i, j, m) - model.w[i, j, m]) * v[m] + v[m] * (model.s[j] - get_tij(i, j, m)) + 0.5 * a[m]
                    * ((model.s[j] - get_tij(i, j, m)) ** 2))

    return dist_time


# 获取旅行时间
def get_travel_time(model, i, j, m):
    if m in col3:
        travel_time = distMat[i][j] / v[m - 1]
    else:
        a, b, c = abc_dict[(i, j)][m]
        travel_time = a * pow(model.s[i], 2) + b * model.s[i] + c

    return travel_time


def setModel():
    # 创建模型
    model = pyo.ConcreteModel()
    # 决策变量
    model.x = pyo.Var(range(num_node), range(num_node), range(max_m), domain=pyo.Binary)  # 在m时间空间里从i前往j
    # model.y = pyo.Var(range(num_node), range(num_node), domain=pyo.Binary)  # 边ij是否被车辆选中旅行
    model.w = pyo.Var(range(num_node), range(num_node), range(max_m), bounds=(0, max(t_table[:max_m])),
                      domain=pyo.NonNegativeReals)  # 在m的时间空间里由i到j的行驶时间
    model.s = pyo.Var(range(num_node), bounds=(0, max(t_table[:max_m])), domain=pyo.NonNegativeReals)  # 从i离开的时间，包括0的正整数
    # model.Q = pyo.Var(range(num_node), bounds=(0, sum(q)), domain=pyo.NonNegativeReals)  # 服务完i后的总需求量
    model.W = pyo.Var(range(num_node), domain=pyo.NonNegativeReals)  # 服务完i后的总做功

    # 目标函数
    model.tot_work = pyo.Objective(expr=model.W[num_node - 1] - model.W[0], sense=pyo.minimize)
    # model.tot_work = pyo.Objective(expr=model.s[num_node - 1] - model.s[0], sense=pyo.minimize)
    # 约束条件
    ## 车辆进出仓库约束
    model.start_back_depot = pyo.ConstraintList()
    model.start_back_depot.add(expr=sum(model.x[0, j, m] for m in range(1, max_m) for j in range(1, num_node - 1)) == 1)
    model.start_back_depot.add(
        expr=sum(model.x[i, num_node - 1, m] for m in range(1, max_m) for i in range(1, num_node - 1)) == 1)

    ## 流平衡约束、至多一辆车服务
    model.flow_balance = pyo.ConstraintList()
    model.vehicle_num = pyo.ConstraintList()
    for k in range(1, num_node - 1):
        model.flow_balance.add(
            expr=sum(model.x[i, k, m] for i in range(num_node - 1) for m in range(1, max_m) if i != k) == sum(
                model.x[k, j, m] for j in range(1, num_node) for m in range(1, max_m) if j != k))
        ### 有问题，再看看
        model.vehicle_num.add(
            expr=sum(model.x[i, k, m] for i in range(num_node - 1) for m in range(1, max_m) if i != k) == 1)
        model.vehicle_num.add(
            expr=sum(model.x[k, j, m] for j in range(1, num_node) for m in range(1, max_m) if j != k) == 1)

    # ## 边约束
    # model.arc = pyo.ConstraintList()
    # for m in range(2, max_m):
    #     for k in range(1, num_node-1):
    #         model.arc.add(expr=sum(model.x[i, k, m-1] for i in range(num_node-1)) <= sum(model.x[k, j, m] for j in range(1, num_node)))
    #         model.arc.add(expr=sum(model.w[i, k, m-1] for i in range(num_node-1)) <= sum(model.w[k, j, m] for j in range(1, num_node)))

    ## 容量约束
    # model.capacity = pyo.ConstraintList()
    # model.capacity.add(expr=model.Q[0] == sum(q))
    # model.capacity.add(expr=model.Q[num_node - 1] == 0)
    # for i in range(num_node - 1):
    #     for j in range(1, num_node):
    #         if i == 0 and j == num_node - 1:
    #             continue
    #         if i != j:
    #             model.capacity.add(
    #                 expr=model.Q[i] - q[j] <= model.Q[j] + 100000 * (
    #                         1 - sum(model.x[i, j, m] for m in range(1, max_m))))
    #             # model.capacity.add(
    #             #     expr=model.Q[i] - q[j] - 100000 * (1 - model.y[i, j]) <= model.Q[j])

    ## 时间窗约束
    model.time_window = pyo.ConstraintList()
    for i in range(num_node - 1):
        for j in range(1, num_node):
            if i == 0 and j == num_node - 1:
                continue
            if i != j:
                for m in range(1, max_m):
                    model.time_window.add(expr=model.w[i, j, m] <= model.x[i, j, m] * get_tij(i, j, m))
                    model.time_window.add(expr=model.w[i, j, m] >= model.x[i, j, m] * get_tij(i, j, m - 1))

    ## 离开时间约束
    model.departure_time = pyo.ConstraintList()
    model.departure_time.add(expr=model.s[0] == 0)
    for i in range(num_node - 1):
        # for j in range(1, num_node):
        # if i == 0 and j == num_node - 1:
        #     continue
        # if i != j:
        model.departure_time.add(
            expr=model.s[i] == sum(model.w[i, j, m] for j in range(1, num_node) for m in range(1, max_m) if
                                   i != j or (i != 0 and j != num_node - 1)))

    # ## 做功约束
    model.total_work = pyo.ConstraintList()
    model.total_work.add(expr=model.W[0] == 0)
    for i in range(num_node - 1):
        for j in range(1, num_node):
            if i == 0 and j == num_node - 1:
                continue
            if i != j:
                for m in range(1, max_m):
                    model.total_work.add(
                        expr=model.W[j] + 100000 * (1 - model.x[i, j, m]) >= get_tot_work(model, i, j, m) + model.W[i])

    ## 距离约束
    model.departure_travel_time = pyo.ConstraintList()
    # model.departure_travel_time.add(expr=model.s[0] == 0)
    for i in range(num_node - 1):
        for j in range(1, num_node):
            if i == 0 and j == num_node - 1:
                continue
            if i != j:
                # model.total_dist_bala.add(expr=distMat[i][j] * model.y[i, j] == get_dist_balance(model, i, j))
                # model.total_dist_bala.add(expr=distMat[i][j] * model.y[i, j] == sum(
                #     model.x[i, j, m] * (model.s[j] - model.w[i, j, m]) for m in range(1, max_m)))
                for m in range(1, max_m):
                    model.departure_travel_time.add(
                        expr=model.s[j] + 100000 * (1 - model.x[i, j, m]) >= model.s[i] + get_travel_time(model,
                                                                                                          i, j,
                                                                                                          m))

    # ## x出发的约束
    # model.choose = pyo.ConstraintList()
    # for i in range(num_node - 1):
    #     for j in range(1, num_node):
    #         if i == 0 and j == num_node - 1:
    #             continue
    #         if i != j:
    #             model.choose.add(expr=sum(model.x[i, j, m] for m in range(1, max_m)) == model.y[i, j])

    # ## y的流平衡
    # model.y_bala = pyo.ConstraintList()
    # for i in range(num_node - 1):
    #     model.y_bala.add(
    #         expr=sum(model.y[i, j] for j in range(1, num_node)) == sum(model.y[j, i] for j in range(1, num_node)))

    return model


# 求解器设置
def calObjFromSolvers(model, mtype, tmlimit):
    print("----Solving----")
    if mtype == 'nlp':
        bonmin_path = '/Users/jingyi/COIN-OR-1.7.3-macosx-x86_64-clang500.2.76/bin/bonmin.exe'
        opt = pyo.SolverFactory('bonmin', executable=bonmin_path)  # 求解器的选择
        opt.options['bonmin.time_limit'] = tmlimit  # bonmin求解时间限制，单位秒
    elif mtype == 'lp':
        glpk_path = 'D:/办公文件/编程/数学建模/solver/winglpk-4.65/glpk-4.65/w64/glpsol.exe'
        opt = pyo.SolverFactory('glpk', executable=glpk_path)  # 求解器的选择
        opt.options['tmlim'] = tmlimit  # glpk求解时间限制，单位秒
    elif mtype == 'grb':
        opt = pyo.SolverFactory("gurobi", solver_io="python")

    elif mtype == "msk":
        opt = pyo.SolverFactory('mosek')

    elif mtype == "ipopt":
        ipopt_path = '/Users/jingyi/COIN-OR-1.7.3-macosx-x86_64-clang500.2.76/bin/ipopt.exe'
        opt = pyo.SolverFactory('ipopt', executable=ipopt_path)

    results = opt.solve(model, tee=True)
    results.write()


if __name__ == "__main__":
    global col1, col2, col3, col4, a, v, distMat, t_table, M, max_m, num_node, q, abc_dict
    r, a2, a3, mu, M = 479.1, -18.93, 0.7876, 1.507, 1000
    t_table = [0, 30, 30, 90, 90, 180, 180, 540, 540, 570, 570, 690, 690, 750, 750, 840, 840]
    col1 = [1, 5, 9, 13]
    col2 = [2, 6, 10, 14]
    col3 = [3, 7, 11, 15]
    col4 = [4, 8, 12]

    instance = '../Instances/4.txt'
    # 距离矩阵在首尾包含depot
    pickups, speedMatrix, distMat, num_pair, NumVechicle, capacityVechicle, Depots, speedprofile = readData(
        instance, t_table)
    case = speedprofile[4]
    print(len(distMat))

    # distMat = [[0, 2, 4, 8, 5, 0], [2, 0, 2, 6, 3, 2], [4, 2, 0, 4, 1, 4], [8, 6, 4, 0, 3, 8], [5, 3, 1, 3, 0, 5],
    #            [0, 2, 4, 8, 5, 0]]

    # 固定参数
    # a = [case[i]['a'] for i in range(1, len(case))]   # 加速度
    max_m = 3 # 时区的个数
    num_node = len(distMat)  # 0、11为depot
    # 各个点的需求量
    q = [0.0]
    for i in range(1, num_node - 1):
        q.append(pickups[i]['load'])
    q.append(0.0)
    # 取出加速度和速度
    a = []
    for i in range(1, len(case)):
        a += [case[i]['a']] * 2
        a += [0] * 2
    a.append(0)
    v_g = [case[i]['speed'] if i != 0 else case[i]['v0'] for i in range(len(case))]  # 速度
    print(v_g)
    v = []
    for i in range(max_m + 1):
        if i == 0:
            v.append(v_g[0])
        elif i in col1:
            v.append(0)
        else:
            idx = (i // 4) + 1 if i % 4 != 0 else (i // 4)
            v.append(v_g[idx])
    print("a:",a)
    print("v:",v_g)

    abc_dict = get_tot_abc()
    # print(res)
    # 1/0

    model = setModel()

    # 保存模型
    # f = open(r'D:\办公文件\科研\working paper\paper\代码\AAEVRP\model.txt', 'w')
    # sys.stdout = f
    model.pprint()
    # f.close()

    calObjFromSolvers(model, 'nlp', 3600 * 12)  # 6h
    print('Min W:', model.tot_work())
    # Q_res = [pyo.value(model.Q[i]) for i in range(num_node)]
    W_res = [pyo.value(model.W[i]) for i in range(num_node)]
    # print(Q_res)
    print(W_res)

    # x的结果
    x_val = []
    for i in range(num_node - 1):
        for j in range(1, num_node):
            if i == 0 and j == num_node - 1:
                continue
            if i != j:
                for m in range(1, max_m):
                    if pyo.value(model.x[i, j, m]) == 1:
                        x_val.append((i, j, m, pyo.value(model.x[i, j, m])))
    w_val = []
    for i in range(num_node - 1):
        for j in range(1, num_node):
            if i == 0 and j == num_node - 1:
                continue
            if i != j:
                for m in range(1, max_m):
                    if pyo.value(model.w[i, j, m]) >= 1:
                        w_val.append((i, j, m, pyo.value(model.w[i, j, m])))
    s_val = []
    for i in range(num_node):
        s_val.append((i, pyo.value(model.s[i])))

    # y_val = []
    # for i in range(num_node - 1):
    #     for j in range(1, num_node):
    #         if i == 0 and j == num_node - 1:
    #             continue
    #         if i != j:
    #             if pyo.value(model.y[i,j]) == 1:
    #                 y_val.append((i,j,pyo.value(model.y[i,j,m])))

    # print(pickups)
    # print(len(q), q)
    # print(speedMatrix)
    # print(dis)
    # print(num_pair)
    # print(NumVechicle)
    # print(capacityVechicle)
    # print(Depots)
    # print(t_table)
    # print(speedprofile)
