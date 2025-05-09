from chromadb.config import Settings
import chromadb
import os
import re


def sanitize_filename(name):
    # Replace invalid characters with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def split_and_save(input_path, output_folder):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chroma_client = chromadb.PersistentClient(path=script_dir)
    # collection = chroma_client.create_collection(name="witcher")
    collection = chroma_client.get_or_create_collection(name="witcher")

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    ids: set = set()
    dict = {}

    with open(input_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split the content by the delimiter
    sections = content.split("--------------------------------------------------------------------------------")

    for idx, section in enumerate(sections):
        # Trim whitespace from each section
        cleaned_section = clean_section(section)
        
        # Skip empty sections
        if not cleaned_section:
            continue

        # TODO: Perform any desired operation on the cleaned_section here
        # For demonstration, let's just save the section as-is

        if should_have_file(cleaned_section):
            # Save each section as a separate file
            sectionId = get_id(cleaned_section)
            fileText = sectionId + "<;>"+ cleaned_section

            sectionId = sectionId.replace(" ", "_").replace(",", "_").replace(".", "_").replace(":", "_").replace("'", "_")
            sectionId = sanitize_filename(sectionId)
            output_file = os.path.join(output_folder, f'{sectionId}.txt')

            if sectionId in ids:
                fileText = "\n\n"+ cleaned_section
                dict[sectionId] += "\n\n" + fileText
            else:
                ids.add(sectionId)
                dict[sectionId] = cleaned_section
            
            if collection.get(sectionId):
                collection.delete(sectionId)

            try:
                with open(output_file, 'a', encoding='utf-8') as output:
                    output.write(fileText)

            except Exception as e:
                print(f"Error writing to file {output_file}: {e}")
                continue


    for sectionId in dict.keys():
        try:
            collection.add(
                documents=list(dict[sectionId]),
                ids=list(sectionId),
                )
        except Exception as e:
            print(f"Error adding to collection {sectionId}: {e}. Section: {dict[sectionId]}")
            continue    
        

        

def should_have_file(section: str) -> bool:
    if ("," in section or "." in section or "is" in section or "are" in section or "was" in section or "were" in section) and len(section) > MIN_LENGTH_OF_SECTION:
        return True
    return False

def clean_section(section: str) -> str:
    # Remove unwanted characters and whitespace
    splited_section = section.split("\n")
    cleaned_section_list = [line.strip() for line in splited_section if len(line) > MIN_LENGTH_OF_LINE_IN_SECTION]
    cleaned_section = "\n".join(cleaned_section_list)
    cleaned_section = cleaned_section.replace("\"", "“").replace("\'", "‘")
    return cleaned_section.strip()

def get_id(section):
    # Extract the ID from the section using regex
    dotIndex = section.find(".")
    commaIndex = section.find(",")
    isIndex = section.find(" is")
    areIndex = section.find(" are")
    wasIndex = section.find(" was")
    wereIndex = section.find(" were")
    bracketIndex = section.find("[")
    parenthesisIndex = section.find("(")
    enterIndex = section.find("\n")

    indexList  = [dotIndex, commaIndex, isIndex, areIndex, wasIndex, wereIndex,  bracketIndex, parenthesisIndex, enterIndex]
    indexList = [index for index in indexList if index != -1]

    if indexList:
        minIndex = min(indexList)
        return section[:minIndex].strip()
    return section.strip()



# Define the input file and output folder
input_path = 'cleaned_output.txt'
output_folder = 'split_files'
MIN_LENGTH_OF_SECTION = 30
MIN_LENGTH_OF_LINE_IN_SECTION = 22

# Call the function
split_and_save(input_path, output_folder)


# x = "--------------------------------------------------------------------------------\n" \
# "Buy: 10\n" \
# "adsd: 5\n" \
# "asd ad is fasd sdh ashd hasdj jjwjh \n" \
# "--------------------------------------------------------------------------------\n" \


# cleaned_x = clean_section(x)
# print(cleaned_x)