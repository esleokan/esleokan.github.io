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
      <img src="{{ item.image }}" alt="{{ item.title }}" />
      <div class="overlay">
        <div class="title">
          {% if item.work_link %}
            <a href="{{ item.work_link }}" target="_blank" rel="noopener noreferrer">{{ item.title }}</a>
          {% else %}
            {{ item.title }}
          {% endif %}
        </div>
        <div class="artist">
          {% if item.author_link %}
            🎨 <a href="{{ item.author_link }}" target="_blank" rel="noopener noreferrer">{{ item.author }}</a>
          {% else %}
            🎨 {{ item.author }}
          {% endif %}
        </div>
      </div>
    </div>
  {% endfor %}
</div>

<script src="/assets/js/gallery.js"></script>
