---
layout: default
---

<div class="lang-en" markdown="1">

## Current appointment

**Eric and Wendy Schmidt AI in Science Postdoctoral Fellow**<br>
Department of Ecology and Evolutionary Biology<br>
Department of Natural Resources and the Environment<br>
Cornell University – Ithaca, NY

## News

{% include news.html lang="en" %}

</div>

<div class="lang-es" lang="es" markdown="1">

## Cargo actual

**Posdoctorado Eric and Wendy Schmidt AI in Science**<br>
Departamento de Ecología y Biología Evolutiva<br>
Departamento de Recursos Naturales y Medio Ambiente<br>
Universidad de Cornell – Ithaca, NY, EE. UU.

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
