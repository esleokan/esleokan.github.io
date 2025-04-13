---
layout: default
title: Gallery
permalink: /gallery/
---

<div class="content">
<!--  <h2 >Note</h2> -->
<p>
I'm not the artist. Just a fursonal archive to keep the commissioned and gifted works by the artists. I appreciate them!
</p>
</div>

<div class="grid">
  {% for item in site.data.gallery %}
    <div class="grid-item fade-in" tabindex="0">
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

<script src="/assets/js/gallery.js"></script>
