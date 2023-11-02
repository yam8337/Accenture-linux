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

                if vehicle_id not in self.vehicle_type_list:
                    self.vehicle_type_list.append(vehicle_id)
                    self.tls_info_list = []
                    self.TLS_id = None


                # Get the velocity of the vehicle at the current simulation time
                velocity = traci.vehicle.getSpeed(vehicle_id)

                self.get_TLS_info(vehicle_id)
                
                # Get the current simulation time
                sim_time = traci.simulation.getTime()
                #print(sim_time,vehicle_id)

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
        
        self.tls_info = traci.vehicle.getNextTLS(veh_id)
        self.TLS = self.tls_info[0]

        if self.TLS[0] not in self.tls_info_list:
            self.tls_info_list.append(self.TLS[0])
            #self.collect_orginal_state()
            self.original_state = traci.trafficlight.getAllProgramLogics(self.TLS[0])[0]
                    
        if self.TLS_id is not None and self.TLS[0] != self.TLS_id:
            #self.revert_changes()
            traci.trafficlight.setProgramLogic(self.TLS_id,self.original_state)

        self.start_TLS_modification()

        return None

    def revert_changes(self): 
         traci.trafficlight.setProgramLogic(self.TLS_id,self.original_state)
         return None

    def start_TLS_modification(self):
                   
            if len(self.tls_info) > 0:
                self.TLS = self.tls_info[0]
                self.TLS_id = self.TLS[0]
                self.TLS_link_index = self.TLS[1]
                self.CurrentDistance = self.TLS[2]
                self.CurrentState = self.TLS[3]

                
                self.change_tls_info()
        
            return None
    

    def collect_orginal_state(self):
         
        """ if vehicle_id not in self.veh_id_list:
            self.veh_id_list.append(vehicle_id)  """ 

        self.original_state = traci.trafficlight.getAllProgramLogics(self.TLS[0])[0]
                    
        return None
    


    def change_tls_info (self):

            if 50 < self.CurrentDistance < 300  :
                    traci.trafficlight.setLinkState(self.TLS_id,self.TLS_link_index,'g')
            elif self.CurrentDistance < 50:
                    state = traci.trafficlight.getRedYellowGreenState(self.TLS_id)
                    self.get_New_State(state,self.TLS_link_index)
                    #traci.trafficlight.setLinkState(self.TLS_id,self.TLS_link_index,'G')
                    #traci.trafficlight.setRedYellowGreenState(TLS_id,self.modified_state)
            else:
                     #traci.trafficlight.setCompleteRedYellowGreenDefinition(self.TLS_id, self.original_state)
                     #traci.trafficlight.setProgramLogic(self.TLS_id,self.original_state)                            
                    None

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

