# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: Clarke Homan
# Collaborators (discussion):
# Date: March 8, 2021
# Time:

# import pyforest
import pylab
import numpy as np
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

SW_CITIES = ['SAN DIEGO', 'PHOENIX', 'DALLAS',
             'ALBUQUERQUE', 'LOS ANGELES', 'LAS VEGAS']

NONCOMMONREGION_CIITES = ['BOSTON',
                          'SEATTLE',
                          'SAN DIEGO',
    
                          'MIAMI',
                          'NEW ORLEANS',
                          'ST LOUIS']

TRAINING_INTERVAL = range(1961, 2010)
TRAINING_INTERVAL1 = range(1961, 2016)
TESTING_INTERVAL = range(2010, 2016)

MODEL_ORDER = {1: 'Linear',
               2: 'Quardatic',
               3: 'Cubic',
               4: 'Fourth',
               5: 'Fifth',
               6: 'Sixth',
               7: 'Seventh',
               8: 'Eighth',
               9: 'Ninth',
               10: 'Tenth',
               11: 'Eleventh',
               12: 'Twelfth',
               13: 'Thirthteenth',
               14: 'Fourteenth',
               15: 'Fifthteenth',
               16: 'Sixtheenth',
               17: 'Seventeenth',
               18: 'Eighteenth',
               19: 'Nineteenth',
               20: 'Twentieth'}

"""
Begin helper code
"""


class Climate():
    """The collection of temperature records loaded from given csv file."""

    def __init__(self, filename):
        """
        Initialize a Climate instance.

        Which stores the temperature records
        loaded from a given csv file specified by filename.

        Args
        ----
            filename: name of the csv file (str)
        """
        # rawdata: 4-D dictionary of city,year,month,day of recorded temps
        self.rawdata = {}

        try:  # safely try to open supplied file
            f = open(filename, 'r')
        except FileNotFoundError:
            print('File: ', filename, 'not found or permissions')

        header = f.readline().strip().split(',')  # skip past header line
        for line in f:
            items = line.strip().split(',')  # split line into 3 items

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)',
                            items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
#
#  Dynamically create dictionary entries for city, year, month and day if
#  not already defined previously
#
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
#
#  Record tempature for specific city, year, month and day
#
            self.rawdata[city][year][month][day] = temperature

        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args
        ----
            city: city name (str)
            year: the year to get the data for (int)

        Returns
        -------
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        #
        for month in self.rawdata[city][year]:
            for day in self.rawdata[city][year][month]:
                temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args
        ----
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns
        -------
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], \
               "provided month is not available"
        assert day in self.rawdata[city][year][month], \
               "provided day is not available"
        return self.rawdata[city][year][month][day]



