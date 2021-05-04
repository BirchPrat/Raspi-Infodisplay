#Visualizing Temperature
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 
import datetime
from pathlib import Path

def vistemp(path, filetag):
    '''
    Creating and saving plots of temperature data
    Input: filepath and common fileending
    '''

    #importing data and parsing Stringtime and setting Stringtime as index
    path = Path(f'{path}')

    filelist = []
    for filepath in list(path.glob(f'*{filetag}')):
        filelist.append(filepath)

    #print(filelist)

    data = pd.concat((pd.read_csv(f, encoding='utf-8', low_memory=False, parse_dates=(['Stringtime']),index_col=('Stringtime'), na_values = ["F", "failed"]) for f in filelist))
    
    #first glance at data
    #print(data.shape)
    #print(data.head(10), data.tail(10))

    #last 24 hours data selection / the str() is a workaround, because without it raised an error on the pi (not so on windows)
    #last24 = data[str(datetime.datetime.now() - datetime.timedelta(days=1, hours=1)) : str(datetime.datetime.now())]
    last24 = data.sort_index()[(datetime.datetime.now() - datetime.timedelta(days=1, hours=1)) : datetime.datetime.now()]
  
    
    #print(last24)
    #print(last24['Outside Temp -C'])

    # Create figure and plot space, also defining figuresize
    fig, ax = plt.subplots(figsize=(5,5))

    # Add x-axis and y-axis
    ax.plot(last24.index, last24['Inside Temp -C'],
           color='red')

    ax.plot(last24.index, last24['Outside Temp -C'],
           color='blue')

    # Set title and labels for axes
    #ax.set(xlabel="Hours",
    #       ylabel="Degrees Celsius")

    # Define the date format
    date_form = mdates.DateFormatter("%H")
    ax.xaxis.set_major_formatter(date_form)

    # Ensure a major tick for each hour using (interval=1) 
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))

    #same for y axis
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(round(start), round(end)+2, 2))

    #getting grid lines
    ax.yaxis.grid(True)

    #making some adjustments to the tick parameters
    ax.tick_params(axis='both', which='major', labelsize=14)

    #displaying plot
    #plt.show()

    #Save Plot
    plt.savefig(f'{path}/hourly_temp.png', bbox_inches='tight')

    ###################################
    ##last week data selection and Plot
    last_week = data.sort_index()[datetime.datetime.now().date() - datetime.timedelta(days=7) : datetime.datetime.now().date()]
    
    #making daily avarages if hourly is not a good fit
    #last_week = last_week.resample(rule='6H').mean()
    #print(last_week)

    # Create figure and plot space
    fig, ax = plt.subplots(figsize=(5,5))

    # Add x-axis and y-axis
    ax.plot(last_week.index, last_week['Inside Temp -C'],
           color='red')

    ax.plot(last_week.index, last_week['Outside Temp -C'],
           color='blue')

    # Set title and labels for axes
    #ax.set(xlabel="Days avarage",
    #       ylabel="Degrees Celsius")

    # Define the date format
    date_form = mdates.DateFormatter("%d.%m")
    ax.xaxis.set_major_formatter(date_form)

    # Ensure a major tick for each hour using (interval=1) 
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))

    #same for y axis
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(round(start), round(end)+2, 2))

    #getting grid lines
    ax.yaxis.grid(True)

    #making some adjustments to the tick parameters
    ax.tick_params(axis='y', which='major', labelsize=14)
    ax.tick_params(axis='x', which='major', labelsize=11)

    #displaying plot
    #plt.show()

    #Save Plot
    plt.savefig(f'{path}/daily_temp.png', bbox_inches='tight')


    ###################################
    ##last months in weeks data selection and Plot
    last_months = data.sort_index()[datetime.datetime.now().date() - datetime.timedelta(weeks=12, hours=1) : datetime.datetime.now().date()]

    #making 12h avarages if hourly is not a good fit
    #last_months = last_months.resample(rule='12H', offset='9H').mean()
    #print(last_months['Outside Temp -C'])

    # Create figure and plot space
    fig, ax = plt.subplots(figsize=(5,5))

    # Add x-axis and y-axis
    ax.plot(last_months.index, last_months['Inside Temp -C'],
           color='red', linewidth=0.25)

    ax.plot(last_months.index, last_months['Outside Temp -C'],
           color='blue', linewidth=0.25)

    # Set title and labels for axes
    #ax.set(xlabel="Weeks avarage",
    #       ylabel="Degrees Celsius")

    # Define the date format
    date_form = mdates.DateFormatter("%U")
    ax.xaxis.set_major_formatter(date_form)

    # Ensure a major tick for each hour using (interval=1) 
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

    #same for y axis
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(round(start), round(end)+2, 2))

    #getting grid lines
    ax.yaxis.grid(True)

    #making some adjustments to the tick parameters
    ax.tick_params(axis='y', which='major', labelsize=14)
    ax.tick_params(axis='x', which='major', labelsize=14)

    #displaying plot
    #plt.show()

    #Save Plot
    plt.savefig(f'{path}/weekly_temp.png', bbox_inches='tight')


if __name__ == "__main__":
    vistemp('/media/SAVE', 'templogger.csv')


