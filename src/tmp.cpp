#include<bits/stdc++.h>
using namespace std;

int main() 
{
    for (auto file : filesystem::directory_iterator("../dataset")) {
        string str = file.path().filename();
        int len = str.length();
        string s = "";
        //if(str[2] == '1') continue;
        for(int i = 0; i < len; i++)
        {
            if(str[i] == '.')
            {
                s = s + "_result.txt";
                break;
            }
            else 
            {
                s = s + str[i];
            }
        }
        cout<<"./main datasetEVRP/" << str << " > ../large_result/srand_100/" << s << endl;
    }

    // string s1[] = {"Q=3000_200_1", "Q=3000_400_1", "Q=3000_600_1", "Q=3000_800_1", "Q=3000_1000_1"};
    // string s2[] = {"LS_SPP_600", "LS_SPP_900"};
    // for(int i=0;i<2;i++)
    //     for(int j=0;j<5;j++)
    //     {
    //         cout<<"./"<<s2[i]<<" datasetEVRP/"<<s1[j]<<".txt > ../compare_result/"<<s1[j]<<"_"<<s2[i]<<"_result.txt"<<endl;
    //     }
    // return 0;

    // for(int seed = 10; seed <= 100; seed += 10)
    // {
    //     for (auto file : filesystem::directory_iterator("../cola_new")) 
    //     {
    //         string str = file.path().filename();
    //         if(str[0] < '0' || str[0] > '9') continue;
    //         int len = str.length();
    //         string s = "";
    //         // if(str[2] == '1') continue;
    //         for(int i = 0; i < len; i++)
    //         {
    //             if(str[i] == '.')
    //             {
    //                 s = s + "_result.txt";
    //                 break;
    //             }
    //             else 
    //             {
    //                 s = s + str[i];
    //             }
    //         }
    //         cout<<"./main_"<<seed<<" cola_new/"<<str<<" > ../small_result/srand_"<<seed<<"/"<<s<<endl; 
    //     }   
    // }
}