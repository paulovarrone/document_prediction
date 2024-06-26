import pickle  # Importing the pickle module to save and load Python objects to files.
import fitz  # PyMuPDF
from nltk.corpus import stopwords  # Importing the list of stopwords from NLTK for text preprocessing.
from nltk.stem import RSLPStemmer  # Importing the RSLP stemmer from NLTK for reducing words to their root form.
from nltk.tokenize import word_tokenize  # Importing the word tokenizer from NLTK to split text into tokens.
from sklearn.pipeline import Pipeline  # Importing the Pipeline class from scikit-learn to chain multiple data processing steps.
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer  # Importing text vectorization tools TF-IDFVectorizer and CountVectorizer from scikit-learn.
from sklearn.naive_bayes import MultinomialNB  # Importing the Multinomial Naive Bayes classifier from scikit-learn.

# Function to extract text from a PDF
def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file using PyMuPDF.

    Parameters:
    file_path (str): The path of the PDF file.

    Returns:
    str: The extracted text from the PDF file.
    """
    text = ""  # Initializing an empty string to store the extracted text.
    try:
        with fitz.open(file_path) as pdf_file:  # Open the PDF file.
            for page in pdf_file:  # Iterate over all pages of the PDF.
                text += page.get_text()  # Extract text from each page and concatenate it to the text string.
    except Exception as e:
        print(f"An error occurred: {e}")
    return text  # Returning the extracted text from the PDF.

# Pipeline for vectorization/training model definition
pipeline = Pipeline([
    ('vect', CountVectorizer(max_features=10000)),  # Vectorization step using CountVectorizer.
    ('clf', MultinomialNB())  # Classification step using Multinomial Naive Bayes.
])

stopwords = stopwords.words('portuguese')  # Getting the list of stopwords in Portuguese.
stemmer = RSLPStemmer()  # Initializing the RSLP stemmer for reducing words to their root form.

def preprocess_text(text):
    """
    Performs text preprocessing.

    Parameters:
    text (str): The text to be preprocessed.

    Returns:
    str: The preprocessed text.
    """
    words = word_tokenize(text, language='portuguese')  # Tokenizing the text into words.
    words = [stemmer.stem(word) for word in words if word not in stopwords]  # Applying stemming and removing stopwords.
    return ' '.join(words)  # Returning the preprocessed text as a single string.

# Retrieving model training data
def load_data(file_path):
    """
    Loads model training data from a file.

    Parameters:
    file_path (str): The path of the file containing training data.

    Returns:
    dict: A dictionary containing the training data.
    """
    with open(file_path, 'rb') as file:  # Opening the file in binary read mode.
        data = pickle.load(file)  # Loading data from the file using pickle.
    return data  # Returning the loaded data.

##########################################################################################################################################
#  Function predict  the  especialized from a PDF file
def predict(file_path):
    initialPetition = extract_text_from_pdf(pdf_file_path)  # Extracting text from the PDF file.

    print('\n')

#     if initialPetition is not None:  # Checking if the text was successfully extracted.
    if not (initialPetition == ''): # Checking if the text was successfully extracted. (Changed at 22/05/2024) 
#         print('Preprocessing information for prediction...')  # Displaying a message indicating the start of preprocessing.
        X_prediction = [initialPetition]  # Putting the petition text into a list.
        prediction_preprocessing = preprocess_text(X_prediction[0])  # Preprocessing the petition text.
#         print('Preprocessing of information for prediction completed!')  # Displaying a message indicating the completion of preprocessing.
        prediction = pipeline.predict([prediction_preprocessing])  # Making a prediction of the case outcome with the trained model.    
        
        # # Getting the specialization based on the value of prediction[0]
        specialized = switch_case.get(prediction[0], 'NOT FOUND')
# 
#         print("Directed towards the specialized :", specialized)
        return(specialized)
     
    else:
#         print("Failed to convert PDF to text.")  # Displaying a failure message if the PDF to text conversion fails.
        return("Failed to convert PDF to text.")

##########################################################################################################################################

# Example usage:
loaded_data = load_data('trainingDataNaiveBayes.pkl')  # Loading training data from the file.
X_train, X_test, y_train, y_test = loaded_data['X_train'], loaded_data['X_test'], loaded_data['y_train'], loaded_data['y_test']
# Extracting training and testing sets from the loaded data.

# print('\n')
# print('Retrieved training data')  # Displaying a message indicating that the data has been successfully retrieved.

# Fitting the pipeline to the training data
pipeline.fit(X_train, y_train)  # Fitting the pipeline to the training data.

# Initializing the dictionary with default values
switch_case = {
    0: 'PAS',
    1: 'PDA',
    2: 'PPE',
    3: 'PSE',
    4: 'PTR',
    5: 'PUMA',
    6: 'PTA',
}

# while True:
# # Predicting a new initial petition
print("\nReviewing a new initial petition \n")
pdf_file_path = input('COLOCAR O INPUT DE DOCUMENTO DO PAV:')
    # Asking the user for the name of the PDF file containing the new initial petition.
    
print(predict(pdf_file_path))
    

