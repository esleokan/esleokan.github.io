---
layout: default
title: Gallery
permalink: /gallery/
---

<div class="content">
  <h2 >Note</h2>
<p>
    <strong>I’m not the artist of the works in this gallery </strong>. They are all commissioned or gifted by talented creators. This gallery is just a personal archive to keep everything in one place. All artworks are credited to their original artists, including personal commissions and works from Skeb.
  </p>
</div>


<div class="grid">
  {% assign reversed_gallery = site.data.gallery | reverse %}
  {% for item in reversed_gallery %}
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
