import pandas as pd
import random
from driving_cycle_construction.DCParametersCalculator import DCParametersCalculator
import os


class DrivingCycle:

    def __init__(self, df, transition_matrix, dc_len, delta_speed, cycle_id=0):
        self.id = cycle_id
        self.df_segment = df
        self.transition_matrix = transition_matrix
        self.len = dc_len
        self.delta_speed = delta_speed
        self.segment_list = self.generate_dc()
        self.df_dc_segment = self.df_segment.iloc[self.segment_list, :]
        self.parameters = self.compute_dc_parameters()
        self.difference = None
        self.rank = None
        self.full_cycle = None

    def select_first_segment(self):
        """ Aleatory select a first segment within the segment data frame df_segment.
        Return the index of the segment and its cluster."""
        sample = self.df_segment.sample()
        return sample.index, int(sample['cluster'])

    def select_next_cluster(self, cluster):
        """ cluster : cluster of the last microtrip
        Given a cluster, return the following cluster using the transition matrix self.transition_matrix."""
        clusters = range(0, len(self.transition_matrix))
        next_cluster = random.choices(clusters, self.transition_matrix[int(cluster)])
        return next_cluster[0]

    def get_cluster(self, seg):
        """ Return the cluster number of a segment seg."""
        return self.df_segment.iloc[seg, :]["cluster"]

    def select_seg(self, cluster):
        """cluster: cluster of the next segment
        Given a cluster, aleatory select a segment in this cluster family"""
        valid_seg = False
        df_len = len(self.df_segment)
        while not valid_seg:
            seg = self.df_segment[self.df_segment['cluster'] == cluster].sample(n=1).index
            if seg < df_len:
                valid_seg = True
        return seg

    def get_seg_length(self, seg):
        """ Return the length in second of a segment seg"""
        return float(self.df_segment.iloc[seg]["T"])

    def generate_dc(self):
        """Generate a list of segment that form the driving cycle following the markov chain method"""
        seg_i, cluster_i = self.select_first_segment()
        f_speed = float(self.df_segment.iloc[seg_i, :]['V_f'])
        dc_ = [int(cluster_i)]
        dc_len = self.get_seg_length(seg_i)
        while dc_len < self.len:
            next_cluster = self.select_next_cluster(cluster_i)
            i = False
            count = 0
            while not i:
                next_seg = self.select_seg(next_cluster)
                i_speed = float(self.df_segment.iloc[next_seg, :]['V_i'])
                # The following condition can be add with bigger dataset.
                # For smaller dataset, there might not be enough microtrips to use a microtrip only one time per driving cycle
                #if next_seg not in dc_ and abs(i_speed - f_speed) < self.delta_speed:
                if abs(i_speed - f_speed) < self.delta_speed:
                    i = True
                    f_speed = float(self.df_segment.iloc[next_seg, :]['V_f'])
                    dc_.append(int(next_seg[0]))
                    cluster_i = next_cluster
                    dc_len += self.get_seg_length(next_seg)
                else:  # this allows the construction to be faster : if no segment with a valid initial speed is found
                    #  within 5 times, a new cluster is selected
                    count += 1
                    if count > 5:
                        i = True
        return dc_

    def compute_dc_parameters(self):
        """Compute the parameters for the cycle. These parameters will be use to compare the cycles with the assessment
        criteria of the entire database."""
        parameters = DCParametersCalculator(self.df_dc_segment, self.id)
        return parameters

    def get_segment_list(self):
        return self.segment_list

    def get_parameters(self):
        return self.parameters.get_parameters()

    def get_desire_len(self):
        return self.len

    def get_real_len(self):
        return self.df_dc_segment["T"].sum()

    def get_difference(self):
        return self.difference

    def get_number_of_mircrotrips(self):
        """Return the number of microtrips in the cycle"""
        return len(self.segment_list)

    def set_rank(self, rank):
        self.rank = rank

    def get_rank(self):
        return self.rank

    def get_full_driving_cycle(self, clean_data_df):
        """Return the full profile of the driving cycle, using the microtrips full data."""
        full_segment_data = []
        for seg in self.segment_list:
            full_segment_data.append(clean_data_df[clean_data_df['Seg'] == seg])

        df = pd.concat(full_segment_data, axis=0, join='outer', ignore_index=False, keys=None,
                       levels=None, names=None, verify_integrity=False, copy=True)
        df["cumulative_time"] = df["Duration"].cumsum()
        self.full_cycle = df
        return df

    def compute_difference(self, assessment_criteria):
        """Compute the difference between the driving cycle parameters and the assessment criteria."""
        diff_ = {}
        for criteria in assessment_criteria:

            diff = abs((assessment_criteria[criteria] - self.parameters.get_parameters()[criteria])
                       / (assessment_criteria[criteria])) if assessment_criteria[criteria] != 0 else float('inf')
            diff_ = {**diff_, **{criteria: diff}}
            self.difference = diff_
        return diff_

    def save_cycle_parameters(self, directory_name, file_name):
        file_name = directory_name + file_name + ".csv"
        with open(file_name, 'w') as f:
            for key in self.get_parameters():
                f.write("%s,%s\n" % (key, self.get_parameters()[key]))

    def save_cycle_difference(self, directory_name, file_name):
        file_name = directory_name + file_name + ".csv"
        with open(file_name, 'w') as f:
            for key in self.get_difference():
                f.write("%s,%s\n" % (key, self.get_parameters()[key]))

    def save_cycle_data(self, directory_name, file_name):
        file_name = directory_name + str(file_name) + ".csv"
        self.full_cycle.to_csv(file_name, sep=";")

    def visualize_dc(self, parameter, title="driving cycle", show=False, path=None):
        """Visualize the driving cycle parameter over time. Each microtip has a different color.
        parameter: 'Speed', 'FuelRate', 'Acc'
        """
        df = self.full_cycle
        fig = df.plot.scatter(x="cumulative_time", y=parameter, c="Seg", title=title, colormap='viridis',
                              legend=False).get_figure()
        if path:
            fig.savefig(path + '.png')
        if show:
            fig.show()
