import gc

gc.collect()
ENCODING = 'utf-8'
try:
    print('Running MicroPython')
    import usocket
    import ussl


    class SocketInterface:
        def __init__(self, sock):
            self._sock = sock

        def settimeout(self, value):
            return self._sock.settimeout(value)

        def write(self, data: bytes):
            # print(data)
            self._sock.write(data)

        def read(self, size=None):
            return self._sock.read() if size is None else self._sock.read(size)

        def readline(self):
            return self._sock.readline()

        def close(self):
            self._sock.close()

except ModuleNotFoundError as e:
    print('Base Python Implementation')
    import socket as usocket
    import ssl

    ussl = ssl.create_default_context()


    class SocketInterface:
        def __init__(self, sock):
            self._sock = sock

        def settimeout(self, value):
            return self._sock.settimeout(value)

        def write(self, data: bytes):
            # print(data)
            self._sock.send(data)

        def read(self, size=None):
            size = 1024 if size is None else size
            buff = b''
            while len(buff) < size:
                buff += self._sock.recv(1)
            return buff

        def readline(self):
            buff = b''
            while True:
                buff += self._sock.recv(1)
                if buff.endswith(b'\r\n'):
                    break
            return buff

        def close(self):
            self._sock.close()

types_map = {
    '.js': 'application/javascript',
    '.mjs': 'application/javascript',
    '.json': 'application/json',
    '.webmanifest': 'application/manifest+json',
    '.doc': 'application/msword',
    '.dot': 'application/msword',
    '.wiz': 'application/msword',
    '.bin': 'application/octet-stream',
    '.a': 'application/octet-stream',
    '.dll': 'application/octet-stream',
    '.exe': 'application/octet-stream',
    '.o': 'application/octet-stream',
    '.obj': 'application/octet-stream',
    '.so': 'application/octet-stream',
    '.oda': 'application/oda',
    '.pdf': 'application/pdf',
    '.p7c': 'application/pkcs7-mime',
    '.ps': 'application/postscript',
    '.ai': 'application/postscript',
    '.eps': 'application/postscript',
    '.m3u': 'application/vnd.apple.mpegurl',
    '.m3u8': 'application/vnd.apple.mpegurl',
    '.xls': 'application/vnd.ms-excel',
    '.xlb': 'application/vnd.ms-excel',
    '.ppt': 'application/vnd.ms-powerpoint',
    '.pot': 'application/vnd.ms-powerpoint',
    '.ppa': 'application/vnd.ms-powerpoint',
    '.pps': 'application/vnd.ms-powerpoint',
    '.pwz': 'application/vnd.ms-powerpoint',
    '.wasm': 'application/wasm',
    '.bcpio': 'application/x-bcpio',
    '.cpio': 'application/x-cpio',
    '.csh': 'application/x-csh',
    '.dvi': 'application/x-dvi',
    '.gtar': 'application/x-gtar',
    '.hdf': 'application/x-hdf',
    '.h5': 'application/x-hdf5',
    '.latex': 'application/x-latex',
    '.mif': 'application/x-mif',
    '.cdf': 'application/x-netcdf',
    '.nc': 'application/x-netcdf',
    '.p12': 'application/x-pkcs12',
    '.pfx': 'application/x-pkcs12',
    '.ram': 'application/x-pn-realaudio',
    '.pyc': 'application/x-python-code',
    '.pyo': 'application/x-python-code',
    '.sh': 'application/x-sh',
    '.shar': 'application/x-shar',
    '.swf': 'application/x-shockwave-flash',
    '.sv4cpio': 'application/x-sv4cpio',
    '.sv4crc': 'application/x-sv4crc',
    '.tar': 'application/x-tar',
    '.tcl': 'application/x-tcl',
    '.tex': 'application/x-tex',
    '.texi': 'application/x-texinfo',
    '.texinfo': 'application/x-texinfo',
    '.roff': 'application/x-troff',
    '.t': 'application/x-troff',
    '.tr': 'application/x-troff',
    '.man': 'application/x-troff-man',
    '.me': 'application/x-troff-me',
    '.ms': 'application/x-troff-ms',
    '.ustar': 'application/x-ustar',
    '.src': 'application/x-wais-source',
    '.xsl': 'application/xml',
    '.rdf': 'application/xml',
    '.wsdl': 'application/xml',
    '.xpdl': 'application/xml',
    '.zip': 'application/zip',
    '.3gp': 'audio/3gpp',
    '.3gpp': 'audio/3gpp',
    '.3g2': 'audio/3gpp2',
    '.3gpp2': 'audio/3gpp2',
    '.aac': 'audio/aac',
    '.adts': 'audio/aac',
    '.loas': 'audio/aac',
    '.ass': 'audio/aac',
    '.au': 'audio/basic',
    '.snd': 'audio/basic',
    '.mp3': 'audio/mpeg',
    '.mp2': 'audio/mpeg',
    '.opus': 'audio/opus',
    '.aif': 'audio/x-aiff',
    '.aifc': 'audio/x-aiff',
    '.aiff': 'audio/x-aiff',
    '.ra': 'audio/x-pn-realaudio',
    '.wav': 'audio/x-wav',
    '.bmp': 'image/bmp',
    '.gif': 'image/gif',
    '.ief': 'image/ief',
    '.jpg': 'image/jpeg',
    '.jpe': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.heic': 'image/heic',
    '.heif': 'image/heif',
    '.png': 'image/png',
    '.svg': 'image/svg+xml',
    '.tiff': 'image/tiff',
    '.tif': 'image/tiff',
    '.ico': 'image/vnd.microsoft.icon',
    '.ras': 'image/x-cmu-raster',
    '.pnm': 'image/x-portable-anymap',
    '.pbm': 'image/x-portable-bitmap',
    '.pgm': 'image/x-portable-graymap',
    '.ppm': 'image/x-portable-pixmap',
    '.rgb': 'image/x-rgb',
    '.xbm': 'image/x-xbitmap',
    '.xpm': 'image/x-xpixmap',
    '.xwd': 'image/x-xwindowdump',
    '.eml': 'message/rfc822',
    '.mht': 'message/rfc822',
    '.mhtml': 'message/rfc822',
    '.nws': 'message/rfc822',
    '.css': 'text/css',
    '.csv': 'text/csv',
    '.html': 'text/html',
    '.htm': 'text/html',
    '.txt': 'text/plain',
    '.bat': 'text/plain',
    '.c': 'text/plain',
    '.h': 'text/plain',
    '.ksh': 'text/plain',
    '.pl': 'text/plain',
    '.rtx': 'text/richtext',
    '.tsv': 'text/tab-separated-values',
    '.py': 'text/x-python',
    '.etx': 'text/x-setext',
    '.sgm': 'text/x-sgml',
    '.sgml': 'text/x-sgml',
    '.vcf': 'text/x-vcard',
    '.xml': 'text/xml',
    '.mp4': 'video/mp4',
    '.mpeg': 'video/mpeg',
    '.m1v': 'video/mpeg',
    '.mpa': 'video/mpeg',
    '.mpe': 'video/mpeg',
    '.mpg': 'video/mpeg',
    '.mov': 'video/quicktime',
    '.qt': 'video/quicktime',
    '.webm': 'video/webm',
    '.avi': 'video/x-msvideo',
    '.movie': 'video/x-sgi-movie',
}


