# 🦁 London Zoo Scraper

## 📄 Overview
The London Zoo Scraper is a Python-based project designed to scrape animal data from the London Zoo website, compiling essential details into a structured CSV file. This information is then further converted into Quizlet-compatible flashcard format for easy import, making it a helpful tool for studying animal facts, learning scientific names, and understanding species conservation statuses.

## 🛠️ Technologies Used
- **Web Scraping**: Python, Requests, BeautifulSoup
- **Data Processing**: Pandas
- **Data Conversion**: CSV, custom Quizlet formatting

## 📂 Project Structure
- `scraper.py`: Main script for scraping animal data from the London Zoo website and saving it as a CSV file.
- `converter.py`: Utility to convert the scraped animal data from CSV format to Quizlet-compatible flashcards.
- `london_zoo_animals.csv`: Output file containing detailed animal data in CSV format.
- `quizlet_format.txt`: Converted flashcard data, ready for Quizlet import.
- `requirements.txt`: Dependencies for running the project.
- `venv/`: Virtual environment for isolated dependency management.

## ⭐ Features
- **Comprehensive Animal Scraping**: Gathers details on animals such as their scientific names, physical appearance, diet, habitat, IUCN status, and unique facts.
- **CSV Export**: Exports the scraped data in CSV format for easy data management.
- **Quizlet Flashcard Conversion**: Transforms animal data into a format suitable for Quizlet, enabling flashcard study for all recorded animals.
- **Modular Design**: The scraper and converter scripts are designed to function independently, allowing you to run only the necessary components.

## 📋 Data Collected
The scraper extracts various fields for each animal:
- **Name** and **Scientific Name**
- **Physical Appearance**
- **Diet** and **Threats**
- **IUCN Status** (conservation status)
- **Order**, **Family**, **Region**, and **Habitat**
- Up to 5 interesting **Facts** per animal

### 🔄 Conversion to Quizlet
The `converter.py` script processes the CSV data into a Quizlet-compatible format. Each animal’s data is converted into a flashcard format with the animal name followed by specific attributes, like scientific name, habitat, and facts.

## 🌱 Setup and Installation

### 📋 Requirements
- **Python 3.8+**: Required for running the scripts
- **Virtual Environment**: Recommended for dependency management

### 🚀 Getting Started
1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/london-zoo-scraper.git
    cd london-zoo-scraper
    ```

2. **Set up a virtual environment**:
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the scraper**:
    ```bash
    python scraper.py
    ```
   The scraped data will be saved in `london_zoo_animals.csv`.

6. **Convert to Quizlet flashcard format** (optional):
    ```bash
    python converter.py
    ```
   This will create `quizlet_format.txt`, ready for Quizlet import.

## 🧪 Testing
To ensure the scraper and converter scripts run smoothly, you can test them individually:
- **Scraper**: Run `python scraper.py` to test data scraping.
- **Converter**: Run `python converter.py` after scraping to ensure data converts correctly into flashcard format.

## 📝 Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests for new features, improvements, or bug fixes.

## 📜 License
This project is licensed under the MIT License – see the LICENSE file for details.
