from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO
from jinja2 import Environment, FileSystemLoader

from search.searcher import Searcher

env = Environment(loader=FileSystemLoader('templates'))
searcher = Searcher()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        template = env.get_template('search.html')
        self.wfile.write(template.render().encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        query = self.rfile.read(content_length).decode('utf-8').split('=')[1]
        print(query)
        result = searcher.search(query)
        self.send_response(200)
        self.end_headers()
        template = env.get_template('search.html')
        self.wfile.write(template.render(result=result).encode('utf-8'))


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()