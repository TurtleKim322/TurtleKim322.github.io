---
layout: single
title: "서울 PS-InSAR 프로젝트"
permalink: /projects/seoul-psinsar/
author_profile: false
toc: false
sidebar: categories
---

{% assign project = site.data.projects.projects | where: "slug", "seoul-psinsar" | first %}

{{ project.description }}

<div class="project-facts">
  <p><strong>사용 데이터</strong><br>{{ project.data }}</p>
  <p><strong>처리 도구</strong><br>{{ project.tools }}</p>
  <p><strong>진행 상태</strong><br>{{ project.status }}</p>
</div>

## 프로젝트 기록

{% assign project_slug = project.slug %}
{% assign project_posts = site.posts | where: "project", project_slug | sort: "project_order" %}
<ol class="project-timeline">
  {% for post in project_posts %}
    <li>
      <a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
      <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y-%m-%d" }}</time>
    </li>
  {% endfor %}
</ol>