def random_string(length: int):
    import random
    numbers = '0123456789'
    letters_lower = 'abcdefghijklmnopqrstuvwxyz'
    letters_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.choice(numbers + letters_upper + letters_lower) for _ in range(length))


class HttpResponse:
    def __init__(self, sock, save_to_file: str = None):
        self._save_to_file = save_to_file
        self._json = None
        self._sock = sock
        self.encoding = ENCODING
        self.http_ver, self.status_code, self.status_text = sock.readline().decode(self.encoding).split(' ', 2)
        self.headers = self.build_headers_dict()
        if self.headers.get('Transfer-Encoding') == 'chunked':
            if self._save_to_file is not None:
                self.save_chunks_to_file(self._save_to_file)
            else:
                self._content = self._read_chunks_into_memory()
        elif self.headers.get('Content-Length') is not None:
            if self._save_to_file is not None:
                self.save_content_to_file(self._save_to_file)
            else:
                self._content = self._sock.read(int(self.headers.get('Content-Length')))
        self._sock.close()

    def _read_chunk(self):
        chunk_len_hex = self._sock.readline().decode(self.encoding).strip()  # First Line is chunk size in HEX
        chunk_len_dec = int(chunk_len_hex, 16)
        print(f'Chunk Length: {chunk_len_dec}')
        if chunk_len_dec == 0:
            return None
        chunk = self._sock.read(size=chunk_len_dec)
        if not self._sock.readline() == b'\r\n':
            raise ValueError('End of Chunk not detected.')
        return chunk

    def _read_chunks_into_memory(self):
        chunks = b''
        while True:
            chunk = self._read_chunk()
            if chunk is None:
                break
            chunks += chunk
            print(f'Chunk: {chunk} | Len {len(chunk)}')
        return chunks

    def save_chunks_to_file(self, file_name: str):
        with open(file_name, 'wb') as outfile:
            while True:
                chunk = self._read_chunk()
                if chunk is None:
                    break
                outfile.write(chunk)

    def save_content_to_file(self, file_name: str):
        with open(file_name, 'wb') as outfile:
            data = self._sock.read(int(self.headers.get('Content-Length')))
            outfile.write(data)

    def build_headers_dict(self) -> dict:
        headers = {}
        while True:
            line = self._sock.readline()
            if not line or line == b'\r\n':
                break
            header, header_val = line.decode(self.encoding).strip().split(': ', 1)
            headers[header] = header_val
        return headers

    @property
    def text(self):
        try:
            return self._content.decode(self.encoding)
        except UnicodeError as e:
            return self._content
        except AttributeError as e:
            print(f'Content saved to file: {self._save_to_file} and not stored in memory')

    @property
    def json(self):
        if self._json is None:
            import json
            self._json = json.loads(self._content)
        return self._json


