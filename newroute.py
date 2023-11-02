import os
from sumolib import checkBinary
import traci
import numpy as np
import matplotlib.pyplot as plt

class EMV():
    def __init__(self):
        self.timestamps = []
        self.velocities = []
        self.emv_data ={}
        self.veh_id_list = []
        self.tls_info_list = []
        self.vehicle_type_list = []


    def start_simulation(self):
            sumo_binary = checkBinary('sumo')
            #sumo_file = "../../artery/scenarios/NewRoute/osm.sumocfg"
            sumo_file = "../../InTAS/scenario/InTAS.sumocfg"
            traci.start([sumo_binary, "-c", sumo_file])
            #traci.simulationStep()

    def close_simulation(self):
            traci.close()

    def run_simulation(self):
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            
            self.collect_emv_velocity_data()

        return self.emv_data
    
    
    def collect_emv_velocity_data(self):
        # Get list of all vehicles in the simulation
        self.all_vehicles = traci.vehicle.getIDList()
        
        
        """ for vehicle_id in self.all_vehicles:
            vehicles_type = traci.vehicle.getTypeID(vehicle_id)
            if vehicles_type not in self.vehicle_type_list:
                self.vehicle_type_list.append(vehicles_type)
                print(vehicles_type) """
            
            

        # Initialize a dictionary to store velocity data for each EMV

        for vehicle_id in self.all_vehicles:
            #if traci.vehicle.getTypeID(vehicle_id) == 'emergency_veh' :
            if vehicle_id.startswith('emv'):
                # Get the velocity of the vehicle at the current simulation time
                velocity = traci.vehicle.getSpeed(vehicle_id)

                self.get_TLS_info(vehicle_id)
                
                # Get the current simulation time
                sim_time = traci.simulation.getTime()
                print(sim_time,vehicle_id)

                # Check if the EMV is already in the dictionary
                if vehicle_id in self.emv_data:
                    self.emv_data[vehicle_id]['time_stamps'].append(sim_time)
                    self.emv_data[vehicle_id]['velocities'].append(velocity)
                else:
                    self.emv_data[vehicle_id] = {'time_stamps': [sim_time], 'velocities': [velocity]}

        return None

    def get_New_State(self, current_state, link_index):
        
        modified_characters = []
        link_index_extended = range(link_index-3, link_index + 2)        # Iterate over the original string
        for index, char in enumerate(current_state):
            if index in link_index_extended:
                modified_characters.append("g")  # Keep "g" at the specific index
            else:
                modified_characters.append("r")  # Replace all other characters with "r"

        # Join the modified characters to create the final string
        self.modified_state = "".join(modified_characters)
        """ print(self.modified_state) """
         
         
        return None
    


    def get_TLS_info (self, veh_id):

        
            """ if veh_id not in self.veh_id_list:
            self.veh_id_list.append(veh_id) """ 
        
            tls_info = traci.vehicle.getNextTLS(veh_id)
            
            if len(tls_info) > 0:
                TLS = tls_info[0]
                TLS_id = TLS[0]
                TLS_link_index = TLS[1]
                CurrentDistance = TLS[2]
                CurrentState = TLS[3]

                self.original_state = traci.trafficlight.getAllProgramLogics(TLS_id)
                #print(self.original_state)


                if 50 < CurrentDistance < 300  :
                    traci.trafficlight.setLinkState(TLS[0],TLS[1],'g')
                elif CurrentDistance < 50:
                    state = traci.trafficlight.getRedYellowGreenState(TLS_id)
                    self.get_New_State(state,TLS_link_index)
                    traci.trafficlight.setLinkState(TLS[0],TLS[1],'G')
                    #traci.trafficlight.setRedYellowGreenState(TLS_id,self.modified_state)
                else:
                     None
                #     traci.trafficlight.setProgramLogic(TLS_id,self.original_state[0])                            
                    
            """ if tls_info not in self.tls_info_list:
                self.tls_info_list.append(tls_info)
                print(tls_info)
            
            for element in self.tls_info_list:
                for sub_element in element:
                    print(sub_element,'\n') """

            return None


    def plot_velocity_graph(self,vehicle_data):
        for vehicle_id, data in vehicle_data.items():
            time_stamps, velocities = data['time_stamps'], data['velocities']
            plt.plot(time_stamps, velocities, label=vehicle_id)
            

        # Set plot labels and title
        plt.xlabel('Simulation Time')
        plt.ylabel('Velocity')
        plt.title('Velocity vs. Simulation Time')
        plt.legend()


        # Show the plot
        plt.show()

if __name__ == "__main__":
    
    emv = EMV()

    # Start simulation
    emv.start_simulation()

    # Continue running the simulation
    emv_data = emv.run_simulation()

    # Collect velocity data for EMVs
    #emv.collect_emv_velocity_data()

    emv.plot_velocity_graph(emv_data)

    # End the simulation and close the connection to the server
    emv.close_simulation()

    # Plot velocity graph for EMVs after the simulation ends
    #emv.plot_velocity_graph(emv_data)

