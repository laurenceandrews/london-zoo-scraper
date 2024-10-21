import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.londonzoo.org"
ANIMAL_LIST_URL = f"{BASE_URL}/whats-here/animals"

def get_animal_links(page_num):
    """Fetch animal links from a single page."""
    if page_num == 1:
        url = ANIMAL_LIST_URL
    else:
        url = f"{ANIMAL_LIST_URL}?page={page_num}"
    
    print(f"Fetching overview page: {url}")
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_num}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the animal listing section
    animal_list = soup.find('ul', class_='animal-listing__card-list')
    
    if not animal_list:
        print(f"No animal cards found on page {page_num}")
        return []
    
    animal_links = []
    for item in animal_list.find_all('li', class_='listing__StyledCardWrapper-sc-z2e3hb-3'):
        # Get the link from <a> tag inside <li>
        link_tag = item.find('a', href=True)
        if link_tag:
            link = link_tag['href']
            # Check if the URL is absolute or relative
            if link.startswith("/"):
                link = BASE_URL + link  # Prepend BASE_URL if the link is relative
            animal_links.append(link)
            print(f"Found animal link: {link}")
    
    return animal_links

def get_animal_info(url):
    """Fetch and parse animal details from its individual page."""
    print(f"Fetching animal page: {url}")
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve animal page: {url}")
        return {}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        # Parse animal name and scientific name
        name = soup.find('h2').text.strip() if soup.find('h2') else "Unknown"
        scientific_name_tag = soup.find('em')
        scientific_name = scientific_name_tag.text.strip() if scientific_name_tag else "Unknown"

        # Description of the animal (first paragraph)
        description_tag = soup.find('p')
        description = description_tag.get_text(separator=' ', strip=True) if description_tag else "No description available."

        # Additional details extracted from the "tile-block" sections
        extra_info = {}
        for tile in soup.find_all('div', class_='tile-block'):
            label = tile.find('div', class_='tile-block--label').text.strip() if tile.find('div', class_='tile-block--label') else None
            value = tile.find('div', class_='tile-block--value').text.strip() if tile.find('div', class_='tile-block--value') else None
            
            if label and value:
                extra_info[label] = value

        return {
            "name": name,
            "scientific_name": scientific_name,
            "description": description,
            "url": url,
            "area_of_zoo": extra_info.get('Area of zoo', 'Unknown'),
            "enclosure_status": extra_info.get('Enclosure status', 'Unknown'),
            "iucn_status": extra_info.get('IUCN status', 'Unknown'),
            "order": extra_info.get('Order', 'Unknown'),
            "family": extra_info.get('Family', 'Unknown'),
            "region": extra_info.get('Region', 'Unknown'),
            "habitat": extra_info.get('Habitat', 'Unknown')
        }
    except AttributeError as e:
        print(f"Error parsing {url}: {e}")
        return {}

def scrape_all_animals():
    """Main function to scrape all animal pages from all pagination."""
    all_animals = []
    page_num = 1
    while True:
        print(f"\nScraping overview page {page_num}...")
        animal_links = get_animal_links(page_num)
        
        if not animal_links:
            print("No more animals found. Ending scraping.")
            break
        
        for link in animal_links:
            animal_info = get_animal_info(link)
            if animal_info:
                all_animals.append(animal_info)
                print(f"Added {animal_info['name']}")
            else:
                print(f"Failed to add animal from {link}")
            
            time.sleep(1)  # Be polite and avoid overwhelming the server
        
        page_num += 1
    
    return all_animals

if __name__ == "__main__":
    animals = scrape_all_animals()
    
    if animals:
        # Define the columns for the CSV output, including the new details
        df = pd.DataFrame(animals, columns=[
            'name', 'scientific_name', 'description', 'url', 
            'area_of_zoo', 'enclosure_status', 'iucn_status', 
            'order', 'family', 'region', 'habitat'
        ])
        
        # Save to CSV
        df.to_csv('london_zoo_animals.csv', index=False)
        print(f"\nScraping complete. {len(animals)} animals saved to london_zoo_animals.csv")
    else:
        print("No animal data scraped.")
