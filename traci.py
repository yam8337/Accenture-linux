import sumolib
from sumolib import checkBinary
import traci

sumo_binary = checkBinary('sumo')
sumo_file = "../../artery/scenarios/city_police/city.sumocfg"
traci.start([sumo_binary,"-c",sumo_file])

vehicle_id = "emv1"
final_desitination = (70,0)

initial_time= None

while True:
    if vehicle_id in traci.vehicle.getIDList() and initial_time is None:
        initial_time = traci.simulation.getTime()
        print("Entering velocity for EMV = ", traci.vehicle.getSpeed(vehicle_id))

    vehicle_position = traci.vehicle.getPosition(vehicle_id)
    
    local_time = traci.simulation.getTime()
    if local_time % 3 == 0:
        print(local_time)
        for veh in traci.vehicle.getIDList():
            speed = traci.vehicle.getSpeed(veh)
            print(veh,"{:.2f}".format(speed))
        

    distance = (final_desitination[0]-vehicle_position[0])
                    
    if vehicle_id in traci.vehicle.getIDList() and distance <= 0.5 :
        print( "EMV location", traci.vehicle.getPosition(vehicle_id))
        break

    traci.simulationStep()

end_time = traci.simulation.getTime()
total_time = end_time - initial_time

print("Time required", total_time)

traci.close()
