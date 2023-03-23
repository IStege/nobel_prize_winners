import requests
import pandas as pd
import logging


def get_data_from_api(url) -> dict:
    """
    _summary_

    Args:
        url (_type_): _description_

    Returns:
        dict: _description_
    """
    result = None
    try:
        response = requests.get(url)
        result = response.json()
        logging.info(f"")
    except:
        logging.exception()
        
    return result

def clean_winners_data(data_dict :dict) -> pd.DataFrame:
    """
    _summary_

    Args:
        data_dict (dict): _description_

    Returns:
        pd.DataFrame: _description_
    """
    
    columns = ['id', 'fullname', 'born', 'unique_price_years', 'unique_price_categories', 'gender', 'country_name']
    
    data_dict = data_dict.get('laureates')
    data_df = pd.DataFrame(data_dict)
    
    #handle fullname
    data_df.fillna({'firstname':"", 'surname':""}, inplace=True)
    data_df['fullname'] = data_df.apply(lambda row: row['firstname'] + " " + row['surname'], axis=1)
    
    #handle unique prizes
    def get_unique_values(row, key):
        values = [x.get(key) for x in row]
        return set(values)

    data_df['unique_price_years'] = data_df['prizes'].apply(lambda row: get_unique_values(row, key='year'))
    data_df['unique_price_categories'] = data_df['prizes'].apply(lambda row: get_unique_values(row, key='category'))
    
    countries_df = pd.DataFrame(countries.get('countries'))
    countries = countries_df.set_index('code').squeeze()
    countries_dict = countries.to_dict()
    
    data_df['country_name'] = data_df['bornCountryCode'].map(countries_dict)
    
    return data_df[columns]
    

def df_to_csv(df: pd.DataFrame):
    df.to_csv('csv_file.csv')

def main():
    url_winners = "https://api.nobelprize.org/v1/laureate.json"
    url_countries = "https://api.nobelprize.org/v1/country.json"
    
    data_dict_winners = get_data_from_api(url_winners)
    data_dict_countries = get_data_from_api(url_countries)
    
    clean_data_winners = clean_winners_data(data_dict_winners)
    df_to_csv(clean_data_winners)
    
    
if __name__ == '__main__':
    main()