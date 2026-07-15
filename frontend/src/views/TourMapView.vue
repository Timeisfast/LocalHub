<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans py-10 px-4">
    <div class="max-w-5xl mx-auto">
      
      <nav class="text-xs text-gray-400 mb-4 font-medium">
        <router-link to="/" class="hover:text-blue-600">홈</router-link> 
        <span class="mx-1">&gt;</span> 
        <span class="text-gray-600 font-semibold">관광지 지도</span>
      </nav>

      <div class="bg-white p-6 rounded-2xl border border-gray-200/70 shadow-sm mb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <span>🗺️</span> 서울 관광 명소 지도
          </h1>
          <p class="text-xs text-gray-400 mt-1">
            지도 위 핀을 클릭해 관광지 정보와 네이버 검색 연결 링크를 확인해 보세요.
          </p>
        </div>
        
        <span class="bg-blue-50 text-blue-600 text-xs font-extrabold px-3 py-1.5 rounded-lg border border-blue-200">
          총 {{ mockTours.length }}개 명소 등록됨
        </span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        
        <div class="lg:col-span-2 relative">
          <div 
            v-if="isMapLoading" 
            class="absolute inset-0 bg-gray-100 flex flex-col items-center justify-center rounded-2xl border border-gray-200 z-10"
          >
            <span class="w-8 h-8 border-3 border-[#03C75A] border-t-transparent rounded-full animate-spin"></span>
            <span class="text-xs text-gray-500 mt-3 font-semibold">지도를 불러오는 중입니다...</span>
          </div>

          <div 
            ref="mapContainer" 
            class="w-full h-[500px] bg-gray-200 rounded-2xl border border-gray-200 shadow-sm overflow-hidden"
          ></div>
        </div>

        <div class="lg:col-span-1 flex flex-col justify-between bg-white p-6 rounded-2xl border border-gray-200/80 shadow-sm min-h-[500px]">
          <div v-if="selectedTour">
            <div class="h-44 w-full overflow-hidden rounded-xl mb-4 relative bg-gray-100">
              <img 
                :src="selectedTour.firstimage" 
                :alt="selectedTour.title" 
                class="w-full h-full object-cover"
                @error="handleImageError"
              />
              <span class="absolute top-2.5 right-2.5 bg-blue-600 text-white text-[10px] font-extrabold px-2 py-0.5 rounded shadow-sm">
                Active
              </span>
            </div>

            <h2 class="text-xl font-bold text-gray-900 mb-2 truncate">{{ selectedTour.title }}</h2>
            
            <div class="space-y-2 text-xs text-gray-600 bg-gray-50 p-3 rounded-lg border border-gray-100 mb-4">
              <p class="flex items-start gap-1">
                <span class="font-bold text-gray-400 w-14 shrink-0">📍 주소</span>
                <span class="flex-1 text-gray-800 leading-relaxed">{{ selectedTour.addr1 }}</span>
              </p>
              <p v-if="selectedTour.tel" class="flex items-start gap-1">
                <span class="font-bold text-gray-400 w-14 shrink-0">📞 전화</span>
                <span class="flex-1 text-gray-800">{{ selectedTour.tel }}</span>
              </p>
            </div>
          </div>

          <div 
            v-else 
            class="flex-1 flex flex-col items-center justify-center text-center text-gray-400 py-10"
          >
            <span class="text-4xl mb-3">📍</span>
            <p class="text-sm font-semibold">지도의 마커를 클릭하시면<br>상세 정보가 나타납니다.</p>
          </div>

          <div class="pt-4 border-t border-gray-100">
            <button 
              :disabled="!selectedTour"
              @click="openNaverSearch"
              class="w-full bg-[#03C75A] hover:bg-[#02b14f] text-white py-3 rounded-xl text-sm font-bold shadow-md disabled:bg-gray-100 disabled:text-gray-400 disabled:shadow-none hover:scale-[1.01] active:scale-[0.99] transition-all flex items-center justify-center gap-2"
            >
              <span>💚</span> 네이버에서 상세 정보 검색하기
            </button>
          </div>
        </div>

      </div>

      <div class="bg-white p-6 rounded-2xl border border-gray-200/80 shadow-sm overflow-hidden">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-lg font-bold text-gray-800 flex items-center gap-2">
            <span>💬</span> 
            <span v-if="selectedTour" class="text-blue-600">"{{ selectedTour.title }}"</span>
            <span v-else>선택된 명소</span> 관련 로컬 이야기
          </h2>
          <router-link to="/posts" class="text-xs font-semibold text-blue-600 hover:underline">
            게시판 바로가기 &rarr;
          </router-link>
        </div>

        <div 
          v-if="!selectedTour" 
          class="py-12 text-center text-gray-400 text-sm font-medium border border-dashed border-gray-200 rounded-xl"
        >
          📍 지도 위의 핀을 클릭해 보세요! 해당 장소가 언급된 이웃들의 게시글을 이곳에서 모아볼 수 있습니다.
        </div>

        <div 
          v-else-if="relatedPosts.length === 0" 
          class="py-12 text-center text-gray-400 text-sm font-medium border border-dashed border-gray-200 rounded-xl"
        >
          😭 아직 이 장소에 관한 게시글이 등록되지 않았습니다. <br>
          <router-link to="/posts/write" class="text-blue-500 underline mt-2 inline-block">
            첫 번째 후기를 작성해 주세요!
          </router-link>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4 animate-slide-up">
          <div 
            v-for="post in relatedPosts" 
            :key="post.id"
            @click="goToPostDetail(post.id)"
            class="group bg-slate-50 hover:bg-blue-50/30 p-5 rounded-xl border border-gray-200/60 hover:border-blue-300 shadow-sm hover:shadow-md transition-all duration-300 cursor-pointer text-left"
          >
            <div class="flex justify-between items-start mb-2.5">
              <span class="bg-blue-100 text-blue-700 text-[10px] font-bold px-2 py-0.5 rounded">
                익명 후기
              </span>
              <span class="text-[11px] text-gray-400 font-medium">{{ post.date }}</span>
            </div>
            
            <h3 class="font-bold text-sm text-gray-900 group-hover:text-blue-600 transition-colors mb-1.5 truncate">
              {{ post.title }}
            </h3>
            
            <p class="text-xs text-gray-500 leading-relaxed line-clamp-2">
              {{ post.content }}
            </p>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { postApi, placeApi } from '@/api/services'
