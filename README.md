# ShorTor
A URL Shortener, designed for Tor

## What is this?

ShorTor is a simple URL Shortener written in Python using the Flask framework. It
is licensed under the MIT License and can be used and modified freely. It has been
designed with Tor in mind and can be easily set up as a Hidden Service. However,
this does not mean that it cannot be used as a normal service, outside of Tor. It has
been tested with Tor Browser and Maximum Security Settings and words without any
issues. For the link storage it uses the file system, and more specifically the 
`links` folder.

The current version of ShorTor does not support any kind of rate limiting so it is
"vulnerable" to abuse, however there are plans for rate limiting in the future. It
has not been incorporated in the current version for simplicity, as well as Tor
compatibility (a Hidden Service cannot see any IP / set a cookie). 

## The API
ShorTor actually has an API built-in that can be used by anyone to shorten links
automatically. It is not a proper API yet, but it works. 

### Shortening new links
A `POST` request to `/new` with the `link` parameter set and `Accept: application/json`
in the headers will return a JSON dictionary with the following information:

```
{
	"success": "true",
	"id": "<ID>",
	"link": "https://<HOSTNAME>/l/<ID>",
	"private_key": "<PRIVATEKEY>"
}
```

If the URL supplied via the `link` parameter is invalid, an HTTP Status `400` will
be returned.

The `success` variable indicates whether the action succeeded, the `id` variable contains
the unique identifier of the shortened link, the `link` variable contains the publicly
accessible shortened URL, and the `private_key` variable contains a Private Key, used
solely for viewing statistics about that Link ID.

## How to run ShorTor

The recommended way of running ShorTor is using `virtualenv`:

```bash
virtualenv .
bin/pip install Flask
./main.py
```

This will start the development server listening on `127.0.0.1:5000`. If you're
interested in running this in a production environment, a full WSGI server like
Gunicorn is recommended. 
