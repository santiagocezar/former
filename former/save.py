import json
from former.formrender import tree

def parse(text: dict):
    answers = dict(tree)
    for k in text.keys():
        if k in answers:
            if answers[k]['type'] == 'text':
                answers[k]['input'] = text[k]
            else:
                answers[k]['input'] = True
    print(json.dumps(answers))
