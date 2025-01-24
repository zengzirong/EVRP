#include<bits/stdc++.h>
#include "gurobi_c++.h"
using namespace std;

const int N = 2000+5;
const int M = 10000;
const double const_y = 460.96;
const double const_m = 1507;
const double const_r = 479.1;
const double const_s = -18.93;
const double const_c = 0.7876;
const double eps = 1e-6;
int VehicleNumber;
double VechicleCapacity, Electricity;

double time_limit = 7200.00;
string data_file;
//string data_file = "dataset/200_1.txt";

vector<vector<int> > route_pool;
vector<vector<int> > route_ids;
vector<vector<int> > candidate_routes;

int n;
struct node{
    double x, y;
    double demand;
    double serve_time;
    int customer_id, node_id;
}pickups[N];
double dis[N][N];

struct vode{
    double t, v, a;
};
const int speed_cnt = 5;
vector<vode> speed[5];
int speed_id[N][N];
#define pdd pair<double,double>
inline double power(double x, int y)
{
    double ans = 1.0;
    for(; y; y >>= 1)
    {
        if(y&1) ans = ans * x;
        x = x * x;
    }
    return ans;
}
inline pdd get_val(int x, int y, double start_time, double load)
{
    int pos = 0;
    int id = speed_id[x][y];
    double cur_time = start_time, ec = 0;
    for(int i=0; i<(int)speed[id].size(); i++)    
    {
        if(cur_time >= speed[id][i].t) pos = i;
        else break;  
    }
    double cur_v = speed[id][pos].v + speed[id][pos].a * (cur_time - speed[id][pos].t);
    double d = dis[x][y];
    while(d > eps)
    {
        double t, tmp_dis, v;
        bool flag = false;
        if(pos == (int)speed[id].size()-1) flag = true;
        else 
        {
            t = speed[id][pos+1].t - cur_time;
            tmp_dis = cur_v * t + 1.0 / 2 * speed[id][pos].a * t * t; 
            flag = (tmp_dis >= d);
        }
        if(!flag)
        {
            v = cur_v + speed[id][pos].a * t;
            // ec += (cur_v + v) / 2.0 * t * (const_y + (const_m + load) * abs(speed[id][pos].a));
            // ec += ((cur_v + v) / 2.0 * t) * (479.1 + abs(speed[id][pos].a) * 1507);
            // ec += ((cur_v + v) / 2.0 * t) * (479.1 + abs(speed[id][pos].a) * (1507 + load));
            double a = speed[id][pos].a;
            ec += const_c / 4.0 * power(a, 3) * power(t, 4);
            ec += (const_s / 3.0 * power(a, 2) + const_c * cur_v * power(a, 2)) * power(t, 3);
            ec += (const_r * a / 2.0 + const_s * cur_v * a + 1.5 * const_c * power(cur_v, 2) * a + (const_m + load) / 2.0 * power(a, 2)) * power(t, 2);
            ec += (const_r * cur_v + const_s * power(cur_v, 2) + const_c * power(cur_v, 3) + (const_m + load) * a * cur_v) * t;
            cur_v = speed[id][pos+1].v;
            cur_time = speed[id][pos+1].t;
            d -= tmp_dis;
            pos++;
        }
        else 
        {
            if(abs(speed[id][pos].a) < eps) t = d / cur_v, v = cur_v;
            else v = sqrt(2 * speed[id][pos].a * d + cur_v * cur_v), t = (v - cur_v) / speed[id][pos].a;
            // ec += (cur_v + v) / 2.0 * t * (const_y + (const_m + load) * abs(speed[id][pos].a));
            // ec += ((cur_v + v) / 2.0 * t) * (479.1 + abs(speed[id][pos].a) * 1507);
            // ec += ((cur_v + v) / 2.0 * t) * (479.1 + abs(speed[id][pos].a) * (1507 + load));
            double a = speed[id][pos].a;
            ec += const_c / 4.0 * power(a, 3) * power(t, 4);
            ec += (const_s / 3.0 * power(a, 2) + const_c * cur_v * power(a, 2)) * power(t, 3);
            ec += (const_r * a / 2.0 + const_s * cur_v * a + 1.5 * const_c * power(cur_v, 2) * a + (const_m + load) / 2.0 * power(a, 2)) * power(t, 2);
            ec += (const_r * cur_v + const_s * power(cur_v, 2) + const_c * power(cur_v, 3) + (const_m + load) * a * cur_v) * t; 
            cur_time += t;
            d = 0;
        }
    }
    return pdd(cur_time - start_time, ec);
}

#define inf 1e9

inline double get_route_dis(vector<int> route)
{
    double ans = 0;
    if(!route.size()) return ans;
    int last = 0;
    for(auto k : route) 
    {
        ans += dis[last][k];
        last = k;
    }
    ans += dis[last][0];
    return ans;
}

