---
layout: archive
title: 카테고리
permalink: /categories/
---

{% assign categories_sorted = site.categories | sort %}
{% for category in categories_sorted %}
  {% assign category_name = category[0] %}
  <section class="category-archive" id="{{ category_name | slugify }}">
    <h2>{{ category_name | escape }}</h2>
    <ul>
      {% assign category_posts = category[1] | sort: "date" | reverse %}
      {% for post in category_posts %}
        <li><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a> <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y-%m-%d" }}</time></li>
      {% endfor %}
    </ul>
  </section>
{% endfor %}
