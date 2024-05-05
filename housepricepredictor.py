import streamlit as st
import pickle
import pandas as pd
import xgboost as xgb

hide_st_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""
st.set_page_config(page_title="House Price Predictor|Kigali", page_icon=":house_buildings:")
st.markdown(hide_st_style, unsafe_allow_html=True)
st.title('Predicting the house price in Kigali')
st.markdown('<style>h1{color: darkgreen;}</style>', unsafe_allow_html=True)

st.sidebar.header('About')
st.sidebar.info("""This project uses the data collected (Web Scrapped) from a website that list the houses for sale in Rwanda, 
and employs machine learning to predict the price of a house given its neighborhood, plot size, number of bedrooms and bathrooms, etc.""")
st.sidebar.header('Info')
st.sidebar.info("""Gaspard Nzasabimfura  \n Data Analyst, Scientist & Engineer  \n Email: nzagaspard@gmail.com  \n Tel: +250789779262""")
     
def predict(features):
    # with open('kigali houses model.sav', 'rb') as saved_model:
    #      model = pickle.load(saved_model)
    #      st.write(features)
    #      price = model.predict(features)
    model = xgb.Booster()
    model.load_model('kigali houses model.bin')
    features_values = features.values
    features_matrix = xgb.DMatrix(predictors)
    price = model.predict(features_matrix)

    return price

neighborhoods = ['','Gacuriro','Gahanga','Gatenga','Gikondo','Gisozi','Kabeza','Kabuga','Ndera','Rusororo',
                 'Kacyiru','Kagarama','Kagugu','Kanombe','Kibagabaga','Kicukiro','Kimihurura','Kimironko',
                 'Kinyinya','Kiyovu','Masaka','Niboyi','Nyamirambo','Nyarutarama','Rebero','Remera','Zindiro']
neighborhood = st.selectbox('Choose the Neighborhood',neighborhoods)
plotsize = ['','300 - 400', '400 - 500', '500 - 600', '700 - 800', '800 - 900', '900+']
plotsizes = st.selectbox('Choose the plotsize in sqm', plotsize)
bedrooms = st.slider('Select the number of bedrooms',3,5)
bathrooms = st.slider('Select the number of bathrooms',1,4)
parking = st.checkbox('Check if has parking')
wardrobes = st.checkbox('Check if has built-in wardrobes')
cabinets = st.checkbox('Check if has kitchen with cabinets')
balcony = st.checkbox('Check if has balcony')
boys_quarters = st.checkbox("Check if has boys' quarter/annex")
col1, col2, col3 = st.columns(3)
predict_button = col2.button('Predict')
prediction_space = st.empty()
 
def prepare_predictors():
    selected_features = ['Bedrooms', 'Bathrooms', 'Wardrobes_No', 'Cabinets_No',
    'Balcony_No', 'Parking_No', 'Quarters_No', 'Neighborhood_Gacuriro', 'Neighborhood_Gahanga',
    'Neighborhood_Gatenga/Gikondo', 'Neighborhood_Gisozi', 'Neighborhood_Kabeza',
     'Neighborhood_Kabuga/Ndera/Rusororo', 'Neighborhood_Kacyiru', 'Neighborhood_Kagarama',
     'Neighborhood_Kagugu', 'Neighborhood_Kanombe', 'Neighborhood_Kibagabaga', 'Neighborhood_Kicukiro',
     'Neighborhood_Kimihurura', 'Neighborhood_Kimironko', 'Neighborhood_Kinyinya', 'Neighborhood_Masaka',
     'Neighborhood_Niboyi', 'Neighborhood_Nyamirambo', 'Neighborhood_Nyarutarama', 'Neighborhood_Rebero',
     'Neighborhood_Remera', 'Plot Category_2', 'Plot Category_3', 'Plot Category_4', 'Plot Category_5',
     'Plot Category_6', 'Plot Category_7']
     
    predictors = {}
    for feature in selected_features:
        predictors[feature] = [0]
    predictors = pd.DataFrame(predictors)
    
    #Bedrooms & Bathrooms
    predictors['Bedrooms'] = bedrooms
    predictors['Bathrooms'] = bathrooms
    
    #Neighboorhood
    for column in predictors.columns:
        if column.find(neighborhood) != -1:
            predictors[column]=1
    
    #Plot Size
    if plotsizes == '400 - 500':
        predictors['Plot Category_2'] = 1
    
    elif plotsizes == '500 - 600':
        predictors['Plot Category_3'] = 1
    
    elif plotsizes == '600 - 700':
        predictors['Plot Category_4'] = 1
    
    elif plotsizes == '700 - 800':
        predictors['Plot Category_5'] = 1
    
    elif plotsizes == '800 - 900':
        predictors['Plot Category_6'] = 1
    
    elif plotsizes == '900+':
        predictors['Plot Category_7'] = 1
        
    #Parking
    if not parking:
        predictors['Parking_No'] = 1
    
    #Wardrobes
    if not wardrobes:
        predictors['Wardrobes_No'] = 1
        
    #Kitchen with Cabinets
    if cabinets:
        predictors['Cabinets_No'] = 1
    
    #Balcony
    if not balcony:
        predictors['Balcony_No'] = 1
        
    #Quarters
    if not boys_quarters:
        predictors['Quarters_No'] = 1
    
    return predictors

if predict_button:
    if (neighborhood == '') | (plotsizes == ''):
        st.error('Please select the neighborhood and the plotsize!')
    else:
        try:
            with st.spinner('Please wait. Predicting ...'):            
                predictors = prepare_predictors()
                predicted_price = round(predict(predictors)[0], -6)
                prediction_space.header(f'The predicted price is {int(predicted_price):,} Rwf')
        except Exception as e:
            st.write(e)
            st.error('Something went wrong, contact the developer!')
     
st.write('#')
disclaimer = st.expander('Details & Disclaimer!')
disclaimer.markdown("""  :warning: This project was developed for practice purposes. Due to some information 
that would help to accurately predict the house price that were not given when listing the houses
in the scraped data, I don't advise to consider and use the predicted prices here as ground truth!""")
disclaimer.markdown(""" :information_source: The notebook used to for explaratory data analysis and building machine learning models can be found [here](https://github.com/nzagaspard/Predicting-House-Prices-In-Kigali/blob/ce89583c83afc587161b31a597913b3f1f32b7b4/Modeling/Predicting%20House%20Price%20In%20Kigali%20Using%20Machine%20Learning.ipynb)""")
