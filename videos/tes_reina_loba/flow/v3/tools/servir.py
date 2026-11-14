# servidor local de solo lectura con CORS para pegar ingredientes en Flow
import http.server, os, sys
R=os.path.abspath(sys.argv[1]) if len(sys.argv)>1 else os.getcwd()
class H(http.server.SimpleHTTPRequestHandler):
    timeout = 20
    def __init__(s,*a,**k): super().__init__(*a,directory=R,**k)
    def end_headers(s):
        s.send_header('Access-Control-Allow-Origin','*'); s.send_header('Access-Control-Allow-Private-Network','true'); s.send_header('Cache-Control','no-store'); super().end_headers()
    def do_OPTIONS(s): s.send_response(204); s.send_header('Access-Control-Allow-Methods','GET, POST'); s.send_header('Access-Control-Allow-Headers','*'); s.end_headers()
    def do_POST(s):
        import re
        n=re.sub(r'[^A-Za-z0-9_.-]','',s.path.split('/')[-1]); L=int(s.headers.get('Content-Length',0)); b=s.rfile.read(L)
        os.makedirs(os.path.join(R,'flow/v3/crudo'),exist_ok=True)
        open(os.path.join(R,'flow/v3/crudo',n),'wb').write(b)
        s.send_response(200); s.end_headers(); s.wfile.write(str(len(b)).encode())
    def log_message(s,*a): pass
http.server.ThreadingHTTPServer(('127.0.0.1',8793),H).serve_forever()
