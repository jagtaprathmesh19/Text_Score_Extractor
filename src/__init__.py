'''
This package contain all the operations and information which used to perform text analysis.
Our main agenda is to perform Text analysis which includes scraping data from the given input urls,
storing in text files using URL_ID as there name and on that data we have to perform some operations which 
gives such informations.

1.URL_ID, URL
2.POSITIVE SCORE
3.NEGATIVE SCORE
4.POLARITY SCORE
5.SUBJECTIVITY SCORE
6.AVG SENTENCE LENGTH
7.PERCENTAGE OF COMPLEX WORDS
8.FOG INDEX
9.AVG NUMBER OF WORDS PER SENTENCE
10.COMPLEX WORD COUNT
11.WORD COUNT
12.SYLLABLE PER WORD
13.PERSONAL PRONOUNS
14.AVG WORD LENGTH

This Package does two major tasks:

Data Extraction
Data Analysis

Project Directory
.
|-- Input.xlsx
|-- MasterDictionary
|   |-- negative-words.txt
|   `-- positive-words.txt
|-- Objective.docx
|-- Output Data Structure.xlsx
|-- StopWords
|   |-- StopWords_Auditor.txt
|   |-- StopWords_Currencies.txt
|   |-- StopWords_DatesandNumbers.txt
|   |-- StopWords_Generic.txt
|   |-- StopWords_GenericLong.txt
|   |-- StopWords_Geographic.txt
|   `-- StopWords_Names.txt
|-- Text Analysis.docx
|-- Text Files
|-------
|-- main.py
|-- src
|   |-- __init__.py
|   |-- data_analyzer.py
|   `-- data_extractor.py

Quick fixes:-

# Install all the requirements
"pip install -r requirement.txt"

# Run main file in terminal
"python main.py"

'''
