---
layout: default
---

{% if site.banners.strip and site.banners.strip != "" %}
<div class="banner-strip"><img src="{{ site.banners.strip | prepend: "/" | relative_url }}" alt=""></div>
{% endif %}

<nav class="tabs" aria-label="Sections">
  <a href="#news" data-tab="news"><span class="lang-en">News</span><span class="lang-es" lang="es">Noticias</span></a>
  <a href="#publications" data-tab="publications"><span class="lang-en">Publications</span><span class="lang-es" lang="es">Publicaciones</span></a>
  <a href="#research" data-tab="research"><span class="lang-en">Research</span><span class="lang-es" lang="es">Investigación</span></a>
</nav>

<section class="tab-panel" id="news" markdown="1">

<h2>{% if site.fish_drawings %}{% include fish.html kind="tiny" %}{% endif %}<span class="lang-en">News</span><span class="lang-es" lang="es">Noticias</span></h2>

<div class="lang-en">{% include news.html lang="en" %}</div>
<div class="lang-es" lang="es">{% include news.html lang="es" %}</div>

</section>

{% if site.banners.divider and site.banners.divider != "" %}<div class="banner-divider" aria-hidden="true"><img src="{{ site.banners.divider | prepend: "/" | relative_url }}" alt=""></div>{% endif %}

<section class="tab-panel" id="publications" markdown="1">

{% assign submitted = site.data.submitted | where_exp: "p", "p.title" %}
{% if submitted.size > 0 %}
<h2>{% if site.fish_drawings %}{% include fish.html kind="tiny" %}{% endif %}<span class="lang-en">Preprints</span><span class="lang-es" lang="es">Preprints</span></h2>

{% include publications.html list=submitted by_year=true %}
{% endif %}

<h2>{% if site.fish_drawings %}{% include fish.html kind="tiny" %}{% endif %}<span class="lang-en">Publications</span><span class="lang-es" lang="es">Publicaciones</span></h2>

{% include publications.html list=site.data.publications by_year=true %}

</section>

{% if site.banners.divider and site.banners.divider != "" %}<div class="banner-divider" aria-hidden="true"><img src="{{ site.banners.divider | prepend: "/" | relative_url }}" alt=""></div>{% endif %}

<section class="tab-panel" id="research" markdown="1">

<h2>{% if site.fish_drawings %}{% include fish.html kind="tiny" %}{% endif %}<span class="lang-en">Research</span><span class="lang-es" lang="es">Investigación</span></h2>

<div class="lang-en">{% include research.html lang="en" %}</div>
<div class="lang-es" lang="es">{% include research.html lang="es" %}</div>

</section>
