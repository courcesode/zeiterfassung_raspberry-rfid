import urllib.request
contents = urllib.request.urlopen("http://localhost:4000/log?id=1&status=1").read()
