---
layout: default
title: Fursuit
permalink: /fursuit/
---
<div class="content">
  <p class="lang-en">
    Fursuit made by <a href="https://www.furmony.com/" class="telegram-link" target="_blank" rel="noopener noreferrer">
    Furmony studio</a>
  </p>
  <p class="lang-zh">
    毛毛與睡衣由 <a href="https://www.furmony.com/" class="telegram-link" target="_blank" rel="noopener noreferrer">
    鴻萌造物</a> 製作
  </p>
</div>

<div class="fursuit-grid">
  {% for item in site.data.fursuit %}
    <div class="grid-item fade-in" tabindex="0">
      <img src="{{ site.baseurl }}{{ item.image }}" alt="{{ item.title | default:'Loyn Fursuit' }}">
      <div class="overlay">
        {% if item.title %}
        <div class="title">{{ item.title }}</div>
        {% endif %}
        <div class="photographer lang-en">📷 {{ item.photographer }}</div>
        <div class="photographer lang-zh">📷 {{ item.photographer }}</div>
        <div class="date lang-en">📅 {{ item.date_taken }}</div>
        <div class="date lang-zh">📅 {{ item.date_taken }}</div>
        {% if item.description %}
        <div class="description lang-en">{{ item.description }}</div>
        {% if item.description_zh %}
        <div class="description lang-zh">{{ item.description_zh }}</div>
        {% else %}
        <div class="description lang-zh">{{ item.description }}</div>
        {% endif %}
        {% endif %}
      </div>
    </div>
  {% endfor %}
</div>

<script src="/assets/js/gallery.js"></script>
