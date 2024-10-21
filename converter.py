import csv

# Function to create the quizlet format string for each row
def format_for_quizlet(row):
    # The name of the animal is added as a prefix to each field's value
    name = row.get("name", "").strip()
    flashcards = []

    # Iterate over all columns other than 'url' and 'image_url'
    fields = [
        "scientific_name", "appearance", "diet", "threats", "area_of_zoo",
        "enclosure_status", "iucn_status", "order", "family", "region", "habitat",
        "Fact 1", "Fact 2", "Fact 3", "Fact 4", "Fact 5"
    ]

    for field in fields:
        value = row.get(field, "").strip()  # Get the value and strip any whitespace
        if value:  # Only include if the field is not empty
            flashcards.append(f"{name} {field.replace('_', ' ').title()},{value}")
    
    return ";".join(flashcards)  # Join the flashcards with a semicolon


# Function to read the CSV and write the quizlet format
def convert_to_quizlet(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        for row in reader:
            quizlet_format = format_for_quizlet(row)
            if quizlet_format:  # Ensure we don't write empty lines
                outfile.write(quizlet_format + "\n")


# Main execution
if __name__ == "__main__":
    input_csv = 'london_zoo_animals.csv'  # Input CSV file path
    output_txt = 'quizlet_format.txt'     # Output Quizlet file path
    convert_to_quizlet(input_csv, output_txt)
    print(f"Conversion complete. Output written to {output_txt}")
