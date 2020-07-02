from flask import Flask, request
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

import former.formrender as formrender
import time

app = Flask(__name__, static_url_path='', static_folder='static')

document = ''

class SourceEventHandler(FileSystemEventHandler):
    def __init__(self, post_url, src_file):
        self.post = post_url
        self.src = src_file

    def on_modified(self, event: FileModifiedEvent):
        global document
        document = formrender.build(self.post, self.src)

@app.route('/')
def index():
    return document

@app.route('/post', methods=['POST'])
def post():
    print(request.form)
    print(formrender.tree)
    return 'ok'

def run(post_url, src_file):
    global document
    document = formrender.build(post_url, src_file) 

    handler = SourceEventHandler(post_url, src_file)
    observer = Observer()
    observer.schedule(handler, src_file)
    observer.start()

    app.run()
    observer.stop()
    observer.join()
