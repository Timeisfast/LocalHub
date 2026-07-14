<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans pb-24">
    <!-- 홈 화면 비주얼 이미지 배너 -->
    <section class="relative overflow-hidden text-white py-24 px-6 shadow-xl h-[340px] sm:h-[400px] flex items-center justify-center">
      
      <!-- 1. 배경 이미지 배치 (object-cover로 꽉 채우고 중심 맞추기) -->
      <img 
        src="@/assets/seoul-bg.jpg" 
        alt="서울 전경" 
        class="absolute inset-0 w-full h-full object-cover object-center"
      />
      
      <!-- 2. 어두운 오버레이 필터 레이어 (글씨 가독성을 위해 어둡게 처리하고 은은한 푸른빛 얹기) -->
      <div class="absolute inset-0 bg-gradient-to-b from-slate-950/70 via-slate-900/60 to-slate-950/85"></div>
      
      <!-- 3. 원형 Blur 데코레이션 (오버레이 위에 살짝 얹어서 트렌디함 더하기) -->
      <div class="absolute -top-10 -left-10 w-40 h-40 bg-blue-500/10 rounded-full blur-3xl"></div>
      
      <!-- 4. 실제 콘텐츠 텍스트 영역 (배경보다 위에 떠 있도록 z-10 설정) -->
      <div class="relative z-10 max-w-4xl mx-auto text-center">
        <span class="inline-flex items-center gap-1.5 bg-blue-500/30 text-blue-200 text-xs font-semibold px-3 py-1 rounded-full border border-blue-400/20 backdrop-blur-sm">
          <span class="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse"></span>
          LocalHub 서울 커뮤니티
        </span>
        <h1 class="text-4xl font-black mt-5 sm:text-5xl tracking-tight leading-tight text-white drop-shadow-md">
          서울 권역 정보 공유 <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-300 to-sky-200">커뮤니티</span>
        </h1>
        <p class="mt-4 text-xs sm:text-sm text-slate-200 max-w-lg mx-auto leading-relaxed drop-shadow">
          서울 주민들과 여행객들이 직접 나누는 생생한 로컬 정보! <br>
          실시간 관광지 정보부터 맛집, 다채로운 축제 이야기까지 한눈에 확인하세요.
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
          <!-- 관광지 카드 (배경 이미지 적용 및 호버 이펙트 고도화) -->
          <router-link 
            to="/posts?category=tour" 
            class="group relative overflow-hidden h-40 rounded-2xl shadow-sm border border-gray-200/80 hover:border-blue-500 hover:shadow-xl hover:-translate-y-1.5 transition-all duration-300 flex flex-col justify-end p-5 text-left"
          >
            <!-- 1. 배경 이미지 (기본 상태에서 미세한 블러와 줌 효과 제공) -->
            <img 
              src="@/assets/tour-bg.jpg" 
              alt="관광지" 
              class="absolute inset-0 w-full h-full object-cover object-center filter brightness-95 group-hover:scale-110 transition-transform duration-500"
            />

            <!-- 2. 그라데이션 어두운 오버레이 (하단 글씨가 또렷하게 보이도록 잡아주는 그라데이션) -->
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-slate-900/40 to-transparent"></div>

            <!-- 3. 카드 콘텐츠 (z-10으로 오버레이 위에 띄우기) -->
            <div class="relative z-10">
              <div class="flex items-center gap-1.5 mb-1">
                <span class="text-xl group-hover:animate-bounce">🏛️</span>
                <span class="font-bold text-white text-lg tracking-tight drop-shadow-md">관광지</span>
              </div>
              <p class="text-[11px] text-gray-200 font-medium drop-shadow-sm">아름다운 서울 명소</p>
            </div>
          </router-link>

          <!-- 식당 카드 (배경 이미지 적용 및 호버 이펙트 고도화) -->
          <router-link 
            to="/restaurants" 
            class="group relative overflow-hidden h-40 rounded-2xl shadow-sm border border-gray-200/80 hover:border-blue-500 hover:shadow-xl hover:-translate-y-1.5 transition-all duration-300 flex flex-col justify-end p-5 text-left"
          >
            <!-- 1. 배경 이미지 (기본 상태에서 미세한 블러와 줌 효과 제공) -->
            <img 
              src="@/assets/restaurant-bg.jpg" 
              alt="식당" 
              class="absolute inset-0 w-full h-full object-cover object-center filter brightness-95 group-hover:scale-110 transition-transform duration-500"
            />

            <!-- 2. 그라데이션 어두운 오버레이 (하단 글씨가 또렷하게 보이도록 잡아주는 그라데이션) -->
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-slate-900/40 to-transparent"></div>

            <!-- 3. 카드 콘텐츠 (z-10으로 오버레이 위에 띄우기) -->
            <div class="relative z-10">
              <div class="flex items-center gap-1.5 mb-1">
                <span class="text-xl group-hover:animate-bounce">🍕</span>
                <span class="font-bold text-white text-lg tracking-tight drop-shadow-md">식당</span>
              </div>
              <p class="text-[11px] text-gray-200 font-medium drop-shadow-sm">서울 식당 모아모아</p>
            </div>
          </router-link>

          <!-- 축제·행사 카드 (배경 이미지 적용 및 호버 이펙트 고도화) -->
          <router-link 
            to="/festivals" 
            class="group relative overflow-hidden h-40 rounded-2xl shadow-sm border border-gray-200/80 hover:border-blue-500 hover:shadow-xl hover:-translate-y-1.5 transition-all duration-300 flex flex-col justify-end p-5 text-left"
          >
            <!-- 1. 배경 이미지 (기본 상태에서 미세한 블러와 줌 효과 제공) -->
            <img 
              src="@/assets/festival-bg.jpg" 
              alt="축제·행사" 
              class="absolute inset-0 w-full h-full object-cover object-center filter brightness-95 group-hover:scale-110 transition-transform duration-500"
            />

            <!-- 2. 그라데이션 어두운 오버레이 (하단 글씨가 또렷하게 보이도록 잡아주는 그라데이션) -->
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-slate-900/40 to-transparent"></div>

            <!-- 3. 카드 콘텐츠 (z-10으로 오버레이 위에 띄우기) -->
            <div class="relative z-10">
              <div class="flex items-center gap-1.5 mb-1">
                <span class="text-xl group-hover:animate-bounce">🎉</span>
                <span class="font-bold text-white text-lg tracking-tight drop-shadow-md">축제·행사</span>
              </div>
              <p class="text-[11px] text-gray-200 font-medium drop-shadow-sm">이번 달 열리는 다채로운 축제 정보</p>
            </div>
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