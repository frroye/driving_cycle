

from projects.ProjectController import *

"""Initialization of the project parameters"""
project_name = "test_4"

# Microtrips length in meters
microtrips_len = 100

# Utilisation of PCA or not
PCA = True

# Number of clusters used for the clustering
number_of_cluster = 8

# Used parameters for the clustering or the PCA
parameters = ['T', 'S', 'FuelR', 'FuelR_r', 'FuelRate_std', 'V', 'V_r', 'V_m', 'V_std', 'Acc', 'Dcc', 'Acc_2',
           'Acc_std', 'Idle_p', 'Acc_p', 'Cru_p', 'Cre_p', 'Dcc_p']
parameters = ['V', 'Acc', 'Idle_p', 'FuelR']
# Driving cycle length in seconds
cycle_len = 500

# Maximum speed difference between the end and the beginning of two microtrips
delta_speed = 3

# Total number of cycle produced
iteration = 10

# Number of selected cycles
nb_of_cycle = 10

# TODO cleaner/code mort
"""Initialization of the project controller"""
pc = ProjectController(project_name, "C://Users//frede//Documents//driving_cycle//")

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
pc.preprocess(raw_data_directory, column_names, microtrips_len)
pc.save_microtrips_data("C://Users//frede//Documents//driving_cycle//test_4//microtrips_data.csv")

"""Clustering of the data"""
pc.cluster(parameters, PCA, number_of_cluster)
# pc.save_clustered_data("C://Users//frede//Documents//driving_cycle//test_4//clustered_data.csv")
#pc.vizualize_cluster_2d(None, None, path="C://Users//frede//Documents//driving_cycle//clustered_data")

"""Driving cycle construction """
driving_cycles = pc.produce_driving_cycle(cycle_len, delta_speed, iteration, nb_of_cycle)
for dc in driving_cycles:
    dc.visualize_dc("Speed", path="C://Users//frede//Documents//driving_cycle//dc//"+str(dc.id))
    dc.save_cycle_data("C://Users//frede//Documents//driving_cycle//dc//", dc.id)

