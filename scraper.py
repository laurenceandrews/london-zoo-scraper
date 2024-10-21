import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.londonzoo.org/whats-here/animals?page="

def get_animal_links(page_num):
    """Fetch animal links from a single page."""
    response = requests.get(BASE_URL + str(page_num))
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links to individual animal pages
    animal_cards = soup.find_all('div', class_='views-row')
    animal_links = ["https://www.londonzoo.org" + card.find('a')['href'] for card in animal_cards]
    return animal_links

def get_animal_info(url):
    """Fetch and parse animal details from its individual page."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: Fetch the animal name and description
    name = soup.find('h1', class_='animal-name').text.strip()
    description = soup.find('div', class_='animal-content').text.strip()

    return {"name": name, "description": description}

def scrape_all_animals():
    """Main function to scrape all animal pages from all pagination."""
    all_animals = []
    page_num = 1
    while True:
        print(f"Scraping page {page_num}...")
        animal_links = get_animal_links(page_num)

        # Stop the loop if no more animals are found
        if not animal_links:
            break

        # Loop through each animal link and scrape info
        for link in animal_links:
            print(f"Scraping animal: {link}")
            animal_info = get_animal_info(link)
            all_animals.append(animal_info)

        page_num += 1

    return all_animals

if __name__ == "__main__":
    animals = scrape_all_animals()

    # Save the data to a CSV file for further use (e.g., Quizlet flashcards)
    df = pd.DataFrame(animals)
    df.to_csv('london_zoo_animals.csv', index=False)
    print("Scraping complete. Data saved to london_zoo_animals.csv")
