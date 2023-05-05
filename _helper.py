from jiffy_search import CheckLineName, SearchAlgorithms
import json
from operator import itemgetter
import os

# config_path = r"Y:\Configurations\Line_Name_configs"
# line_mapping_config_file = os.path.join(config_path,'Line_Name_Mapping_Configurations.json')
# f = (line_mapping_config_file,'r') 
# config_list =json.load(f)
# unavoidable_list_data = []
# for itm in config_list:
#     if("|" not in itm['Name']):
#         unavoidable_list_data.append(itm['Name'])
#     else:
#         itm_list = str(itm).split("|")
#         unavoidable_list_data.extend(itm_list)
# unavoidable_list = "|".join(unavoidable_list_data)

exlusion_list = "a VCBS|EyeQ|OCR|Adults|Video|Standard|640|480|PMNT|Local|Entertainment|VCBS|pls|note|dart|dates|please|dark|Plus|News|Exclusion|dma|vantage|25-54|18-54|:15|15s|:30|30s|:60|:60s|15|30|60|san|CDSM|CDHC|ch22|sports|can|desktop|mobile|ott|City|Falls|Desk|Mob|zips|Zips|Skip|Non|is|or|an|am|iam|auto|bay"
priority_list = "city|"
mandatory_list = "anniversary|campus"
delimetter = ["`",'~','|','@','#','$','%','&','^','*','(',')','_','-',' ',',','-'," "]
unavoidable_list = "ct|wk"

def unique_list(list_items):
    unique_list = []
    for x in list_items:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

def make_response(status,algorithm,keyword,target,match_count=0,word_match=None):
    return {
        'status':status,
        'algorithm':algorithm,
        'keyword':keyword,
        'target':target,
        'match_count':match_count,
        'word_match':word_match
    }

def club_line_name(line_name):
    line_name_split = str(line_name).split(" ")
    new_line_split = []
    for i in range(len(line_name_split)-1):
        if(len(line_name_split[i]) >= 3 and len(line_name_split[i+1])>=3):
            word = line_name_split[i] + " "+line_name_split[i+1]
            new_line_split.append(word)
            word = line_name_split[i] + line_name_split[i+1]
            new_line_split.append(word)
    if(len(new_line_split)>=1):
        return new_line_split
    else:
        return False

def club_three_line_name(line_name):
    line_name_split = str(line_name).split(" ")
    new_line_split = []
    for i in range(len(line_name_split)-2):
        if(len(line_name_split[i]) == 1):
            try:
                word = line_name_split[i-1] +line_name_split[i] + line_name_split[i+1]
                new_line_split.append(word)
            except:
                pass
        if(len(line_name_split[i]) >= 3 and len(line_name_split[i+1])>=1):
            word = line_name_split[i] +line_name_split[i+1] +line_name_split[i+2]
            new_line_split.append(word)
            word = line_name_split[i] + " " + line_name_split[i+1] + " " + line_name_split[i+2]
            new_line_split.append(word)
        else:
            word = line_name_split[i]+" " +line_name_split[i+1]
            new_line_split.append(word)
    if(len(new_line_split)>=1):
        return new_line_split
    else:
        return False
    
def unique_list(list_items):
    unique_list = []
    for x in list_items:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


def clean_line_name(x,original_line_name):
    removed_count = 0
    line_name = x.lower()
    x = x.lower()
    x = str(x).replace("|"," ")
    x_list = x.split(" ")
    keywords = str(exlusion_list).split("|")
    if(len(x)>=1):
        for words in keywords:
            words = str(words).lower()
            for name in x_list:
                name = name.lower()
                if(str(words)== str(name)):
                    removed_count +=1
                    x = str(x).replace(words,"").replace(")"," ").replace("("," ")
                    x = x.strip()
    if(removed_count >= 1):
        new_line_name = str(x).replace("  "," ").strip()
        if(len(new_line_name) <= 1):
            original_line_name_split = str(original_line_name).split("|")
            line_name = original_line_name_split[3]
            return line_name
        else:
            return new_line_name
    else:
        return line_name.strip()