struct RouteInfo{
    double ec;
    double total_time;
    double total_dis;
};

inline RouteInfo get_route_info(vector<int> route)
{
    if(!route.size()) return (RouteInfo){0, 0, 0};
    double load = 0;
    for(auto k : route) load += pickups[k].demand;
    if(load > VechicleCapacity) return (RouteInfo){inf, inf, inf};
    double total_dis = get_route_dis(route);
    if(total_dis > Electricity) return (RouteInfo){inf, inf, inf};
    double cur_time = 0, cur_ec = 0; 
    pdd tmp = get_val(0, route[0], cur_time, load);
    cur_time += tmp.first;
    cur_ec += tmp.second;
    for(int i = 0; i < (int)route.size() - 1; i++)
    {
        load -= pickups[route[i]].demand;
        tmp = get_val(route[i], route[i+1], cur_time, load);
        cur_time += tmp.first;
        cur_ec += tmp.second;
    }
    load -= pickups[route[(int)route.size()-1]].demand;
    // assert(abs(load) < 1e-6);
    tmp = get_val(route[(int)route.size()-1], 0, cur_time, load);
    // assert(tmp.second != 0);
    cur_time += tmp.first;
    cur_ec += tmp.second;
    // cout<<"qwe"<<endl;
    // for(auto k : route) cout << k << " ";
    // cout<<endl; 
    // cout<<cur_EC<<endl;
    // if(cur_EC > Electricity) return inf;
    // cout<<"yes"<<endl;
    // if((int)route_pool.size() < M) route_pool.push_back(route);
    return (RouteInfo){cur_ec, cur_time, total_dis};
}

struct Solution{
    vector<vector<int> > routes;
    double ec;
    double total_time;
    double total_dis;
    inline void update()
    {
        ec = 0;
        total_time = 0;
        total_dis = 0;
        for(auto route : routes)
        {
            RouteInfo val = get_route_info(route);
            ec += val.ec;
            total_time += val.total_time;
            total_dis += val.total_dis;
        }
    }
    // inline void update_ec()
    // {
    //     ec = 0;
    //     for(auto route : routes)
    //         ec += get_route_info(route);
    // }
};

map<int, int> mp;
double dis_matrix[N][N];
inline void read_data()
{
    ifstream cin;
    cin.open("../cola_new/Customer2ID.txt");
    int customer_id, node_id;
    while(cin >> customer_id >> node_id)
    {
        mp[customer_id] = node_id - 1;
    }
    //cout << mp.size() << endl;
    cin.close();
    cin.open("../cola_new/ODMatrix.txt");
    int id1, id2; double d;
    // int id_max = 0;
    while(cin >> id1 >> id2 >> d)
    {
        dis_matrix[id1 - 1][id2 - 1] = d;
        // id_max = max(id_max, id1 - 1);
        // id_max = max(id_max, id2 - 1);
    }
    // cout<<"id_max = "<<id_max<<endl;
    // double maxx_val=0;
    // for(int i=0;i<id_max;i++) maxx_val=max(maxx_val,dis_matrix[0][i]+dis_matrix[i][0]);
    // cout<<"maxx_val = "<<maxx_val<<endl;
    // exit(0);
    //cout << "tot = " << tot << endl;
    cin.close();
    data_file = "../" + data_file;
    cin.open(data_file);
    cin >> VehicleNumber >> VechicleCapacity >> Electricity;
    n = VehicleNumber;
    string trash;
    for(int i = 1; i <= 11; i++) cin >> trash; 
    cin >> trash; // [pickup]
    int pickupid, customerid, demand, servetime;
    for(int i = 1; i <= n; i++)
    {
        cin >> pickupid >> customerid >> demand >> servetime;
        pickups[i].demand = demand;
        pickups[i].serve_time = servetime;
        pickups[i].x = pickups[i].y = 0.0;
        pickups[i].customer_id = customerid;
        pickups[i].node_id = mp[customerid];
    }
    for(int i = 0; i <= n; i++)
        for(int j = 0; j <= n; j++)
        {
            int id1 = pickups[i].node_id;
            int id2 = pickups[j].node_id;
            dis[i][j] = dis_matrix[id1][id2];
        }
    // double maxx_dis = 0;
    // for(int i=1;i<=n;i++) maxx_dis=max(maxx_dis, dis[0][i] + dis[i][0]);
    // cout<<"maxx_dis = " << maxx_dis << endl;
    // exit(0);
    for(int i = 0; i < speed_cnt; i++)
    {
        cin >> trash >> trash; // [Speed id]
        double last_speed = 0, last_time = 0;
        cin >> last_speed;
        double StartTime, EndTime, FloatNumber, Speed;
        for(int j = 1; j <= 6; j++)
        {
            cin >> StartTime >> EndTime >> FloatNumber >> Speed;
            double a = (Speed - last_speed) / (StartTime - last_time);
            speed[i].push_back((vode){last_time, last_speed, a});
            speed[i].push_back((vode){StartTime, Speed, 0});
            last_time = EndTime;
            last_speed = Speed;
        }
    }
    cin >> trash >> trash >> trash; // [speed choose matrix]
    for(int i = 0; i <= n; i++)
        for(int j = 0; j <= n; j++)
            cin >> speed_id[i][j];
    cin.close();
}

