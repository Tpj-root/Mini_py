import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import cgi

UPLOAD_DIR = "uploads"

class FileUploadHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/upload':
            content_type, pdict = cgi.parse_header(self.headers['Content-Type'])
            if content_type == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})

                file_item = form['file']
                if file_item.filename:
                    os.makedirs(UPLOAD_DIR, exist_ok=True)
                    file_path = os.path.join(UPLOAD_DIR, os.path.basename(file_item.filename))
                    with open(file_path, 'wb') as f:
                        f.write(file_item.file.read())
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"File uploaded successfully!")
                    return
        
        self.send_response(400)
        self.end_headers()
        self.wfile.write(b"Failed to upload file.")

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <body>
                    <h2>Upload a File</h2>
                    <form action="/upload" method="post" enctype="multipart/form-data">
                        <input type="file" name="file">
                        <input type="submit" value="Upload">
                    </form>
                </body>
                </html>
            """)
        else:
            super().do_GET()

if __name__ == "__main__":
    server_address = ("", 8000)  # Runs on http://localhost:8000
    httpd = HTTPServer(server_address, FileUploadHandler)
    print("Serving at http://localhost:8000")
    httpd.serve_forever()