def clean_placement_name(filter_placement_data):
    try:
        creative_name = filter_placement_data[0]['Placement_Names']
        for delim in delimetter:
            split_creative_name = str(creative_name).split(delim)
            if(len(split_creative_name) > 1):
                for word in split_creative_name:
                    word = str(word).lower()
                    # print("word",word)
                    wordmatchcount = 0
                    for track in filter_placement_data:
                        if(word.lower() in str(track['Placement_Names']).lower()):
                            # print("mactch Foiunf")
                            wordmatchcount +=1
                    # print("macthcount",wordmatchcount)
                    # print("rtrack count",len(filter_placement_data))
                    # print("placement namer = ",track['Placement_Names'])
                    if(wordmatchcount == len(filter_placement_data)):
                        for iteeem in filter_placement_data:
                            if(len(word) >= 2):
                                iteeem['Placement_Names'] = str(iteeem['Placement_Names']).lower().replace(word,"")
                                iteeem['Placement_Names'] = str(iteeem['Placement_Names']).lower().replace(delim,"")
                                # print("Replaced",iteeem['Placement_Names'])
    except:
        return filter_placement_data

def check_present_status(write_data,payload):
    for item in write_data:
        if(item['Line Name'] == payload['Line Name'] and item['Placement Name'] == payload['Placement Name']):
            return True
    return False

def remove_spcl_characters(placement_name):
    SPECIAL_CHARACTERS = ["`",'~','|','@','#','$','%','&','^','*','(',')','_','-',' ',',','-'," ","/",";",':',"\\","."]
    placement_name = ''.join([i if ord(i) < 128 else ' ' for i in placement_name])
    for delim in SPECIAL_CHARACTERS:
        placement_name = str(placement_name.replace(delim," "))
    # nums = re.findall(r'\d{2,10}', str(placement_name))
    # if(len(nums) >= 1):
    #     for n in nums:
    #         placement_name = str(placement_name).replace(n,'')
    return placement_name.replace("  "," ").strip()

def remove_starting_chars(placement_name):
    split_placement_name = placement_name.split(" ")
    try:
        if(len(split_placement_name[0]) == 1):
            split_placement_name.remove(split_placement_name[0])
    except:
        pass
    return " ".join(split_placement_name).replace("  "," ").strip()

def re_search(new_line_name,new_placement_name):
    line_name_split = club_line_name(new_line_name)
    # print(line_name_split)
    if(line_name_split != False):
        for item in line_name_split:
            response = SearchAlgorithms(item,new_placement_name).search_forward()
            if(response['status'] == False):
                response = SearchAlgorithms(item,new_placement_name).search_backward()
                if(response['status'] == False):
                    response = SearchAlgorithms(item,new_placement_name).search_contains()
                    if(response['status'] == True):
                        return response
                else:
                    return response
            else:
                return response
        return response
    else:
        return False

def re_three_search(new_line_name,new_placement_name):
    line_name_split = club_three_line_name(new_line_name)
    if(line_name_split != False):
        for item in line_name_split:
            response = SearchAlgorithms(item,new_placement_name).search_forward()
            if(response['status'] == False):
                response = SearchAlgorithms(item,new_placement_name).search_backward()
                if(response['status'] == False):
                    response = SearchAlgorithms(item,new_placement_name).search_contains()
                    if(response['status'] == True):
                        return response
                else:
                    return response
            else:
                return response
        return response
    else:
        return False
    
def check_with_mapped_line_name(mapped_line_name,new_line_name,new_placement_name):
    try:
        if("|" in mapped_line_name):
            mapped_line_name = mapped_line_name.split("|")
            mapped_match_count = 0
            mapped_match_words = []
            for linename in mapped_line_name:
                print(linename)
                process_status = False
                line_name_split = linename.split(" ")
                if(len(line_name_split) >= 2):
                    if(len(line_name_split[1]) == 1):
                        process_status == False
                    else:
                        process_status = True
                else:
                    process_status = True
                if(process_status == True):
                    # print("process_status True")
                    response = CheckLineName(linename,new_placement_name).find_match()
                    if(response['status'] == True):
                        print(response)
                        mapped_match_words.extend(response['word_match'])
                    # print(response)
            if(len(mapped_match_words) >=1):
                return make_response(True,'Mapped Line Name',mapped_line_name,new_placement_name,len(mapped_match_words),mapped_match_words)
            else:
                return make_response(False,'Mapped Line Name',mapped_line_name,new_placement_name,0)
                        
        else:
            process_status = False
            line_name_split = mapped_line_name.split(" ")
            if(len(line_name_split) >= 2):
                if(len(line_name_split[1]) == 1):
                    process_status == False
                else:
                    process_status = True
            else:
                process_status = True
            if(process_status == True):
                response = CheckLineName(mapped_line_name,new_placement_name).find_match()
                return response
            else:
                return make_response(False,'Mapped Line Name',mapped_line_name,new_placement_name,0)
    except Exception as e:
        raise Exception(str(e))
    

