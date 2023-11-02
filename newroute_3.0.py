import traci
from sumolib import checkBinary
import matplotlib.pyplot as plt

class EMVSimulator:
    def __init__(self):
        self.emv_data = {}
        self.tls_info_list = []
        self.emv_vehicle_list = []
        self.TLS_id = None

    def start_simulation(self):
        """
        Start the SUMO simulation.
        """
        sumo_binary = checkBinary('sumo-gui')
        #sumo_file = "../../artery/scenarios/NewRoute/osm.sumocfg"
        sumo_file = "../../InTAS/scenario/InTAS.sumocfg"
        traci.start([sumo_binary, "-c", sumo_file])

    def close_simulation(self):
        """
        Close the SUMO simulation.
        """
        traci.close()

    def run_simulation(self):
        """
        Run the simulation and collect EMV velocity data.
        """
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            self.collect_emv_velocity_data()
        return self.emv_data

    def collect_emv_velocity_data(self):
        """
        Collect velocity data for Emergency Vehicles (EMVs).
        """
        self.all_vehicles = traci.vehicle.getIDList()

        for vehicle_id in self.all_vehicles:
            if vehicle_id.startswith('emv'):
                if vehicle_id not in self.emv_vehicle_list:
                    self.emv_vehicle_list.append(vehicle_id)
                    print(vehicle_id,len(traci.vehicle.getNextTLS(vehicle_id)), traci.vehicle.getNextTLS(vehicle_id))
                    self.TLS_id = []
                    self.tls_info_list = []

                self.get_tls_info(vehicle_id)

                velocity = traci.vehicle.getSpeed(vehicle_id)
                sim_time = traci.simulation.getTime()
                #print(sim_time)

                if vehicle_id in self.emv_data:
                    self.emv_data[vehicle_id]['time_stamps'].append(sim_time)
                    self.emv_data[vehicle_id]['velocities'].append(velocity)
                else:
                    self.emv_data[vehicle_id] = {'time_stamps': [sim_time], 'velocities': [velocity]}

    def get_tls_info(self, veh_id):
        """
        Get Traffic Light System (TLS) information for a vehicle.
        """
        self.tls_info = traci.vehicle.getNextTLS(veh_id)
       
        if len(self.tls_info) > 0:
            self.TLS = self.tls_info[0]

            if self.TLS[0] not in self.tls_info_list:
                self.tls_info_list.append(self.TLS[0])
                self.original_state = traci.trafficlight.getAllProgramLogics(self.TLS[0])[0]

            #if self.TLS_id is not None and self.TLS[0] != self.TLS_id:
            #if self.TLS[0] != self.TLS_id:
             #   if len(self.TLS_id)>0:
              #      self.revert_changes()

            
            #self.TLS = self.tls_info[0]
            self.TLS_id = self.TLS[0]
            self.TLS_link_index = self.TLS[1]
            self.current_distance = self.TLS[2]
            self.current_state = self.TLS[3]

            #self.change_tls_info()

            self.start_tls_modification()

    def revert_changes(self):
        """
        Revert changes made to the Traffic Light System (TLS).
        """
        traci.trafficlight.setProgramLogic(self.TLS_id, self.original_state)

    def start_tls_modification(self):
        """
        Start modification of Traffic Light System (TLS) based on vehicle's proximity.
        """
        if len(self.tls_info) > 0:
            self.TLS = self.tls_info[0]
            self.TLS_id = self.TLS[0]
            self.TLS_link_index = self.TLS[1]
            self.current_distance = self.TLS[2]
            self.current_state = self.TLS[3]

            self.change_tls_info()
            #self.get_new_state()

        return None
    
    def change_tls_info(self):
        """
        Change Traffic Light System (TLS) based on vehicle's proximity.
        """
        """ if 50 < self.current_distance < 300:
            traci.trafficlight.setLinkState(self.TLS_id, self.TLS_link_index, 'g')
        elif self.current_distance < 50:
            state = traci.trafficlight.getRedYellowGreenState(self.TLS_id)
            self.get_new_state(state, self.TLS_link_index) """

        if  self.current_distance < 300:
            state = traci.trafficlight.getRedYellowGreenState(self.TLS_id)
            self.get_new_state(state, self.TLS_link_index)
            traci.trafficlight.setRedYellowGreenState(self.TLS_id,self.modified_state)

    def get_new_state(self, current_state, link_index):
        """
        Get new state for Traffic Light System (TLS) based on link index.
        """
        modified_characters = []
        link_index_extended = range(link_index , link_index +1)
        for index, char in enumerate(current_state):
            if index in link_index_extended:
                modified_characters.append("g")
            else:
                modified_characters.append("r")
        self.modified_state = "".join(modified_characters)

    def plot_velocity_graph(self, vehicle_data):
        """
        Plot velocity graph for EMVs.
        """
        for vehicle_id, data in vehicle_data.items():
            time_stamps, velocities = data['time_stamps'], data['velocities']
            plt.plot(time_stamps, velocities, label=vehicle_id)

        plt.xlabel('Simulation Time')
        plt.ylabel('Velocity')
        plt.title('Velocity vs. Simulation Time')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    emv_simulator = EMVSimulator()

    # Start simulation
    emv_simulator.start_simulation()

    # Run the simulation and collect EMV velocity data
    emv_data = emv_simulator.run_simulation()

    # Plot velocity graph for EMVs
    emv_simulator.plot_velocity_graph(emv_data)

    # Close the simulation
    emv_simulator.close_simulation()
