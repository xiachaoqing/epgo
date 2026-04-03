<?php defined('IN_MET') or exit('No permission'); ?>
<include file="head.php" />

<style>
/* 演讲视频播放页面样式 */
.epgo-speech-banner {
  background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
  color: white;
  padding: 60px 0;
  text-align: center;
}

.epgo-speech-banner h1 {
  font-size: 48px;
  font-weight: 800;
  margin: 0 0 20px;
}

.epgo-speech-banner p {
  font-size: 18px;
  margin: 0;
  opacity: 0.95;
}

/* 视频容器 */
.epgo-video-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
  margin-bottom: 30px;
  border: 1px solid #e5e7eb;
}

.epgo-video-card:hover {
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.12);
  transform: translateY(-4px);
}

.epgo-video-thumbnail {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  overflow: hidden;
  background: #000;
}

.epgo-video-thumbnail iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
}

.epgo-video-player-btn {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  background: rgba(255,255,255,0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  z-index: 1;
}

.epgo-video-player-btn:hover {
  background: white;
  transform: translate(-50%, -50%) scale(1.1);
}

.epgo-video-player-btn::after {
  content: '';
  width: 0;
  height: 0;
  border-left: 25px solid #2563eb;
  border-top: 15px solid transparent;
  border-bottom: 15px solid transparent;
  margin-left: 4px;
}

.epgo-video-info {
  padding: 24px;
}

.epgo-video-info h3 {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.epgo-video-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: #9ca3af;
  margin-bottom: 12px;
}

.epgo-video-desc {
  color: #6b7280;
  font-size: 14px;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.epgo-video-tags {
  margin-top: 12px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.epgo-video-tag {
  display: inline-block;
  background: #eff6ff;
  color: #2563eb;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  text-decoration: none;
  transition: all 0.2s;
}

.epgo-video-tag:hover {
  background: #2563eb;
  color: white;
}

/* 视频网格布局 */
.epgo-videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

/* 分类筛选 */
.epgo-filter-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 30px;
  flex-wrap: wrap;
  justify-content: center;
}

.epgo-filter-btn {
  padding: 10px 20px;
  border: 2px solid #e5e7eb;
  background: white;
  color: #6b7280;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
  font-size: 14px;
}

.epgo-filter-btn:hover,
.epgo-filter-btn.active {
  border-color: #2563eb;
  background: #2563eb;
  color: white;
}

/* 响应式 */
@media (max-width: 768px) {
  .epgo-speech-banner h1 {
    font-size: 32px;
  }

  .epgo-speech-banner p {
    font-size: 14px;
  }

  .epgo-videos-grid {
    grid-template-columns: 1fr;
  }

  .epgo-video-info {
    padding: 16px;
  }

  .epgo-filter-tabs {
    justify-content: flex-start;
    overflow-x: auto;
    padding-bottom: 8px;
  }
}

@media (max-width: 480px) {
  .epgo-speech-banner h1 {
    font-size: 24px;
  }

  .epgo-filter-btn {
    padding: 8px 14px;
    font-size: 12px;
  }
}
</style>

<main class="met-news animsition">
  <!-- 标题区 -->
  <div class="epgo-speech-banner">
    <div class="container">
      <h1>英文演讲播放</h1>
      <p>精选世界名人演讲，提升英语听力和表达能力</p>
    </div>
  </div>

  <div class="container" style="padding: 60px 0;">
    <!-- 分类筛选 -->
    <div class="epgo-filter-tabs">
      <button class="epgo-filter-btn active" onclick="epgoFilterByType('all')">全部</button>
      <button class="epgo-filter-btn" onclick="epgoFilterByType('ted')">TED演讲</button>
      <button class="epgo-filter-btn" onclick="epgoFilterByType('bbc')">BBC纪录</button>
      <button class="epgo-filter-btn" onclick="epgoFilterByType('oxford')">牛津讲座</button>
      <button class="epgo-filter-btn" onclick="epgoFilterByType('comedy')">英式喜剧</button>
    </div>

    <!-- 视频网格 -->
    <div class="epgo-videos-grid">
      <!-- 从MetInfo获取视频列表 -->
      <tag action='list' type='product' num='12'>
      <div class="epgo-video-card" data-type="ted">
        <div class="epgo-video-thumbnail">
          <if value="$v['imgurl']">
            <img src="{$v.imgurl|thumb:400,225}" alt="{$v.title}" style="width:100%; height:100%; object-fit:cover;">
          <else/>
            <div style="width:100%; height:100%; background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);"></div>
          </if>
          <!-- 播放按钮 -->
          <div class="epgo-video-player-btn" onclick="epgoPlayVideo('{$v.url}', '{$v.title}')"></div>
        </div>

        <div class="epgo-video-info">
          <h3>{$v.title}</h3>

          <div class="epgo-video-meta">
            <span><i class="icon wb-calendar" style="margin-right:4px;"></i>{$v.updatetime|date='Y-m-d'}</span>
            <span><i class="icon wb-eye" style="margin-right:4px;"></i>{$v.hits}</span>
          </div>

          <p class="epgo-video-desc">{$v.description}</p>

          <div class="epgo-video-tags">
            <a href="#" class="epgo-video-tag">英文演讲</a>
            <a href="#" class="epgo-video-tag">{$v.issue}</a>
          </div>
        </div>
      </div>
      </tag>
    </div>

    <!-- 加载更多按钮 -->
    <div style="text-align:center; margin-top:40px;">
      <button onclick="epgoLoadMoreVideos()" style="padding:14px 32px; background:#2563eb; color:white; border:none; border-radius:8px; font-weight:700; cursor:pointer; font-size:16px; transition:all 0.3s;">
        加载更多视频 ↓
      </button>
    </div>
  </div>

  <!-- 视频播放弹窗 -->
  <div id="epgo-video-modal" style="display:none; position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.8); z-index:9999; flex-direction:column; align-items:center; justify-content:center;">
    <div style="position:relative; width:90%; max-width:900px; background:black; border-radius:12px; overflow:hidden;">
      <!-- 关闭按钮 -->
      <button onclick="epgoCloseVideo()" style="position:absolute; top:10px; right:10px; background:rgba(255,255,255,0.9); border:none; width:40px; height:40px; border-radius:50%; font-size:28px; cursor:pointer; z-index:10; transition:all 0.3s; color:#333;" onmouseover="this.style.background='white'" onmouseout="this.style.background='rgba(255,255,255,0.9)'">×</button>

      <!-- 视频容器 -->
      <div id="epgo-video-container" style="position:relative; width:100%; padding-bottom:56.25%;">
        <iframe id="epgo-video-iframe"
                style="position:absolute; top:0; left:0; width:100%; height:100%; border:none;"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen>
        </iframe>
      </div>

      <!-- 视频标题 -->
      <div style="padding:16px; color:white; text-align:center;">
        <h3 id="epgo-video-title" style="margin:0; font-size:18px; font-weight:700;"></h3>
      </div>
    </div>
  </div>
</main>

<script>
(function(){
  // 视频播放功能
  window.epgoPlayVideo = function(url, title) {
    var modal = document.getElementById('epgo-video-modal');
    var iframe = document.getElementById('epgo-video-iframe');
    var titleEl = document.getElementById('epgo-video-title');

    // 识别视频URL类型并转换为嵌入链接
    var embedUrl = url;
    if (url.includes('youtube.com') || url.includes('youtu.be')) {
      var videoId = url.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=))([^\s&]+)/)[1];
      embedUrl = 'https://www.youtube.com/embed/' + videoId + '?autoplay=1';
    } else if (url.includes('youku.com')) {
      // 优酷视频处理
      embedUrl = url.replace(/watch\//, 'embed/').replace(/\.html/, '');
    } else if (url.includes('vimeo.com')) {
      var vimeoId = url.match(/vimeo\.com\/(\d+)/)[1];
      embedUrl = 'https://player.vimeo.com/video/' + vimeoId;
    }

    iframe.src = embedUrl;
    titleEl.innerText = title;
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  };

  // 关闭视频播放
  window.epgoCloseVideo = function() {
    var modal = document.getElementById('epgo-video-modal');
    var iframe = document.getElementById('epgo-video-iframe');
    iframe.src = '';
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
  };

  // 视频分类筛选
  window.epgoFilterByType = function(type) {
    var btns = document.querySelectorAll('.epgo-filter-btn');
    var cards = document.querySelectorAll('.epgo-video-card');

    btns.forEach(function(btn) {
      btn.classList.remove('active');
    });
    event.target.classList.add('active');

    if (type === 'all') {
      cards.forEach(function(card) {
        card.style.display = 'block';
      });
    } else {
      cards.forEach(function(card) {
        if (card.getAttribute('data-type') === type) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    }
  };

  // 加载更多
  window.epgoLoadMoreVideos = function() {
    alert('更多视频加载中...');
    // 实现分页加载逻辑
  };

  // 点击弹窗外部关闭
  document.getElementById('epgo-video-modal').addEventListener('click', function(e) {
    if (e.target === this) {
      epgoCloseVideo();
    }
  });

  // ESC键关闭
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      epgoCloseVideo();
    }
  });
})();
</script>

<include file="foot.php" />
