from transformers import MarianMTModel, MarianTokenizer

""" 
reserved for use in case translate_comment.py shut down 
because request limit provided by googletrans library

here transformer is being used
"""



model_name = "Helsinki-NLP/opus-mt-en-fr"
model = MarianMTModel.from_pretrained(model_name)
tokenizer = MarianTokenizer.from_pretrained(model_name)


def translate(comment):

    if type(comment) == str:
        translated = model.generate(**tokenizer(
            comment,
            return_tensors = "pt",
            padding = True
        ))

        return tokenizer.decode(translated[0], skip_special_tokens = True)
    
    elif type(comment) == list: 
        translated_comments = [] 
        for com in comment:
            translated = model.generate(**tokenizer(
                com,
                return_tensors = "pt",
                padding = True
            ))
            com = tokenizer.decode(translated[0], skip_special_tokens = True)
            translated_comments.append(com)
    
        return translated_comments
    

def get_comments_translation(comments, code_line_split):

    translated_data = []

    for comment in comments:
    
        if comment["type"] == "single line":
            index = comment["line"]
            start_col = comment["start_col"]

            res = translate(code_line_split[index][start_col + 1:])

            comment_slice_1 = code_line_split[index][0:start_col + 1]

            translated_comment = comment_slice_1 + " " + res

            translated_data.append(translated_comment)
            print("if: ", translated_comment)


        elif comment["type"] == "multiline":
            start_index = comment["start"]["line"] + 1
            end_index = comment["end"]["line"]
            start_col = comment["start"]["start_col"]

            res = translate(code_line_split[start_index:end_index])


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

            res = translate(code_line_split[index][start_col:end_col])

            comment_slice_1 = code_line_split[index][start_col:start_col + 3]
            translated_comment = comment_slice_1 + res + code_line_split[end_col]

            translated_data.append(translated_comment)
            print("elif 2: ", translated_comment)

    return translated_data
