<template>
  <div class="home">
    <!-- 现代化英雄区域 -->
    <section id="hero" class="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <!-- 动态背景粒子 -->
      <div class="absolute inset-0">
        <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-blue-500/10 via-transparent to-transparent"></div>
        <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div class="absolute bottom-1/4 right-1/4 w-64 h-64 bg-blue-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>
      
      <!-- 内容区域 -->
      <div class="container mx-auto px-6 relative z-10">
        <div class="grid lg:grid-cols-2 gap-16 items-center">
          <!-- 文字内容 -->
          <div class="space-y-8">
            <div class="space-y-6">
              <div class="inline-flex items-center gap-3 px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full border border-white/20">
                <div class="w-2 h-2 bg-green-400 rounded-full animate-ping"></div>
                <span class="text-sm text-white/80">探索中华文化瑰宝</span>
              </div>
              
              <h1 class="text-5xl lg:text-7xl font-bold text-white leading-tight">
                传承
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">千年文化</span>
                <br>
                展现
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-500">民族风情</span>
              </h1>
              
              <p class="text-xl text-gray-300 leading-relaxed max-w-2xl">
                沉浸式体验中华56个民族的独特文化魅力，从传统艺术到现代创新，
                感受跨越时空的文化对话与传承。
              </p>
            </div>
            
            <!-- 交互式按钮组 -->
            <div class="flex flex-col sm:flex-row gap-4">
              <button 
                @click="scrollToSection('cultures')"
                class="group relative overflow-hidden bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white px-8 py-4 rounded-xl font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-2xl"
              >
                <span class="relative z-10 flex items-center gap-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                  </svg>
                  开始探索
                </span>
                <div class="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent transform -skew-x-12 translate-x-[-150%] group-hover:translate-x-[150%] transition-transform duration-1000"></div>
              </button>
              
              <button 
                @click="scrollToSection('about')"
                class="group border-2 border-white/30 hover:border-white/50 text-white hover:bg-white/10 px-8 py-4 rounded-xl font-medium backdrop-blur-sm transition-all duration-300 transform hover:scale-105"
              >
                <span class="flex items-center gap-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                  </svg>
                  了解更多
                </span>
              </button>
            </div>
            
            <!-- 统计数据 -->
            <div class="flex gap-8 pt-8 border-t border-white/10">
              <div class="text-center">
                <div class="text-3xl font-bold text-white">56+</div>
                <div class="text-sm text-gray-400">民族数量</div>
              </div>
              <div class="text-center">
                <div class="text-3xl font-bold text-white">5000+</div>
                <div class="text-sm text-gray-400">文化项目</div>
              </div>
              <div class="text-center">
                <div class="text-3xl font-bold text-white">100+</div>
                <div class="text-sm text-gray-400">地区覆盖</div>
              </div>
            </div>
          </div>
          
          <!-- 3D视觉元素 -->
          <div class="relative">
            <div class="relative z-10">
              <div class="w-full h-96 bg-gradient-to-br from-cyan-500/20 to-purple-500/20 rounded-3xl p-8 backdrop-blur-xl border border-white/10 shadow-2xl transform rotate-3 hover:rotate-0 transition-transform duration-700">
                <img 
                  src="https://images.unsplash.com/photo-1545569341-9eb8b30979d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80" 
                  alt="中华文化展示" 
                  class="w-full h-full object-cover rounded-2xl shadow-2xl"
                  loading="lazy"
                >
              </div>
            </div>
            
            <!-- 浮动装饰元素 -->
            <div class="absolute -top-4 -left-4 w-20 h-20 bg-cyan-400/30 rounded-full blur-xl animate-bounce"></div>
            <div class="absolute -bottom-4 -right-4 w-24 h-24 bg-purple-400/30 rounded-full blur-xl animate-bounce delay-500"></div>
            <div class="absolute top-1/2 -right-8 w-16 h-16 bg-pink-400/20 rounded-full blur-xl animate-pulse"></div>
          </div>
        </div>
      </div>
      
      <!-- 滚动指示器 -->
      <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div class="w-6 h-10 border-2 border-white/30 rounded-full flex justify-center">
          <div class="w-1 h-3 bg-white/50 rounded-full mt-2 animate-pulse"></div>
        </div>
      </div>
    </section>

    <!-- 现代化民族文化展示区域 -->
    <section id="cultures" class="py-20 bg-gradient-to-br from-slate-50 via-white to-slate-100">
      <div class="container mx-auto px-6">
        <!-- 标题区域 -->
        <div class="text-center mb-20">
          <div class="inline-flex items-center gap-3 px-6 py-3 bg-white/80 backdrop-blur-sm rounded-full border border-gray-200 shadow-sm mb-6">
            <div class="w-3 h-3 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full animate-pulse"></div>
            <span class="text-sm font-medium text-gray-700">多元文化探索</span>
          </div>
          
          <h3 class="text-4xl lg:text-6xl font-bold text-gray-900 mb-6">
            民族文化
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-pink-600">瑰宝</span>
          </h3>
          
          <p class="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            中华56个民族，每个民族都有其独特的文化传统和艺术表现形式，
            共同构成了丰富多彩的中华文化宝库。
          </p>
        </div>
        
        <!-- 现代化卡片网格 -->
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <!-- 藏族文化卡片 -->
          <div class="group relative bg-white rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-4 border border-gray-100">
            <!-- 卡片装饰 -->
            <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-purple-500 to-cyan-500"></div>
            
            <!-- 图片区域 -->
            <div class="relative overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1580136579312-94651dfd596d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80" 
                alt="藏族文化" 
                class="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-700"
                loading="lazy"
              >
              <!-- 渐变遮罩 -->
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
              
              <!-- 标签 -->
              <div class="absolute top-4 left-4">
                <span class="px-3 py-1 bg-white/90 backdrop-blur-sm text-purple-600 text-sm font-medium rounded-full">
                  雪域文化
                </span>
              </div>
              
              <!-- 标题 -->
              <div class="absolute bottom-6 left-6 text-white">
                <h4 class="text-2xl font-bold mb-2">藏族文化</h4>
                <p class="text-sm opacity-90">神秘的高原文明</p>
              </div>
            </div>
            
            <!-- 内容区域 -->
            <div class="p-6">
              <p class="text-gray-600 mb-6 leading-relaxed">
                藏族文化源远流长，包括藏传佛教、唐卡艺术、藏戏等丰富的文化遗产，
                展现了雪域高原独特的宗教与艺术魅力。
              </p>
              
              <!-- 交互式按钮 -->
              <button class="group relative w-full bg-gradient-to-r from-purple-500 to-cyan-500 hover:from-purple-600 hover:to-cyan-600 text-white py-3 rounded-xl font-medium transition-all duration-300 overflow-hidden">
                <span class="relative z-10 flex items-center justify-center gap-2">
                  探索详情
                  <svg class="w-4 h-4 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                  </svg>
                </span>
                <div class="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent transform -skew-x-12 translate-x-[-150%] group-hover:translate-x-[150%] transition-transform duration-1000"></div>
              </button>
            </div>
          </div>

          <!-- 彝族文化卡片 -->
          <div class="group relative bg-white rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-4 border border-gray-100">
            <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-orange-500 to-red-500"></div>
            
            <div class="relative overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1576086213369-97a306d36557?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80" 
                alt="彝族文化" 
                class="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-700"
                loading="lazy"
              >
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
              
              <div class="absolute top-4 left-4">
                <span class="px-3 py-1 bg-white/90 backdrop-blur-sm text-orange-600 text-sm font-medium rounded-full">
                  火的文化
                </span>
              </div>
              
              <div class="absolute bottom-6 left-6 text-white">
                <h4 class="text-2xl font-bold mb-2">彝族文化</h4>
                <p class="text-sm opacity-90">热情的民族风情</p>
              </div>
            </div>
            
            <div class="p-6">
              <p class="text-gray-600 mb-6 leading-relaxed">
                彝族拥有丰富的火把节文化、彝族年、毕摩文化等独特的民族传统，
                展现了彝族人民热情奔放的生活态度。
              </p>
              
              <button class="group relative w-full bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 text-white py-3 rounded-xl font-medium transition-all duration-300 overflow-hidden">
                <span class="relative z-10 flex items-center justify-center gap-2">
                  探索详情
                  <svg class="w-4 h-4 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                  </svg>
                </span>
                <div class="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent transform -skew-x-12 translate-x-[-150%] group-hover:translate-x-[150%] transition-transform duration-1000"></div>
              </button>
            </div>
          </div>

          <!-- 傣族文化卡片 -->
          <div class="group relative bg-white rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-4 border border-gray-100">
            <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-green-500 to-teal-500"></div>
            
            <div class="relative overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1554629947-334ff61d85dc?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80" 
                alt="傣族文化" 
                class="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-700"
                loading="lazy"
              >
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
              
              <div class="absolute top-4 left-4">
                <span class="px-3 py-1 bg-white/90 backdrop-blur-sm text-green-600 text-sm font-medium rounded-full">
                  水的民族
                </span>
              </div>
              
              <div class="absolute bottom-6 left-6 text-white">
                <h4 class="text-2xl font-bold mb-2">傣族文化</h4>
                <p class="text-sm opacity-90">柔美的热带风情</p>
              </div>
            </div>
            
            <div class="p-6">
              <p class="text-gray-600 mb-6 leading-relaxed">
                傣族以泼水节、傣剧、孔雀舞等文化特色闻名，
                展现了热带雨林民族柔情似水的独特魅力与生活智慧。
              </p>
              
              <button class="group relative w-full bg-gradient-to-r from-green-500 to-teal-500 hover:from-green-600 hover:to-teal-600 text-white py-3 rounded-xl font-medium transition-all duration-300 overflow-hidden">
                <span class="relative z-10 flex items-center justify-center gap-2">
                  探索详情
                  <svg class="w-4 h-4 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                  </svg>
                </span>
                <div class="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent transform -skew-x-12 translate-x-[-150%] group-hover:translate-x-[150%] transition-transform duration-1000"></div>
              </button>
            </div>
          </div>
        </div>
        
        <!-- 查看更多按钮 -->
        <div class="text-center mt-12">
          <button class="group inline-flex items-center gap-3 px-8 py-4 bg-white hover:bg-gray-50 text-gray-700 font-medium rounded-xl border border-gray-200 hover:border-gray-300 transition-all duration-300 transform hover:scale-105 shadow-sm hover:shadow-md">
            <span>查看更多民族文化</span>
            <svg class="w-5 h-5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>
        </div>
      </div>
    </section>

    <!-- 现代化地区风情展示区域 -->
    <section id="regions" class="py-20 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 relative overflow-hidden">
      <!-- 背景装饰 -->
      <div class="absolute inset-0 bg-gradient-to-br from-purple-900/20 via-transparent to-cyan-900/20"></div>
      <div class="absolute top-0 left-0 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 right-0 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>
      
      <div class="container mx-auto px-6 relative z-10">
        <!-- 标题区域 -->
        <div class="text-center mb-20">
          <div class="inline-flex items-center gap-3 px-6 py-3 bg-white/10 backdrop-blur-sm rounded-full border border-white/20 mb-6">
            <div class="w-3 h-3 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full animate-pulse"></div>
            <span class="text-sm font-medium text-white/90">地域文化探索</span>
          </div>
          
          <h3 class="text-4xl lg:text-6xl font-bold text-white mb-6">
            地区
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400">风情</span>
          </h3>
          
          <p class="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
            从江南水乡到塞北草原，从巴蜀文化到岭南风情，
            感受不同地域的文化魅力与独特风情。
          </p>
        </div>
        
        <!-- 现代化卡片布局 -->
        <div class="grid lg:grid-cols-2 gap-12 items-center">
          <!-- 江南水乡卡片 -->
          <div class="group relative">
            <!-- 卡片装饰 -->
            <div class="absolute -inset-4 bg-gradient-to-r from-purple-500/20 to-cyan-500/20 rounded-3xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            
            <div class="relative bg-white/10 backdrop-blur-md rounded-3xl overflow-hidden border border-white/20 shadow-2xl transform group-hover:scale-105 transition-all duration-500">
              <!-- 图片区域 -->
              <div class="relative overflow-hidden">
                <img 
                  src="https://images.unsplash.com/photo-1559827260-dc66d52bef19?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80" 
                  alt="江南水乡" 
                  class="w-full h-80 object-cover group-hover:scale-110 transition-transform duration-700"
                  loading="lazy"
                >
                <!-- 渐变遮罩 -->
                <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
                
                <!-- 标签 -->
                <div class="absolute top-6 left-6">
                  <span class="px-4 py-2 bg-white/90 backdrop-blur-sm text-purple-600 text-sm font-semibold rounded-full">
                    水乡文化
                  </span>
                </div>
                
                <!-- 标题 -->
                <div class="absolute bottom-6 left-6 text-white">
                  <h4 class="text-3xl font-bold mb-2">江南水乡</h4>
                  <p class="text-lg opacity-90">烟雨朦胧的诗意</p>
                </div>
              </div>
              
              <!-- 内容区域 -->
              <div class="p-8">
                <p class="text-gray-200 mb-6 leading-relaxed text-lg">
                  小桥流水人家，烟雨朦胧的江南水乡，孕育了独特的吴越文化。
                  这里有着精致的园林艺术、婉约的诗词歌赋和细腻的丝绸工艺。
                </p>
                
                <!-- 交互式按钮 -->
                <button class="group relative w-full bg-gradient-to-r from-purple-500 to-cyan-500 hover:from-purple-600 hover:to-cyan-600 text-white py-4 rounded-xl font-semibold transition-all duration-300 overflow-hidden">
                  <span class="relative z-10 flex items-center justify-center gap-3">
                    探索江南
                    <svg class="w-5 h-5 transform group-hover:translate-x-2 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                    </svg>
                  </span>
                  <div class="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent transform -skew-x-12 translate-x-[-150%] group-hover:translate-x-[150%] transition-transform duration-1000"></div>
                </button>
              </div>
            </div>
          </div>
          
          <!-- 塞北草原卡片 -->
          <div class="group relative">
            <div class="absolute -inset-4 bg-gradient-to-r from-orange-500/20 to-red-500/20 rounded-3xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            
            <div class="relative bg-white/10 backdrop-blur-md rounded-3xl overflow-hidden border border-white/20 shadow-2xl transform group-hover:scale-105 transition-all duration-500">
              <div class="relative overflow-hidden">
                <img 
                  src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80" 
                  alt="塞北草原" 
                  class="w-full h-80 object-cover group-hover:scale-110 transition-transform duration-700"
                  loading="lazy"
                >
                <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
                
                <div class="absolute top-6 left-6">
                  <span class="px-4 py-2 bg-white/90 backdrop-blur-sm text-orange-600 text-sm font-semibold rounded-full">
                    草原文化
                  </span>
                </div>
                
                <div class="absolute bottom-6 left-6 text-white">
                  <h4 class="text-3xl font-bold mb-2">塞北草原</h4>
                  <p class="text-lg opacity-90">豪放的游牧风情</p>
                </div>
              </div>
              
              <div class="p-8">
                <p class="text-gray-200 mb-6 leading-relaxed text-lg">
                  天苍苍，野茫茫，风吹草低见牛羊。塞北草原孕育了豪放的游牧文化，
                  有着独特的蒙古包、马头琴和那达慕大会。
                </p>
                
                <button class="group relative w-full bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 text-white py-4 rounded-xl font-semibold transition-all duration-300 overflow-hidden">
                  <span class="relative z-10 flex items-center justify-center gap-3">
                    探索塞北
                    <svg class="w-5 h-5 transform group-hover:translate-x-2 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                    </svg>
                  </span>
                  <div class="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent transform -skew-x-12 translate-x-[-150%] group-hover:translate-x-[150%] transition-transform duration-1000"></div>
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 查看更多按钮 -->
        <div class="text-center mt-16">
          <button class="group inline-flex items-center gap-4 px-10 py-5 bg-white/10 hover:bg-white/20 backdrop-blur-md text-white font-semibold rounded-2xl border border-white/30 hover:border-white/50 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl">
            <span class="text-lg">探索更多地区文化</span>
            <svg class="w-6 h-6 transform group-hover:translate-x-2 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>
        </div>
      </div>
    </section>

    <!-- 现代化文化展示区域 -->
    <section id="showcase" class="py-20 bg-gradient-to-br from-slate-50 via-white to-slate-100">
      <div class="container mx-auto px-6">
        <!-- 标题区域 -->
        <div class="text-center mb-20">
          <div class="inline-flex items-center gap-3 px-6 py-3 bg-white/80 backdrop-blur-sm rounded-full border border-gray-200 shadow-sm mb-6">
            <div class="w-3 h-3 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full animate-pulse"></div>
            <span class="text-sm font-medium text-gray-700">艺术文化展示</span>
          </div>
          
          <h3 class="text-4xl lg:text-6xl font-bold text-gray-900 mb-6">
            文化
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-green-600 to-emerald-600">展示</span>
          </h3>
          
          <p class="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            欣赏传统绘画、民间工艺、戏曲艺术等丰富多彩的文化表现形式，
            感受中华文化的深厚底蕴与艺术魅力。
          </p>
        </div>
        
        <!-- 现代化图片网格 -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          <!-- 传统绘画卡片 -->
          <div class="group relative overflow-hidden rounded-3xl shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-4">
            <!-- 图片 -->
            <div class="relative overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1541961017774-22349e4a1262?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80" 
                alt="传统绘画" 
                class="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-700"
                loading="lazy"
              >
              <!-- 渐变遮罩 -->
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
              
              <!-- 悬停效果 -->
              <div class="absolute inset-0 bg-gradient-to-br from-green-500/20 to-emerald-500/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              
              <!-- 标签 -->
              <div class="absolute top-4 left-4">
                <span class="px-3 py-1 bg-white/90 backdrop-blur-sm text-green-600 text-sm font-medium rounded-full">
                  绘画艺术
                </span>
              </div>
              
              <!-- 标题 -->
              <div class="absolute bottom-4 left-4 text-white">
                <h4 class="text-xl font-bold">传统绘画</h4>
                <p class="text-sm opacity-90">水墨丹青的意境</p>
              </div>
              
              <!-- 悬停显示的内容 -->
              <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                <div class="text-center text-white p-6">
                  <h5 class="text-2xl font-bold mb-2">传统绘画</h5>
                  <p class="text-sm opacity-90">欣赏水墨丹青的艺术魅力</p>
                  <button class="mt-4 px-6 py-2 bg-white/20 backdrop-blur-sm rounded-full text-white border border-white/30 hover:bg-white/30 transition-all">
                    了解更多
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 民间工艺卡片 -->
          <div class="group relative overflow-hidden rounded-3xl shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-4">
            <div class="relative overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80" 
                alt="民间工艺" 
                class="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-700"
                loading="lazy"
              >
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
              <div class="absolute inset-0 bg-gradient-to-br from-orange-500/20 to-red-500/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              
              <div class="absolute top-4 left-4">
                <span class="px-3 py-1 bg-white/90 backdrop-blur-sm text-orange-600 text-sm font-medium rounded-full">
                  手工艺品
                </span>
              </div>
              
              <div class="absolute bottom-4 left-4 text-white">
                <h4 class="text-xl font-bold">民间工艺</h4>
                <p class="text-sm opacity-90">巧夺天工的技艺</p>
              </div>
              
              <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                <div class="text-center text-white p-6">
                  <h5 class="text-2xl font-bold mb-2">民间工艺</h5>
                  <p class="text-sm opacity-90">感受传统手工艺的魅力</p>
                  <button class="mt-4 px-6 py-2 bg-white/20 backdrop-blur-sm rounded-full text-white border border-white/30 hover:bg-white/30 transition-all">
                    了解更多
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 戏曲艺术卡片 -->
          <div class="group relative overflow-hidden rounded-3xl shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-4">
            <div class="relative overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1547036967-23a11daca0d6?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80" 
                alt="戏曲艺术" 
                class="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-700"
                loading="lazy"
              >
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
              <div class="absolute inset-0 bg-gradient-to-br from-purple-500/20 to-pink-500/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              
              <div class="absolute top-4 left-4">
                <span class="px-3 py-1 bg-white/90 backdrop-blur-sm text-purple-600 text-sm font-medium rounded-full">
                  表演艺术
                </span>
              </div>
              
              <div class="absolute bottom-4 left-4 text-white">
                <h4 class="text-xl font-bold">戏曲艺术</h4>
                <p class="text-sm opacity-90">唱念做打的精髓</p>
              </div>
              
              <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                <div class="text-center text-white p-6">
                  <h5 class="text-2xl font-bold mb-2">戏曲艺术</h5>
                  <p class="text-sm opacity-90">体验传统戏曲的魅力</p>
                  <button class="mt-4 px-6 py-2 bg-white/20 backdrop-blur-sm rounded-full text-white border border-white/30 hover:bg-white/30 transition-all">
                    了解更多
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 传统建筑卡片 -->
          <div class="group relative overflow-hidden rounded-3xl shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-4">
            <div class="relative overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1545569341-9eb8b30979d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80" 
                alt="传统建筑" 
                class="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-700"
                loading="lazy"
              >
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
              <div class="absolute inset-0 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              
              <div class="absolute top-4 left-4">
                <span class="px-3 py-1 bg-white/90 backdrop-blur-sm text-blue-600 text-sm font-medium rounded-full">
                  建筑艺术
                </span>
              </div>
              
              <div class="absolute bottom-4 left-4 text-white">
                <h4 class="text-xl font-bold">传统建筑</h4>
                <p class="text-sm opacity-90">飞檐翘角的韵味</p>
              </div>
              
              <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                <div class="text-center text-white p-6">
                  <h5 class="text-2xl font-bold mb-2">传统建筑</h5>
                  <p class="text-sm opacity-90">欣赏古建筑的独特魅力</p>
                  <button class="mt-4 px-6 py-2 bg-white/20 backdrop-blur-sm rounded-full text-white border border-white/30 hover:bg-white/30 transition-all">
                    了解更多
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 查看更多按钮 -->
        <div class="text-center mt-16">
          <button class="group inline-flex items-center gap-4 px-10 py-5 bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-semibold rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl overflow-hidden">
            <span class="text-lg">探索更多文化展示</span>
            <svg class="w-6 h-6 transform group-hover:translate-x-2 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
            <div class="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent transform -skew-x-12 translate-x-[-150%] group-hover:translate-x-[150%] transition-transform duration-1000"></div>
          </button>
        </div>
      </div>
    </section>

    <!-- 现代化联系我们区域 -->
    <section id="contact" class="py-20 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <div class="container mx-auto px-6">
        <!-- 标题区域 -->
        <div class="text-center mb-20">
          <div class="inline-flex items-center gap-3 px-6 py-3 bg-white/10 backdrop-blur-sm rounded-full border border-white/20 shadow-sm mb-6">
            <div class="w-3 h-3 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full animate-pulse"></div>
            <span class="text-sm font-medium text-white/90">联系我们</span>
          </div>
          
          <h3 class="text-4xl lg:text-6xl font-bold text-white mb-6">
            联系
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">我们</span>
          </h3>
          
          <p class="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
            如果您对我们的民俗文化项目感兴趣，欢迎与我们取得联系，
            我们将为您提供最专业的服务和支持。
          </p>
        </div>
        
        <div class="grid lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
          <!-- 现代化联系表单 -->
          <div class="bg-white/5 backdrop-blur-md rounded-3xl border border-white/10 p-8 shadow-2xl">
            <div class="flex items-center gap-3 mb-8">
              <div class="w-3 h-3 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full"></div>
              <h4 class="text-2xl font-bold text-white">发送消息</h4>
            </div>
            
            <form @submit.prevent="submitForm" class="space-y-6">
              <!-- 姓名输入 -->
              <div class="group">
                <label for="name" class="block text-sm font-medium text-gray-300 mb-3 transition-all duration-300 group-focus-within:text-blue-400">
                  姓名
                </label>
                <div class="relative">
                  <input 
                    type="text" 
                    id="name" 
                    v-model="form.name"
                    class="w-full px-6 py-4 bg-white/5 border border-white/20 rounded-2xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 backdrop-blur-sm"
                    placeholder="请输入您的姓名"
                    required
                  >
                  <div class="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-cyan-500/10 rounded-2xl opacity-0 group-focus-within:opacity-100 transition-opacity duration-300"></div>
                </div>
              </div>
              
              <!-- 邮箱输入 -->
              <div class="group">
                <label for="email" class="block text-sm font-medium text-gray-300 mb-3 transition-all duration-300 group-focus-within:text-blue-400">
                  邮箱
                </label>
                <div class="relative">
                  <input 
                    type="email" 
                    id="email" 
                    v-model="form.email"
                    class="w-full px-6 py-4 bg-white/5 border border-white/20 rounded-2xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 backdrop-blur-sm"
                    placeholder="请输入您的邮箱"
                    required
                  >
                  <div class="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-cyan-500/10 rounded-2xl opacity-0 group-focus-within:opacity-100 transition-opacity duration-300"></div>
                </div>
              </div>
              
              <!-- 文化选择 -->
              <div class="group">
                <label for="culture" class="block text-sm font-medium text-gray-300 mb-3 transition-all duration-300 group-focus-within:text-blue-400">
                  感兴趣的文化
                </label>
                <div class="relative">
                  <select 
                    id="culture" 
                    v-model="form.culture"
                    class="w-full px-6 py-4 bg-white/5 border border-white/20 rounded-2xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 backdrop-blur-sm appearance-none"
                  >
                    <option value="" class="text-gray-800">请选择</option>
                    <option value="民族服饰" class="text-gray-800">民族服饰</option>
                    <option value="传统建筑" class="text-gray-800">传统建筑</option>
                    <option value="民间工艺" class="text-gray-800">民间工艺</option>
                    <option value="地方戏曲" class="text-gray-800">地方戏曲</option>
                    <option value="节庆习俗" class="text-gray-800">节庆习俗</option>
                  </select>
                  <div class="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-cyan-500/10 rounded-2xl opacity-0 group-focus-within:opacity-100 transition-opacity duration-300"></div>
                  <div class="absolute right-4 top-1/2 transform -translate-y-1/2 pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                  </div>
                </div>
              </div>
              
              <!-- 留言输入 -->
              <div class="group">
                <label for="message" class="block text-sm font-medium text-gray-300 mb-3 transition-all duration-300 group-focus-within:text-blue-400">
                  留言
                </label>
                <div class="relative">
                  <textarea 
                    id="message" 
                    v-model="form.message"
                    rows="5"
                    class="w-full px-6 py-4 bg-white/5 border border-white/20 rounded-2xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 backdrop-blur-sm resize-none"
                    placeholder="请输入您的留言内容"
                    required
                  ></textarea>
                  <div class="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-cyan-500/10 rounded-2xl opacity-0 group-focus-within:opacity-100 transition-opacity duration-300"></div>
                </div>
              </div>
              
              <!-- 提交按钮 -->
              <button 
                type="submit" 
                class="group relative w-full py-4 px-6 bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-semibold rounded-2xl transition-all duration-300 transform hover:scale-105 hover:shadow-2xl overflow-hidden"
              >
                <span class="relative z-10">发送留言</span>
                <div class="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent transform -skew-x-12 translate-x-[-150%] group-hover:translate-x-[150%] transition-transform duration-1000"></div>
                <div class="absolute inset-0 bg-gradient-to-r from-blue-600 to-cyan-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </button>
            </form>
          </div>
          
          <!-- 现代化联系信息 -->
          <div class="space-y-8">
            <!-- 联系信息标题 -->
            <div class="flex items-center gap-3 mb-8">
              <div class="w-3 h-3 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full"></div>
              <h4 class="text-2xl font-bold text-white">联系信息</h4>
            </div>
            
            <!-- 联系信息卡片 -->
            <div class="space-y-6">
              <!-- 地址信息 -->
              <div class="group bg-white/5 backdrop-blur-md rounded-2xl border border-white/10 p-6 hover:border-blue-500/50 transition-all duration-300 transform hover:-translate-y-1">
                <div class="flex items-center space-x-4">
                  <div class="w-14 h-14 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-2xl flex items-center justify-center border border-white/10 group-hover:border-blue-500/50 transition-all">
                    <svg class="w-7 h-7 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                    </svg>
                  </div>
                  <div>
                    <p class="font-semibold text-white text-lg">地址</p>
                    <p class="text-gray-300">北京市朝阳区文化路123号</p>
                  </div>
                </div>
              </div>
              
              <!-- 电话信息 -->
              <div class="group bg-white/5 backdrop-blur-md rounded-2xl border border-white/10 p-6 hover:border-green-500/50 transition-all duration-300 transform hover:-translate-y-1">
                <div class="flex items-center space-x-4">
                  <div class="w-14 h-14 bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-2xl flex items-center justify-center border border-white/10 group-hover:border-green-500/50 transition-all">
                    <svg class="w-7 h-7 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                    </svg>
                  </div>
                  <div>
                    <p class="font-semibold text-white text-lg">电话</p>
                    <p class="text-gray-300">400-123-4567</p>
                  </div>
                </div>
              </div>
              
              <!-- 邮箱信息 -->
              <div class="group bg-white/5 backdrop-blur-md rounded-2xl border border-white/10 p-6 hover:border-purple-500/50 transition-all duration-300 transform hover:-translate-y-1">
                <div class="flex items-center space-x-4">
                  <div class="w-14 h-14 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-2xl flex items-center justify-center border border-white/10 group-hover:border-purple-500/50 transition-all">
                    <svg class="w-7 h-7 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                    </svg>
                  </div>
                  <div>
                    <p class="font-semibold text-white text-lg">邮箱</p>
                    <p class="text-gray-300">contact@minsu.com</p>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 社交媒体 -->
            <div class="bg-white/5 backdrop-blur-md rounded-2xl border border-white/10 p-6">
              <h5 class="text-xl font-bold text-white mb-6">关注我们</h5>
              <div class="flex space-x-4">
                <a href="#" class="group w-14 h-14 bg-white/5 rounded-2xl flex items-center justify-center border border-white/10 hover:border-blue-500/50 hover:bg-blue-500/20 transition-all duration-300 transform hover:scale-110">
                  <svg class="w-7 h-7 text-white group-hover:text-blue-400 transition-colors" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
                  </svg>
                </a>
                <a href="#" class="group w-14 h-14 bg-white/5 rounded-2xl flex items-center justify-center border border-white/10 hover:border-cyan-500/50 hover:bg-cyan-500/20 transition-all duration-300 transform hover:scale-110">
                  <svg class="w-7 h-7 text-white group-hover:text-cyan-400 transition-colors" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M22.46 6c-.77.35-1.6.58-2.46.69.88-.53 1.56-1.37 1.88-2.38-.83.5-1.75.85-2.72 1.05C18.37 4.5 17.26 4 16 4c-2.35 0-4.27 1.92-4.27 4.29 0 .34.04.67.11.98C8.28 9.09 5.11 7.38 3 4.79c-.37.63-.58 1.37-.58 2.15 0 1.49.75 2.81 1.91 3.56-.71 0-1.37-.2-1.95-.5v.03c0 2.08 1.48 3.82 3.44 4.21a4.22 4.22 0 0 1-1.93.07 4.28 4.28 0 0 0 4 2.98 8.521 8.521 0 0 1-5.33 1.84c-.34 0-.68-.02-1.02-.06C3.44 20.29 5.7 21 8.12 21 16 21 20.33 14.46 20.33 8.79c0-.19 0-.37-.01-.56.84-.6 1.56-1.36 2.14-2.23z"/>
                  </svg>
                </a>
                <a href="#" class="group w-14 h-14 bg-white/5 rounded-2xl flex items-center justify-center border border-white/10 hover:border-pink-500/50 hover:bg-pink-500/20 transition-all duration-300 transform hover:scale-110">
                  <svg class="w-7 h-7 text-white group-hover:text-pink-400 transition-colors" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.174-.105-.949-.199-2.403.042-3.441.219-.937 1.406-5.965 1.406-5.965s-.359-.719-.359-1.782c0-1.668.967-2.914 2.171-2.914 1.023 0 1.518.769 1.518 1.69 0 1.029-.653 2.567-.992 3.992-.285 1.193.602 2.165 1.775 2.165 2.128 0 3.768-2.245 3.768-5.487 0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 1.033.394 2.143.889 2.741.094.113.108.212.08.326-.09.375-.293 1.199-.334 1.363-.053.225-.172.271-.402.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.357-.629-2.748-1.378 0 0-.599 2.282-.744 2.84-.282 1.084-1.064 2.456-1.549 3.235C9.584 23.815 10.77 24.001 12.017 24.001c6.624 0 11.99-5.367 11.99-11.988C24.007 5.367 18.641.001 12.017.001z"/>
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 表单数据
const form = ref({
  name: '',
  email: '',
  culture: '',
  message: ''
})

