import os
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
import subprocess
class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type="text/html"):
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.end_headers()
    def _send_html_response(self, html_content):
        self._set_headers(content_type="text/html")
        self.wfile.write(html_content.encode("utf-8"))
    def do_GET(self):
        try:
            base_path = os.path.abspath("/")
            decoded_path = unquote(self.path)
            file_path = os.path.abspath(os.path.join(base_path, decoded_path[1:]))
            if not file_path.startswith(base_path):
                raise PermissionError("403 Forbidden")
            if self.path == "/":
                self._serve_directory_listing(file_path)
            else:
                if os.path.exists(file_path):
                    if os.path.isdir(file_path):
                        self._serve_directory_listing(file_path)
                    else:
                        self._serve_file(file_path)
                else:
                    self.send_error(404)  # Send the default error message for 404 Not Found
        except PermissionError as e:
            self.send_error(403, str(e))
        except Exception as e:
            self.send_error(500, str(e))
    def _serve_directory_listing(self, directory):
        files = os.listdir(directory)
        file_list = "<ul>"
        for file_name in files:
            full_path = os.path.join(directory, file_name)
            if os.path.isdir(full_path):
                file_list += f"<li><a href='{file_name}/'>{file_name}/</a></li>"
            else:
                file_list += f"<li><a href='{file_name}'>{file_name}</a></li>"
        file_list += "</ul>"
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <title>File Viewer</title>
        </head>
        <body>
        <h1>File Viewer</h1>
        {file_list}
        </body>
        </html>
        """
        self._send_html_response(html)
    def _serve_file(self, file_path):
        content_type, _ = mimetypes.guess_type(file_path)
        self._set_headers(content_type=content_type)
        with open(file_path, "rb") as file:
            self.wfile.write(file.read())
    def send_error(self, code, message=None):
        # Override the default error handling to send a custom error message
        self._set_headers(code, "text/html")
        error_message = """
            <!DOCTYPE html>
            <html>
            <head>
            <title>Error</title>
            </head>
            <body>
            <h1>{}</h1>
            </body>
            </html>
            """.format(code)
        self.wfile.write(error_message.encode("utf-8"))
class Server(HTTPServer):
    def __init__(self, address, handler):
        super().__init__(address, handler)
    def handle_error(self, request, client_address):
        # Override the default error handling to avoid unwanted noise in the console
        pass
def get_ip_address():
    command = "ifconfig en0 | grep 'inet ' | awk '{print $2}'"
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    return output.strip()
def run_server(server_class=Server, handler_class=RequestHandler, port=80):
    try:
        server_address = ("", port)
        httpd = server_class(server_address, handler_class)
        print("start on http://{}".format(get_ip_address()))
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print("stop")
run_server()
