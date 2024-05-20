import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_all_players(base_url, players_list_url):
    players = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(players_list_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve page with status code {response.status_code}")
        return players

    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '/player/_/id/' in href:
            player_id = href.split('/')[-1]
            player_name = link.text.strip()
            player_url = f"{base_url}{href}"
            players.append({'name': player_name, 'id': player_id, 'url': player_url})
    
    return players

def save_to_csv(players, filename='nhl_players.csv'):
    df = pd.DataFrame(players)
    df.to_csv(filename, index=False)
    print(f"Data has been successfully saved to {filename}")

def main():
    base_url = 'https://www.espn.com'
    players_list_url = 'https://www.espn.com/nhl/team/roster/_/name/bos/boston-bruins'
    
    players = get_all_players(base_url, players_list_url)
    if players:
        save_to_csv(players)

if __name__ == "__main__":
    main()
