import csv

def format_flashcard(animal_data):
    """Generate flashcard format for an animal."""
    flashcards = []
    animal_name = animal_data['name']
    
    # Define the fields to include in the flashcards
    fields = ['scientific_name', 'appearance', 'diet', 'threats', 'iucn_status', 'order', 
              'family', 'region', 'habitat', 'Fact 1', 'Fact 2', 'Fact 3', 'Fact 4', 'Fact 5']
    
    for field in fields:
        if animal_data.get(field):
            field_value = animal_data[field].strip()  # Remove unnecessary whitespace
            if field_value:  # Only include non-empty values
                # Prepend the animal name to each field for clarity in Quizlet format
                flashcard = f"{animal_name} ({field.replace('_', ' ').capitalize()}): {field_value}"
                flashcards.append(flashcard)
    
    # Join all flashcards for a single animal with semicolons (;)
    # Ensure there is no trailing semicolon or colon at the end of the group
    return "; ".join(flashcards).rstrip(";") + ";"

def convert_csv_to_quizlet(input_file, output_file):
    """Convert the zoo CSV file to Quizlet flashcard format."""
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        all_flashcards = []
        
        for row in reader:
            # Get formatted flashcards for each animal and add to the list
            animal_flashcards = format_flashcard(row)
            all_flashcards.append(animal_flashcards)
        
        # Join all animals' flashcards with line breaks between each animal's group of cards
        quizlet_format = " \n".join(all_flashcards)
        
        # Write to the output file
        outfile.write(quizlet_format)
        print(f"Successfully converted {input_file} to {output_file} in Quizlet format!")

if __name__ == "__main__":
    input_csv = 'london_zoo_animals.csv'  # Input CSV file
    output_quizlet = 'quizlet_format.txt'  # Output file in Quizlet format
    convert_csv_to_quizlet(input_csv, output_quizlet)
