import json
import time

from uhttp import requests
from uuid import uuid4
from flask import Flask, jsonify, request
from werkzeug.datastructures import EnvironHeaders, Headers
from threading import Thread
import pytest
import base64
import os


class MockServer:
    '''
    Create a mock flask server that we can send requests to and verify the format headers, data etc.

    '''

    def __init__(self, port=5000):
        self.port = port
        self.app = Flask(__name__)
        self.url = "http://localhost:%s" % self.port

    def start(self):
        server_thread = Thread(target=self.app.run, kwargs={'port': self.port}, daemon=True)
        server_thread.start()

    def add_callback_response(self, url, callback, methods=('GET',)):
        callback.__name__ = str(uuid4())  # change name of method to mitigate flask exception
        self.app.add_url_rule(url, view_func=callback, methods=methods)

    def add_json_response(self, url, serializable, methods=('GET',)):
        def callback():
            return jsonify(serializable)

        self.add_callback_response(url, callback, methods=methods)


@pytest.fixture(scope='session')
def mock_server(request):
    server = MockServer()
    server.start()
    yield server


@pytest.fixture(scope='session')
def image_file_bytes() -> bytes:
    with open('tests/static/image.png', 'rb') as reader:
        image_file_bytes: bytes = reader.read()
    return image_file_bytes


@pytest.fixture(scope='session')
def index_file_bytes() -> bytes:
    with open('tests/static/index.html', 'rb') as reader:
        index_file_bytes: bytes = reader.read()
    return index_file_bytes


def test_base_http_request():
    http_request = requests.HttpRequest('https://www.google.com/')
    assert http_request.response.status_code == '200'


def test_http_get_request_json_response(mock_server):
    mock_server.add_json_response('/test', {'test': 'get'})
    http_request = requests.HttpRequest('http://127.0.0.1:5000/test')
    assert http_request.response.status_code == '200'
    assert http_request.response.json == {'test': 'get'}


def test_http_post_request_json_response(mock_server):
    mock_server.add_json_response('/test_post', {'test': 'post'}, methods=('POST',))
    http_request = requests.HttpRequest('http://127.0.0.1:5000/test_post', method='POST')
    assert http_request.response.status_code == '200'
    assert http_request.response.json == {'test': 'post'}


def serialize_headers(headers: Headers) -> dict:
    return {key: value for key, value in headers.items()}


def serialize_data_json(data: bytes) -> dict:
    return {'data': json.loads(data)}


def serialize_data_bytes(data: bytes) -> dict:
    return {'data': base64.b64encode(data).decode('ascii')}


def serialize_form(form_data):
    return {'form': {key: value for key, value in form_data.items()}}


def serialize_files(file_data):
    return {'files': {key: base64.b64encode(value.read()).decode('ascii') for key, value in file_data.items()}}


def serialize_method(method):
    return {'method': str(method)}


def serialize_request_callback():
    request_dict = {
        "method": request.method,
        "headers": request.headers,
        "body": request.data,
        "form": request.form,
        "files": request.files,
    }
    print(request_dict)
    data = serialize_data_json(request.data) if request.is_json else serialize_data_bytes(request.data)
    return json.dumps(
        serialize_headers(request.headers) | data | serialize_form(request.form) | serialize_files(
            request.files) | serialize_method(request.method))


def test_http_post_body_file(mock_server, image_file_bytes: bytes):
    mock_server.add_callback_response('/serialize_request', serialize_request_callback,
                                      methods=('POST', 'GET', 'PUT', 'PATCH', 'DELETE',))
    http_body = requests.HttpBodyFile(file_name='tests/static/image.png')
    http_request = requests.HttpRequest('http://127.0.0.1:5000/serialize_request', body=http_body, method='POST')
    assert http_request.response.status_code == '200'
    assert http_request.response.json['Content-Type'] == 'image/png'
    assert int(http_request.response.json['Content-Length']) == len(image_file_bytes)
    assert base64.b64decode(http_request.response.json['data']) == image_file_bytes
    assert http_request.response.json['method'] == 'POST'


def test_http_post_body_form_data(mock_server):
    form_dict = {'name': "David", 'number': '32'}  # Url Encoded Form data is all converted to strings
    http_body = requests.HttpBodyForm(form_dict)
    http_request = requests.HttpRequest('http://127.0.0.1:5000/serialize_request', body=http_body, method='POST')
    assert http_request.response.status_code == '200'
    assert http_request.response.json['Content-Type'] == 'application/x-www-form-urlencoded'
    assert int(http_request.response.json['Content-Length']) == http_body.content_len
    assert http_request.response.json['form'] == form_dict
    assert http_request.response.json['method'] == 'POST'


