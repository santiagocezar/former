import json
import uuid
from yaml import load, Loader

template = """
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Encuesta</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;900&display=swap" rel="stylesheet"> 
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <img src="/static/logo.svg" alt="logo" width="48" id="logo">
    <h1>{}</h1>
    <main>
        <form method="post" accept-charset="utf-8">
            {}
            <input type="submit" value="Enviar">
        </form>
    </main>
</body>
</html>
"""


def parse(src: str) -> (dict, str):
    with open(src) as f:
        form = load(f, Loader=Loader)
    body = ""

    if not ('title' in form and 'questions' in form):
        raise KeyError
    
    section = 0
    for q in form['questions']:
        title = q['title']
        info = q['info']

        if section != 0:
            body += '<hr>'
        
        body += f'<h2>{title}</h2>'
        body += f'<p>{info}</p>'
        if q['type'] == 'text':
            label = q['label']
            body += f'<input type="text" name="{section}" placeholder="{label}"><br>'
        else:
            n = 0
            if q['type'] == 'buttongroup': body += '<ul class="group">'
            for o in q['opts']:
                id = uuid.uuid1()
                if q['type'] == 'radio' or q['type'] == 'buttongroup':
                    body += (
                        f'<label radio for="{id}">'
                        f'<input type="radio" name="{section}" id="{id}" value="{o}">'
                        f'<span>{o}</span>'
                        f'</label>\n'
                    )
                if q['type'] == 'checkbox':
                    print(q['type'])
                    body += (
                        f'<label check for="{id}">'
                        f'<input type="checkbox" name="{section}:{n}" id="{id}" value="{o}">'
                        f'<span>{o}</span>'
                        f'</label>\n'
                    )
                n += 1
            if q['type'] == 'buttongroup': body += '</ul>'

        section += 1


    return (form, template.format(form['title'], body))