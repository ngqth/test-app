# %%
import pandas as pd

# %%
data_production = pd.read_excel('Production.xlsx')

# %%
data_sales = pd.read_excel('Sales.xlsx')

# %%
data_dates = pd.read_excel('Date.xlsx')

# %%
data_dates = data_dates[['Date', 'StartOfWeek']]
data_dates.rename(columns={'Date': 'date', 'StartOfWeek': 'week_start'}, inplace=True)    # Rename column
data_dates_1 = data_dates.copy()    # Copy the data_dates table

# %%
data_dates_1['date_next_week'] = data_dates_1['week_start'] + pd.DateOffset(7)    # Add 7 days to date

# %%
# Join the data_sales and data_sales tables on 'Date Sold' and 'date' columns
data_sales = data_sales.merge(data_dates, left_on='Date Sold', right_on='date', how='left')
data_sales_1 = data_sales.copy()    # Copy the data_sales table

# %%
# Add new column 'Sold amt' in data_sales table, using 'Sold Qty' * 'Price Sold' columns
data_sales['Sold amt'] = data_sales['Sold Qty'] * data_sales['Price Sold']  # Add new column

# %%
# Groupy by 'ID', 'Name', 'week_start' and sum the 'Sold Qty' and 'Sold amt' columns
data_sales_grouped = data_sales.groupby(['ID', 'Name', 'week_start'])[['Sold Qty', 'Sold amt']].sum().reset_index()

# %%
# Add new colum 'Mean(Price Sold)' in data_sales_grouped table, using 'Sold amt' / 'Sold Qty' columns
data_sales_grouped['Mean(Price Sold)'] = data_sales_grouped['Sold amt'] / data_sales_grouped['Sold Qty']  # Add new column

# %%
# Remove column 'Sold amt' from data_sales_grouped table
data_sales_grouped.drop(columns='Sold amt', inplace=True)    # Remove column

# %%
# Join data_sales_grouped with data_production table on 'ID' and 'week_start' columns, with 'ID' and 'Date' columns
data_production = data_production.merge(data_sales_grouped, left_on=['ID', 'Date'], right_on=['ID', 'week_start'], how='left')
data_production.drop(columns=['Name_y', 'week_start'], inplace=True)    # Remove column
data_production.rename(columns={'Name_x': 'Name'}, inplace=True)    # Rename column

# %%
print(data_production.shape)

# %%
# Sort data_production table by 'ID' desc and 'Date' asc columns
data_production.sort_values(['ID', 'Date'], ascending=[False, True], inplace=True)    # Sort table

# %%
# Join data_production table with data_dates_1 table on 'Date' and 'date' columns, only keep 'date_next_week' column from data_dates_1 table
data_production = data_production.merge(data_dates_1[['date', 'date_next_week']], left_on='Date', right_on='date', how='left')

# %%
data_production.drop(columns=['date'], inplace=True)    # Remove column
# data_production.rename(columns={'Date': 'date', 'date_next_week_x': 'date_next_week'}, inplace=True)    # Rename column

# %%
print(data_production.dtypes)

# %%
# Fill missing values in column with float type with 0
data_production['Production'] = data_production['Production'].fillna(0)    # Fill missing values
data_production['Price Submited'] = data_production['Price Submited'].fillna(0)    # Fill missing values
data_production['Sold Qty'] = data_production['Sold Qty'].fillna(0)    # Fill missing values
data_production['Mean(Price Sold)'] = data_production['Mean(Price Sold)'].fillna(0)    # Fill missing values

# %%
# Order data_production table by 'ID' and 'Date' columns
data_production.sort_values(['ID', 'Date'], inplace=True)    # Sort table

# Add cumulative sum column 'Running Sold' of 'Sum(Sold Qty)' column by 'ID' group
data_production_1 = data_production.copy()    # Copy the data_production table
data_production_1['Running Sold'] = data_production_1.groupby('ID')['Sold Qty'].cumsum()    # Add new column

# %%
# Add cumulative sum column 'Running Production' of 'Production' column by 'ID' group
data_production_1['Running Production'] = data_production_1.groupby('ID')['Production'].cumsum()    # Add new column

# %%
data_production_1 = data_production_1.drop(columns=['Name', 'Date', 'Price Submited', 'Sold Qty', 'Mean(Price Sold)'])    # Remove columns

# %%
# data_production

# %%
# data_production_1

# %%
data_production_2 = data_production.merge(data_production_1, left_on=['Date', 'ID'], right_on=['date_next_week', 'ID'], how='left')    # Merge tables

# %%
# print(data_production_2.dtypes)

# %%
# Keep columns 'ID', 'Name', 'Date', 'Production', 'Price Submited', 'Sold Qty', 'Mean(Price Sold)', 'Running Sold', 'Running Production'
data_production_2 = data_production_2[['ID', 'Name', 'Date', 'Production_x', 'Price Submited', 'Sold Qty', 'Mean(Price Sold)', 'Running Sold', 'Running Production']]

