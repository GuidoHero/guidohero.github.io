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

## Education

**Ph.D. Ecology & Evolutionary Biology 2020 - 2025**<br>
  The University of Tennessee - Knoxville, TN

**M.Sc. Modeling of Ecological Systems 2016 - 2018**<br>
  University of Toulouse III Paul Sabatier - Toulouse, France

**B.Sc. Biology 2011-2015**<br>
  Pontifical Javeriana University - Bogotá, Colombia

</div>

<div class="lang-es" lang="es" markdown="1">

## Cargo actual

**Posdoctorado Eric and Wendy Schmidt AI in Science**<br>
Departamento de Ecología y Biología Evolutiva<br>
Departamento de Recursos Naturales y Medio Ambiente<br>
Universidad de Cornell – Ithaca, NY, EE. UU.

## Noticias

{% include news.html lang="es" %}

## Formación académica

**Ph.D. Ecología y Biología Evolutiva 2020 - 2025**<br>
  Universidad de Tennessee - Knoxville, TN, EE. UU.

**M.Sc. Modelación de Sistemas Ecológicos 2016 - 2018**<br>
  Universidad de Toulouse III Paul Sabatier - Toulouse, Francia

**B.Sc. Biología 2011-2015**<br>
  Pontificia Universidad Javeriana - Bogotá, Colombia

</div>

{% assign submitted = site.data.submitted | where_exp: "p", "p.title" %}
{% if submitted.size > 0 %}
<h2 id="preprints"><span class="lang-en">Preprints and submitted</span><span class="lang-es" lang="es">Preprints y manuscritos enviados</span></h2>

{% include publications.html list=submitted %}
{% endif %}

<h2 id="publications"><span class="lang-en">Publications</span><span class="lang-es" lang="es">Publicaciones</span></h2>

{% include publications.html list=site.data.publications by_year=true %}
