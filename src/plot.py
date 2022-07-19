"""
Plot charts using the World in Data datasets.
For tweets, the best image size is 599x675
"""
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Import CSV file
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'

df = pd.read_csv(url)
df['date'] = pd.to_datetime(df['date'])

# Filter out all countries except Mexico
country = 'Mexico'
df_mx = df[df['location'] == country]


# Guideline 1: remove redundant attributes
# 1.bad: 3D chart
fig_1_1 = go.Figure(data=[go.Mesh3d(
    x=(df_mx['date']),
    y=([100]*len(df_mx)),
    z=(df['total_cases']),
    opacity=0.5,
    color='rgba(244,22,100,0.6)',
    )],
    layout=dict(
        title="🤢 Too many things going on"
        )
    )

fig_1_1.update_layout(scene=dict(
    xaxis = dict(
        backgroundcolor="rgb(200, 200, 230)",
        gridcolor="white",
        showbackground=True,
        zerolinecolor="white",),
    yaxis = dict(
        backgroundcolor="rgb(230, 200,230)",
        gridcolor="white",
        showbackground=True,
        zerolinecolor="white"),
    zaxis = dict(
        backgroundcolor="rgb(230, 230,200)",
        gridcolor="white",
        showbackground=True,
        zerolinecolor="white",),
    xaxis_title="Date",
    yaxis_title="",
    zaxis_title="Total Cases",
))

#fig_1_1.show()

# 2.good: 2D chart
fig_1_2 = px.line(df_mx, x="date", y="total_cases", title="😌 Much better")

#fig_1_2.show()

# Guideline 2: Length and position
df_2 = df[df['location'].isin(['European Union', 'Asia', 'North America', 'South America', 'Oceania', 'Africa'])]
df_2 = df_2.groupby("location").sum().reset_index()

## Bad
fig_2_1 = px.pie(df_2, values='new_cases', names='location',
                 labels={'location': 'new_cases'},
                 title='😓 Pie charts make comparison hard')
#fig_2_1.show()

## Good
fig_2_2 = px.bar(df_2.sort_values(by='new_cases', ascending=True), 
                 orientation='h', y='location', x='new_cases',
                 text="new_cases", text_auto='.4s',
                 title="😀 Length and position make it easier to compare")
#fig_2_2.show()

# Guideline 3: Patterns vs details
df_3 = df_mx.copy()
df_3['year'] = df_3['date'].dt.year
df_3['month'] = df_3['date'].dt.month
df_3_pt = pd.pivot_table(df_3, values='new_cases', index='year', columns='month')

# Patterns
fig_3_1 = px.imshow(df_3_pt, title="🔥 Heatmaps are good for spotting patterns")
#fig_3_1.show()

# Details
fig_3_2 = px.line(df_3, x="date", y="new_cases", title="🔎 Lines are better for showing details")
#fig_3_2.show()

# Guideline 4: Use meaningful axis ranges
df_4 = df_mx.copy()
df_4['date_bin'] = df_4['date'].dt.strftime('%Y%m')
df_4 = df_4.groupby('date_bin').sum().reset_index()

## When absolute figures matter, axis should start at zero
fig_4_1 = px.bar(
    df_4, x='date_bin', y='new_cases', text='new_cases', text_auto='.4s',
    range_x=[5,10], range_y=[0,300000],
    labels={'date_bin': 'Month', 'new_cases': 'New Covid cases'},
    title="When absolute figures matter, the y axis should start at zero.")
fig_4_1.show()

## When changes are important, axis can be zoomed-in
fig_4_2 = px.bar(
    df_4, x='date_bin', y='new_cases', text='new_cases',
    range_x=[5,10], range_y=[135000,250000],
    labels={'date_bin': 'Month', 'new_cases': 'New Covid cases'},
    color='new_cases',
    title="⚠️ When changes matter, zoom in your y axis. But warn audience!")
fig_4_2.update_coloraxes(showscale=False)
fig_4_2.show()