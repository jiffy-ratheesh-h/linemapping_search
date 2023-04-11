from jiffy_search import CheckLineName, SearchAlgorithms
from ._helper import *
from datetime import datetime
import csv
import os
import pandas as pd

def line_name_search(traffic,track_data,traffic_data):
    write_data = []
    for track in track_data:
        response = search_here(traffic,track,traffic_data)
        match_keyword = response['match_keyword'].strip()
        print(match_keyword)
        if(response['word_match'] is None):
            response['word_match'] = ""
        payload = {
            'Status':response['status'],
            'Original Line Name':traffic['Original_Line_Name'],
            'Original Placement Name':track['Original_Placement_Name'],
            'Line Name':traffic['New_Line_Name'],
            'Mapped Line Name':traffic['Mapped_Line_Name'],
            'Placement Name':response['target'],
            'Operative ID':traffic.get('Operative_ID',None),
            'Algorithm':response['algorithm'],
            'Count':response['match_count'],
            'Info':response['word_match'],
            'Rank':0,
            'Match Keyword':match_keyword,
            'Longest Keyword' : "",
            'Track':track
        }
        present_status = check_present_status(write_data,payload)
        if(present_status == False):
            write_data.append(payload)
    new_write_data = get_ranked(write_data)
    return new_write_data

    
def check_line_name(traffic,track):
    response = search_here(traffic,track,[])
    if(response['status'] == True):
        return True
    else:
        return False


def rank_based_filter(write_data):
    new_response_track = []
    new_filtered_write_data = list(filter(lambda d: int(d['Rank']) == 1 and d['Status'] == True, write_data))
    for item in new_filtered_write_data:
        new_response_track.append(item['Track'])
    return new_response_track


def creative_name_search(keyword,target):
    response = CheckLineName(keyword,target).find_match()
    print(response)
    if(response['status'] == True):
        return True
    else:
        return False
    

def  write_excel_data(response,file_path,traffic):
    try:
        if(os.path.exists(file_path) == True):
            df2 = pd.DataFrame(response)
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:  
                df2.to_excel(writer, sheet_name=str(traffic['Operative_ID']))
        else:
            df2 = pd.DataFrame(response)
            with pd.ExcelWriter(file_path) as writer:  
                df2.to_excel(writer, sheet_name=str(traffic['Operative_ID']))
    except:
        pass