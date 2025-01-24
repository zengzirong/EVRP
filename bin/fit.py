#! /usr/bin/python3
import sys, getopt
from readData import readmain
from travel_time import ttTao
from test import evaluate
import signal

# 处理程序，用于停止程序
def handler(signum, frame):
    print("Time's up!")
    raise SystemExit

# 设置定时器
signal.signal(signal.SIGALRM, handler)
signal.alarm(3600*12)
instance = ""
arf1,T0,q,armax,armin,arRate,gamma,rou1,rou2,rou3=0.99, 247 ,0.99 , 0.80  ,0.32   ,0.36 , 0.32 ,  20 ,  12 ,   3

def main(argv):
    global arf1,T0,q,armax,armin,arRate,gamma,rou1,rou2,rou3,instance
    try:
        opts, args = getopt.getopt(argv, "i:arf1: T0: q: armax: armin: arRate: gamma :rou1: rou2: rou3:s:",\
                                   ["instance=","arf1=","T0=","q=",\
                                    "armax=","armin=","arRate=","gamma=", "rou1=", "rou2=", "rou3=","seed="])
    except getopt.GetoptError:
        print("fit.py -i <instance> -mu <param mu> -lamda <param lamda> -pc <param pc> -pe <param pe> -arfa <param arfa>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--instance"):
            instance = arg
        elif opt in ("-arf1", "--arf1"):
            arf1 = float(arg)
        elif opt in ("-rou1", "--rou1"):
            rou1 = int(arg)
        elif opt in ("-rou2", "--rou2"):
            rou2 = int(arg)
        elif opt in ("-rou3", "--rou3"):
            rou3 = int(arg)
        elif opt in ("-T0", "--T0"):
            T0 = int(arg)
        elif opt in ("-q", "--q"):
            q = float(arg)
        elif opt in ("-armax", "--armax"):
            armax = float(arg)
        elif opt in ("-arRate", "--arRate"):
            arRate = float(arg)
        elif opt in ("-armin", "--armin"):
            armin = float(arg)
        elif opt in ("-gamma", "--gamma"):
            gamma = float(arg)
    #'''
try:
    # 在这里编写您的程序
    while True:
        a = input()
        instance = '../cola_new/' + a + '.txt'
        k = input()
        res = evaluate(arf1, T0, q, armax, armin, arRate, gamma, rou1, rou2, rou3, instance, a, k)
        print(res)
        pass
except SystemExit:
    print("Program stopped.")
