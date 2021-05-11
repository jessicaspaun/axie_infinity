import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from datetime import datetime

import plotly.express as px
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html


# Set app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Read Data
aqua = pd.read_csv('data/aqua_master.csv')
plant = pd.read_csv('data/plant_master.csv')
beast = pd.read_csv('data/beast_master.csv')
bird = pd.read_csv('data/bird_master.csv')

aqua['type'] = 'aqua'
plant['type'] = 'plant'
beast['type'] = 'beast'
bird['type'] = 'bird'

df = aqua.append(plant).append(beast).append(bird)

df['prices'] = [float(x.strip('$').replace(',','')) for x in df['price']]
date= [x.split('-') for x in df['date']]
x_axis = []
for i in date:
	x_axis.append(float(str(i[0]) +'.'+ str(i[1])))
df['date'] = [datetime.strptime(x, "%Y%m%d-%H%M") for x in df['date']]

print(df.head())

def get_options(list):
	dict_list = []
	for i in list:
		dict_list.append({'label': i, 'value': i})
	return dict_list

PARAMETER_OPTIONS = [
	{
		'label': 'Axie Type',
		'value': 'Number of Routes'
	},
	{
		'label': 'Aqua',
		'value': 'Value of Route'
	},
	{
		'label': 'Plant',
		'value': 'Popularity of route'
	}
]



app.layout = html.Div(
	children=[
			html.Div(
				className="row",
				children=[
						html.Div(
							className="four columns div-model-inputs",
							children=[
									html.H3('Axie Infinity Price Tracker'),
									html.P(
										'I pull the price of 4 filters of Axie every half hour', 
										style={}
									),
									html.Br(),
									html.P([
											html.Strong('Plant: '),
											'FILTERS', html.Br(),
											html.Strong('Aqua: '),
											'FILTERS', html.Br(),
											html.Strong('Beast: '),
											'FILTERS', html.Br(),
											html.Strong('Bird: '),
											'FILTERS', html.Br()
										], 
										style={}
									),
									html.Hr(className='hr-divider'),
									
									html.H6('What Axie would you like to track?'),
									
									html.Div(
											className="div-station-companies",
											children=[
													dcc.Checklist(
														id='company',
														options=get_options(
																df['type'].unique()),
														value=['plant', 'aqua', "bird", 'beast'],
														labelStyle={
															'display': 'inline-block',
															'width': '100px',
															'textAlign': 'center',
															'paddingTop': '2px',
															'paddingBottom': '2px',
															'paddingLeft': '4px',
															'paddingRight': '4px',
														}
													)		
											]
									),			
							]
						),
				]
		),

		html.Div(
			className="row-divider",
			children=[
				html.Hr(className='hr-divider'),
			]
		),

		html.Div(
			className="row",
			children=[
					html.Div(
						className="two-thirds column app__left__section",
						children=[
								# TODO: Need to link this to a download function
								dcc.Graph(
									id='map_v2',
									figure={}
								),
						],
					)
			]
		)
	]
)
                

@app.callback(
    [
        Output('map_v2', 'figure')
    ],
    [
        Input('company', 'value')
    ]
)
def update_figure(selected_fuel):
		df_sub = df[df.type.isin(selected_fuel)]

		# Use Min-Max Normalization Rescaling to get a size metric for scatter plot based on the
		# chosen secondary metric. Has been used to normalize values where [a,b] = [0.5,1]
		# https://en.wikipedia.org/wiki/Feature_scaling#Rescaling_(min-max_normalization)
		A = 0.05
		B = .5
		pri_plot = px.scatter(
			df_sub, 
			title='Axie Prices',
			x='date', 
			y='price', 
			color='type', 
			color_discrete_map={'bird': 'red', 'aqua': 'blue', "plant": 'green', 'beast': 'orange'}
		)


		figures = [pri_plot]
		[fig_.update_layout(paper_bgcolor='#879085', plot_bgcolor='#879085') for fig_ in figures]
		return figures


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=3001)

