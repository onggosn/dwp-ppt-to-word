<template>
  <div>
    <p class="pt-0 ml-6 text-left text-18 text-darkBlue fw-600">Worklist</p>
    <p class="pt-0 ml-6 text-left text-13 text-darkBlue fw-400">
      A list of pending tasks to help you manage your work efficiently.
    </p>
    <template v-if="isLoading">
      <div class="mx-5 mt-4">
        <div
          v-for="index in 5"
          :key="index"
          class="skeleton-card"
          :style="{ animationDelay: `${(index - 1) * 0.1}s` }"
        >
          <!-- Left accent bar -->
          <div class="skeleton-accent"></div>

          <!-- Card body -->
          <div class="skeleton-body">
            <!-- Title block -->
            <div class="skeleton-title"></div>
            <!-- Status block -->
            <div class="skeleton-status"></div>
            <!-- Button block -->
            <div class="skeleton-btn"></div>
          </div>
        </div>
      </div>
    </template>
    <template v-else>
      <template v-if="list.length == 0">
        <img
          :src="require('@/v2/assets/empty/no_available_state.svg')"
          class="img-no-available"
        />
      </template>
      <template v-else>
        <template v-for="(item, index) in list" :key="item.id">
          <v-card
            :class="['card-task mt-5 mb-5 ml-5 mr-5', getCardBorder(item.type)]"
            elevation="4"
            :style="{ animationDelay: `${index * 0.08}s` }"
          >
            <v-row no-gutters class="align-center">
              <v-col :cols="hasValidFileType(item) ? 4 : 6">
                <v-sheet
                  class="text-ellipsis pa-2 text-left text-15 fw-600 text-newBlack ml-4"
                >
                  {{ item.title }}
                  <v-tooltip activator="parent" location="bottom">
                    {{ item.title }}
                  </v-tooltip>
                </v-sheet>
              </v-col>
              <v-col cols="2" v-if="hasValidFileType(item)">
                <v-sheet class="pa-2 ma-2 text-center">
                  <img
                    style="width: 24px; height: 30px"
                    :src="getImageSrc(item.fileType ?? '')"
                  />
                </v-sheet>
              </v-col>
              <v-col>
                <v-sheet class="pa-2 ma-2 text-13 fw-700 text-center">
                  <span :style="{ color: getStatusLabelColor(item.status) }">
                    {{ item.status }}
                  </span>
                </v-sheet>
              </v-col>
              <v-col cols="2">
                <v-sheet class="pa-2 ma-2">
                  <v-btn
                    :size="isSmallScreen ? 'small' : 'default'"
                    class="bg-gradient-darkred text-white border-radius-dwp fw-600"
                    :class="isSmallScreen ? 'text-11' : 'text-14'"
                    @click="seeDetail(item)"
                    :loading="loadingButtons[item.id] || false"
                  >
                    See Detail</v-btn
                  >
                </v-sheet>
              </v-col>
            </v-row>
          </v-card>
        </template>

        <v-btn
          variant="text"
          class="btn-see-all ml-2 fw-600 text-14"
          color="#267DC2"
          @click="router.push({ name: 'dashboard.workspace.v2' })"
        >
          <span class="text-decoration-underline font-italic">See More</span>
          &nbsp;>>
        </v-btn>
      </template>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { useDisplay } from "vuetify";
import { TWorklistItem } from "@v2/Type";
import { getStatusLabelColor } from "@v2/helpers/color";

const store = useStore();
const router = useRouter();
const { width } = useDisplay();
const list = ref<TWorklistItem[]>([]);
const isLoading = computed(() => store.getters["homeStore/getIsLoading"]);
const loadingButtons = ref<Record<string, boolean>>({});
const isSmallScreen = computed(() => width.value <= 1180);

onMounted(() => {
  getList();
});

function getList() {
  store.dispatch("homeStore/getTop5WorkList").then((response) => {
    list.value = response?.responseData;
  });
}

function hasValidFileType(item: any) {
  return item.fileType && item.fileType !== "-" && item.fileType !== "";
}

function getImageSrc(extension: string) {
  switch (extension) {
    case ".pptx":
    case ".ppt":
      return require("@v2/assets/icon/docImage/iconPpt.svg");
    case ".docx":
    case ".doc":
      return require("@v2/assets/icon/docImage/iconWord.svg");
    case ".pdf":
      return require("@v2/assets/icon/docImage/iconPdf.svg");
    default:
      return require("@v2/assets/icon/docImage/iconPpt.svg");
  }
}

function getRouteConfig(item: TWorklistItem): {
  name: string;
  params: Record<string, any>;
} {
  switch (item.type.toLowerCase()) {
    case "assignment":
      return {
        name: "assignment-detail-new",
        params: { id: item.id },
      };

    case "meetingmaterial":
      return {
        name: "v2.meeting-detail-material",
        params: { idEvent: item.idEvent },
      };

    case "meetinghasil":
      return {
        name: "v2.meeting-detail-result",
        params: { idEvent: item.idEvent },
      };

    case "bpdocument":
    default:
      return {
        name: ["rdgb", "rdgtk"].includes(item.linkHelper ?? "")
          ? "v2.rdg-collaboration"
          : "om.rdg-collaboration",
        params: {
          typeRDG: item.linkHelper,
          idEvent: item.idEvent,
          idDoc: item.id,
        },
      };
  }
}

function getCardBorder(type: string) {
  const t = type.toLowerCase();
  if (t === "bpdocument") return "border-bpdocument";
  if (t === "assignment") return "border-assignment";
  if (t === "meetingmaterial" || t === "meetinghasil") return "border-meeting";
  return "border-bpdocument";
}

function seeDetail(item: TWorklistItem): void {
  loadingButtons.value[item.id] = true;
  const routeConfig = getRouteConfig(item);
  router.push(routeConfig).finally(() => {
    loadingButtons.value[item.id] = false;
  });
}
</script>
<style scoped>
.img-no-available {
  margin-top: 5vh;
  width: 100%;
  height: 20vh;
  margin-bottom: 5vh;
}
.card-task {
  background-color: white;
  border-radius: 25px;
  padding: 2px;
  border-left: 5px solid #065695;

  /* Entrance animation */
  animation: fadeSlideUp 0.45s ease-out both;

  /* Hover lift */
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.card-task:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.13) !important;
}

.border-bpdocument {
  border-left: 5px solid #fe7411 !important;
}

.border-assignment {
  border-left: 5px solid #065695 !important;
}

.border-meeting {
  border-left: 5px solid #dc3545 !important;
}

.text-ellipsis {
  white-space: pre-wrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  line-clamp: 1;
  -webkit-box-orient: vertical;
  padding: 0px !important;
}

:deep(.v-card--variant-elevated) {
  box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.12) !important;
}

/* Entrance keyframe — uses `translate` (separate property) so hover transform: is never blocked */
@keyframes fadeSlideUp {
  from {
    opacity: 0;
    translate: 0 20px;
  }
  to {
    opacity: 1;
    translate: 0 0;
  }
}

/* See More button pulse */
.btn-see-all {
  animation: btnPulse 2.4s ease-in-out infinite;
}

@keyframes btnPulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}

/* ── Skeleton shimmer ─────────────────────────────── */
.skeleton-card {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 25px;
  overflow: hidden;
  margin-bottom: 10px;
  height: 64px;
  box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.1);

  /* staggered fade-in so skeleton itself appears smoothly */
  animation: fadeSlideUp 0.35s ease-out both;
}

.skeleton-accent {
  width: 5px;
  align-self: stretch;
  border-radius: 25px 0 0 25px;
  background: linear-gradient(180deg, #c8d8e8 0%, #d8e8f2 100%);
  flex-shrink: 0;
}

.skeleton-body {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 20px;
}

/* Each block is a shimmer pill */
.skeleton-title,
.skeleton-status,
.skeleton-btn {
  border-radius: 8px;
  position: relative;
  overflow: hidden;
  background: #eeeeee;
}

.skeleton-title {
  flex: 1;
  height: 14px;
}
.skeleton-status {
  width: 80px;
  height: 14px;
}
.skeleton-btn {
  width: 90px;
  height: 32px;
  border-radius: 20px;
}

/* Sweep animation on each block */
.skeleton-title::after,
.skeleton-status::after,
.skeleton-btn::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.65) 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: shimmerSweep 1.4s ease-in-out infinite;
}

/* Stagger the sweep per sibling so it feels organic */
.skeleton-status::after {
  animation-delay: 0.15s;
}
.skeleton-btn::after {
  animation-delay: 0.3s;
}

@keyframes shimmerSweep {
  from {
    background-position: -200% 0;
  }
  to {
    background-position: 200% 0;
  }
}

@media (max-width: 768px) {
  .card-task :deep(.v-btn) {
    font-size: 11px !important;
    padding: 0 10px !important;
    min-height: 28px !important;
    height: 28px !important;
  }
}

@media (max-width: 480px) {
  .card-task :deep(.v-btn) {
    font-size: 10px !important;
    padding: 0 8px !important;
    min-height: 24px !important;
    height: 24px !important;
  }
}
</style>
