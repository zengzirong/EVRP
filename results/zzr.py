import os 
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# directory = ["final_large/srand_10", "final_large/srand_20", "final_large/srand_30",
#              "final_large/srand_40", "final_large/srand_50", "final_large/srand_60", 
#              "final_large/srand_70", "final_large/srand_80", "final_large/srand_90", 
#              "final_large/srand_100"]

# total_time = [0 for i in range(50)]
# total_ec = [0 for i in range(50)]
# ec = [1e9 for i in range(50)]
# Nveh = [0 for i in range(50)]
# run_time = [0 for i in range(50)]

# for id in range(10):
#     files = []
#     for filename in os.listdir(directory[id]):
#         if (filename == ".DS_Store"):
#             continue
#         files.append(filename)
#     files = sorted(files, key=lambda f: tuple(int(x) for x in f.split("=")[1].split("_")[:3]))

#     for i in range(len(files)):
#         lines = []
#         file = open(directory[id] + "/" + files[i], "r")
#         for line in file: lines.append(line)
#         tot = len(lines)
#         tmp_ec = float(lines[tot - 4].split(" ")[3])
#         tmp_total_time = float(lines[tot - 3].split(" ")[3])
#         tmp_run_time = float(lines[tot - 1].split(" ")[3])
#         tmp_Nveh = int(lines[tot - 5].split(" ")[0].split("Route")[1].split(":")[0])
#         total_ec[i] += tmp_ec
#         run_time[i] += tmp_run_time
#         if(tmp_ec < ec[i]):
#             ec[i] = tmp_ec
#             Nveh[i] = tmp_Nveh
#             total_time[i] = tmp_total_time
# for i in range(50): print(Nveh[i])
# print()
# for i in range(50): print(total_time[i])
# print()
# for i in range(50): print(total_ec[i] / 10)
# print()
# for i in range(50): print(ec[i])
# print()
# for i in range(50): print(run_time[i] / 10)
# print()
# for i in range(50): print(math.fabs((total_ec[i] / 10) - ec[i]) / ec[i] * 100)
# print()

# directory = ["algo_compare_1/LS_SPP_result", "algo_compare_1/tmp1", "algo_compare_1/tmp2"]

# ec = [0 for i in range(25)]
# run_time = [0 for i in range(25)]
# total_time = [0 for i in range(25)]
# total_dis = [0 for i in range(25)]

# ec_a = [0 for i in range(25)]
# ec_b = [0 for i in range(25)]
# ec_c = [0 for i in range(25)]

# for id in range(3):
#     files = []
#     for filename in os.listdir(directory[id]):
#         if (filename == ".DS_Store"):
#             continue
#         files.append(filename)
#     files = sorted(files, key=lambda f: tuple(int(x) for x in f.split("=")[1].split("_")[:3]))

#     for i in range(len(files)):
#         lines = []
#         file = open(directory[id] + "/" + files[i], "r")
#         for line in file: lines.append(line)
#         tot = len(lines)
#         tmp_ec = float(lines[tot - 4].split(" ")[3])
#         tmp_total_time = float(lines[tot - 3].split(" ")[3])
#         tmp_total_dis = float(lines[tot - 2].split(" ")[3])
#         tmp_run_time = float(lines[tot - 1].split(" ")[3])
#         tmp_Nveh = int(lines[tot - 5].split(" ")[0].split("Route")[1].split(":")[0])
#         run_time[i] = tmp_run_time
#         ec[i] = tmp_ec
#         total_time[i] = tmp_total_time
#         total_dis[i] = tmp_total_dis
#         # if(id == 0): ec_a[i] = tmp_total_dis
#         # if(id == 1): ec_b[i] = tmp_total_dis
#         # if(id == 2): ec_c[i] = tmp_total_dis
#     for i in range(25): print(ec[i])
#     print()
#     for i in range(25): print(run_time[i])
#     print()

