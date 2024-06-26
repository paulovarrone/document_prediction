import os  # Imports the os module to interact with the operating system.
import numpy as np  # Imports the numpy module for efficient numerical operations.
import pandas as pd  # Imports the pandas module for data manipulation in DataFrame format.
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer  # Imports TF-IDF and CountVectorizer text vectorization tools from scikit-learn.
from sklearn.model_selection import train_test_split  # Imports the train_test_split function from scikit-learn to split data into training and testing sets.
from sklearn.naive_bayes import MultinomialNB  # Imports the Multinomial Naive Bayes classifier from scikit-learn.
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix  # Imports metrics to evaluate model performance.
from sklearn.pipeline import Pipeline  # Imports the Pipeline class from scikit-learn to chain multiple data processing steps.
from nltk.corpus import stopwords  # Imports the NLTK stopwords list for text preprocessing.
from nltk.stem import RSLPStemmer  # Imports the RSLP stemmer from NLTK for reducing words to their root form.
from nltk.tokenize import word_tokenize  # Imports the NLTK word tokenizer to split text into tokens.
#from PyPDF2 import PdfReader  # Imports the PdfReader class from PyPDF2 to extract text from PDF files.
from tqdm import tqdm  # Imports the tqdm function to display progress bars during loops.
import pickle
import fitz  # PyMuPDF

