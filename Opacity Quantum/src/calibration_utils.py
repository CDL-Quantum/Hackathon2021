import numpy as np

from scipy.optimize import curve_fit

from qiskit import IBMQ
import qiskit.pulse as pulse
import qiskit.pulse.library as pulse_lib
from qiskit.compiler import assemble
from qiskit.pulse.library import Waveform

from qiskit.tools.monitor import job_monitor


"""
Unit conversion factors
"""
GHz = 1.0e9  # Gigahertz
MHz = 1.0e6  # Megahertz
us = 1.0e-6  # Microseconds
ns = 1.0e-9  # Nanoseconds


"""
Drive pulse parameters
"""
drive_sigma_us = 0.075                     # This determines the actual width of the gaussian
drive_samples_us = drive_sigma_us * 8      # This is a truncating parameter (Gaussians don't have a finite length).


class Calibration:
    """
    A set of tools for calibrating 0 <-> 1 and 1 <-> 2 transitions.
    """

    def __init__(self, backend_name, qubit_idx, num_shots, scale_factor):
        self.backend_name = backend_name
        self.qubit = qubit_idx
        self.num_shots = num_shots
        self.scale_factor = scale_factor

        # Load account and backend.
        IBMQ.load_account()
        self.provider = IBMQ.get_provider(
            hub='ibm-q-startup',
            group='opacity-quantum',
            project='testing'
        )
        self.backend = self.provider.get_backend(self.backend_name)
        assert self.backend.configuration().open_pulse, "Backend doesn't support Pulse"

        # Default qubit frequency in Hz.
        self.default_qubit_freq = self.backend.defaults().qubit_freq_est[self.qubit]
        print(f"Qubit {self.qubit} has an estimated frequency of {self.default_qubit_freq / GHz} GHz.")

        # Collect the necessary channels.
        self.drive_chan = pulse.DriveChannel(self.qubit)
        self.meas_chan = pulse.MeasureChannel(self.qubit)
        self.acq_chan = pulse.AcquireChannel(self.qubit)

        # Drive pulse parameters in units of dt.
        self.dt = self.backend.configuration().dt
        self.drive_sigma = get_closest_multiple_of_16(drive_sigma_us * us / self.dt)
        self.drive_samples = get_closest_multiple_of_16(drive_samples_us * us / self.dt)

        # Find out which measurement map index is needed for this qubit
        self.meas_map_idx = None
        for i, measure_group in enumerate(self.backend.configuration().meas_map):
            if self.qubit in measure_group:
                self.meas_map_idx = i
                break
        assert self.meas_map_idx is not None, f"Couldn't find qubit {self.qubit} in the meas_map!"

        # Get default measurement pulse from instruction schedule map
        self.inst_sched_map = self.backend.defaults().instruction_schedule_map
        self.measure = self.inst_sched_map.get(
            'measure',
            qubits=self.backend.configuration().meas_map[self.meas_map_idx]
        )

    def create_ground_freq_sweep_program(self, freqs, drive_power):
        """
        Builds a program that does a freq sweep by exciting the ground state.
        Depending on drive power this can reveal the 0 <-> 1 frequency or the 0 <-> 2 frequency.
        """
        if len(freqs) > 75:
            raise ValueError("You can only run 75 schedules at a time.")

        # Print information on the sweep
        print(f"The frequency sweep will go from {freqs[0] / GHz} GHz to {freqs[-1] / GHz} GHz "
              f"using {len(freqs)} frequencies. The drive power is {drive_power}.")

        # Define the drive pulse
        ground_sweep_drive_pulse = pulse_lib.gaussian(
            duration=self.drive_samples,
            sigma=self.drive_sigma,
            amp=drive_power,
            name='ground_sweep_drive_pulse'
        )

        # Create the base schedule
        schedule = pulse.Schedule(name='Frequency sweep starting from ground state.')
        schedule |= pulse.Play(ground_sweep_drive_pulse, self.drive_chan)
        schedule |= self.measure << schedule.duration

        # Define frequencies for the sweep
        schedule_freqs = [{self.drive_chan: freq} for freq in freqs]

        # Assemble the program
        # Note: we only require a single schedule since each does the same thing; for each schedule, the LO frequency
        # that mixes down the drive changes this enables our frequency sweep.
        ground_freq_sweep_program = assemble(
            schedule,
            backend=self.backend,
            meas_level=1,
            meas_return='avg',
            shots=self.num_shots,
            schedule_los=schedule_freqs
        )

        return ground_freq_sweep_program

    def run_ground_freq_sweep_program(self, freqs, drive_power):
        """
        Runs a freq sweep by exciting the ground state.
        """
        ground_freq_sweep_program = self.create_ground_freq_sweep_program(
            freqs=freqs,
            drive_power=drive_power
        )
        ground_freq_sweep_job = self.backend.run(ground_freq_sweep_program)

        # Print job info and status.
        print('Job ID: ' + ground_freq_sweep_job.job_id())
        job_monitor(ground_freq_sweep_job)

        return ground_freq_sweep_job

    def create_rabi_01_program(self, cal_qubit_freq, drive_amps):
        """
        Builds a program that does a Rabi experiment in the 0 <-> 1 transition.
        """
        # Create schedule
        rabi_01_schedules = []

        # Loop over all drive amplitudes
        for ii, drive_amp in enumerate(drive_amps):
            # Drive pulse
            rabi_01_pulse = pulse_lib.gaussian(
                duration=self.drive_samples,
                amp=drive_amp,
                sigma=self.drive_sigma,
                name='rabi_01_pulse_%d' % ii
            )

            # Add commands to schedule
            schedule = pulse.Schedule(name='Rabi Experiment at drive amp = %s' % drive_amp)
            schedule |= pulse.Play(rabi_01_pulse, self.drive_chan)
            schedule |= self.measure << schedule.duration  # shift measurement to after drive pulse
            rabi_01_schedules.append(schedule)

        # Assemble the schedules into a program.
        rabi_01_program = assemble(
            rabi_01_schedules,
            backend=self.backend,
            meas_level=1,
            meas_return='avg',
            shots=self.num_shots,
            schedule_los=[{self.drive_chan: cal_qubit_freq}] * len(drive_amps)
        )

        return rabi_01_program

    def run_rabi_01_program(self, cal_qubit_freq, drive_amps):
        """
        Runs a Rabi experiment for the 0 <-> 1 transition.
        """
        rabi_01_program = self.create_rabi_01_program(
            cal_qubit_freq=cal_qubit_freq,
            drive_amps=drive_amps
        )
        rabi_01_job = self.backend.run(rabi_01_program)

        # Print job info and status.
        print('Job ID: ' + rabi_01_job.job_id())
        job_monitor(rabi_01_job)

        return rabi_01_job

    def apply_sideband(self, pulse, freq, cal_qubit_freq):
        """
        Apply a sinusoidal sideband to this pulse at frequency freq.
        """
        # Time goes from 0 to dt*drive_samples, sine arg of form 2*pi*f*t
        t_samples = np.linspace(0, self.dt * self.drive_samples, self.drive_samples)
        sine_pulse = np.sin(2 * np.pi * (freq - cal_qubit_freq) * t_samples)  # no amp for the sine

        # Create sample pulse w/ sideband applied
        # Note: need to make sq_pulse.samples real, multiply elementwise
        sideband_pulse = Waveform(np.multiply(np.real(pulse.samples), sine_pulse), name='sideband_pulse')

        return sideband_pulse

    def create_excited_freq_sweep_program(self, freqs, cal_qubit_freq, pi_pulse_01, drive_power):
        """
        Builds a program that does a freq sweep by exciting the |1> state. This allows us to obtain the 1 <-> 2
        frequency. We get from the |0> to |1> state via a pi pulse using the calibrated qubit frequency. To do the
        frequency sweep from |1> to |2>, we use a sideband method by tacking a sine factor onto the sweep drive pulse.
        """
        if len(freqs) > 75:
            raise ValueError("You can only run 75 schedules at a time.")

        print(f"The frequency sweep will go from {freqs[0] / GHz} GHz to {freqs[-1] / GHz} GHz "
              f"using {len(freqs)} frequencies. The drive power is {drive_power}.")

        base_12_pulse = pulse_lib.gaussian(
            duration=self.drive_samples,
            sigma=self.drive_sigma,
            amp=drive_power,
            name='base_12_pulse'
        )

        schedules = []
        for jj, freq in enumerate(freqs):
            # Add sideband to gaussian pulse
            freq_sweep_12_pulse = self.apply_sideband(base_12_pulse, freq, cal_qubit_freq)

            # Add commands to schedule
            schedule = pulse.Schedule(name="Frequency = {}".format(freq))

            # Add 0->1 pulse, freq sweep pulse and measure
            schedule |= pulse.Play(pi_pulse_01, self.drive_chan)
            schedule |= pulse.Play(freq_sweep_12_pulse, self.drive_chan) << schedule.duration
            schedule |= self.measure << schedule.duration  # shift measurement to after drive pulses

            schedules.append(schedule)

        num_freqs = len(freqs)

        # Draw a schedule
        # display(schedules[-1].draw(channels=[self.drive_chan, self.meas_chan], label=True, scale=1.0))

        # Assemble freq sweep program
        # Note: LO is at cal_qubit_freq for each schedule; accounted for by sideband
        excited_freq_sweep_program = assemble(
            schedules,
            backend=self.backend,
            meas_level=1,
            meas_return='avg',
            shots=self.num_shots,
            schedule_los=[{self.drive_chan: cal_qubit_freq}] * num_freqs
        )

        return excited_freq_sweep_program

    def run_excited_freq_sweep_program(self, freqs, cal_qubit_freq, pi_pulse_01, drive_power):
        """
        Runs a freq sweep by exciting the first excited state.
        """
        excited_freq_sweep_program = self.create_excited_freq_sweep_program(
            freqs=freqs,
            cal_qubit_freq=cal_qubit_freq,
            pi_pulse_01=pi_pulse_01,
            drive_power=drive_power
        )
        excited_freq_sweep_job = self.backend.run(excited_freq_sweep_program)

        # Print job info and status.
        print('Job ID: ' + excited_freq_sweep_job.job_id())
        job_monitor(excited_freq_sweep_job)

        return excited_freq_sweep_job

    def create_rabi_12_program(self, cal_qubit_freq, pi_pulse_01, qubit_12_freq, drive_amps):
        """
        Builds a program that does a Rabi experiment in the 0 <-> 1 transition.
        """
        # Create schedule
        rabi_12_schedules = []

        # Loop over all drive amplitudes
        for ii, drive_amp in enumerate(drive_amps):
            base_12_pulse = pulse_lib.gaussian(
                duration=self.drive_samples,
                sigma=self.drive_sigma,
                amp=drive_amp,
                name='base_12_pulse'
            )
            # Apply sideband at the 1->2 frequency
            rabi_12_pulse = self.apply_sideband(base_12_pulse, qubit_12_freq, cal_qubit_freq)

            # Add commands to schedule
            schedule = pulse.Schedule(name='Rabi Experiment at drive amp = %s' % drive_amp)
            schedule |= pulse.Play(pi_pulse_01, self.drive_chan)  # 0 -> 1
            schedule |= pulse.Play(rabi_12_pulse, self.drive_chan) << schedule.duration  # 1 -> 2 Rabi pulse
            schedule |= self.measure << schedule.duration  # Shift measurement to after drive pulse

            rabi_12_schedules.append(schedule)

        # Assemble the schedules into a program.
        # Note: The LO frequency is at cal_qubit_freq to support the 0->1 pi pulse; it is modified for the 1->2 pulse
        # using sidebanding.
        rabi_12_program = assemble(
            rabi_12_schedules,
            backend=self.backend,
            meas_level=1,
            meas_return='avg',
            shots=self.num_shots,
            schedule_los=[{self.drive_chan: cal_qubit_freq}] * len(drive_amps)
        )

        return rabi_12_program

    def run_rabi_12_program(self, cal_qubit_freq, pi_pulse_01, qubit_12_freq, drive_amps):
        """
        Runs a Rabi experiment for the 0 <-> 1 transition.
        """
        rabi_12_program = self.create_rabi_12_program(
            cal_qubit_freq=cal_qubit_freq,
            pi_pulse_01=pi_pulse_01,
            qubit_12_freq=qubit_12_freq,
            drive_amps=drive_amps
        )
        rabi_12_job = self.backend.run(rabi_12_program)

        # Print job info and status.
        print('Job ID: ' + rabi_12_job.job_id())
        job_monitor(rabi_12_job)

        return rabi_12_job


"""
Useful functions
"""


def get_closest_multiple_of_16(num):
    """
    Compute the nearest multiple of 16. Needed because pulse enabled devices require
    durations which are multiples of 16 samples.
    """
    return int(num) - (int(num) % 16)


def get_job_data(job, average, qubit_idx, scale_factor):
    """
    Retrieve data from a job that has already run.
    """
    job_results = job.result(timeout=120)  # Timeout after 120 s
    result_data = []
    for i in range(len(job_results.results)):
        if average:  # Get avg data
            result_data.append(job_results.get_memory(i)[qubit_idx] * scale_factor)
        else:  # Get single data
            result_data.append(job_results.get_memory(i)[:, qubit_idx] * scale_factor)
    return result_data


def fit_function(x_values, y_values, function, init_params):
    """
    Fit a function using scipy curve_fit.
    """
    fitparams, conv = curve_fit(function, x_values, y_values, init_params)
    y_fit = function(x_values, *fitparams)
    return fitparams, y_fit


def baseline_remove(values):
    """
    Center data around 0.
    """
    return np.array(values) - np.mean(values)
