World Bank
================


Python wrapper for the  [World Bank data API](http://data.worldbank.org/developers).  Based on the [Fred API](https://github.com/zachwill/fred) of Zach Williams.
Also [lightcatcher](http://data.worldbank.org/developers)
The World Bank no longer requires an API key.


Usage
-----

With your API key saved in the `fred_api_key` file:

    >>> from fred import Fred
    >>> Fred().category(category_id=125)


### Methods

* `category` -- Get economic data for a specific category.
<pre><code>
    >>> Fred().category(category_id=120)
</code></pre>


* `releases` -- Get all releases of economic data.
<pre><code>
    >>> Fred().releases(limit=10)

    >>> Fred().releases('dates', xml_output=True)
</code></pre>


* `release` -- Get economic data for a specific release.
<pre><code>
    >>> Fred().release('series', release_id=51)
</code></pre>


* `series` -- Get economic series of data.
<pre><code>
    >>> Fred().series('search', search_text="money stock")

    >>> Fred().series(series_id='IRA')
</code></pre>


* `sources` -- Get all of FRED's sources of economic data.
<pre><code>
    >>> Fred().sources()
</code></pre>


* `source` -- Get a single source of economic data.
<pre><code>
    >>> Fred().source(source_id=51)
</code></pre>


* `api` -- Generic way of interacting with the FRED API.
<pre><code>
    >>> Fred().api('release', 'dates', release_id=51)

    >>> Fred().api('category', category_id=119)
</code></pre>


**NOTE**: Normally, data is returned in dictionary format instead of XML. If you're
looking for XML output, however, just pass in the `xml_output=True` argument to a
method.

    >>> Fred().releases(xml_output=True)


License
-------

**Author**: Zach Williams

All code released under [the Unlicense](http://unlicense.org/) (a.k.a. Public
Domain).
