<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-logo-section">
          <div class="footer-logo">
            <router-link to="/">
              <img src="@/assets/images/logo.png" alt="乘灼平台" />
              <span class="logo-text">乘灼</span>
            </router-link>
          </div>
          <p class="footer-description">
            传承乘灼精神，弘扬中华文明
          </p>
          <div class="footer-social">
            <router-link to="#" class="social-link" aria-label="微信">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M7.5 7.5C5.01 7.5 3 9.51 3 12C3 14.49 5.01 16.5 7.5 16.5C7.84 16.5 8.17 16.45 8.5 16.36V19.5L13.5 16.5C15.99 16.5 18 14.49 18 12C18 9.51 15.99 7.5 13.5 7.5C11.01 7.5 9 9.51 9 12C9 12.19 9.01 12.38 9.03 12.57C9.03 12.62 9.03 12.66 9.04 12.71C9.42 12.3 10.06 12 10.8 12C12.49 12 13.8 13.31 13.8 15C13.8 15.11 13.79 15.22 13.78 15.33C12.83 15.92 11.57 16.2 10.2 16.2C6.41 16.2 3 12.79 3 9C3 5.21 6.41 1.8 10.2 1.8C15.02 1.8 18.6 5.38 18.6 10.2C18.6 10.73 18.59 11.26 18.56 11.78C19.78 11.22 21 10.09 21 8.7C21 6.51 19.16 4.66 16.94 4.66C15.86 4.66 14.83 5.13 14.13 5.94C13.59 5.88 13.04 5.84 12.5 5.84C8.71 5.84 5.4 9.15 5.4 12.94C5.4 13.41 5.42 13.88 5.46 14.34C4.75 14.21 4.09 14.02 3.45 13.76V12C3.45 9.51 5.46 7.5 7.95 7.5Z" fill="currentColor" />
              </svg>
            </router-link>
            <router-link to="#" class="social-link" aria-label="微博">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M17.68 4.32C16.23 2.87 14.25 2 12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 9.75 21.13 7.77 19.68 6.32L12 14L4.32 6.32C5.77 4.87 7.75 4 10 4H14L17.68 4.32Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </router-link>
            <router-link to="#" class="social-link" aria-label="抖音">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 18C15.31 18 18 15.31 18 12C18 8.69 15.31 6 12 6C8.69 6 6 8.69 6 12C6 15.31 8.69 18 12 18Z" stroke="currentColor" stroke-width="2" />
                <path d="M19 12C19 15.87 15.87 19 12 19C8.13 19 5 15.87 5 12C5 8.13 8.13 5 12 5C15.87 5 19 8.13 19 12Z" stroke="currentColor" stroke-width="2" />
                <circle cx="16" cy="8" r="1" fill="currentColor" />
                <path d="M12 2V4" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                <path d="M12 20V22" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                <path d="M4.93 4.93L6.34 6.34" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                <path d="M17.66 17.66L19.07 19.07" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                <path d="M2 12H4" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                <path d="M20 12H22" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                <path d="M4.93 19.07L6.34 17.66" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                <path d="M17.66 6.34L19.07 4.93" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
              </svg>
            </router-link>
          </div>
        </div>
        
        <div class="footer-links-section">
          <h3 class="footer-heading">快速链接</h3>
          <ul class="footer-links">
            <li>
              <router-link to="/" class="footer-link">首页</router-link>
            </li>
            <li>
              <router-link to="/cultures" class="footer-link">乘灼</router-link>
            </li>
            <li>
              <router-link to="/regions" class="footer-link">地区风情</router-link>
            </li>
            <li>
              <router-link to="/stories" class="footer-link">传承故事</router-link>
            </li>
            <li>
              <router-link to="/videos" class="footer-link">精彩视频</router-link>
            </li>
          </ul>
        </div>
        
        <div class="footer-contact-section">
          <h3 class="footer-heading">联系我们</h3>
          <ul class="footer-contact-info">
            <li class="contact-item">
              <svg class="contact-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.58 20 4 16.42 4 12C4 7.58 7.58 4 12 4C16.42 4 20 7.58 20 12C20 16.42 16.42 20 12 20ZM12 15C13.66 15 15 13.66 15 12C15 10.34 13.66 9 12 9C10.34 9 9 10.34 9 12C9 13.66 10.34 15 12 15Z" fill="currentColor" />
              </svg>
              <span>北京市朝阳区乘灼大厦</span>
            </li>
            <li class="contact-item">
              <svg class="contact-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <span>+86 123 4567 8910</span>
            </li>
            <li class="contact-item">
              <svg class="contact-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 8L10 13L21 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <span>info@minzuwenhua.com</span>
            </li>
          </ul>
        </div>
      </div>
      
      <div class="footer-bottom">
        <div class="footer-copyright">
          <p>&copy; 2024 乘灼平台. 保留所有权利.</p>
        </div>
        <div class="footer-terms">
          <router-link to="#" class="terms-link">隐私政策</router-link>
          <router-link to="#" class="terms-link">使用条款</router-link>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
