from bs4 import BeautifulSoup

from transfermarktparser.data.statistics import Statistics


class StatisticsParser:
    def parse(self, page: str) -> Statistics | None:
        soup = BeautifulSoup(page, "lxml")
        if not self._check_valid_page(soup):
            # print("There isn't statistics of a match")
            return

        statistics = self._parse_statistics(soup)
        return statistics

    @staticmethod
    def _parse_statistics(soup: BeautifulSoup) -> Statistics:
        match_id = int(soup.find("meta", {"property": "og:url"})["content"].split("/")[-1].strip())
        stat_blocks = soup("div", class_="sb-statistik")
        home_total_shots = int(stat_blocks[0].find_all("div", class_="sb-statistik-zahl")[0].text.strip())
        away_total_shots = int(stat_blocks[0].find_all("div", class_="sb-statistik-zahl")[1].text.strip())
        home_shots_off_target = int(stat_blocks[1].find_all("div", class_="sb-statistik-zahl")[0].text.strip())
        away_shots_off_target = int(stat_blocks[1].find_all("div", class_="sb-statistik-zahl")[1].text.strip())
        home_shots_saved = int(stat_blocks[2].find_all("div", class_="sb-statistik-zahl")[0].text.strip())
        away_shots_saved = int(stat_blocks[2].find_all("div", class_="sb-statistik-zahl")[1].text.strip())
        home_corners = int(stat_blocks[3].find_all("div", class_="sb-statistik-zahl")[0].text.strip())
        away_corners = int(stat_blocks[3].find_all("div", class_="sb-statistik-zahl")[1].text.strip())
        home_free_kicks = int(stat_blocks[4].find_all("div", class_="sb-statistik-zahl")[0].text.strip())
        away_free_kicks = int(stat_blocks[4].find_all("div", class_="sb-statistik-zahl")[1].text.strip())
        home_fouls = int(stat_blocks[5].find_all("div", class_="sb-statistik-zahl")[0].text.strip())
        away_fouls = int(stat_blocks[5].find_all("div", class_="sb-statistik-zahl")[1].text.strip())
        home_offsides = int(stat_blocks[6].find_all("div", class_="sb-statistik-zahl")[0].text.strip())
        away_offsides = int(stat_blocks[6].find_all("div", class_="sb-statistik-zahl")[1].text.strip())


        return Statistics(
            match_id=match_id,
            home_total_shots=home_total_shots,
            away_total_shots=away_total_shots,
            home_shots_off_target=home_shots_off_target,
            away_shots_off_target=away_shots_off_target,
            home_shots_saved=home_shots_saved,
            away_shots_saved=away_shots_saved,
            home_corners=home_corners,
            away_corners=away_corners,
            home_free_kicks=home_free_kicks,
            away_free_kicks=away_free_kicks,
            home_fouls=home_fouls,
            away_fouls=away_fouls,
            home_offsides=home_offsides,
            away_offsides=away_offsides,
        )

    @staticmethod
    def _check_valid_page(soup: BeautifulSoup) -> bool:
        main_block = soup("div", class_="sb-statistik")
        if main_block:
            return True
        return False
