import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

import dimod
from dwave.system.samplers import LeapHybridSampler, DWaveSampler
from dimod import BinaryQuadraticModel, ExactSolver

from dwave.system.composites import EmbeddingComposite
from neal import SimulatedAnnealingSampler
from datetime import datetime as dt

from matplotlib import pyplot as plt


class EnergyBQM:
    def __init__(self, context):

        self.schedules = context.get('schedules')
        self.demand_schedule = context.get('demand_schedule')

        self.sources = context.get('sources')
        self.cost_usage = context.get('cost_usage')
        self.cost_switch = context.get('cost_switch')
        self.cost_emission = context.get('cost_emission')
        self.capacity = context.get('capacity')

        self.n_energy_sources = len(self.sources)
        self.n_schedules = len(self.schedules)

        # define the binary quadratic model
        self.bqm = BinaryQuadraticModel(dimod.BINARY)

        # fill in the BQM
        self._define_variables()
        self._define_objective()
        self._define_constraints()

    def _define_variables(self):
        for s in self.schedules:
            for alpha in self.sources:
                self.bqm.add_variable(s+alpha)

    def _define_objective(self):
        # Objective
        # linear components
        for i in range(self.n_schedules):
            for alpha in range(self.n_energy_sources):
                self.bqm.set_linear(f's_{i}'+self.sources[alpha],
                                    self.demand_schedule[i]*(self.cost_usage[alpha] + self.cost_emission[alpha]))

        # quadratic components
        for i in range(self.n_schedules-1):
            for alpha in range(self.n_energy_sources):
                for beta in range(self.n_energy_sources):
                    if alpha != beta:
                        self.bqm.set_quadratic(f's_{i}'+self.sources[alpha],
                                               f's_{i+1}'+self.sources[beta],
                                               self.cost_switch[alpha] + self.cost_switch[beta])

    def _define_constraints(self):
        # Constraints
        # lb <= \sum_{i,k} a_{i,k} x_{i,k} + constant <= ub
        # inequality constraint: power > demand
        for i in range(self.n_schedules):
            for alpha in range(self.n_energy_sources):
                self.bqm.add_linear_inequality_constraint(
                    [(f's_{i}'+self.sources[alpha], self.capacity[alpha]) for alpha in range(self.n_energy_sources)],
                    constant=-self.demand_schedule[i],
                    lb=0,
                    lagrange_multiplier=50,
                    label='slack_'
                )

        # equality constraint: power = demand
        # for i in range(n_schedules):
        #     for alpha in range(n_energy_sources):
        #             bqm.add_linear_equality_constraint(
        #             [(f's_{i}'+sources[alpha], power_generation[alpha]) for alpha in range(n_energy_sources)],
        #             constant=-demand_schedule[i],
        #             lagrange_multiplier=10,
        #         )

    def solve_with_LeapHybridSampler(self, verbose=True):
        # Leap hybrid solver
        sampler = LeapHybridSampler()
        start = dt.now()
        self.result = sampler.sample(self.bqm, time_limit=50)
        if verbose:
            print('elapsed time (Leap Hybrid sampler): ', dt.now() - start)
            print(self.result.aggregate())
        return self.result

    def solve_with_SimulatedAnnealingSampler(self, verbose=True):
        sampler = SimulatedAnnealingSampler()
        start = dt.now()
        self.result = sampler.sample(self.bqm)
        if verbose:
            print('Elapsed time (simulated annealing): ', dt.now() - start)
            print(self.result.aggregate())
        return self.result

    def solve_with_QPU(self, verbose=True):
        # QPU solver (does not work for large problems)
        sampler = EmbeddingComposite(DWaveSampler(solver='DW_2000Q_6'))
        start = dt.now()
        self.result = sampler.sample(self.bqm)
        if verbose:
            print('Elapsed time (QPU - Chimera): ', dt.now() - start)
            print(self.result.aggregate())
        return self.result

    def solve_with_ExactSampler(self, verbose=True):
        # Exact sampler (does not work for large problems)
        sampler = ExactSolver()
        start = dt.now()
        self.result = sampler.sample(self.bqm)
        if verbose:
            print('Elapsed time (Exact solver): ', dt.now() - start)
            print(self.result.aggregate())
        return self.result

    def plot_results(self):
        df = self.result.aggregate().to_pandas_dataframe()
        if 'chain_break_fraction' in df.columns:
            df = df.drop('chain_break_fraction', axis=1)

        df = df[df.energy == min(df.energy)]
        df['status'] = 'status'

        ddf = df.set_index('status').drop(['energy', 'num_occurrences'], axis=1).transpose()
        ddf['schedule'] = ddf.index.map(lambda x: int(x[2:-1]))
        ddf['source'] = ddf.index.map(lambda x: x[-1])

        plt.plot(self.demand_schedule, label='demand')

        list_plots = []
        for i in range(len(self.sources)):
            p_df = ddf[ddf.source == self.sources[i]]
            p_df['power'] = self.capacity[i] * p_df.status
            p_df.sort_values(by='schedule')
            bottom_plots = sum([x.power.values for x in list_plots])
            list_plots.append(p_df)
            plt.bar(p_df.schedule.values, p_df.power.values,
                    bottom=bottom_plots,
                    label=self.sources[i])

        plt.legend()
        plt.show()


