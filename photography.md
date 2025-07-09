---
layout: default
title: Photography
permalink: /photography/
---
<div class="content">
  <p>
  Sony A7IV + 50mm f1.4 GM  
  </p>
</div>

<div class="fursuit-grid" id="photography-grid">
  {% for item in site.data.photography %}
    <div class="grid-item fade-in" tabindex="0" data-index="{{ forloop.index0 }}">
      <img src="{{ site.baseurl }}{{ item.image }}" alt="{{ item.title | default:'Loyn Photography' }}">
      <div class="overlay">
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
<script>
// 簡化的隨機排序攝影作品
function shufflePhotography() {
  const grid = document.getElementById('photography-grid');
  if (!grid) {
    console.log('找不到 photography-grid');
    return;
  }
  
  const items = Array.from(grid.children);
  console.log('找到', items.length, '張圖片');
  
  if (items.length === 0) {
    console.log('沒有圖片項目');
    return;
  }
  
  // 簡單的隨機排序
  for (let i = items.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    grid.appendChild(items[j]);
  }
  
  console.log('隨機排序完成');
}

// 頁面載入時執行隨機排序
document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM 載入完成，開始隨機排序');
  shufflePhotography();
});

// 如果頁面已經載入，直接執行
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', shufflePhotography);
} else {
  console.log('頁面已載入，直接執行隨機排序');
  shufflePhotography();
}
</script> 