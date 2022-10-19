# Covid-19-API
**This API deprecated on the 31st of October, 2022.**

This is the code running in AWS Lambda powering covid-api.mmediagroup.fr/v1

<!-- wp:paragraph -->
<p>In our bid to do our part, we've created a free public API for others to build apps upon. The API returns live cases and historical data.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><a href="https://blog.mmediagroup.fr/post/m-media-coronavirus-api-passes-1-million-requests/">This API has now been called over <a href="https://blog.mmediagroup.fr/post/m-media-covid-api-passes-30-million-requests/">30 million times now!</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>The API has endpoints to handle historical as well as near realtime data (updated once every hour). The average API response time is between 70 and 250 ms but may take up to 3 seconds, depending if the request is in the cache or not.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>You can see a human-friendly webpage that uses the API here <a href="https://mmediagroup.fr/covid-19">https://mmediagroup.fr/covid-19</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>What the API is for</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The API is intended for developers, machines, programs, and other websites to be able to quickly fetch up to date information on the COVID-19 epidemic.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>It can be used to build tools and systems that are used for data analysis all the way to websites that act as public dashboards and charts.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Using the API</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>If you're a developer, you can use the API right now. Please be nice to us and cache the data locally so we don't pay too much :)!</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>API base:<br><a rel="noreferrer noopener" href="https://covid-api.mmediagroup.fr/v1/cases" target="_blank">https://covid-api.mmediagroup.fr/v1</a></p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>Live cases data</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Request:<br>GET <a rel="noreferrer noopener" href="https://covid-api.mmediagroup.fr/v1/cases" target="_blank">/cases</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Optional query parameters</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
  <li>country<ul><li>Any country name (case sensitive)</li></ul></li>
  <li>ab<ul><li>Any country ISO abbreviation (example: FR) (takes precedence over "country" parameter)</li></ul></li>
  <li>continent<ul><li>Any world continent (example: Europe) (takes precedence over "country" parameter)</li></ul></li>
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
Example request:
  <pre><code class="lang-http"><span class="hljs-attr">GET /cases?country</span>=<span class="hljs-string">France</span>
</code></pre>

Example response:
```json
{
  "All": {
    "confirmed": 2604595,
    "recovered": 195365,
    "deaths": 62548,
    "country": "France",
    "population": 64979548,
    "sq_km_area": 551500,
    "life_expectancy": "78.8",
    "elevation_in_meters": 375,
    "continent": "Europe",
    "abbreviation": "FR",
    "location": "Western Europe",
    "iso": 250,
    "capital_city": "Paris",
    "lat": "46.2276",
    "long": "2.2137",
    "updated": "2020/12/26 12:21:56+00"
  },
  "French Guiana": {
    "lat": "4",
    "long": "-53",
    "confirmed": 12685,
    "recovered": 9995,
    "deaths": 71,
    "updated": "2020/12/26 12:21:56+00"
  }
}
```

<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>Historical cases data</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Request:<br>GET <a rel="noreferrer noopener" href="https://covid-api.mmediagroup.fr/v1/history" target="_blank">/history</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Required query parameters</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><li>status<ul><li>Confirmed</li><li>Deaths</li><li>Recovered (DEPRECIATED)</li></ul></li></ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>Optional query parameters</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><li>country<ul><li>Any country name (case sensitive)</li></ul></li><li>ab<ul><li>Any country ISO abbreviation (example: FR) (takes precedence over "country" parameter)</li></ul></li>
  <li>continent<ul><li>Any world continent (example: Europe) (takes precedence over "country" parameter)</li></ul></li>
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
Example request:
<pre><code class="lang-http">GET /<span class="hljs-built_in">history</span>?country=Germany&amp;status=deaths
</code></pre>

Example response:
```JSON
{
  "All": {
    "country": "Germany",
    "population": 82114224,
    "sq_km_area": 357022,
    "life_expectancy": "77.4",
    "elevation_in_meters": 263,
    "continent": "Europe",
    "abbreviation": "DE",
    "location": "Western Europe",
    "iso": 276,
    "capital_city": "Berlin",
    "dates": {
      "2020-12-25": 29580,
      "2020-12-24": 29330,
      "2020-12-23": 28909,
      "2020-12-22": 28096,
      "2020-12-21": 27110
    }
  }
}
```

