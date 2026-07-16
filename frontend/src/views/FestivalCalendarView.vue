<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans py-10 px-4">
    <div class="max-w-5xl mx-auto">
      
      <nav class="text-xs text-gray-400 mb-4 font-medium">
        <router-link to="/" class="hover:text-blue-600">홈</router-link> 
        <span class="mx-1">&gt;</span> 
        <span class="text-gray-600 font-semibold">축제 캘린더</span>
      </nav>

      <div class="bg-white p-6 rounded-2xl border border-gray-200/70 shadow-sm mb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <span>📅</span> 서울 축제 & 행사 일정
          </h1>
          <p class="text-xs text-gray-400 mt-1">
            달력의 축제 일정을 클릭하시면 하단에서 상세한 행사 정보를 확인할 수 있습니다.
          </p>
        </div>
        
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

      <div class="bg-white p-6 rounded-2xl border border-gray-200/70 shadow-sm overflow-hidden mb-6">
        <FullCalendar :key="calendarKey" :options="calendarOptions" :dayMaxEvents="4" />
      </div>

      <div class="transition-all duration-300">
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
            <button 
              @click="selectedEvent = null"
              class="text-gray-400 hover:text-gray-600 text-sm font-semibold p-1"
            >
              닫기 ✕
            </button>
          </div>

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
import { ref, onMounted, watch } from 'vue'
import { festivalApi } from '@/api/services'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import { useRoute } from 'vue-router'

const route = useRoute()
const selectedEvent = ref(null)
const festivalEvents = ref([])
const calendarKey = ref(0)

const handleQueryParamLocation = () => {
  const targetId = route.query.id
  if (!targetId || festivalEvents.value.length === 0) return

  const matchedEvent = festivalEvents.value.find(event => event.id === Number(targetId))

  if (matchedEvent) {
    selectedEvent.value = {
      title: matchedEvent.title,
      start: matchedEvent.start,
      end: matchedEvent.end,
      backgroundColor: matchedEvent.backgroundColor,
      extendedProps: matchedEvent.extendedProps
    }
  }
}

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

  dayMaxEvents: 4,
  dayMaxEventRows: 4,
  moreLinkClick: 'popover',

  events: [],
  eventClick: (info) => {
    selectedEvent.value = {
      title: info.event.title,
      start: info.event.startStr,
      end: info.event.endStr ? info.event.endStr : info.event.startStr,
      backgroundColor: info.event.backgroundColor,
      extendedProps: info.event.extendedProps
    }
  }
})

onMounted(async () => {
  try {
    const rawEvents = await festivalApi.getFestivals()

    const parsedEvents = rawEvents.map(event => {
      const title = event.title;
      let bgColor = '#FCE7F3';
      let borderColor = '#FBCFE8';
      let textColor = '#BE185D';

      if (title.includes('야시장') || title.includes('푸드') || title.includes('먹거리')) {
        bgColor = '#EFF6FF';
        borderColor = '#DBEAFE';
        textColor = '#1E40AF';
      } else if (title.includes('문화') || title.includes('역사') || title.includes('전통')) {
        bgColor = '#ECFDF5';
        borderColor = '#D1FAE5';
        textColor = '#065F46';
      } else if (title.includes('페스티벌') || title.includes('전시') || title.includes('공연')) {
        bgColor = '#FDF2F8';
        borderColor = '#FCE7F3';
        textColor = '#9D174D';
      }

      let finalEndDate = event.end_date;
      if (event.start_date && event.end_date) {
        const start = new Date(event.start_date);
        const end = new Date(event.end_date);
        const diffTime = Math.abs(end - start);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        if (diffDays >= 7) {
          finalEndDate = event.start_date; 
        }
      }

      return {
        id: event.id,
        title: event.title,
        start: event.start_date,
        end: finalEndDate ? finalEndDate : event.start_date,
        backgroundColor: bgColor,
        borderColor: borderColor,
        textColor: textColor,
        extendedProps: {
          location: event.addr1,
          description: event.description || '상세 정보가 없습니다.'
        }
      }
    })

    festivalEvents.value = parsedEvents
    calendarOptions.value.events = parsedEvents
    calendarKey.value++

    handleQueryParamLocation()
  } catch (error) {
    console.error('축제 데이터 로드 실패:', error)
  }
})

watch(
  () => route.query.id,
  () => {
    handleQueryParamLocation()
  }
)
</script>

<style>
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
.fc-daygrid-more-link {
  font-size: 11px !important;
  font-weight: 800 !important;
  color: #3b82f6 !important;
  background-color: #eff6ff !important;
  padding: 2px 6px !important;
  border-radius: 4px !important;
  display: inline-block !important;
  margin-top: 2px !important;
  transition: all 0.2s ease;
}

.fc-daygrid-more-link:hover {
  background-color: #dbeafe !important;
  text-decoration: none !important;
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

@keyframes slideUp {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-slide-up {
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
</style>