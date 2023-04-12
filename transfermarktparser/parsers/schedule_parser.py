from bs4 import BeautifulSoup, Tag

from transfermarktparser.data.match import Match
from transfermarktparser.utils.text_handler import TextHandler


class ScheduleParser:
    def parse(self, page: str) -> list[Match]:
        soup = BeautifulSoup(page, "lxml")
        if not self._is_valid_season(soup):
            print("Season isn't valid.")
            return []

        return self._parse_games(soup)

    def _parse_league_info(self, soup: BeautifulSoup) -> tuple[str | None, str | None, int | None,
                                                               int | None, str | None]:
        league = soup.find("h1", class_="data-header__headline-wrapper "
                                        "data-header__headline-wrapper--oswald").text.strip()
        country = soup.find("span", class_="data-header__club").text.strip()
        tier = soup.find("span", class_="data-header__label").find("span", class_="data-header__content").text.strip()
        level = self._get_league_level(tier)
        season = int(soup.find("option", {"selected": "selected"})['value'])
        league_id = soup.find("li", {"id": "news"}).find("a")['href'].split("/")[-1].strip()

        return league, country, level, season, league_id

    @staticmethod
    def _get_league_level(tier: str) -> int | None:
        match tier.lower():
            case "first tier":
                return 1
            case "second tier":
                return 2
            case "third tier":
                return 3
            case "fourth tier":
                return 4
            case "fifth tier":
                return 5
            case _:
                print("League level is unknown")
                return None

    def _parse_games(self, soup: BeautifulSoup) -> list[Match]:
        games = []
        league, country, level, season, league_id = self._parse_league_info(soup)
        matchdays = soup("div", class_="row")[1].find_all("div", recursive=False)[1:]
        matches = [match for matchday in matchdays for match in matchday.find("tbody").find_all("tr", class_="")]
        previous_date, previous_time = None, None
        for match in matches:
            game = self._parse_game(match)
            previous_date = game["date"] if game["date"] else previous_date
            previous_time = game["time"] if game["time"] else previous_time

            games.append(Match(
                league=league,
                country=country,
                level=level,
                season=season,
                league_id=league_id,
                date=previous_date,
                time=previous_time,
                tour=game["tour"],
                home_team=game["home_team"],
                away_team=game["away_team"],
                home_score=game["home_score"],
                away_score=game["away_score"],
                home_id=game["home_id"],
                away_id=game["away_id"],
                match_id=game["summary_id"],
            ))
        return games

    @staticmethod
    def _parse_game(game_block: Tag) -> dict:
        tour = int(game_block.parent.parent.parent.find("div", class_="content-box-headline").text.split(".")[0])

        date = game_block("td")[0].text.strip()
        if len(date) > 1 and not date.lower() == "unknown":
            date = date.split()[1].strip()
            date = TextHandler.parse_date(date)
        else:
            date = None

        time = game_block("td")[1].text
        if len(time) > 1:
            time = time.strip()
            time = TextHandler.parse_time(time)
        else:
            time = None

        home_team = game_block("td")[2].find("a")["title"].strip()
        if not (idx := home_team.find("(")) == -1:
            home_team = home_team[:idx].strip()
        home_id = int(game_block("td")[2].find("a")["href"].split("/")[-3])
        away_team = game_block("td")[6].find("a")["title"].strip()
        if not (idx := away_team.find("(")) == -1:
            away_team = away_team[:idx].strip()
        away_id = int(game_block("td")[6].find("a")["href"].split("/")[-3])
        home_score, away_score = game_block("td")[4].find("a").text.strip().split(":")
        home_score = int(home_score) if home_score != "-" else None
        away_score = int(away_score) if away_score != "-" else None
        summary_id = int(game_block("td")[4].find("a")["href"].split("/")[-1])

        return {"tour": tour,
                "date": date,
                "time": time,
                "home_team": home_team,
                "away_team": away_team,
                "home_score": home_score,
                "away_score": away_score,
                "home_id": home_id,
                "away_id": away_id,
                "summary_id": summary_id, }

    @staticmethod
    def _is_valid_season(soup: BeautifulSoup) -> bool:
        if soup.find("option", {"selected": "selected"}):
            return True
        return False