def check_list_is_same_or_not(date_list):
    current_date = date_list[0]
    count = date_list.count(current_date)
    if(count == len(date_list)):
        return True
    else:
        return False
    
def get_longest_word_from_list(test_list):
    res = ""
    len_list = [len(itm) for itm in test_list]
    if(check_list_is_same_or_not(len_list)):
        return test_list
    else:
        max_len = -1
        for ele in test_list:
            if len(ele) > max_len:
                max_len = len(ele)
                res = ele
        return [res]

def split_line_name(line_name):
    line_name_split = line_name.split()
    if(len(line_name_split) == 1):
        return True
    elif(len(line_name_split) == 2):
        if(len(line_name_split[1]) == 1):
            return True
        else:
            return False
    else:
        return False

def remove_common_words(original_line_name, filter_line_name_data):
    # filtered_line_name = [str(item['Original_Line_Name']).lower() for item in filter_line_name_data]
    original_line_name = str(original_line_name).lower()
    original_line_name_split = str(original_line_name).split(" ")
    if(len(original_line_name_split) >= 1):
        for word in original_line_name_split:
            count = 0
            for line_name in filter_line_name_data:
                if(word in str(line_name['Original_Line_Name']).lower()):
                    count += 1
            if(count == len(filter_line_name_data)):
                original_line_name_split.remove(word)
        return " ".join(original_line_name_split)
    return original_line_name

def clean_original_line_name(original_line_name):
    removed_count = 0
    line_name = original_line_name.lower()
    x = original_line_name.lower()
    x = str(x).replace("|"," ")
    x_list = x.split(" ")
    keywords = str(priority_list).split("|")
    if(len(x)>=1):
        for words in keywords:
            words = str(words).lower()
            for name in x_list:
                name = name.lower()
                if(str(words)== str(name)):
                    removed_count +=1
                    x = str(x).replace(words,"").replace(")"," ").replace("("," ")
                    x = x.strip()
    if(removed_count >= 1):
        new_line_name = str(x).replace("  "," ").strip()
        if(len(new_line_name) <= 1):
            original_line_name_split = str(original_line_name).split("|")
            line_name = original_line_name_split[3]
            return line_name
        else:
            return new_line_name
    else:
        return line_name.strip()

def check_with_original_line_name(original_line_name,new_placement_name,filter_line_name_data=[]):
    response = False
    original_line_name = original_line_name
    original_line_name = original_line_name.split("|")
    original_line_name = remove_spcl_characters(original_line_name[len(original_line_name) -1])
    original_line_name = remove_starting_chars(original_line_name)
    # original_line_name = clean_original_line_name(original_line_name)
    if(len(filter_line_name_data) >= 2):
        original_line_name = remove_common_words(original_line_name, filter_line_name_data)
    original_line_name_split = original_line_name.split()
    try:
        if(len(original_line_name_split[1]) >= 2):
            response = CheckLineName(original_line_name,new_placement_name).find_match()
            if(response['status'] == False or response['match_count'] == 1):
                clubbed_line_name = club_three_line_name(original_line_name)
                # print(clubbed_line_name)
                if(clubbed_line_name is not False):
                    for word in clubbed_line_name:
                        response = CheckLineName(word,new_placement_name).find_match()
                        if(response['status'] == True):
                            return response
                else:
                    return response
        else:
            return False
    except:
        response = False
    return response