inline bool local_search1(Solution &solution) // swap
{
    for(int i = 0; i < (int)solution.routes.size(); i++)
    {
        if(!(int)solution.routes[i].size()) continue;
        double w1 = get_route_info(solution.routes[i]).ec;
        for(int j = i + 1; j < (int)solution.routes.size(); j++)
        {
            double w2 = get_route_info(solution.routes[j]).ec;
            for(int k1 = 0; k1 < (int)solution.routes[i].size(); k1++)
                for(int k2 = 0; k2 < (int)solution.routes[j].size(); k2++)
                {
                    vector<int> tmp1 = solution.routes[i];
                    vector<int> tmp2 = solution.routes[j];
                    swap(tmp1[k1], tmp2[k2]);
                    if(get_route_info(tmp1).ec + get_route_info(tmp2).ec < w1 + w2)
                    {
                        swap(solution.routes[i][k1], solution.routes[j][k2]);
                        return true;
                    }
                }
        }
    }
    return false;
}
inline bool local_search2(Solution &solution) // reverse
{
    for(auto &route : solution.routes)
    {
        if((int)route.size() <= 1) continue;
        double w1 = get_route_info(route).ec;
        for(int k1 = 0; k1 < (int)route.size(); k1++)
            for(int k2 = k1 + 1; k2 < (int)route.size(); k2++)
            {
                vector<int> tmp = route;
                reverse(tmp.begin() + k1, tmp.begin() + k2 + 1);
                double w2 = get_route_info(tmp).ec;
                if(w2 < w1) 
                {
                    reverse(route.begin() + k1, route.begin() + k2 + 1);
                    return true;
                } 
            }
    }
    return false;
}
inline bool local_search3(Solution &solution) // relocate
{
    for(int i = 0; i < (int)solution.routes.size(); i++)
    {
        if(!(int)solution.routes[i].size()) continue;
        double w1 = get_route_info(solution.routes[i]).ec;
        for(int j = 0; j < (int)solution.routes.size(); j++)
        {
            if(j == i) continue;
            double w2 = get_route_info(solution.routes[j]).ec;
            for(int k1 = 0; k1 < (int)solution.routes[i].size(); k1++)
                for(int k2 = 0; k2 <= (int)solution.routes[j].size(); k2++)
                {
                    vector<int> tmp1 = solution.routes[i];
                    vector<int> tmp2 = solution.routes[j];
                    int k = tmp1[k1];
                    tmp1.erase(tmp1.begin() + k1);
                    tmp2.insert(tmp2.begin() + k2, k);
                    if(get_route_info(tmp1).ec + get_route_info(tmp2).ec < w1 + w2)
                    {
                        solution.routes[i].erase(solution.routes[i].begin() + k1);
                        solution.routes[j].insert(solution.routes[j].begin() + k2, k);
                        return true;
                    }
                }
        }
    }
    return false;
}
inline bool local_search4(Solution &solution, bool flag) // abswap & abrex
{
    for(int i = 0; i < (int)solution.routes.size(); i++)
    {
        if((int)solution.routes[i].size() < 2) continue;
        double w1 = get_route_info(solution.routes[i]).ec;
        for(int j = 0; j < (int)solution.routes.size(); j++)
        {
            if(j == i || (int)solution.routes[j].size() < 2) continue;
            double w2 = get_route_info(solution.routes[j]).ec;
            for(int len = 2; len <= min((int)solution.routes[i].size(), (int)solution.routes[j].size()); len++)
                for(int l1 = 0; l1 + len - 1 < (int)solution.routes[i].size(); l1++)
                    for(int l2 = 0; l2 + len - 1 < (int)solution.routes[j].size(); l2++)
                    {
                        int r1 = l1 + len - 1;
                        int r2 = l2 + len - 1;
                        vector<int> tmp1 = solution.routes[i];
                        vector<int> tmp2 = solution.routes[j];
                        vector<int> p1, p2;
                        for(int k = l1; k <= r1; k++) p1.push_back(solution.routes[i][k]); 
                        for(int k = l2; k <= r2; k++) p2.push_back(solution.routes[j][k]);
                        if(flag) reverse(p2.begin(), p2.end());
                        tmp1.erase(tmp1.begin() + l1, tmp1.begin() + r1 + 1);
                        tmp2.erase(tmp2.begin() + l2, tmp2.begin() + r2 + 1);
                        // tmp2.insert(tmp2.begin() + l2, p1.begin(), p1.end());
                        // tmp1.insert(tmp1.begin() + l1, p2.begin(), p2.end());
                        while(p1.size()) tmp2.insert(tmp2.begin() + l2, p1.back()), p1.pop_back();
                        while(p2.size()) tmp1.insert(tmp1.begin() + l1, p2.back()), p2.pop_back();
                        if(get_route_info(tmp1).ec + get_route_info(tmp2).ec < w1 + w2)
                        {
                            for(int k = l1; k <= r1; k++) p1.push_back(solution.routes[i][k]); 
                            for(int k = l2; k <= r2; k++) p2.push_back(solution.routes[j][k]);
                            if(flag) reverse(p2.begin(), p2.end());
                            solution.routes[i].erase(solution.routes[i].begin() + l1, solution.routes[i].begin() + r1 + 1);
                            solution.routes[j].erase(solution.routes[j].begin() + l2, solution.routes[j].begin() + r2 + 1);
                            while(p1.size()) solution.routes[j].insert(solution.routes[j].begin() + l2, p1.back()), p1.pop_back();
                            while(p2.size()) solution.routes[i].insert(solution.routes[i].begin() + l1, p2.back()), p2.pop_back();
                            return true;
                        }
                    }
        }
    }
    return false;
}