// 表单提交处理
const submitForm = () => {
  alert('感谢您的留言！我们会尽快回复您。')
  form.value = {
    name: '',
    email: '',
    culture: '',
    message: ''
  }
}
</script>

<style scoped>
/* 全局样式 */
body {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

/* 基础动画 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-30px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes slideInRight {
  from { opacity: 0; transform: translateX(30px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.animate-fade-in {
  animation: fadeIn 0.8s ease-out forwards;
}
.animate-slide-left {
  animation: slideInLeft 0.8s ease-out forwards;
}
.animate-slide-right {
  animation: slideInRight 0.8s ease-out forwards;
}
.animate-float {
  animation: float 3s ease-in-out infinite;
}

/* 水墨效果 */
.water-ink {
  position: relative;
  overflow: hidden;
}
.water-ink::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><filter id="waterInk"><feTurbulence type="fractalNoise" baseFrequency="0.01" numOctaves="3" seed="1"/><feDisplacementMap in="SourceGraphic" scale="5"/></filter></defs><rect width="100" height="100" filter="url(%23waterInk)" fill="none" stroke="%238B7355" stroke-width="0.5"/></svg>') repeat;
  opacity: 0.1;
  pointer-events: none;
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: #F5F2EE;
}
::-webkit-scrollbar-thumb {
  background: #8B7355;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #6B5A45;
}

/* 响应式字体大小 */
@media (max-width: 640px) {
  .text-responsive {
    font-size: clamp(1rem, 4vw, 1.25rem);
  }
  .text-responsive-lg {
    font-size: clamp(1.5rem, 6vw, 2.5rem);
  }
}
@media (min-width: 641px) and (max-width: 1024px) {
  .text-responsive {
    font-size: clamp(1.125rem, 3vw, 1.5rem);
  }
  .text-responsive-lg {
    font-size: clamp(2rem, 5vw, 3rem);
  }
}
@media (min-width: 1025px) {
  .text-responsive {
    font-size: clamp(1.25rem, 2vw, 1.75rem);
  }
  .text-responsive-lg {
    font-size: clamp(2.5rem, 4vw, 4rem);
  }
}
</style>