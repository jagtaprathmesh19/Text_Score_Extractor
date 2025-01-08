"""
The data_analyzer module: Support for analyzaing data from text files.

At large scale, the structure of the module is following:
* Imports and exports, all required depandencies.
* Internal helper functions: these should never be used in code outside this module.
^ Performs all the necessary Natural Language text analysis process.
"""
from typing import List
from os import getcwd, listdir
from string import punctuation
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords


class TextAnalyzer:
    __positiveWords = []
    __negativeWords = []

    def __init__(self):
        '''
        Instantiated all the text analysis information which we have to perform
        '''
        self.__curEntryInfo = None
        self.__text = None
        self.__wordTokens = []
        self.__sentTokens = []
        self.__stopWords = []
        self.__wordsWithoutPunctactions = []
        self.__cleanWords = []
        self.__positiveScore = 0
        self.__negativeScore = 0
        self.__polarityScore = 0
        self.__subjectivityScore = 0
        self.__avgSentenceLength = 0
        self.__percentOfComplexWords = 0
        self.__fogIndex = 0
        self.__avgWordsPerSentence = 0
        self.__complexWordCount = 0
        self.__wordCount = 0
        self.__syllablePerWord = 0
        self.__personalPronouns = 0
        self.__avgWordLength = 0
        self.__curDataset = []

    @staticmethod
    def define_master_dictionary() -> List[str]:
        '''
        This creates list of positive and negative words.
        '''
        path = getcwd() + "\\MasterDictionary"
        master_dictionary = listdir(path)
        NP_files = [''.join((path, '\\', name)) for name in master_dictionary]

        with open(NP_files[0], 'r') as f:
            # n_words = f.read()
            TextAnalyzer.__negativeWords = set(f.read().splitlines())

        with open(NP_files[1], 'r') as f:
            # p_words = f.read()
            TextAnalyzer.__positiveWords = set(file.read().splitlines())

    @staticmethod
    def StopWords_list() -> List[str]:
        '''
        This creates a list of stopwords form text files
        '''
        path = getcwd() + "\\StopWords"
        StopWord_txt = listdir(path)
        SW_txt_paths = [''.join((path + '\\' + name)) for name in StopWord_txt]

        stopWords = []
        for txt in SW_txt_paths:
            SW_file = open(txt, 'r')
            words = SW_file.read()
            stop_words = words.lower().split()
            stopWords.extend(stop_words)
        # len(stopWords) == 14328
        return stopWords

    def __extract_text(self):
        '''
        It helps to read all the text files
        '''
        fileLoc = self.__curEntryInfo['File Loc']
        try:
            file = open(fileLoc, 'r')
            self.__text = file.read()
        except:
            file = open(fileLoc, 'rb')
            self.__text = file.read().decode('utf-8')
        file.close()

    def __cal_tokens(self):
        '''
        This methods is used to get tokenize words and sentences
        then create liste of clean words
        '''
        self.__wordTokens = word_tokenize(self.__text)
        self.__sentTokens = sent_tokenize(self.__text)
        self.__stopWords = set(TextAnalyzer.StopWords_list())
        self.__wordsWithoutPunctactions = [
            word for word in self.__wordTokens if not (word in punctuation)]
        self.__cleanWords = [word for word in self.__wordsWithoutPunctactions if not (
            word.lower() in self.__stopWords)]

    def __sentiment_analysis(self):
        """
        This method get all the parameters which is used for sentiment analysis

        Returns: 
        -Positive Score
        -Negative Score
        -Polarity Score
        -Subjectivity Score
        """
        positiveScore = 0
        negativeScore = 0

        for word in self.__cleanWords:
            if word in self.__positiveWords:
                positiveScore += 1
        for word in self.__cleanWords:
            if word in self.__negativeWords:
                negativeScore += 1

        self.__positiveScore = positiveScore
        self.__negativeScore = negativeScore
        sumPositiveandNegative = (self.__positiveScore + self.__negativeScore)
        self.__polarityScore = (
            self.__positiveScore - self.__negativeScore) / (sumPositiveandNegative + 0.000001)
        self.__subjectivityScore = sumPositiveandNegative / \
            (len(self.__cleanWords) + 0.000001)

    def __analysis_of_readability(self):
        """
        This method returns the parameters which used to analysis the readability of text

        Returns:
        -Average Sentence lenght
        -Percentage of Complex words
        -Fog Index
        """
        self.__avgSentenceLength = len(
            self.__wordsWithoutPunctactions) / len(self.__sentTokens)
        self.__percentOfComplexWords = self.__complexWordCount / \
            len(self.__wordsWithoutPunctactions)
        self.__fogIndex = 0.4 * \
            (self.__avgSentenceLength + self.__percentOfComplexWords)

    def __average_words_per_sentence(self):
        self.__avgWordsPerSentence = len(
            self.__wordsWithoutPunctactions) / len(self.__sentTokens)

    def __complex_word_count(self):
        complex_word = 0
        for word in self.__wordsWithoutPunctactions:
            if self.__count_syllable(word) > 2:
                complex_word += 1

        self.__complexWordCount = complex_word

    def __word_count(self):
        self.__wordCount = len(self.__cleanWords)

    def __syllable_count_per_word(self):
        total_syllable = 0
        for word in self.__wordsWithoutPunctactions:
            total_syllable += self.__count_syllable(word)

        self.__syllablePerWord = total_syllable / \
            len(self.__wordsWithoutPunctactions)

    @staticmethod
    def __count_syllable(word) -> int:
        vowels = ['a', 'e', 'i', 'o', 'u']
        cur_syllable = 0
        word = word.lower()
        for char in word:
            if char in vowels:
                cur_syllable += 1

        if word.endswith('ed') or word.endswith('es'):
            cur_syllable -= 1

        cur_syllable = max(0, cur_syllable)
        return cur_syllable

    def __personal_pronouns(self):
        wordsWithTags = pos_tag(self.__wordsWithoutPunctactions)
        personal_pronouns = []
        for words in wordsWithTags:
            if words[1] in ['PRP']:
                personal_pronouns.append(words[0])
        self.__personalPronouns = len(personal_pronouns)

    def __average_word_lenght(self):
        total = 0
        for word in self.__wordsWithoutPunctactions:
            total += len(word)

        self.__avgWordLength = total / len(self.__wordsWithoutPunctactions)

    def analyze(self, cur_entry_info):
        '''
        This method collect all the information for text analysis
        '''
        self.__curEntryInfo = cur_entry_info
        self.__extract_text()
        if len(self.__text) > 1:
            self.__cal_tokens()
            self.__sentiment_analysis()
            self.__syllable_count_per_word()
            self.__complex_word_count()
            self.__analysis_of_readability()
            self.__average_words_per_sentence()
            self.__word_count()
            self.__personal_pronouns()
            self.__average_word_lenght()

    def get_cur_dataset(self) -> list:
        '''
        This creates  list of data which perform text analysis.'''
        self.__curDataset = [self.__curEntryInfo['URL_ID'],
                             self.__curEntryInfo['URL'],
                             self.__positiveScore,
                             self.__negativeScore,
                             self.__polarityScore,
                             self.__subjectivityScore,
                             self.__avgSentenceLength,
                             self.__percentOfComplexWords,
                             self.__fogIndex,
                             self.__avgWordsPerSentence,
                             self.__complexWordCount,
                             self.__wordCount,
                             self.__syllablePerWord,
                             self.__personalPronouns,
                             self.__avgWordLength
                             ]
        return self.__curDataset