def se_over_slope(x, y, estimated, model):
    """
    Linear regression model, calculates ratio of SE to curve's slope.

    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.

    Args
    ----
        x (1-d pylab array with length N): represents the x-coordinates of
            the N sample points
        y (1-d pylab array with length N): represents the y-coordinates of
            the N sample points
        estimated (1-d pylab array of values): estimated by a linear
            regression model
        model (pylab array): storing the coefficients of a linear regression
            model

    Returns
    -------
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]


"""
End helper code
"""


def generate_models(x, y, degs):
    """
    Generate regression models that fit x and y vectors.

    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args
    ----
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points. In this case, x is an array of integer Years.
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points. In this case, y is an array of float
            Tempatures.
        degs: a list of integer degrees of the fitting polynomial

    Returns
    -------
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    #
    #  Paramter validation section
    #
    assert type(x) and type(y) is np.ndarray
    assert len(x) == len(y)
    assert type(degs) is list
    assert len(degs) > 0

    retArrays = []  # return array
    for deg in degs:  # rifle thru list of degrees generating fit coefficients
        fit = pylab.polyfit(x, y, deg)
        retArrays.append(fit)
    return retArrays
    # TODO
    # pass


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.

    The R-squared error term, also known as the 'coefficient of
    determination', provides a measure of how well the total variation of
    samples is explained by the model.

    Args
    ----
        y (1-d pylab array with length N): represents the y-coordinates of
           the N sample points
        estimate (1-d pylab array of values with length N): estimated by the
        regression model

    Returns
    -------
        a float for the R-squared error term
    """
    #
    #  Paramter validation section
    #
    assert type(y) and type(estimated) is np.ndarray
    assert len(y) == len(estimated)

#
#  Calculate numerator of r-squared term
#
    numerator = sum((y - estimated)**2)
#
#  Calculate denominator of r-squared term (need to calculate yMean as well)
#
    yMean = sum(y) / len(y)
    denominator = sum((y - yMean)**2)
#
#  Put rSquared term together and return rSquared
#
    rSquared = float(1 - (numerator / denominator))
    return rSquared
    # TODO
    # pass


def evaluate_models_on_training(x, y, models, cityName, monthDay,
                                movingAvg=False):
    """
    Compute and plot r-squared values for each supplied model for a city.

    For each regression model, compute the R-squared value for this model with
    the standard error over slope of a linear regression line (only if the
    model is linear), and plot the data along with the best fit curve. Actual
    temps identified in legend if movingAvg is False. Otherwise, line legend
    entry identifies data as moving average

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope).

    Args
    ----
        x (1-d pylab array with length N): represents the x-coordinates of
            the N sample points
        y (1-d pylab array with length N): represents the y-coordinates of
            the N sample points
        models (list of pylab arrays):  each array are regression coefficients
        of a polynomial to apply to data (generated by function
                                          generate_models)
        cityName (str): name of city
        monthDay (str): month and day

    Returns
    -------
        None
    """
    #
    #  Paramter validation section
    #
    assert type(x) and type(y) is np.ndarray
    assert len(x) == len(y)

    if movingAvg is False:
        plotLabel = 'Training Data Actual temperatures (C)'
    else:
        plotLabel = 'Training Data 5-year moving\naverage temperatures (C)'

    numModels = len(models)

    for i in range(numModels):  # process each regression model
        predictedTemperatures = 0.0
        # if i == 0:  # linear regression model
        pylab.plot(x, y, 'bo', label=plotLabel)
        #
        # generate predicted temperatures
        #
        numCoefficents = len(models[i])
        for j in range(numCoefficents-1):
            predictedTemperatures += models[i][j] * \
                (x**(numCoefficents - 1 - j))
        predictedTemperatures += models[i][numCoefficents-1]

        rSquared = round(r_squared(y, predictedTemperatures), 5)
        if numCoefficents == 2:  # linear model
            #
            #  Calculate Standard Error to Fitted Curve Ratio
            #
            SEFittedCurveRatioratio = round(se_over_slope(x, y,
                                            predictedTemperatures,
                                            models[0]), 5)
            #
            #  Format the plot title string
            #
            plotTitle = cityName + ' Temperatures for ' + monthDay + \
                ' over the years\n' + \
                str(MODEL_ORDER[numCoefficents-1]) + ' Regression Modeling\n' \
                + 'Model R-Squared Value: ' + str(rSquared) + '\n' + \
                'Standard Error over Slope Ratio: ' + \
                str(SEFittedCurveRatioratio)
        else:  # non-linear regression model
            plotTitle = cityName + ' Temperatures for ' + monthDay + \
                ' over the years\n' + str(MODEL_ORDER[numCoefficents-1]) + \
                ' order Regression Modeling\n' + \
                'Model R-Squared Value: ' + str(rSquared)

        pylab.title(plotTitle)

        # plot predicted temperatures
        pylab.plot(x, predictedTemperatures, 'r-',
                   label='Predicted temperatures (C) \n by ' +
                   str(MODEL_ORDER[numCoefficents-1]) + ' order model')
        pylab.legend(loc='best')
        pylab.figure()  # change plot figure for subsequent plots
    # TODO
    # pass


def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args
    ----
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns
    -------
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperatyture over the given
        cities for a given year.
    """
    assert type(multi_cities) is list
    # assert type(years) is range


    averageTemps = []
    # loop thru each year in the training interval
    for year in years:
        nationalAvg = 0.0
        for city in multi_cities:  # loop thru each city
            cityYearlyTemperatures = climate.get_yearly_temp(city, year)
            nationalAvg += sum(cityYearlyTemperatures) / \
                len(cityYearlyTemperatures)
            # nationalAvg += cityYearlyAvg
        nationalAvg = nationalAvg / len(multi_cities)
        averageTemps.append(nationalAvg)  # add national avg to list

    nationalTempsArray = np.array(averageTemps)
    return nationalTempsArray
    # TODO
    pass


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args
    ----
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns
    -------
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    #
    #  Paramter validation section
    #
    assert type(y) is list
    assert len(y) > 0
    assert type(window_length) is int
    assert window_length > 0

    yCoordinates = np.array(y)  # convert y list to proper array
    tempAvg = []
    for i in range(len(yCoordinates)):  # slide the window over yCoordinates
        leftIndex = max((i - window_length + 1), 0)
        rightIndex = i+1
        tempAvg.append(sum(yCoordinates[leftIndex:rightIndex]) /
                       (rightIndex - leftIndex))
    return np.array(tempAvg)
    # TODO
    # pass


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args
    ----
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns
    -------
        a float for the root mean square error term
    """
    #
    #  Paramter validation section
    #
    assert type(y) and type(estimated) is np.ndarray
    assert len(y) and len(estimated) > 0
    assert len(y) == len(estimated)

    #
    #  Calculate the RMSE term which measures the deviation  between predicted
    #  values generated from models develoved on training data with actual
    #  values
    #
    # RMSE = sqrt((sum(Yi - Ei)**2)/N)
    #
    # Steps:
    #  1. Calculate numerator (sum of (difference between actual versus
    #                          predicted) ** 2
    #  2. Determine N to be vector length of Actuals
    #  3. Divide the Numerator by denominator (yielding variance)
    #  4. Take square root of dividend yielding rmse (yielding RMSE or SD of
    #     error)
    #  5. Return rmse
    #
    numerator = sum((y - estimated)**2)
    denominator = len(y)
    rmse = (numerator / denominator) ** 0.5
    return rmse
    # TODO
    # pass


def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged
    yearly temperatures for each city in multi_cities.

    Args
    ----
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev
        calculation (list of str) years: the range of years to calculate
        standard deviation for (list of int)

    Returns
    -------
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual
        city temperatures for the given cities in a given year.
    """
    # TODO
    assert type(multi_cities) is list
    # assert type(years) is range

    #
    # nationalAvg is the average temps for all cities for a given year
    # cityDailyTemperatures is array of daily temps for a city for a given year
    # averageTemps is the list of annual average temps for all cities
    # nationalVariance is the variance of allCitiesDailyTemps from average for
    #   that day
    # nationalTempsSDArray is array of SD
    #
    averageTemps = []
    cityTempsDeviance = []
    yearlyNationalVariance = []
    nationalTempsSDArray = []
    # loop thru each year in the training interval
    for year in years:
        nationalAvg = 0.0
        nationalVariance = pylab.array([0])
        allCitiesDailyTemps = pylab.array([0])
        for city in multi_cities:  # loop thru each city
            cityDailyTemperatures = climate.get_yearly_temp(city, year)
            allCitiesDailyTemps = allCitiesDailyTemps + cityDailyTemperatures
        allCitiesDailyTemps = allCitiesDailyTemps / len(multi_cities)

        nationalAvgTemp = sum(allCitiesDailyTemps) / len(cityDailyTemperatures)

        nationalVariance = sum((allCitiesDailyTemps - nationalAvgTemp)**2)
        nationalVariance /= len(allCitiesDailyTemps)
        nationalTempsSDArray.append(nationalVariance**0.5) # take sqrt of var
    return nationalTempsSDArray
        

    # nationalTempsArray = np.array(averageTemps)
    # return nationalTempsArray
    pass

