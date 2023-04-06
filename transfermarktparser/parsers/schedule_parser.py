import asyncio
from datetime import datetime

from bs4 import BeautifulSoup, Tag

from transfermarktparser.data.match import Match
from transfermarktparser.utils.text_handler import TextHandler


class ScheduleParser:
    def parse_matches(self, page: str, searched_matches: list[dict] = None) -> list[Match]:
        soup = BeautifulSoup(page, "lxml")
        if not self._is_valid_season(soup):
            print("Season isn't valid.")
            return []
        games = self._parse_games(soup, searched_matches)

        return games

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

    def _parse_games(self, soup: BeautifulSoup, searched_matches: list[dict] | None) -> list[Match]:
        games = []
        league, country, level, season, league_id = self._parse_league_info(soup)
        matchday_blocks = soup("div", class_="row")[1].find_all("div", recursive=False)[1:]
        for matchday_block in matchday_blocks:
            tour = int(matchday_block.find("div", class_="content-box-headline").text.split(".")[0])
            game_blocks = matchday_block.find("tbody").find_all("tr", class_="")

            previous_time = None
            previous_date = None
            for game_block in game_blocks:
                game = self._parse_game(game_block, previous_date, previous_time)

                if searched_matches is not None:
                    for searched_match in searched_matches:
                        if searched_match["home_team"] == game["home_team"] and \
                                searched_match["away_team"] == game["away_team"]:
                            searched_matches.remove(searched_match)
                            break
                    else:
                        continue

                previous_time, previous_date = game["time"], game["date"]
                games.append(Match(
                    league=league,
                    country=country,
                    level=level,
                    season=season,
                    league_id=league_id,
                    date=game["date"],
                    time=game["time"],
                    tour=tour,
                    home_team=game["home_team"],
                    away_team=game["away_team"],
                    home_score=game["home_score"],
                    away_score=game["away_score"],
                    home_id=game["home_id"],
                    away_id=game["away_id"],
                    summary_id=game["summary_id"],
                ))
        return games

    @staticmethod
    def _parse_game(game_block: Tag, previous_date: datetime.date, previous_time: datetime.time) -> dict:
        date = game_block("td")[0].text.strip()
        if len(date) > 1:
            date = date.split()[1].strip()
            date = TextHandler.parse_date(date)
        else:
            date = previous_date

        time = game_block("td")[1].text
        if len(time) > 1:
            time = time.strip()
            time = TextHandler.parse_time(time)
        else:
            time = previous_time

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

        return {"date": date,
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