# Function to extract text from a PDF
def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file using PyMuPDF.

    Parameters:
    file_path (str): The path of the PDF file.

    Returns:
    str: The extracted text from the PDF file.
    """
    text = ""  # Inicializa uma string vazia para armazenar o texto extraído.
    try:
        with open(file_path, 'rb') as file:  # Abre o arquivo PDF no modo de leitura binária.
            pdf_document = fitz.open(file)  # Abre o documento PDF com PyMuPDF.
            for page_num in range(pdf_document.page_count):  # Itera sobre todas as páginas do PDF.
                page = pdf_document.load_page(page_num)  # Carrega a página atual do PDF.
                text += page.get_text()  # Extrai o texto da página atual e concatena-o à string de texto.
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    return text  # Retorna o texto extraído do PDF.

# Mapping of alphabetical codes to sector numbers
sector_mapping = {  # Defines a dictionary to map alphabetical sector codes to numbers.
    'PAS' :  0,
    'PDA' :  1,
    'PPE' :  2,
    'PSE' :  3,
    'PTR' :  4,
    'PUMA':  5,
    'PTA' :  6
}

# Directory where the data (PDFs) are stored
data_dir = 'DirTrein'  # Defines the directory where the PDF files are stored.
pdf_files = os.listdir(data_dir)  # Lists the files in the specified directory.
documents = []  # Initializes a list to store the documents (text extracted from PDFs).
labels = []  # Initializes a list to store the document labels (mapped sector codes).

for file in tqdm(pdf_files, desc='Processing PDFs'):  # Iterates over the PDF files in the directory.
    if file.endswith('.pdf'):  # Checks if the file is a PDF.
        pdf_path = os.path.join(data_dir, file)  # Gets the full path of the PDF file.
        text = extract_text_from_pdf(pdf_path)  # Extracts text from the PDF.
        documents.append(text)  # Adds the extracted text to the list of documents.
        sector_code = file.split('_')[0]  # Extracts the sector code from the file name.
        sector_label = sector_mapping.get(sector_code)  # Gets the sector number mapped to the code.
        if sector_label is not None:  # Checks if the sector code is valid.
            labels.append(sector_label)  # Adds the label to the list of labels.
        else:
            print(f'Warning: Invalid sector code found in file {file}')  # Warning if the sector code is invalid.

# Creating a DataFrame with the two training variables
df = pd.DataFrame({'documents': documents,  # Creates a DataFrame with the documents.
                   'labels': labels  # Adds the labels to the DataFrame.
                  })

X = df['documents']  # Extracts the documents as independent variables.
y = df['labels']  # Extracts the labels as dependent variables.

# Pipeline for vectorization/training model definition
pipeline = Pipeline([
    ('vect', CountVectorizer(max_features=10000)),  # Vectorization step using CountVectorizer.
    ('clf', MultinomialNB())  # Classification step using Multinomial Naive Bayes.
])

stopwords = stopwords.words('portuguese')  # Gets the list of stopwords in Portuguese.
stemmer = RSLPStemmer()  # Initializes the RSLP stemmer for reducing words to their root form.

def preprocess_text(text):  # Defines a function for text preprocessing.
    """
    Performs text preprocessing.

    Parameters:
    text (str): The text to be preprocessed.

    Returns:
    str: The preprocessed text.
    """
    words = word_tokenize(text, language='portuguese')  # Tokenizes the text into words.
    words = [stemmer.stem(word) for word in words if word not in stopwords]  # Applies stemming and removes stopwords.
    return ' '.join(words)  # Returns the preprocessed text as a single string.

print('Preprocessing training data...')  # Displays a message indicating the start of preprocessing.
X_prep = X.apply(preprocess_text)  # Applies preprocessing to the documents.
print('Preprocessing completed!')  # Displays a message indicating the completion of preprocessing.

# Training the Naive Bayes model
pipeline.fit(X_prep, y)  # Trains the model with the preprocessed documents and corresponding labels.

# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_prep, labels, test_size=0.2, random_state=42)
# Splits the data into training and testing sets, where:
# X_train are the training documents
# X_test are the testing documents
# y_train are the training labels
# y_test are the testing labels

# # Accuracy evaluation with report using test data
# y_pred = pipeline.predict(X_test)
# # Makes predictions with the trained model using the testing documents
# report = classification_report(y_test, y_pred)
# # Generates a classification report comparing the actual labels (y_test) with the predictions (y_pred)
# print('Classification report:\n', report)
# # Displays the classification report
# 
# accuracy = accuracy_score(y_test, y_pred)
# # Calculates the accuracy of the model by comparing the actual labels with the predictions
# print(f'Model accuracy: {accuracy:.2f}')
# # Displays the model accuracy with two decimal places
# 
# print("\n")
# 
# # Confusion matrix
# confusion_matrix = confusion_matrix(y_test, y_pred)
# # Calculates the confusion matrix to evaluate the model performance
# print("Confusion Matrix:")
# print(confusion_matrix)
# # Displays the confusion matrix
# 
# print("\n")
# 
# # Predicting a new initial petition
# print("Reviewing a new initial petition \n")
# pdf_file_path = input('Enter the name of the "pdf" file with the initial petition:')
# # Asking the user for the name of the PDF file containing the new initial petition.
# 
# initialPetition = extract_text_from_pdf(pdf_file_path)  # Extracting text from the PDF file.
# 
# print('\n')
# 
# if initialPetition is not None:  # Checking if the text was successfully extracted.
#     print('Preprocessing information for prediction...')  # Displaying a message indicating the start of preprocessing.
#     X_prediction = [initialPetition]  # Putting the petition text into a list.
#     prediction_preprocessing = preprocess_text(X_prediction[0])  # Preprocessing the petition text.
#     print('Preprocessing of information for prediction completed!')  # Displaying a message indicating the completion of preprocessing.
#     prediction = pipeline.predict([prediction_preprocessing])  # Making a prediction of the case outcome with the trained model.    
#     
#     # Initializing the dictionary with default values
#     switch_case = {
#         0: 'PAS',
#         1: 'PDA',
#         2: 'PPE',
#         3: 'PSE',
#         4: 'PTR',
#         5: 'PUMA',
#         6: 'PTA',
#     }
# 
#     # # Getting the specialization based on the value of prediction[0]
#     specialized = switch_case.get(prediction[0], 'NOT FOUND')
# 
#     print("Directed towards the specialized :", specialized)
#  
# else:
#     print("Failed to convert PDF to text.")  # Displaying a failure message if the PDF to text conversion fails.

#############################################################################################
# Saving the model training data    


def save_data(X_train, X_test, y_train, y_test, file_path):
    """
    Saves the model training and testing data to a file.

    Parameters:
    X_train (DataFrame): The training documents.
    X_test (DataFrame): The testing documents.
    y_train (DataFrame): The training labels.
    y_test (DataFrame): The testing labels.
    file_path (str): The file path to save the data.
    """
    data = {'X_train': X_train, 'X_test': X_test, 'y_train': y_train, 'y_test': y_test}
    # Creates a dictionary containing the training and testing data
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)
        # Saves the data to the specified file using pickle
    print(f'Data saved to {file_path}')
    # Displays a message indicating that the data has been saved successfully

# Example usage:
file_path = 'trainingDataNaiveBayes.pkl'
save_data(X_train, X_test, y_train, y_test, file_path)
# Saves the model training and testing data to a file
print('\n')
print('Model training data saved')
# Displays a message indicating that the data has been saved successfully
