<template>
  <div class="fixed bottom-6 right-6 z-50 font-sans">
    
    <!-- 챗 위젯 열기 버튼 -->
    <button 
      v-if="!isOpen"
      @click="toggleChat"
      class="bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-full shadow-2xl hover:scale-110 active:scale-95 transition-all flex items-center justify-center relative group"
    >
      <span class="absolute -top-1 -right-1 flex h-3.5 w-3.5">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
        <span class="relative inline-flex rounded-full h-3.5 w-3.5 bg-red-500 text-[8px] text-white items-center justify-center font-bold">1</span>
      </span>
      
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" />
      </svg>
    </button>

    <!-- 챗 창 본체 -->
    <div 
      v-else
      class="bg-white border border-gray-200/80 rounded-2xl shadow-2xl overflow-hidden flex flex-col transition-all duration-300 animate-slide-up
             w-screen h-screen fixed inset-0 
             sm:relative sm:w-[380px] sm:h-[520px] sm:inset-auto sm:rounded-2xl"
    >
      <!-- 헤더 -->
      <div class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-4 flex items-center justify-between shadow-sm">
        <div class="flex items-center gap-2">
          <div class="w-2.5 h-2.5 bg-green-400 rounded-full animate-pulse"></div>
          <span class="font-bold text-sm tracking-tight">LocalHub AI 가이드</span>
        </div>
        <button 
          @click="toggleChat"
          class="text-white/80 hover:text-white p-1 rounded-lg hover:bg-white/10 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- 대화 목록 내역 -->
      <div class="flex-1 p-4 overflow-y-auto space-y-4 bg-slate-50" ref="chatContainer">
        <div 
          v-for="(msg, idx) in chatHistory" 
          :key="idx"
          :class="['flex flex-col max-w-[85%]', msg.role === 'user' ? 'ml-auto items-end' : 'mr-auto items-start']"
        >
          <!-- 텍스트 말풍선 -->
          <div 
            :class="[
              'p-3 text-xs rounded-2xl shadow-sm leading-relaxed whitespace-pre-line',
              msg.role === 'user' 
                ? 'bg-blue-600 text-white rounded-tr-none' 
                : 'bg-white text-gray-800 rounded-tl-none border border-gray-100'
            ]"
          >
            {{ msg.content }}
          </div>

          <!-- 💡 [실전 API 연동 꽃] 추천 장소 카드 리스트 출력 -->
          <div v-if="msg.items && msg.items.length > 0" class="w-full mt-2.5 space-y-2">
            <div 
              v-for="item in msg.items" 
              :key="item.id"
              class="bg-white rounded-xl border border-gray-200/80 p-3 shadow-sm flex flex-col gap-2 transition-all hover:border-blue-400"
            >
              <img 
                v-if="item.image_url" 
                :src="item.image_url" 
                :alt="item.title"
                class="w-full h-24 object-cover rounded-lg bg-gray-100"
              />
              <div>
                <div class="flex items-center gap-1.5 mb-1">
                  <span class="text-[10px] font-extrabold bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded">
                    {{ item.category === 'tourist' ? '관광지' : '쇼핑' }}
                  </span>
                  <h4 class="font-bold text-xs text-gray-900 truncate">{{ item.title }}</h4>
                </div>
                <p class="text-[10px] text-gray-500 line-clamp-2 leading-relaxed">{{ item.description }}</p>
                <p v-if="item.address" class="text-[9px] text-gray-400 mt-1">📍 {{ item.address }}</p>
              </div>
            </div>
          </div>

          <!-- 전송 시간 표시 -->
          <span class="text-[9px] text-gray-400 mt-1 px-1">
            {{ msg.time }}
          </span>
        </div>

        <!-- 💡 챗봇 답변 대기 애니메이션 (Typing Indicator) -->
        <div v-if="isThinking" class="flex flex-col max-w-[80%] mr-auto items-start">
          <div class="bg-white border border-gray-100 p-3 rounded-2xl rounded-tl-none shadow-sm flex gap-1.5 items-center">
            <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"></span>
            <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:0.2s]"></span>
            <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:0.4s]"></span>
          </div>
        </div>
      </div>

      <!-- 입력 폼 -->
      <form @submit.prevent="sendMessage" class="p-3 bg-white border-t border-gray-100 flex gap-2">
        <input 
          v-model="userInput"
          type="text" 
          placeholder="지역 축제, 맛집을 물어보세요..." 
          class="flex-1 bg-gray-50 text-xs rounded-xl border border-gray-200 px-3.5 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:bg-white transition-all"
        />
        <button 
          type="submit"
          :disabled="isThinking"
          class="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white text-xs font-bold px-4 py-2.5 rounded-xl transition-colors shrink-0"
        >
          전송
        </button>
      </form>
    </div>

  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import { chatApi } from '@/api/services' // 💡 API 모듈 추가

const isOpen = ref(false)
const userInput = ref('')
const chatContainer = ref(null)
const isThinking = ref(false) // 💡 대기 상태 스위치 추가

const chatHistory = ref([
  { 
    role: 'bot', 
    content: '안녕하세요! LocalHub AI 지역 가이드봇입니다. 서울의 다채로운 관광지, 맛집, 축제 일정 등을 추천해 드릴 수 있어요. 무엇이 궁금하신가요?', 
    time: '오후 4:50' 
  }
])

const toggleChat = () => {
  isOpen.value = !isOpen.value
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

watch(isOpen, (newVal) => {
  if (newVal) {
    scrollToBottom()
  }
})

// 💡 [핵심 구현] 진짜 API 호출 연동 및 비동기 처리
const sendMessage = async () => {
  if (!userInput.value.trim() || isThinking.value) return

  const now = new Date()
  const timeString = now.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
  const query = userInput.value.trim()

  // 1. 유저 말풍선 화면에 즉각 추가
  chatHistory.value.push({
    role: 'user',
    content: query,
    time: timeString
  })

  userInput.value = ''
  scrollToBottom()

  // 2. 챗봇 대기 상태 On
  isThinking.value = true

  try {
    // 3. /api/chat 백엔드 통신 실행
    const response = await chatApi.sendMessage(query)

    // 4. API가 전해준 응답 스키마 풀링 가공
    if (response) {
      chatHistory.value.push({
        role: 'bot',
        content: response.answer || '추천 결과가 준비되었습니다.',
        items: response.items || [], // 💡 추천 장소 아이템 바인딩!
        time: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
      })
    }
  } catch (error) {
    console.error('챗봇 통신 에러:', error)
    // 에러 상황을 유저에게 친절히 고지
    chatHistory.value.push({
      role: 'bot',
      content: '🤖 죄송합니다. 일시적인 통신 불안정으로 서울 정보를 불러오지 못했습니다. 잠시 후 다시 입력해 주세요.',
      time: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
    })
  } finally {
    // 5. 챗봇 대기 상태 Off 및 스크롤 다운
    isThinking.value = false
    scrollToBottom()
  }
}
</script>

<style scoped>
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-slide-up {
  animation: slideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;  
  overflow: hidden;
}
</style>