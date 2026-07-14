<template>
  <div class="fixed bottom-6 right-6 z-50 font-sans">
    
    <!-- 1. 접힌 상태: 플로팅 버튼 (의뢰서 스펙 ①) -->
    <button 
      v-if="!isOpen"
      @click="toggleChat"
      class="bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-full shadow-2xl hover:scale-110 active:scale-95 transition-all flex items-center justify-center relative group"
    >
      <!-- 깜찍한 알림 배지 효과 (UI 생동감 추가) -->
      <span class="absolute -top-1 -right-1 flex h-3.5 w-3.5">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
        <span class="relative inline-flex rounded-full h-3.5 w-3.5 bg-red-500 text-[8px] text-white items-center justify-center font-bold">1</span>
      </span>
      
      <!-- 챗봇 아이콘 (말풍선) -->
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" />
      </svg>
    </button>

    <!-- 2. 펼친 상태: 대화창 위젯 (의뢰서 스펙 ②, ③) -->
    <!-- 모바일 전체 화면 대응: sm: 미만일 때 고정 해제 및 전체 화면 배치 클래스 적용 -->
    <div 
      v-else
      class="bg-white border border-gray-200/80 rounded-2xl shadow-2xl overflow-hidden flex flex-col transition-all duration-300 animate-slide-up
             w-screen h-screen fixed inset-0 
             sm:relative sm:w-[360px] sm:h-[480px] sm:inset-auto sm:rounded-2xl"
    >
      <!-- 챗봇 헤더 -->
      <div class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-4 flex items-center justify-between shadow-sm">
        <div class="flex items-center gap-2">
          <div class="w-2.5 h-2.5 bg-green-400 rounded-full animate-pulse"></div>
          <span class="font-bold text-sm tracking-tight">LocalHub AI 가이드</span>
        </div>
        <!-- 닫기 버튼 -->
        <button 
          @click="toggleChat"
          class="text-white/80 hover:text-white p-1 rounded-lg hover:bg-white/10 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- 대화 히스토리 출력 영역 -->
      <div class="flex-1 p-4 overflow-y-auto space-y-3.5 bg-slate-50" ref="chatContainer">
        <div 
          v-for="(msg, idx) in chatHistory" 
          :key="idx"
          :class="['flex flex-col max-w-[80%]', msg.role === 'user' ? 'ml-auto items-end' : 'mr-auto items-start']"
        >
          <!-- 말풍선 -->
          <div 
            :class="[
              'p-3 text-xs rounded-2xl shadow-sm leading-relaxed',
              msg.role === 'user' 
                ? 'bg-blue-600 text-white rounded-tr-none' 
                : 'bg-white text-gray-800 rounded-tl-none border border-gray-100'
            ]"
          >
            {{ msg.content }}
          </div>
          <!-- 시간초 (디테일) -->
          <span class="text-[9px] text-gray-400 mt-1 px-1">
            {{ msg.time }}
          </span>
        </div>
      </div>

      <!-- 대화 입력창 -->
      <form @submit.prevent="sendMessage" class="p-3 bg-white border-t border-gray-100 flex gap-2">
        <input 
          v-model="userInput"
          type="text" 
          placeholder="지역 축제, 맛집을 물어보세요..." 
          class="flex-1 bg-gray-50 text-xs rounded-xl border border-gray-200 px-3.5 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:bg-white transition-all"
        />
        <button 
          type="submit"
          class="bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-4 py-2.5 rounded-xl transition-colors shrink-0"
        >
          전송
        </button>
      </form>
    </div>

  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'

const isOpen = ref(false)
const userInput = ref('')
const chatContainer = ref(null)

// 초깃값 및 가상 대화 기록 세팅 (의뢰서 스펙 반영)
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

// 자동 스크롤 함수 (대화가 길어질 때 최하단으로 밀어줌)
const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

// 모달이 열릴 때 스크롤 위치 보정
watch(isOpen, (newVal) => {
  if (newVal) {
    scrollToBottom()
  }
})

// 가상 전송 및 응답 핸들러 (Day 2에 실제 OpenAI API 엔드포인트 연동 예정)
const sendMessage = () => {
  if (!userInput.value.trim()) return

  const now = new Date()
  const timeString = now.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })

  // 1. 유저 메시지 추가
  chatHistory.value.push({
    role: 'user',
    content: userInput.value,
    time: timeString
  })

  const query = userInput.value.trim()
  userInput.value = ''
  scrollToBottom()

  // 2. 가상 봇 리액션 (QA 테스트용 시나리오 작동)[cite: 2]
  setTimeout(() => {
    let botReply = '죄송해요, 해당 지역 정보는 아직 제가 열심히 공부 중이랍니다! 다른 관광지나 맛집을 질문해 주시겠어요?'

    if (query.includes('축제') || query.includes('행사')) {
      botReply = '🎉 서울 권역의 다가오는 대표 축제로는 이번 주말 여의도에서 개최되는 "한강 달빛 야시장"과 상시 열리는 "경복궁 야간 개장" 투어가 추천 코스입니다![cite: 2]'
    } else if (query.includes('맛집') || query.includes('식당')) {
      botReply = '🍕 서울시 행정 인증을 받은 우수 맛집 리스트 중, 인사동 근처의 가성비 좋은 전통 찻집과 광화문 주변의 로컬 순대국밥집이 활발하게 공유되고 있어요!'
    } else if (query.includes('주차')) {
      botReply = '🚗 한강공원 근처는 주말 오후 시간대에 혼잡하니 가급적 도보 5분 거리의 인근 공영 주차장을 우회 이용하시는 것을 추천해 드려요.'
    }

    chatHistory.value.push({
      role: 'bot',
      content: botReply,
      time: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
    })
    scrollToBottom()
  }, 800)
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
</style>