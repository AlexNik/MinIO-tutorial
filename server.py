import http.server
import socketserver
import os
from minio import Minio

PORT = 8080

remote_url = os.getenv('REMOTE_URL')
minio_host = os.getenv('MINIO_HOST')
minio_port = os.getenv('MINIO_PORT')
minio_url = f'{minio_host}:{minio_port}'

minio_user = os.getenv('MINIO_USER')
minio_password = os.getenv('MINIO_PASSWORD')

bucket_name = 'uploads'

client = Minio(
    minio_url,
    access_key=minio_user,
    secret_key=minio_password,
    secure=False
)

if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if '/presignedUrl' in self.path:
            self.send_response(200, 'OK')
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            filename = self.path.split('=')[1]
            original_minio_str = client.presigned_put_object(bucket_name, filename)
            fixed_minio_str = original_minio_str.replace(minio_url, remote_url)
            self.wfile.write(str.encode(fixed_minio_str))

            return
        elif '/files' in self.path:
            self.send_response(200, 'OK')
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            files = list(client.list_objects(bucket_name, recursive=True))
            files_str = '<br>'.join(
                [f'<p>{file.object_name} &emsp; {client.stat_object(bucket_name, file.object_name).metadata}</p>' for
                 file in files])

            self.wfile.write(str.encode(files_str))

            return
        else:
            with open('index.html', 'r') as web_page_file:
                web_page = web_page_file.read()

            self.send_response(200, 'OK')
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(str.encode(web_page))

            return


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
