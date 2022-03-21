from blogapp.dashapp.data_preparation import update_data
from pathlib import Path

# load data from data folder
df = update_data(Path(__file__).parent.joinpath('data', 'raw'))
region_options = [{'label': rname, 'value': rname}  for rname in df['Region'].unique()]
volcano_options = [{'label': rname, 'value': rname}  for rname in df['Volcano Name'].unique()]

