import asyncio 
from googletrans import Translator



async def translate_line(comment, **kwargs):
    """  
    translate a line code from a code split into line list data
    args: comment, **kwargs
    return: translated line or translated line list
    """

    translator = Translator()

    if type(comment) == str:
        translated_comment = await translator.translate(comment, dest = "fr")

        return translated_comment.text
    
    elif type(comment) == list: 
        translated_comments = [] 
        for com in comment:
            translated_com = await translator.translate(com, dest = "fr")
            translated_comments.append(translated_com.text)
    
        return translated_comments


def get_comments_translation(comments, code_line_split):

    translated_data = []

    for comment in comments:
    
        if comment["type"] == "single line":
            index = comment["line"]
            start_col = comment["start_col"]

            res = asyncio.run(translate_line(code_line_split[index][start_col + 1:]))

            comment_slice_1 = code_line_split[index][0:start_col + 1]

            translated_comment = comment_slice_1 + " " + res

            translated_data.append(translated_comment)


        elif comment["type"] == "multiline":
            start_index = comment["start"]["line"] + 1
            end_index = comment["end"]["line"]
            start_col = comment["start"]["start_col"]

            res = asyncio.run(translate_line(code_line_split[start_index:end_index]))

            for i, r in enumerate(res):
                if i == 0:
                    translated_data.append(code_line_split[start_index - 1])
                    translated_data.append(r)
                elif i == len(res) - 1:
                    translated_data.append(r)
                    translated_data.append(code_line_split[end_index])
                else:
                    translated_data.append(r)


        elif comment["type"] == "inline":
            index = comment["line"]
            start_col = comment["start_col"]
            end_col = comment["end_col"]

            res = asyncio.run(translate_line(code_line_split[index][start_col:end_col]))

            comment_slice_1 = code_line_split[index][start_col:start_col + 3]
            translated_comment = comment_slice_1 + res + code_line_split[end_col]

            translated_data.append(translated_comment)

    return translated_data
