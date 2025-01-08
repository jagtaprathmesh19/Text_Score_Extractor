from warnings import filterwarnings
from os import makedirs, path, remove
from pandas import read_excel, DataFrame, ExcelWriter
from src.data_extractor import WebScrapper
from src.data_analyzer import TextAnalyzer


def main():
    '''
    This function creates a file with url, url_id and all text analysis features which is stored in 
    excel file. 
    '''
    # Reading the input excel file
    inputDataset = read_excel("Input.xlsx")
    totalDataset = []

    folderName = "Text Files"  # text files folder name
    if path.exists(folderName):
        remove(folderName)
    makedirs(folderName, exist_ok=True)  # it creates folder

    TextAnalyzer.define_master_dictionary()
    for index in range(inputDataset.shape[0]):
        # This creates file name using url_id
        filename = str(inputDataset.loc[index, 'URL_ID']) + '.txt'
        fileLoc = path.join(folderName, filename)  # creates file name
        # This is the dictionary which is used to scrap and analyze data
        curEntryInfo = {'URL_ID': inputDataset.loc[index, 'URL_ID'],
                        'URL': inputDataset.loc[index, 'URL'],
                        'File Loc': fileLoc}
        web_scrape = WebScrapper()  # Calling data extractor
        web_scrape.scrape(cur_entry_info=curEntryInfo)

        text_analysis = TextAnalyzer()  # callign data analyzer
        text_analysis.analyze(cur_entry_info=curEntryInfo)
        curDataset = text_analysis.get_cur_dataset()
        totalDataset.append(curDataset)
    print("Analysis Completed")

    columns = ['URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE',
               'POLARITY SCORE', 'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH',
               'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
               'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT',
               'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']
    outputDataset = DataFrame(totalDataset, columns=columns)
    writer = ExcelWriter('Output Data Structure.xlsx',
                         engine='xlsxwriter')
    outputDataset.to_excel(writer, sheet_name='Sheet1',
                           index=False, na_rep='NaN', float_format="%.2f")

    for column in outputDataset:
        column_width = int(
            max(outputDataset[column].astype(str).map(len).max(), len(column)))
        col_idx = outputDataset.columns.get_loc(column)
        writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_width)

    writer.save()
    print("Output Successfully Saved!!")


if __name__ == '__main__':
    filterwarnings("ignore")
    main()
