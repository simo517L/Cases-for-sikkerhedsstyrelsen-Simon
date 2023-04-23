import pandas as pd
import networkx as nx
from pyvis.network import Network

# Vi loaded data
website_dataframe = pd.read_csv('website_dataframe.csv',converters={'Connected websites': pd.eval}) #loaded data
print(website_dataframe.head())

# Vi laver en liste af alle de hjemmesider scraperen har besøgt
website_series = website_dataframe['Connected websites'].explode().dropna()
website_series = website_series.unique()
website_list = website_series.tolist()
website_list = [x for x in website_list if x in website_dataframe['Website'].explode().dropna().tolist()]
# Nu bytter vi lister ud med en søjle for hver hjemmeside
for domain in website_list:
    temp_list = []
    for i in range(0,len(website_dataframe['Connected websites'])):
        if domain in website_dataframe['Connected websites'][i]:
            temp_list = temp_list + [1]
        else:
            temp_list = temp_list + [0]
    website_dataframe[domain] = temp_list

#For at lave en visualisering af netværket, fjerne vi de første tre søjler og giver rækkerne de samme navne som søjlerne
website_dataframe_temp = website_dataframe.drop(columns=['Website', 'Order','Connected websites'])
website_dataframe_temp.index = website_dataframe_temp.columns

# Vi kan så lave dataframet om til en adjaceny matrix med networkx pakken og visualisere det med pyvis.network
network_of_websites = nx.from_pandas_adjacency(website_dataframe_temp,create_using=nx.DiGraph() )

#'1000px', '1000px'
nt = Network('900px', '2000px',directed =True)

nt.from_nx(network_of_websites)
nt.show('nx.html', notebook=False)