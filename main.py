from transfermarktparser.transfermarkt_parser import TransfermarktParser
from transfermarktparser.utils.data_writer import DataWriter

leagues = ["RU1", "GB1", "L1", "ES1", "IT1", "FR1"]
years = [year for year in range(2014, 2023)]
base_url = "https://www.transfermarkt.com/x/gesamtspielplan/wettbewerb/{league}/saison_id/{year}"
urls = [base_url.format(league=league, year=year) for league in leagues for year in years]

if __name__ == "__main__":
    result = TransfermarktParser.get_matches(leagues, years)
    writer = DataWriter()
    writer.to_csv(result, filename="schedule")