class HttpBody:
    def send_body(self, sock):
        raise NotImplementedError


class HttpBodyEmpty(HttpBody):
    def send_body(self, sock):
        sock.write(b"\r\n")


class HttpBodyJSON(HttpBody):
    def __init__(self, json_data: dict):
        import json
        self._json_data: dict = json_data
        self._json_bytes_str: bytes = json.dumps(self._json_data).encode(ENCODING)
        self.content_len = len(self._json_bytes_str)

    def send_body(self, sock):
        sock.write(b'Content-Type: application/json\r\n')
        sock.write(b"Content-Length: %d\r\n" % self.content_len)
        sock.write(b"\r\n")
        sock.write(self._json_bytes_str)


class HttpBodyForm(HttpBody):
    def __init__(self, form_data: dict):
        self._form_data = form_data
        self._form_url_encoded = '&'.join(['='.join([str(k), str(v)]) for k, v in self._form_data.items()]).encode(
            ENCODING)
        self.content_len = len(self._form_url_encoded)

    def send_body(self, sock):
        sock.write(b'Content-Type: application/x-www-form-urlencoded\r\n')
        sock.write(b"Content-Length: %d\r\n" % self.content_len)
        sock.write(b"\r\n")
        sock.write(self._form_url_encoded)


class HttpBodyFile(HttpBody):
    def __init__(self, file_name: str):
        self._file_name = file_name
        self._name, self._ext = self._file_name.split('.')
        self._name = self._name.encode(ENCODING)
        self._ext = ('.' + self._ext).encode(ENCODING)
        with open(self._file_name, 'rb') as file:
            self._file_data_bytes = file.read()
        self.content_len = len(self._file_data_bytes)

    def send_body(self, sock):
        sock.write(b"Content-Length: %d\r\n" % self.content_len)
        sock.write(b'Content-Type: %s\r\n' % types_map[self._ext.decode(ENCODING)].encode(ENCODING))
        sock.write(b"\r\n")
        sock.write(self._file_data_bytes)


