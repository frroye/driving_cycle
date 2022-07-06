from driving_cycle_construction.DrivingCycleController import DrivingCyclesController
from projects.ProjectController import *

"""Initialization of the project parameters"""
project_name = "test_4"

# Microtrips length in meters
microtrips_len = 250

# Utilisation of PCA or not
PCA = False

# Number of clusters used for the clustering
number_of_cluster = 3

# Used parameters for the clustering or the PCA
parameters = ['T', 'S', 'FuelR', 'FuelR_r', 'FuelRate_std', 'V', 'V_r', 'V_m', 'V_std', 'Acc', 'Dcc', 'Acc_2',
           'Acc_std', 'Idle_p', 'Acc_p', 'Cru_p', 'Cre_p', 'Dcc_p']
parameters = ['V', 'Idle_p']
# Driving cycle length in seconds
cycle_len = 500

# Maximum speed difference between the end and the beginning of two microtrips
delta_speed = 3

# Total number of cycle produced
iteration = 10

# Number of selected cycles
nb_of_cycle = 10


"""Initialization of the project controller"""
project_controller = ProjectController(project_name, "C://Users//frede//Documents//driving_cycle//")

"""Creation of the sub directories"""
#project_controller.create_directories()

"""
**** Preprocessing of the data ****
Files in raw data directory are expected to be in csv format
Columns of files in raw data directory are expected to be as follow:
'DateTime' : date and time in format AAA-MM-JJ  HH:MM:SS,
'Speed' : speed,
'Acc' : acceleration,
'FuelRate' : fuel rate,
'gps_Lat' : gps latitude,
'gps_Long': gps longitude
"""

column_names = ['DateTime', 'Speed', 'Acc', 'FuelRate', 'gps_Lat', 'gps_Long']
raw_data_directory = "C://Users//frede//Documents//driving_cycle//stm//"
project_controller.preprocess(raw_data_directory, column_names, microtrips_len)


"""Clustering of the data"""
project_controller.cluster(parameters, PCA, number_of_cluster)

"""Driving cycle construction """
driving_cycles = project_controller.produce_driving_cycle(cycle_len, delta_speed, iteration, nb_of_cycle)
for dc in driving_cycles:
    dc.visualize_dc("Speed", path="C://Users//frede//Documents//driving_cycle//dc//"+str(dc.id))
    dc.save_cycle_data("C://Users//frede//Documents//driving_cycle//dc//", dc.id)

