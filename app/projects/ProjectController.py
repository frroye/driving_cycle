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
    def __init__(self):
        self.clean_data_df = None
        self.microtrip_df = None
        self.clustered_microtrip_df = None
        self.raw_data_controler = None
        self.clustering_controller = None

    def preprocess(self, raw_data_directory, column_names, microtrip_len):
        """Preprocess the content of data/raw_data.
        Save the resulting clean and segmented data in self.microtrip_df"""
        if not directory_is_empty(raw_data_directory):
            fc = find_files(raw_data_directory, column_names)
            microtrip_len = microtrip_len
            self.raw_data_controler = RawDataController(fc)
            self.raw_data_controler.build_microtrips(microtrip_len)
            self.microtrip_df = self.raw_data_controler.combine_microtrips()
            self.clean_data_df = self.raw_data_controler.get_combined_clean_data()
        else:
            print("data/raw_data is empty.")

    def save_microtrips_data(self, path):
        self.microtrip_df.to_csv(path, sep=";")

    def save_clean_data(self, path):
        self.clean_data_df.to_csv(path, sep=";")

    def set_microtrips_data(self, path):
        self.microtrip_df = pd.read_csv(path, sep=';', encoding='latin-1')
        self.clustering_controller = ClusteringController(self.microtrip_df)

    def set_clean_data(self, path):
        self.clean_data_df = pd.read_csv(path, sep=';', encoding='latin-1')

    def save_clustered_data(self, path):
        self.clean_data_df.to_csv(path, sep=";")

    def set_clustered_data(self, path):
        self.clustered_microtrip_df = pd.read_csv(path, sep=';', encoding='latin-1')

    def cluster(self, columns, PCA, number_of_cluster=7):
        self.clustering_controller = ClusteringController(self.microtrip_df)
        self.clustering_controller.select_clustering_columns(columns, PCA)
        self.clustering_controller.kmeans(number_of_cluster)
        self.clustered_microtrip_df = self.clustering_controller.df

    def vizualize_cluster_2d(self, x, y, show=False, path=None):
        self.clustering_controller.visualize_cluster_2d(x, y, show=show, path=path)

    def produce_driving_cycle(self, cycle_len, delta_speed, iteration, number_of_cycle=1):
        dc_controller = DrivingCyclesController(self.clustered_microtrip_df, self.clean_data_df, cycle_len, delta_speed)
        dc_controller.generate_cycle(iteration, number_of_cycle)
        return dc_controller.cycles
