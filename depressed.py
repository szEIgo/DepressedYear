import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bokeh.charts import Donut, Bar, show
import operator

print("Reading csv from URL")


df = pd.read_csv("AviationDataset.csv", encoding ='latin1').fillna(0)
#df = pd.read_csv("https://raw.githubusercontent.com/edipetres/Depressed_Year/master/Dataset_Assignment/AviationDataset.csv").fillna(0)

print("file loaded")

## 1
fatality_dict = {}
for phase in df['Broad.Phase.of.Flight'].unique():
    if phase != 0:
        fatality_dict.update({ phase : sum(df[df['Broad.Phase.of.Flight'] == phase]['Total.Fatal.Injuries']) / len(df[df['Broad.Phase.of.Flight'] == phase]) * 100})

## Plotting Some Stuff
x, y = zip(*sorted(fatality_dict.items()))
data = pd.Series(y, x)
pie_chart = Donut(data, plot_width=800, plot_height=800)
# show(pie_chart)

## 2
df['Location'] = df['Location'].apply(lambda word: str(word)[-2:])
us_states = df.loc[df['Country'] == 'United States']['Location'].unique()

injury_dict = {}
for state in us_states:
    injury_dict.update({ state : sum(df[df['Location'] == state][cat]) for cat in ['Total.Fatal.Injuries', 'Total.Serious.Injuries', 'Total.Minor.Injuries']} )
result_dict = dict(sorted(injury_dict.items(), key=operator.itemgetter(1), reverse=True)[:5])

# Plotting, fucking plotting
x, y = zip(*sorted(result_dict.items()))
data = pd.Series(y, x)
bar2 = Bar(data, ylabel="hej", title="Top 5 States Of Aviation Injuries", plot_width=400, color="origin")


show(bar2)
