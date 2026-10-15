---
layout: default
---

<nav class="tabs" role="tablist" aria-label="Sections">
  <a role="tab" href="#news" data-tab="news"><span class="lang-en">News</span><span class="lang-es" lang="es">Noticias</span></a>
  <a role="tab" href="#publications" data-tab="publications"><span class="lang-en">Publications</span><span class="lang-es" lang="es">Publicaciones</span></a>
  <a role="tab" href="#research" data-tab="research"><span class="lang-en">Research</span><span class="lang-es" lang="es">Investigación</span></a>
</nav>

<div class="tab-panel" id="panel-news" data-panel="news" role="tabpanel" markdown="1">

<h2 class="tab-heading"><span class="lang-en">News</span><span class="lang-es" lang="es">Noticias</span></h2>

<div class="lang-en">{% include news.html lang="en" %}</div>
<div class="lang-es" lang="es">{% include news.html lang="es" %}</div>

</div>

<div class="tab-panel" id="panel-publications" data-panel="publications" role="tabpanel" markdown="1">

{% assign submitted = site.data.submitted | where_exp: "p", "p.title" %}
{% if submitted.size > 0 %}
<h2 id="preprints"><span class="lang-en">Preprints and submitted</span><span class="lang-es" lang="es">Preprints y manuscritos enviados</span></h2>

{% include publications.html list=submitted %}
{% endif %}

<h2 id="publications-list"><span class="lang-en">Publications</span><span class="lang-es" lang="es">Publicaciones</span></h2>

{% include publications.html list=site.data.publications by_year=true %}

</div>

<div class="tab-panel" id="panel-research" data-panel="research" role="tabpanel" markdown="1">

<h2 class="tab-heading"><span class="lang-en">Research</span><span class="lang-es" lang="es">Investigación</span></h2>

<div class="lang-en">{% include research.html lang="en" %}</div>
<div class="lang-es" lang="es">{% include research.html lang="es" %}</div>

</div>
