from driving_cycle_construction.DrivingCycle import DrivingCycle
from driving_cycle_construction.TransitionMatrixController import TransitionMatrixController
from driving_cycle_construction.DCParametersCalculator import DCParametersCalculator
import pandas as pd


class DrivingCyclesController:
    def __init__(self, clustered_microtrip_df, clean_data_df, cycle_len, delta_speed, comparisonParameters=[]):
        self.segment_df = clustered_microtrip_df
        self.clean_data_df = clean_data_df
        self.cycle_len = cycle_len
        self.delta_speed = delta_speed
        self.comparisonParameters = comparisonParameters
        self.cycles = []

        # generate the transition matrix
        tmc = TransitionMatrixController(self.segment_df)
        self.transition_matrix = tmc.get_transition_matrix()

        # generate the assessment criteria
        dc_parameter_controller = DCParametersCalculator(self.segment_df, id=-1)
        self.assessment_criteria = dc_parameter_controller.summarize()

    def get_full_cycles(self):
        return [dc.get_full_driving_cycle(self.clean_data_df) for dc in self.cycles]

    def generate_cycle(self, iteration, number_of_cycle):
        """Generate cycles and select the best one. 
        Cycles contains the potential cycles.
        Parameters contains the difference between the cycles parameter and the the assessment criteria.
        iteration: number of cycles generated
        dc_len: length of the cycles, in seconds
        delta_speed: accepted speed difference between two microtrips edges
        Return the selected cycles.
        """

        parameters = []
        cycles = []
        print(self.transition_matrix)
        for i in range(0, iteration):
            print(i)
            cycle = DrivingCycle(self.segment_df, self.transition_matrix, self.cycle_len, self.delta_speed, i)
            cycles.append(cycle)
            parameters.append(cycle.compute_difference(self.assessment_criteria))
        comparison_df = self.compare_cycle(parameters)
        selected_cycles = []
        for c in range(0, number_of_cycle):
            nb = comparison_df['rank'].sort_values(ascending=True).index.values[c]
            cycles[nb].set_rank((comparison_df.iloc[int(nb)]['rank']))
            selected_cycles.append(nb)
        self.cycles = [cycles[nb] for nb in selected_cycles]
        self.get_full_cycles()

    def compare_cycle(self, parameters):
        """Compare the cycles contained in parameters. 
        It ranks the cycles according to each criterion. The most performant cycle according to a 
        criterion is given a rank 0. This rank is added to the column rank, that contains the
        sum of all ranks of a cycle. It only ranks the cycle according to the comparison parameters 
        in self.comparisonParameters.
        """
        comparison_df = pd.DataFrame(parameters)
        comparison_df['rank'] = 0
        if len(self.comparisonParameters) == 0:
            self.comparisonParameters = [col for col in comparison_df.columns if col != 'rank']
        for column in comparison_df[self.comparisonParameters]:
            index = comparison_df[column].sort_values(ascending=True).index.values
            for i in range(0, len(index)):
                comparison_df.loc[index[i], 'rank'] += i
        return comparison_df
