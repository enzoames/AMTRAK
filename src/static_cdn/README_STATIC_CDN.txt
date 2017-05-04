This is the static_cdn folder

The stati_cdn directory contains another folder admin. admin is ralted to the django admin itself.
Everything related to the admin (fonts, etc) is added here.

Static cdn sepparates itself from the local static dir from amtrak


IMPORTANT!

The reason we have static_cdn is to simulate the use of a sepparate server. In production we will have a server
to hold all out static files. Our project that will be in production will grab the static files from the server and
render them. We also have a static folder local to us, which we will use for testing. Once we test all functions
and its fully working, we run the command:      python manage.py collectstatic

What this command does is send our static files to the server where it will be retrieved.