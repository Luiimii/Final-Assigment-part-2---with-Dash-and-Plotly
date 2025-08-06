#!/usr/bin/env python
# coding: utf-8

import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the data
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [i for i in range(1980, 2024, 1)]

# Layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={"textAlign": "center", "color": "#503D36", "font-size": 24}),
    
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value="Select Statistics",
            placeholder='Select a report type',
            style={"width": "80%", "padding": "3px", "font-size": "20px", "text-align-last": "center"}
        )
    ]),
    
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value="Select-year",
            placeholder="Select year",
            style={"width": "80%", "padding": "3px", "font-size": "20px", "text-align-last": "center"}
        )
    ]),
    
    html.Div(id='output-container', className='chart-grid', style={"display": "flex", "flex-wrap": "wrap", "justify-content": "center"})
])

@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Average Automobile Sales fluctuation over Recession Period
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales Fluctuation Over Recession Period"))

        # Plot 2: Average Vehicles Sold by Type during Recession
        average_sales = recession_data.groupby("Vehicle_Type")["Automobile_Sales"].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title="Average Vehicles Sold by Type"))

        # Plot 3: Advertising Expenditure Share by Vehicle Type
        exp_rec = recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(exp_rec, names="Vehicle_Type", values="Advertising_Expenditure", title="Advertising Expenditure Share by Vehicle Type"))

        # Plot 4: Effect of Unemployment Rate on Vehicle Type and Sales
        unemp_data = recession_data.groupby(["unemployment_rate", "Vehicle_Type"])["Automobile_Sales"].sum().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales',
                                           labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Automobile Sales'},
                                           title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return [
            html.Div(R_chart1, style={'width': '48%', 'padding': '10px'}),
            html.Div(R_chart2, style={'width': '48%', 'padding': '10px'}),
            html.Div(R_chart3, style={'width': '48%', 'padding': '10px'}),
            html.Div(R_chart4, style={'width': '48%', 'padding': '10px'})
        ]

    elif (input_year and selected_statistics=='Yearly Statistics'):
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly Average Automobile Sales
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x="Year", y="Automobile_Sales", title="Yearly Average Automobile Sales"))

        # Plot 2: Total Monthly Automobile Sales
        mas = data.groupby("Month")["Automobile_Sales"].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas, x='Month', y='Automobile_Sales', title='Total Monthly Automobile Sales'))

        # Plot 3: Average Vehicles Sold by Type in Selected Year
        avr_vdata = yearly_data.groupby("Vehicle_Type")["Automobile_Sales"].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x="Vehicle_Type", y="Automobile_Sales", title=f'Average Vehicles Sold by Type in {input_year}'))

        # Plot 4: Advertisement Expenditure Share by Vehicle Type in Selected Year
        exp_data = yearly_data.groupby("Vehicle_Type")["Advertising_Expenditure"].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, names="Vehicle_Type", values="Advertising_Expenditure", title="Advertisement Expenditure Share by Vehicle Type"))

        return [
            html.Div(Y_chart1, style={'width': '48%', 'padding': '10px'}),
            html.Div(Y_chart2, style={'width': '48%', 'padding': '10px'}),
            html.Div(Y_chart3, style={'width': '48%', 'padding': '10px'}),
            html.Div(Y_chart4, style={'width': '48%', 'padding': '10px'})
        ]
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
