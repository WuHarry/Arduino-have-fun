import BaseHTTPServer

callback = None

class AjaxHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		contenttype = callback(self.path)
		self.send_response(200)
		self.send_header("Content-type", contenttype[1])
		self.end_headers()
		self.wfile.write(contenttype[0])