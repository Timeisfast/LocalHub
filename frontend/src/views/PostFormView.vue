<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans py-10 px-4">
    <div class="max-w-3xl mx-auto">
      
      <nav class="text-xs text-gray-400 mb-4 font-medium">
        <router-link to="/" class="hover:text-blue-600">홈</router-link> 
        <span class="mx-1">&gt;</span> 
        <router-link to="/posts" class="hover:text-blue-600">게시판</router-link> 
        <span class="mx-1">&gt;</span> 
        <span class="text-gray-600 font-semibold">{{ isEditMode ? '글수정' : '글쓰기' }}</span>
      </nav>

      <div class="bg-white rounded-2xl shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] border border-gray-200/80 overflow-hidden">
        <div class="p-6 border-b border-gray-100 bg-gray-50/50">
          <h1 class="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <span>{{ isEditMode ? '📝' : '✍️' }}</span> 
            {{ isEditMode ? '게시글 수정' : '새 게시글 작성' }}
          </h1>
          <p class="text-xs text-gray-400 mt-1">
            {{ isEditMode ? '기존 내용을 수정하고 저장해 주세요.' : '지역 주민들과 나눌 유익한 이야기를 들려주세요.' }}
          </p>
        </div>

        <form @submit.prevent="handleSubmit" class="p-6 space-y-5">
          
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
import { postApi } from '@/api/services'

const route = useRoute()
const router = useRouter()

const isEditMode = computed(() => !!route.params.id)

const formData = ref({
  title: '',
  content: '',
  author: '익명',
  password: ''
})


onMounted(async () => {
  if (isEditMode.value) {
    const postId = parseInt(route.params.id)
    try {
      const foundPost = await postApi.getPostDetail(postId)
      const savedPass = sessionStorage.getItem(`post_auth_pass_${postId}`) || ''

      formData.value = {
        title: foundPost.title,
        content: foundPost.content,
        author: foundPost.author,
        password: savedPass
      }
    } catch (error) {
      console.error('게시글 상세 정보 호출 실패:', error)
      alert('데이터를 가져올 수 없습니다. 목록으로 돌아갑니다.')
      router.push('/posts')
    }
  }
})

const handleSubmit = async () => {
  try {
    if (isEditMode.value) {
      await postApi.updatePost(route.params.id, formData.value)
      alert('게시글이 성공적으로 수정되었습니다!')
      sessionStorage.removeItem(`post_auth_pass_${route.params.id}`)
      router.push(`/posts/${route.params.id}`)
    } else {
      await postApi.createPost(formData.value)
      alert('새 게시글이 등록되었습니다!')
      router.push('/posts')
    }
  } catch (error) {
    console.error('게시글 제출 중 에러 발생:', error)
    alert('올바른 비밀번호가 아니거나 에러가 발생했습니다.')
  }
}

const handleCancel = () => {
  if (isEditMode.value) {
    router.push(`/posts/${route.params.id}`)
  } else {
    router.push('/posts')
  }
}
</script>