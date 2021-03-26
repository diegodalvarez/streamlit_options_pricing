import yfinance as yf
import datetime as dt
import streamlit as st

from streamlit_options_calculator import *

calculations_method = ['monte carlo', 'Black Scholes']

st.header("Get Options Chain")
find_options = st.sidebar.selectbox("Select method", ("ticker lookup", "manual"))

today = dt.datetime.today()

if find_options == "ticker lookup":

    ticker_input = st.text_input('Please enter your company ticker here:')
    status_radio = st.radio('Please click Search when you are ready.', ('Entry', 'Search'))
    
    select_contract_type = False
    
    if status_radio == "Search":
        
        ticker = yf.Ticker(str(ticker_input))
        expirations = list(ticker.options)
        
        expiration = st.selectbox("select expiration date", expirations)
        option_chain = ticker.option_chain(date = expiration)
        calls = option_chain.calls.sort_values("lastTradeDate")
        puts = option_chain.puts.sort_values("lastTradeDate")
        
        st.subheader("Option Chain - Calls")
        st.dataframe(calls)
        
        st.subheader("Option Chain - Puts")
        st.dataframe(puts)
        
        select_contract_type = True
        
    if select_contract_type == True:
        
        today = dt.datetime.today() 
        start = today - dt.timedelta(days = 2)
        ticker = ticker_input
        df = yf.download(ticker, start, today)['Close']
        
        status_radio = st.radio('Please click Search when you are ready.', ('Call', 'Put'))
        
        if status_radio == "Call":
            
            strikes = calls['strike'].tolist()
            strike = st.selectbox("select a strike price", strikes)
            counter = 0
            
            for i in strikes:
                
                if i == strike:
                    break
                
                else:
                    counter += 1
            
            vol = calls['impliedVolatility'][counter]
            spot = df[len(df) - 1]
            days_to_expiration = (dt.datetime.strptime(expiration, "%Y-%m-%d") - today).days
            
            st.subheader("double check information")
            st.write("days to expiration:", days_to_expiration)
            st.write("strike:", strike)
            st.write("spot:", round(spot,2))
            st.write("vol:", round(vol,2))
            
            risk_free = st.number_input("risk free rate")
            options = options_calculation(days_to_expiration, strike, spot, vol, risk_free)
            
            calculation_method = st.selectbox("select a calculation method", calculations_method)
            
            if calculation_method == "monte carlo":
                
                start = 100000
                simulations = []
                simulations.append(start)
                max_num = 10
                
                for i in range(max_num):
                    
                    number = (i+1) * start
                    simulations.append(number)
                    
                simulation_num = st.selectbox('select number of simulations', simulations)
                value = options.MCcalculation(simulation_num)
                st.write(value)
                
            if calculation_method == "Black Scholes":
                
                value = options.bsm_call_value()
                st.write(round(value,2))
                
        
        if status_radio == "Put":
            
            st.subheader("Put Options calculation in progress")
            
            '''
            strikes = calls['strike'].tolist()
            strike = st.selectbox("select a strike price", strikes)
            counter = 0
            
            for i in strikes:
                
                if i == strike:
                    break
                
                else:
                    counter += 1
            
            vol = puts['impliedVolatility'][counter]
            spot = df[len(df) - 1]
            days_to_expiration = (dt.datetime.strptime(expiration, "%Y-%m-%d") - today).days
            
            st.subheader("double check information")
            st.write("days to expiration:", days_to_expiration)
            st.write("strike:", strike)
            st.write("spot:", spot)
            st.write("vol:", vol)
            
            risk_free = st.number_input("risk free rate")
            options = options_calculation(days_to_expiration, strike, spot, vol, risk_free)
            
            calculation_method = st.selectbox("select a calculation method", calculations_method)
            
            if calculation_method == "monte carlo":
                
                start = 100000
                simulations = []
                simulations.append(start)
                max_num = 10
                
                for i in range(max_num):
                    
                    number = (i+1) * start
                    simulations.append(number)
                    
                simulation_num = st.selectbox('select number of simulations', simulations)
                value = options.MCcalculation(simulation_num)
                st.write(value)
            '''
            
if find_options == "manual":
    
    st.subheader("for call options")
    
    tomorrow = today + dt.timedelta(days=1)
    today = today.date()
    expiration = st.date_input("Expiration", tomorrow)
    
    strike = st.number_input("Strike")
    spot = st.number_input("Spot")
    vol = st.number_input("vol")
    risk_free = st.number_input("risk free rate")
    
    calculation_method = st.selectbox("select a calculation method", calculations_method)
    days_to_expiration = (expiration - today).days
    options = options_calculation(days_to_expiration, strike, spot, vol, risk_free)
    
    if calculation_method == "monte carlo":
        
        start = 100000
        simulations = []
        simulations.append(start)
        max_num = 10
        
        for i in range(max_num):
            
            number = (i+1) * start
            simulations.append(number)
            
        simulation_num = st.selectbox('select number of simulations', simulations)
        st.write("days to expiration:", days_to_expiration)
        
        value = options.MCcalculation(simulation_num)
        st.write(value)
        
    if calculation_method == "Black Scholes":
        
        status_radio = st.radio('Click run when ready.', ('stop', 'run'))
        
        if status_radio == "run":
        
            value = options.bsm_call_value()
            st.write(round(value,2))
