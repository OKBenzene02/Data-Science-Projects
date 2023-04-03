import numpy as np

from flight import app
from flask import render_template, flash, url_for, request, redirect
import pandas as pd
import sklearn as sk
from sklearn.preprocessing import StandardScaler
import pickle

address_flight = 'C:\\Users\\liyak\\OneDrive\\Documents\\Python Scripts\\Some Projects\\flight price prediction\\flight_model.pkl'
address_house = 'C:\\Users\\liyak\\OneDrive\\Documents\\Python Scripts\\Some Projects\\house price prediction\\house_preds_model.pkl'
flight_model = pickle.load(open(address_flight, 'rb'))
house_model = pickle.load(open(address_house, 'rb'))


@app.route('/')
@app.route('/home')
def hello_world():
    return render_template('home.html')


@app.route('/flights', methods=['GET', 'POST'])
def flight_preds():
    if request.method == "POST":
        # Getting Departure details
        dep_time = request.form['Dep_Time']
        journey_day = pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").day
        journey_month = pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").month

        departure_hour = pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").hour
        departure_min = pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").minute

        # Getting Arrival details
        arrival_time = request.form['Arrival_Time']
        arrival_hour = pd.to_datetime(arrival_time, format="%Y-%m-%dT%H:%M").hour
        arrival_min = pd.to_datetime(arrival_time, format="%Y-%m-%dT%H:%M").minute

        # Getting Total Stops
        total_stops = int(request.form['Total_stops'])

        # Getting Duration Hour and Duration Minute
        dur_hour = abs(arrival_hour - departure_hour)
        dur_min = abs(arrival_min - departure_min)

        # Getting Airline
        airline = request.form['Airline']
        if airline == "Jet Airways":
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 1
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        elif airline == "IndiGo":
            Air_India = 0
            GoAir = 0
            IndiGo = 1
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        elif airline == "Air India":
            Air_India = 1
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        elif airline == "Multiple carriers":
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 1
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        elif airline == "SpiceJet":
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 1
            Trujet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        elif airline == "Vistara":
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 0
            Vistara = 1
            Vistara_Premium_economy = 0

        elif airline == "GoAir":
            Air_India = 0
            GoAir = 1
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        elif airline == "Multiple carriers Premium economy":
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 1
            SpiceJet = 0
            Trujet = 0
            Vistara = 1
            Vistara_Premium_economy = 0

        elif airline == "Jet Airways Business":
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 1
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 0
            Vistara = 1
            Vistara_Premium_economy = 0

        elif airline == "Vistara Premium economy":
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 1
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 0
            Vistara = 1
            Vistara_Premium_economy = 1

        elif airline == "Trujet":
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 1
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 1
            Vistara = 0
            Vistara_Premium_economy = 0

        else:
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 1
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Trujet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        # Getting the Source information
        source = request.form['Source']
        if source == 'Delhi':
            s_Delhi = 1
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        elif source == 'Kolkata':
            s_Delhi = 0
            s_Kolkata = 1
            s_Mumbai = 0
            s_Chennai = 0

        elif source == 'Mumbai':
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 1
            s_Chennai = 0

        elif source == 'Chennai':
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 1

        else:
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        # Getting the Destination details
        destination = request.form['Destination']
        if destination == 'Cochin':
            d_Cochin = 1
            d_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        elif destination == 'Delhi':
            d_Cochin = 0
            d_Delhi = 1
            d_Hyderabad = 0
            d_Kolkata = 0

        elif destination == 'Hyderabad':
            d_Cochin = 0
            d_Delhi = 0
            d_Hyderabad = 1
            d_Kolkata = 0

        elif destination == 'Kolkata':
            d_Cochin = 0
            d_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 1

        else:
            d_Cochin = 0
            d_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        predictions = flight_model.predict([[
            total_stops,
            journey_day,
            journey_month,
            departure_hour,
            departure_min,
            arrival_hour,
            arrival_min,
            dur_hour,
            dur_min,
            s_Chennai,
            s_Delhi,
            s_Kolkata,
            s_Mumbai,
            d_Cochin,
            d_Delhi,
            d_Hyderabad,
            d_Kolkata,
            Air_India,
            GoAir,
            IndiGo,
            Jet_Airways,
            Jet_Airways_Business,
            Multiple_carriers,
            Multiple_carriers_Premium_economy,
            SpiceJet,
            Trujet,
            Vistara,
            Vistara_Premium_economy
        ]])[0]

        price = round(predictions, 2)

        return render_template('flights.html', predictions=f"You will have to pay Rs. {price}")

    else:
        return render_template('flights.html')


