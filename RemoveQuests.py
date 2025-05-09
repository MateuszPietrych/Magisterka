import re

def clean_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Removing all segments that start with "Type: " and end with "--------------------------------------------------------------------------------"
    cleaned_content = re.sub(r'Type: .*?--------------------------------------------------------------------------------', '', content, flags=re.DOTALL)

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

input_path = 'combined_output.txt'
output_path = 'cleaned2_output.txt'
clean_file(input_path, output_path)

print(f"Cleaned file saved as: {output_path}")


# then remove TV/Film and quests 
# remove "Do you really wish to know?" — Spoilers from the books and/or adaptations to follow!
#
# Remove:
#--------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------
#
#  regular expresion to ->  --------------------------------------------------------------------------------\n\s*".*
#