---
layout: archive
title: 카테고리
permalink: /categories/
---

{% for category in site.data.categories.categories %}
  {% assign category_name = category.name %}
  {% assign category_posts = site.categories[category_name] %}
  {% assign category_count = category_posts | size %}
  {% if category_count > 0 %}{% assign category_posts = category_posts | sort: "date" | reverse %}{% endif %}
  <section class="category-archive" id="{{ category.slug }}">
    <h2>{{ category.name | escape }} <span class="taxonomy__count">{{ category_count }}</span></h2>
    {% if category_count > 0 %}
      <ul>
        {% for post in category_posts %}
          <li><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a> <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y-%m-%d" }}</time></li>
        {% endfor %}
      </ul>
    {% else %}
      <p class="category-archive__empty">아직 분류된 글이 없습니다.</p>
    {% endif %}
    {% for child in category.children %}
      {% assign child_name = child.name %}
      {% assign child_posts = site.categories[child_name] %}
      {% assign child_count = child_posts | size %}
      {% if child_count > 0 %}{% assign child_posts = child_posts | sort: "date" | reverse %}{% endif %}
      <section class="category-archive__child" id="{{ child.slug }}">
        <h3>{{ child.name | escape }} <span class="taxonomy__count">{{ child_count }}</span></h3>
        {% if child_count > 0 %}
          <ul>
            {% for post in child_posts %}
              <li><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a> <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y-%m-%d" }}</time></li>
            {% endfor %}
          </ul>
        {% else %}
          <p class="category-archive__empty">아직 분류된 글이 없습니다.</p>
        {% endif %}
      </section>
    {% endfor %}
  </section>
{% endfor %}
