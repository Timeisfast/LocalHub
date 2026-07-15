<script setup>
import { RouterLink, RouterView } from 'vue-router'
import ChatWidget from './components/chat/ChatWidget.vue' 
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col font-sans">
    
    <header class="bg-white/70 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50 shadow-sm">
      <div class="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
        
        <RouterLink to="/" class="flex items-center gap-2">
          <span class="text-2xl font-black tracking-tight text-blue-600 font-mono">LocalHub</span>
        </RouterLink>

        <div class="flex items-center gap-6">
          <nav class="hidden sm:flex items-center gap-4 text-sm font-medium text-gray-600">
            <RouterLink to="/" class="hover:text-blue-600 transition-colors" active-class="text-blue-600 font-bold">홈</RouterLink>
            <RouterLink to="/posts" class="hover:text-blue-600 transition-colors" active-class="text-blue-600 font-bold">게시판</RouterLink>
          </nav>
        </div>

      </div>
    </header>

    <div class="flex-1">
      <RouterView />
    </div>

    <footer class="bg-white border-t border-gray-200 py-6 mt-auto">
      <div class="max-w-5xl mx-auto px-4 text-center sm:text-left sm:flex sm:justify-between sm:items-center text-xs text-gray-400">
        <p>© 2026 LocalHub. 서울 권역 공공데이터 활용 프로젝트.</p>
        <p class="mt-2 sm:mt-0">SSAFY 16기 FE 개발팀 산출물</p>
      </div>
    </footer>

    <ChatWidget />

  </div>
</template>

<style>
</style>