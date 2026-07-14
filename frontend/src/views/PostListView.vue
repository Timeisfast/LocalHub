<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans py-10 px-4">
    <div class="max-w-5xl mx-auto">
      
      <!-- 1. 브레드크럼 (Navigation Depth) -->
      <nav class="text-xs text-gray-400 mb-4 font-medium">
        <span>홈</span> <span class="mx-1">&gt;</span> <span class="text-gray-600 font-semibold">게시판</span>
      </nav>

      <!-- 2. 게시판 타이틀 및 검색/작성 영역 -->
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-6">
        <h1 class="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          <span>📢</span> 지역 정보 공유 게시판
        </h1>

        <!-- 검색창 및 글쓰기 버튼 레이아웃 (의뢰서 구성 반영) -->
        <div class="flex flex-col sm:flex-row gap-3 items-center justify-between">
          <div class="w-full sm:flex-1 flex gap-2">
            <input 
              v-model="searchQuery"
              @keyup.enter="handleSearch"
              type="text" 
              placeholder="게시글 검색어를 입력하세요" 
              class="flex-1 bg-gray-50 text-sm rounded-lg border border-gray-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all"
            />
            <button 
              @click="handleSearch"
              class="bg-gray-800 text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-gray-900 transition-colors"
            >
              검색
            </button>
          </div>

          <!-- 라우터를 통해 글쓰기 폼으로 이동 -->
          <router-link 
            to="/posts/write"
            class="w-full sm:w-auto text-center bg-blue-600 text-white px-6 py-2.5 rounded-lg text-sm font-bold hover:bg-blue-700 hover:scale-[1.02] active:scale-[0.98] transition-all shadow-sm"
          >
            + 글쓰기
          </router-link>
        </div>
      </div>

      <!-- 3. 게시글 목록 테이블 섹션 -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b border-gray-200 bg-gray-50 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                <th class="py-3.5 px-6 w-20">번호</th>
                <th class="py-3.5 px-6">제목</th>
                <th class="py-3.5 px-6 text-right w-32">작성일</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 text-sm">
              <!-- 데이터가 없을 때의 예외 처리 -->
              <tr v-if="filteredPosts.length === 0">
                <td colspan="3" class="py-12 text-center text-gray-400 font-medium">
                  검색 결과 또는 등록된 게시글이 없습니다.
                </td>
              </tr>
              
              <!-- 게시글 반복 렌더링 -->
              <tr 
                v-for="post in filteredPosts" 
                :key="post.id" 
                class="hover:bg-blue-50/30 transition-colors cursor-pointer"
                @click="goToDetail(post.id)"
              >
                <td class="py-4 px-6 text-gray-500 font-medium">{{ post.id }}</td>
                <td class="py-4 px-6">
                  <span class="text-gray-900 font-semibold hover:text-blue-600 transition-colors">
                    {{ post.title }}
                  </span>
                </td>
                <td class="py-4 px-6 text-right text-gray-400 font-medium">{{ post.date }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 4. 페이지네이션 (Pagination) -->
        <div class="border-t border-gray-100 py-4 flex items-center justify-center gap-2">
          <button class="p-2 rounded hover:bg-gray-100 text-gray-400 hover:text-gray-700 transition-colors">
            &lt;
          </button>
          <button class="px-3.5 py-1.5 text-xs font-bold rounded bg-blue-600 text-white">
            1
          </button>
          <button class="px-3.5 py-1.5 text-xs font-medium rounded text-gray-600 hover:bg-gray-100 transition-colors">
            2
          </button>
          <button class="px-3.5 py-1.5 text-xs font-medium rounded text-gray-600 hover:bg-gray-100 transition-colors">
            3
          </button>
          <button class="p-2 rounded hover:bg-gray-100 text-gray-400 hover:text-gray-700 transition-colors">
            &gt;
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchQuery = ref('')
const activeSearch = ref('')

// 로컬 테스트 및 마크업 검증을 위한 가상 데이터 (Mock Data)
const mockPosts = ref([
  { id: 7, title: '서울 야간 궁궐 투어 코스 추천드립니다!', date: '07/14' },
  { id: 6, title: '축제 일정 공유 고맙습니다.', date: '07/14' },
  { id: 5, title: '주변에 공영 주차장 자리 많나요?', date: '07/13' },
  { id: 4, title: '맛집 리스트 검증해봤습니다.', date: '07/12' },
  { id: 3, title: '한강 달빛야시장 푸드트럭 관련 질문!', date: '07/12' },
  { id: 2, title: '익명이라 글 쓰기 정말 편하네요.', date: '07/11' },
  { id: 1, title: 'LocalHub 서비스 오픈을 축하합니다!', date: '07/11' }
])

// 검색 필터링 로직 (API 붙이기 전 임시 프론트엔드 동작 확인용)
const filteredPosts = computed(() => {
  if (!activeSearch.value) return mockPosts.value
  return mockPosts.value.filter(post => 
    post.title.toLowerCase().includes(activeSearch.value.toLowerCase())
  )
})

const handleSearch = () => {
  activeSearch.value = searchQuery.value
}

// 상세 페이지로 이동
const goToDetail = (id) => {
  router.push(`/posts/${id}`)
}
</script>