import os, json
from datetime import datetime, timedelta
from eod import EodHistoricalData

#updater thru Github actions
class UPDATE_DATA:
    """
    Periodically updates the data through github actions.
    """
    def __init__(self) -> None:
        pass

    def get_historical_prices(self,ticker_symbol, from_date, to_date) -> list:
        client = EodHistoricalData(os.environ["API_KEY"])
        resp = client.get_prices_eod(f'{ticker_symbol.upper()}.PSE', period='a', order='a', from_=from_date, to = to_date )
        return resp
    
    def update_data(self):
        a = open(os.path.join("data.json"),"r")
        load_json = json.load(a)
        a.close()
        updated_json = {}
        dates = []
        for data in load_json.values():
            try:
                #take not that by default, the data is ascending
                if data[-1]['date'] not in dates:
                    dates.append(datetime.strptime((data[-1]['date']), "%Y-%m-%d"))
            except IndexError:
                # "Stock is halted,terminated, or inactive."
                pass

        from_when=max(dates) + timedelta(days=1)
        to_when=datetime.now().date()

        ####

        for data in load_json.items():
            update = self.get_historical_prices(data[0].strip(),from_date=from_when,to_date=to_when)
            updated_json[data[0]] = data[1] + update

        update_data = open(os.path.join("temp","data.json"),"w")
        json.dump(updated_json,update_data,indent=2)
            
        ####

        logger = open(os.path.join("temp","logger.txt"),"a")
        logger.write(f"Updated --- {datetime.now()}\n")
        logger.close()



if __name__ == "__main__":
    a = UPDATE_DATA()
    a.update_data()
