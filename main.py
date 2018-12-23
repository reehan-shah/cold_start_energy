# Pandas and Numpy for data management
import pandas as pd
import numpy as np

# os methods for manipulating paths
import os

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from bokeh.plotting import Figure,figure
from bokeh.layouts import layout, widgetbox, WidgetBox
from bokeh.models import ColumnDataSource, Div, axes,Range1d, LabelSet, Label, HoverTool, DataTable, TableColumn, RadioButtonGroup, CheckboxGroup, Panel, Tabs, CategoricalColorMapper, SingleIntervalTicker, LinearAxis
from bokeh.models.widgets import Slider, Select, TextInput, CheckboxGroup, RangeSlider, Tabs
from bokeh.io import curdoc,output_file, show, output_notebook, push_notebook
from bokeh.layouts import row, widgetbox, column
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.palettes import Category20_16

#The user interface is created using a python library called Bokeh which is used to create interactive plots and applications
#Most of the bokeh plotting functions handle data in the form of objects called ColumnDataSources

# The code is divided into a set of functions, each **_tab function creates a different tab in the UI
# The overall code creates an Application Interface that can be run using the command prompt.
# The application can be started by running the following script on your Jupyter notebook/terminal containing python:
# !bokeh serve --show .../bokeh_app
# here, bokeh_app is simply a folder that contains this file (must be called main.py) and any other datasets or data files that it uses
# ... must be replaced with the path to the folder bokeh_app


def trends_tab(df): # This function creates a tab for making a plot of the trends for predictions of the following week

#The code for the function is split into 4 parts - creating the dataset dynamically, defining the style for the plot
#, creating the plot and updating the values based on the user input

# The make_dataset function is used to dynamically edit the dataset that is being plotted according to the user inputs
# It takes two parameters, week_list and efficiency which are both results of a dropdown menu and a slider button on the UI
# It returns a ColumnDataSource for the plotting function to input and plot
	def make_dataset(week_list,efficiency):
        by_week = pd.DataFrame(columns=['id','day','week','consumption','day_name'])
        week_list=[str(i) for i in range(week_list+1)]
        for week_num in (week_list):
            subset = df[df['week']==week_num]
            if week_num!='0':
                subset['consumption'] = subset.consumption*efficiency/100
            by_week = by_week.append(subset)
        return ColumnDataSource(by_week)


# The style function simply adds elements of style to the plot. It can be modified according to different plots that need to be displayed
    def style(p):
        # Title 
        p.title.align = 'center'
        p.title.text_font_size = '20pt'
        p.title.text_font = 'serif'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style = 'bold'
        # Tick labels
        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font_size = '12pt'

        return p
    
# The make_plot function takes as input the ColumnDataSource created by the make_dataset function
# The bokeh plotting works in the form of glyphs that are overlapped on to the same plot, in this case 'p'

    def make_plot(src):
        p = figure(plot_width = 700, plot_height = 500, # the figure function creates a figure with the required title and x and y axis labels
                  title = 'Daily Consumption for Your Building',
                  x_axis_label = 'Day', y_axis_label = 'Consumption (Wh)', y_range = [0,5000000])

        p.line(x="day", y="consumption", source=src) # the line function creates a line glyph onto the p plot
        hover = HoverTool(tooltips = [("Day of Week",'@day_name'), # the hover function creates glyphs that allow for text to be displayed as you hover over the graph
                                 ("Consumption (Wh)",'@consumption')],
                         mode='vline')
        p.add_tools(hover)

        p = style(p)

        return p
    
# The update function uses Javascript callbacks to update values of the variables depending on the user inputs

    def update(attr, old, new):
        weeks_to_plot = int(week_selection.value) # this takes the values of the week selection dropdown table as integers
        efficiency = efficiency_select.value # this takes the value of the slider table
        new_src = make_dataset(weeks_to_plot,efficiency) # this calls the make_dataset function with the updated data
        src.data.update(new_src.data) # the original src table is now modified using the newly created data and is subsequently plotted on the graph

# This creates the widget for the Slider for the user to select the efficiency
# The on_change function is a JS callback that is reactive to the users inputs
    efficiency_select = Slider(start = 0, end = 100, 
                     step = 10, value = 100,
                     title = 'Reduced Energy Consumption (%)')
    efficiency_select.on_change('value', update)

# This creates the widget for the Dropdown for number of weeks to predict
    week_selection = Select(title="Number of Weeks to Predict:", value="1", options=['1','2','3'])
    week_selection.on_change('value',update)
    
# This combines the two widgets into a 'widgetbox' to be put on the UI
    controls = WidgetBox(week_selection,efficiency_select)

# Initial values are provided for the first/default run of the UI
    initial_weeks = 1
    init_efficiency = 100

# The table src contains the data for the plot and is constantly modified on the user's response
    src = make_dataset(initial_weeks,init_efficiency)
# p makes the plot on the UI
    p = make_plot(src)
# the stats table is used to create a static datatable on the UI for a summary of the weekly consumption
    stats = pd.DataFrame(df.groupby('week').consumption.sum().astype(int))
    stats = ColumnDataSource(stats)
    columns = [TableColumn(field="week", title="Week Number"),TableColumn(field="consumption", title="Consumption (Wh)")]
    data_table = DataTable(source=stats, columns=columns, width=400, height=350)
    desc = Div(text="<br><br><br><b>Building Energy Consumption Summary by Week</b>")
# the left part of the UI is a column arrangement of the control widgets, data summary table and its description
	left = column(controls,desc,data_table)
# the overall arrangement of the page is a row arrangement of left and the trend plot
	layout = row(left,p)
# the function returns a tab object which can be put on the UI as an individual tab among many others
    tab = Panel(child=layout, title = 'Trend Plot')

    return tab

# The table tab function creates another tab for the UI which contains a day wise consumption summary for the data of the past week and predictions for next 3 weeks
# it takes the overall dataframe as input and outputs a tab that contains a day-wise grouped data for the next 3 weeks
def table_tab(df):
    x = df.pivot(columns='week',index='day_name',values='consumption').rename(columns={"0":"week_0","1":"week_1","2":"week_2","3":"week_3"}).reset_index()
    x = ColumnDataSource(x)
    columns = [TableColumn(field='day_name',title='Day of Week'),TableColumn(field='week_0',title="Past Week"),TableColumn(field='week_1',title="Future Week 1"),TableColumn(field='week_2',title="Future Week 2"),TableColumn(field='week_3',title="Future Week 3")]
    data_table = DataTable(source=x, columns=columns, width=600, height=350)
    layout = row(data_table)
    tab = Panel(child=layout,title='Data Table')
    return tab

# the data is taken from a file created by the prediction file that creates a table with the following columns:
# the data contains a building id, the week number (0 for past and 1,2,3 for future), the day number (from 1-28) and the consumption
 
df = pd.read_csv('ui.csv')
df['week'] = df['week'].astype(str)
#the code below creates a day of the week for the day number
df['day_name'] = 'Mon'
df.loc[df['day']%7==2,'day_name']='Tue'
df.loc[df['day']%7==3,'day_name']='Wed'
df.loc[df['day']%7==4,'day_name']='Thu'
df.loc[df['day']%7==5,'day_name']='Fri'
df.loc[df['day']%7==6,'day_name']='Sat'
df.loc[df['day']%7==0,'day_name']='Sun'

# Create each of the tabs
tab1 = trends_tab(df)
tab2 = table_tab(df)


# Put all the tabs into one application
tabs = Tabs(tabs = [tab1,tab2])

# Put the tabs in the current document for display
curdoc().add_root(tabs)