int tmp_id[N];
inline void update_route(vector<int> &route)
{
    vector<int> ans, tmp;
    double minn = inf;
    int cnt = (int)route.size();
    // if(cnt == 8)
    // {
    //     double t1 = clock();
    //     int tot = 1;
    //     for(int i=1;i<=cnt;i++) tot*=i;
    //     for(int i = 1; i < 125 * tot; i++)
    //     {
    //         tmp.resize(cnt);
    //         for(int i = 0; i < cnt; i++) 
    //             tmp[i] = route[i];
    //         double val = get_route_info(tmp).ec;
    //         // printf("val = %.10f\n", val);
    //     }
    //     double t2 = clock();
    //     printf("time = %.10f\n", (t2 - t1) / CLOCKS_PER_SEC);
    //     exit(0);
    // }
    if(cnt <= 1 || cnt > 8) return;
    ans.resize(cnt);
    tmp.resize(cnt);
    for(int i = 0; i < cnt; i++) 
        tmp_id[i] = i;
    do
    {
        for(int i = 0; i < cnt; i++) 
            tmp[i] = route[tmp_id[i]];
        double val = get_route_info(tmp).ec;
        if(val < minn)
        {
            minn = val;
            ans = tmp;
        }
    } 
    while (next_permutation(tmp_id, tmp_id + cnt));
    route = ans;
}
inline void local_search(Solution &solution)
{
    int tot = 0;
    while(true)
    {
        tot++;
        // printf("tot = %d\n", tot);
        bool flag = false;
        if(local_search1(solution)) flag = true;
        if(local_search2(solution)) flag = true;
        if(local_search3(solution)) flag = true;
        if(local_search4(solution, false)) flag = true;
        if(local_search4(solution, true)) flag = true;
        if(!flag || tot > 100) break;
        // if(!flag) break;
        // solution.update_ec();
        // cout<<solution.ec<<endl;
    }
    for(auto &route : solution.routes) update_route(route);
    solution.update();
}

// int zzr[] = {21, 24, 7, 3, 5, 4, 10, 14, 19, 6, 20, 13, 2, 8, 28, 9, 30, 29, 17, 1, 26, 12, 16, 11, 15, 25, 23, 22, 18, 27};
inline Solution init()
{
    Solution ans;
    for(int i = 1; i <= n; i++) tmp_id[i] = i;
    random_shuffle(tmp_id + 1, tmp_id + n + 1);
    // for(int i = 1; i <= n; i++) tmp_id[i] = zzr[i-1];
    int pos = 1;
    vector<int> route;
    while(pos <= n)
    {
        int lef = pos, rig = n;
        while(lef < rig)
        {
            int mid = (lef + rig + 1) / 2;
            vector<int> tmp;
            for(int i = pos; i <= mid; i++) tmp.push_back(tmp_id[i]);
            if(get_route_info(tmp).ec < inf) lef = mid;
            else rig = mid - 1;
        }
        route.clear();
        for(int i = pos; i <= lef; i++) route.push_back(tmp_id[i]);
        ans.routes.push_back(route);
        pos = lef + 1;
    }
    while((int)ans.routes.size() < VehicleNumber) 
    {
        // cout << "current size = " << ans.routes.size() << endl;
        vector<int> route;
        ans.routes.push_back(route);
        // cout << "route added" << endl;
    }
    local_search(ans);
    ans.update();
    return ans;
}

inline int random(int l, int r)
{
    return rand() % (r - l + 1) + l;
}

