# My first program to fetch stock market data using API
# Project: AI Powered Stock Screening Web App

import yfinance as yf
import os
import json

# selecting a company ticker (Infosys - Indian stock)
company_symbol = "INFY.NS"

# creating a folder to store API data
folder_name = "api_data"

if not os.path.exists(folder_name):
    os.mkdir(folder_name)

print("Connecting to Market API (Yahoo Finance)...")

# creating ticker object (API connection)
stock_data = yf.Ticker(company_symbol)

#  API CALL 1: Company Information 
print("\nFetching Company Information...")
company_info = stock_data.info

# saving company info as JSON file
company_file = open(folder_name + "/company_info.json", "w")
json.dump(company_info, company_file, indent=4)
company_file.close()

print("Company Information saved successfully!")
print(company_info)


#  API CALL 2: Fundamental Data 
print("\nFetching Fundamental Financial Data...")
fundamental_data = stock_data.financials

# saving fundamental data as csv
fundamental_data.to_csv(folder_name + "/fundamental_data.csv")
print("Fundamental Data saved successfully!")


#  API CALL 3: Historical Stock Data 
print("\nFetching Historical Stock Data (1 Year)...")
historical_data = stock_data.history(period="1y")

# saving historical data
historical_data.to_csv(folder_name + "/historical_data.csv")
print("Historical Data saved successfully!")

# printing first 5 rows
print("\nSample Historical Data:")
print(historical_data.head())

print("\nAll 3 API calls completed and data stored locally.")
