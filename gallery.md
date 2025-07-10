---
layout: default
title: Gallery
permalink: /gallery/
---

<div class="content">
  <p class="lang-en">
    I'm not the artist. Just a fursonal archive to keep the commissioned and gifted works by the artists. I appreciate them!
  </p>
  <p class="lang-zh">
    我不是繪師，這邊是展示來自不同繪師筆下的洛恩。感謝他們！
  </p>
  <p class="lang-fr">
    Je ne suis pas l'artiste. Juste un archivage fursonal pour conserver les œuvres commandées et offertes par les artistes. Je les apprécie !
  </p>
</div>

<div class="grid">
  {% for item in site.data.gallery %}
    <div class="grid-item fade-in" tabindex="0">
      {% if item.work_link %}
        <img src="{{ item.image }}" alt="{{ item.title }}" data-work-link="{{ item.work_link }}" />
        <div class="overlay">
          <div class="title" data-link="{{ item.work_link }}">{{ item.title }}</div>
          <div class="artist">🎨 <span data-link="{{ item.author_link | default:'#' }}">{{ item.author }}</span></div>
        </div>
      {% else %}
        <img src="{{ item.image }}" alt="{{ item.title }}" />
        <div class="overlay">
          <div class="title">{{ item.title }}</div>
          <div class="artist">🎨 <span data-link="{{ item.author_link | default:'#' }}">{{ item.author }}</span></div>
        </div>
      {% endif %}
    </div>
  {% endfor %}
</div>

<script src="/assets/js/gallery.js"></script>