// Footer component
</script>

<style lang="scss">
.footer {
  background-color: #87CEEB;
  padding: 3rem 0 2rem;
  color: #2c3e50;
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.5rem;
  }
  
  .footer-content {
    display: grid;
    grid-template-columns: 1fr;
    gap: 2rem;
    margin-bottom: 2rem;
    
    @media (min-width: 768px) {
      grid-template-columns: repeat(3, 1fr);
    }
  }
  
  .footer-logo-section {
    .footer-logo {
      margin-bottom: 1rem;
      
      a {
        display: flex;
        align-items: center;
        text-decoration: none;
        gap: 0.75rem;
      }
      
      img {
        height: 32px;
      }
      
      .logo-text {
        font-size: 1.25rem;
        font-weight: 700;
        color: #212529;
      }
    }
    
    .footer-description {
      margin-bottom: 1.5rem;
      line-height: 1.6;
    }
    
    .footer-social {
      display: flex;
      gap: 1rem;
      
      .social-link {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #e9ecef;
        color: #495057;
        transition: all 0.3s ease;
        
        &:hover {
          background-color: #0d6efd;
          color: white;
          transform: translateY(-3px);
        }
        
        svg {
          width: 20px;
          height: 20px;
        }
      }
    }
  }
  
  .footer-links-section {
    .footer-heading {
      font-size: 1.125rem;
      font-weight: 600;
      color: #212529;
      margin-bottom: 1rem;
      position: relative;
      padding-bottom: 0.5rem;
      
      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 40px;
        height: 2px;
        background-color: #0d6efd;
      }
    }
    
    .footer-links {
      list-style: none;
      margin: 0;
      padding: 0;
      
      li {
        margin-bottom: 0.75rem;
      }
      
      .footer-link {
        color: #495057;
        text-decoration: none;
        transition: color 0.3s ease;
        display: inline-block;
        
        &:hover {
          color: #0d6efd;
          transform: translateX(3px);
        }
      }
    }
  }
  
  .footer-contact-section {
    .footer-heading {
      font-size: 1.125rem;
      font-weight: 600;
      color: #212529;
      margin-bottom: 1rem;
      position: relative;
      padding-bottom: 0.5rem;
      
      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 40px;
        height: 2px;
        background-color: #0d6efd;
      }
    }
    
    .footer-contact-info {
      list-style: none;
      margin: 0;
      padding: 0;
      
      .contact-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        margin-bottom: 1rem;
        
        .contact-icon {
          width: 20px;
          height: 20px;
          color: #0d6efd;
          margin-top: 2px;
          flex-shrink: 0;
        }
      }
    }
  }
  
  .footer-bottom {
    border-top: 1px solid #dee2e6;
    padding-top: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    
    @media (min-width: 768px) {
      flex-direction: row;
      justify-content: space-between;
      align-items: center;
    }
    
    .footer-copyright {
      text-align: center;
      
      @media (min-width: 768px) {
        text-align: left;
      }
      
      p {
        margin: 0;
        font-size: 0.875rem;
      }
    }
    
    .footer-terms {
      display: flex;
      justify-content: center;
      gap: 1.5rem;
      
      .terms-link {
        color: #495057;
        text-decoration: none;
        font-size: 0.875rem;
        transition: color 0.3s ease;
        
        &:hover {
          color: #0d6efd;
        }
      }
    }
  }
}
</style>
