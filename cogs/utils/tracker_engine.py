# Import libraries
import urllib.parse
import requests
from bs4 import BeautifulSoup
from decouple import config


class PrivateProfileException(Exception):
    pass


class PlayerNotFoundException(Exception):
    pass


# Declare variables
API_KEY = config("TRN-Api-Key")
HEADERS = {"TRN-Api-Key": API_KEY}
PRIVATE_PROFILE_ERROR_MESSAGE = "If this is your account, you can view your stats by continuing with Riot Sign On below!"
PLAYER_NOT_FOUND_ERROR_MESSAGE = "Make sure you are not forgetting the # tag in the Riot ID, it's required."


# Gets user stat page soup from username
def get_soup(username):
    # Get tracker URL from username
    url = f"https://tracker.gg/valorant/profile/riot/{urllib.parse.quote(username)}/overview?playlist=competitive&season=all"

    # Get user tracker page and open it
    user_page = requests.get(url, headers=HEADERS)
    user_page_soup = BeautifulSoup(user_page.content, "html.parser")

    # Return the soup
    return user_page_soup


def find_error(soup):
    # Find the error message
    error_message = soup.find("p", class_="error-message")

    # Check if the error message exists
    if error_message is not None:
        # Check if error message is from private profile or player not found
        if error_message.text.strip() == PRIVATE_PROFILE_ERROR_MESSAGE:
            raise PrivateProfileException
        elif error_message.text.strip() == PLAYER_NOT_FOUND_ERROR_MESSAGE:
            raise PlayerNotFoundException
        else:
            raise Exception


def get_stats_from_username(username):
    # Get soup and find errors
    user_page_soup = get_soup(username)
    find_error(user_page_soup)

    # Get and return stats dictionary
    stats_dictionary = get_stats_from_soup(user_page_soup)
    return stats_dictionary


def get_images_from_username(username):
    # Get soup and find errors
    user_page_soup = get_soup(username)
    find_error(user_page_soup)

    # Get and return images dictionary
    images_dictionary = get_image_urls_from_soup(user_page_soup)
    return images_dictionary


def get_rank_from_username(username):
    # Get the username page soup and call find_error
    user_page_soup = get_soup(username)
    find_error(user_page_soup)

    # Find the rank and return it
    rank = user_page_soup.find("span", class_="valorant-highlighted-stat__value")
    return rank.text


def get_peak_rank_from_username(username):
    # Get the username page soup and call find_error
    user_page_soup = get_soup(username)
    find_error(user_page_soup)

    # Find peak rank information and return it
    peak_rank_dictionary = get_peak_rank_from_soup(user_page_soup)
    return peak_rank_dictionary


def get_peak_rank_images_from_username(username):
    # Get soup and find errors
    user_page_soup = get_soup(username)
    find_error(user_page_soup)

    # Get and return images dictionary
    images_dictionary = get_peak_rank_image_urls_from_soup(user_page_soup)
    return images_dictionary


def get_stats_from_soup(user_page_soup):
    # Declare stats dictionary
    stats_dictionary = {"Rank": "", "Damage/Round": "", "K/D Ratio": "", "HS%": "", "Win %": "", "Wins": "",
                        "Kills": "", "Headshots": "", "Deaths": "", "Assists": "", "Score/Round": "", "Kills/Round": "",
                        "Clutches": "", "Flawless": "", "Most Kills (Match)": ""}

    # Find stats and add them to stats dictionary
    # Find rank
    rank = user_page_soup.find("span", class_="valorant-highlighted-stat__value")
    stats_dictionary["Rank"] = rank.text

    # Find giant stats by looping through
    giant_stats_soup = user_page_soup.find("div", class_="giant-stats")
    for stat in giant_stats_soup.find_all("div", class_="numbers"):
        stat_name = stat.find("span", class_="name")
        stat_value = stat.find("span", class_="value")
        stats_dictionary[stat_name.text] = stat_value.text

    # Find main stats by looping through
    main_stats_soup = user_page_soup.find("div", class_="main")
    for stat in main_stats_soup.find_all("div", class_="numbers"):
        stat_name = stat.find("span", class_="name")
        stat_value = stat.find("span", class_="value")
        stats_dictionary[stat_name.text] = stat_value.text

    # Return stats dictionary
    return stats_dictionary


def get_image_urls_from_soup(user_page_soup):
    # Declare images dictionary
    images_dictionary = {"profile_image": "", "rank_image": ""}

    # Find profile image and rank image urls
    profile_image_url = user_page_soup.find("svg", class_="decagon-avatar").image.get("href")
    rank_image_url = user_page_soup.find("div", class_="valorant-highlighted-content__stats").img.get("src")

    # Add urls to the images dictionary and return it
    images_dictionary["profile_image"] = profile_image_url
    images_dictionary["rank_image"] = rank_image_url
    return images_dictionary


def get_peak_rank_from_soup(user_page_soup):
    # Declare peak rank dictionary
    peak_rank_dictionary = {"Peak Rank": "", "Act": ""}

    # Get peak_rank_soup
    peak_rank_soup = user_page_soup.find("div", class_="rating-content rating-content--secondary")

    # Get peak_rank info
    peak_rank = peak_rank_soup.find("div", class_="value")
    peak_rank_dictionary["Peak Rank"] = peak_rank.text.strip()

    # Get act info
    peak_rank_act = peak_rank_soup.find("div", class_="subtext")
    peak_rank_dictionary["Act"] = peak_rank_act.text

    return peak_rank_dictionary


def get_peak_rank_image_urls_from_soup(user_page_soup):
    # Declare images dictionary
    images_dictionary = {"profile_image": "", "peak_rank_image": ""}

    # Get peak_rank soup
    peak_rank_soup = user_page_soup.find("div", class_="rating-content rating-content--secondary")

    # Find profile image and rank image urls
    profile_image_url = user_page_soup.find("svg", class_="decagon-avatar").image.get("href")
    peak_rank_image_url = peak_rank_soup.find("div", class_="rating-entry__icon").img.get("src")

    # Add urls to the images dictionary and return it
    images_dictionary["profile_image"] = profile_image_url
    images_dictionary["peak_rank_image"] = peak_rank_image_url
    return images_dictionary
