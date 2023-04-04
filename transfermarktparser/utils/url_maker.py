class UrlMaker:
    _SCHEDULE_URL = "https://www.transfermarkt.com/x/gesamtspielplan/wettbewerb/{league}/saison_id/{year}"

    @staticmethod
    def get_schedule_url(league_id: str, year: int) -> str:
