<template>
  <p class="pt-3 text-left text-18 text-darkBlue fw-600">Event</p>

  <!-- ── Custom Skeleton shimmer ─────────────────────── -->
  <div v-if="!isReady" class="skeleton-event-card">
    <!-- Banner image placeholder -->
    <div class="skeleton-banner">
      <div class="skeleton-live-badge"></div>
    </div>

    <!-- Info area -->
    <div class="skeleton-info">
      <!-- Title row -->
      <div class="skeleton-row skeleton-row--title">
        <div class="skeleton-chevron"></div>
        <div class="skeleton-title"></div>
        <div class="skeleton-chevron"></div>
      </div>

      <!-- Clock row -->
      <div class="skeleton-row skeleton-row--item">
        <div class="skeleton-icon-box"></div>
        <div class="skeleton-lines">
          <div class="skeleton-line skeleton-line--primary"></div>
          <div class="skeleton-line skeleton-line--secondary"></div>
        </div>
      </div>

      <!-- Location row -->
      <div class="skeleton-row skeleton-row--item">
        <div class="skeleton-icon-box"></div>
        <div class="skeleton-lines">
          <div class="skeleton-line skeleton-line--primary"></div>
          <div class="skeleton-line skeleton-line--secondary"></div>
        </div>
      </div>
    </div>

    <!-- Footer btn -->
    <div class="skeleton-footer">
      <div class="skeleton-see-more"></div>
    </div>
  </div>

  <template v-if="isReady && emptyState">
    <img
      :src="require('@/v2/assets/empty/no_available_state.svg')"
      class="img-no-available"
      width="100%"
      height="120vh"
    />
  </template>
  <template v-else>
    <v-card
      class="border-radius-dwp mr-1 event-card"
      elevation="4"
      v-if="isReady && length > 0"
    >
      <v-window v-model="onboarding">
        <v-window-item v-for="n in length" :key="`card-${n}`" :value="n">
          <v-img
            v-if="listData[n - 1].eventTemplateType == 'RDG'"
            :src="listData[n - 1].bannerHighlightEvent"
            class=""
          >
            <v-toolbar color="rgba(0, 0, 0, 0)">
              <template v-slot:prepend>
                <div class="live-text" v-if="listData[n - 1].liveStatus">
                  Live
                </div>
              </template>
            </v-toolbar>
          </v-img>
          <v-img v-else src="@/v2/assets/home/event_banner_low.png" class="">
            <v-toolbar color="rgba(0, 0, 0, 0)">
              <template v-slot:prepend>
                <div class="live-text" v-if="listData[n - 1].liveStatus">
                  Live
                </div>
              </template>
            </v-toolbar>
          </v-img>

          <v-card
            min-height="200px"
            class="justify-center align-center pt-5"
            style="border-radius: 0px"
          >
            <v-row no-gutters>
              <v-col cols="1">
                <v-btn
                  v-if="length > 1"
                  variant="plain"
                  icon="mdi-chevron-left"
                  @click="prev"
                ></v-btn
              ></v-col>
              <v-col cols="10" class="align-self-center">
                <p
                  class="text-left pl-2 font-weight-bold text-newBlack event-title"
                >
                  {{ listData[n - 1].title }}
                </p>
              </v-col>
              <v-col cols="1" style="text-align-last: end">
                <v-btn
                  v-if="length > 1"
                  variant="plain"
                  icon="mdi-chevron-right"
                  @click="next"
                ></v-btn>
              </v-col>
            </v-row>
            <v-list class="ml-3">
              <v-list-item
                :title="listData[n - 1].eventDate"
                :subtitle="listData[n - 1].eventTime"
                class="text-black font-weight-bold text-left text-subtitle-2 event-list-item"
              >
                <template v-slot:prepend>
                  <div class="bg-young-grey pa-1 rounded-lg mr-4">
                    <v-icon color="#4B4B4B">mdi-clock-outline</v-icon>
                  </div>
                </template>
              </v-list-item>
              <v-list-item
                :title="listData[n - 1].method"
                :subtitle="listData[n - 1].meetingPlatform"
                class="text-black text-left text-subtitle-2 event-list-item"
                style="animation-delay: 0.1s"
              >
                <template v-slot:prepend>
                  <div class="bg-young-grey pa-1 rounded-lg mr-4">
                    <v-icon color="#4B4B4B">mdi-map-marker-outline</v-icon>
                  </div>
                </template>
              </v-list-item>
            </v-list>
          </v-card>
        </v-window-item>
      </v-window>
      <v-item-group v-model="onboarding" class="text-center" mandatory>
        <v-item
          v-for="n in length"
          :key="`btn-${n}`"
          v-slot="{ isSelected, toggle }"
          :value="n"
        >
          <v-btn
            v-if="length > 1"
            variant="text"
            :style="{ color: isSelected ? '#065695' : 'grey' }"
            icon="mdi-record"
            size="x-small"
            @click="toggle"
            class="ml-n4"
          ></v-btn>
        </v-item>
      </v-item-group>
      <template v-if="length > 0">
        <v-divider class="mt-1"></v-divider>
        <v-btn
          class="mb-1 mt-1 text-cammelCase btn-see-more"
          variant="text"
          width="100%"
          @click="handleDetail(onboarding)"
        >
          <p class="text-gradient-red">See More</p>
          <!-- :to="{ name: 'v2.meeting-management' }" -->
        </v-btn>
      </template>
    </v-card>
  </template>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const router = useRouter();
const listData = ref<EventBanner[]>([]);
const length = ref(0);
const onboarding = ref(1);
const emptyState = ref(false);
const store = useStore();

const isReady = ref(false);

store.dispatch("eventStore/fetchHighlightEvent").then((data) => {
  if (data.data) {
    listData.value = data.data;
    if (listData.value.length > 0) {
      length.value = listData.value.length;
    } else {
      emptyState.value = true;
    }
  } else {
    length.value = 0;
    emptyState.value = true;
  }
  isReady.value = true;
});

const next = () => {
  onboarding.value =
    onboarding.value + 1 > length.value ? 1 : onboarding.value + 1;
};

const prev = () => {
  onboarding.value =
    onboarding.value - 1 <= 0 ? length.value : onboarding.value - 1;
};

const handleDetail = (temp) => {
  let data = listData.value[temp - 1];
  router.push({
    name: "v2.meeting-detail-description",
    params: { idEvent: data.id },
  });
};

const autoSlide: any = () => {
  setInterval(() => {
    next();
  }, 15000);
};

onMounted(() => {
  autoSlide();
});

onUnmounted(() => {
  clearInterval(autoSlide);
});

interface EventBanner {
  id: string;
  title: string;
  eventDate: string;
  eventTime: string;
  method: string;
  meetingPlatform: string;
  liveStatus: boolean;
  bannerHighlightEvent: string;
  eventTemplateType: string;
}
</script>

<style scoped>
:deep(.v-img__img) {
  width: 100% !important;
}
.bg-young-grey {
  background-color: #f0f0f0;
}

/* ── Live badge pulse ──────────────────────────────── */
.live-text {
  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
  padding: 0 10px;
  border-radius: 4px;
  font-size: 12px;
  line-height: 24px;
  text-align: center;
  color: white;
  font-weight: 600;
  letter-spacing: 0.1px;
  white-space: nowrap;
  animation: livePulse 1.6s ease-in-out infinite;
}

@keyframes livePulse {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(220, 33, 42, 0.55);
  }
  50% {
    box-shadow: 0 0 0 6px rgba(220, 33, 42, 0);
  }
}

:deep(.v-list-item-title) {
  font-size: 14px;
}
:deep(.v-list-item-subtitle) {
  font-size: 12px;
}

/* ── Card entrance animation ───────────────────────── */
.event-card {
  animation: fadeSlideUp 0.45s ease-out both;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.event-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.12) !important;
}

/* Title slide in */
.event-title {
  animation: slideInLeft 0.5s ease-out both;
}

/* List items slide in with stagger */
.event-list-item {
  animation: slideInLeft 0.5s ease-out both;
}

/* See More button */
.btn-see-more {
  transition: opacity 0.2s ease;
}
.btn-see-more:hover {
  opacity: 0.75;
}

/* ── Skeleton card ─────────────────────────────────── */
.skeleton-event-card {
  border-radius: 12px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 12px;
  animation: fadeSlideUp 0.35s ease-out both;
}

/* Banner placeholder */
.skeleton-banner {
  width: 100%;
  height: 160px;
  background: #e0e0e0;
  position: relative;
  overflow: hidden;
}
.skeleton-banner::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.5) 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: shimmerSweep 1.4s ease-in-out infinite;
}

.skeleton-live-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  width: 40px;
  height: 20px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.35);
}

/* Info section */
.skeleton-info {
  padding: 14px 16px 4px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.skeleton-row {
  display: flex;
  align-items: center;
}

.skeleton-row--title {
  justify-content: space-between;
  gap: 8px;
}

.skeleton-row--item {
  gap: 12px;
}

.skeleton-chevron {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #eeeeee;
  flex-shrink: 0;
  position: relative;
  overflow: hidden;
}
.skeleton-chevron::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.6),
    transparent
  );
  background-size: 200% 100%;
  animation: shimmerSweep 1.4s ease-in-out infinite 0.05s;
}

.skeleton-title {
  flex: 1;
  height: 13px;
  border-radius: 6px;
  background: #eeeeee;
  position: relative;
  overflow: hidden;
}
.skeleton-title::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.65),
    transparent
  );
  background-size: 200% 100%;
  animation: shimmerSweep 1.4s ease-in-out infinite;
}

.skeleton-icon-box {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: #eeeeee;
  flex-shrink: 0;
  position: relative;
  overflow: hidden;
}
.skeleton-icon-box::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.65),
    transparent
  );
  background-size: 200% 100%;
  animation: shimmerSweep 1.4s ease-in-out infinite 0.1s;
}

.skeleton-lines {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.skeleton-line {
  border-radius: 6px;
  background: #eeeeee;
  position: relative;
  overflow: hidden;
}
.skeleton-line--primary {
  height: 12px;
  width: 70%;
}
.skeleton-line--secondary {
  height: 10px;
  width: 50%;
}

.skeleton-line::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.65),
    transparent
  );
  background-size: 200% 100%;
  animation: shimmerSweep 1.4s ease-in-out infinite 0.2s;
}

/* Footer */
.skeleton-footer {
  padding: 10px 16px 12px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: center;
}

.skeleton-see-more {
  width: 80px;
  height: 12px;
  border-radius: 6px;
  background: #eeeeee;
  position: relative;
  overflow: hidden;
}
.skeleton-see-more::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.65),
    transparent
  );
  background-size: 200% 100%;
  animation: shimmerSweep 1.4s ease-in-out infinite 0.3s;
}

/* ── Shared keyframes ──────────────────────────────── */
@keyframes shimmerSweep {
  from {
    background-position: -200% 0;
  }
  to {
    background-position: 200% 0;
  }
}

@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-16px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