def test_http_post_body_json(mock_server):
    json_dict = {'name': "David", 'number': '32'}  # Url Encoded Form data is all converted to strings
    http_body = requests.HttpBodyJSON(json_dict)
    http_request = requests.HttpRequest('http://127.0.0.1:5000/serialize_request', body=http_body, method='POST')
    assert http_request.response.status_code == '200'
    assert http_request.response.json['Content-Type'] == 'application/json'
    assert int(http_request.response.json['Content-Length']) == http_body.content_len
    assert http_request.response.json['data'] == json_dict
    assert http_request.response.json['method'] == 'POST'


def test_http_post_body_multi_file(mock_server, image_file_bytes, index_file_bytes):
    http_body_section_1 = requests.HttpBodyMultiFileSection('my_image', file_path='tests/static/image.png')
    http_body_section_2 = requests.HttpBodyMultiFileSection('my_index', file_path='tests/static/index.html')
    http_body_section_3 = requests.HttpBodyMultiFileSection('just-text', value="This is just some text")
    http_body = requests.HttpBodyMultiFile([http_body_section_1, http_body_section_2, http_body_section_3])
    http_request = requests.HttpRequest('http://127.0.0.1:5000/serialize_request', body=http_body, method='POST')
    assert http_request.response.status_code == '200'
    assert int(http_request.response.json['Content-Length']) == http_body.content_len
    assert 'multipart/form-data' in http_request.response.json['Content-Type']
    assert http_body._boundary.decode('utf-8') in http_request.response.json['Content-Type']
    assert http_request.response.json['form'] == {'just-text': "This is just some text"}
    assert base64.b64decode(http_request.response.json['files']['my_image']) == image_file_bytes
    assert base64.b64decode(http_request.response.json['files']['my_index']) == index_file_bytes
    assert http_request.response.json['method'] == 'POST'


def test_http_post_body_chunked(mock_server, image_file_bytes):
    http_body = requests.HttpBodyChunked('tests/static/image.png', chunk_size=512)
    http_request = requests.HttpRequest('http://127.0.0.1:5000/serialize_request', body=http_body, method='POST')
    assert http_request.response.status_code == '200'
    assert 'chunked' in http_request.response.json['Transfer-Encoding']
    assert 'image/png' in http_request.response.json['Content-Type']
    assert base64.b64decode(http_request.response.json['data']) == image_file_bytes
    assert http_request.response.json['method'] == 'POST'


def test_http_post_custom_headers(mock_server):
    custom_headers = {'Authorization': 'Bearer AXVubzpwQDU1dzByYM'}
    http_request = requests.HttpRequest('http://127.0.0.1:5000/serialize_request', custom_headers=custom_headers,
                                        method='POST')
    assert http_request.response.json['Authorization'] == custom_headers['Authorization']
    assert http_request.response.json['method'] == 'POST'


def test_request_get(mock_server):
    r = requests.request('http://127.0.0.1:5000/serialize_request', method='GET')
    assert r.json['method'] == 'GET'
    assert int(r.status_code) == 200


def test_get(mock_server):
    r = requests.get('http://127.0.0.1:5000/serialize_request')
    assert r.json['method'] == 'GET'
    assert int(r.status_code) == 200


def test_post(mock_server):
    r = requests.post('http://127.0.0.1:5000/serialize_request')
    assert r.json['method'] == 'POST'
    assert int(r.status_code) == 200


def test_put(mock_server):
    r = requests.put('http://127.0.0.1:5000/serialize_request')
    assert r.json['method'] == 'PUT'
    assert int(r.status_code) == 200


def test_patch(mock_server):
    r = requests.patch('http://127.0.0.1:5000/serialize_request')
    assert r.json['method'] == 'PATCH'
    assert int(r.status_code) == 200


def test_delete(mock_server):
    r = requests.delete('http://127.0.0.1:5000/serialize_request')
    assert r.json['method'] == 'DELETE'
    assert int(r.status_code) == 200


def test_post_data(mock_server):
    data = {'hello': 'world'}
    r = requests.post('http://127.0.0.1:5000/serialize_request', data=data)
    assert r.json['form'] == data


def test_post_data_save(mock_server):
    data = {'hello': 'world'}
    r = requests.post('http://127.0.0.1:5000/serialize_request', data=data, save_to_file='data.json')
    with open('data.json', 'r') as reader:
        file_data = json.loads(reader.read())
    os.remove('data.json')
    with pytest.raises(AttributeError) as e:
        content = r.json['form']
    assert file_data['form'] == data