def evaluate_models_on_testing(x, y, models, cityName, monthDay,
                               movingAvg=False):
    """
    Compute RMSE value for each model and plot actual and predicted data.

    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points.

    Args
    ----
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.
        cityName (str): name of city
        monthDay (str): month and day
        movingAvg (Boolean): flag to enable moving average

    Returns
    -------
        None
    """
    assert type(x) and type(y) is np.ndarray
    assert len(x) == len(y)
    # assert type(models) is list

    if movingAvg is False:
        plotLabel = 'Training Data Actual temperatures (C)'
    else:
        plotLabel = 'Training Data 5-year moving\naverage temperatures (C)'

    numModels = len(models)

    for i in range(numModels):  # process each regression model
        predictedTemperatures = 0.0
        # if i == 0:  # linear regression model
        pylab.plot(x, y, 'bo', label=plotLabel)
        #
        # generate predicted temperatures
        #
        numCoefficents = len(models[i])
        for j in range(numCoefficents-1):
            predictedTemperatures += models[i][j] * \
                (x ** (numCoefficents - 1 - j))
        predictedTemperatures += models[i][numCoefficents-1]

        #  Calculate model RMSE statistic
        modelRMSE = round(rmse(y, predictedTemperatures), 5)

        #
        #  Format the plot title string
        #
        plotTitle = cityName + ' Temperatures for ' + monthDay + \
            ' over the years\n' + \
            str(MODEL_ORDER[numCoefficents-1]) + ' Regression Modeling\n' \
            + 'Model RMSE Value: ' + str(modelRMSE)

        pylab.title(plotTitle)

        # plot predicted temperatures
        pylab.plot(x, predictedTemperatures, 'r-',
                   label='Predicted temperatures (C) \n by ' +
                   str(MODEL_ORDER[numCoefficents-1]) + ' order model')
        pylab.legend(loc='best')
        pylab.figure()  # change plot figure for subsequent plots

    # TODO
    pass