class HttpBodyMultiFileSection:
    def __init__(self, name: str, file_path: str = None, value=None):
        self._name = name
        if value is not None:
            self._file_path = None
            self._file_ext = None
            self._file_name = None
        elif file_path is not None:
            self._file_path = file_path
            self._file_ext = file_path.split('.')[-1]
            self._file_name = self._name + self._file_ext
        else:
            raise ValueError(f'HttpBodyMultiFile must either be passed a value or filepath argument.')
        self._value = b'' if value is None else value.encode(ENCODING)

    def _read_file(self):
        try:
            with open(self._file_path, 'rb') as reader:
                data_bytes = reader.read()
            return data_bytes
        except OSError:
            print('OS Error while accessing file - Ensure file exists.')
            return b''

    def build_section(self, boundary, is_first=False, last_section=False):
        data_bytes = self._read_file() if self._file_ext is not None else self._value

        start = b'--%s\r\n' % boundary if is_first else b''
        end = b'--%s--\r\n' % boundary if last_section else b'--%s\r\n' % boundary

        name = b' name="%s";' % self._name.encode(ENCODING)
        file_name = b' filename="%s"' % self._file_name.encode(ENCODING) if self._file_ext is not None else b''
        section = [start, b'Content-Disposition: form-data;', name, file_name, b'\r\n',
                   b'Content-Type: %s\r\n\r\n' % types_map.get(self._file_ext, 'text/plain').encode(
                       ENCODING),
                   data_bytes, b'\r\n', end]
        return section, sum(len(item) for item in section)


class HttpBodyMultiFile(HttpBody):
    '''
     HTTP Multipart accepts a list of body sections with will then be combined and sent.

     Notes:
         This body type should be avoided as it loads several files into memory. Chunked data should be used instead.
    '''

    def __init__(self, http_body_sections: list):
        self._http_body_sections = http_body_sections
        self._boundary = random_string(20).encode(ENCODING)
        self.content, self.content_len = self.generate_content()

    def generate_content(self) -> (list, int):
        complete_content = []
        total_size = 0
        for index, section in enumerate(self._http_body_sections):
            is_last = index == len(self._http_body_sections) - 1
            is_first = index == 0
            content, size = section.build_section(self._boundary, is_first=is_first, last_section=is_last)
            complete_content += content
            total_size += size
        return complete_content, total_size

    def send_body(self, sock):
        sock.write(b'Content-Type: multipart/form-data; boundary=%s\r\n' % self._boundary)
        sock.write(b"Content-Length: %d\r\n" % self.content_len)
        sock.write(b'\r\n')
        for line in self.content:
            sock.write(line)


class HttpBodyChunked(HttpBody):
    def __init__(self, file_name: str, chunk_size: int = 512):
        self._file_name = file_name
        _, self._file_ext = file_name.split('.')
        self._file_ext = f'.{self._file_ext}'
        self._chunk_size = chunk_size

    def send_body(self, sock):
        sock.write(b"Transfer-Encoding: chunked\r\n")
        sock.write(b'Content-Type: %s\r\n' % types_map.get(self._file_ext, 'text/plain').encode(
            ENCODING))
        sock.write(b'\r\n')
        with open(self._file_name, 'rb') as reader:
            while True:
                chunk = reader.read(self._chunk_size)
                if len(chunk) == 0:
                    break
                sock.write(b"%x\r\n" % len(chunk))
                sock.write(chunk)
                sock.write(b"\r\n")
        sock.write(b"0\r\n\r\n")


