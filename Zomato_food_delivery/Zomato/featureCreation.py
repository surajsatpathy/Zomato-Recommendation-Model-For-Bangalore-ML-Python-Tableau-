import pandas as pd
import pickle
import numpy as np


class FeatureCreator:
    def __init__(self) :
        self.z=pd.read_csv("data//price_model_data.csv")

    def transform(self,user_input_loc,user_input_cuisine,user_input_price):
        user_input_loc = user_input_loc.lower()
        user_input_cuisine = user_input_cuisine.lower()
        user_input_price=float(user_input_price)

        self.z['location'] = self.z['location'].str.lower()
        user_input_lat = self.z[self.z['location'] == user_input_loc]['Latitude'].unique()[0]
        user_input_lon = self.z[self.z['location'] == user_input_loc]['Longitude'].unique()[0]
        user_input_data = pd.DataFrame([[user_input_lon,user_input_lat,user_input_loc,user_input_cuisine,user_input_price]],
        columns= ['Longitude','Latitude','Location','Cuisine','price_for_one'])

        
        cluster_input_metrics = ['Longitude','Latitude','price_for_one']
        cluster_input_data = pd.DataFrame([[np.nan,np.nan,np.nan]],columns=cluster_input_metrics)

        max_min_data=pd.read_csv("data//max_min_data.csv")
        for m in cluster_input_metrics:

            min_value = max_min_data[max_min_data['Variable'] == m]['Min'].values[0]
            max_value = max_min_data[max_min_data['Variable'] == m]['Max'].values[0]
            # print(user_input_data[m][0],min_value,max_value)

            scaled_value = (user_input_data[m][0]-min_value)/(max_value-min_value)
            cluster_input_data[m][0] = scaled_value        

        filename="saved_model//cluster_predictor.pickle"
        cluster_predictor = pickle.load(open(filename, 'rb'))
        cluster_input_data['Cluster_Label'] = cluster_predictor.predict(cluster_input_data)

        user_input_data['Cluster_Label'] = cluster_input_data['Cluster_Label'][0]

        filename="data//cusines_encoded_dict.pickle"
        cusines_encoded_dict = pickle.load(open(filename, 'rb'))

        feature1=user_input_data['Cluster_Label'].values[0]
        feature2=cusines_encoded_dict[user_input_data['Cuisine'][0]]
        
        return feature1,feature2


    