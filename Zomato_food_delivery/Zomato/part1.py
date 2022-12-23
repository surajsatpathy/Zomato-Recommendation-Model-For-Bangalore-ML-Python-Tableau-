import pandas as pd 
import numpy as np
class Part1:
    def __init__(self) :
        self.f_res_cusine_info=pd.read_csv("data//f_res_cuisine_info.csv")
        self.f_res_cusine_info["location"] = self.f_res_cusine_info["location"].str.lower()
        self.f_res_cusine_info['Cusines_all'] = self.f_res_cusine_info['Cusines_all'].str.lower()
        self.f_res_cusine_info.dropna(inplace=True)
        self.df=pd.read_csv("data//df.csv")
        self.df.dropna(inplace=True)
        self.re_cu_loc=pd.read_csv("data//re_cu_loc.csv")

    ## preffererd location wise popular cusines
    def locationWisePopularCusines(self,prefferd_loc):
        f_res_cusine_info_loc=self.f_res_cusine_info[self.f_res_cusine_info['location'].str.contains(prefferd_loc)]
        print(prefferd_loc)
        print(len(f_res_cusine_info_loc))
        re_cu_data =f_res_cusine_info_loc.groupby(['Cusines_all']).agg({"delivery_review_number":"mean"}).reset_index()
        re_cu_data.columns=["cuisine","avg_review_count"]
        pop_cuisine_list=list(re_cu_data[re_cu_data["avg_review_count"]==re_cu_data.avg_review_count.max()]["cuisine"].values)
        # pop_cuisines=pop_cuisine_list.join(",")
        return ",".join(pop_cuisine_list)
        # res_loc = self.df.rename(columns={'Name':'Restaurant'})[['Restaurant','location']]
        # loc_wise_cuisine=self.re_cu_loc.groupby(['location','Cusines_all']).agg({'Cusines_all':'count'})
        # loc_wise_cuisine=loc_wise_cuisine.rename(columns={'Cusines_all':'Available_in_restaurant'}).reset_index()
        # loc_wise_populer_cuisine=loc_wise_cuisine.groupby('location').max().reset_index()
        # loc_wise_populer_cuisine.rename(columns={'Cusines_all':'Populer cusines'},inplace=True)
        # loc_wise_populer_cuisine=loc_wise_populer_cuisine.drop(columns='Available_in_restaurant')
        # return loc_wise_populer_cuisine[loc_wise_populer_cuisine['location']==prefferd_loc].values[0]
# IndexError: index 0 is out of bounds for axis 0 with size 0


    # prefferd location wise average price for 1
    def avgPrice(self,prefferd_loc):
        # print(self.f_res_cusine_info.isna().sum())

        self.f_res_cusine_info["price_for_one"]=[int(i) for i in self.f_res_cusine_info["price_for_one"]]
        f_res_cusine_info_loc=self.f_res_cusine_info[self.f_res_cusine_info['location'].str.contains(prefferd_loc)]
        loc_wise_avg_priceforOne=f_res_cusine_info_loc.groupby('Restaurant').agg({'price_for_one':'mean'}).reset_index()
        # print(len(f_res_cusine_info_loc))
        loc_wise_avg_priceforOne.columns=["Restaurant","price_for_one"]
        # loc_wise_avg_priceforOne.to_csv("loc_wise_avg_priceforOne.csv")
        # loc_wise_avg_priceforOne.rename(columns={'price_for_one':'Average_price_for_1'},inplace=True)
        # return int(loc_wise_avg_priceforOne[loc_wise_avg_priceforOne['location'].str.contains(prefferd_loc)]["Average_price_for_1"].values[0])
        # print(np.mean(loc_wise_avg_priceforOne.price_for_one))
        return int(np.mean(loc_wise_avg_priceforOne.price_for_one))

    # preffered location wise popular restaurant and their cuisine
    def popularRestuarantAndCusine(self,prefferd_loc):
        # loc_wise_pop_res=self.f_res_cusine_info.groupby(['location','Name','cusines']).agg({'Rating':'max'}).reset_index().groupby('location').max().reset_index()
        # loc_wise_pop_res=loc_wise_pop_res.drop(columns='Rating')
        # loc_wise_pop_res= loc_wise_pop_res.rename(columns={'Name':'Popular Restaurant','cusines':'Available cusines'})
        # # return loc_wise_pop_res[loc_wise_pop_res['location']==prefferd_loc].values[0][1],loc_wise_pop_res[loc_wise_pop_res['location'].str.contains(prefferd_loc)].values[0][2]
        # return loc_wise_pop_res[loc_wise_pop_res['location']==prefferd_loc].values[0][1],loc_wise_pop_res[loc_wise_pop_res['location'].str.contains(prefferd_loc)].values[0][2]
        pop_res_cuisine= self.f_res_cusine_info[self.f_res_cusine_info['location'].str.contains(prefferd_loc)].groupby(['Restaurant','Cusines_all']).agg({'delivery_review_number':'max'}).reset_index()    
        pop_res_cuisine= pop_res_cuisine[pop_res_cuisine['delivery_review_number']==pop_res_cuisine['delivery_review_number'].max()]         
        pop_res_cuisine['available_cuisines'] = pop_res_cuisine.groupby(['Restaurant'])['Cusines_all'].transform(lambda x: ','.join(x))
        pop_res_cuisine.drop(columns='Cusines_all',inplace=True)
        pop_res_cuisine.drop_duplicates(inplace=True)
        return pop_res_cuisine['Restaurant'].values[0],','.join(pop_res_cuisine['available_cuisines'].values)

    # most popular restaurant for prefferd cusine near preffered location
    def prefCuisineResturant(self,selected_cusine_name,prefferd_loc):
        # res_delivery_reviwe = self.f_res_cusine_info[(self.f_res_cusine_info['Cusines_all'].str.contains(selected_cusine_name))& (self.f_res_cusine_info['location'].str.contains(prefferd_loc))].groupby('Restaurant').agg({'delivery_review_number': 'max'}).reset_index()
        # return temp2[(temp2['Cusines_all']== selected_cusine_name)&(temp2['location'].str.contains(prefferd_loc))]['Restaurant'].values[0]
        # return res_delivery_reviwe.sort_values('delivery_review_number',ascending=False).values[:,:1][0]
        pref_loc_pop_res = self.f_res_cusine_info[(self.f_res_cusine_info['Cusines_all'].str.contains(selected_cusine_name)) & (self.df['location'].str.contains(prefferd_loc))].groupby('Restaurant').agg({'delivery_review_number': 'max'}).reset_index()
        pref_loc_pop_res = pref_loc_pop_res.sort_values(by='delivery_review_number',ascending=False)
        return list(pref_loc_pop_res.values[:,:1])
        # return pref_loc_pop_res.values
        #pref_loc_pop_res.values[:,:1][0]
    
        
