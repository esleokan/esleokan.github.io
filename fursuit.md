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
  <p class="lang-fr">
    Fursuit fabriqué par <a href="https://www.furmony.com/" class="telegram-link" target="_blank" rel="noopener noreferrer">
    Furmony studio</a>
  </p>
</div>

<div class="fursuit-grid" id="fursuit-grid" style="opacity: 0;">
  {% for item in site.data.fursuit %}
    <div class="grid-item fade-in" tabindex="0" data-index="{{ forloop.index0 }}">
      <img src="{{ site.baseurl }}{{ item.image }}" alt="{{ item.title | default:'Loyn Fursuit' }}">
      <div class="overlay">
        {% if item.title %}
        <div class="title">{{ item.title }}</div>
        {% endif %}
        <div class="photographer lang-en">📷 {{ item.photographer }}</div>
        <div class="photographer lang-zh">📷 {{ item.photographer }}</div>
        <div class="photographer lang-fr">📷 {{ item.photographer }}</div>
        <div class="date lang-en">📅 {{ item.date_taken }}</div>
        <div class="date lang-zh">📅 {{ item.date_taken }}</div>
        <div class="date lang-fr">📅 {{ item.date_taken }}</div>
        {% if item.description %}
        <div class="description lang-en">{{ item.description }}</div>
        {% if item.description_zh %}
        <div class="description lang-zh">{{ item.description_zh }}</div>
        {% else %}
        <div class="description lang-zh">{{ item.description }}</div>
        {% endif %}
        {% if item.description_fr %}
        <div class="description lang-fr">{{ item.description_fr }}</div>
        {% else %}
        <div class="description lang-fr">{{ item.description }}</div>
        {% endif %}
        {% endif %}
      </div>
    </div>
  {% endfor %}
</div>

<script src="/assets/js/gallery.js"></script>
<script>
// 隨機排序毛毛照片
function shuffleFursuit() {
  const grid = document.getElementById('fursuit-grid');
  if (!grid) {
    return;
  }
  
  const items = Array.from(grid.children);
  
  if (items.length === 0) {
    return;
  }
  
  // 簡單的隨機排序
  for (let i = items.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    grid.appendChild(items[j]);
  }
  
  // 排序完成後顯示
  grid.style.opacity = '1';
}

// 頁面載入時執行隨機排序
document.addEventListener('DOMContentLoaded', shuffleFursuit);

// 如果頁面已經載入，直接執行
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', shuffleFursuit);
} else {
  shuffleFursuit();
}
</script>
