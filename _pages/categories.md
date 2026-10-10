---
layout: archive
title: 카테고리
permalink: /categories/
description: "주제별 글 모음입니다. SAR, 신호처리, 수학, 프로그래밍과 개인 프로젝트의 글을 찾아보세요."
---
{% for category in site.data.category_routes %}
<section id="{{ category.slug }}" class="list__item">
  <h2 class="archive__item-title"><a href="{{ category.url | relative_url }}">{{ category.name | escape }} <span class="taxonomy__count">{{ site.categories[category.name] | size }}</span></a></h2>
</section>
{% endfor %}

<script src="{{ "/assets/js/category-legacy.js" | relative_url }}" defer></script>
