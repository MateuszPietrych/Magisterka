from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd










# Load the Excel file
excel_path = 'witcher_info.xlsx'  # Change this to your actual file path
xls = pd.ExcelFile(excel_path)

# List all sheet names
print(xls.sheet_names)

# Load a specific sheet (e.g., 'Gounter O'Dim')
df = pd.read_excel(xls, sheet_name="Ghoul")

# Display the first few rows
print(df.head())

# Access specific columns (e.g., 'Story', 'Scene')
selected_columns = df[['Story', 'Scene', 'Participants', 'Dialogue Game', 'Dialogue LLM']].copy()
print(selected_columns)

selected_columns.columns = ['Story', 'Scene', 'Participants', 'Dialogue Game', 'Dialogue LLM']

# Define the texts
Story = selected_columns['Story'].get(0)
Scene = selected_columns['Scene'].get(0)
Dialogue_Game = selected_columns['Dialogue Game'].get(0)
Dialogue_LLM = selected_columns['Dialogue LLM'].get(0)
# Shared participants

participants = selected_columns['Participants']
Participants_Text = ",\n".join(str(p) for p in selected_columns['Participants'])
print(f"Participants: {Participants_Text}")

# All texts to be vectorized
texts = [Story, Scene, Dialogue_Game, Dialogue_LLM, Participants_Text]

print("-----------------------------------------------------------------------------------------------------------------")
print(f"Story: {Story}\n")
print(f"Scene: {Scene}\n")
print(f"Dialogue_Game: {Dialogue_Game}\n")
print(f"Dialogue_LLM: {Dialogue_LLM}\n")
print(f"Participants: {Participants_Text}\n")
print("-----------------------------------------------------------------------------------------------------------------")















# TF-IDF vectorization
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(texts)

# Indices
i_story = 0
i_scene = 1
i_game = 2
i_llm = 3
i_participants = 4

# Cosine similarity matrix
similarity_matrix = cosine_similarity(tfidf_matrix)

# Cosine similarities
print("Cosine Similarity Results:\n")

print(f"Story           ↔ Dialogue_Game : {similarity_matrix[i_story][i_game]:.4f}")
print(f"Story           ↔ Dialogue_LLM  : {similarity_matrix[i_story][i_llm]:.4f}")
print(f"Scene           ↔ Dialogue_Game : {similarity_matrix[i_scene][i_game]:.4f}")
print(f"Scene           ↔ Dialogue_LLM  : {similarity_matrix[i_scene][i_llm]:.4f}")
print(f"Dialogue_Game   ↔ Dialogue_LLM  : {similarity_matrix[i_game][i_llm]:.4f}")
print(f"Participants    ↔ Dialogue_Game : {similarity_matrix[i_participants][i_game]:.4f}")
print(f"Participants    ↔ Dialogue_LLM  : {similarity_matrix[i_participants][i_llm]:.4f}\n")

# Summary
print("Summary of Cosine Similarities:\n")
print(f"Story: G-{similarity_matrix[i_story][i_game]:.4f} LLM-{similarity_matrix[i_story][i_llm]:.4f}")
print(f"Scene: G-{similarity_matrix[i_scene][i_game]:.4f} LLM-{similarity_matrix[i_scene][i_llm]:.4f}")
print(f"Participants: G-{similarity_matrix[i_participants][i_game]:.4f} LLM-{similarity_matrix[i_participants][i_llm]:.4f}")