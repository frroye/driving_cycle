import os

from driving_cycle_construction.DrivingCycle import DrivingCycle
from driving_cycle_construction.DrivingCycleController import DrivingCyclesController
from preprocessing.RawDataController import *
from clustering.ClusteringController import ClusteringController


def directory_is_empty(sub_directory):
    directory = os.listdir(sub_directory)
    if len(directory) == 0:
        return 1
    else:
        return 0;


def create_directory(directory_name, parent_dir):
    path = os.path.join(parent_dir, directory_name)
    if not os.path.exists(path):
        os.makedirs(path)


class ProjectController:
    def __init__(self, project_name, path="../results/"):
        self.project_name = project_name + "/"
        create_directory(self.project_name, path)
        self.path = path + self.project_name
        self.clean_data_df = None
        self.microtrip_df = None
        self.clustered_microtrip_df = None

    def create_directories(self):
        """Create the require sub directories:
        raw_data, microtrips, clustered_microtrips, clean_data and results."""
        if directory_is_empty(self.path):
            self.create_directory('data/', self.path)
            data_sub_directory = ["raw_data", "microtrips", "clustered_microtrips", "clean_data", "results"]
            for directory in data_sub_directory:
                create_directory(directory, self.path + 'data/')
        else:
            print(str(self.path) + " is not empty")

    def preprocess(self, raw_data_directory, column_names, microtrip_len):
        """Preprocess the content of data/raw_data.
        Save the resulting clean and segmented data in self.microtrip_df"""
        if not directory_is_empty(raw_data_directory):
            fc = find_files(raw_data_directory, column_names)
            microtrip_len = microtrip_len
            data_controler = RawDataController(fc)
            data_controler.build_microtrips(microtrip_len)
            self.microtrip_df = data_controler.combine_microtrips()
            self.clean_data_df = data_controler.get_combined_clean_data()
        else:
            print("data/raw_data is empty.")

    def cluster(self, columns, PCA=True, number_of_cluster=7):
        clustering_controller = ClusteringController(self.microtrip_df)
        clustering_controller.select_clustering_columns(columns, PCA)
        clustering_controller.kmeans(number_of_cluster)
        self.clustered_microtrip_df = clustering_controller.df
        clustering_controller.visualize_cluster_2d(columns[0], columns[1])

    def produce_driving_cycle(self, cycle_len, delta_speed, iteration, number_of_cycle=1):
        dc_controller = DrivingCyclesController(self.clustered_microtrip_df, self.clean_data_df, cycle_len, delta_speed)
        dc_controller.generate_cycle(iteration, number_of_cycle)
        return dc_controller.cycles
