import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'AI Daily News',
  description: 'AI/编程/科技/创业/经济/数码/新能源汽车/数码影像 每日资讯',
  lang: 'zh-CN',
  base: '/ai-daily-news/',
  
  themeConfig: {
    logo: '/logo.svg',
    
    nav: [
      { text: '首页', link: '/' },
      { text: '今日', link: '/daily/current' },
      { text: '归档', link: '/daily/archive' },
      { text: 'GitHub', link: 'https://github.com/spidereast/ai-daily-news' }
    ],
    
    sidebar: {
      '/daily/': [
        {
          text: '历史日报',
          items: [
            { text: '最新', link: '/daily/current' },
            { text: '归档', link: '/daily/archive' }
          ]
        }
      ]
    },
    
    socialLinks: [
      { icon: 'github', link: 'https://github.com/spidereast/ai-daily-news' }
    ],
    
    footer: {
      message: '基于 VitePress 构建 | 内容由 AI 自动生成',
      copyright: 'Copyright © 2025 AI Daily News'
    },
    
    search: {
      provider: 'local'
    }
  },
  
  // 构建配置
  build: {
    rollupOptions: {
      output: {
        entryFileNames: `assets/[name].js`,
        chunkFileNames: `assets/[name].js`,
        assetFileNames: `assets/[name].[ext]`
      }
    }
  }
})