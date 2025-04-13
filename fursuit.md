---
layout: default
title: Fursuit
permalink: /fursuit/
---
<div class="content">
<p>
Fursuit made by  <a href="https://www.furmony.com/" class="telegram-link" target="_blank" rel="noopener noreferrer">
Furmony studio</a>
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
        <div class="photographer">📷 {{ item.photographer }}</div>
        <div class="date">📅 {{ item.date_taken }}</div>
        {% if item.description %}
        <div class="description">{{ item.description }}</div>
        {% endif %}
      </div>
    </div>
  {% endfor %}
</div>

<script src="/assets/js/gallery.js"></script>
