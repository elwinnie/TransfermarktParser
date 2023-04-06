class UrlMaker:
    _SCHEDULE_URL = "https://www.transfermarkt.com/x/gesamtspielplan/wettbewerb/{league_id}/saison_id/{year}"

    @classmethod
    def get_schedule_urls(cls, league_ids: list[str] | str, years: list[int] | int) -> list[str]:
        if type(league_ids) is not list:
            league_ids = [league_ids]
        if type(years) is not list:
            years = [years]

        urls = []
        for league_id in league_ids:
            for year in years:
                url = cls._SCHEDULE_URL.format(league_id=league_id, year=year)
                urls.append(url)
        return urls
