import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import datetime

headers = {"User-Agent": f"{UserAgent().random}"}
date = "-".join(reversed(str(datetime.datetime.now().date()).split("-")))

def Score(sport="football", date=date):
    url = f"https://www.sport-express.ru/live/{sport}/{date}"
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    data = soup.find('div', class_='se-matchcenter-sports-list') \
        .find_all("div", class_="se-matchcenter-sports-list__competition")

    league_information = {}
    league_information_live = {}
    status_live = {'перерыв', '1-й тайм', '2-й тайм', '1-й период', '2-й период', '3-й период', 'овертайм',
                   '1-я четверть', '2-я четверть', '3-я четверть', '4-я четверть', '1-й перерыв', '2-й перерыв',
                   '3-й перерыв'}

    for i in data:
        league = i.find("div", class_="se-competition-titled-block__title").text.strip()
        matches_fin = i.find_all("div",
                                 class_="se-matchcenter-matches__match se-matchcenter-matches__match--status-fin")
        matches_fin_2 = i.find_all("a",
                                   class_="se-matchcenter-matches__match se-matchcenter-matches__match--status-fin")
        matches_not_started = i.find_all("a",
                                         class_="se-matchcenter-matches__match se-matchcenter-matches__match--status-not-started")
        matches_delayed = i.find_all("div",
                                     class_="se-matchcenter-matches__match se-matchcenter-matches__match--status-not-started")
        league_information[league] = ''

        for m in [matches_fin, matches_fin_2, matches_not_started, matches_delayed]:
            try:
                for j in m:
                    time = j.find("div", class_="se-matchcenter-matches__match-date").text.strip()
                    status = j.find("div", class_="se-matchcenter-matches__match-status").text.strip()
                    team1 = j.find("div",
                                   class_="se-matchcenter-matches__match-team se-matchcenter-matches__match-team--1") \
                        .find("div", class_="se-matchcenter-matches__match-team__name").text.strip()
                    team2 = j.find("div",
                                   class_="se-matchcenter-matches__match-team se-matchcenter-matches__match-team--2") \
                        .find("div", class_="se-matchcenter-matches__match-team__name").text.strip()
                    score = j.find("div", class_="se-matchcenter-matches__match-score").text
                    score = " ".join(score.split())

                    league_information[league] = league_information.get(league, '') + \
                                                 f"{time} | {status}\n{team1}   {score}   {team2}\n"

                    if status in status_live:
                        league_information_live[league] = league_information.get(league, '') + \
                                                          f"{time} | {status}\n{team1}   {score}   {team2}\n"

            except:
                continue

    return (league_information, league_information_live)
