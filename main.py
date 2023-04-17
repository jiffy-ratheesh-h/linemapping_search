from .utils import *



class LineNameFilter:
    def __init__(self,traffic:dict,track_data:list,traffic_data:list,case_path:str,master_uuid:str):
     self.traffic = traffic
     self.track_data = track_data
     self.traffic_data = traffic_data
     self.case_path = case_path
     self.master_uuid = master_uuid
    
    def filter_matched(self):
       response = line_name_search(self.traffic,self.track_data,self.traffic_data)
       file_path = os.path.join(self.case_path,self.master_uuid + "_linename_search_response.xlsx")
       write_excel_data(response,file_path,self.traffic)
       final_response = rank_based_filter(response)
       return unique_list(final_response)

class lineNameMatch:
    def __init__(self,traffic:dict,track_data:dict):
     self.traffic = traffic
     self.track_data = track_data
    
    def check_match(self):
       response = check_line_name(self.traffic,self.track_data)
       return response
   
class CreatitveNameSearch:
    def __init__(self,keyword:str,target:str):
     self.keyword = keyword
     self.target = target
    
    def creative_name_search(self):
       response = creative_name_search(self.keyword,self.target)
       return response


class CustomLineNameFilter:
    def __init__(self,traffic:dict,track_data:list,traffic_data:list,track_column:str, trafic_column:str,recheck:bool=False):
     self.traffic = traffic
     self.track_data = track_data
     self.traffic_data = traffic_data
     self.track_column = track_column
     self.trafic_column = trafic_column
     self.recheck = recheck
    
    def filter_matched(self):
       response = custom_line_name_search(self.traffic,self.track_data,self.traffic_data,self.trafic_column,self.track_column,self.recheck)
       final_response = rank_based_filter(response)
       return final_response