@app.route('/house', methods=['GET', 'POST'])
def house_preds():
    if request.method == "POST":
        # Getting Zoning Details
        mszoning = request.form['MS_zoning']
        if mszoning == 'mszoning_c':
            MSZoning_C = 1
            MSZoning_FV = 0
            MSZoning_RH = 0
            MSZoning_RL = 0
            MSZoning_RM = 0

        elif mszoning == "mszoning_fv":
            MSZoning_C = 0
            MSZoning_FV = 1
            MSZoning_RH = 0
            MSZoning_RL = 0
            MSZoning_RM = 0

        elif mszoning == "mszoning_rh":
            MSZoning_C = 0
            MSZoning_FV = 0
            MSZoning_RH = 1
            MSZoning_RL = 0
            MSZoning_RM = 0

        elif mszoning == "mszoning_rl":
            MSZoning_C = 0
            MSZoning_FV = 0
            MSZoning_RH = 0
            MSZoning_RL = 1
            MSZoning_RM = 0

        else:
            MSZoning_C = 0
            MSZoning_FV = 0
            MSZoning_RH = 0
            MSZoning_RL = 0
            MSZoning_RM = 1

        # Getting details of Sale Condition
        sale_condition = request.form['SaleCondition']
        if sale_condition == "sc_normal":
            SaleCondition_Abnorml = 0
            SaleCondition_AdjLand = 0
            SaleCondition_Alloca = 0
            SaleCondition_Family = 0
            SaleCondition_Normal = 1
            SaleCondition_Partial = 0

        elif sale_condition == 'sc_abnormal':
            SaleCondition_Abnorml = 1
            SaleCondition_AdjLand = 0
            SaleCondition_Alloca = 0
            SaleCondition_Family = 0
            SaleCondition_Normal = 0
            SaleCondition_Partial = 0

        elif sale_condition == 'sc_adj':
            SaleCondition_Abnorml = 0
            SaleCondition_AdjLand = 1
            SaleCondition_Alloca = 0
            SaleCondition_Family = 0
            SaleCondition_Normal = 0
            SaleCondition_Partial = 0

        elif sale_condition == 'sc_alloc':
            SaleCondition_Abnorml = 0
            SaleCondition_AdjLand = 0
            SaleCondition_Alloca = 1
            SaleCondition_Family = 0
            SaleCondition_Normal = 0
            SaleCondition_Partial = 0

        elif sale_condition == 'sc_family':
            SaleCondition_Abnorml = 0
            SaleCondition_AdjLand = 0
            SaleCondition_Alloca = 0
            SaleCondition_Family = 1
            SaleCondition_Normal = 0
            SaleCondition_Partial = 0

        else:
            SaleCondition_Abnorml = 0
            SaleCondition_AdjLand = 0
            SaleCondition_Alloca = 0
            SaleCondition_Family = 0
            SaleCondition_Normal = 0
            SaleCondition_Partial = 1

        # Getting the details of Land Slope
        land_slope = request.form['LandSlope']
        if land_slope == 'ls_gtl':
            LandSlope_Gtl = 1
            LandSlope_Mod = 0
            LandSlope_Sev = 0

        elif land_slope == 'ls_mod':
            LandSlope_Gtl = 0
            LandSlope_Mod = 1
            LandSlope_Sev = 0

        else:
            LandSlope_Gtl = 0
            LandSlope_Mod = 0
            LandSlope_Sev = 1

        # Getting the details of Dwelling type
        dwell_type = request.form['Dwelling_type']
        if dwell_type == 'dwell_one':
            BldgType_1Fam = 1
            BldgType_2fmCon = 0
            BldgType_Duplex = 0
            BldgType_Twnhs = 0
            BldgType_TwnhsE = 0

        elif dwell_type == 'dwell_two':
            BldgType_1Fam = 0
            BldgType_2fmCon = 1
            BldgType_Duplex = 0
            BldgType_Twnhs = 0
            BldgType_TwnhsE = 0

        elif dwell_type == 'dwell_duplex':
            BldgType_1Fam = 0
            BldgType_2fmCon = 0
            BldgType_Duplex = 1
            BldgType_Twnhs = 0
            BldgType_TwnhsE = 0

        elif dwell_type == 'dwell_town_inside':
            BldgType_1Fam = 0
            BldgType_2fmCon = 0
            BldgType_Duplex = 0
            BldgType_Twnhs = 1
            BldgType_TwnhsE = 0

        else:
            BldgType_1Fam = 0
            BldgType_2fmCon = 0
            BldgType_Duplex = 0
            BldgType_Twnhs = 0
            BldgType_TwnhsE = 1

        # Getting the details of Year Built
        year_built = request.form['YearBuilt']
        YearBuilt = pd.to_datetime(year_built, format="%Y-%m-%dT%H:%M").year

        # Getting the details of Year Remodeled
        year_remodel = request.form['YearRemodeled']
        YearRemodeled = pd.to_datetime(year_remodel, format="%Y-%m-%dT%H:%M").year

        # Getting the details of Total Basement sqft
        TotalBsmtSF = float(request.form['TotalBasementSF'])

        # Getting the details of Graded living area
        GrLivArea = float(request.form['GrLivArea'])

        # Getting the details of Above Graded Rooms
        TotRmsAbvGrd = int(request.form['TotRmsAbvGrd'])

        # Getting the details of First Floor Square foot
        FirstFloorSqft = float(request.form['FirstFloorSqft'])

        # Getting the details of Garage Area
        GarageArea = float(request.form['GarageArea'])

        # Getting the details of Garage Cars
        GarageCars = int(request.form['GarageCars'])

        # Getting the details of Utilities
        utilities = request.form['Utilities']
        if utilities == 'utils_pub':
            Utilities_AllPub = 1
            Utilities_NoSeWa = 0
        else:
            Utilities_NoSeWa = 1
            Utilities_AllPub = 0

        # Getting the details of Heating type
        heating = request.form['Heating']
        if heating == 'heat_floor':
            Heating_Floor = 1
            Heating_GasA = 0
            Heating_GasW = 0
            Heating_Grav = 0
            Heating_OthW = 0
            Heating_Wall = 0

        elif heating == 'heat_gas_a':
            Heating_Floor = 0
            Heating_GasA = 1
            Heating_GasW = 0
            Heating_Grav = 0
            Heating_OthW = 0
            Heating_Wall = 0

        elif heating == 'heat_gas_w':
            Heating_Floor = 0
            Heating_GasA = 0
            Heating_GasW = 1
            Heating_Grav = 0
            Heating_OthW = 0
            Heating_Wall = 0

        elif heating == 'heat_grav':
            Heating_Floor = 0
            Heating_GasA = 0
            Heating_GasW = 0
            Heating_Grav = 1
            Heating_OthW = 0
            Heating_Wall = 0

        elif heating == 'heat_oth':
            Heating_Floor = 1
            Heating_GasA = 0
            Heating_GasW = 0
            Heating_Grav = 0
            Heating_OthW = 1
            Heating_Wall = 0

        else:
            Heating_Floor = 0
            Heating_GasA = 0
            Heating_GasW = 0
            Heating_Grav = 0
            Heating_OthW = 0
            Heating_Wall = 1

        # Getting the details of Kitchen Quality
        kitchen = request.form['Kitchen']
        if kitchen == 'kq_ex':
            KitchenQual_Ex = 1
            KitchenQual_Fa = 0
            KitchenQual_Gd = 0
            KitchenQual_TA = 0

        elif kitchen == 'kq_gd':
            KitchenQual_Ex = 0
            KitchenQual_Fa = 0
            KitchenQual_Gd = 1
            KitchenQual_TA = 0

        elif kitchen == 'kq_ta':
            KitchenQual_Ex = 0
            KitchenQual_Fa = 0
            KitchenQual_Gd = 0
            KitchenQual_TA = 1

        else:
            KitchenQual_Ex = 0
            KitchenQual_Fa = 1
            KitchenQual_Gd = 0
            KitchenQual_TA = 0

        # Getting the details of Full Bath
        FullBath = int(request.form['FullBath'])

        # Getting the details of Overall Quality
        OverallQual = int(request.form['OverallQual'])

        # Making Predictions

        scaler = StandardScaler()
        preds_list_encoded = scaler.fit_transform([[OverallQual, YearBuilt, YearRemodeled, TotalBsmtSF, FirstFloorSqft,
                                                    GrLivArea, FullBath, TotRmsAbvGrd, GarageCars, GarageArea]])

        preds_list = [preds_list_encoded[0][0], preds_list_encoded[0][1], preds_list_encoded[0][2], preds_list_encoded[0][3],
                      preds_list_encoded[0][4], preds_list_encoded[0][5], preds_list_encoded[0][6], preds_list_encoded[0][7],
                      preds_list_encoded[0][8], preds_list_encoded[0][9], MSZoning_C, MSZoning_FV, MSZoning_RH,
                      MSZoning_RL, MSZoning_RM, Utilities_AllPub,
                      Utilities_NoSeWa, BldgType_1Fam, BldgType_2fmCon, BldgType_Duplex, BldgType_Twnhs, BldgType_TwnhsE,
                      Heating_Floor, Heating_GasA, Heating_GasW, Heating_Grav,
                      Heating_OthW, Heating_Wall, KitchenQual_Ex, KitchenQual_Fa, KitchenQual_Gd, KitchenQual_TA,
                      SaleCondition_Abnorml, SaleCondition_AdjLand,
                      SaleCondition_Alloca, SaleCondition_Family, SaleCondition_Normal, SaleCondition_Partial,
                      LandSlope_Gtl, LandSlope_Mod, LandSlope_Sev
                      ]

        predictions = house_model.predict([preds_list])[0]
        price = round(predictions, 2)
        return render_template('HousePrice.html', predictions=f"You will have to pay Rs. {price}")

    else:
        return render_template('HousePrice.html')


@app.route('/stocks', methods=['GET', 'POST'])
def stocks_preds():
    tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC', 'NKE', 'WMT', 'TSLA', 'MSFT']
    stock_name = ['Bank of America', 'Citigroup', 'Goldmann Sachs', 'JP Morgan',
                  'Morgan Stanley', 'Wells Fargo', 'Nike', 'Walmart', 'Tesla', 'Microsoft']
    max_close = [49.38, 81.91, 423.85, 171.78, 108.73, 65.93, 177.51, 159.87,
                 409.97, 343.11]
    max_high = [50.11, 83.11, 426.158, 172.96, 109.73, 66.31, 179.1,
                160.77, 414.497, 349.67]

    return render_template('stocks.html', max_closing=max_close, max_high=max_high, tickers=tickers, stock_name=stock_name)
