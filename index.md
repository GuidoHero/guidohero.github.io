---
layout: default
---

<div class="lang-en" markdown="1">

## News

{% include news.html lang="en" %}

</div>

<div class="lang-es" lang="es" markdown="1">

## Noticias

{% include news.html lang="es" %}

</div>

{% assign submitted = site.data.submitted | where_exp: "p", "p.title" %}
{% if submitted.size > 0 %}
<h2 id="preprints"><span class="lang-en">Preprints and submitted</span><span class="lang-es" lang="es">Preprints y manuscritos enviados</span></h2>

{% include publications.html list=submitted %}
{% endif %}

<h2 id="publications"><span class="lang-en">Publications</span><span class="lang-es" lang="es">Publicaciones</span></h2>

{% include publications.html list=site.data.publications by_year=true %}
