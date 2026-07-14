<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans py-10 px-4">
    <div class="max-w-5xl mx-auto">
      
      <!-- 1. 브레드크럼 -->
      <nav class="text-xs text-gray-400 mb-4 font-medium">
        <router-link to="/" class="hover:text-blue-600">홈</router-link> 
        <span class="mx-1">&gt;</span> 
        <span class="text-gray-600 font-semibold">식당</span>
      </nav>

      <!-- 2. 상단 헤더 카드 -->
      <div class="bg-white p-6 rounded-2xl border border-gray-200/70 shadow-sm mb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <span>🍕</span> 서울 식당 가이드
          </h1>
          <p class="text-xs text-gray-400 mt-1">
            지역 주민과 여행객들이 인정한 서울 권역 식당 리스트입니다.
          </p>
        </div>
        
        <!-- 카테고리 필터 탭 (UI 디테일) -->
        <div class="flex gap-2 bg-slate-100 p-1 rounded-xl border border-gray-200/50">
          <button 
            v-for="tab in ['전체', '한식', '일식/중식', '양식', '카페']" 
            :key="tab"
            @click="selectedCategory = tab"
            :class="[
              'px-3.5 py-1.5 text-xs font-bold rounded-lg transition-all',
              selectedCategory === tab 
                ? 'bg-white text-blue-600 shadow-sm' 
                : 'text-gray-500 hover:text-gray-800'
            ]"
          >
            {{ tab }}
          </button>
        </div>
      </div>

      <!-- 3. 식당 카드 그리드 영역 -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <div 
          v-for="restaurant in filteredRestaurants" 
          :key="restaurant.id"
          @click="selectRestaurant(restaurant)"
          class="group bg-white rounded-2xl border border-gray-200/80 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 overflow-hidden cursor-pointer"
        >
          <!-- 식당 대표 이미지 -->
          <div class="h-44 overflow-hidden relative">
            <img 
              :src="restaurant.image" 
              :alt="restaurant.name" 
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            />
            <span class="absolute top-3 right-3 bg-slate-900/80 backdrop-blur-sm text-white text-[10px] font-extrabold px-2 py-1 rounded-md">
              {{ restaurant.category }}
            </span>
          </div>

          <!-- 식당 요약 정보 -->
          <div class="p-5">
            <div class="flex items-center justify-between mb-1">
              <h3 class="font-bold text-base text-gray-900 group-hover:text-blue-600 transition-colors">
                {{ restaurant.name }}
              </h3>
              <span class="text-xs text-amber-500 font-bold flex items-center gap-0.5">
                ★ {{ restaurant.rating }}
              </span>
            </div>
            <p class="text-xs text-gray-400 mb-3 truncate">{{ restaurant.description }}</p>
            
            <div class="flex items-center gap-1.5 text-[11px] text-gray-500 font-medium">
              <span>📍</span> <span class="truncate">{{ restaurant.location }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 4. 하단: 선택된 식당 상세 안내 보드 (캘린더 상세보드와 통일된 UX) -->
      <div class="transition-all duration-300">
        <div 
          v-if="selectedRestaurant" 
          class="bg-white p-6 rounded-2xl border-2 border-blue-500/30 shadow-md animate-slide-up"
        >
          <div class="flex justify-between items-start mb-4">
            <div>
              <span class="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded mb-2 inline-block">
                {{ selectedRestaurant.category }}
              </span>
              <h2 class="text-xl font-bold text-gray-900 flex items-center gap-1.5">
                {{ selectedRestaurant.name }}
                <span class="text-sm text-amber-500">★ {{ selectedRestaurant.rating }}</span>
              </h2>
            </div>
            <button 
              @click="selectedRestaurant = null"
              class="text-gray-400 hover:text-gray-600 text-sm font-semibold p-1"
            >
              닫기 ✕
            </button>
          </div>

          <!-- 상세 디테일 정보 -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-700 bg-slate-50 p-4 rounded-xl border border-gray-100">
            <div class="space-y-2">
              <p><span class="font-bold text-gray-500 inline-block w-20">📍 위치:</span> {{ selectedRestaurant.location }}</p>
              <p><span class="font-bold text-gray-500 inline-block w-20">📞 전화번호:</span> {{ selectedRestaurant.phone }}</p>
              <p><span class="font-bold text-gray-500 inline-block w-20">⏰ 영업시간:</span> {{ selectedRestaurant.hours }}</p>
            </div>
            <div>
              <p class="leading-relaxed">
                <span class="font-bold text-gray-500 block mb-1">📝 대표 메뉴 & 특징:</span>
                {{ selectedRestaurant.longDescription }}
              </p>
            </div>
          </div>
        </div>

        <!-- 미선택 상태 가이드 -->
        <div 
          v-else 
          class="bg-white py-10 px-6 rounded-2xl border border-dashed border-gray-300 text-center text-gray-400 text-sm font-medium"
        >
          🔍 위 목록에서 관심 있는 식당을 클릭하시면 상세 영업 정보와 대표 메뉴를 확인하실 수 있습니다.
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const selectedCategory = ref('전체')
const selectedRestaurant = ref(null)

// 푸드 이미지를 매핑한 가상 식당 리스트
const mockRestaurants = ref([
  {
    id: 1,
    name: '명동 진 칼국수',
    category: '한식',
    rating: '4.8',
    location: '서울 중구 명동길 25-7',
    phone: '02-776-5348',
    hours: '10:30 ~ 21:00 (연중무휴)',
    image: 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=500&q=80',
    description: '진한 닭 육수와 쫄깃한 면발의 조화가 일품인 50년 전통 칼국수',
    longDescription: '명동의 상징적인 칼국수 전문점입니다. 닭 뼈를 푹 고아내어 깊고 무거운 국물 맛이 일품이며, 고명으로 올라가는 다진 고기와 만두가 조화를 이룹니다. 매콤하고 알싸한 마늘 겉절이 김치가 식사의 완성도를 높여줍니다.'
  },
  {
    id: 2,
    name: '인사 찻집',
    category: '카페',
    rating: '4.6',
    location: '서울 종로구 인사동길 35-1',
    phone: '02-735-6582',
    hours: '11:00 ~ 22:00',
    image: 'https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=500&q=80',
    description: '전통 한옥의 고즈넉한 무드 속에서 즐기는 쌍화차와 수제 대추차',
    longDescription: '인사동 쌈지길 인근에 위치한 고풍스러운 전통 한옥 카페입니다. 직접 오랜 시간 끓여낸 십전대보차와 진한 대추차가 대표적이며, 쫀득한 가래떡 구이와 약과를 곁들여 마당 정원을 보며 여유를 즐기기 좋습니다.'
  },
  {
    id: 3,
    name: '남산 힐 그릴',
    category: '양식',
    rating: '4.5',
    location: '서울 용산구 소파로 83',
    phone: '02-753-1234',
    hours: '11:30 ~ 21:30 (Break 15:00~17:00)',
    image: 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=500&q=80',
    description: '남산 뷰를 바라보며 즐기는 시그니처 텍사스식 스모크 립과 스테이크',
    longDescription: '소월길에 자리 잡고 있어 남산 야경을 통유리창으로 조망할 수 있는 정통 아메리칸 그릴 레스토랑입니다. 참나무 향을 입혀 12시간 동안 천천히 구워낸 스모크 립과 부드러운 안심 스테이크가 시그니처 메뉴입니다.'
  },
  {
    id: 4,
    name: '혜화 수제 만두',
    category: '한식',
    rating: '4.7',
    location: '서울 종로구 대학로9길 12',
    phone: '02-744-9981',
    hours: '11:00 ~ 20:30 (매주 월요일 휴무)',
    image: 'https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=500&q=80',
    description: '대학로 연극인들이 사랑하는 푸짐하고 얇은 피의 이북식 손만두 전문점',
    longDescription: '매일 아침 주인장이 직접 빚는 얇고 쫄깃한 이북식 손만두 전골이 주메뉴입니다. 신선한 채소와 버섯, 그리고 담백한 육수가 어우러져 깊은 맛을 냅니다. 고소하고 바삭한 평양식 녹두빈대떡도 훌륭한 사이드 메뉴입니다.'
  }
])

// 카테고리 필터링 계산 프로퍼티
const filteredRestaurants = computed(() => {
  if (selectedCategory.value === '전체') {
    return mockRestaurants.value
  }
  return mockRestaurants.value.filter(r => r.category === selectedCategory.value)
})

const selectRestaurant = (res) => {
  selectedRestaurant.value = res
}
</script>

<style scoped>
@keyframes slideUp {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-slide-up {
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
</style>