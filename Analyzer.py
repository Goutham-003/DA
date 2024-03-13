import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import os
import re
import csv

nltk.download('punkt')
nltk.download('stopwords')

# Function to load stop words from multiple files
def load_stop_words(stop_words_folder):
    stop_words = set()
    for filename in os.listdir(stop_words_folder):
        with open(os.path.join(stop_words_folder, filename), 'r') as file:
            stop_words.update(word.strip() for word in file.readlines())
    return stop_words

# Function to load positive and negative words from dictionary folder
def load_dictionary(dictionary_folder):
    positive_words = set()
    negative_words = set()
    for filename in os.listdir(dictionary_folder):
        with open(os.path.join(dictionary_folder, filename), 'r') as file:
            words = [word.strip() for word in file.readlines()]
            if "positive" in filename:
                positive_words.update(words)
            elif "negative" in filename:
                negative_words.update(words)
    return positive_words, negative_words

# Function to clean text using stop words list
def clean_text(text, stop_words_folder):
    stop_words = load_stop_words(stop_words_folder)
    cleaned_text = [word.lower() for word in word_tokenize(text) if word.lower() not in stop_words and re.match(r'\b\w+\b', word)]
    return cleaned_text

# Function to calculate derived variables
def calculate_variables(text, positive_words, negative_words, stop_words_folder):
    cleaned_text = clean_text(text, stop_words_folder)
    positive_score = sum(1 for word in cleaned_text if word in positive_words)
    negative_score = sum(1 for word in cleaned_text if word in negative_words)
    polarity_score = (positive_score - negative_score) / (positive_score + negative_score + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(cleaned_text) + 0.000001)
    return positive_score, negative_score, polarity_score, subjectivity_score

# Function to analyze readability
def analyze_readability(text,stop_words_folder):
    words = clean_text(text,stop_words_folder)
    sentences = sent_tokenize(text)
    if len(sentences)>0:
        average_sentence_length = len(words) / len(sentences)
        average_words_per_sentence = len(words) / len(sentences)
    else:
        average_sentence_length = 0
        average_words_per_sentence = 0
    complex_words = [word for word in words if len(word) > 2]
    if len(words)>0:
        percentage_complex_words = len(complex_words) / len(words)
        syllable_count = sum(syllable_count_word(word) for word in words)/len(words)
    else:
        percentage_complex_words = 0
        syllable_count = 0
    fog_index = 0.4 * (average_sentence_length + percentage_complex_words)
    complex_word_count = len(complex_words)
    word_count = len(words)
    return average_words_per_sentence, complex_word_count, word_count, fog_index,average_sentence_length,percentage_complex_words,syllable_count

# Function to count personal pronouns
def count_personal_pronouns(text):
    personal_pronouns = ["I", "we", "my", "ours", "us"]
    personal_pronouns_count = sum(1 for word in clean_text(text,stop_words_folder) if word.lower() in personal_pronouns)
    return personal_pronouns_count

# Function to calculate average word length
def average_word_length(text):
    words = clean_text(text,stop_words_folder)
    total_characters = sum(len(word) for word in words)
    if len(words) > 0:
        average_length = total_characters / len(words)
    else:
        average_length = 0
    return average_length

# Function to count syllables in a word
def syllable_count_word(word):
    word = word.lower()
    if len(word) <= 3:
        return 1
    count = 0
    vowels = 'aeiouy'
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        count += 1
    return count

# Sample text for analysis
sample_text = "Sample text for analysis. It contains positive and negative words like happy, sad, good, bad, etc."

# Folder containing positive and negative keyword files
dictionary_folder = "./dictionary"
# Folder containing stop words files
stop_words_folder = "./stopwords"

output_csv_file = "analysis_results.csv"

# Load positive and negative keywords from dictionary folder
positive_words, negative_words = load_dictionary(dictionary_folder)

# Calculate derived variables
# positive_score, negative_score, polarity_score, subjectivity_score = calculate_variables(sample_text, positive_words, negative_words, stop_words_folder)
# print("Positive Score:", positive_score)
# print("Negative Score:", negative_score)
# print("Polarity Score:", polarity_score)
# print("Subjectivity Score:", subjectivity_score)

# Analyze readability
# average_words_per_sentence, complex_word_count, word_count, fog_index,average_sentence_length, percentage_of_complex_words, syllable_count = analyze_readability(sample_text,stop_words_folder)
# print("Average Sentence Length:",average_sentence_length)
# print("Percentage of Complex words:",percentage_of_complex_words)
# print("Fog Index:", fog_index)
# print("Average Number of Words Per Sentence:", average_words_per_sentence)
# print("Complex Word Count:", complex_word_count)
# print("Word Count:", word_count)
# print("Syllable Per Word:", syllable_count)
# Count personal pronouns
# personal_pronouns_count = count_personal_pronouns(sample_text)
# print("Personal Pronouns:", personal_pronouns_count)

# # Calculate average word length
# avg_word_length = average_word_length(sample_text)
# print("Average Word Length:", avg_word_length)

with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["Filename", "Positive Score", "Negative Score", "Polarity Score", "Subjectivity Score",
                  "Average Sentence Length", "Percentage of Complex Words", "Fog Index", "Average Number of Words Per Sentence",
                  "Complex Word Count", "Word Count", "Syllable Per Word", "Personal Pronouns", "Average Word Length"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through each text file in the articles folder
    for filename in os.listdir("articles"):
        if filename.endswith(".txt"):
            with open(os.path.join("articles", filename), 'r', encoding='utf-8') as file:
                text = file.read()

            # Calculate derived variables
            positive_score, negative_score, polarity_score, subjectivity_score = calculate_variables(text, positive_words, negative_words, stop_words_folder)
            average_words_per_sentence, complex_word_count, word_count, fog_index,average_sentence_length, percentage_of_complex_words, syllable_count = analyze_readability(text, stop_words_folder)
            personal_pronouns_count = count_personal_pronouns(text)
            avg_word_length = average_word_length(text)

            # Write the analysis results to the CSV file
            writer.writerow({
                "Filename": filename,
                "Positive Score": positive_score,
                "Negative Score": negative_score,
                "Polarity Score": polarity_score,
                "Subjectivity Score": subjectivity_score,
                "Average Sentence Length": average_sentence_length,
                "Percentage of Complex Words": percentage_of_complex_words,
                "Fog Index": fog_index,
                "Average Number of Words Per Sentence": average_words_per_sentence,
                "Complex Word Count": complex_word_count,
                "Word Count": word_count,
                "Syllable Per Word": syllable_count,
                "Personal Pronouns": personal_pronouns_count,
                "Average Word Length": avg_word_length
            })

print("Analysis results saved to:", output_csv_file)