# %%
# rename columns 'ID_x', 'Production_x' to 'ID', 'Production'
data_production_2.rename(columns={'ID_x': 'ID', 'Production_x': 'Production'}, inplace=True)    # Rename columns

# %%
data_production_2['Production'] =data_production_2['Production'].fillna(0)    # Fill missing values
data_production_2['Price Submited'] =data_production_2['Price Submited'].fillna(0)    # Fill missing values
data_production_2['Sold Qty'] =data_production_2['Sold Qty'].fillna(0)    # Fill missing values
data_production_2['Mean(Price Sold)'] = data_production_2['Mean(Price Sold)'].fillna(0)    # Fill missing values
data_production_2['Running Sold'] =data_production_2['Running Sold'].fillna(0)    # Fill missing values
data_production_2['Running Production'] = data_production_2['Running Production'].fillna(0)    # Fill missing values

# %%
data_production_2['Opening'] = data_production_2['Running Production'] - data_production_2['Running Sold']    # Add new column

# %%
data_production_2['Available'] = data_production_2['Production'] + data_production_2['Opening']    # Add new column
data_production_2['Closing'] = data_production_2['Available'] - data_production_2['Sold Qty']    # Add new column
# data_production_2

# %%
data_production_2['rank'] = data_production_2.groupby('ID').cumcount()

# %%
print(data_production_2['ID'].shift(1))

# %%
# Add new column 'prev_available' with logic: if "ID" = ["ID",-1] then ["Available",-1] else 0
if not data_production_2['ID'].shift(1).isnull().all():
    data_production_2['prev_available'] = data_production_2['Available'].shift(1).where(
        data_production_2['ID'] == data_production_2['ID'].shift(1), 0
    )
# data_production_2

# %%
data_production_2['prev_available']

# %%
data_production_2['prev_closing'] = data_production_2.apply(
    lambda row: 0 if row['prev_available'] == 0 else data_production_2.loc[row.name - 1, 'Closing'] if row.name > 0 else 0,
    axis=1
)

# %%
data_production_2['close_rate'] = 0.0

# %%
# Iterate through each row to calculate 'Init rate'
for i in range(len(data_production_2)):
    if data_production_2.at[i, 'rank'] == 0:
        data_production_2.at[i, 'close_rate'] = data_production_2.at[i, 'Price Submited']
    else:
        # Calculate using the formula with previous 'Init rate'
        previous_init_rate = data_production_2.at[i-1, 'close_rate']
        stock_available = data_production_2.at[i, 'prev_closing']
        production_weight = data_production_2.at[i, 'Production']
        production_rate = data_production_2.at[i, 'Price Submited']
        
        data_production_2.at[i, 'close_rate'] = (stock_available * previous_init_rate + production_weight * production_rate) / (stock_available + production_weight)

# %%
# data_production_2
data_production_2.sort_values(['ID', 'rank'], ascending=[True, True], inplace=True)    # Sort table

# %%
# Add new column 'start_rate' with logic: if "rank" = 0 then 0 else ["Init rate",-1]
data_production_2['start_rate'] = data_production_2['close_rate'].shift(1).where(data_production_2['rank'] != 0, 0)

# %%
# Write the data_production_2 table to a new Excel file
# change 'date' column type from datetime to date
data_production_2['Date'] = data_production_2['Date'].dt.date    # Change column type
data_production_2.to_excel('summary_.xlsx', index=False)    # Write to Excel file

# %%
data_production_3 = data_production_2[['ID', 'Date', 'close_rate']]
# %%
data_production_3['Date'] = pd.to_datetime(data_production_3['Date'])
# %%
# data_sales_1
# %%
data_sales_1 = data_sales_1.drop(columns=['date'])
# %%
# data_sales_1.head()
# %%
# Inner join data_sales_1 and data_production_3 tables on 'ID' and 'Date'='week_start' columns
data_sales_1 = data_sales_1.merge(data_production_3, left_on=['ID', 'week_start'], right_on=['ID', 'Date'], how='inner')
# data_sales_1.head()
# %%
data_sales_1 = data_sales_1.drop(columns=['Date', 'week_start'])
# data_sales_1.head()
# %%
data_sales_1.sort_values(['ID', 'Date Sold'], ascending=[True, True], inplace=True)    # Sort table
# %%
# Add new column 'Counter' indexing row from 1, do not group by any column
data_sales_1['Counter'] = range(1, len(data_sales_1) + 1)    # Add new column
# data_sales_1.head()
# %%
data_sales_1['Date Sold'] = data_sales_1['Date Sold'].dt.date    # Change column type
data_sales_1.to_excel('sold_.xlsx', index=False)    # Write to Excel file
# %%