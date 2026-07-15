<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans py-10 px-4">
    <div class="max-w-5xl mx-auto">
      
      <nav class="text-xs text-gray-400 mb-4 font-medium">
        <span>홈</span> <span class="mx-1">&gt;</span> <span class="text-gray-600 font-semibold">게시판</span>
      </nav>

      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-6">
        <h1 class="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          <span>📢</span> 지역 정보 공유 게시판
        </h1>

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

          <router-link 
            to="/posts/write"
            class="w-full sm:w-auto text-center bg-blue-600 text-white px-6 py-2.5 rounded-lg text-sm font-bold hover:bg-blue-700 hover:scale-[1.02] active:scale-[0.98] transition-all shadow-sm"
          >
            + 글쓰기
          </router-link>
        </div>
      </div>

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
              <tr v-if="filteredPosts.length === 0">
                <td colspan="3" class="py-12 text-center text-gray-400 font-medium">
                  검색 결과 또는 등록된 게시글이 없습니다.
                </td>
              </tr>
              
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { postApi } from '@/api/services'

const router = useRouter()
const searchQuery = ref('')
const filteredPosts = ref([])

const formatDate = (isoString) => {
  const date = new Date(isoString)
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${month}/${day}`
}

const fetchPostData = async () => {
  try{
    if (searchQuery.value.trim()) {
      filteredPosts.value = await postApi.searchPosts(searchQuery.value.trim())
    } else {
      filteredPosts.value = await postApi.getPostsPage(1, 10)
    }
  } catch (error) {
    console.error('게시글 로드 중 에러 발생:', error)
  }
}

const handleSearch = () => {
  fetchPostData()
}

onMounted(() => {
  fetchPostData()
})

const goToDetail = (id) => {
  router.push(`/posts/${id}`)
}
</script>