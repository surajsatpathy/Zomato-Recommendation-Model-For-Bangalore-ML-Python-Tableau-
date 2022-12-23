
from flask import Flask, render_template, request
from part1 import Part1
from featureCreation import FeatureCreator
import pickle
import sklearn
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit',methods=['POST','GET'])
def showRecommendaion():
    obj=Part1()
    featureCreatorObj=FeatureCreator()
    if request.method=='POST':
        prefferd_loc=request.form['prefered-location']
        prefferd_loc=prefferd_loc.lower()
        selected_cusine_name=request.form['cuisine']
        selected_cusine_name = selected_cusine_name.lower()
        # selected_cusine_name=selected_cusine_name
        pref_price=request.form['prefered-price-for-one']
        pref_price=int(pref_price)
    ###############################  PART - 1  #####################################################
    cusines=obj.locationWisePopularCusines(prefferd_loc)
    avg_price=obj.avgPrice(prefferd_loc)
    pop_res,pop_res_cusine=obj.popularRestuarantAndCusine(prefferd_loc)
    pop_res_prefCus_wise=obj.prefCuisineResturant(prefferd_loc,selected_cusine_name)

    ###############################  PART - 2  #####################################################
    feature1,feature2=featureCreatorObj.transform(prefferd_loc,selected_cusine_name,pref_price)
    filename="saved_model//rfg_price_predictor.pickle"
    price_predictor = pickle.load(open(filename, 'rb'))
    suggested_price=price_predictor.predict([[feature1,feature2]])
    suggested_price=round(suggested_price[0],2)

    if pref_price > suggested_price:
        processed_suggested_price=suggested_price+(pref_price-suggested_price)*0.5
    else:
        processed_suggested_price=suggested_price

    return render_template('index.html',loc=prefferd_loc,price=pref_price,cuisine=selected_cusine_name,avg_price=avg_price,cusines=cusines,pop_res=pop_res,pop_res_cusine=pop_res_cusine,pop_res_prefCus_wise=pop_res_prefCus_wise,rec_price=suggested_price,pro_rec_price=processed_suggested_price)

if __name__ == "__main__":
    app.run(debug=True)