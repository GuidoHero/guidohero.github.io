---
layout: default
---

## Current appointment

**Eric and Wendy Schmidt AI in Science Postdoctoral Fellow**\
Department of Ecology and Evolutionary Biology\
Department of Natural Resources and the Environment\
Cornell University – Ithaca, NY

## Education

**Ph.D. Ecology & Evolutionary Biology 2020 - 2025**\
  The University of Tennessee - Knoxville, TN

**M.Sc. Modeling of Ecological Systems 2016 - 2018**\
  University of Toulouse III Paul Sabatier - Toulouse, France

**B.Sc. Biology 2011-2015**\
  Pontifical Javeriana University - Bogotá, Colombia

{% assign submitted = site.data.submitted | where_exp: "p", "p.title" %}
{% if submitted.size > 0 %}
## Preprints and submitted

{% include publications.html list=submitted %}
{% endif %}

## Publications

{% include publications.html list=site.data.publications by_year=true %}
