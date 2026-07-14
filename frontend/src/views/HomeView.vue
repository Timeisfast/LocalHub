<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans pb-24">
    <!-- 1. 메인 배너 섹션 (선정 권역 소개) -->
    <section class="relative overflow-hidden bg-gradient-to-br from-slate-900 via-indigo-950 to-blue-900 text-white py-20 px-6 shadow-xl">
      <!-- 배경 디자인 데코레이션용 원형 Blur 이펙트 -->
      <div class="absolute -top-10 -left-10 w-40 h-40 bg-blue-500/20 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-20 -right-10 w-64 h-64 bg-indigo-500/20 rounded-full blur-3xl"></div>
      
      <div class="relative max-w-4xl mx-auto text-center">
        <span class="inline-flex items-center gap-1.5 bg-blue-500/20 text-blue-300 text-xs font-semibold px-3 py-1 rounded-full border border-blue-500/30 backdrop-blur-sm">
          <span class="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse"></span>
          LocalHub 커뮤니티
        </span>
        <h1 class="text-4xl font-black mt-5 sm:text-6xl tracking-tight leading-tight">
          서울 권역 정보 공유 <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-sky-300">커뮤니티</span>
        </h1>
        <p class="mt-5 text-sm sm:text-base text-slate-300 max-w-lg mx-auto leading-relaxed">
          우리 지역 주민과 관광객이 자유롭게 소통하는 공간입니다.<br>
          다양한 관광지, 맛집, 축제 정보를 한눈에 만나보세요!
        </p>
      </div>
    </section>

    <!-- 메인 콘텐츠 영역 (1단 레이아웃으로 공수 최소화) -->
    <main class="max-w-5xl mx-auto px-4 mt-10">
      
      <!-- 2. 카테고리 바로가기 카드 섹션 -->
      <section class="mb-12">
        <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          <span>📂</span> 카테고리 바로가기
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <!-- 관광지 카드 -->
          <router-link to="/posts?category=tour" class="bg-white p-6 rounded-2xl shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] border border-gray-100 hover:border-blue-500 hover:shadow-xl hover:-translate-y-1.5 transition-all duration-300 text-center">
            <div class="text-3xl mb-2 group-hover:scale-110 transition-transform">🏛️</div>
            <div class="font-bold text-gray-800 text-lg">관광지</div>
            <p class="text-xs text-gray-500 mt-1">지역 명소 및 추천 명소</p>
          </router-link>

          <!-- 맛집 카드 -->
          <router-link to="/posts?category=food" class="bg-white p-6 rounded-2xl shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] border border-gray-100 hover:border-blue-500 hover:shadow-xl hover:-translate-y-1.5 transition-all duration-300 text-center">
            <div class="text-3xl mb-2 group-hover:scale-110 transition-transform">🍕</div>
            <div class="font-bold text-gray-800 text-lg">맛집</div>
            <p class="text-xs text-gray-500 mt-1">행정 인증 맛집 및 추천 식당</p>
          </router-link>

          <!-- 축제·행사 카드 -->
          <router-link to="/posts?category=festival" class="bg-white p-6 rounded-2xl shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] border border-gray-100 hover:border-blue-500 hover:shadow-xl hover:-translate-y-1.5 transition-all duration-300 text-center">
            <div class="text-3xl mb-2 group-hover:scale-110 transition-transform">🎉</div>
            <div class="font-bold text-gray-800 text-lg">축제·행사</div>
            <p class="text-xs text-gray-500 mt-1">이번 달 열리는 다채로운 축제 정보</p>
          </router-link>
        </div>
      </section>

      <!-- 3. 최근 게시글 목록 섹션 (가상 Mock Data 바인딩) -->
      <section class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-bold text-gray-800 flex items-center gap-2">
            <span>📝</span> 최근 게시글
          </h2>
          <router-link to="/posts" class="text-sm font-medium text-blue-600 hover:underline">
            전체 보기 &rarr;
          </router-link>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b border-gray-200 bg-gray-50 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                <th class="py-3 px-4">번호</th>
                <th class="py-3 px-4">제목</th>
                <th class="py-3 px-4 text-right">작성일</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 text-sm">
              <tr v-for="post in mockPosts" :key="post.id" class="hover:bg-gray-50 transition-colors">
                <td class="py-3.5 px-4 text-gray-500 font-medium">{{ post.id }}</td>
                <td class="py-3.5 px-4">
                  <router-link :to="`/posts/${post.id}`" class="text-gray-900 font-semibold hover:text-blue-600">
                    {{ post.title }}
                  </router-link>
                </td>
                <td class="py-3.5 px-4 text-right text-gray-400">{{ post.date }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// API 연동 전 마크업 검증을 위한 가상 데이터 (Mock Data)
const mockPosts = ref([
  { id: 7, title: '서울 야간 궁궐 투어 코스 추천드립니다!', date: '07/14' },
  { id: 6, title: '이번 주말 한강 달빛야시장 푸드트럭 라인업 공유', date: '07/14' },
  { id: 5, title: '남산타워 케이블카 대기 시간 얼마나 걸리나요?', date: '07/13' },
  { id: 4, title: '인사동 근처 전통 찻집 가성비 좋은 곳 찾았습니다.', date: '07/12' },
  { id: 3, title: '익명 커뮤니티라 편하네요. 비밀번호 잘 기억하세요!', date: '07/11' }
])
</script>