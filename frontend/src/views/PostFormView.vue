<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans py-10 px-4">
    <div class="max-w-3xl mx-auto">
      
      <!-- 1. 브레드크럼 (Navigation Depth) -->
      <nav class="text-xs text-gray-400 mb-4 font-medium">
        <router-link to="/" class="hover:text-blue-600">홈</router-link> 
        <span class="mx-1">&gt;</span> 
        <router-link to="/posts" class="hover:text-blue-600">게시판</router-link> 
        <span class="mx-1">&gt;</span> 
        <span class="text-gray-600 font-semibold">{{ isEditMode ? '글수정' : '글쓰기' }}</span>
      </nav>

      <!-- 2. 입력 폼 카드 컨테이너 -->
      <div class="bg-white rounded-2xl shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] border border-gray-200/80 overflow-hidden">
        <!-- 폼 헤더 -->
        <div class="p-6 border-b border-gray-100 bg-gray-50/50">
          <h1 class="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <span>{{ isEditMode ? '📝' : '✍️' }}</span> 
            {{ isEditMode ? '게시글 수정' : '새 게시글 작성' }}
          </h1>
          <p class="text-xs text-gray-400 mt-1">
            {{ isEditMode ? '기존 내용을 수정하고 저장해 주세요.' : '지역 주민들과 나눌 유익한 이야기를 들려주세요.' }}
          </p>
        </div>

        <!-- 폼 본문 양식 -->
        <form @submit.prevent="handleSubmit" class="p-6 space-y-5">
          
          <!-- 제목 입력란 -->
          <div>
            <label class="block text-xs font-bold uppercase tracking-wider text-gray-500 mb-1.5">제목</label>
            <input 
              v-model="formData.title"
              type="text" 
              required
              placeholder="제목을 입력해주세요" 
              class="w-full bg-gray-50 text-sm rounded-xl border border-gray-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:bg-white transition-all font-semibold"
            />
          </div>

          <!-- 내용 입력란 -->
          <div>
            <label class="block text-xs font-bold uppercase tracking-wider text-gray-500 mb-1.5">내용</label>
            <textarea 
              v-model="formData.content"
              required
              rows="10"
              placeholder="내용을 상세히 입력해주세요" 
              class="w-full bg-gray-50 text-sm rounded-xl border border-gray-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:bg-white transition-all leading-relaxed"
            ></textarea>
          </div>

          <!-- 수정용 비밀번호 입력란 (의뢰서 필수 스펙) -->
          <div class="bg-blue-50/50 p-4 rounded-xl border border-blue-100/60">
            <label class="block text-xs font-bold uppercase tracking-wider text-blue-700 mb-1">
              수정용 비밀번호
            </label>
            <p class="text-[11px] text-blue-600/80 mb-2 font-medium">
              * 익명 커뮤니티 특성상 본인 확인을 위해 필수입니다. 평문으로 비교되므로 안전한 공용 암호 사용을 권장합니다.
            </p>
            <input 
              v-model="formData.password"
              type="password" 
              required
              :disabled="isEditMode"
              placeholder="4자리 입력" 
              maxlength="4"
              class="w-40 bg-white text-sm rounded-lg border border-gray-200 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 disabled:bg-gray-100 disabled:text-gray-400 font-mono tracking-widest text-center"
            />
          </div>

          <!-- 하단 폼 버튼 액션 세트 -->
          <div class="pt-4 border-t border-gray-100 flex justify-end gap-2">
            <button 
              type="button"
              @click="handleCancel"
              class="text-sm font-semibold text-gray-600 hover:text-gray-900 border border-gray-200 px-5 py-2.5 rounded-xl hover:bg-gray-50 transition-colors"
            >
              취소
            </button>
            <button 
              type="submit"
              class="bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold px-6 py-2.5 rounded-xl shadow-md hover:scale-[1.01] active:scale-[0.99] transition-all"
            >
              {{ isEditMode ? '수정 완료' : '등록하기' }}
            </button>
          </div>

        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// 1. 라우터 파라미터에 id가 있으면 '수정 모드'로 판별
const isEditMode = computed(() => !!route.params.id)

// 2. 폼 바인딩 상태 정의
const formData = ref({
  title: '',
  content: '',
  password: ''
})

// 가상 데이터 목록 (수정 모드 진입 시 기존 데이터를 불러오기 위한 Mock)
const mockPosts = [
  { id: 7, title: '서울 야간 궁궐 투어 코스 추천드립니다!', content: '경복궁 야간 개장 다녀왔는데 너무 예쁘네요. 한옥의 야경과 은은한 조명이 어우러져서 데이트 코스로 최적입니다. 한복 입고 가시면 입장료도 무료이니 참고하세요!', password: '1234' }
]

onMounted(() => {
  // 수정 모드인 경우, id에 맞는 기존 데이터를 폼에 바인딩
  if (isEditMode.value) {
    const postId = parseInt(route.params.id)
    const foundPost = mockPosts.find(post => post.id === postId)
    
    if (foundPost) {
      formData.value = {
        title: foundPost.title,
        content: foundPost.content,
        password: foundPost.password // 비밀번호 평문 바인딩
      }
    } else {
      alert('해당 게시글을 찾을 수 없습니다.')
      router.push('/posts')
    }
  }
})

// 3. 폼 제출(Submit) 액션 핸들러
const handleSubmit = () => {
  if (isEditMode.value) {
    // 수정 API 바인딩 시점 (PUT /api/posts/{id})
    alert('게시글이 성공적으로 수정되었습니다!')
  } else {
    // 작성 API 바인딩 시점 (POST /api/posts)
    alert('새 게시글이 등록되었습니다!')
  }
  router.push('/posts')
}

// 취소 액션 처리
const handleCancel = () => {
  if (isEditMode.value) {
    router.push(`/posts/${route.params.id}`) // 수정 취소 시 상세 페이지로
  } else {
    router.push('/posts') // 작성 취소 시 목록 페이지로
  }
}
</script>