if __name__ == '__main__':

    #   pass
    # Part A.4
    # TODO: replace this line with your code
    #
    #  Import city temperature data from text file
    #
    climatedb = Climate('data.csv')

    # nycTemps = []  # list that will contain daily NYC temps
    # tempsYears = []
    # _JANUARY = 1
    # #
    #  Part A Problem 4.I: January 10 over the years for NYC
    #
    # for year in TRAINING_INTERVAL:
    #     tempsYears.append(year)
    #     nycTemps.append(climatedb.get_daily_temp('NEW YORK', _JANUARY,
    #                                              10, year))
    # nycTempsArray = np.array(nycTemps)
    # nycTempsYearsArray = np.array(tempsYears)

    #
    # Generate the expected models coefficients (1st, 2nd and 3rd order)
    # for NYC temps given sample actuals
    #
    # modelsDegrees = [1, 2, 3]
    # models = generate_models(nycTempsYearsArray, nycTempsArray, modelsDegrees)
    # assert len(models) == len(modelsDegrees)
    # assert type(models) is list
    # assert type(models[0]) is pylab.ndarray

    #
    #  Evaulate and plot the NYC temps (both actuals and expected temps)
    #
    # evaluate_models_on_training(nycTempsYearsArray, nycTempsArray, models,
    #                            'NYC', 'Jan 10')
    #
    #  Part A Problem 4.II: Annual temperature over the years for NYC
    #  Steps:
    #   1. Extract annual temperatures for city for each year in training set
    #   2. Compute average temperature for each year for city in training set
    #   3. Compute linear regression model for averages
    #   4. Generate new plot of actual versus expected (model) averages for NYC
    # avgTempsYears = []
    # tempsYears = []
    # for year in TRAINING_INTERVAL:
    #     tempsYears.append(year)
    #     yearlyTemperatures = climatedb.get_yearly_temp('NEW YORK', year)
    #     yearlyAvg = sum(yearlyTemperatures) / len(yearlyTemperatures)
    #     avgTempsYears.append(yearlyAvg)

    # nycTempsArray = np.array(avgTempsYears)  # convert years list into array
    # nycTempsYearsArray = np.array(tempsYears)  # convert temp avgs into array
    #
    # Generate the expected models coefficients (1st, 2nd and 3rd order)
    # for NYC temps given sample actuals
    #
    # modelsDegrees = [1, 2, 3]
    # models = generate_models(nycTempsYearsArray, nycTempsArray,
    #                          modelsDegrees)
    # assert len(models) == len(modelsDegrees)
    # assert type(models) is list
    # assert type(models[0]) is pylab.ndarray

    #
    #  Evaulate and plot the NYC temps (both actuals and expected temps)
    #
    # evaluate_models_on_training(nycTempsYearsArray, nycTempsArray, models,
    #                           'NYC', 'Average Yearly Temps')

    # Part B (using gen_cities_avg() function to generate annual averages)
    # Annual temperature over the years for multiple cities
    #  Steps:
    #   1. Extract annual temperatures for each city for each year in training
    #      set
    #   2. Compute average temperature for each year for each city in training
    #      set
    #   3. Compute national average temperature for each year based upon
    #      averaging the cities annual average for the year
    #   4. Compute linear regression model for annual averages
    #   5. Generate new plot of actual versus expected (model) averages for
    #      the nation
    # avgNationalTemps = []
    # tempsYears = []

    # tempsYears = list(TRAINING_INTERVAL)
    # avgNationalTemps = gen_cities_avg(climatedb, CITIES, TRAINING_INTERVAL)
    # nationalYearsArray = np.array(tempsYears)
    # #
    # # Generate the expected models coefficients (1st, 2nd and 3rd order)
    # # for national temps given sample actuals
    # #
    # modelsDegrees = [1, 2, 3]
    # models = generate_models(nationalYearsArray, avgNationalTemps,
    #                          modelsDegrees)
    # assert len(models) == len(modelsDegrees)
    # assert type(models) is list
    # assert type(models[0]) is pylab.ndarray

    #
    #  Evaulate and plot the national temps (both actuals and expected temps)
    #
    # evaluate_models_on_training(nationalYearsArray, avgNationalTemps, models,
    #                             'National', 'Average Yearly Temps')

    #
    # Evaluate a particular region: SW US
    #
    # avgNationalTemps = []
    # tempsYears = list(TRAINING_INTERVAL)
    # avgNationalTemps = gen_cities_avg(climatedb, SW_CITIES,
    # TRAINING_INTERVAL)
    # nationalYearsArray = np.array(tempsYears)

    # Generate the expected models coefficients (1st, 2nd and 3rd order)
    # for national temps given sample actuals

    # modelsDegrees = [1, 2, 3]
    # models = generate_models(nationalYearsArray, avgNationalTemps,
    #                           modelsDegrees)
    # assert len(models) == len(modelsDegrees)
    # assert type(models) is list
    # assert type(models[0]) is pylab.ndarray

    # Evaulate and plot the SW Cities temps (both actuals and expected temps)

    # evaluate_models_on_training(nationalYearsArray, avgNationalTemps, models,
    #                             'SW Cities', 'Average Yearly Temps')

    #
    # Evaluate scattered throughout US cities
    #
    # avgNationalTemps = []
    # tempsYears = list(TRAINING_INTERVAL)
    # avgNationalTemps = gen_cities_avg(climatedb, NONCOMMONREGION_CIITES,
    #                                   TRAINING_INTERVAL)
    # nationalYearsArray = np.array(tempsYears)
    #
    # Generate the expected models coefficients (1st, 2nd and 3rd order)
    # for national temps given sample actuals
    #
    # modelsDegrees = [1, 2, 3]
    # models = generate_models(nationalYearsArray, avgNationalTemps,
    #                          modelsDegrees)
    # assert len(models) == len(modelsDegrees)
    # assert type(models) is list
    # assert type(models[0]) is pylab.ndarray

    #
    #  Evaulate and plot the scattered cities temps
    #  (both actuals and expected temps)
    #
    # evaluate_models_on_training(nationalYearsArray, avgNationalTemps, models,
    #                             'Scattered Citites', 'Average Yearly Temps')

    # Part C: 5 Year Moving Average (using moving_average() function)
    # Annual temperature over the years for multiple cities
    #  Steps:
    #   1. Extract annual temperatures for each city for each year in training
    #      set
    #   2. Compute average temperature for each year for each city in training
    #      for each city in training set
    #   3. Compute national average temperature for each year based upon
    #      averaging the cities annual average for the year
    #   4. Compute 5 year moving average for national averages
    #   5. Compute linear regression model for moving averages
    #   6. Generate new plot of actual versus expected (model) moving averages
    #      for the nation
    # avgNationalTemps = []
    # tempsYears = []

    # tempsYears = list(TRAINING_INTERVAL)
    # avgNationalTemps = gen_cities_avg(climatedb, CITIES, TRAINING_INTERVAL)
    # nationalYearsArray = np.array(tempsYears)

    # #
    # #  Generate Moving Averages with differeing window lengths for
    # #  National Average
    # #
    # window_length = 5
    # movingAverage5 = moving_average(avgNationalTemps.tolist(), window_length)

    # window_length = 3
    # movingAverage3 = moving_average(avgNationalTemps.tolist(), window_length)
    # #

    # # Generate the expected models coefficients (1st, 2nd and 3rd order)
    # # for national temps given sample actuals
    # #
    # modelsDegrees = [1, 2, 3]
    # models5 = generate_models(nationalYearsArray, movingAverage5,
    #                           modelsDegrees)

    # models3 = generate_models(nationalYearsArray, movingAverage3,
    #                           modelsDegrees)

    # assert len(models5) == len(modelsDegrees)
    # assert type(models5) is list
    # assert type(models5[0]) is pylab.ndarray

    #
    #  Evaulate and plot the national temps (both actuals and expected temps)
    #
    # evaluate_models_on_training(nationalYearsArray, movingAverage5, models5,
    #                             'National', '5 Year Moving Average', True)

    # evaluate_models_on_training(nationalYearsArray, movingAverage3, models3,
    #                             'National', '3 Year Moving Average', True)

    # TODO: replace this line with your code

    # Part D.2
    #   Problem 2.I: Generate more models
    #   Steps:
    #     1. Using gen_cities_avg():
    #         - Extract annual temperatures for each city in CITIES for each
    #           year in training set (years 1961 - 2009)
    #         - Compute average temperature for each year for each city in
    #           training for each city in training set
    #         - Compute national average temperature for each year based upon
    #           averaging the cities annual average for the year
    #     2. Compute 5 year moving average for national moving averages
    #     3. Compute regression models for moving averages
    #     4. Generate new plot of actual versus expected (model) moving
    #        averages for the nation

    avgNationalTemps = []
    tempsYears = []

    tempsYears = list(TRAINING_INTERVAL)
    nationalYearsArray = np.array(tempsYears)

    # # Step 1:
    avgNationalTemps = gen_cities_avg(climatedb, CITIES, TRAINING_INTERVAL)

    # # Step 2:
    window_length = 10
    movingAverage = moving_average(avgNationalTemps.tolist(), window_length)

    # # Step 3:
    modelsDegrees = [1, 2, 3]
    models = generate_models(nationalYearsArray, movingAverage,
                              modelsDegrees)

    # # Step 4:
    evaluate_models_on_training(nationalYearsArray, movingAverage, models,
                                'National', 'Average Yearly Temps', True)

    #    Problem 2.II  Predict the results
    #    Steps:
    #      1.Compute 5-year moving averages of the national yearly temperature
    #        from 2010-2015 as your test data samples.
    #      2. For each model obtained in the previous problem (i.e., the curves
    #         fit to 5-year moving averages of the national yearly temperature
    #         from 1961-2009 with degree 1, 2, and 20),
    #         evaluate_models_on_testing​ for applying the model and plotting
    #         the results.
    # avgNationalTemps = []
    # tempsYears = []

    # tempsYears = list(TESTING_INTERVAL)
    # nationalYearsArray = np.array(tempsYears)
    # # Step 1:
    # avgNationalTemps = gen_cities_avg(climatedb, CITIES, TESTING_INTERVAL)
    # window_length = 5
    # movingAverageTesting = moving_average(avgNationalTemps.tolist(),
    #                                       window_length)
    # # Step 2:
    # evaluate_models_on_testing(nationalYearsArray, movingAverageTesting,
    #                            models, 'National', 'Average Yearly Temps',
    #                            True)

    #
    # What if we want to model NYC annual temps instead of National
    #
    # tempsYears = list(TRAINING_INTERVAL)
    # nationalYearsArray = np.array(tempsYears)

    # avgNYCTemps = gen_cities_avg(climatedb, ['NEW YORK'], TRAINING_INTERVAL)

    # modelsDegrees = [1, 2, 3, 20]
    # models = generate_models(nationalYearsArray, avgNYCTemps,
    #                          modelsDegrees)

    # evaluate_models_on_training(nationalYearsArray, avgNYCTemps, models,
    #                             'NYC', 'Average Yearly Temps', False)

    # tempsYears = list(TESTING_INTERVAL)
    # nationalYearsArray = np.array(tempsYears)
    # avgNYCtempsTesting = gen_cities_avg(climatedb, ['NEW YORK'],
    #                                     TESTING_INTERVAL)

    # evaluate_models_on_testing(nationalYearsArray, avgNYCtempsTesting,
    #                            models, 'NYC', 'Average Yearly Temps',
    #                            False)
    # TODO: replace this line with your code

    # Part E
    # TODO: replace this line with your code
    climate = Climate('data.csv')
    years = pylab.array(TESTING_INTERVAL)
    tempsSD = gen_std_devs(climate, CITIES, years)

    window_length = 5
    movingAverageTempTesting = moving_average(tempsSD,
                                              window_length)

    modelsDegrees = [1, 2, 3]
    models = generate_models(years, movingAverageTempTesting,
                             modelsDegrees)

    evaluate_models_on_training(years, movingAverageTempTesting, models,
                                'National', 'Temp Std Dev', True)
    pass
