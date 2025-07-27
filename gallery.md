---
layout: default
title: Gallery
permalink: /gallery/
---

<!-- 委託圖區域 -->
<div class="section-title">
  <h2 class="lang-en">Commissioned Works</h2>
  <h2 class="lang-zh">委託作品</h2>
  <h2 class="lang-fr">Œuvres Commandées</h2>
</div>

<div class="content gallery-description">
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

<div class="grid" id="commissioned-grid">
  {% for item in site.data.gallery %}
    {% unless item.gifted %}
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
    {% endunless %}
  {% endfor %}
</div>

<!-- 贈圖區域 -->
<div class="section-title">
  <h2 class="lang-en">Gifted Works</h2>
  <h2 class="lang-zh">繪師贈圖</h2>
  <h2 class="lang-fr">Œuvres Offertes</h2>
</div>

<div class="content gallery-description">
  <p class="lang-en">
    Gifted works from friends around the world. Thank you all!
  </p>
  <p class="lang-zh">
    來自各方朋友的贈圖，感謝你們
  </p>
  <p class="lang-fr">
    Œuvres offertes par des amis du monde entier. Merci à tous !
  </p>
</div>

<div class="grid" id="gifted-grid">
  {% for item in site.data.gallery %}
    {% if item.gifted %}
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
    {% endif %}
  {% endfor %}
</div>

<script src="/assets/js/gallery.js"></script>