def keyword_map(new_line_name):
    '''
    Mapping with the x value with Y table Name
    '''
    # new_line_name = ' '.join(e for e in new_line_name if e.isalnum())

    # print("################### Row Len = {} #####################".format(len(mapping_details)))
    file = open('Line_Name_Configurations.json')
    mapping_details =json.load(file) 
    mapped_line_name = []
    for item in mapping_details:
        new_keyword_list = []
        keywords_list = str(item['Keywords']).split("|")
        name_list = str(item['Name']).split("|")

        for itm in keywords_list:
            if itm.strip():
                new_keyword_list.append(itm.lower().strip())
        
        for word in new_keyword_list:
            resp = {}
            new_line_name = str(new_line_name).lower().strip()
            resp['status'] = True if word == new_line_name else False
            if(resp['status'] == True):
                name = str(item['Name']).replace("|","")
                mapped_line_name.append(name)
    if(len(mapped_line_name) == 0):
        for item in mapping_details:
            new_keyword_list = []
            keywords_list = str(item['Keywords']).split("|")
            name_list = str(item['Name']).split("|")

            for itm in keywords_list:
                if itm.strip():
                    new_keyword_list.append(itm.lower().strip())
            
            for word in new_keyword_list:
                resp = {}
                new_line_name = str(new_line_name).lower().strip()
                resp = CheckLineName(word,new_line_name).find_match()
                if(resp['status'] == True):
                    name = str(item['Name']).replace("|","")
                    mapped_line_name.append(name)
    if(len(mapped_line_name) == 0):
        for item in mapping_details:
            new_keyword_list = []
            keywords_list = str(item['Name']).split("|")

            for itm in keywords_list:
                if itm.strip():
                    new_keyword_list.append(itm.lower().strip())
            
            for word in new_keyword_list:
                resp = {}
                new_line_name = str(new_line_name).lower().strip()
                resp['status'] = True if word == new_line_name else False
                if(resp['status'] == True):
                    name = str(item['Keywords']).replace("|","")
                    mapped_line_name.append(name)
    if(len(mapped_line_name) >= 1):
        mapped_line_name = unique_list(mapped_line_name)
        return "|".join(mapped_line_name).strip()
    return new_line_name.strip()


def check_mandory_list(original_line_name,keyword_list,mandatory_list):
    mandatory_match_list = []
    mandatory_validity_status = False
    for word in mandatory_list:
        word = str(word).lower()
        if(word in original_line_name):
            mandatory_validity_status = True
            if(len(keyword_list) >= 2):
                mandatory_match_list.append(word)
    if(mandatory_validity_status == True and len(mandatory_match_list) >= 1):
        return True
    elif(mandatory_validity_status == True and len(mandatory_match_list) == 0):
        return False
    else:     
        return True

def check_priority(keyword,exlusion_list,original_line_name,mandatory_list):
    new_exlusion_list = str(exlusion_list).lower().split("|")
    keyword_list = str(keyword).lower().split(',')
    mandatory_list = str(mandatory_list).split("|")
    original_line_name = str(original_line_name).lower()
    mandatory_status = check_mandory_list(original_line_name,keyword_list,mandatory_list)
    if(mandatory_status == True):
        if(len(keyword_list) == 1):
            if(len(keyword_list[0]) >= 3):
                if(keyword in new_exlusion_list or len(keyword) <= 2):
                    return False
                else:
                    return True
            else:
                if(keyword in unavoidable_list.split("|")):
                    return True
                return False
        else:
            exclusion_count = 0
            for word in keyword_list:
                if(word in new_exlusion_list):
                    exclusion_count += 1
            if(len(keyword_list) == exclusion_count):
                return False
            else:
                return True
    else:
        return False
        
