---
layout: archive
title: 마인크래프트 AI
taxonomy: 마인크래프트 AI
permalink: /categories/minecraft-ai/
description: Minecraft Self-Learning AI의 기획 배경, 아키텍처, 기술 후보, 관측 데이터와 개발 로드맵을 기록합니다.
---

<nav aria-label="프로젝트 카테고리 경로">
  <a href="{{ '/categories/hobby/' | relative_url }}">취미</a> →
  <a href="{{ '/categories/personal-project/' | relative_url }}">개인 프로젝트</a> →
  <span aria-current="page">마인크래프트 AI</span>
</nav>

<p><strong>현재 상태: 기획 단계.</strong> 초기 환경 구축도 시작하지 않았습니다. 아래 글은 구현 결과가 아닌 설계와 검토 기록이며, 기술 스택과 개발 일정은 아직 확정하지 않았습니다.</p>

<p>명령을 기다리는 봇에서 출발해, 경험으로 행동을 개선하는 에이전트를 만들 수 있을까요? 다섯 편을 순서대로 읽으며 목표와 검증 기준을 정리합니다.</p>

{% assign project_posts = site.categories['마인크래프트 AI'] | where: 'project', 'minecraft-ai' | sort: 'project_order' %}
<h2 class="archive__subtitle">기획 연재 <span class="taxonomy__count">{{ project_posts | size }}</span></h2>
<div class="entries-list">
{% for post in project_posts %}{% include archive-single.html type='list' %}{% endfor %}
</div>
