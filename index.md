---
layout: default
---

<nav class="tabs" aria-label="Sections">
  <a href="#news" data-tab="news"><span class="lang-en">News</span><span class="lang-es" lang="es">Noticias</span></a>
  <a href="#publications" data-tab="publications"><span class="lang-en">Publications</span><span class="lang-es" lang="es">Publicaciones</span></a>
  <a href="#research" data-tab="research"><span class="lang-en">Research</span><span class="lang-es" lang="es">Investigación</span></a>
</nav>

<section class="tab-panel" id="news" markdown="1">

<h2><span class="lang-en">News</span><span class="lang-es" lang="es">Noticias</span></h2>

<div class="lang-en">{% include news.html lang="en" %}</div>
<div class="lang-es" lang="es">{% include news.html lang="es" %}</div>

</section>

<section class="tab-panel" id="publications" markdown="1">

{% assign submitted = site.data.submitted | where_exp: "p", "p.title" %}
{% if submitted.size > 0 %}
<h2><span class="lang-en">Preprints</span><span class="lang-es" lang="es">Preprints</span></h2>

{% include publications.html list=submitted %}
{% endif %}

<h2><span class="lang-en">Publications</span><span class="lang-es" lang="es">Publicaciones</span></h2>

{% include publications.html list=site.data.publications by_year=true %}

</section>

<section class="tab-panel" id="research" markdown="1">

<h2><span class="lang-en">Research</span><span class="lang-es" lang="es">Investigación</span></h2>

<div class="lang-en">{% include research.html lang="en" %}</div>
<div class="lang-es" lang="es">{% include research.html lang="es" %}</div>

</section>
