---
layout: archive
title: 카테고리
permalink: /categories/
---

{% for category in site.data.categories.categories %}
  {% assign category_posts = site.categories[category.name] | sort: "date" | reverse %}
  <section class="category-archive" id="{{ category.slug }}">
    <h2>{{ category.name | escape }} <span class="taxonomy__count">{{ category_posts | size }}</span></h2>
    {% if category_posts.size > 0 %}
      <ul>
        {% for post in category_posts %}
          <li><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a> <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y-%m-%d" }}</time></li>
        {% endfor %}
      </ul>
    {% else %}
      <p class="category-archive__empty">아직 분류된 글이 없습니다.</p>
    {% endif %}
    {% for child in category.children %}
      {% assign child_posts = site.categories[child.name] | sort: "date" | reverse %}
      <section class="category-archive__child" id="{{ child.slug }}">
        <h3>{{ child.name | escape }} <span class="taxonomy__count">{{ child_posts | size }}</span></h3>
        {% if child_posts.size > 0 %}
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
