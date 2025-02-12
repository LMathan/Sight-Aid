class PagesModel:
    def __init__(self,result_lst:list):
        self.data={}
        self.convert_data(result_lst)

    def convert_data(self, result):

        print(result)
        for page in result[1:]:  
            self.data[page[0]] = page[1]



class QueryModel:
    def __init__(self,id,query,language,response,itemorplace):
        self.id=id
        self.query=query
        self.language=language
        self.response=response
        self.itemorplace=itemorplace