if __name__ == "__main__":
    np.random.seed(123)
    # Assume looking at the future 24 hours
    n_schedules = 24

    # define binary variables
    schedules = [f's_{i}' for i in range(n_schedules)]

    # read in the hourly load values for a single year
    demand_data = pd.read_excel('./data/Monthly-hourly-load-values_2014_IT.xlsx')

    # collect the demand data for the year into a list
    demand = []
    for i in range(len(demand_data)):
        demand += list((demand_data.iloc[i, 6:]))

    # Plot demand schedule for a single day (24h)
    plt.plot(demand[0:24], label='demand')
    plt.show()

    # scaling down demand to size of problem /3000 to obtain a range of values compatible with our energy network
    demand_schedule = [20 * i / max(demand) for i in demand[0:n_schedules]]

    # Nuclear 'n', Coal 'c', Hydro 'h', Gas 'g', Solar 's', Wind 'w'
    sources = ['n', 'c', 'h', 'g', 's', 'w']

    # Operating costs by plant type(Operation,Maintenance,Fuel) mills per kwh
    # operating_costs = [('n',11.17+7.06+7.48),
    #                    ('c',5.16+5.41+26.70),
    #                    ('h',8.37+5.06),
    #                    ('g',2.34+2.68+28.22),
    #                    ('s',5.16+5.41),
    #                    ('w',5.16+5.41)]

    # converted costs to integer for implementation of constraint on Leap Hybrid solver
    operating_costs = [('n', 11 + 7 + 7),
                       ('c', 5 + 5 + 26),
                       ('h', 8 + 5),
                       ('g', 2 + 2 + 28),
                       ('s', 5 + 5),
                       ('w', 5 + 5)]

    # define the cost of usage (total operating costs)
    cost_usage = [operating_costs[i][1] for i in range(len(operating_costs))]

    # define the cost to switch off/on one of the energy sources
    cost_switch = [10, 2, 1, 1, 5, 2]

    # define the carbon emission per kWh
    cost_emission = [20, 25, 7, 10, 1, 2]

    # define the max power generation per kWh per source and plant
    capacity = [7, 6, 3, 5, 4, 2]

    context = {}
    context['schedules'] = schedules
    context['demand_schedule'] = demand_schedule

    context['sources'] = sources
    context['cost_usage'] = cost_usage
    context['cost_switch'] = cost_switch
    context['cost_emission'] = cost_emission
    context['capacity'] = capacity

    # define BQM
    bqm = EnergyBQM(context)

    res = bqm.solve_with_LeapHybridSampler(verbose=True)

    bqm.plot_results()

    # classical_res = bqm.solve_with_SimulatedAnnealingSampler(verbose=True)
    #
    # bqm.plot_results()
