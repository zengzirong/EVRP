VehicleNumber
VechicleCapacity
Electricity

[Node]
Integer Integer Integer Integer Integer
CustomerNum Integer Integer Integer Integer

[pickup]
PickupId CustomerId Demand ServeTime
...

[Speed id]
InitialSpeed
StartTime EndTime FloatNumber Speed
...

[speed choose matrix]
(describes the chosen speed id)

compiling commands:
GUROBI_HOME="/Library/gurobi1200/macos_universal2/"
clang++ seed=10_main.cpp -I${GUROBI_HOME}/include/ -L${GUROBI_HOME}/lib -lgurobi_c++ -lgurobi120 -o seed=10_main
clang++ seed=20_main.cpp -I${GUROBI_HOME}/include/ -L${GUROBI_HOME}/lib -lgurobi_c++ -lgurobi120 -o seed=20_main
clang++ seed=30_main.cpp -I${GUROBI_HOME}/include/ -L${GUROBI_HOME}/lib -lgurobi_c++ -lgurobi120 -o seed=30_main
clang++ seed=40_main.cpp -I${GUROBI_HOME}/include/ -L${GUROBI_HOME}/lib -lgurobi_c++ -lgurobi120 -o seed=40_main
clang++ seed=50_main.cpp -I${GUROBI_HOME}/include/ -L${GUROBI_HOME}/lib -lgurobi_c++ -lgurobi120 -o seed=50_main
clang++ NO_LS.cpp -I${GUROBI_HOME}/include/ -L${GUROBI_HOME}/lib -lgurobi_c++ -lgurobi120 -o NO_LS
./main <data_file_path>





