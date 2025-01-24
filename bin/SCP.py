from gurobipy import *
def columns_progress(routes_pool, num_pair):
    # 每一行对应一个a_ip，A_ip[i][p]表示第i个客户是否被第p列服务，若被服务则A_ip[i][p]=1，反之为0
    A_ip = [[0 for _ in range(len(routes_pool))] for _ in range(num_pair + 2)]
    columns_cost = []

    for p in range(len(routes_pool)):
        sol = routes_pool[p]
        #print(sol)
        for node_id in sol[0]:
            A_ip[node_id][p] = 1
        columns_cost.append(sol[1][0])

    return A_ip, columns_cost


# 求解模型并输出目标值和列
def solve_scp_model(routes_pool, num_pair):
    A_ip, columns_cost = columns_progress(routes_pool, num_pair)
    col_num = len(routes_pool)
    # 新建模型
    model = Model("mip1")

    # 决策变量
    y = [0 for i in range(col_num)]
    for i in range(col_num):
        y[i] = model.addVar(vtype=GRB.BINARY, name= str(i))

    # 目标函数
    tot_cost = 0
    for p in range(col_num):
        tot_cost += columns_cost[p] * y[p]
    model.setObjective(tot_cost, GRB.MINIMIZE)
    # 约束条件

    for i in range(1, num_pair + 1):
        tmp = sum(A_ip[i][p] * y[p] for p in range(col_num))
        model.addConstr(tmp == 1)
    model.setParam('TimeLimit',  1200)
    model.optimize()

    route = []
    route.append(0)
    sumcost = 0
    for v in model.getVars():
        #print("v.x",v.x)
        if round(v.x,0) == 1:
            #print(routes_pool[int(v.varName)])
            sumcost += routes_pool[int(v.varName)][1][0]
            for k in routes_pool[int(v.varName)][0]:
                route.append(k)

    route.append(num_pair+1)
    #print("sumcost", sumcost, route)
    #a = input()
    #model.getAttr('Pi',y)
    #print("route from SPP:",route)
    return sumcost, route

if __name__ == "__main__":
    print("")