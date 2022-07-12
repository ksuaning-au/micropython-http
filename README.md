# uHTTP

uHTTP is a Micropython http request module. The module supports most standard HTTP requests and such features as sending and receiving chunked data. 

## Installation

Place uhttp onto your microcontroller running Micropython into the directory with your main.py or some other library directory on your Micropython PATH. The module should now be available for import.

## Usage

```python
from uhttp import requests

url = 'http://someurl.com/'

# GET request
r = requests.get(url)
print(r.status_code)
print(r.text)
print(r.json)

# GET request which will save the body of the response to data.json
r = requests.get(url , save_to_file='data.json')

# POST request that sends the file 'data.json'
r = requests.post(url , file='data.json')

# POST request that sends the file 'my-image.png'
r = requests.post(url , file='my-image.png')

# POST request that will send data:dict as application/x-www-form-urlencoded
r = requests.post(url , data={'data':'my_data'})

# POST request that will send data:dict as application/json
r = requests.post(url , json={'data':'my_data'})

# POST request that will send empty body
r = requests.post(url)

# POST request with custom_headers
r = requests.post(url, custom_headers={"Authorization" : "Bearer myToken12355"})

# POST request that will send file in chunks
r = requests.post(url, file='my-image.png', chunked=True, chunk_size=128)

# Looking through the test directory will provide further insight into how the module functions.
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)