const double const_e1 = 0.27;
const double const_e2 = 1.45;
vector<int> insert_ids;
struct tode{
    int id;
    double similarity;
};
priority_queue<tode> q;
inline bool operator < (tode x, tode y)
{
    return x.similarity > y.similarity;
}

bool vis[N];
inline void LNS_remove(Solution &solution, int cnt)
{
    int opt = random(0, 4);
    if(opt == 0)
    {
        for(int i=1; i<=n; i++) vis[i] = false;
        while(cnt--)
        {
            int remove_id;
            while(true)
            {
                remove_id = random(1, n);
                if(vis[remove_id]) continue;
                vis[remove_id] = true;
                break;
            }
            insert_ids.push_back(remove_id);
            for(auto &route : solution.routes)
            {
                bool flag = false;
                for(int i = 0; i < (int)route.size(); i++)
                    if(route[i] == remove_id)
                    {
                        route.erase(route.begin() + i);
                        flag = true;
                        break;
                    }
                if(flag) break;
            }
        }
    }
    else if (opt == 1)
    {
        while(cnt--)
        {
            double maxx = -1e9;
            int node_id = -1, route_id = -1, pickup_id = -1;
            for(int i = 0; i < (int)solution.routes.size(); i++)
            {
                vector<int> route = solution.routes[i];
                for(int j = 0; j < (int)route.size(); j++)
                {
                    int pre = 0, nex = 0, cur = route[j];
                    if(j > 0) pre = route[j - 1];
                    if(j < (int)route.size() - 1) nex = route[j + 1]; 
                    double dis_delta = dis[pre][cur] + dis[cur][nex] - dis[pre][nex];
                    if(dis_delta > maxx) maxx = dis_delta, route_id = i, node_id = j, pickup_id = cur;
                }
            }   
            solution.routes[route_id].erase(solution.routes[route_id].begin() + node_id);
            insert_ids.push_back(pickup_id);
        }   
    }
    else if (opt == 2)
    {
        while(cnt--)
        {
            double maxx = -1e9;
            int node_id = -1, route_id = -1, pickup_id = -1;
            for(int i = 0; i < (int)solution.routes.size(); i++)
            {
                vector<int> route = solution.routes[i];
                for(int j = 0; j < (int)route.size(); j++)
                {
                    int cur = route[j];
                    double val = pickups[cur].demand * const_e1 + j;
                    if(val > maxx) maxx = val, route_id = i, node_id = j, pickup_id = cur;
                }
            }   
            solution.routes[route_id].erase(solution.routes[route_id].begin() + node_id);
            insert_ids.push_back(pickup_id);
        }
    }
    else if (opt == 3)
    {
        while(cnt--)
        {
            double maxx = -1e9;
            int node_id = -1, route_id = -1, pickup_id = -1;
            for(int i = 0; i < (int)solution.routes.size(); i++)
            {
                double pre_ec = get_route_info(solution.routes[i]).ec; 
                for(int j = 0; j < (int)solution.routes[i].size(); j++)
                {
                    vector<int> route = solution.routes[i];
                    route.erase(route.begin() + j);
                    double cur_ec = get_route_info(route).ec;
                    double val = pre_ec - cur_ec;
                    if(val > maxx) maxx = val, route_id = i, node_id = j, pickup_id = solution.routes[i][j];
                }
            }   
            solution.routes[route_id].erase(solution.routes[route_id].begin() + node_id);
            insert_ids.push_back(pickup_id);
        }
    }
    else
    {
        for(int i=1; i<=n; i++) vis[i] = false;
        while(q.size()) q.pop();
        int init = random(1, n);
        q.push((tode){init, 0});
        while(cnt--)
        {
            tode tmp = q.top();
            q.pop();
            int remove_id = tmp.id;
            if(vis[remove_id]) continue;
            vis[remove_id] = true;
            insert_ids.push_back(remove_id);
            bool flag = false; 
            for(auto &route : solution.routes)
            {
                for(int i = 0; i < (int)route.size(); i++)
                    if(route[i] == remove_id)
                    {
                        route.erase(route.begin() + i);
                        flag = true;
                        break;
                    }
                if(flag) break; 
            }     
            for(int i = 1; i <= n; i++)
            {
                if(vis[i]) continue;
                double similarity = dis[i][remove_id] + const_e2 * abs(pickups[remove_id].demand - pickups[i].demand);
                q.push((tode){i, similarity});
            }
        }
    }
}

