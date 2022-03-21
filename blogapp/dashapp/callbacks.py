from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np
from blogapp.dashapp.utils import *


def register_callbacks(dashapp):
    #  1st figure: Abacus plot of volcano activities
    @dashapp.callback(Output(component_id='abacus_plot', component_property='figure'),
                      [Input(component_id='dropdown', component_property='value')])
    def graph_update(dropdown_value):
        print(dropdown_value)
        # process data with requested volcano
        if dropdown_value == 'ALL':
            df_j = df[df['Decades'] >= 180]
        else:
            df_j = df[(df['Decades'] >= 180) & (df['Region'] == dropdown_value)]
        # generate statistics
        df_plot = df_j.groupby(['Decades', 'Max VEI'])['Volcano Name'].count().reset_index()
        # plot figure
        fig = go.Figure(data=[go.Scatter(
            x=10 * df_plot['Decades'],
            y=df_plot['Max VEI'],
            text='Count: ' + df_plot['Volcano Name'].astype(str),
            mode='markers',
            marker=dict(
                size=50 * np.sqrt(df_plot['Volcano Name'] / df_plot['Volcano Name'].max()),
                opacity=0.7,
                symbol='circle',
                color='red',
            ))])

        fig.update_layout(
            title='Regional Eruption Activities (1800-2020)',
            width=1200, height=800,
            xaxis_title='Year',
            yaxis_title='Volcano Eruption Index (VEI)',
            yaxis_range=[-0.5, 7.5]
        )
        return fig

    #  2nd figure: Geographical plots of volcano activities
    @dashapp.callback(Output(component_id='geo_plot', component_property='figure'),
                      [Input(component_id='dropdown', component_property='value')])
    def graph_update(dropdown_value):
        print(dropdown_value)
        # process data with requested region
        if dropdown_value == 'ALL':
            df_j = df
        else:
            df_j = df[df['Region'] == dropdown_value]
        # generate statistics
        df_plot = df_j.groupby(['Volcano Name',
                                'Latitude',
                                'Longitude']).agg({'Max VEI': ['max', 'count']}).reset_index()
        # plot figure
        fig = go.Figure(data=[go.Scattergeo(
            lat=df_plot["Latitude"],
            lon=df_plot['Longitude'],
            text=df_plot['Volcano Name'] + ' [Max VEI: ' + \
                 df_plot['Max VEI', 'max'].astype(str) + \
                 ', Recorded Eruption: ' + \
                 df_plot['Max VEI', 'count'].astype(str),
            mode='markers',
            marker=dict(
                size=8 + 3 * df_plot['Max VEI', 'max'].fillna(1),
                opacity=0.8,
                symbol='triangle-up',
                color=df_plot['Max VEI', 'count'],
                colorscale='hot',
                colorbar_title="Recorded Eruptions"
            ))])

        fig.update_layout(
            title='Volcano Eruption Distribution',
            width=1400, height=700,
            geo=dict(
                showland=True,
                landcolor="rgb(250, 250, 250)",
                subunitcolor="rgb(217, 217, 217)",
                countrycolor="rgb(217, 217, 217)",
                countrywidth=0.5,
                subunitwidth=0.5
            ),
        )
        return fig
