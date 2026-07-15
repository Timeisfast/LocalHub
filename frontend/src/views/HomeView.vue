<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans pb-24">
    <!-- 홈 화면 비주얼 이미지 배너 -->
    <section class="relative overflow-hidden text-white py-16 px-6 shadow-xl min-h-[380px] flex items-center justify-center">
      
      <!-- 1. 배경 이미지 배치 (object-cover로 꽉 채우고 중심 맞추기) -->
      <img 
        src="@/assets/seoul-bg.jpg" 
        alt="서울 전경" 
        class="absolute inset-0 w-full h-full object-cover object-center"
      />
      
      <!-- 2. 어두운 오버레이 필터 레이어 (글씨 가독성을 위해 어둡게 처리하고 은은한 푸른빛 얹기) -->
      <div class="absolute inset-0 bg-gradient-to-b from-slate-950/70 via-slate-900/60 to-slate-950/85"></div>
      
      <!-- 3. 콘텐츠 레이아웃 (텍스트와 날씨 카드를 나란히 배치) -->
      <div class="relative z-10 max-w-5xl w-full mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 items-center text-left">
      
        <!-- 좌측: 메인 타이틀 및 소개글 (2/3 분할) -->
        <div class="md:col-span-2 space-y-4">
          <span class="inline-flex items-center gap-1.5 bg-blue-500/30 text-blue-200 text-xs font-semibold px-3 py-1 rounded-full border border-blue-400/20 backdrop-blur-sm">
            <span class="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse"></span>
            LocalHub 서울 커뮤니티
          </span>
          <h1 class="text-3xl font-black sm:text-5xl tracking-tight leading-tight text-white drop-shadow-md">
            서울 권역 정보 공유 <br class="hidden sm:inline">
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-300 to-sky-200">커뮤니티</span>
          </h1>
          <p class="text-xs sm:text-sm text-slate-200 max-w-lg leading-relaxed drop-shadow">
            우리 지역 주민과 관광객이 직접 나누는 생생한 로컬 정보! <br>
            실시간 관광지 정보부터 맛집, 다채로운 축제 이야기까지 한눈에 확인하세요.
          </p>
        </div>

        <!-- 우측: 실시간 날씨 정보 카드 (1/3 분할 - 프론트 단독 연동) -->
        <div class="md:col-span-1 bg-white/10 backdrop-blur-md rounded-2xl p-5 border border-white/10 shadow-xl flex flex-col justify-between h-48">
          <div>
            <div class="flex justify-between items-center mb-1">
              <span class="text-xs font-bold text-blue-300 tracking-wider">REALTIME WEATHER</span>
              <span class="text-[10px] bg-blue-500/30 text-blue-200 px-2 py-0.5 rounded-md font-bold">서울 📍</span>
            </div>
            <p class="text-[11px] text-slate-300">실시간 기상 정보</p>
          </div>

          <!-- 로딩 상태 UI -->
          <div v-if="isLoading" class="flex flex-col items-center justify-center flex-1 py-2">
            <span class="w-6 h-6 border-2 border-blue-400 border-t-transparent rounded-full animate-spin"></span>
            <span class="text-[11px] text-slate-400 mt-2">날씨 정보 로딩 중...</span>
          </div>

          <!-- 날씨 로드 완료 시 노출되는 메인 데이터 UI -->
          <div v-else-if="weatherInfo" class="flex items-center justify-between py-2">
            <div class="flex items-center gap-2">
              <!-- OpenWeatherMap 공식 날씨 아이콘 매핑 -->
              <img 
                :src="`https://openweathermap.org/img/wn/${weatherInfo.icon}@2x.png`" 
                alt="날씨 아이콘"
                class="w-16 h-16 object-contain drop-shadow"
              />
              <div>
                <span class="text-3xl font-black tracking-tighter">{{ weatherInfo.temp }}°C</span>
                <p class="text-xs font-bold text-slate-200 mt-0.5">{{ weatherInfo.description }}</p>
              </div>
            </div>
            <div class="text-right text-[11px] text-slate-300 space-y-0.5">
              <p>💧 습도: {{ weatherInfo.humidity }}%</p>
              <p>💨 풍속: {{ weatherInfo.wind }}m/s</p>
            </div>
          </div>

          <!-- 에러 혹은 초기 Mock 데이터 폴백 UI -->
          <div v-else class="flex flex-col items-center justify-center flex-1 text-center">
            <span class="text-2xl">☀️</span>
            <span class="text-xs text-slate-300 font-semibold mt-1">24°C | 맑음</span>
            <p class="text-[10px] text-slate-400">API 키를 세팅해 주세요.</p>
          </div>

          <!-- 하단: 날씨 맞춤형 여행 가이드 가이드라인 안내 (의뢰서 스펙 반영) -->
          <div class="border-t border-white/10 pt-2.5 mt-1 text-[11px] text-blue-200 font-medium flex items-center gap-1 truncate">
            <span>{{ weatherRecommendation }}</span>
          </div>
        </div>
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
            to="/tours" 
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
import { ref, onMounted, computed } from 'vue'

