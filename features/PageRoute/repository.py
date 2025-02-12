import csv
from features.PageRoute.model import QueryModel
from features.PageRoute.model import PagesModel
from core.constants.constants import Database_URI,DB_NAME,Collections

# Data Source Class
class PagesRepo:
    def __init__(self, file_name:str):

        self.csv_filename = file_name
        self.file=open(self.csv_filename,'r')

    def GetPagesCSV(self) -> PagesModel:

        reader = csv.reader(self.file)
        result=[]
        for row in reader:
            result.append(row)

        return PagesModel(result)


from pymongo import MongoClient
class QueriesRepo:



    def StoreQueries(self , queries: QueryModel) -> list:

      
         queries.id = "none"
        