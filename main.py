import os
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

teams_page = ["https://www.imsa.com/weathertech/teams/", "https://www.imsa.com/michelinpilotchallenge/teams/",
              "https://www.imsa.com/vpracingsportscarchallenge/teams/"]


def team_socials(team_site):
    if not len(team_site):
        link = " "
    else:
        for team in team_site:
            link = team.get_attribute("href")

    return link


def team_dump(team_names, team_twitters, team_facebooks, team_instagrams, team_sites):
    data = {'Team Name': team_names, 'Twitter': team_twitters, 'Facebook': team_facebooks, 'Instagram': team_instagrams,
            'Team Site': team_sites}
    df = pd.DataFrame(data, columns=['Team Name', 'Twitter', 'Facebook', 'Instagram', 'Team Site'])
    if os.path.exists('Teams.csv'):
        header = False
    else:
        header = True
    df.to_csv('Teams.csv', mode='a', index=False, header=header)

def scrapper():
    for teams in teams_page:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(teams)
        teams_count = 0

        teams_length = len(driver.find_elements(By.CLASS_NAME, "team-item"))

        team_names = []
        team_twitters = []
        team_facebooks = []
        team_instagrams = []
        team_sites = []

        while teams_count < teams_length:
            team = driver.find_elements(By.CLASS_NAME, "team-item")

            team[teams_count].click()

            team_name = driver.find_elements(By.TAG_NAME, "h2")
            team_twitter = driver.find_elements(By.XPATH, "//div[@class='team-social']/a[@class='social-link twitter']")
            team_facebook = driver.find_elements(By.XPATH, "//div[@class='team-social']/a[@class='social-link facebook']")
            team_instagram = driver.find_elements(By.XPATH, "//div[@class='team-social']/a[@class='social-link instagram']")
            team_site = driver.find_elements(By.XPATH, "//div[@class='team-social']/a[@class='social-link offical']")

            team_names.append(team_name[0].text)
            team_twitters.append(team_socials(team_twitter))
            team_facebooks.append(team_socials(team_facebook))
            team_instagrams.append(team_socials(team_instagram))
            team_sites.append(team_socials(team_site))

            time.sleep(3)
            driver.back()
            teams_count += 1

        team_dump(team_names, team_twitters, team_facebooks, team_instagrams, team_sites)
        driver.quit()


scrapper()

# References
# https://stackoverflow.com/questions/58717379/how-to-do-loop-with-click-in-selenium
# https://www.w3schools.com/xml/xpath_syntax.asp
# https://github.com/Logan-Manor/Data_Mining_Project/tree/master
