## Documentation

### Start

#### Init
To start you have to import the API object from drowse package and instantiate it.

API constructor has only one required parameter, the base url of the api, es `https://my.endpooint.base/api/v1/`

```python
from drowse import API
api = API(`https://my.endpooint.base/api/v1/`)
```
The API object is the base used for all requests.

#### Authentication
drowse support 3 authentication method in API creation:

* basic http authentication by `authUser` parameter and `authSecret` parameter
```python
api = API(`https://my.endpooint.base/api/v1/`, authUser=`my_user', authSecret='my_secret', authSecretHash=False)
```
* digest http authentication by authUser parameter and `authSecret` parameter with flag authSecretHash set to True (default)
```python
api = API(`https://my.endpooint.base/api/v1/`, authUser=`my_user', authSecret='my_secret', authSecretHash=True)
```
* custom header token authentication by `authKeyHeader` parameter and `authSecret` parameter
```python
api = API(`https://my.endpooint.base/api/v1/`, authKeyHeader=`my_token_header' authSecret='my_token')
```

All of this parameters have as default `None` so if you don`t provide them you have a no authenticated connection.
```python
api = API(`https://my.endpooint.base/api/v1/`)
```

#### SSL
drowse expose the requests verify flags, which controls if to verify or not the SSL certificate of the endpoint. It defaults to `True` but if you want to test a REST api with self-signed certificates
you can set it to False.

```python
api = API(`https://my.endpooint.base/api/v1/`, verify=False)
```

### Interaction

#### Basic

You can interact with the api with the syntax:

`api.{{ resource_name }}.{{ method }}`

this is recursive so to interact with inner resource you can:

`api.{{ resource_name }}.{{ inner_resource_name }}{{ method }}`

It's possible also to access specific resource with the `id` parameter:

`api.{{ resource_name }}({{ id }}).{{ inner_resource_name }}({{ inner_id }}){{ method }}`

#### Data type

drowse transmit and decode data as `content-type: application/json`.

#### Get

With the get method you can have basic get:

```python
response = api.resoure.get()
```
and get with parameters too:

```python
response = api.resoure.get(attr=value)
```

In the response you have a dict of output data parsed from json

#### Post

The post method use a dict as input data and send it as a json:

```python
response = api.resource.post(my_json)
```
In the response you have a dict of output data parsed from json.

#### Put

Put method requires an `id` parameter and use a dict as input data:

```python
response = api.resource(my_id).put(my_json)
```

In the response you have a dict of output data parsed from json.


#### Delete

Delete method requires and `id` parameters requires no input data:

```python
api.resource(my_id).delete()
```
This is a no response method.

### Workflow

#### 4XX and 5XX error codes

drowse doesn't perform any check on response status code, if a request returns and HTTP error code (both client and server) the requests underlying library raise an exception of type `requests.exceptions.HTTPError` with the status code in the message.
You have to manage these for your worflow.

#### Errors and Exceptions

drowse doesn`t perform any checks on generic connection problems, it relies to the requests underlying library:

> In the event of a network problem (e.g. DNS failure, refused connection, etc), Requests will raise a ConnectionError exception.
> In the rare event of an invalid HTTP response, Requests will raise an HTTPError exception.
> If a request times out, a Timeout exception is raised.
> If a request exceeds the configured number of maximum redirections, a TooManyRedirects exception is raised.
> All exceptions that Requests explicitly raises inherit from requests.exceptions.RequestException.

