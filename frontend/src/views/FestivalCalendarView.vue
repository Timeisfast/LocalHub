<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans py-10 px-4">
    <div class="max-w-5xl mx-auto">
      
      <!-- 1. 브레드크럼 -->
      <nav class="text-xs text-gray-400 mb-4 font-medium">
        <router-link to="/" class="hover:text-blue-600">홈</router-link> 
        <span class="mx-1">&gt;</span> 
        <span class="text-gray-600 font-semibold">축제 캘린더</span>
      </nav>

      <!-- 2. 상단 헤더 카드 -->
      <div class="bg-white p-6 rounded-2xl border border-gray-200/70 shadow-sm mb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <span>📅</span> 서울 축제 & 행사 일정
          </h1>
          <p class="text-xs text-gray-400 mt-1">
            달력의 축제 일정을 클릭하시면 하단에서 상세한 행사 정보를 확인할 수 있습니다.
          </p>
        </div>
        
        <!-- 범례 (Legend) -->
        <div class="flex flex-wrap gap-3 bg-slate-50 p-3 rounded-xl border border-gray-100">
          <div class="flex items-center gap-1.5 text-xs font-semibold text-gray-600">
            <span class="w-3 h-3 rounded bg-blue-500 inline-block"></span> 야시장/푸드
          </div>
          <div class="flex items-center gap-1.5 text-xs font-semibold text-gray-600">
            <span class="w-3 h-3 rounded bg-emerald-500 inline-block"></span> 문화/역사
          </div>
          <div class="flex items-center gap-1.5 text-xs font-semibold text-gray-600">
            <span class="w-3 h-3 rounded bg-pink-500 inline-block"></span> 페스티벌/전시
          </div>
        </div>
      </div>

      <!-- 3. 메인 캘린더 레이아웃 영역 -->
      <div class="bg-white p-6 rounded-2xl border border-gray-200/70 shadow-sm overflow-hidden mb-6">
        <FullCalendar :options="calendarOptions" />
      </div>

      <!-- 4. 캘린더 하단: 선택된 행사 상세 정보 카드 (개선 적용 부분) -->
      <div class="transition-all duration-300">
        <!-- 선택된 행사가 있을 때 -->
        <div 
          v-if="selectedEvent" 
          class="bg-white p-6 rounded-2xl border-2 border-blue-500/30 shadow-md animate-slide-up"
        >
          <div class="flex justify-between items-start mb-4">
            <div class="flex items-center gap-2">
              <span 
                class="w-3 h-3 rounded-full" 
                :style="{ backgroundColor: selectedEvent.backgroundColor }"
              ></span>
              <h2 class="text-xl font-bold text-gray-900">{{ selectedEvent.title }}</h2>
            </div>
            <!-- 닫기 버튼 -->
            <button 
              @click="selectedEvent = null"
              class="text-gray-400 hover:text-gray-600 text-sm font-semibold p-1"
            >
              닫기 ✕
            </button>
          </div>

          <!-- 세부 가이드 표 레이아웃 -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-700 bg-slate-50 p-4 rounded-xl border border-gray-100">
            <div>
              <p class="mb-2"><span class="font-bold text-gray-500 inline-block w-20">📅 기간:</span> {{ selectedEvent.start }} ~ {{ selectedEvent.end }}</p>
              <p><span class="font-bold text-gray-500 inline-block w-20">📍 장소:</span> {{ selectedEvent.extendedProps.location }}</p>
            </div>
            <div>
              <p class="leading-relaxed">
                <span class="font-bold text-gray-500 block mb-1">💡 축제 정보:</span>
                {{ selectedEvent.extendedProps.description }}
              </p>
            </div>
          </div>
        </div>

        <!-- 아무것도 선택하지 않았을 때의 안내 문구 -->
        <div 
          v-else 
          class="bg-white py-10 px-6 rounded-2xl border border-dashed border-gray-300 text-center text-gray-400 text-sm font-medium"
        >
          🔍 달력에서 궁금한 축제 일정을 클릭해 보세요! 상세한 안내가 여기에 표시됩니다.
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'

// 현재 사용자가 클릭하여 선택한 축제 데이터 상태
const selectedEvent = ref(null)

