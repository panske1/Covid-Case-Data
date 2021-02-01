#!/usr/bin/env python
"""
===========================================================================================================================
Author: Patrick Anske
Last Update: 1/29/2021
Purpose: Visualize COVID Cases and Deaths at National and State levels
Data Source: CDC (link - https://data.cdc.gov/Case-Surveillance/COVID-19-Case-Surveillance-Public-Use-Data/vbim-akqf/data )
Files: States.csv - 2 variable dataframe row 1 is full state name, row 2 is state abbreviate
       US_covid.csv - 15 variable dataframe from CDC. Includes aggregated and daily covid data organized by date and state
============================================================================================================================
"""

#Step 1: Import packages to be used throughout project

import tkinter as tk
import tkinter.messagebox
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

"""
Step 2: Read in data, create National(NTL) dataframe, append National daily statistics to full dataframe
    (should be downloaded and stored locally prior to running program)
"""
covid = pd.read_csv("US_covid.csv", parse_dates=True)
##Step 2a: Replace missing values in covid data with 0
covid = covid.replace(np.nan,0)

####Initiliaze list of state names to be used for options list later
states = pd.read_csv("states.csv")
state = list(states["state"])
national = covid.drop(columns='state')
national = national.groupby('submission_date').sum()
####Add new state abbr for National data rows
national.insert(column = 'state',value='NTL',loc=0)
national.sort_values(by='submission_date', ascending=True)
nat = national.reset_index()
####Append national statistics onto full covid dataframe
covid = covid.append(nat, ignore_index=True)


"""
Step 3: Create class to manage operations for interactive features (i.e. dropdowns, creating plots, exit)
"""
class App(tk.Frame):
    ##Step 3a: Initialize selection window which stores dropdown(options menu), submit, and option to close program
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.state = state
        self.var = tk.StringVar(self)
        ####Set option menu equal to values in "state" list
        self.options = tk.OptionMenu(self, self.var, *self.state)
        ####Default selection 'National'
        self.var.set('National')
        self.options.pack()
        ####Initialize submit button
        self.btn = tk.Button(self, text="Submit", width=8, command=self.submit)
        self.btn.pack()
        ####Initiliaze close button
        self.close = tk.Button(self,text = "Close",width=8,command = self.exit)
        self.close.pack()
        self.pack()

    ##Step 3b: Establish function to run when submit is clicked in the selection window
    def submit(self, *args):
        ####Get value currently selected in options menu
        var1 = self.var.get()
        ####Find state name in list and return abbreviation
        key = state.index(var1)
        abbr = states.at[key, 'abbr']

        ####Call visualize function and pass the abbreviation to it
        self.visualize(abbr)

    ##Step 3c: Subset covid data based on selection and initialize new window to contain visuals of selected data
    def visualize(self,*abbr):

        ####Select all rows from covid dataframe that match the state abbreviation returned from submit
        sub = covid.loc[covid['state']==abbr[0],['submission_date','state','tot_cases','new_case','tot_death','new_death']]
        sub['submission_date'] = pd.to_datetime(sub['submission_date'])
        sub = sub.sort_values(by='submission_date',ascending= False)
        sub = sub.reset_index(drop=True)

        ####Identify highest daily gains in cases and deaths
        day_max_case = sub["new_case"].idxmax()
        day_max_death = sub["new_death"].idxmax()
        ####Initialize second window to contain visual and button
        root = tk.Tk()
        if abbr[0] == 'NTL':
            root.wm_title("National Cases and Deaths")
        else:
            root.wm_title("State Cases and Deaths: " + abbr[0])
        ####Call create_plot and pass values to actually plot data and format visual
        stateplot=self.create_plot(sub,*abbr,day_max_case,day_max_death)
        ####Create canvas for plot to be drawn on
        canvas = FigureCanvasTkAgg(stateplot, master=root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack()
        ####Add return button to close visualization and go back to selection window
        button = tkinter.Button(root, text="Return to menu", command=root.destroy)
        button.pack()

        tk.mainloop()

    ##Step 3d: Create Subplot and plot data in grid
    def create_plot(self, cdata,abbr,day_max_c,day_max_d):
        ####Establish figure to hold each plot
        fig = plt.figure(figsize=(8, 8))
        ####Reformat dates to simple date (no timestamp)
        #cdata['submission_date'] = cdata['submission_date'].dt.date
        cases = str(cdata.iloc[day_max_c, 0]) + " -- " + str(cdata.iloc[day_max_c, 3]) + " Cases"
        deaths = str(cdata.iloc[day_max_d, 0]) + " -- " + str(cdata.iloc[day_max_d, 5]) + " Deaths"
        ####Assign figure title based on selection (National or state) from options menu
        if abbr == 'NTL':
            plt.suptitle("Covid daily cases, aggregate cases, & aggregate deaths " +
                         "\nNational " + "\nHighest Daily Cases: " + cases +
                         "\nHighest Daily Deaths: " + deaths)

        else:
            plt.suptitle("Covid daily cases, aggregate cases, & aggregate deaths "+
                        "\nState: "+abbr+"\nHighest Daily Cases: "+cases+
                        "\nHighest Daily Deaths: "+deaths)

        ####Reformat dates for X-axis
        format = mpl.dates.DateFormatter('%Y-%m-%d')

        #Initialize first plot to which will contain daily case lineplot
        ax1 = plt.subplot2grid((8,8),(0,0),rowspan=4,colspan=9,fig=fig)
        ax1.xaxis_date()
        ax1.xaxis.set_major_formatter(format)
        ax1.grid(True)
        ####Plot data
        ax1 = sns.lineplot(data=cdata, color='g',x='submission_date', y='new_case')
        plt.yticks(color='g')
        ####Assign Axis labels
        ax1.set_xlabel('Date')
        ax1.set_ylabel('New Daily Cases')

        ####Initialize 2nd plot, this will be a double line plot with a shared x-axis (date) and two Y-Axis (Total Cases on left and Total Deaths on right)
        ax2 = plt.subplot2grid((8, 8), (5, 0), rowspan=4, colspan=9)
        ax2.xaxis_date()
        ax2.xaxis.set_major_formatter(format)
        ax2 = sns.lineplot(data=cdata,color='b', x='submission_date', y='tot_cases')
        ax2.xaxis.grid(True)
        ax2.set_xlabel('Date')
        plt.yticks(color='b')
        ####Axis auto-scales based on input, so to a is dependent on if the scale is presented in standard notation or scientific
        if cdata.iloc[cdata['tot_cases'].idxmax(),2] > 1e6:
            ax2.set_ylabel('Total Cases (in Millions)')
        else:
            ax2.set_ylabel('Total Cases')


        ####ax3 will share X-axis with ax2
        ax3 = ax2.twinx()
        ax3 = sns.lineplot(data=cdata,color='r',x='submission_date',y='tot_death')
        ax3.set_ylabel('Total Deaths')
        plt.yticks(color='r')

        #plt.show()
        return fig

    ##Step 3e: when exit command is called abort close window and destroy stored values
    def exit(self):
        root.quit()
        root.destroy()

"""
Step 4: Call App
"""
####Initialize new instance of tkinter
root = tk.Tk()
root.wm_title("Covid Visualization")
label=tk.Label(root,text="Please select the locality data you would like to visualize")
label.pack()
####Call app, all subsequent steps are followed to create menu and execute commands
app = App(root)
####End tkinter instance when Exit is called and App ends
app.mainloop()