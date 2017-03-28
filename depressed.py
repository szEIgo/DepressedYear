import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bokeh.charts import Donut, Bar, show, vplot, Line, output_file
import operator
from bokeh.charts.attributes import cat, color
from bokeh.charts.operations import blend
from bokeh.charts.utils import df_from_json
from bokeh.sampledata.olympics2014 import data
from tqdm import tqdm
#import msvcrt as m


print("Reading csv from URL")


df = pd.read_csv("AviationDataset.csv", encoding ='latin1').fillna(0)
print("file loaded")

# ## 1
#fatality_dict = {}
#for phase in df['Broad.Phase.of.Flight'].unique():
#     if phase != 0:
#         fatality_dict.update({ phase : sum(df[df['Broad.Phase.of.Flight'] == phase]['Total.Fatal.Injuries']) / len(df[df['Broad.Phase.of.Flight'] == phase]) * 100})
#x, y = zip(*sorted(fatality_dict.items()))
#data = pd.Series(y, x)
#pie_chart = Donut(data, plot_width=800, plot_height=800)
#def wait():
#    m.getch()
#show(pie_chart)

# # 2
#df['Location'] = df['Location'].apply(lambda word: str(word)[-2:])
#us_states = df.loc[df['Country'] == 'United States']['Location'].unique()

#injury_dict = {}
#for state in us_states:
#    injury_dict.update({ state : sum(df[df['Location'] == state][cat]) for cat in ['Total.Fatal.Injuries', 'Total.Serious.Injuries', 'Total.Minor.Injuries']} )
#result_dict = dict(sorted(injury_dict.items(), key=operator.itemgetter(1), reverse=True)[:5])
#x, y = zip(*sorted(result_dict.items()))
#data = pd.Series(y, x)
#bar2 = Bar(data, title="Top 5 States Of Aviation Injuries", plot_width=400)

#show(bar2)


## 3
# minor_dict = dict.fromkeys(df['Model'].unique(), 0)
#serious_dict = dict.fromkeys(df['Model'].unique(), 0)
#fatal_dict  = dict.fromkeys(df['Model'].unique(), 0)
#
# for row in df.itertuples():
#     minor, serious, fatal = [int(row[cat]) for cat in [24, 25, 26]]
#     flight_model = row[16]
#
#     minor_dict.update({ flight_model : minor_dict.get(flight_model) + minor})
#     serious_dict.update({ flight_model : serious_dict.get(flight_model) + minor})
#     fatal_dict.update({ flight_model : fatal_dict.get(flight_model) + minor})
#
# # Plotting
# mx, my = zip(*sorted(minor_dict.items(), key=operator.itemgetter(1), reverse=True)[:5])
# sx, sy = zip(*sorted(serious_dict.items(), key=operator.itemgetter(1), reverse=True)[:5])
# fx, fy = zip(*sorted(fatal_dict.items(), key=operator.itemgetter(1), reverse=True)[:5])
#
# minor_data = pd.Series(my, mx)
# serious_data = pd.Series(sy, sx)
# fatal_data = pd.Series(fy, fx)
#
# minor_chart, serious_chart, fatal_chart = [Donut(data[0], plot_width=400, title=data[1] ,plot_height=400) for data in [[minor_data, 'Minor Data'], [serious_data, 'Serious Data'], [fatal_data, 'Fatal Data']]]
#
# p = vplot(minor_chart, serious_chart, fatal_chart)
# show(p)

# 4
# cols = ['Event.Date', 'Total.Fatal.Injuries']
# workframe = df[cols]
# twenty_year_fatalities = {}
# this_year = 2017
#
# for idx, row in tqdm(workframe.iterrows()):
#     temp_stamp = int(row['Event.Date'][:4])
#     if row['Total.Fatal.Injuries'] == '0' or temp_stamp < this_year - 20:
#         continue
#     if temp_stamp in twenty_year_fatalities.keys():
#         twenty_year_fatalities[temp_stamp] += row['Total.Fatal.Injuries']
#     else:
#         twenty_year_fatalities.update({temp_stamp:row['Total.Fatal.Injuries']})
# twenty_year_stats = []
#
# for k, v in twenty_year_fatalities.items():
#     twenty_year_stats.append((k,v))
# twenty_year_stats.sort(reverse=False)
#
# result_df = pd.DataFrame(twenty_year_stats, columns=['Year', 'Fatalities'])
#
# result_dict = {}
# for row in result_df.itertuples():
#     result_dict.update({ row[1] : row[2]})
#
# mx, my = zip(*sorted(result_dict.items()))
# result_data = pd.Series(my, mx)
# chart = Line(result_data, title="Fatal Injury Distribution", legend="top_right", ylabel='Number of Fatalities', xlabel='Year')
# show(chart)

# 5
year_fatal = dict.fromkeys(range(1993, 2018), 0)
year_alive = dict.fromkeys(range(1993, 2018), 0)
for idx, row in tqdm(df[['Event.Date', 'Aircraft.Damage', 'Total.Fatal.Injuries', 'Total.Minor.Injuries', 'Total.Serious.Injuries', 'Total.Uninjured']].iterrows()):
    cats = ['Destroyed', 'Substantial']
    year = int(row['Event.Date'][:4])
    if (row['Aircraft.Damage'] in cats and year > 1992):
        fatal = row['Total.Fatal.Injuries']
        alive = sum(row[cat] for cat in ['Total.Serious.Injuries', 'Total.Minor.Injuries', 'Total.Uninjured'])
        year_fatal.update({year : year_fatal.get(year) + fatal})
        year_alive.update({year : year_alive.get(year) + alive})
fx, fy = zip(*sorted(year_fatal.items()))
fatal_data = pd.Series(fy, fx, name="fatal")
#print(fatal_data.head(5))

ax, ay = zip(*sorted(year_alive.items()))
alive_data = pd.Series(ay, ax, name="alive")
#print(alive_data.head(5))

data = pd.concat([alive_data, fatal_data], axis=1)

#http://datascience.stackexchange.com/questions/10322/how-to-plot-multiple-variables-with-pandas-and-bokeh

#chart = Bar(data,title="Fatal Injury Distribution", legend="top_right", ylabel='Number of Fatalities', xlabel='Year')
#chart = Bar(data,
#          values=blend('fatal', 'alive', name='persons', labels_name='person'),
#          label=cat(columns='year', sort=False),
#          stack=cat(columns='person', sort=False),
#          color=color(columns='person', 
#          palette=['SaddleBrown', 'Silver'],
#          sort=False))

chart = Bar(data, stacked=True)
show(chart)

