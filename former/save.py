from yaml import dump
from uuid import uuid1
import os

home = os.environ['HOME']

class InvalidResponse(Exception):
    def __init__(self, where, message):
        self.where = where
        self.message = message


def parse(file, base: dict, form: dict):
    answers = dict(base)
    for k in form:
        try:
            nk = int(k.split(':')[0])
        except (ValueError, TypeError):
            raise InvalidResponse(f'pregunta {k}', 'NAN')
        try:
            title = answers['questions'][nk]['title']
        except (KeyError):
            raise InvalidResponse(f'pregunta {k}', 'Esa pregunta no existe')
        
        q = answers['questions'][nk]

        if ':' in k:
            if q['type'] != 'checkbox':
                raise InvalidResponse(title, 'No era multiple choice')
            if 'answer' in q and type(q['answer']) is list:
                q['answer'].append(form[k])
            else:
                q['answer'] = [form[k]]
        else:
            q['answer'] = form[k]
            
    path = f'{home}/.former/{file}_answers'
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.isdir(path):
        os.remove(path)
        os.mkdir(path)
            
    with open(f'{path}/{uuid1()}.yml', 'w') as f:
        f.write(dump(answers))
        
