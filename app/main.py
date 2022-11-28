
import os
from projects.ProjectController import *

absolute_path = os.path.dirname(__file__)

"""Initialization of the project parameters"""

# Microtrips length in meters
microtrips_len = 100

# Utilisation of PCA or not
PCA = False

# Number of clusters used for the clustering
number_of_cluster = 3

# Used parameters for the clustering or the PCA
parameters = ['T', 'S', 'FuelR', 'FuelR_r', 'FuelRate_std', 'V', 'V_r', 'V_m', 'V_std', 'Acc', 'Dcc', 'Acc_2',
           'Acc_std', 'Idle_p', 'Acc_p', 'Cru_p', 'Cre_p', 'Dcc_p']
parameters = ['V', 'Acc']
# Driving cycle length in seconds
cycle_len = 100

# Maximum speed difference between the end and the beginning of two microtrips
delta_speed = 20

# Total number of cycle produced
iteration = 50

# Number of selected cycles
nb_of_cycle = 1

"""Initialization of the project controller"""
pc = ProjectController()

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
relative_raw_data_directory = "data\\raw_data\\asad_test\\"
pc.preprocess(os.path.join(absolute_path, relative_raw_data_directory), column_names, microtrips_len)

relative_microtrips_path = "results\\microtrips_data.csv"

pc.save_microtrips_data(os.path.join(absolute_path, relative_microtrips_path))

"""Clustering of the data"""
pc.cluster(parameters, PCA, number_of_cluster)
relative_clustered_data_path = "results\\clustered_data.csv"
pc.save_clustered_data(os.path.join(absolute_path, relative_clustered_data_path))
pc.vizualize_cluster_2d(None, None, path=os.path.join(absolute_path, "results\\clusters"))

"""Driving cycle construction """

driving_cycles = pc.produce_driving_cycle(cycle_len, delta_speed, iteration, nb_of_cycle)
print('Assessment criteria: ', pc.get_assessment_criteria())
for dc in driving_cycles:
    dc.visualize_dc("Speed", path=os.path.join(absolute_path, "results\\dc"+str(dc.id)))
    dc.visualize_dc_line(parameter="Speed",
                         path=os.path.join(absolute_path, "results\\dc_line_"+str(dc.id)),
                         title="Title",
                         xLabel="Cumulative time")
    dc.save_cycle_data(os.path.join(absolute_path, "results\\dc"), dc.id)
    y = pd.DataFrame(dc.get_parameters(), index=[0])
    y.to_csv(os.path.join(absolute_path,'results\\DC.csv'), mode='a', index=False, header=False, sep=';')


