# Problem Set 4: Simulating the Spread of Disease and Bacteria Population Dynamics
# Name:
# Collaborators (Discussion):
# Time:

import math
import numpy as np
import pylab as pl
import random


##########################
# End helper code
##########################

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleBacteria
    and ResistantBacteria classes to indicate that a bacteria cell does not
    reproduce. You should use NoChildException as is; you do not need to
    modify it or add any code.
    """
    pass  # Added pass statement for consistency


def make_one_curve_plot(x_coords, y_coords, x_label, y_label, title) -> None:
    """
    Plot of the x coordinates and the y coordinates.

    With the labels and title provided.

    Args
    ----
        x_coords (list of floats): x coordinates to graph
        y_coords (list of floats): y coordinates to graph
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): title for the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords)
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


def make_two_curve_plot(x_coords,
                        y_coords1,
                        y_coords2,
                        y_name1,
                        y_name2,
                        x_label,
                        y_label,
                        title) -> None:
    """
    Plot with two curves on it.

    Based on the x coordinates with each of the set of y coordinates provided.

    Args
    ----
        x_coords (list of floats): the x coordinates to graph
        y_coords1 (list of floats): the first set of y coordinates to graph
        y_coords2 (list of floats): the second set of y-coordinates to graph
        y_name1 (str): name describing the first y-coordinates line
        y_name2 (str): name describing the second y-coordinates line
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): the title of the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords1, label=y_name1)
    pl.plot(x_coords, y_coords2, label=y_name2)
    pl.legend()
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


##########################
# PROBLEM 1
##########################

class SimpleBacteria(object):
    """A simple bacteria cell with no antibiotic resistance."""

    def __init__(self, birth_prob, death_prob) -> None:
        """
        Class constructor method.

        Args
        ----
            birth_prob (float): value between 0 and 1. Maximum possible
              reproduction probability
            death_prob (float): value between 0 and 1. Maximum death
              probability

        Returns
        -------
            None.

        """
#
#  Parameter validation section
#
        if type(birth_prob) != float:
            raise TypeError('Bacteria birth probability must be a float.')
        if not 0.0 <= birth_prob <= 1.0:
            raise ValueError('Bacteria birth probability must be between 0.0 \
                             and 1.0')

        if type(death_prob) != float:
            raise TypeError('Bacteria death probability must be a float.')
        if not 0.0 <= death_prob <= 1.0:
            raise ValueError('Bacteria death probability must be between 0.0 \
                             and 1.0')

        self.birth_prob = birth_prob
        self.death_prob = death_prob
        self.killed = False  # flag to indicate if bacteria is dead
        pass  # TODO

    def is_killed(self) -> bool:
        """
        Randomly determine if bacteria cell is killed at this time step.

        Stochastically determines whether this bacteria cell is killed in
        the patient's body at a time step, i.e. the bacteria cell dies with
        some probability equal to the death probability each time step.

        Returns
        -------
            isDead (boolean): Returns True if cell is killed, else False

        """
        randomDeathEvent = random.random()
        if randomDeathEvent <= self.death_prob:
            isDead = True
        else:
            isDead = False
        return isDead
        pass  # TODO

    def killBacteria(self) -> None:
        """Kill a particular bacteria."""
        self.killed = True

    def reproduce(self, pop_density) -> None:
        """
        Stochastically determines if bacteria cell reproduces at a time step.

        Called by the update() method in the Patient and TreatedPatient
        classes.

        The bacteria cell reproduces with probability
        self.birth_prob * (1 - pop_density).

        If this bacteria cell reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleBacteria (which has the same
        birth_prob and death_prob values as its parent).

        Args
        ----
            pop_density (float): The population density, defined as the
                current bacteria population divided by the maximum population

        Returns
        -------
            childBacteria (SimpleBacteria): A new instance representing the
              offspring of this bacteria cell (if the bacteria reproduces). The
              child should have the same birth_prob and death_prob values as
              this bacteria.

        Raises
        ------
            NoChildException if this bacteria cell does not reproduce.

        """
#
#  Parameter validation section
#
        if type(pop_density) != float:
            raise TypeError('Pop_density must be a float')
        if pop_density < 0.0 or pop_density > 1.0:
            raise ValueError('Pop_density must be beteen 0.0 and 1.0')

        randomBirthEvent = random.random()  # generate random event prob

#
#  Compare the randomBirthEvent with the birth probability which is a function
#  of the birth probability and population density. If the event predicts a
#  birth, return a SimpleBacteria object with the parent's birth and death
#  probability. Else generate a NoChildException custom exception
#
        if not self.killed: # if bacterium is not already dead
            if randomBirthEvent <= self.birth_prob * (1.0 - pop_density):
                childBacteria = SimpleBacteria(self.birth_prob,
                                               self.death_prob)
                return childBacteria
            # else:
            #     try:
            #         raise NoChildException('No Child Bacteria Generated')
            #     except NoChildException as e:
            #         print('Catched NoChildException: {}'.format(e))

        pass  # TODO


class Patient(object):
    """
    Representation of a simplified patient.

    The patient does not take any
    antibiotics and his/her bacteria populations have no antibiotic resistance.
    """

    def __init__(self, bacteria, max_pop) -> None:
        """
        Class constructor.

        Args
        ----
            bacteria (list of SimpleBacteria): The bacteria in the population
            max_pop (int): Maximum possible bacteria population size for
                this patient

        Returns
        -------
            None
        """
#
#  Parameter validation section
#
        if type(bacteria) != list:
            raise TypeError('Patient bacteria parameter must be a list')
        if type(max_pop) != int:
            raise TypeError('Patient max_pop parameter must be an int')
        if max_pop <= 0:
            raise ValueError('Patient max_pop parameter must be > 0')

        self.bacteria = bacteria  # not sure a copy or reference needed
        self.max_pop = max_pop

        pass  # TODO

    def get_total_pop(self) -> int:
        """
        Get the size of the current total bacteria population.

        Returns
        -------
            int: The total bacteria population
        """
        count = 0
        for i in range(len(self.bacteria)):
            if not self.bacteria[i].killed:
                count += 1
        return count
        pass  # TODO

    def update(self) -> None:
        """
        Update the patient's bacteria population state for a time step.

        Update() should execute the following steps in
        this order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. Calculate the current population density by dividing the surviving
           bacteria population by the maximum population. This population
           density value is used for the following steps until the next call
           to update()

        3. Based on the population density, determine whether each surviving
           bacteria cell should reproduce and add offspring bacteria cells to
           a list of bacteria in this patient. New offspring do not reproduce.

        4. Reassign the patient's bacteria list to be the list of surviving
           bacteria and new offspring bacteria

        Returns
        -------
            int: The total bacteria population at the end of the update
        """
#
#  Step 1. Update bacteria list pruning off dead bacteria
#
        listOriginalLen = len(self.bacteria)  # Save the original list len
        for listItem in range(listOriginalLen):  # process bacteria list
            if not self.bacteria[listItem].killed:  # prevents killing dead
                if self.bacteria[listItem].is_killed():  # determine if time to kill
                    self.bacteria[listItem].killBacteria()  # kill bacteria

#
#  Step 2. Update current population density based upon processed bacteria list
#
        self.currentPopulationDensity = float(self.get_total_pop()) / \
            float(self.max_pop)

#
#  Step 3. Generate updated bacteria list that includes produced children
#
        newBacteriaList = []
        for bacterium in self.bacteria:
            childBacterium = bacterium.reproduce(self.currentPopulationDensity)
            newBacteriaList.append(bacterium)
            if childBacterium:
                newBacteriaList.append(childBacterium)

#
#  Step 4. Update patient's self.bacteria list to the updated newBacteria list
#
        self.bacteria = newBacteriaList

        return len(self.bacteria)  # return total bacteria pop count
        pass  # TODO


##########################
# PROBLEM 2
##########################

def calc_pop_avg(populations, n) -> float:
    """
    Find the average bacteria population size across trials at time step n.

    Args
    ----
        populations (list): (list of lists or 2D array): populations[i][j] is
          the number of bacteria in trial i at time step j
        n (int): time step number

    Returns
    -------
        avgBacteriaPop (float): The average bacteria population size at time
          step n

    """
    numTrials = len(populations)
    numSteps = len(populations[0])
    totalBacteriaPopSlice = 0.0
    if n > numSteps:
        raise ValueError('n (timestep number) exceeds number \
                         of timesteps in pop')

    for trialNum in range(numTrials):
        totalBacteriaPopSlice += populations[trialNum][n]
    avgBacteriaPop = float(totalBacteriaPopSlice / numTrials)
    return avgBacteriaPop

    pass  # TODO


def simulation_without_antibiotic(num_bacteria,
                                  max_pop,
                                  birth_prob,
                                  death_prob,
                                  num_trials) -> list:
    """
    Run the simulation and plot the graph for problem 2.

    No antibiotics are used, and bacteria do not have any antibiotic
    resistance.

    For each of num_trials trials:
        * instantiate a list of SimpleBacteria
        * instantiate a Patient using the list of SimpleBacteria
        * simulate changes to the bacteria population for 300 timesteps,
          recording the bacteria population after each time step. Note
          that the first time step should contain the starting number of
          bacteria in the patient

    Then, plot the average bacteria population size (y-axis) as a function of
    elapsed time steps (x-axis) You might find the make_one_curve_plot
    function useful.

    Args
    ----
        num_bacteria (int): number of SimpleBacteria to create for patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float in [0, 1]): maximum reproduction probability
        death_prob (float in [0, 1]): maximum death probability
        num_trials (int): number of simulation runs to execute

    Returns
    -------
        populations (list of lists or 2D array)

    """
#
#  Parameter Validation Section
#
    if type(num_bacteria) != int:
        raise TypeError('num_bacteria must be an int')
    if num_bacteria < 1:
        raise ValueError('num_bacteria must be > 0')
    if type(max_pop) != int:
        raise TypeError('max_pop must be an int')
    if max_pop < 1:
        raise ValueError('max_pop must be > 0')
    if type(birth_prob) != float:
        raise TypeError('birth_prob must be a float')
    if not 0.0 <= birth_prob <= 1.0:
        raise ValueError('birth_prob must be between 0.0 and 1.0')
    if type(death_prob) != float:
        raise TypeError('death_prob must be a float')
    if not 0.0 <= death_prob <= 1.0:
        raise ValueError('death_prob must be between 0.0 and 1.0')
    if type(num_trials) != int:
        raise TypeError('num_trials must be an int')
    if num_trials < 1:
        raise ValueError('num_trials must be > 0')

    _numTimeSteps = 300
    timeSteps, trials = [], []

    for trial in range(num_trials):
        bacteriaCount = []  # initialize bacteria counts area for trial
        print('Trial number:', trial)
#
#  Step 1: Instantiate a list of SimpleBacteria
#
        bacteria = []  # create empty list for bacteria
        for i in range(num_bacteria):
            bacterium = SimpleBacteria(birth_prob, death_prob)  # create singleton
            bacteria.append(bacterium)  # add the bacterium to the  list

#
#  Step 2: Instantiate a Patient using the list of SimpleBacteria
#
        patient = Patient(bacteria, max_pop)

#
#  Step 3: Simulate changes to the bacteria population for 300 timesteps,
#          recording the bacteria population after each time step.
#
        bacteriaCount.append(num_bacteria)
        for i in range(1, _numTimeSteps):
            # Update the patient bacteria population for this timestep
            bacUpdateCount = patient.update()
            #  Capture live bacteria population counts for this time step
            bacteriaCount.append(patient.get_total_pop())
        trials.append(bacteriaCount)  # capture the bacteria growth for trial
#
#  Step 4: Plot Results
#
#
# calculate bacteria time step averages across trials (Y-axis numbers)
# and also generate time steps indces across trials (X-axis numbers)
#
    bacteriaStepAvgs = []
    for stepNum in range(_numTimeSteps):
        bacteriaStepAvgs.append(calc_pop_avg(trials, stepNum))
        timeSteps.append(stepNum)

    make_one_curve_plot(timeSteps, bacteriaStepAvgs, 'Time Steps',
                        'Bacteria Average Population',
                        'Simulation Without Antibiotic')

#
#  Step 5: Return Trials (which is the bacteria population counts for each
#          time step for each trial (trials[num_trials][_numTimeSteps]))
#
    return trials
    pass  # TODO


# When you are ready to run the simulation, uncomment the next line
populations = simulation_without_antibiotic(100, 1000, 0.1, 0.025, 50)

##########################
# PROBLEM 3
##########################

def calc_pop_std(populations, t) -> float:
    """
    Calculate standard deviation of population time slice across trials.

    Finds the standard deviation of populations across different trials
    at time step t by:
        * calculating the average population at time step t
        * compute average squared distance of the data points from the average
          and take its square root

    You may not use third-party functions that calculate standard deviation,
    such as numpy.std. Other built-in or third-party functions that do not
    calculate standard deviation may be used.

    Args
    ----
        populations (list): (list of lists or 2D array): populations[i][j] is
            the number of bacteria present in trial i at time step j
        t (int): time step slice index

    Returns
    -------
        (float): the standard deviation of populations across different
            trials at a specific time step

    """
    numTrials = len(populations)  # determine number of trials in populations
    numSteps = len(populations[0])  # determine times steps per trials
    sumDifferences = 0.0  # initialize
    if t > numSteps:  # check time slice index not exceeding num time slices
        raise ValueError('n (timestep number) exceeds number \
                         of timesteps in pop')

    sliceXBar = calc_pop_avg(populations, t)  # calcualte time slice XBar

    for trial in range(numTrials):  # calculate differences of samples
        sumDifferences += (populations[trial][t] - sliceXBar)**2
    return float(math.sqrt(sumDifferences / numTrials))
    pass  # TODO


def calc_95_ci(populations, t) -> tuple:
    """
    Find 95% confidence interval around the average bacteria population.

    At time t by:
        * computing the mean and standard deviation of the sample
        * using the standard deviation of the sample to estimate the
          standard error of the mean (SEM)
        * using the SEM to construct confidence intervals around the
          sample mean
    Args
    ----
        populations (list): 2D array of bacteria population samples
        t (int): time step

    Returns
    -------
        tuple (mean, width):
            mean (float): the sample mean
            width (float): 1.96 * SEM

    """
    numTrials = len(populations)  # determine number of trials in populations
    numSteps = len(populations[0])  # determine times steps per trials
    if t > numSteps:  # check time slice index not exceeding num time slices
        raise ValueError('n (timestep number) exceeds number \
                         of timesteps in pop')

    sliceXBar = calc_pop_avg(populations, t)  # calcualte time slice XBar

    sliceSD = calc_pop_std(populations, t)  # calculate time slice stddev

    sliceSEM = sliceSD / (math.sqrt(numTrials))

    return (sliceXBar, (1.96 * sliceSEM))
    pass  # TODO


calc_std = calc_pop_std(populations, 299)
print('\nStandard Diviation of Time Step 299: ', round(calc_std, 5))
c_avg, calc_ci_95 = calc_95_ci(populations, 299)
print('95% Confidence Interval of Time Step 299: {', c_avg -
        round(calc_ci_95, 5), ', ', c_avg + round(calc_ci_95, 5), '}')

##########################
# PROBLEM 4
##########################


class ResistantBacteria(SimpleBacteria):
    """A bacteria cell that can have antibiotic resistance."""

    def __init__(self, birth_prob, death_prob, resistant, mut_prob) -> None:
        """
        Restistant Bacteria class (subclass of SimpleBacteria) constructor.

        Args
        ----
            birth_prob (float in [0, 1]): reproduction probability
            death_prob (float in [0, 1]): death probability
            resistant (bool): whether this bacteria has antibiotic resistance
            mut_prob (float in [0, 1]): mutation probability for this bacteria
                     cell. This is the maximum probability of the offspring
                     acquiring antibiotic resistance

        Returns
        -------
            None.

        """
        SimpleBacteria.__init__(self, birth_prob, death_prob)
        self.resistant = resistant
        self.mutation_prob = mut_prob
        pass  # TODO

    def get_resistant(self) -> bool:
        """Return whether the bacteria has antibiotic resistance."""
        return self.resistant
        pass  # TODO

    def is_killed(self) -> bool:
        """
        Determine if bacteria is killed in given time step.

        Stochastically determines whether this bacteria cell is killed in
        the patient's body at a given time step.

        Checks whether the bacteria has antibiotic resistance. If resistant,
        the bacteria dies with the regular death probability. If not resistant,
        the bacteria dies with the regular death probability / 4.

        Returns
        -------
            bool: True if the bacteria dies with the appropriate probability
                and False otherwise.
        """
        shouldBeKilled = False  # default return value

        deathEvent = random.random()  # generate stochastic death event

        if deathEvent <= self.death_prob:  # determine if death event is "ripe"
            if self.resistant:  # if bacteria is antibiotic resistant
                shouldBeKilled = True
            # compare non-resistant 1/4 death probability with random death
            # event
            elif deathEvent <= self.death_prob / 4.0:
                shouldBeKilled = True

        return shouldBeKilled
        pass  # TODO

    def reproduce(self, pop_density) -> None:
        """
        Determine if bacteria cell reproduces at a time step.

        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A surviving bacteria cell will reproduce with probability:
        self.birth_prob * (1 - pop_density).

        If the bacteria cell reproduces, then reproduce() creates and returns
        an instance of the offspring ResistantBacteria, which will have the
        same birth_prob, death_prob, and mut_prob values as its parent.

        If the bacteria has antibiotic resistance, the offspring will also be
        resistant. If the bacteria does not have antibiotic resistance, its
        offspring have a probability of self.mut_prob * (1-pop_density) of
        developing that resistance trait. That is, bacteria in less densely
        populated environments have a greater chance of mutating to have
        antibiotic resistance.

        Args
        ----
            pop_density (float): the population density

        Returns
        -------
            ResistantBacteria: an instance representing the offspring of
            this bacteria cell (if the bacteria reproduces). The child should
            have the same birth_prob, death_prob values and mut_prob
            as this bacteria. Otherwise, raises a NoChildException if this
            bacteria cell does not reproduce.
        """
#
#  Parameter validation section
#
        if type(pop_density) != float:
            raise TypeError('Pop_density must be a float')
        if pop_density < 0.0 or pop_density > 1.0:
            raise ValueError('Pop_density must be beteen 0.0 and 1.0')

        randomBirthEvent = random.random()  # generate random event prob

#
#  Compare the randomBirthEvent with the birth probability which is a function
#  of the birth probability and population density. If the event predicts a
#  birth, return a ResistantBacteria object with the parent's birth and death
#  probability. Else generate a NoChildException custom exception
#
        if not self.killed:  # if bacterium is not already dead
            if randomBirthEvent <= self.birth_prob * (1.0 - pop_density):
                isResistant = self.get_resistant()
                if not isResistant:  # if parent bacterium is not resistant
                    # generate random event prob for child bacteria resistance
                    randomResistantEvent = random.random()
                    childResistant = False  # default assumption
                    if randomResistantEvent <= \
                       self.mutation_prob * (1.0 - pop_density):
                        childResistant = True
                    childBacteria = ResistantBacteria(self.birth_prob,
                                                      self.death_prob,
                                                      childResistant,
                                                      self.mutation_prob)
                else:  # resistant parents produce resistant children
                    childBacteria = ResistantBacteria(self.birth_prob,
                                                      self.death_prob,
                                                      isResistant,
                                                      self.mutation_prob)
                return childBacteria
        return None  # return None if parent is dead or not a birth event
        pass  # TODO


class TreatedPatient(Patient):
    """
    Representation of a treated patient.

    The patient is able to take an
    antibiotic and his/her bacteria population can acquire antibiotic
    resistance. The patient cannot go off an antibiotic once on it.
    """

    def __init__(self, bacteria, max_pop) -> None:
        """
        Class constructor.

        This function should initialize self.on_antibiotic, which represents
        whether a patient has been given an antibiotic. Initially, the
        patient has not been given an antibiotic.

        Don't forget to call Patient's __init__ method at the start of this
        method.

        Args
        ----
            bacteria (list): The list representing the bacteria population
                             (a list of bacteria instances)
            max_pop (int): The maximum bacteria population for this patient
        """
        Patient.__init__(self, bacteria, max_pop)
        self.on_antibiotic = False
        pass  # TODO

    def set_on_antibiotic(self) -> bool:
        """
        Administer an antibiotic to this patient.

        The antibiotic acts on the bacteria population for all subsequent time
        steps.

        Return
        ------
            self.on_antibiotic (bool): Current patient antibiotic state
        """
        self.on_antibiotic = True
        return self.on_antibiotic
        pass  # TODO

    def get_resist_pop(self)->int:
        """
        Get the population size of bacteria cells with antibiotic resistance.

        Returns
        -------
            int: the number of bacteria with antibiotic resistance
        """
        numBacteria = 0
        for bacterium in self.bacteria:
            if bacterium.get_resistant() and not bacterium.killed:
                numBacteria += 1
        return numBacteria
        pass  # TODO

    def update(self)->int:
        """
        Update the bacteria population state for this patient.

        For a single time step. update() should execute these
        actions in order:

            1. Determine whether each bacteria cell dies (according to the
               is_killed method) and create a new list of surviving bacteria
               cells.

            2. If the patient is on antibiotics, the surviving bacteria cells
               from (1) only survive further if they are resistant. If the
               patient is not on the antibiotic, keep all surviving bacteria
               cells from (1).

            3. Calculate the current population density. This value is used
               until the next call to update(). Use the same calculation as
               in Patient.

            4. Based on this value of population density, determine whether
               each surviving bacteria cell should reproduce and add offspring
               bacteria cells to the list of bacteria in this patient.

            5. Reassign the patient's bacteria list to be the list of survived
               bacteria and new offspring bacteria.

        Returns
        -------
           bacteriaCnt (int): Total bacteria population at the end of the
                              update
        """
#
#  Step 1. Update bacteria list marking off dead bacteria
#
        listOriginalLen = len(self.bacteria)  # Save the original list len
        for listItem in range(listOriginalLen):  # process bacteria list
            if not self.bacteria[listItem].killed:  # prevents killing dead
                if self.bacteria[listItem].is_killed():  # is time to kill?
                    self.bacteria[listItem].killBacteria()  # kill bacteria

#
#  Step 2a. Generate new bacteria list from old based on whether the patient
#          is on antibiotics and whether the bacterim is antibiotics resistent
#
        newBacteriaList = []
        if self.on_antibiotic:  # determine if patient is on antibiotics
            for bacterium in self.bacteria:
                if bacterium.get_resistant() and not bacterium.killed:
                    newBacteriaList.append(bacterium)
        else:  # patient is not on antibiotics
            for bacterium in self.bacteria:
                if not bacterium.killed:
                    newBacteriaList.append(bacterium)
#
#   Step 2b. Update patient's bacteria pop with newly processed list
#
        self.bacteria = newBacteriaList

#
#  Step 3. Update current population density based upon processed bacteria list
#
        self.currentPopulationDensity = float(self.get_total_pop()) / \
            float(self.max_pop)

#
#   Step 4. Deterine which living bacteria should reproduce
#
        newBacteriaList = []
        for bacterium in self.bacteria:
            childBacterium = bacterium.reproduce(self.currentPopulationDensity)
            newBacteriaList.append(bacterium)
            if childBacterium:
                newBacteriaList.append(childBacterium)
#
#  Step 5. Update patient's self.bacteria list to the updated newBacteria list
#
        self.bacteria = newBacteriaList

        return len(self.bacteria)  # return total bacteria pop count
        pass  # TODO


##########################
# PROBLEM 5
##########################

def simulation_with_antibiotic(num_bacteria,
                               max_pop,
                               birth_prob,
                               death_prob,
                               resistant,
                               mut_prob,
                               num_trials) -> list:
    """
    Run simulations and plots graphs for problem 4.

    For each of num_trials trials:
        * instantiate a list of ResistantBacteria
        * instantiate a patient
        * run a simulation for 150 timesteps, add the antibiotic, and run the
          simulation for an additional 250 timesteps, recording the total
          bacteria population and the resistance bacteria population after
          each time step

    Plot the average bacteria population size for both the total bacteria
    population and the antibiotic-resistant bacteria population (y-axis) as a
    function of elapsed time steps (x-axis) on the same plot. You might find
    the helper function make_two_curve_plot helpful

    Args
    ----
        num_bacteria (int): number of ResistantBacteria to create for
            the patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float int [0-1]): reproduction probability
        death_prob (float in [0, 1]): probability of a bacteria cell dying
        resistant (bool): whether the bacteria initially have
            antibiotic resistance
        mut_prob (float in [0, 1]): mutation probability for the
            ResistantBacteria cells
        num_trials (int): number of simulation runs to execute

    Returns
    -------
        a tuple of two lists of lists, or two 2D arrays
        populations (list of lists or 2D array): the total number of bacteria
            at each time step for each trial; total_population[i][j] is the
            total population for trial i at time step j
        resistant_pop (list of lists or 2D array): the total number of
            resistant bacteria at each time step for each trial;
            resistant_pop[i][j] is the number of resistant bacteria for
            trial i at time step j
    """
#
#  Parameter Validation Section
#
    if type(num_bacteria) != int:
        raise TypeError('num_bacteria must be an int')
    if num_bacteria < 1:
        raise ValueError('num_bacteria must be > 0')
    if type(max_pop) != int:
        raise TypeError('max_pop must be an int')
    if max_pop < 1:
        raise ValueError('max_pop must be > 0')
    if type(birth_prob) != float:
        raise TypeError('birth_prob must be a float')
    if not 0.0 <= birth_prob <= 1.0:
        raise ValueError('birth_prob must be between 0.0 and 1.0')
    if type(death_prob) != float:
        raise TypeError('death_prob must be a float')
    if not 0.0 <= death_prob <= 1.0:
        raise ValueError('death_prob must be between 0.0 and 1.0')
    if type(resistant) != bool:
        raise TypeError('Resistant flag must be a bool')
    if type(mut_prob) != float:
        raise TypeError('mutant probability must be a float')
    if not 0.0 <= mut_prob <= 1.0:
        raise ValueError('mutant probability must be between 0.0 and 1.0')
    if type(num_trials) != int:
        raise TypeError('num_trials must be an int')
    if num_trials < 1:
        raise ValueError('num_trials must be > 0')

    _untreatedNumTimeSteps = 150
    _treatedNumTimeSteps = 250
    timeSteps, trialsPopTotals, trialsPopResist = [], [], []

    for trial in range(num_trials):
        bacteriaCount = []  # initialize bacteria counts area for trial
        resistBacteriaCnt = []
        print('Trial number:', trial)
#
#  Step 1: Instantiate a list of ResistantBacteria
#
        bacteria = []  # create empty list for bacteria
        for i in range(num_bacteria):
            bacterium = ResistantBacteria(birth_prob,
                                          death_prob,
                                          resistant,
                                          mut_prob)  # create singleton
            bacteria.append(bacterium)  # add the bacterium to the  list

#
#   Step 2. Instantiate a TreatedPatient using the list of ResistantBacteria
#
        patient = TreatedPatient(bacteria, max_pop)

#
#  Step 3: Simulate changes to the bacteria population for 300 timesteps,
#          recording the bacteria population after each time step.
#
        bacteriaCount.append(num_bacteria)
        resistBacteriaCnt.append(patient.get_resist_pop())
        
#
#  Step 3a. Untreated patient portion of trial simulation
#
        for timeStep in range(1, _untreatedNumTimeSteps):
            # Update the patient bacteria population for this timestep
            bacUpdateCount = patient.update()
            #  Capture live bacteria population counts for this time step
            bacteriaCount.append(patient.get_total_pop())
            resistBacteriaCnt.append(patient.get_resist_pop())
#
#  Step 3b. Treated patient portion of trial simulation
#
        isInnoculated = patient.set_on_antibiotic()
        for timeStep in range(_treatedNumTimeSteps):
            # Update the patient bacteria population for this timestep
            bacUpdateCount = patient.update()
            #  Capture live bacteria population counts for this time step
            bacteriaCount.append(patient.get_total_pop())
            resistBacteriaCnt.append(patient.get_resist_pop())
            
#
#  Capture bacteria count results
#
        trialsPopTotals.append(bacteriaCount)  # capt bacteria growth 4 trial
        trialsPopResist.append(resistBacteriaCnt)  # capture resist bact growth

#  Step 4: Plot Results
#
#
# calculate bacteria time step averages across trials (Y-axis numbers)
# and also generate time steps indces across trials (X-axis numbers)
#
    bacteriaStepAvgs = []
    resistBacteriaStepAvgs = []
    for stepNum in range(_untreatedNumTimeSteps+_treatedNumTimeSteps):
        bacteriaStepAvgs.append(calc_pop_avg(trialsPopTotals, stepNum))
        resistBacteriaStepAvgs.append(calc_pop_avg(trialsPopResist, stepNum))
        timeSteps.append(stepNum)

    # make_one_curve_plot(timeSteps, bacteriaStepAvgs, 'Time Steps',
    #                     'Bacteria Average Population',
    #                     'Simulation with Antibiotic')

    # make_one_curve_plot(timeSteps, resistBacteriaStepAvgs, 'Time Steps',
    #                     'Resistant Bacteria Average Population',
    #                     'Simulation with Antibiotic')

    make_two_curve_plot(timeSteps,
                        bacteriaStepAvgs,
                        resistBacteriaStepAvgs,
                        'Total Bacteria',
                        'Resistant Bacteria',
                        'Time Steps',
                        'Bacteria Average Population',
                        'Simulation with Antibiotic')
#
#  Step 5: Return Trials (which is the bacteria population counts for each
#          time step for each trial (trials[num_trials][_numTimeSteps]))
#
    return trialsPopTotals, trialsPopResist
    pass  # TODO


# When you are ready to run the simulations, uncomment the next lines one
# at a time
print('Simulations with Patient with antibiotics and resistant bacteria')
trialsPopTotals, trialsPopResist = simulation_with_antibiotic(num_bacteria=100,
                                                              max_pop=1000,
                                                              birth_prob=0.3,
                                                              death_prob=0.2,
                                                              resistant=False,
                                                              mut_prob=0.8,
                                                              num_trials=50)

calc_std = calc_pop_std(trialsPopTotals, 100)
print('\nStandard Diviation of Time Step 100 for all Bacteria in simulation \
of birth rate greater than death rate:',
      round(calc_std, 5))
c_avg, calc_ci_95 = calc_95_ci(trialsPopTotals, 100)
print('95% Confidence Interval of Time Step 100 for all Bacteria: {',
      c_avg - round(calc_ci_95, 5), ', ', c_avg + round(calc_ci_95, 5), '}')

calc_std = calc_pop_std(trialsPopResist, 100)
print('\nStandard Diviation of Time Step 100 for Resistant:',
      round(calc_std, 5))
c_avg, calc_ci_95 = calc_95_ci(trialsPopResist, 100)
print('95% Confidence Interval of Time Step 299 for Resistant: {',
      c_avg - round(calc_ci_95, 5), ', ', c_avg + round(calc_ci_95, 5), '}\n')

calc_std = calc_pop_std(trialsPopTotals, 299)
print('\nStandard Diviation of Time Step 299 for all Bacteria in simulation \
of birth rate greater than death rate:',
      round(calc_std, 5))
c_avg, calc_ci_95 = calc_95_ci(trialsPopTotals, 299)
print('95% Confidence Interval of Time Step 299 for all Bacteria: {',
      c_avg - round(calc_ci_95, 5), ', ', c_avg + round(calc_ci_95, 5), '}')

calc_std = calc_pop_std(trialsPopResist, 299)
print('\nStandard Diviation of Time Step 299 for Resistant:',
      round(calc_std, 5))
c_avg, calc_ci_95 = calc_95_ci(trialsPopResist, 299)
print('95% Confidence Interval of Time Step 299 for Resistant: {',
      c_avg - round(calc_ci_95, 5), ', ', c_avg + round(calc_ci_95, 5), '}\n')


trialsPopTotals, trialsPopResist = simulation_with_antibiotic(num_bacteria=100,
                                                              max_pop=1000,
                                                              birth_prob=0.17,
                                                              death_prob=0.2,
                                                              resistant=False,
                                                              mut_prob=0.8,
                                                              num_trials=50)

calc_std = calc_pop_std(trialsPopTotals, 100)
print('\nStandard Diviation of Time Step 100 for all Bacteria in simulation \
of birth rate less thn death rate:',
      round(calc_std, 5))
c_avg, calc_ci_95 = calc_95_ci(trialsPopTotals, 100)
print('95% Confidence Interval of Time Step 100 for all Bacteria: {',
      c_avg - round(calc_ci_95, 5), ', ', c_avg + round(calc_ci_95, 5), '}')

calc_std = calc_pop_std(trialsPopResist, 100)
print('\nStandard Diviation of Time Step 100 for Resistant: ',
      round(calc_std, 5))
c_avg, calc_ci_95 = calc_95_ci(trialsPopResist, 100)
print('95% Confidence Interval of Time Step 100 for Resistant: {',
      c_avg - round(calc_ci_95, 5), ', ', c_avg + round(calc_ci_95, 5), '}\n')

calc_std = calc_pop_std(trialsPopTotals, 299)
print('\nStandard Diviation of Time Step 299 for all Bacteria in simulation \
of birth rate less thn death rate:',
      round(calc_std, 5))
c_avg, calc_ci_95 = calc_95_ci(trialsPopTotals, 299)
print('95% Confidence Interval of Time Step 299 for all Bacteria: {',
      c_avg - round(calc_ci_95, 5), ', ', c_avg + round(calc_ci_95, 5), '}')

calc_std = calc_pop_std(trialsPopResist, 299)
print('\nStandard Diviation of Time Step 299 for Resistant: ',
      round(calc_std, 5))
c_avg, calc_ci_95 = calc_95_ci(trialsPopResist, 299)
print('95% Confidence Interval of Time Step 299 for Resistant: {',
      c_avg - round(calc_ci_95, 5), ', ', c_avg + round(calc_ci_95, 5), '}\n')