<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>Vaccines data</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Request:<br>GET <a rel="noreferrer noopener" href="https://covid-api.mmediagroup.fr/v1/vaccines" target="_blank">/vaccines</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Optional query parameters</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
  <li>country<ul><li>Any country name (case sensitive)</li></ul></li>
  <li>ab<ul><li>Any country ISO abbreviation (example: FR) (takes precedence over "country" parameter)</li></ul></li>
  <li>continent<ul><li>Any world continent (example: Europe) (takes precedence over "country" parameter)</li></ul></li>
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
Example request:
  <pre><code class="lang-http"><span class="hljs-attr">GET /vaccines?country</span>=<span class="hljs-string">France</span>
</code></pre>

Example response:
```JSON
{
  "All": {
    "administered": 7927771,
    "people_vaccinated": 2297100,
    "people_partially_vaccinated": 5630671,
    "country": "France",
    "population": 64979548,
    "sq_km_area": 551500,
    "life_expectancy": "78.8",
    "elevation_in_meters": 375,
    "continent": "Europe",
    "abbreviation": "FR",
    "location": "Western Europe",
    "iso": 250,
    "capital_city": "Paris",
    "lat": "46.2276",
    "long": "2.2137",
    "updated": "2020/12/26 12:21:56+00"
  }
}
```

<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>Authorization</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>No authorisation is required to fetch data from the API.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Built using this API</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Feel free to share your projects that implement this API!</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><li><a href="https://mmediagroup.fr/covid-19">mmediagroup.fr/covid-19</a></li><li><a href="https://covid-t.herokuapp.com">covid-t.herokuapp.com</a></li>
 <li><a href="https://github.com/Fr0sty404/GoCoronaVirusAPIParser">GoCoronaVirusAPIParser</a></li>
 <li><a href="https://blog.mmediagroup.fr/post/coronavirus-covid-19-watch-wordpress-plugin/">Coronavirus-COVID-19-Watch-WordPress-Plugin</a></li>
 <li><a href="https://github.com/ladybug-tools/spider-covid-19-viz-3d">Spider 3d vizualizer</a></li>
 <li><a href="https://github.com/MasterBrian99/Discord-bot-miku" >Discord bot-miku</a></li>
 <li><a href="https://github.com/LexxFade/Ivis-Bot"> Ivis-Bot [Discord]</a></li>
 <li><a href="https://github.com/CrisesKhaos/COVID-19">NoCo Mobile App</a></li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Data sources</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Historical data:&nbsp;<a rel="noreferrer noopener" href="https://github.com/CSSEGISandData/COVID-19" target="_blank">https://github.com/CSSEGISandData/COVID-19</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Realtime data:&nbsp;<a rel="noreferrer noopener" href="https://opendata.arcgis.com/datasets/bbb2e4f589ba40d692fab712ae37b9ac_1.csv" target="_blank">https://opendata.arcgis.com/datasets/bbb2e4f589ba40d692fab712ae37b9ac_1.csv</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Population data:<br><a href="https://github.com/M-Media-Group/country-json/blob/master/src/countries-master.json">https://github.com/M-Media-Group/country-json/blob/master/src/countries-master.json</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Vaccine data:&nbsp;<a rel="noreferrer noopener" href="https://github.com/govex/COVID-19" target="_blank">https://github.com/govex/COVID-19</a></p>
<!-- /wp:paragraph -->


<!-- wp:heading -->
<h2>Rate limits</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>A rate limiter is applied. Realistically, the data updates around once an hour so more frequent requests are futile (though possible). Ridiculous amount of requests will result in you being banned.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>GNU AGPLv3 Licence</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Additionally, we ask you to please not create API's that just use this API as the underlying source.</p>
<p>If you make absurd amounts of requests to our API we will block you. You can contact us to resolve the issue. Please cache the API responses with a lifetime of at least 10 minutes to avoid this happening.</p>
<!-- /wp:paragraph -->
