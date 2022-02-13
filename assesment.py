import pandas as pd
import requests
import json
from datetime import date
from matplotlib import pyplot as plt

def convert_to_date(timestamp):
  return date.fromtimestamp(timestamp)

def ScaleIt(value):
  return float(value)


def main():
    for symbol in ['WMATIC','USDC']:
        # THE Graphql querry for the website to be able to fetch data
        query = """query {
        tokens(first :1000, where: { symbol: """+'"'+symbol+'"'+""" }) {
            id
            tokenDayData(first :1000,orderBy: date, orderDirection: asc){
            date
            token{
                name
            }
            volume
            volumeUSD
            feesUSD
            priceUSD
            untrackedVolumeUSD
            totalValueLocked
            totalValueLockedUSD
            }
            }
        }"""
#       Now passing the querry in through the post method to be able to fetch the data
        url = 'https://api.thegraph.com/subgraphs/name/muranox/uniswap-v3-matic'
        r = requests.post(url, json={'query': query})
        json_data = json.loads(r.text)
        # I have implemented try and except as sometime even if everything is correct the api of thegraph aint working properly
        try:
            data = json_data['data']['tokens']
            df_data = data[0]['tokenDayData']
            # converted to the dataframe
            df = pd.DataFrame(df_data)
            # as the date was in timestamp format we were required to change it
            df['date']  = df['date'].apply(convert_to_date)
            # volume was in string format so we need to change it to int
            df['volume'] = df['volume'].apply(ScaleIt)
            
            # we were supposed to calculate multiple metrices graphql is giving only two data correctly an in all the other it is showing 0
            # so I just made it for volume
            indicator = 'volume'
            
            # there was no instruction regarding the view format of the resultant charts so I just used matplotlib for plotting our data
            plt.plot(df['date'],df[f'{indicator}'])
            plt.title(f"{indicator} AGAINST Date For {symbol}")
            plt.xlabel('Date')
            plt.ylabel('Volume')
            plt.tight_layout()
            plt.show()
            print("Now getting the data for next symbol")

        except:
            print(f"didn't got the data for the symbool -> {symbol}")
            
if __name__ == "__main__":
    main()