// 축제 가상 데이터 (장소 및 풍성한 디테일 추가)
const festivalEvents = ref([
  { 
    title: '🍔 한강 달빛 야시장', 
    start: '2026-07-03', 
    end: '2026-07-06', 
    backgroundColor: '#3B82F6', 
    borderColor: '#2563EB',
    extendedProps: { 
      location: '여의도 한강공원 일대',
      description: '맛있는 푸드트럭 먹거리와 아기자기한 수공예 셀러들이 한곳에 모이는 서울의 대표 야시장 축제입니다. 시원한 한강 강바람과 야경을 즐기며 낭만적인 밤을 보내보세요!'
    }
  },
  { 
    title: '🏛️ 경복궁 야간 특별 관람', 
    start: '2026-07-08', 
    end: '2026-07-13', 
    backgroundColor: '#10B981', 
    borderColor: '#059669',
    extendedProps: { 
      location: '경복궁 광화문 및 흥례문 일원',
      description: '고궁의 밤을 거닐 수 있는 상반기 경복궁 특별 야간 관람 행사입니다. 은은하고 따뜻한 빛에 둘러싸인 한옥의 고즈넉한 멋을 감상하며 데이트나 가족 나들이를 떠나보세요.'
    }
  },
  { 
    title: '💦 신촌 물총 페스티벌', 
    start: '2026-07-17', 
    end: '2026-07-19', 
    backgroundColor: '#EC4899', 
    borderColor: '#DB2777',
    extendedProps: { 
      location: '신촌 연세로 차 없는 거리',
      description: '한여름 무더위를 날려 버릴 가장 역동적인 도심 축제! 남녀노소 신나게 즐기는 물총 싸움부터 쏟아지는 물줄기와 어우러지는 신나는 DJ 일렉트로닉 댄스 파티까지 준비되어 있습니다.'
    }
  },
  { 
    title: '🎨 DDP 서울라이트 가을 전시', 
    start: '2026-07-22', 
    end: '2026-07-27', 
    backgroundColor: '#EC4899', 
    borderColor: '#DB2777',
    extendedProps: { 
      location: '동대문디자인플라자(DDP) 서측 외벽',
      description: 'DDP의 은빛 비정형 외벽을 캔버스 삼아 환상적인 미디어가 투사되는 대형 빛 축제입니다. 세계적인 아티스트들의 미디어 아트를 통해 빛의 물결을 감상해 보세요.'
    }
  },
  { 
    title: '🍺 신촌 맥주 축제', 
    start: '2026-07-29', 
    end: '2026-08-01', 
    backgroundColor: '#3B82F6', 
    borderColor: '#2563EB',
    extendedProps: { 
      location: '신촌 이대/연세 광장 및 골목 상권',
      description: '전국의 개성 넘치는 로컬 수제 맥주 브루어리들이 대거 참여하는 축제입니다. 감미로운 라이브 버스킹 음악을 배경으로 시원하고 목 넘김이 좋은 맥주와 어울리는 푸드 페어링을 경험해 보세요.'
    }
  }
])

const calendarOptions = ref({
  plugins: [dayGridPlugin],
  initialView: 'dayGridMonth',
  locale: 'ko',
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: ''
  },
  height: 'auto',
  events: festivalEvents.value,
  // 💡 [핵심 변경] 클릭 시 alert 대신 로컬 Vue 상태에 이벤트 객체를 매핑함
  eventClick: (info) => {
    selectedEvent.value = {
      title: info.event.title,
      start: info.event.startStr,
      // FullCalendar 특성상 end가 null인 하루짜리 일정을 대비한 삼항 연산자 가이드라인
      end: info.event.endStr ? info.event.endStr : info.event.startStr,
      backgroundColor: info.event.backgroundColor,
      extendedProps: info.event.extendedProps
    }
  }
})
</script>

<style>
/* ... (이전 FullCalendar 커스텀 스타일 동일하게 적용) ... */
.fc {
  font-family: inherit;
}
.fc .fc-toolbar-title {
  font-size: 1.25rem !important;
  font-weight: 800 !important;
  color: #1f2937;
}
.fc .fc-col-header-cell-cushion {
  font-size: 13px;
  font-weight: 700;
  color: #4b5563;
  text-decoration: none !important;
  padding: 8px 0 !important;
}
.fc .fc-daygrid-day-number {
  font-size: 12px;
  font-weight: 500;
  color: #6b7280;
  text-decoration: none !important;
  padding: 6px 8px !important;
}
.fc .fc-day-sun .fc-col-header-cell-cushion,
.fc .fc-day-sun .fc-daygrid-day-number {
  color: #ef4444 !important;
}
.fc .fc-day-sat .fc-col-header-cell-cushion,
.fc .fc-day-sat .fc-daygrid-day-number {
  color: #3b82f6 !important;
}
.fc .fc-day-today {
  background-color: #eff6ff !important;
}
.fc-v-event, .fc-h-event {
  border-radius: 6px !important;
  padding: 3px 6px !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: transform 0.1s ease;
}
.fc-v-event:hover, .fc-h-event:hover {
  transform: translateY(-1px);
}
.fc .fc-button-primary {
  background-color: #f3f4f6 !important;
  border-color: #e5e7eb !important;
  color: #4b5563 !important;
  font-size: 12px !important;
  font-weight: 700 !important;
  border-radius: 8px !important;
  padding: 6px 12px !important;
}
.fc .fc-button-primary:hover {
  background-color: #e5e7eb !important;
}

/* 아래서 솟아오르는 인터랙션 애니메이션 */
@keyframes slideUp {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-slide-up {
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
</style>