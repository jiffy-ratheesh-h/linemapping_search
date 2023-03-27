from utils import *



class LineNameFilter:
    def __init__(self,traffic:dict,track_data:list,traffic_data:list):
     self.traffic = traffic
     self.track_data = track_data
     self.traffic_data = traffic_data
    
    def filter_matched(self):
       response = line_name_search(self.traffic,self.track_data,self.traffic_data)
       final_response = rank_based_filter(response)
       return final_response

class lineNameMatch:
    def __init__(self,traffic:dict,track_data:dict):
     self.traffic = traffic
     self.track_data = track_data
    
    def check_matched(self):
       
       response = check_line_name(self.traffic,self.track_data)
       return response
   
class CreatitveNameSearch:
    def __init__(self,keyword:str,target:str):
     self.keyword = keyword
     self.target = target
    
    def filter_matched(self):
       response = creative_name_search(self.keyword,self.target)
       return response