const weatherInfo = ref(null)
const isLoading = ref(true)

// 날씨 상태에 따른 스마트 여행 적합 여부 메시지 자동 생성 (의뢰서 스펙 구현)
const weatherRecommendation = computed(() => {
  if (isLoading.value) return '⏳ 기상 상태 분석 중...'
  if (!weatherInfo.value) return '🗺️ 오늘 서울은 여행하기 좋은 날씨입니다!'
  
  const temp = weatherInfo.value.temp
  const desc = weatherInfo.value.description

  if (desc.includes('비') || desc.includes('소나기')) {
    return '☔ 실내 미술관이나 고궁 카페 투어를 추천해요!'
  }
  if (desc.includes('흐림') || desc.includes('구름')){
    return '☁️ 햇빛이 약해요! 낙산공원 성곽길 산책은 어떨까요?'
  }
  if (temp >= 30) {
    return '🥵 폭염 주의! 야간 경복궁 투어를 권장합니다.'
  }
  if (temp <= 5) {
    return '🥶 한파 주의! 실내 복합 문화공간이 좋아요.'
  }
  return '🗺️ 쾌적한 날씨입니다! 야외 축제를 즐겨보세요!'
})

// 실시간 OpenWeatherMap API 호출 함수
const fetchWeather = async () => {
  // .env 파일에 등록한 API KEY 로드
  const API_KEY = import.meta.env.VITE_WEATHER_API_KEY
  const CITY = 'Seoul'
  
  // 만약 API Key가 주입되지 않은 초기 마크업 단계라면 가상 데이터로 우회 처리하여 에러 방지
  if (!API_KEY || API_KEY.startsWith('네가_')) {
    setTimeout(() => {
      weatherInfo.value = {
        temp: 24,
        description: '맑음',
        icon: '01d',
        humidity: 55,
        wind: 2.1
      }
      isLoading.value = false
    }, 600)
    return
  }

  try {
    const response = await fetch(
      `https://api.openweathermap.org/data/2.5/weather?q=${CITY}&appid=${API_KEY}&units=metric&lang=kr`
    )
    if (!response.ok) throw new Error('날씨 API 통신 오류')
    
    const data = await response.json()
    
    // 💡 번역 정제 로직 추가
    let cleanDescription = data.weather[0].description
    if (cleanDescription === '온흐림') {
      cleanDescription = '흐림'
    } else if (cleanDescription === '튼구름') {
      cleanDescription = '구름 많음'
    } else if (cleanDescription === '실비') {
      cleanDescription = '가벼운 비'
    }

    weatherInfo.value = {
      temp: Math.round(data.main.temp),
      description: cleanDescription, // 정제된 한글 단어로 바인딩!
      icon: data.weather[0].icon,
      humidity: data.main.humidity,
      wind: data.wind.speed
    }
  } catch (error) {
    console.error('날씨 데이터 로드 에러:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchWeather()
})

// API 연동 전 마크업 검증을 위한 가상 데이터 (Mock Data)
const mockPosts = ref([
  { id: 7, title: '서울 야간 궁궐 투어 코스 추천드립니다!', date: '07/14' },
  { id: 6, title: '이번 주말 한강 달빛야시장 푸드트럭 라인업 공유', date: '07/14' },
  { id: 5, title: '남산타워 케이블카 대기 시간 얼마나 걸리나요?', date: '07/13' },
  { id: 4, title: '인사동 근처 전통 찻집 가성비 좋은 곳 찾았습니다.', date: '07/12' },
  { id: 3, title: '익명 커뮤니티라 편하네요. 비밀번호 잘 기억하세요!', date: '07/11' }
])
</script>