inline void LNS_insert(Solution &solution)
{
    // for(auto k : insert_ids) cout << k << " ";
    // cout<<endl;
    // cout << "route number = " << solution.routes.size() << endl;
    int opt = random(0, 3);
    // cout << "opt = " << opt << endl;
    // if(insert_ids.size() > 25) 
    // {
    //     cout<<(int)insert_ids.size()<<endl;
    // }
    //if((int)insert_ids.size() >= 25) cout << (int)insert_ids.size() << endl;
    // assert((int)insert_ids.size() < n);
    if(opt == 0)
    {
        random_shuffle(insert_ids.begin(), insert_ids.end());
        while(insert_ids.size())
        {
            int id = insert_ids.back();
            insert_ids.pop_back();
            double minn = 1e9;
            int route_id = -1, node_id = -1;
            for(int i = 0; i < (int)solution.routes.size(); i++)
            {
                double pre_ec = get_route_info(solution.routes[i]).ec; 
                for(int j = 0; j <= (int)solution.routes[i].size(); j++)
                {
                    vector<int> route = solution.routes[i];
                    route.insert(route.begin() + j, id);
                    double cur_ec = get_route_info(route).ec;
                    double val = cur_ec - pre_ec;
                    if(val < minn) minn = val, route_id = i, node_id = j;
                }
            }   
            solution.routes[route_id].insert(solution.routes[route_id].begin() + node_id, id);
        }
    }
    else if(opt == 1)
    {
        // cout<<"yes"<<endl;
        while(insert_ids.size())
        {
            double minn = 1e9;
            int route_id = -1, node_id = -1, pickup_id = -1;
            for(auto id : insert_ids)
            {
                for(int i = 0; i < (int)solution.routes.size(); i++)
                {
                    double pre_ec = get_route_info(solution.routes[i]).ec; 
                    for(int j = 0; j <= (int)solution.routes[i].size(); j++)
                    {
                        vector<int> route = solution.routes[i];
                        route.insert(route.begin() + j, id);
                        double cur_ec = get_route_info(route).ec;
                        double val = cur_ec - pre_ec;
                        if(val < minn) minn = val, route_id = i, node_id = j, pickup_id = id;
                    }
                }  
            } 
            solution.routes[route_id].insert(solution.routes[route_id].begin() + node_id, pickup_id);
            for(int i = 0; i < (int)insert_ids.size(); i++)
                if(insert_ids[i] == pickup_id) 
                {
                    insert_ids.erase(insert_ids.begin() + i);
                    break;
                }
        }
        // cout<<"no"<<endl;
    }
    else if(opt == 2 || opt == 3)
    {
        // cout << "opt = " << opt << endl;
        while(insert_ids.size())
        {
            // for(auto k : insert_ids) cout << k << " ";
            // cout << endl;
            double maxx = -1e9, minn = 1e9;
            int pickup_id = -1;
            for(auto id : insert_ids)
            {
                // cout << "id = " << id << endl;
                vector<int> delta_ec;
                for(int i = 0; i < (int)solution.routes.size(); i++)
                {
                    double pre_ec = get_route_info(solution.routes[i]).ec; 
                    for(int j = 0; j <= (int)solution.routes[i].size(); j++)
                    {
                        vector<int> route = solution.routes[i];
                        route.insert(route.begin() + j, id);
                        double cur_ec = get_route_info(route).ec;
                        delta_ec.push_back(cur_ec - pre_ec);
                    }
                }  
                sort(delta_ec.begin(), delta_ec.end());
                double val = 0;
                for(int i = 1; i < opt; i++) val += (delta_ec[i] - delta_ec[0]);
                if(val > maxx || (val == maxx && delta_ec[0] < minn)) maxx = val, minn = delta_ec[0], pickup_id = id;
            } 
            // cout << "1" << endl;
            minn = 1e9;
            int route_id = -1, node_id = -1;
            for(int i = 0; i < (int)solution.routes.size(); i++)
            {
                double pre_ec = get_route_info(solution.routes[i]).ec; 
                for(int j = 0; j <= (int)solution.routes[i].size(); j++)
                {
                    vector<int> route = solution.routes[i];
                    route.insert(route.begin() + j, pickup_id);
                    double cur_ec = get_route_info(route).ec;
                    double val = cur_ec - pre_ec;
                    if(val < minn) minn = val, route_id = i, node_id = j;
                }
            }  
            solution.routes[route_id].insert(solution.routes[route_id].begin() + node_id, pickup_id);
            for(int i = 0; i < (int)insert_ids.size(); i++)
                if(insert_ids[i] == pickup_id) 
                {
                    insert_ids.erase(insert_ids.begin() + i);
                    break;
                }
            // assert(flag);
            // cout << "pickup_id = " << pickup_id << endl;
            // cout << "2" << endl;
        }
    }
}

double tmp_ec[M + 5];
bool ignoreFlag[M + 5];
GRBVar var[M + 5];
GRBLinExpr constraints[N];

