[Boundless CRM](https://zerg.casino)
====================================

If [ClickFunnels](https://clickfunnel.com) & [Hyros](https://hyros.com) had a baby with [MixMax](http://mixmax.com), [Twilio](https://twilio.com) & [Thanks](https://thanks.io)...


Install
-------

**Be sure to use the same version of the code as the version of the docs
you're reading.** You probably want the latest tagged version, but the
default Git version is the main branch:

    # clone the repository
    $ git clone https://github.com/hoytnix/boundless-crm
    $ cd boundless-crm
    # checkout the correct version
    $ git tag  # shows the tagged versions
    $ git checkout latest-tag-found-above

Create a virtualenv and activate it:

    $ python3 -m venv .venv
    $ . .venv/bin/activate

Or on Windows cmd:

    $ py -3 -m venv .venv
    $ .venv\Scripts\activate.bat

Install Flaskr:

    $ pip install -e .

Or if you are using the main branch, install Flask from source before
installing Flaskr:

    $ pip install -e ../..
    $ pip install -e .


Run
---

    $ flask --app flaskr init-db
    $ flask --app flaskr run --debug

Open http://127.0.0.1:5000 in a browser.


Test
----

    $ pip install '.[test]'
    $ pytest

Run with coverage report:

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser


Collaboration
-------------

**Boundless CRM is an Alpha application!**

With that being said, thanks for your interest!

You may reach out to Michael Hoyt for questions about collaborating:

    📧: michael [d0t] hoyt [@t] fatfirecake [d0t] com
    ☎: +1 (989) 217 - HEMP (4367)

### Eruda

Boundless CRM uses [Eruda](https://eruda.liriliri.io/) for debugging. Eruda
is a mobile browser inspection console. If you are working from a phone
or tablet instead of a desktop you can reach the console by appending
`?eruda=true` to the end of any URL.
