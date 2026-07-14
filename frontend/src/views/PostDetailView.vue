<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans py-10 px-4">
    <div class="max-w-3xl mx-auto">
      
      <!-- 1. 브레드크럼 (Navigation Depth) -->
      <nav class="text-xs text-gray-400 mb-4 font-medium">
        <router-link to="/" class="hover:text-blue-600">홈</router-link> 
        <span class="mx-1">&gt;</span> 
        <router-link to="/posts" class="hover:text-blue-600">게시판</router-link> 
        <span class="mx-1">&gt;</span> 
        <span class="text-gray-600 font-semibold">상세보기</span>
      </nav>

      <!-- 2. 게시글 상세 카드 -->
      <div v-if="currentPost" class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <!-- 게시글 헤더 -->
        <div class="p-6 border-b border-gray-100 bg-gray-50/50">
          <h1 class="text-2xl font-bold text-gray-900 mb-3">
            {{ currentPost.title }}
          </h1>
          <div class="flex items-center justify-between text-xs text-gray-400">
            <div class="flex items-center gap-2">
              <span class="bg-blue-100 text-blue-700 px-2 py-0.5 rounded font-bold">익명</span>
              <span>작성일: {{ currentPost.date }}</span>
            </div>
            <div>
              <span>조회수: 124</span>
            </div>
          </div>
        </div>

        <!-- 게시글 본문 -->
        <div class="p-6 min-h-[250px] text-gray-800 leading-relaxed whitespace-pre-wrap">
          {{ currentPost.content }}
        </div>

        <!-- 하단 액션 버튼 영역 -->
        <div class="p-6 border-t border-gray-100 bg-gray-50/30 flex justify-between items-center">
          <router-link 
            to="/posts" 
            class="text-sm font-semibold text-gray-600 hover:text-gray-900 border border-gray-300 px-4 py-2 rounded-lg hover:bg-gray-50 transition-colors"
          >
            &larr; 목록으로
          </router-link>

          <div class="flex gap-2">
            <button 
              @click="openPasswordModal('edit')"
              class="text-sm font-semibold text-blue-600 hover:text-white border border-blue-600 hover:bg-blue-600 px-4 py-2 rounded-lg transition-all"
            >
              수정
            </button>
            <button 
              @click="openPasswordModal('delete')"
              class="text-sm font-semibold text-red-600 hover:text-white border border-red-600 hover:bg-red-600 px-4 py-2 rounded-lg transition-all"
            >
              삭제
            </button>
          </div>
        </div>
      </div>

      <!-- 게시글을 찾을 수 없을 때의 예외 처리 -->
      <div v-else class="bg-white p-16 rounded-xl shadow-sm border border-gray-200 text-center">
        <div class="text-4xl mb-3">📭</div>
        <p class="text-gray-500 font-semibold mb-6">존재하지 않거나 삭제된 게시글입니다.</p>
        
        <router-link 
          to="/posts" 
          class="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold px-6 py-3 rounded-lg shadow-sm hover:scale-[1.02] active:scale-[0.98] transition-all"
        >
          &larr; 게시판 목록으로 돌아가기
        </router-link>
      </div>
    </div>

    <!-- 3. [모달] 수정/삭제 전용 비밀번호 확인 팝업 (의뢰서 스펙 반영) -->
    <div 
      v-if="isModalOpen" 
      class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
    >
      <div class="bg-white rounded-xl shadow-2xl border border-gray-200 max-w-md w-full overflow-hidden animate-fade-in">
        <div class="p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-2">비밀번호 확인</h3>
          <p class="text-xs text-gray-500 mb-4 whitespace-nowrap break-keep">
            이 게시글을 <span class="font-bold text-blue-600">{{ modalMode === 'edit' ? '수정' : '삭제' }}</span>하시려면 작성 시 등록한 비밀번호를 입력해 주세요.
          </p>
          
          <input 
            v-model="passwordInput"
            @keyup.enter="handlePasswordSubmit"
            type="password" 
            placeholder="수정용 비밀번호 입력" 
            class="w-full bg-gray-50 text-sm rounded-lg border border-gray-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all mb-4"
          />

          <!-- 에러 메시지 -->
          <p v-if="isPasswordWrong" class="text-xs text-red-500 font-semibold mb-3 flex items-center gap-1">
            ⚠️ 비밀번호가 일치하지 않습니다. 다시 시도해 주세요.
          </p>

          <div class="flex gap-2">
            <button 
              @click="closePasswordModal"
              class="flex-1 text-center bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-semibold py-2.5 rounded-lg transition-colors"
            >
              취소
            </button>
            <button 
              @click="handlePasswordSubmit"
              class="flex-1 text-center bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold py-2.5 rounded-lg transition-colors"
            >
              확인
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// 현재 활성화된 글 상태
const currentPost = ref(null)

// 모달 상태 관리
const isModalOpen = ref(false)
const modalMode = ref('edit') // 'edit' 또는 'delete'
const passwordInput = ref('')
const isPasswordWrong = ref(false)

// 가상 데이터 목록 (실제 연동 시에는 API를 호출해서 조회할 예정)
const mockPosts = [
  { id: 7, title: '서울 야간 궁궐 투어 코스 추천드립니다!', content: '경복궁 야간 개장 다녀왔는데 너무 예쁘네요. 한옥의 야경과 은은한 조명이 어우러져서 데이트 코스로 최적입니다. 한복 입고 가시면 입장료도 무료이니 참고하세요!', date: '07/14', password: '1234' },
  { id: 6, title: '축제 일정 공유 고맙습니다.', content: '덕분에 주말 알차게 보냈습니다! 다음 주에 열리는 야시장 축제 정보도 업데이트 부탁드려요.', date: '07/14', password: '1111' },
  { id: 5, title: '주변에 공영 주차장 자리 많나요?', content: '오후 시간대에 차 끌고 가려는데, 주차가 늘 걱정이네요. 주차 공간 넉넉한 구역 아시는 분 제보 부탁드립니다.', date: '07/13', password: '2222' }
]

// URL 파라미터(id)를 기준으로 가상 데이터에서 매칭되는 게시글 찾기
onMounted(() => {
  const postId = parseInt(route.params.id)
  const foundPost = mockPosts.find(post => post.id === postId)
  if (foundPost) {
    currentPost.value = foundPost
  }
})

// 모달 제어 함수
const openPasswordModal = (mode) => {
  modalMode.value = mode
  passwordInput.value = ''
  isPasswordWrong.value = false
  isModalOpen.value = true
}

const closePasswordModal = () => {
  isModalOpen.value = false
}

// 비밀번호 검증 처리 (평문 비교 - 교육적 목적 설계 스펙 반영)[cite: 2]
const handlePasswordSubmit = () => {
  if (passwordInput.value === currentPost.value.password) {
    isPasswordWrong.value = false
    isModalOpen.value = false
    
    if (modalMode.value === 'edit') {
      // 수정 화면으로 이동 (동일한 폼 재사용하므로 path 뒤에 /edit을 붙여 전달)[cite: 2]
      router.push(`/posts/${currentPost.value.id}/edit`)
    } else {
      // 삭제 처리 시뮬레이션
      alert('게시글이 성공적으로 삭제되었습니다.')
      router.push('/posts')
    }
  } else {
    // 비밀번호 불일치 시 에러 노출
    isPasswordWrong.value = true
  }
}
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
.animate-fade-in {
  animation: fadeIn 0.2s ease-out;
}
</style>