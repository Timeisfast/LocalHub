<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans py-10 px-4">
    <div class="max-w-5xl mx-auto">
      
      <!-- 브레드크럼 -->
      <nav class="text-xs text-gray-400 mb-4 font-medium">
        <router-link to="/" class="hover:text-blue-600">홈</router-link> 
        <span class="mx-1">&gt;</span> 
        <span class="text-gray-600 font-semibold">쇼핑 명소 지도</span>
      </nav>

      <!-- 상단 헤더 -->
      <div class="bg-white p-6 rounded-2xl border border-gray-200/70 shadow-sm mb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <span>🛍️</span> 서울 쇼핑 명소 지도
          </h1>
          <p class="text-xs text-gray-400 mt-1">
            지도 위 핀을 클릭해 쇼핑 명소 정보와 네이버 검색 연결 링크를 확인해 보세요.
          </p>
        </div>
        
        <span class="bg-blue-50 text-blue-600 text-xs font-extrabold px-3 py-1.5 rounded-lg border border-blue-200">
          총 {{ mockShops.length }}개 명소 등록됨
        </span>
      </div>

      <!-- 메인 레이아웃 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- 지도 영역 -->
        <div class="lg:col-span-2 relative">
          <!-- 지도 로딩 스켈레톤 -->
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

        <!-- 우측 상세 정보 패널 -->
        <div class="lg:col-span-1 flex flex-col justify-between bg-white p-6 rounded-2xl border border-gray-200/80 shadow-sm min-h-[400px]">
          <div v-if="selectedShop">
            <!-- 썸네일 이미지 -->
            <div class="h-44 w-full overflow-hidden rounded-xl mb-4 relative bg-gray-100">
              <img 
                :src="selectedShop.firstimage" 
                :alt="selectedShop.title" 
                class="w-full h-full object-cover"
                @error="handleImageError"
              />
              <span class="absolute top-2.5 right-2.5 bg-blue-600 text-white text-[10px] font-extrabold px-2 py-0.5 rounded shadow-sm">
                Shopping
              </span>
            </div>

            <!-- 기본 정보 -->
            <h2 class="text-xl font-bold text-gray-900 mb-2 truncate">{{ selectedShop.title }}</h2>
            
            <div class="space-y-2 text-xs text-gray-600 bg-gray-50 p-3 rounded-lg border border-gray-100 mb-4">
              <p class="flex items-start gap-1">
                <span class="font-bold text-gray-400 w-14 shrink-0">📍 주소</span>
                <span class="flex-1 text-gray-800 leading-relaxed">{{ selectedShop.addr1 }}</span>
              </p>
              <p v-if="selectedShop.tel" class="flex items-start gap-1">
                <span class="font-bold text-gray-400 w-14 shrink-0">📞 전화</span>
                <span class="flex-1 text-gray-800">{{ selectedShop.tel }}</span>
              </p>
            </div>
          </div>

          <!-- 미선택 상태 가이드 -->
          <div 
            v-else 
            class="flex-1 flex flex-col items-center justify-center text-center text-gray-400 py-10"
          >
            <span class="text-4xl mb-3">🛍️</span>
            <p class="text-sm font-semibold">지도의 쇼핑 핀을 클릭하시면<br>상세 정보가 나타납니다.</p>
          </div>

          <!-- 네이버 검색 연동 버튼 -->
          <div class="pt-4 border-t border-gray-100">
            <button 
              :disabled="!selectedShop"
              @click="openNaverSearch"
              class="w-full bg-[#03C75A] hover:bg-[#02b14f] text-white py-3 rounded-xl text-sm font-bold shadow-md disabled:bg-gray-100 disabled:text-gray-400 disabled:shadow-none hover:scale-[1.01] active:scale-[0.99] transition-all flex items-center justify-center gap-2"
            >
              <span>💚</span> 네이버에서 매장 정보 검색하기
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
const selectedShop = ref(null)
const isMapLoading = ref(true)
let mapInstance = null

// 공공데이터 스펙과 일치하게 설계된 쇼핑 가상 데이터 리스트
const mockShops = ref([
  {
    contentid: "2000001",
    title: "통인시장",
    addr1: "서울특별시 종로구 자하문로15길 18",
    firstimage: "https://images.unsplash.com/photo-1506084868230-bb9d95c24759?auto=format&fit=crop&w=500&q=80",
    mapx: "126.969796",
    mapy: "37.580811",
    tel: "02-722-0913"
  },
  {
    contentid: "2000002",
    title: "더현대 서울",
    addr1: "서울특별시 영등포구 여의대로 108",
    firstimage: "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=500&q=80",
    mapx: "126.928424",
    mapy: "37.525897",
    tel: "02-767-2233"
  },
  {
    contentid: "2000003",
    title: "동대문 평화시장",
    addr1: "서울특별시 중구 청계천로 246",
    firstimage: "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=500&q=80",
    mapx: "127.007622",
    mapy: "37.569941",
    tel: "02-2265-3531"
  }
])

onMounted(() => {
  loadNaverMapScript()
})

const loadNaverMapScript = () => {
  if (window.naver && window.naver.maps) {
    initMap()
    return
  }

  const clientId = import.meta.env.VITE_NAVER_MAP_CLIENT_ID
  if (!clientId) {
    console.error("❌ VITE_NAVER_MAP_CLIENT_ID가 설정되지 않았습니다.")
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
    console.error("네이버 지도 로딩 실패")
    isMapLoading.value = false
  }

  document.head.appendChild(script)
}

const initMap = () => {
  if (!mapContainer.value) return

  const defaultCenter = new window.naver.maps.LatLng(
    parseFloat(mockShops.value[0].mapy),
    parseFloat(mockShops.value[0].mapx)
  )

  const mapOptions = {
    center: defaultCenter,
    zoom: 13,
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
  mockShops.value.forEach((shop) => {
    const position = new window.naver.maps.LatLng(
      parseFloat(shop.mapy),
      parseFloat(shop.mapx)
    )

    const marker = new window.naver.maps.Marker({
      position: position,
      map: mapInstance,
      title: shop.title,
      animation: window.naver.maps.Animation.DROP
    })

    window.naver.maps.Event.addListener(marker, 'click', () => {
      selectedShop.value = shop
      mapInstance.panTo(position)
    })
  })
}

const openNaverSearch = () => {
  if (!selectedShop.value) return
  const keyword = encodeURIComponent(selectedShop.value.title)
  window.open(`https://search.naver.com/search.naver?query=${keyword}`, '_blank')
}

const handleImageError = (e) => {
  e.target.src = 'https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?auto=format&fit=crop&w=500&q=80'
}
</script>