def decode_match_keyword(response):
    match_keyword = []
    if(response['word_match'] is not None):
        for wordMatch in response['word_match']:
            if(type(wordMatch['Target']) is list and type(wordMatch['Keyword']) is list):
                if(len(wordMatch['Target']) > len(wordMatch['Keyword'])):
                    match_keyword.append(", ".join(wordMatch['Keyword']))
                elif(len(wordMatch['Target']) < len(wordMatch['Keyword'])):
                    match_keyword.append(", ".join(wordMatch['Target']))
                else:
                    match_keyword.append(", ".join(wordMatch['Target']))
            elif(type(wordMatch['Target']) is str and type(wordMatch['Keyword']) is str):
                split_keyword = wordMatch['Keyword'].split(" ")
                split_target = wordMatch['Target'].split(" ")
                if(len(split_keyword) < len(split_target)):
                    match_keyword.append(", ".join(split_keyword))
                else:
                    match_keyword.append(", ".join(split_target))
            elif(type(wordMatch['Target']) is list and type(wordMatch['Keyword']) is not list):
                split_keyword = wordMatch['Keyword'].split(" ")
                match_keyword.append(", ".join(split_keyword))
            else:
                split_target = wordMatch['Target'].split(" ")
                match_keyword.append(", ".join(split_target))
    if(len(match_keyword) >= 1):
        new_match_keyword = []
        for itm in match_keyword:
            if("," in itm):
                new_itm = itm.split(",")
                new_itm = [str(item).strip().lower() for item in new_itm]
                new_match_keyword.extend(new_itm)
            else:
                new_match_keyword.append(itm) 
        match_keyword = unique_list(new_match_keyword)
        return match_keyword
    else:
        match_keyword = []
    return match_keyword

def check_exists_on_match_word_list(response,match_word_list):
    response_list = decode_match_keyword(response)
    for itm in response_list:
        if(itm in match_word_list):
            return False
    return True

def search_here(traffic,track,traffic_data=[]):
    match_word_list = []
    response = CheckLineName(traffic['New_Line_Name'],track['Placement_Name']).find_match()
    if(response['status'] == True and response['match_count'] >=2):
        match_word_list.extend(decode_match_keyword(response))
        response['match_count'] = len(match_word_list)
    if(response['status'] == True and response['match_count'] == 1 and response['algorithm'] != "Exact Match"):
        match_word_list.extend(decode_match_keyword(response))
        re_response = re_search(traffic['New_Line_Name'],track['Placement_Name'])
        if(re_response != False and re_response['status'] == True and check_exists_on_match_word_list(re_response,match_word_list)):
            match_word_list.extend(decode_match_keyword(re_response))
            response = re_response
            response['match_count'] = len(match_word_list)

        if(int(response['match_count']) == 1 or response['status'] == False):
            re_response = check_with_original_line_name(traffic['Original_Line_Name'],track['Placement_Name'],traffic_data)
            if(re_response != False and re_response['status'] == True and check_exists_on_match_word_list(re_response,match_word_list)):
                match_word_list.extend(decode_match_keyword(re_response))
                response = re_response
                response['match_count'] = len(match_word_list)
                
        elif(int(response['match_count']) == 0):
            re_response = check_with_mapped_line_name(traffic['Mapped_Line_Name'],traffic['New_Line_Name'],track['Placement_Name'])
            if(re_response != False and re_response['status'] == True and check_exists_on_match_word_list(re_response,match_word_list)):
                match_word_list.extend(decode_match_keyword(re_response))
                response = re_response
                response['match_count'] = len(match_word_list)
    elif(response['status'] == False):
        # print("Original Line Namr check")
        re_response = check_with_original_line_name(traffic['Original_Line_Name'],track['Placement_Name'],traffic_data)
        if(re_response != False and re_response['status'] == True and check_exists_on_match_word_list(re_response,match_word_list)):
            match_word_list.extend(decode_match_keyword(re_response))
            response = re_response
            response['match_count'] = len(match_word_list)

    if(response['status'] == False):
        re_response = re_three_search(traffic['New_Line_Name'],track['Placement_Name'])
        if(re_response != False and re_response['status'] == True and check_exists_on_match_word_list(re_response,match_word_list)):
            match_word_list.extend(decode_match_keyword(re_response))
            response = re_response
            response['match_count'] = len(match_word_list)

    if(response['status'] == False):
        re_response = check_with_mapped_line_name(traffic['Mapped_Line_Name'],traffic['New_Line_Name'],track['Placement_Name'])
        print(re_response)
        if(re_response != False and re_response.get('status',False) == True and check_exists_on_match_word_list(re_response,match_word_list)):
            match_word_list.extend(decode_match_keyword(re_response))
            response = re_response
            response['match_count'] = len(match_word_list)
    if(len(match_word_list) >= 1):
        response['match_keyword'] = match_word_list
    else:
        response['match_keyword'] = decode_match_keyword(response)
    response['match_keyword'] = ",".join(response['match_keyword']).strip()
    return response


