<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans py-10 px-4">
    <div class="max-w-5xl mx-auto">
      
      <!-- 1. 브레드크럼 -->
      <nav class="text-xs text-gray-400 mb-4 font-medium">
        <router-link to="/" class="hover:text-blue-600">홈</router-link> 
        <span class="mx-1">&gt;</span> 
        <span class="text-gray-600 font-semibold">관광지 지도</span>
      </nav>

      <!-- 2. 상단 헤더 카드 -->
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

      <!-- 3. 메인 레이아웃 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- 지도 영역 -->
        <div class="lg:col-span-2 relative">
          <!-- 지도 로딩 표시용 스켈레톤 -->
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

        <!-- 4. 우측 상세 정보 패널 -->
        <div class="lg:col-span-1 flex flex-col justify-between bg-white p-6 rounded-2xl border border-gray-200/80 shadow-sm min-h-[400px]">
          <div v-if="selectedTour">
            <!-- 썸네일 이미지 -->
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

            <!-- 기본 정보 -->
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

          <!-- 미선택 상태 가이드 -->
          <div 
            v-else 
            class="flex-1 flex flex-col items-center justify-center text-center text-gray-400 py-10"
          >
            <span class="text-4xl mb-3">📍</span>
            <p class="text-sm font-semibold">지도의 마커를 클릭하시면<br>상세 정보가 나타납니다.</p>
          </div>

          <!-- 5. 네이버 검색 연동 버튼 -->
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

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const mapContainer = ref(null)
const selectedTour = ref(null)
const isMapLoading = ref(true)
let mapInstance = null

// 공공 데이터 기반 가상 리스트
const mockTours = ref([
  {
    contentid: "1059877",
    title: "양화한강공원",
    addr1: "서울특별시 영등포구 노들로 221 (당산동)",
    firstimage: "https://tong.visitkorea.or.kr/cms/resource_photo/46/3551346_image2_1.jpg",
    mapx: "126.9023658810",
    mapy: "37.5382819489",
    tel: "02-3780-0581"
  },
  {
    contentid: "1234567",
    title: "여의도 한강공원",
    addr1: "서울특별시 영등포구 여의동로 330",
    firstimage: "https://images.unsplash.com/photo-1540959733332-eab4deceeaf7?auto=format&fit=crop&w=500&q=80",
    mapx: "126.934086",
    mapy: "37.528430",
    tel: "02-3780-0561"
  }
])

onMounted(() => {
  loadNaverMapScript()
})

// 1. 네이버 지도 스크립트 동적 비동기 로딩
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
  // 네이버 지도 스크립트 요청 URL 양식
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

// 2. 네이버 지도 초기화 및 마커 렌더링
const initMap = () => {
  if (!mapContainer.value) return

  // 경위도 좌표 지정 (기본 중심: 양화한강공원)
  const defaultCenter = new window.naver.maps.LatLng(
    parseFloat(mockTours.value[0].mapy),
    parseFloat(mockTours.value[0].mapx)
  )

  const mapOptions = {
    center: defaultCenter,
    zoom: 14, // 네이버 지도는 줌 범위가 카카오맵과 다르므로 기본값 14 내외가 적당합니다.
    zoomControl: true, // 우측 줌 컨트롤러 자동 탑재
    zoomControlOptions: {
      position: window.naver.maps.Position.RIGHT_BOTTOM
    }
  }

  mapInstance = new window.naver.maps.Map(mapContainer.value, mapOptions)

  renderMarkers()
  isMapLoading.value = false
}

// 3. 마커 생성 및 클릭 리스너 설정
const renderMarkers = () => {
  mockTours.value.forEach((tour) => {
    const position = new window.naver.maps.LatLng(
      parseFloat(tour.mapy),
      parseFloat(tour.mapx)
    )

    // 네이버 마커 생성 규격
    const marker = new window.naver.maps.Marker({
      position: position,
      map: mapInstance,
      title: tour.title,
      // 네이버 기본 핀에 애니메이션 효과 추가 (선택 사항)
      animation: window.naver.maps.Animation.DROP 
    })

    // 네이버 지도 이벤트 리스너 바인딩 (naver.maps.Event 사용)
    window.naver.maps.Event.addListener(marker, 'click', () => {
      selectedTour.value = tour
      
      // 마커를 클릭하면 부드럽게 지도의 중심을 마커 위치로 이동
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