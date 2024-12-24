

def line_split(text):
    index1 = 0
    index2 = 0

    line_split_data = []

    for i in range(0, len(text)):
        if text[i] == "\n" and i == 0:
            pass
        elif text[i] == "\n" and i != 0:
            index2 = i + 1
            line_data = text[index1:index2]
            if len(line_data) > 1:
                line_data = line_data.replace("\n", "")
            line_split_data.append(line_data)
            index1 = i
    
    return line_split_data

    """ 
    text.strip().split("\n") could have worked
    """