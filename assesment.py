import requests
from datetime import datetime
import os
import pandas as pd

# Connects to CONAGUA API 
def get_weather_data():
    url = "https://conagua.gob.mx/webservices/?method=3"
    
    try:
        return requests.get(url).json()
    except Exception as e:
        print("Error fetching data from conagua API,", e,"\n")
        return False

def read_weather_data(data_path):
    df= pd.read_json(data_path)
    print(f"Using data from {data_path}\n")
    return df

def extract_data(df):
    new_data= df[df['nhor']>= max(df['nhor'])-1 ]
    new_data=new_data[['ides','idmun','temp','prec']]
    new_data=new_data.rename(columns={'ides':'id_state','idmun':'id_town','temp':'avg_temp','prec':'avg_prec'})
    new_data= new_data.groupby(['id_state','id_town']).mean().reset_index()
    return new_data

def get_latest_folder(main_folder):
    folders = os.listdir(main_folder)
    folder_dates = [datetime.strptime(folder, "%Y%m%d") for folder in folders if len(folder) == 8]

    if len(folder_dates) > 0:
        latest_folder = folders[folder_dates.index(max(folder_dates))]
        return latest_folder
    else:
        print(f"No folders found in the main folder.\n")



def read_existing_data(main_path, folder_name):
    existing_data_path = os.path.join(main_path, 'data_municipios', folder_name, 'data.csv')
    
    if not os.path.isfile(existing_data_path):
        raise ValueError(f'File not found: {existing_data_path}\n')
    
    existing_data = pd.read_csv(existing_data_path)
    existing_data = existing_data.rename(columns={'Cve_Ent': 'id_state', 'Cve_Mun': 'id_town'})
    return existing_data

def table_join(new_data,existing_data):
    updated_data= new_data.set_index(['id_state', 'id_town']).join(existing_data.set_index(['id_state', 'id_town']))
    updated_data=updated_data.reindex(columns=['Value','avg_temp','avg_prec'])
    print("Correctly joined data.csv with new_data\n")
    return updated_data

def save_currentfile(updated_data,main_path):
    actual_date = datetime.now().strftime("%Y%m%d-%H%M")
    file_name= f"{actual_date}.csv"
    output_folder= os.path.join(main_path, 'output')
    file_path= os.path.join(output_folder,file_name)
    updated_data.to_csv(file_path)
    file_path_current= os.path.join(output_folder,"current.csv")
    updated_data.to_csv(file_path_current)
    print(f"Correctly saved {file_name} and current.csv file to:{output_folder}\n")

def main():

    df= get_weather_data()
    if df == False:
        df= read_weather_data(data_path="C:\\Users\monte\Documents\Assesment\HourlyForecast_MX\HourlyForecast_MX")
    
    new_records= extract_data(df)
    path = "C:\\Users\monte\Documents\Assesment" # Replace with the full path to the main folder
    folder= os.path.join(path,'data_municipios')
    newest_folder= get_latest_folder(main_folder=folder)
    active_data= read_existing_data(main_path=path, folder_name=newest_folder)
    updated_table= table_join(new_data= new_records, existing_data=active_data)
    save_currentfile(updated_data= updated_table, main_path= path)


main()