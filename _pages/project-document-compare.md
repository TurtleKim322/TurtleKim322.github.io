---
layout: single
title: "문서 비교 프로그램 개발 기록"
permalink: /projects/document-compare/
author_profile: false
toc: false
sidebar: categories
---

문서의 텍스트 차이와 확인 가능한 페이지 위치를 나란히 검토하는 Windows 앱을 만들었다.
Python + PyQt6를 유지하면서 형식별 파서, OCR, 검토 UI, 대용량 경계와 Page View 성능을 개선한 과정을 기록한다.

현재 버전은 0.4.2 MVP다. HWP는 한컴 Automation이 필요하고, 이미지 전용 변경·복잡한 서식은 완전 비교하지 않는다.
소스는 별도 Private GitHub 저장소에서 관리한다. 이 공개 연재에는 전체 소스나 실제 업무 자료를 포함하지 않는다.

## 순서대로 읽기

{% assign project_posts = site.posts | where: "project", "document-compare" | sort: "project_order" %}
<ol class="project-timeline">
{% for post in project_posts %}
  <li><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a> <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y-%m-%d" }}</time></li>
{% endfor %}
</ol>

[이 프로젝트의 카테고리](/categories/document-compare/) · [개인 프로젝트](/categories/personal-project/)