import { useRouter } from 'vue-router'

const router = useRouter()
const mapContainer = ref(null)
const selectedTour = ref(null)
const isMapLoading = ref(true)
const relatedPosts = ref([])
const mockTours = ref([])
let mapInstance = null

watch(selectedTour, async (newTour) => {
  if (!newTour) {
    relatedPosts.value = []
    return
  }

  try {
    const keyword = newTour.title.trim()
    relatedPosts.value = await postApi.searchPosts(keyword)
  } catch (error) {
    console.error("관련 게시글 로드 실패:", error)
    relatedPosts.value = []
  }
})

const goToPostDetail = (postId) => {
  router.push(`/posts/${postId}`)
}

onMounted(async () => {
  try {
    mockTours.value = await placeApi.getPlaces('tourist')
    loadNaverMapScript()
  } catch (error) {
    console.error('관광 명소 데이터 호출 실패:', error)
    isMapLoading.value = false
  }
})

const loadNaverMapScript = () => {
  if (window.naver && window.naver.maps) {
    initMap()
    return
  }

  const clientId = import.meta.env.VITE_NAVER_MAP_CLIENT_ID
  if (!clientId) {
    console.error("❌ .env 파일 내 VITE_NAVER_MAP_CLIENT_ID 변수 값을 확인해 주세요.")
    isMapLoading.value = false
    return
  }

  const script = document.createElement('script')
  script.src = `https://oapi.map.naver.com/openapi/v3/maps.js?ncpKeyId=${clientId}`
  script.async = true

  script.onload = () => {
    initMap()
  }

  script.onerror = () => {
    console.error("네이버 지도 SDK 로드 중 에러가 발생했습니다.")
    isMapLoading.value = false
  }

  document.head.appendChild(script)
}

const initMap = () => {
  if (!mapContainer.value) return

  const defaultCenter = new window.naver.maps.LatLng(
    parseFloat(mockTours.value[0].mapy),
    parseFloat(mockTours.value[0].mapx)
  )

  const mapOptions = {
    center: defaultCenter,
    zoom: 14,
    zoomControl: true,
    zoomControlOptions: {
      position: window.naver.maps.Position.RIGHT_BOTTOM
    }
  }

  mapInstance = new window.naver.maps.Map(mapContainer.value, mapOptions)

  renderMarkers()
  isMapLoading.value = false
}

const renderMarkers = () => {
  mockTours.value.forEach((tour) => {
    const position = new window.naver.maps.LatLng(
      parseFloat(tour.mapy),
      parseFloat(tour.mapx)
    )

    const marker = new window.naver.maps.Marker({
      position: position,
      map: mapInstance,
      title: tour.title,
      animation: window.naver.maps.Animation.DROP 
    })

    window.naver.maps.Event.addListener(marker, 'click', () => {
      selectedTour.value = tour
      mapInstance.panTo(position)
    })
  })
}

const openNaverSearch = () => {
  if (!selectedTour.value) return
  const keyword = encodeURIComponent(selectedTour.value.title)
  window.open(`https://search.naver.com/search.naver?query=${keyword}`, '_blank')
}

const handleImageError = (e) => {
  e.target.src = 'https://images.unsplash.com/photo-1590001155093-a3c66ab0c3ff?auto=format&fit=crop&w=500&q=80'
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;  
  overflow: hidden;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-slide-up {
  animation: slideUp 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
</style>