# x = np.zeros(25)
# y = np.zeros(25)
# for i in range(25):
#     x[i] = ec_a[i]
#     y[i] = ec_b[i]
# # Plot scatter points
# plt.scatter(x, y, color='blue', s=10)
# plt.plot([0, 20000], [0, 20000], 'r--', label='45° Line')
# plt.xlabel('The minimum W obtained by LNS-SPP')
# plt.ylabel('The minimum W obtained by LNS (without SPP)')
# plt.title('Best Solution Quality Comparison')
# # # plt.grid(True, linestyle='--', alpha=0.3)
# # # plt.tight_layout()
# # # Show plot
# plt.show()

# directory = "algo_compare_2/all_result"
# ec = [0 for i in range(60)]

# def from_key(str = 'Q=3000_1000_1_LS_SPP_1200_result.txt'):
#     try:
#         _, key2, _, key0, key1, key3, _ =str.split('_')
#     except: print(f"Failed {str}")
    
#     return (key0, key1, int(key2), int(key3))
    
# files = []
# for filename in os.listdir(directory):
#     if (filename == ".DS_Store"):
#         continue
#     files.append(filename)
# files = sorted(files, key=from_key)

# for i in range(len(files)):
#     print(files[i])
# print()
    
# for i in range(len(files)):
#     lines = []
#     file = open(directory + "/" + files[i], "r")
#     for line in file: lines.append(line)
#     tot = len(lines)
#     tmp_ec = float(lines[tot - 4].split(" ")[3])
#     ec[i] = tmp_ec
    
# for i in range(60): print(ec[i])

# def from_key(str = '82B_result.txt'):
#     try:
#         s, _ = str.split('_')
#     except: print(f"Failed {str}")
    
#     val = 0
#     number_str = ""
#     for ch in s:
#         if(ch.isdigit()):
#             number_str += ch
#         else:
#             val += 0.01 * (ord(ch) - ord('A'))
#             break
#     val += int(number_str)
#     return val 

# directory = ["final_small/srand_10", "final_small/srand_20", "final_small/srand_30",
#              "final_small/srand_40", "final_small/srand_50", "final_small/srand_60", 
#              "final_small/srand_70", "final_small/srand_80", "final_small/srand_90", 
#              "final_small/srand_100"]

# total_time = [0 for i in range(62)]
# total_ec = [0 for i in range(62)]
# ec = [1e9 for i in range(62)]
# Nveh = [0 for i in range(62)]
# run_time = [0 for i in range(62)]

# for id in range(10):
#     files = []
#     for filename in os.listdir(directory[id]):
#         if (filename == ".DS_Store"):
#             continue
#         files.append(filename)
#     key = files = sorted(files, key = from_key)

#     for i in range(len(files)):
#         lines = []
#         file = open(directory[id] + "/" + files[i], "r")
#         for line in file: lines.append(line)
#         tot = len(lines)
#         tmp_ec = float(lines[tot - 4].split(" ")[3])
#         tmp_total_time = float(lines[tot - 3].split(" ")[3])
#         tmp_run_time = float(lines[tot - 1].split(" ")[3])
#         tmp_Nveh = int(lines[tot - 5].split(" ")[0].split("Route")[1].split(":")[0])
#         total_ec[i] += tmp_ec
#         run_time[i] += tmp_run_time
#         if(tmp_ec < ec[i]):
#             ec[i] = tmp_ec
#             Nveh[i] = tmp_Nveh
#             total_time[i] = tmp_total_time
# for i in range(62): print(Nveh[i])
# print()
# for i in range(62): print(total_time[i])
# print()
# for i in range(62): print(total_ec[i] / 10)
# print()
# for i in range(62): print(ec[i])
# print()
# for i in range(62): print(run_time[i] / 10)
# print()
# for i in range(62): print(math.fabs((total_ec[i] / 10) - ec[i]) / ec[i] * 100)
# print()