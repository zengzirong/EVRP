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
clang++ main.cpp -I${GUROBI_HOME}/include/ -L${GUROBI_HOME}/lib -lgurobi_c++ -lgurobi120 -o main
./main <data_file_path>





