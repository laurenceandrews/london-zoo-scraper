import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

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
    animal_list = soup.find('ul', class_='animal-listing__card-list')
    
    if not animal_list:
        print(f"No animal cards found on page {page_num}")
        return []
    
    animal_links = []
    for item in animal_list.find_all('li', class_='listing__StyledCardWrapper-sc-z2e3hb-3'):
        link_tag = item.find('a', href=True)
        if link_tag:
            # Correcting the URL concatenation
            link = link_tag['href']
            if not link.startswith("http"):
                link = BASE_URL + link
            animal_links.append(link)
            print(f"Found animal link: {link}")
        else:
            print("No link found in this card.")
    
    return animal_links

def extract_facts(text):
    """Split description into multiple facts."""
    facts = text.split('. ')
    facts = [fact.strip() + '.' for fact in facts if fact]  # Ensure each fact ends with a period
    return facts

def get_largest_image_url(srcset):
    """Extract the largest image URL from a srcset attribute."""
    image_candidates = [img.strip() for img in srcset.split(',')]
    if image_candidates:
        return image_candidates[-1].split()[0]  # Return the URL of the largest image
    return "No image available"

def get_animal_info(url):
    """Fetch and parse animal details from its individual page."""
    print(f"Fetching animal page: {url}")
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve animal page: {url}")
        return {}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        # Animal name
        name = soup.find('h1').text.strip()

        # Scientific name - Found in a <span> tag within the hero section
        scientific_name_tag = soup.find('div', class_='hero__inner-wrapper').find('span')
        scientific_name = scientific_name_tag.text.strip() if scientific_name_tag else "N/A"

        # Area of zoo
        area_tag = soup.find('div', class_='tile-block--label', string='Area of zoo')
        area_of_zoo = area_tag.find_next('div', class_='tile-block--value').text.strip() if area_tag else "Unknown"

        # Enclosure status
        enclosure_status_tag = soup.find('div', class_='tile-block--label', string='Enclosure status')
        enclosure_status = enclosure_status_tag.find_next('div', class_='tile-block--value').text.strip() if enclosure_status_tag else "Unknown"

        # IUCN status
        iucn_status_tag = soup.find('div', class_='tile-block--label', string='IUCN status')
        iucn_status = iucn_status_tag.find_next('div', class_='tile-block--value').text.strip() if iucn_status_tag else "Unknown"

        # Order and Family
        order_tag = soup.find('div', class_='tile-block--label', string='Order')
        order = order_tag.find_next('div', class_='tile-block--value').text.strip() if order_tag else "Unknown"

        family_tag = soup.find('div', class_='tile-block--label', string='Family')
        family = family_tag.find_next('div', class_='tile-block--value').text.strip() if family_tag else "Unknown"

        # Region
        region_tag = soup.find('div', class_='tile-block--label', string='Region')
        region = region_tag.find_next('div', class_='tile-block--value').text.strip() if region_tag else "Unknown"

        # Habitat
        habitat_tag = soup.find('div', class_='tile-block--label', string='Habitat')
        habitat = habitat_tag.find_next('div', class_='tile-block--value').text.strip() if habitat_tag else "Unknown"

        # Image URL - Extract from 'srcset' in the hero image section
        image_tag = soup.find('div', class_='hero__image').find('img')
        image_url = get_largest_image_url(image_tag['srcset']) if image_tag and 'srcset' in image_tag.attrs else "No image available"

        # Extract section-based data
        appearance, diet, threats, general_facts = "", "", "", []
        fact_tags = soup.find_all('h3')  # Headers where facts, appearance, and diet might be

        for tag in fact_tags:
            header = tag.text.strip()
            content = tag.find_next('p').text.strip()

            if re.search(r"(What do|What does).*look like", header, re.IGNORECASE):
                appearance = content
            elif re.search(r"(What do|What does).*eat", header, re.IGNORECASE):
                diet = content
            elif re.search(r"threats", header, re.IGNORECASE):
                threats = content
            else:
                # General fact section
                general_facts += extract_facts(content)

        # Ensure we have up to Fact 1 to Fact 5
        fact_fields = {}
        for i, fact in enumerate(general_facts[:5], start=1):
            fact_fields[f'Fact {i}'] = fact

        return {
            "name": name,
            "scientific_name": scientific_name,
            "appearance": appearance,
            "diet": diet,
            "threats": threats,
            "url": url,
            "image_url": image_url,
            "area_of_zoo": area_of_zoo,
            "enclosure_status": enclosure_status,
            "iucn_status": iucn_status,
            "order": order,
            "family": family,
            "region": region,
            "habitat": habitat,
            **fact_fields  # Add Fact 1, Fact 2, etc.
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
        df = pd.DataFrame(animals)
        df.to_csv('london_zoo_animals.csv', index=False)
        print(f"\nScraping complete. {len(animals)} animals saved to london_zoo_animals.csv")
    else:
        print("No animal data scraped.")
