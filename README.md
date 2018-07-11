# drowse

drowse is a human readable Python slim REST client inspired by [Siesta](https://github.com/scastillo/siesta) and powered by [requests](https://github.com/kennethreitz/requests).

## Quickstart
```python
from drowse import API
api = API('https://api.github.com/')
repos = api.users.lgaggini.repos.get()
```
## Features
* slim
* human-readable
* powered by rock-solid requests
* json only
* errors and exceptions leaved to upper layers

## Install
### Github
```
git clone https://github.com/lgaggini/drowse.git
cd drowse
python2 setup.py install
```

### Pypi
```
pip install drowse
```

## Status
Beta version 0.2.0, manual tested on a medium tests set.

## Documentation
See the [readme](https://github.com/lgaggini/drowse/tree/master/docs/README.md) in the docs folder.
