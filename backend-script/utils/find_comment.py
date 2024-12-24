
# specify that there is presence of quotes in the line 
def look_for_quotes(data): 
    quotes_index_list = []
    for i in range(0, len(data)):
        if data[i] == "\"" or data[i] == "\'":
            quotes_index_list.append(i)
    
    return quotes_index_list


def find_comment(data):
    comments_data = []
    count = 0

    for i in range(0, len(data)):
        if "#" in data[i] or "//" in data[i]: # checking if there is a possibility that the line is a comment
            count += 1
            #k = 0
            dict_data = {} # outer dict
            dict_details = {} # inner dict/nested dict

            quotes_index_list = look_for_quotes(data[i])

            for j in range(0, len(data[i])): # looping through a line for find position detail of comments identifier
                if data[i][j] == "#" or data[i][j] == "/" and data[i][j+1] == "/":
                    if (len(quotes_index_list) > 0 and (j < quotes_index_list[0] or j > quotes_index_list[1])) or len(quotes_index_list) == 0:
                        dict_details["line"] = i
                        dict_details["col-1"] = j
                        dict_details["col-2"] = len(data[i]) - 1
                #k += 1

            if len(dict_details) != 0:
                dict_data["id"] = count 
                dict_data["details"] = dict_details 
                comments_data.append(dict_data)
    
    return comments_data