inline bool check_worse(int i, int j)
{
    if((int)route_ids[i].size() != (int)route_ids[j].size()) return false;
    // int pos = 0;
    // for(auto k : route_ids[i])
    // {
    //     while(pos < (int)route_ids[j].size() && route_ids[j][pos] != k) pos++;
    //     if(pos == (int)route_ids[j].size()) return false; 
    //     pos++;
    // }
    for(int k = 0; k < (int)route_ids[i].size(); k++)
        if(route_ids[i][k] != route_ids[j][k])
            return false;
    // return true;
    // return false;
    return (tmp_ec[i] > tmp_ec[j] + 1e-3);
}

int tmp_cnt[N];
inline bool check_route(vector<vector<int> >routes)
{
    memset(tmp_cnt, 0, sizeof(tmp_cnt));
    for(auto route : routes)
        for(auto k : route)
            tmp_cnt[k]++;
    for(int i = 1; i <= n; i++)
        if(tmp_cnt[i] != 1) 
            return false;
    return true;
}

inline Solution SPP()
{
    Solution ans;
    route_ids = route_pool;
    int cnt = (int)route_pool.size();
    // cout<<"cnt="<<cnt<<endl;
    for(int i = 0; i < cnt; i++) tmp_ec[i] = get_route_info(route_pool[i]).ec, ignoreFlag[i] = false;
    // for(int i = 0; i < cnt; i++) sort(route_ids[i].begin(), route_ids[i].end());
    // cout<<"begin!"<<endl;
    // for(int i = 0; i < cnt; i++) 
    //     for(int j = 0; j < cnt; j++)
    //     {
    //         if(j == i || ignoreFlag[j]) continue;
    //         if(check_worse(i, j)) 
    //         {
    //             ignoreFlag[i] = true;
    //             break;
    //         }
    //     }
    // cout<<"hello"<<endl;

    int tot = 0;
    candidate_routes.clear();
    for(int i = 0; i < cnt; i++)
        if(!ignoreFlag[i])
        {
            tmp_ec[tot] = tmp_ec[i];
            tot++;
            candidate_routes.push_back(route_pool[i]);
        }
    cnt = tot;

    // cout<<"yes"<<endl;
    // exit(0);
    
    try {
        // Create an environment
        GRBEnv env = GRBEnv(true);
        env.set("LogFile", "zzr.log");
        env.start();
        // Create an empty model
        GRBModel model = GRBModel(env);
        model.set(GRB_IntParam_Threads, 8);  // 设置线程数为 8
        // ///time limit
        model.set(GRB_DoubleParam_TimeLimit, 720.0);
        // Create variables
        for(int i = 0; i < cnt; i++) var[i] = model.addVar(0.0, 1.0, 0.0, GRB_BINARY);
        // Set objective
        GRBLinExpr obj = 0.0;
        for(int i = 0; i < cnt; i++) 
            obj += tmp_ec[i] * var[i];
        model.setObjective(obj, GRB_MINIMIZE);
        // Add constraints
        for(int i = 1; i <= n; i++) constraints[i] = 0.0;
        for(int i = 0; i < cnt; i++) 
            for(auto k : candidate_routes[i])
                constraints[k] += var[i];
        for(int i = 1; i <= n; i++)
            model.addConstr(constraints[i] == 1.0);
        // Optimize model
        model.optimize();
        for(int i = 0; i < cnt; i++)
            if(var[i].get(GRB_DoubleAttr_X) == 1.0)
                ans.routes.push_back(candidate_routes[i]);
    } catch(GRBException e) {
        cout << "Error code = " << e.getErrorCode() << endl;
        cout << e.getMessage() << endl;
    } catch(...) {
        cout << "Exception during optimization" << endl;
    }
    ans.update();
    if(!check_route(ans.routes))
    {
        cout<<"bomb!"<<endl;
        // for(int i = 0; i < cnt; i++)
        // {
        //     for(auto k : candidate_routes[i]) cout << k << " ";
        //     cout << endl;
        //     cout << "ec = " << tmp_ec[i];
        //     cout << endl;
        // }
        // cout << "=========================" << endl;
        
        // for(auto route : ans.routes)
        // {
        //     for(auto k : route) cout << k << " ";
        //     cout << endl;
        // }

        // cout << "=========================" << endl;

        // for(int i = 0; i < cnt; i++)
        // {
        //     if(abs(var[i].get(GRB_DoubleAttr_X) - 1.0) < eps) 
        //     {
        //         for(auto k : candidate_routes[i]) cout << k << " ";
        //         cout << endl;
        //     }
        // }
        assert(false);
    }
    return ans;
}

