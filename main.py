import tkinter as tk
import tkinter.messagebox
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import itertools
import datetime
from datetime import datetime as dt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

pd.set_option('display.max_rows', 12)
pd.set_option('display.max_columns', 12)

states = pd.read_csv("states.csv")
state = list(states["state"])
states = pd.read_csv("states.csv")

covid = pd.read_csv("US_covid.csv", parse_dates=True)
covid = covid.replace(np.nan,0)
state = list(states["state"])

temp = covid.drop(columns='state')
temp['new_death'] = temp['new_death']-temp['pnew_death']
temp['new_case'] = temp['new_case']-temp['pnew_case']
national = temp.groupby('submission_date').sum()
national.insert(column = 'state',value='NTL',loc=0)
national.sort_values(by='submission_date', ascending=True)
nat = national.reset_index()
print(nat.head())
covid = covid.append(nat, ignore_index=True)
print(covid.shape)


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.state = state
        self.var = tk.StringVar(self)

        self.options = tk.OptionMenu(self, self.var, *self.state)

        self.var.set('National')
        self.options.pack()

        self.btn = tk.Button(self, text="Submit", width=8, command=self.submit)
        self.btn.pack()

        self.close = tk.Button(self,text = "Exit",width=8,command = self.exit)
        self.close.pack()
        self.pack()


    def submit(self, *args):
        var1 = self.var.get()
        key = state.index(var1)
        abbr = states.at[key, 'abbr']
        self.visualize(abbr)

    def visualize(self,*abbr):
        sub = covid.loc[covid['state']==abbr[0],['submission_date','state','tot_cases','new_case','tot_death','new_death']]
        sub['submission_date'] = pd.to_datetime(sub['submission_date'])
        sub = sub.sort_values(by='submission_date',ascending= False)
        sub = sub.reset_index(drop=True)
        day_max_case = sub["new_case"].idxmax()
        day_max_death = sub["new_death"].idxmax()
        root = tk.Tk()
        if abbr[0] == 'NTL':
            root.wm_title("State Cases and Deaths: "+abbr[0])
        else:
            root.wm_title("National Cases and Deaths")
        stateplot=self.create_plot(sub,*abbr,day_max_case,day_max_death)
        canvas = FigureCanvasTkAgg(stateplot, master=root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack()
        button = tkinter.Button(root, text="Return to menu", command=root.destroy)
        button.pack()

        tk.mainloop()


    def create_plot(self, cdata,abbr,day_max_c,day_max_d):
        fig = plt.figure(figsize=(8, 8))
        cdata['submission_date'] = cdata['submission_date'].dt.date
        if abbr == 'NTL':
            cases = str(cdata.iloc[day_max_c, 0]) + " -- " + str(cdata.iloc[day_max_c, 2]) + " Cases"
            deaths = str(cdata.iloc[day_max_d, 0]) + " -- " + str(cdata.iloc[day_max_d, 4]) + " Deaths"
            plt.suptitle("Covid daily cases, aggregate cases, & aggregate deaths " +
                         "\nNational " + "\nHighest Daily Cases: " + cases +
                         "\nHighest Daily Deaths: " + deaths)

        else:
            cases = str(cdata.iloc[day_max_c,0]) +" -- "+ str(cdata.iloc[day_max_c,3]) + " Cases"
            deaths = str(cdata.iloc[day_max_d,0]) +" -- "+ str(cdata.iloc[day_max_d,5]) + " Deaths"


            plt.suptitle("Covid daily cases, aggregate cases, & aggregate deaths "+
                        "\nState: "+abbr+"\nHighest Daily Cases: "+cases+
                        "\nHighest Daily Deaths: "+deaths)

        format = mpl.dates.DateFormatter('%Y-%m-%d')

        ax1 = plt.subplot2grid((8,8),(0,0),rowspan=4,colspan=9,fig=fig)
        ax1.xaxis_date()
        ax1.xaxis.set_major_formatter(format)
        ax1.grid(True)
        ax1 = sns.lineplot(data=cdata, color='g',x='submission_date', y='new_case')
        plt.yticks(color='g')
        ax1.set_xlabel('Date')

        ax2 = plt.subplot2grid((8, 8), (5, 0), rowspan=4, colspan=9)
        ax2.xaxis_date()
        ax2.xaxis.set_major_formatter(format)
        ax2 = sns.lineplot(data=cdata,color='b', x='submission_date', y='tot_cases')
        ax2.xaxis.grid(True)
        ax2.set_xlabel('Date')
        if cdata.iloc[cdata['tot_cases'].idxmax(),2] > 1e6:
            ax2.set_ylabel('Total Cases (in Millions)')
        else:
            ax2.set_ylabel('Total Cases')
        plt.yticks(color='b')

        ax3 = ax2.twinx()
        ax3 = sns.lineplot(data=cdata,color='r',x='submission_date',y='tot_death')
        ax3.set_ylabel('Total Deaths')
        plt.yticks(color='r')

        #plt.show()
        return fig


    def exit(self):
        root.quit()
        root.destroy()

root = tk.Tk()
app = App(root)
app.mainloop()