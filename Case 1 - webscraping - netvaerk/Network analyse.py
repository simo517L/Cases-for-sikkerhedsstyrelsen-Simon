import pandas as pd
import networkx as nx
from pyvis.network import Network

# Vi loaded data
website_dataframe = pd.read_csv('website_dataframe.csv') #loaded data
print(website_dataframe.head())


#For at lave en visualisering af netværket, fjerne vi de første tre søjler og giver rækkerne de samme navne som søjlerne
website_dataframe_temp = website_dataframe.drop(columns=['Website','url', 'Order'])
website_dataframe_temp.index = website_dataframe_temp.columns

# Vi kan så lave dataframet om til en adjaceny matrix med networkx pakken og visualisere det med pyvis.network
network_of_websites = nx.from_pandas_adjacency(website_dataframe_temp,create_using=nx.DiGraph() )

#'1000px', '1000px'
nt = Network('900px', '2000px',directed =True)

nt.from_nx(network_of_websites)
nt.show('nx.html', notebook=False)