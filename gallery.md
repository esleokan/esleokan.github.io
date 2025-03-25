---
layout: default
title: Gallery
permalink: /gallery/
---

<div class="grid">
  {% assign reversed_gallery = site.data.gallery | reverse %}
  {% for item in reversed_gallery %}
    <div class="grid-item fade-in">
      {% if item.work_link %}
        <a href="{{ item.work_link }}" target="_blank">
          <img src="{{ item.image }}" alt="{{ item.title }}" />
          <div class="overlay">
            <div class="title"><a href="{{ item.work_link }}" target="_blank">{{ item.title }}</a></div>
            <div class="artist">🎨 <a href="{{ item.author_link | default:'#' }}" target="_blank">{{ item.author }}</a></div>
          </div>
        </a>
      {% else %}
        <img src="{{ item.image }}" alt="{{ item.title }}" />
        <div class="overlay">
          <div class="title">{{ item.title }}</div>
          <div class="artist">🎨 <a href="{{ item.author_link | default:'#' }}" target="_blank">{{ item.author }}</a></div>
        </div>
      {% endif %}
    </div>
  {% endfor %}
</div>
