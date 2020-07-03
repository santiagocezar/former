import uuid
import re
import mistune
from enum import Enum

tree = {}


class FormRenderer(mistune.HTMLRenderer):
    RADIO = re.compile(r'^\((.*)\) *(.*)')
    CHECKBOX = re.compile(r'^\[ ?\] *(.*)')
    TEXT = re.compile(r'^\[&gt;\] *(.*)')
    
    CURRENT_SECTION = -1
    CURRENT_SECTION_NAME = ''
    CURRENT_ELEMENT = -1

    FLAGS = {}
    
    def heading(self, text, level):
        if level == 2:
            self.CURRENT_SECTION += 1
            self.CURRENT_SECTION_NAME = text
            self.CURRENT_ELEMENT = -1
        return super().heading(text, level)

    def paragraph(self, text: str):
        if text.startswith('::'):
            self.FLAGS[text[2:]] = True
            return ''
        else:
            return super().paragraph(text)

    def list(self, text, ordered, level, start=None):
        if 'buttons' in self.FLAGS and self.FLAGS['buttons']:
            self.FLAGS['buttons'] = False
            return '<ul class="group">\n' + text + '</ul>\n'
        return super().list(text, ordered, level, start)

    def list_item(self, text, level):
        global tree
        id = uuid.uuid1()

        el = {
            'section': self.CURRENT_SECTION_NAME,
            'type': '',
            'name': ''
        }

        self.CURRENT_ELEMENT += 1
        name = f'{self.CURRENT_SECTION}:{self.CURRENT_ELEMENT}'
        
        re_radio = self.RADIO.match(text)
        re_checkbox = self.CHECKBOX.match(text)
        re_text = self.TEXT.match(text)

        html = ''

        if re_radio is not None:
            
            value = re_radio[1]
            label = re_radio[2]
            if value == '' or value == ' ':
                value = label

            el['type'] = 'radio'
            el['name'] = label

            html = (
                f'<label radio for="{id}">'
                f'<input type="radio" name="{name}" id="{id}" value="{value}">'
                f'<span>{label}</span>'
                f'</label>\n'
            )

        elif re_checkbox is not None:
            label = re_checkbox[1]
            
            el['type'] = 'checkbox'
            el['name'] = label

            html = (
                f'<label check for="{id}">'
                f'<input type="checkbox" name="{name}" id="{id}" value="yes">'
                f'<span>{label}</span>'
                f'</label>\n'
            )
        elif re_text is not None:
            label = re_text[1]

            el['type'] = 'text'
            el['name'] = label
            
            html = f'<input type="text" name="{name}" id="{id}" placeholder="{label}"><br>'
        else:
            self.CURRENT_ELEMENT -= 1
            html = super().list_item(text, level)

        tree[name] = el

        return html

_markdown = mistune.create_markdown(True, renderer=FormRenderer())

_template = """
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Encuesta</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;900&display=swap" rel="stylesheet"> 
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <img src="logo.svg" alt="logo" width="48" id="logo">
    <main>
        <form action="{}" method="post" accept-charset="utf-8">
            {}
            <input type="submit" value="Enviar">
        </form>
    </main>
</body>
</html>
"""

def build(post_url, file):
    with open(file) as f:
        formbody = _markdown(f.read())
        return _template.format(post_url, formbody)