const double r_min = 0.23;
const double r_max = 0.85;
const double const_e = 0.02;
inline Solution LNS()
{
    double start_time = clock();
    Solution cur_solution = init();
    // cout<<"initial solution:"<<endl;
    // double distance = 0;
    // int route_cnt=0;
    // for(auto route : cur_solution.routes)
    // {
    //     if(!route.size()) continue;
    //     cout<<"======================="<<endl;
    //     route_cnt++;
    //     printf("routeId = %d\n", route_cnt);
    //     for(auto k : route) 
    //     {
    //         cout<<k<<" ";
    //     }
    //     cout << endl;
    //     RouteInfo val = get_route_info(route);
    //     cout << "ec = " << val.ec << endl;
    //     cout << "dis = " << val.total_dis << endl;
    // }
    printf("energy consumption = %.10f\n", cur_solution.ec);
    cout<<"init completed"<<endl;

    for(auto route : cur_solution.routes)
        if((int)route_pool.size() < 8000)
            route_pool.push_back(route);
    // exit(0);
    
    int fail_count = 0;
    int iterations = 0;
    while(true)
    {
        iterations++;
        cout<<endl;
        cout<<"==========================================="<<endl;
        printf("running on iteration %d:\n", iterations);
        printf("current ec = %.10f\n", cur_solution.ec);
        printf("current total_time = %.10f\n", cur_solution.total_time);
        printf("current total_dis = %.10f\n", cur_solution.total_dis);

        int cnt_max = min(r_max, r_min + const_e * fail_count) * n;
        int cnt_min = r_min * n;
        int cnt = random(cnt_min, cnt_max);
        cnt = min(cnt, 200);
        printf("remove/insert cnt = %d\n",cnt);

        Solution tmp_solution = cur_solution;
        if(!check_route(tmp_solution.routes))
        {
            cout<<"bomb1!"<<endl;
            assert(false);
        }
        // for(auto route : tmp_solution.routes)
        // {
        //     for(auto k : route) cout << k << " ";
        //     cout<<endl;
        // }
        cout<<"running on LNS_remove"<<endl;
        LNS_remove(tmp_solution, cnt);
        cout<<"remove completed"<<endl;

        cout<<"running on LNS_insert"<<endl;
        LNS_insert(tmp_solution);
        cout<<"insert completed"<<endl;
        
        if(!check_route(tmp_solution.routes))
        {
            cout<<"bomb2!"<<endl;
            assert(false);
        }
        tmp_solution.update();
        for(auto route : tmp_solution.routes)
            if((int)route_pool.size() < 8000)
                route_pool.push_back(route);
        if(tmp_solution.ec < 1.25 * cur_solution.ec) 
        {
            cout<<"running local search"<<endl;
            local_search(tmp_solution);
            cout<<"local search completed"<<endl;
            if(!check_route(tmp_solution.routes))
            {
                cout<<"bomb3!"<<endl;
                assert(false);
            }
            for(auto route : tmp_solution.routes)
                if((int)route_pool.size() < 8000)
                    route_pool.push_back(route);
        }
        else if(iterations % 5 == 0)
        {
            cout<<"running local search"<<endl;
            local_search(tmp_solution);
            cout<<"local search completed"<<endl;
            if(!check_route(tmp_solution.routes))
            {
                cout<<"bomb3!"<<endl;
                assert(false);
            }
            for(auto route : tmp_solution.routes)
                if((int)route_pool.size() < 8000)
                    route_pool.push_back(route);
        }

        if(tmp_solution.ec < cur_solution.ec)
        {
            fail_count = 0;
            cur_solution = tmp_solution;
        }
        else fail_count++;

        double cur_time = clock();
        if((cur_time - start_time) / CLOCKS_PER_SEC > time_limit) break;
        if(iterations >= 10 * n) break;
        if((int)route_pool.size() >= 8000)
        {
            cout<<"running SPP"<<endl;
            tmp_solution = SPP();
            cout<<"SPP completed"<<endl;
            if(tmp_solution.ec < cur_solution.ec) cur_solution = tmp_solution;
            route_pool.clear();
            for(auto route : cur_solution.routes)
                if((int)route_pool.size() < 8000)
                    route_pool.push_back(route);
        }
    }
    return cur_solution;
}

int main(int argc, char* argv[])
{
    double start_time = clock();
    srand(40);
    if (argc < 2) {
        cout << "Usage: " << argv[0] << " <data_file_path>" << endl;
        return 1;
    }
    data_file = argv[1];  // 从命令行参数获取数据文件路径
    read_data();
    Solution ans = LNS();
    cout<<endl;
    cout<<"==========================================="<<endl;
    int tot = 0;
    for(auto route : ans.routes)
    {
        if(!route.size()) continue;
        tot++;
        printf("Route%d: ", tot);
        for(auto k : route) printf("%d ", k);        
        printf("\n");       
    }
    ans.update();
    printf("energy consumption = %.10f\n", ans.ec);
    printf("total time = %.10f\n", ans.total_time);
    printf("total distance = %.10f\n", ans.total_dis);
    double end_time = clock();
    printf("running time = %.10f\n", (end_time - start_time) / CLOCKS_PER_SEC);
    return 0;
}