def get_ranked(write_data):
    for itm in write_data:
        filtered_write_data = list(filter(lambda d: d['Original Line Name'] == itm['Original Line Name'], write_data))
        new_filtered_write_data = list(filter(lambda d: d['Status'] == True and d['Count'] >= 2, filtered_write_data))
        if(len(new_filtered_write_data) >= 1):
            if(len(new_filtered_write_data) == 1):
                new_filtered_write_data[0]['Rank'] = 1
            else:
                sorted_list = sorted(new_filtered_write_data, key = itemgetter('Count'),reverse=True)
                # print(sorted_list)
                biggest_count = max([item['Count'] for item in sorted_list])
                for data in sorted_list:
                    if(data['Algorithm'] == 'Mapped Line Name'):
                        priority_status = True
                    else:
                        priority_status = check_priority(data['Match Keyword'],exlusion_list,data['Original Line Name'],mandatory_list)
                    if(priority_status):
                        if(data['Count'] == biggest_count):
                            data['Rank'] = 1
                        else:
                            data['Rank'] = 0
                    else:
                        data['Rank'] = 0
        else:
            new_filtered_write_data = list(filter(lambda d: int(d['Count']) ==1, filtered_write_data))
            match_keyword_list = [item['Match Keyword'] for item in new_filtered_write_data]
            # longest_word = get_longest_word_from_list(match_keyword_list)
            if(len(new_filtered_write_data) >= 1):
                sorted_list = sorted(new_filtered_write_data, key = itemgetter('Count'),reverse=True)
                biggest_count = max([item['Count'] for item in sorted_list])
                for data in sorted_list:
                    if(data['Algorithm'] == 'Mapped Line Name'):
                        priority_status = True
                    else: 
                        priority_status = check_priority(data['Match Keyword'],exlusion_list,data['Original Line Name'],mandatory_list)
                    if(priority_status):
                        if(data['Count'] == biggest_count):
                            line_name_split_status = split_line_name(data['Line Name'])
                            if(line_name_split_status):
                                data['Rank'] = 1
                                data['Status'] = True
                            # elif(data['Match Keyword'] in longest_word):
                            else:
                                # For handling numeric data on matched keyword
                                match_status = True
                                m_split = data['Match Keyword'].split(",")
                                if(len(m_split) == 1):
                                    for i in m_split:
                                        if(i.isnumeric()):
                                            match_status = False
                                            break
                                if(match_status == True):
                                    data['Rank'] = 1
                                    data['Status'] = True
                                    # data['Longest Keyword'] = longest_word
                                else:
                                    data['Rank'] = 0
                                    data['Status'] = False
                                    # data['Longest Keyword'] = longest_word
                        else:
                            data['Rank'] = 0
                            data['Status'] = False
                            # data['Longest Keyword'] = longest_word
                    else:
                        data['Rank'] = 0
                        data['Status'] = False
    return write_data

def custom_remove_common_words(filter_line_name_data,column_name):
    keyword = filter_line_name_data[0][column_name]
    keyword = remove_spcl_characters(keyword).lower().split(" ")
    if(len(keyword) >= 1):
        for word in keyword:
            count = 0
            for line_name in filter_line_name_data:
                if(word in str(line_name[column_name]).lower()):
                    count += 1
            if(count == len(filter_line_name_data)):
                for itm in filter_line_name_data:
                    itm[column_name] = remove_spcl_characters(itm[column_name]).lower().replace(word," ").replace("  "," ").strip()
    return filter_line_name_data

