# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 22:15:45 2018

@author: Mezu
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

#Let's read in data and parse the Date field into Datetime
df_water_quality = pd.read_csv(
    'https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/'
    'master/module4/Data/riverkeeper_data_2013.csv',parse_dates=['Date'])

#Convert datetime to date string in Year, month day for sorting
df_water_quality['Date_str']=df_water_quality['Date'].dt.strftime('%Y-%m-%d')
df_water_quality['Date']= pd.to_datetime(df_water_quality['Date'])

# Start and End of observations
start = min(df_water_quality['Date'])
end = max(df_water_quality['Date'])
# We notice some '<' and '>' signs in the Enterocount column. Let's replace them

#for '<' Let's find those values
dummy=df_water_quality[df_water_quality['EnteroCount'].str.startswith('<', na=False)].EnteroCount.unique()


#we can see that it is <1 and <10  are the values we need to replace that have <
df_water_quality['EnteroCount'].replace(to_replace = "<10", value = 9, inplace = True)
df_water_quality['EnteroCount'].replace(to_replace = "<1", value = 0, inplace = True)

#for '>' Let's find those values
dummy2=df_water_quality[df_water_quality['EnteroCount'].str.startswith('>', na=False)].EnteroCount.unique()

#we can see that it is >2420 and >24196 are the values we need to replace that have <
df_water_quality['EnteroCount'].replace(to_replace = ">2420", value = 2421, inplace = True)
df_water_quality['EnteroCount'].replace(to_replace = ">24196", value = 24197, inplace = True)

#Ensure that the field is numeric
df_water_quality['EnteroCount'] = pd.to_numeric(df_water_quality['EnteroCount'])


def Recommended_Sites(userdate):
    date=pd.to_datetime(userdate)

    #Let's filter out records with test dates greater than chosen date

    df_water_quality2 =df_water_quality[df_water_quality['Date']<=date]
    
    
    #Calculate the number days the last test was taken before the arbitrary selected date 
    #for each row in dataset.
    
    df_water_quality2['Date_rank'] = date - df_water_quality2['Date']
    
    #for all the sites in filtered data set get the average Enterocount
    df_wq_mean_entero = pd.DataFrame(df_water_quality2.groupby(['Site'],as_index=False)['EnteroCount'].mean())
    df_wq_mean_entero=df_wq_mean_entero.rename(columns = {'EnteroCount':'Mean_EnteroCount'})
    #Join result from df_wq_mean_entero to the df_water_quality2
    
    df_water_quality3 = pd.merge(df_water_quality2, df_wq_mean_entero, how='left',on=['Site'])
    
    
    #Let's find the Sites that were tested within last 30days
    df_water_quality4 = df_water_quality3[df_water_quality3['Date_rank'] <= '30 days']
    
    
    #Rank the sites by the Latest EnteroCount, Average EnteroCount and Date Rank
    Result_df = df_water_quality4.sort_values(by=['EnteroCount','Mean_EnteroCount','Date_rank']).head(10)
    
    Result_df=Result_df[['Site', 'Date','EnteroCount','Mean_EnteroCount']]
    Result_df=Result_df.rename(columns={'Date':'Site_Last_Test_Date'})
    
    return Result_df

#date=pd.to_datetime('2010-09-07')



#The logic is that if we rank them by the latest EnteroCount we would pick the site with lowest
#single Enterococcus sample test result from the site in last 30 days. Then if we have multiple Sites
#with same low sample Enterococcus count we break the tie based on the site which has a lower average:
#of Enterococcus count since beginning of sample test. We further break that tie with the most recent
#sample tests

app = dash.Dash()

markdown_text = '''
## Site Recommendations app based on Water Quality

### Criteria for Site Recommendations

The recommendation logic applied here is to rank sites by the latest EnteroCount we would 
pick the site with lowest single Enterococcus sample test result from the site in last 30 days. 
Then if we have multiple Sites with same low sample Enterococcus count we break the tie based 
on the site which has a lower average of Enterococcus count since beginning of sample testing. 
We further break that tie with the most recent sample tests.
We recommend sites with the lowest EnteroCount as safe but also considering the Average EnteroCount.
This empowers the user with necessary information to make an informed decision while picking a safe site
'''


app.layout = html.Div(children=[
    dcc.Markdown(children=markdown_text),
    html.H4(children='Pick an intended Site visit Date'),
    dcc.DatePickerSingle(
        id='datepicker',
        min_date_allowed=start,
        max_date_allowed=end,
        initial_visible_month=pd.to_datetime("2010-1-1"),
        date=pd.to_datetime("2010-1-1")),
    html.H4(children='Top 10 Safest Recommended Sites'),
    html.Div(id='table-container')
])
    
@app.callback(dash.dependencies.Output('table-container', 'children'),
        [dash.dependencies.Input('datepicker', 'date')])
def update_table(date):
    date = pd.to_datetime(date)
    dff = Recommended_Sites(date) 
    return generate_table(dff)

if __name__ == '__main__':
    app.run_server()


