<script setup>
import { RouterLink, RouterView } from 'vue-router'
// 추후 챗봇 위젯 컴포넌트가 완성되면 여기에 import해서 얹어두면 됨
// import ChatWidget from './components/chat/ChatWidget.vue' 
</script>

<template>
  <!-- 글로벌 최상위 컨테이너 -->
  <div class="min-h-screen bg-gray-50 flex flex-col font-sans">
    
    <!-- 1. 공통 GNB 헤더 영역 (의뢰서 스펙 반영) -->
    <header class="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
      <div class="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
        
        <!-- 로고 영역: 클릭 시 홈으로 이동 -->
        <RouterLink to="/" class="flex items-center gap-2">
          <span class="text-2xl font-black tracking-tight text-blue-600 font-mono">LocalHub</span>
        </RouterLink>

        <!-- 통합 검색 및 메뉴 바 영역 -->
        <div class="flex items-center gap-6">
          <nav class="hidden sm:flex items-center gap-4 text-sm font-medium text-gray-600">
            <RouterLink to="/" class="hover:text-blue-600 transition-colors" active-class="text-blue-600 font-bold">홈</RouterLink>
            <RouterLink to="/posts" class="hover:text-blue-600 transition-colors" active-class="text-blue-600 font-bold">게시판</RouterLink>
          </nav>

          <!-- 의뢰서 예시의 우측 상단 돋보기(Q) 검색바 뼈대 -->
          <div class="relative">
            <input 
              type="text" 
              placeholder="통합 검색..." 
              class="w-40 sm:w-48 bg-gray-100 text-xs rounded-lg pl-8 pr-3 py-2 border border-transparent focus:outline-none focus:bg-white focus:border-blue-500 transition-all"
            />
            <span class="absolute left-2.5 top-2.5 text-gray-400 text-xs">🔍</span>
          </div>
        </div>

      </div>
    </header>

    <!-- 2. 동적 페이지 렌더링 영역 (1단 레이아웃 본문) -->
    <div class="flex-1">
      <RouterView />
    </div>

    <!-- 3. 공통 푸터 영역 -->
    <footer class="bg-white border-t border-gray-200 py-6 mt-auto">
      <div class="max-w-5xl mx-auto px-4 text-center sm:text-left sm:flex sm:justify-between sm:items-center text-xs text-gray-400">
        <p>© 2026 LocalHub. 서울 권역 공공데이터 활용 프로젝트.</p>
        <p class="mt-2 sm:mt-0">SSAFY 16기 FE 개발팀 산출물</p>
      </div>
    </footer>

    <!-- 4. 챗봇 플로팅 위젯 레이어 (여기에 위치하면 페이지가 바뀌어도 챗봇이 유지됨) -->
    <!-- <ChatWidget /> -->
    <div class="fixed bottom-6 right-6 z-50">
      <button class="bg-blue-600 text-white p-3.5 rounded-full shadow-xl hover:bg-blue-700 hover:scale-105 transition-all flex items-center justify-center font-bold text-sm">
        💬 Chat
      </button>
    </div>

  </div>
</template>

<style>
/* 
  Vite 기본 제공 scoped 스타일과 좌우 배치 CSS 미디어 쿼리를 전부 걷어내고 
  Tailwind CSS 유틸리티 클래스가 주도하도록 완전히 비워둠.
*/
</style>