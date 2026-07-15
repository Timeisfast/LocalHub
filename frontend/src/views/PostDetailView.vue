<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans py-10 px-4">
    <div class="max-w-3xl mx-auto">
      
      <nav class="text-xs text-gray-400 mb-4 font-medium">
        <router-link to="/" class="hover:text-blue-600">홈</router-link> 
        <span class="mx-1">&gt;</span> 
        <router-link to="/posts" class="hover:text-blue-600">게시판</router-link> 
        <span class="mx-1">&gt;</span> 
        <span class="text-gray-600 font-semibold">상세보기</span>
      </nav>

      <div v-if="currentPost" class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="p-6 border-b border-gray-100 bg-gray-50/50">
          <h1 class="text-2xl font-bold text-gray-900 mb-3">
            {{ currentPost.title }}
          </h1>
          <div class="flex items-center justify-between text-xs text-gray-400">
            <div class="flex items-center gap-2">
              <span class="bg-blue-100 text-blue-700 px-2 py-0.5 rounded font-bold">익명</span>
              <span>작성일: {{ formatDate(currentPost.created_at) }}</span>
            </div>
          </div>
        </div>

        <div class="p-6 min-h-[250px] text-gray-800 leading-relaxed whitespace-pre-wrap">
          {{ currentPost.content }}
        </div>

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
import { postApi } from '@/api/services'

const route = useRoute()
const router = useRouter()

const currentPost = ref(null)

const isModalOpen = ref(false)
const modalMode = ref('edit')
const passwordInput = ref('')
const isPasswordWrong = ref(false)

const formatDate = (isoString) => {
  if (!isoString) return ''
  return isoString.split('T')[0]
}

onMounted(async () => {
  const postId = parseInt(route.params.id)
  try {
    currentPost.value = await postApi.getPostDetail(postId)
  } catch (error) {
    console.error('상세 정보 호출 실패:', error)
  }
})

const openPasswordModal = (mode) => {
  modalMode.value = mode
  passwordInput.value = ''
  isPasswordWrong.value = false
  isModalOpen.value = true
}

const closePasswordModal = () => {
  isModalOpen.value = false
}

const handlePasswordSubmit = async () => {
  const postId = currentPost.value.id

  if (modalMode.value === 'edit') {
    sessionStorage.setItem(`post_auth_pass_${postId}`, passwordInput.value)
    router.push(`/posts/${postId}/edit`)
  } else {
    try {
      await postApi.deletePost(postId, passwordInput.value)
      alert('게시글이 성공적으로 삭제되었습니다.')
      router.push('/posts')
    } catch (error) {
      console.error('삭제 처리 실패:', error)
      isPasswordWrong.value = true
    }
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