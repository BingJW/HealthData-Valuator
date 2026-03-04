<!-- frontend/src/views/Home.vue -->
<template>
  <div class="home-container">
    <!-- 导航栏 -->
    <el-header class="header">
      <div class="header-content">
        <div class="logo">
          <h1>医疗数据资产价值计量器</h1>
        </div>
        <div class="nav-links">
          <el-button type="text" @click="scrollTo('features')">产品亮点</el-button>
          <el-button type="text" @click="scrollTo('team')">团队简介</el-button>
          <el-button type="text" @click="scrollTo('contact')">联系我们</el-button>
        </div>
        <div class="auth-buttons">
          <el-button @click="$router.push('/login')">登录</el-button>
          <el-button type="primary" @click="$router.push('/register')">免费注册</el-button>
        </div>
      </div>
    </el-header>

    <!-- 主内容区 -->
    <el-main>
      <!-- 英雄区域 -->
      <section class="hero-section">
        <div class="hero-content">
          <h2>科学评估医疗数据价值</h2>
          <p class="subtitle">基于9大指标体系，为医院提供专业的数据资产评估服务</p>
          <div class="hero-actions">
            <el-button type="primary" size="large" @click="$router.push('/register')">
              立即体验
            </el-button>
            <el-button size="large" @click="scrollTo('features')">了解更多</el-button>
          </div>
        </div>
      </section>

      <!-- 产品亮点 -->
      <section id="features" class="features-section">
        <h3>产品亮点与价值</h3>
        <div class="features-grid">
          <el-card class="feature-card">
            <template #header>
              <div class="card-header">
                <span class="feature-icon">📊</span>
                <h4>科学评估体系</h4>
              </div>
            </template>
            <p>基于9大成本维度，建立全面的医疗数据资产价值评估模型，涵盖数据全生命周期成本。</p>
          </el-card>
          
          <el-card class="feature-card">
            <template #header>
              <div class="card-header">
                <span class="feature-icon">⚡</span>
                <h4>快速评估</h4>
              </div>
            </template>
            <p>在线填写，即时计算，3分钟内完成数据资产评估，生成专业评估报告。</p>
          </el-card>
          
          <el-card class="feature-card">
            <template #header>
              <div class="card-header">
                <span class="feature-icon">🔒</span>
                <h4>数据安全</h4>
              </div>
            </template>
            <p>采用加密传输和存储，确保医院数据安全，评估过程不保存原始业务数据。</p>
          </el-card>
          
          <el-card class="feature-card">
            <template #header>
              <div class="card-header">
                <span class="feature-icon">📈</span>
                <h4>可视化报告</h4>
              </div>
            </template>
            <p>生成可视化评估报告，清晰展示各项成本构成，支持PDF导出和打印。</p>
          </el-card>
        </div>
      </section>

      <!-- 团队简介 -->
      <section id="team" class="team-section">
        <h3>团队简介</h3>
        <el-card class="team-card">
          <p>我们是一支专注于医疗数据价值评估的专业团队，由资深的数据科学家、医疗行业专家和软件工程师组成。</p>
          <p>团队深耕医疗数据领域多年，深刻理解医院数据管理需求，致力于通过技术创新帮助医疗机构挖掘数据资产价值。</p>
          <p>目前已为全国超过50家三甲医院提供数据资产评估咨询服务，积累了丰富的行业经验。</p>
        </el-card>
      </section>

      <!-- 注册入口 -->
      <section class="cta-section">
        <h3>开始评估您的医疗数据资产价值</h3>
        <p>免费注册，立即体验专业的医疗数据资产评估服务</p>
        <el-button type="primary" size="large" @click="$router.push('/register')">
          免费注册
        </el-button>
      </section>

      <!-- 联系我们 -->
      <section id="contact" class="contact-section">
        <h3>联系我们</h3>
        <p>邮箱: xxx</p>
        <p>电话: xxx</p>
        <p>地址: xxx</p>
      </section>
    </el-main>

    <!-- 页脚 -->
    <el-footer class="footer">
      <p>© 2026 医疗数据资产价值计量器. All rights reserved.</p>
    </el-footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const scrollTo = (id) => {
  const element = document.getElementById(id)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #fff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.logo h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #409EFF;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.auth-buttons {
  display: flex;
  gap: 10px;
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 100px 20px;
  text-align: center;
}

.hero-content h2 {
  font-size: 3rem;
  margin-bottom: 20px;
}

.subtitle {
  font-size: 1.2rem;
  margin-bottom: 40px;
  opacity: 0.9;
}

.hero-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.features-section, .team-section, .cta-section, .contact-section {
  max-width: 1200px;
  margin: 60px auto;
  padding: 0 20px;
}

.features-section h3, .team-section h3, .cta-section h3, .contact-section h3 {
  text-align: center;
  margin-bottom: 40px;
  font-size: 2rem;
  color: #333;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  margin-top: 40px;
}

.feature-card {
  height: 100%;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.feature-icon {
  font-size: 1.5rem;
}

.team-card {
  text-align: center;
  padding: 40px;
}

.cta-section {
  text-align: center;
  background-color: #f5f7fa;
  padding: 60px 20px;
  border-radius: 10px;
}

.contact-section {
  text-align: center;
  padding: 40px 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
}

.footer {
  text-align: center;
  padding: 20px;
  background-color: #333;
  color: white;
  margin-top: auto;
}
</style>


