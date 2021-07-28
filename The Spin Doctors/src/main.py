from src.utils.BQM import EnergyBQM

import pandas as pd
import numpy as np


if __name__ == "__main__":
    np.random.seed(123)
    # todo: think about possible number of schedules (e.g. 24 hours for a quarter). Currently the
    #  schedule is based on assuming days and yearly seasonality. The problem does not apply if we
    #  consider real historical data.
    n_schedules = 90

    # define binary variables
    schedules = [f's_{i}' for i in range(n_schedules)]
    sources = ['g', 'n', 's', 'w'] # gas, nuclear, solar, wind
    n_energy_sources = len(sources)

    # renwable = pd.read_csv('data/renewable_power_plants_EU.csv')

    # todo: change the following fake demand schedule to actual data (e.g. historical series)
    # parameters: demand schedule, cost of usage, cost of switching on-off
    # demand_schedule = [3, 2, 2, 2]
    week = 7
    year = 365

    # simulate the demand schedule based on a weekly (weekend low demand) and yearly seasonality
    demand_schedule = [int(4*((2-np.sin(int(i%week/6)))*(2 + np.sin(2 * np.pi * i/year))/2 + np.random.rand()))
                       for i in range(n_schedules)]

    # plt.plot(demand_schedule)

    # todo: define a good set of energy sources and power plants, with corresponding:
    #  - cost of usage
    #  - cost of switching on-off
    #  - cost associated to carbon emission (via taxes or buying certificates)

    # energy sources: 0: gas, 1: nuclear, 2: solar, 3: wind
    # define the cost of usage per kWh
    # todo: check operating costs for 2019 at https://www.eia.gov/electricity/annual/html/epa_08_04.html
    cost_usage = [2, 10, 1, 5]

    # define the cost to switch off/on one of the energy sources
    cost_switch = [5, 20, 0, 1]

    # define the carbon emission per kWh
    cost_emission = [10, 20, 0, 0]

    # todo: define the max power generation per kWh per source and plant
    # info on capacity
    # solar: 1-5 MW https://www.eia.gov/todayinenergy/detail.php?id=38272
    # wind: 2.5–3 MW https://www.ewea.org/wind-energy-basics/faq/#:~:text=The%20output%20of%20a%20wind,average%20EU%20households%20with%20electricity.
    #

    capacity = [7, 15, 3, 5]

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

    classical_res = bqm.solve_with_SimulatedAnnealingSampler(verbose=True)

    bqm.plot_results()
