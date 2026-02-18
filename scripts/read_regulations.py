import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import math

def write_json(in_dict, out_file):
    with open(out_file, "w") as json_file:
        json.dump(in_dict, json_file, indent=4)

def scrape_html_table(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        raise

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    return df

def main():
    url = "https://wvdnr.gov/hunting-seasons/"
    outfile = "../wv_grouse_regs.json"
    species = "Ruffed Grouse"

    regs_table = scrape_html_table(url)
    grouse = regs_table[regs_table['Species'].str.contains(species)].set_index('Species').T.to_dict()
    write_json(grouse, outfile)


if __name__ == "__main__":
    main()