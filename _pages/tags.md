---
layout: archive
title: 태그
permalink: /tags/
---

{% assign tags_sorted = site.tags | sort %}
{% for tag in tags_sorted %}
  {% assign tag_name = tag[0] %}
  <section class="category-archive" id="{{ tag_name | slugify }}">
    <h2>{{ tag_name | escape }}</h2>
    <ul>
      {% assign tag_posts = tag[1] | sort: "date" | reverse %}
      {% for post in tag_posts %}
        <li><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a> <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y-%m-%d" }}</time></li>
      {% endfor %}
    </ul>
  </section>
{% endfor %}