def custom_search_here(traffic,track,traffic_data,traffic_column,track_column):
    match_word_list = []
    response = CheckLineName(traffic[traffic_column],track[track_column]).find_match()
    if(response['status'] == True and response['match_count'] == 1 and response['algorithm'] != "Exact Match"):
        match_word_list.extend(decode_match_keyword(response))
        re_response = re_search(traffic[traffic_column],track[track_column])
        if(re_response != False and re_response['status'] == True and check_exists_on_match_word_list(re_response,match_word_list)):
            match_word_list.extend(decode_match_keyword(re_response))
            response = re_response
            response['match_count'] = len(match_word_list)

    elif(response['status'] == False):
        # print("Original Line Namr check")
        re_response = check_with_original_line_name(traffic[traffic_column],track[track_column],traffic_data)
        if(re_response != False and re_response['status'] == True and check_exists_on_match_word_list(re_response,match_word_list)):
            match_word_list.extend(decode_match_keyword(re_response))
            response = re_response
            response['match_count'] = len(match_word_list)

    if(response['status'] == False):
        re_response = re_three_search(traffic[traffic_column],track[track_column])
        if(re_response != False and re_response['status'] == True and check_exists_on_match_word_list(re_response,match_word_list)):
            match_word_list.extend(decode_match_keyword(re_response))
            response = re_response
            response['match_count'] = len(match_word_list)
   
    if(len(match_word_list) >= 1):
        response['match_keyword'] = match_word_list
    else:
        response['match_keyword'] = decode_match_keyword(response)
    response['match_keyword'] = ",".join(response['match_keyword']).strip()
    return response


def custom_check_present_status(write_data,payload,traffic_column,track_column):
    for item in write_data:
        if(item[traffic_column] == payload[traffic_column] and item[track_column] == payload[track_column]):
            return True
    return False


def custom_get_ranked(write_data,traffic_column_name):
    new_filtered_write_data = list(filter(lambda d: d['Status'] == True and d['Count'] >= 2, write_data))
    if(len(new_filtered_write_data) >= 1):
        if(len(new_filtered_write_data) == 1):
            new_filtered_write_data[0]['Rank'] = 1
        else:
            sorted_list = sorted(new_filtered_write_data, key = itemgetter('Count'),reverse=True)
            biggest_count = max([item['Count'] for item in sorted_list])
            for data in sorted_list:
                if(data['Algorithm'] == 'Mapped Line Name'):
                    priority_status = True
                else:
                    priority_status = check_priority(data['Match Keyword'],exlusion_list,data[traffic_column_name],mandatory_list)
                if(priority_status):
                    if(data['Count'] == biggest_count):
                        data['Rank'] = 1
                    else:
                        data['Rank'] = 0
                else:
                    data['Rank'] = 0
    else:
        new_filtered_write_data = list(filter(lambda d: int(d['Count']) >=1, write_data))
        match_keyword_list = [item['Match Keyword'] for item in new_filtered_write_data]
        # longest_word = get_longest_word_from_list(match_keyword_list)
        if(len(new_filtered_write_data) >= 1):
            sorted_list = sorted(new_filtered_write_data, key = itemgetter('Count'),reverse=True)
            biggest_count = max([item['Count'] for item in sorted_list])
            for data in sorted_list:
                if(data['Algorithm'] == 'Mapped Line Name'):
                    priority_status = True
                else: 
                    priority_status = check_priority(data['Match Keyword'],exlusion_list,data[traffic_column_name],mandatory_list)
                if(priority_status):
                    if(data['Count'] == biggest_count):
                        line_name_split_status = split_line_name(data[traffic_column_name])
                        if(line_name_split_status):
                            data['Rank'] = 1
                            data['Status'] = True
                        # elif(data['Match Keyword'] in longest_word):
                        else:
                                # For handling numeric data on matched keyword
                                match_status = True
                                m_split = data['Match Keyword'].split(",")
                                if(len(m_split) == 1):
                                    for i in m_split:
                                        if(i.isnumeric()):
                                            match_status = True
                                            break
                                if(match_status == True):
                                    data['Rank'] = 1
                                    data['Status'] = True
                                    # data['Longest Keyword'] = longest_word
                                else:
                                    data['Rank'] = 0
                                    data['Status'] = False
                                    # data['Longest Keyword'] = longest_word
                    else:
                        data['Rank'] = 0
                        data['Status'] = False
                        # data['Longest Keyword'] = longest_word
                else:
                    data['Rank'] = 0
                    data['Status'] = False
    return write_data