class HttpRequest:
    def __init__(self, url: str, port: int = None, method: str = 'GET', custom_headers: dict = None,
                 body: HttpBody = None, save_to_file: str = None):
        self._proto, _dummy, self._host, self._path = self.url_parse(url)
        self._host, self._port = self._parse_port(self._host, self._proto) if port is None else (self._host, port)

        self._method = method
        self._custom_headers = custom_headers
        self._body: HttpBody = HttpBodyEmpty() if body is None else body
        # Move to Bytes instead of Strings
        self._proto, self._host, self._path, self._method = self._bulk_encode(self._proto, self._host, self._path,
                                                                              self._method)
        self._save_to_file = save_to_file
        self.response = self.request()

    @staticmethod
    def _bulk_encode(*args):
        return map(lambda x: x.encode(ENCODING), args)

    @staticmethod
    def _protocol_port_select(proto):
        if proto == 'http:':
            return 80
        elif proto == 'https:':
            return 443
        raise ValueError(f'Unsupported protocol: {proto}')

    @classmethod
    def _parse_port(cls, host, proto):
        if ':' in host:
            host, port = host.split(':', 1)
            return host, int(port)
        return host, cls._protocol_port_select(proto)

    @staticmethod
    def url_parse(url: str) -> (str, str, str, str):
        try:
            return tuple(url.split('/', 3))
        except ValueError:
            return tuple(url.split('/', 2)) + ('',)

    def _send_custom_headers(self, sock):
        if self._custom_headers is None:
            return
        for key, value in self._custom_headers.items():
            sock.write('{}: {}\r\n'.format(key, value).encode(ENCODING))

    def _send_headers(self, sock):
        sock.write(b'%s /%s HTTP/1.1\r\n' % (self._method, self._path))
        sock.write(b'Host: %s\r\n' % self._host)
        self._send_custom_headers(sock)
        sock.write(b'User-Agent: MicroPython Client\r\n')

    def _create_socket(self):
        self._host = b'127.0.0.1' if self._host == b'localhost' else self._host
        address_info = usocket.getaddrinfo(self._host, self._port, 0, usocket.SOCK_STREAM)
        if len(address_info) < 1:
            raise ValueError('You are not connected to the internet...')
        address_info = address_info[0]
        # print(f'Address Info: {address_info}')
        return usocket.socket(address_info[0], address_info[1], address_info[2]), address_info

    def request(self):
        sock, address_info = self._create_socket()
        sock.settimeout(2)
        print(f"Address Info: {address_info[-1]}")
        sock.connect(address_info[-1])
        if self._port == 443:
            sock = ussl.wrap_socket(sock, server_hostname=self._host)
        sock = SocketInterface(sock)
        self._send_headers(sock)
        self._body.send_body(sock)
        gc.collect()
        resp = HttpResponse(sock, save_to_file=self._save_to_file)
        return resp


def request(url: str, port: int = None, method: str = 'GET', data=None, json=None, file=None, custom_headers=None,
            save_to_file: str = None):
    if data is not None:
        http_body = HttpBodyForm(form_data=data)
    elif json is not None:
        http_body = HttpBodyJSON(json_data=json)
    elif file is not None:
        http_body = HttpBodyFile(file_name=file)
    else:
        http_body = HttpBodyEmpty()
    http_request = HttpRequest(url, port=port, custom_headers=custom_headers, method=method,
                               save_to_file=save_to_file, body=http_body)
    return http_request.response


def get(url, **kw):
    return request(url, method='GET', **kw)


def post(url, **kw):
    return request(url, method='POST', **kw)


def put(url, **kw):
    return request(url, method='PUT', **kw)


def patch(url, **kw):
    return request(url, method='PATCH', **kw)


def delete(url, **kw):
    return request(url, method='DELETE', **kw)
