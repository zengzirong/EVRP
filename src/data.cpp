#include <bits/stdc++.h>
using namespace std;

inline int random(int l, int r)
{
    return rand() % (r - l + 1) + l;
}

int VehicleNumber = 1000;
double VechicleCapacity = 1000, Electricity = 1000;
double trash = 0;

const int N = 2000 + 5;
int len = 0, re[N];
bool vis[N];

inline void prework()
{
    ifstream cin;
    cin.open("../cola_new/Customer2ID.txt");
    int customer_id, node_id;
    while (cin >> customer_id >> node_id)
    {
        if(customer_id != 0)
        re[++len] = customer_id;
    }
    cin.close();
}

int main()
{
    srand(time(0));

    prework();

    cout << VehicleNumber << endl;
    cout << VechicleCapacity << endl;
    cout << Electricity << endl;
    cout << endl;

    cout << "[Node]" << endl;
    for (int i = 1; i <= 10; i++)
    {
        cout << trash;
        if (i == 5 || i == 10)
            cout << endl;
        else
            cout << " ";
    }
    cout << endl;

    cout << "[pickup]" << endl;
    for (int i = 1; i <= VehicleNumber; i++)
    {
        int PickupId = i;
        int CustomerId;
        double Demand;
        while (true)
        {
            int k = random(1, len);
            if (vis[k])
                continue;
            vis[k] = true;
            CustomerId = re[k];
            break;
        }
        Demand = random(VechicleCapacity * 0.1, VechicleCapacity * 0.8);
        cout << PickupId << " " << CustomerId << " " << Demand << " " << trash << endl;
    }
    cout << endl;

    cout << "[Speed 0]" << endl;
    cout << "0.81" << endl;
    cout << "30.0 60.0 0.0 0.6" << endl;
    cout << "90.0 150 0.0 0.4" << endl;
    cout << "300.0 540.0 0.0 0.81" << endl;
    cout << "570.0 630.0 0.0 0.6" << endl;
    cout << "660.0 720.0 0.0 0.4" << endl;
    cout << "750.0 840.0 0.0 0.81" << endl;
    cout << endl;

    cout << "[Speed 1]" << endl;
    cout << "1.33" << endl;
    cout << "30.0 60.0 0.0 0.8" << endl;
    cout << "90.0 150 0.0 0.6" << endl;
    cout << "300.0 540.0 0.0 1.33" << endl;
    cout << "570.0 630.0 0.0 0.8" << endl;
    cout << "660.0 720.0 0.0 1.3" << endl;
    cout << "750.0 840.0 0.0 2" << endl;
    cout << endl;

    cout << "[Speed 2]" << endl;
    cout << "1.33" << endl;
    cout << "30.0 60.0 0.0 1.0" << endl;
    cout << "90.0 150 0.0 0.8" << endl;
    cout << "300.0 540.0 0.0 1.33" << endl;
    cout << "570.0 630.0 0.0 0.8" << endl;
    cout << "660.0 720.0 0.0 0.6" << endl;
    cout << "750.0 840.0 0.0 1.5" << endl;
    cout << endl;

    cout << "[Speed 3]" << endl;
    cout << "1.5" << endl;
    cout << "30.0 60.0 0.0 0.9" << endl;
    cout << "90.0 150 0.0 0.8" << endl;
    cout << "300.0 540.0 0.0 1.5" << endl;
    cout << "570.0 630.0 0.0 0.9" << endl;
    cout << "660.0 720.0 0.0 0.8" << endl;
    cout << "750.0 840.0 0.0 1.5" << endl;
    cout << endl;

    cout << "[Speed 4]" << endl;
    cout << "2" << endl;
    cout << "30.0 60.0 0.0 1.1" << endl;
    cout << "90.0 150 0.0 0.9" << endl;
    cout << "300.0 540.0 0.0 2" << endl;
    cout << "570.0 630.0 0.0 1.1" << endl;
    cout << "660.0 720.0 0.0 0.9" << endl;
    cout << "750.0 840.0 0.0 2" << endl;
    cout << endl;

    cout << "[speed choose matrix]" << endl;
    for (int i = 0; i <= VehicleNumber; i++)
    {
        int speed;
        for (int j = 0; j <= VehicleNumber; j++)
        {
            if (i == 0 || j == 0)
                speed = 4;
            else
                speed = random(0, 4);
            if (j == VehicleNumber)
                cout << speed << endl;
            else
                cout << speed << " ";
        }
    }
    srand(time(0));
}