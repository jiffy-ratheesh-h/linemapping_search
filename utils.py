from jiffy_search import CheckLineName, SearchAlgorithms
from ._helper import *
from datetime import datetime
import copy
import sys
import os
import pandas as pd

def line_name_search(traffic,track_data,traffic_data):
    write_data = []
    track_data_copy = copy.deepcopy(track_data)
    for track in track_data:
        response = search_here(traffic,track,traffic_data)
        match_keyword = response['match_keyword'].strip()
        if(response['word_match'] is None):
            response['word_match'] = ""
        track_obj = {}
        for i in track_data_copy:
            if(track['UUID'] == i['UUID']):
                track_obj = i
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
    exact_match_filter = list(filter(lambda d: str(d['Algorithm']) == 'Exact Match' and d['Status'] == True, write_data))
    if(len(exact_match_filter) == 0):
        new_filtered_write_data = list(filter(lambda d: int(d['Rank']) == 1 and d['Status'] == True, write_data))
        for item in new_filtered_write_data:
            new_response_track.append(item['Track'])
    else:
        for item in exact_match_filter:
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


def custom_line_name_search(traffic,track_data,traffic_data,traffic_column,track_column,recheck):
    write_data = []
    try:
        track_data_copy = copy.deepcopy(track_data)
        print(f"Len of Track Data = {len(track_data_copy)}")
        if(recheck == False):
            if(len(track_data_copy) >= 2):
                print("Entered on Cleansing of removing common keyword")
                track_data_copy = custom_remove_common_words(track_data_copy,track_column)
        for track in track_data_copy:
            if(traffic[traffic_column] is not None and track[track_column] is not None):
                track_obj = {}
                for i in track_data:
                    if(track['UUID'] == i['UUID']):
                        track_obj = i
                print(f"Moving on comparison part with {traffic[traffic_column]} XX {track[track_column]}")
                response = custom_search_here(traffic,track,traffic_data,traffic_column,track_column)
                print(traffic[traffic_column],"  X  ",track[track_column])
                print(response)
                match_keyword = response['match_keyword'].strip()
                if(response['word_match'] is None):
                    response['word_match'] = ""
                payload = {
                    'Status':response['status'],
                    traffic_column:traffic[traffic_column],
                    track_column:track[track_column],
                    'Algorithm':response['algorithm'],
                    'Count':response['match_count'],
                    'Info':response['word_match'],
                    'Rank':0,
                    'Match Keyword':match_keyword,
                    'Longest Keyword' : "",
                    'UUID':track_obj['UUID'],
                    'Track':track_obj
                }
                present_status = custom_check_present_status(write_data,payload,traffic_column,track_column)
                if(present_status == False):
                    write_data.append(payload)
        new_write_data = custom_get_ranked(write_data,traffic_column)
        # print(new_write_data)
        return new_write_data
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err_msg = "Error = {0} Line Number : {1} , Error Type = {2} File = {3}".format(str(e),exc_tb.tb_lineno,exc_type,fname)
        print(err_msg)
        print("Exception Occurred on custom Line Name Search",str(e))
        return []