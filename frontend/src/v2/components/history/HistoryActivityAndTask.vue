<template>
  <div class="activity-task-list my-5 mx-2">
    <!-- Loading Shimmer -->
    <div v-if="loading" class="mb-6">
      <div v-for="n in 3" :key="n" class="shimmer-item mb-4">
        <div class="shimmer-content">
          <v-row>
            <v-col cols="8">
              <div class="shimmer-text-long shimmer"></div>
            </v-col>
            <v-col cols="4">
              <div class="shimmer-chip shimmer"></div>
            </v-col>
          </v-row>
        </div>
      </div>
    </div>

    <!-- Actual Content -->
    <v-expansion-panels
      v-else
      class="mb-6 panel-expansion"
      v-model="panel"
      multiple
    >
      <v-expansion-panel v-for="item in items" :key="item.taskID">
        <v-expansion-panel-title>
          <v-row>
            <v-col cols="6" class="item-label d-flex align-center">
              {{ item.taskName }}
            </v-col>
            <v-col cols="3" class="item-information">
              <v-chip :color="getActivityTaskLabelColor(item.activityName)">
                {{ item.activityName || "-" }}
              </v-chip>
            </v-col>

            <v-col cols="3" class="item-information">
              <v-chip
                :style="getColorChipStyle(item.status)"
                class="uniform-chip"
              >
                {{ item.status || "-" }}
              </v-chip>
            </v-col>
          </v-row>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <div>
            <v-divider></v-divider>

            <div class="info my-4">
              <v-row>
                <v-col cols="6">
                  <div class="item-content-label">Description</div>
                  <div class="item-content-information mt-2">
                    {{ item.description || "-" }}
                  </div>
                </v-col>
                <v-col cols="6">
                  <div class="item-content-label">Destination Statement</div>
                  <div class="item-content-information mt-2">
                    {{ item.destinationStatement || "-" }}
                  </div>
                </v-col>

                <v-col cols="6">
                  <div class="item-content-label">PS</div>
                  <div class="item-content-information mt-2">
                    {{ item.ps || "-" }}
                  </div>
                </v-col>

                <v-col cols="6">
                  <div class="item-content-label">Satker Penyaji</div>
                  <div class="item-content-information mt-2">
                    {{ item.satkerPenyaji || "-" }}
                  </div>
                </v-col>

                <v-col cols="6">
                  <div class="item-content-label">Task Type</div>
                  <div class="item-content-information mt-2">
                    {{ item.taskType || "-" }}
                  </div>
                </v-col>

                <v-col cols="6">
                  <div class="item-content-label">Satker Diundang</div>
                  <div class="item-content-information mt-2">
                    {{ item.satkerDiundang || "-" }}
                  </div>
                </v-col>

                <v-col cols="6">
                  <div class="item-content-label">Periode</div>
                  <div class="item-content-information mt-2">
                    {{ item.periode || "-" }}
                  </div>
                </v-col>

                <v-col cols="6">
                  <div class="item-content-label">ADG Bidang</div>
                  <div class="item-content-information mt-2">
                    {{ item.adgBidang || "-" }}
                  </div>
                </v-col>

                <v-col cols="6">
                  <div class="item-content-label">Tanggal Pelaksanaan</div>
                  <div class="item-content-information mt-2">
                    {{ item.tanggalPelaksana || "-" }}
                  </div>
                </v-col>

                <v-col cols="6">
                  <div class="item-content-label">PIC</div>
                  <div class="item-content-information mt-2">
                    <template v-if="item.pic">
                      <template v-if="getPicText(item.pic).length > 100">
                        <span v-if="!item.showFullPic">
                          {{ getPicText(item.pic).substring(0, 100) }}...
                          <v-btn
                            variant="text"
                            size="small"
                            color="blue"
                            @click="toggleShowMore(item, 'pic')"
                            class="ml-1 pa-0 see-more-btn"
                          >
                            See more >>
                          </v-btn>
                        </span>
                        <span v-else>
                          {{ getPicText(item.pic) }}
                          <v-btn
                            variant="text"
                            size="small"
                            color="blue"
                            @click="toggleShowMore(item, 'pic')"
                            class="ml-1 pa-0 see-more-btn"
                          >
                            See less
                          </v-btn>
                        </span>
                      </template>
                      <span v-else>{{ getPicText(item.pic) }}</span>
                    </template>
                    <span v-else>-</span>
                  </div>
                </v-col>

                <v-col cols="6">
                  <div class="item-content-label">Waktu Pelaksanaan</div>
                  <div class="item-content-information mt-2">
                    {{ item.waktuPelaksana || "-" }}
                  </div>
                </v-col>

                <v-col cols="6">
                  <div class="item-content-label">Kontributor</div>
                  <div class="item-content-information mt-2">
                    <template v-if="item.kontributor">
                      <template
                        v-if="getKontributorText(item.kontributor).length > 100"
                      >
                        <span v-if="!item.showFullKontributor">
                          {{
                            getKontributorText(item.kontributor).substring(
                              0,
                              100
                            )
                          }}...
                          <v-btn
                            variant="text"
                            size="small"
                            color="blue"
                            @click="toggleShowMore(item, 'kontributor')"
                            class="ml-1 pa-0 see-more-btn"
                          >
                            See more >>
                          </v-btn>
                        </span>
                        <span v-else>
                          {{ getKontributorText(item.kontributor) }}
                          <v-btn
                            variant="text"
                            size="small"
                            color="blue"
                            @click="toggleShowMore(item, 'kontributor')"
                            class="ml-1 pa-0 see-more-btn"
                          >
                            See less
                          </v-btn>
                        </span>
                      </template>
                      <span v-else>{{
                        getKontributorText(item.kontributor)
                      }}</span>
                    </template>
                    <span v-else>-</span>
                  </div>
                </v-col>

                <v-col cols="6">
                  <div class="item-content-label">
                    Durasi Waktu Pembahasan (dalam menit)
                  </div>
                  <div class="item-content-information mt-2">
                    {{ item.durasi || "-" }}
                  </div>
                </v-col>

                <v-col cols="6">
                  <div class="item-content-label">Participant</div>
                  <div class="item-content-information mt-2">
                    <template v-if="item.participant">
                      <template
                        v-if="getParticipantText(item.participant).length > 100"
                      >
                        <span v-if="!item.showFullParticipant">
                          {{
                            getParticipantText(item.participant).substring(
                              0,
                              100
                            )
                          }}...
                          <v-btn
                            variant="text"
                            size="small"
                            color="blue"
                            @click="toggleShowMore(item, 'participant')"
                            class="ml-1 pa-0 see-more-btn"
                          >
                            See more >>
                          </v-btn>
                        </span>
                        <span v-else>
                          {{ getParticipantText(item.participant) }}
                          <v-btn
                            variant="text"
                            size="small"
                            color="blue"
                            @click="toggleShowMore(item, 'participant')"
                            class="ml-1 pa-0 see-more-btn"
                          >
                            See less
                          </v-btn>
                        </span>
                      </template>
                      <span v-else>{{
                        getParticipantText(item.participant)
                      }}</span>
                    </template>
                    <span v-else>-</span>
                  </div>
                </v-col>
              </v-row>
            </div>
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <!-- Empty State -->
    <div
      v-if="!loading && items.length === 0"
      class="empty-state text-center py-8"
    >
      <v-icon
        icon="mdi-clipboard-text-off"
        size="64"
        color="grey-lighten-1"
      ></v-icon>
      <div class="empty-text mt-4">No activities or tasks found</div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, defineProps, onMounted } from "vue";
import { useStore } from "vuex";
import {
  getActivityTaskLabelColor,
  getColorChipStyle,
} from "@/v2/helpers/color";

interface ActivityTaskItem {
  taskID: string;
  taskName: string;
  activityName: string;
  status: string;
  description: string;
  ps: any[];
  taskType: string;
  periode: any[];
  tanggalPelaksana: string;
  waktuPelaksana: string;
  durasi: any[];
  destinationStatement: any[];
  satkerPenyaji: any[];
  satkerDiundang: any[];
  adgBidang: any[];
  pic: string[];
  kontributor: string[];
  participant: any[];
  // UI state properties
  showFullPic?: boolean;
  showFullKontributor?: boolean;
  showFullDescription?: boolean;
  showFullParticipant?: boolean;
}

const panel = ref<number[]>([]);

const props = defineProps<{ id: string }>();
const store = useStore();

const loading = ref(true);
const items = ref<ActivityTaskItem[]>([]);
const payload = { idWorkspace: props.id };

onMounted(() => {
  fetchTaskList();
});

const fetchTaskList = () => {
  store
    .dispatch("historyStore/getHistoryActivityTaskList", payload)
    .then((res) => {
      if (res.responseCode == "011000") {
        items.value = res.responseData;
      }
      loading.value = false;
    })
    .catch(() => {
      loading.value = false;
    });
};

const toggleShowMore = (item: ActivityTaskItem, field: string) => {
  switch (field) {
    case "pic":
      item.showFullPic = !item.showFullPic;
      break;
    case "kontributor":
      item.showFullKontributor = !item.showFullKontributor;
      break;
    case "description":
      item.showFullDescription = !item.showFullDescription;
      break;
    case "participant":
      item.showFullParticipant = !item.showFullParticipant;
      break;
  }
};

const getPicText = (pic: string[] | string | any): string => {
  if (!pic) return "-";
  if (Array.isArray(pic)) {
    return pic.join(", ");
  }
  return String(pic);
};

const getKontributorText = (kontributor: string[] | string | any): string => {
  if (!kontributor) return "-";
  if (Array.isArray(kontributor)) {
    return kontributor.join(", ");
  }
  return String(kontributor);
};

const getParticipantText = (participant: string[] | string | any): string => {
  if (!participant) return "-";
  if (Array.isArray(participant)) {
    return participant.join(", ");
  }
  return String(participant);
};
</script>

<style scoped>
/* Uniform chip styling */
.uniform-chip {
  min-width: 100px !important;
  width: 80px !important;
  min-height: 28px !important;
  justify-content: center !important;
  font-size: 0.875rem !important;
  font-weight: 400 !important;
  text-align: center !important;
  padding: 0 11px !important;
}

.line-dashed {
  width: 100%;
  height: 1px;
  border-top: 1.5px dashed #065695;
  background-color: transparent;
}

/* .line {
  width: 100%;
  height: 1px;
  border-top: 1px dashed ;
  background-color: transparent;
} */

.item-content-information {
  color: #4b4b4b;
  font-size: 13px;
  line-height: 19.5px;
}

.item-content-label {
  color: #a6abc7;
  font-size: 13px;
  line-height: 19.5px;
  font-weight: 600;
}

.item-information {
  color: #797979e5;
  font-size: 14px;
  line-height: 19.5px;
}

.item-label {
  color: #4b4b4b;
  font-size: 15px;
  line-height: 19.5px;
  font-weight: 800;
}

.comment-item {
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #065695;
}

.comment-header {
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 600;
  color: #4b4b4b;
  font-size: 13px;
}

.comment-date {
  color: #a6abc7;
  font-size: 12px;
}

.comment-text {
  color: #4b4b4b;
  font-size: 13px;
  line-height: 18px;
}

.empty-state {
  color: #a6abc7;
}

.empty-text {
  font-size: 16px;
  color: #797979e5;
}

.see-more-btn {
  min-width: auto !important;
  height: auto !important;
  font-size: 12px !important;
  text-transform: none !important;
  padding: 0 4px !important;
}

/* Shimmer Loading Styles */
.shimmer-item {
  background: white;
  border-radius: 10px;
  box-shadow: 0px 2px 4px 0px #0000001f;
  padding: 16px;
  min-height: 60px;
}

.shimmer-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.shimmer {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 4px;
}

.shimmer-text-long {
  height: 20px;
  flex: 1;
  max-width: 300px;
}

.shimmer-chip {
  height: 24px;
  width: 60px;
  border-radius: 12px;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* Expansion Panel Styles */
:deep(
    .v-expansion-panel-title--active > .v-expansion-panel-title__overlay,
    .v-expansion-panel-title[aria-haspopup="menu"][aria-expanded="true"]
      > .v-expansion-panel-title__overlay
  ) {
  opacity: 0 !important;
}

:deep(.v-expansion-panel) {
  border-radius: 10px !important;
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

:deep(.v-expansion-panel:hover) {
  transform: translateY(-2px);
  box-shadow: 0px 4px 12px 0px rgba(0, 0, 0, 0.15) !important;
}

:deep(.v-expansion-panel__shadow) {
  box-shadow: 0px 2px 4px 0px #0000001f !important;
}

:deep(.v-expansion-panel-title) {
  min-height: 60px;
}

:deep(.v-expansion-panel-title__icon) {
  border: 1px solid #065695 !important;
  border-radius: 10px !important;
  padding: 4px !important;
  background-color: white !important;
  color: #065695 !important;
}

:deep(.v-expansion-panel .v-expansion-panel--after-active) {
  border-radius: 10px !important;
}

:deep(
    .v-expansion-panels:not(.v-expansion-panels--variant-accordion)
      > :not(:first-child):not(:last-child):not(.v-expansion-panel--active):not(
        .v-expansion-panel--after-active
      )
  ) {
  border-radius: 10px !important;
}

:deep(.v-expansion-panel:not(:first-child)::after) {
  display: none;
}

:deep(
    .v-expansion-panels:not(.v-expansion-panels--variant-accordion)
      > :last-child:not(:first-child):not(.v-expansion-panel--active):not(
        .v-expansion-panel--after-active
      )
  ) {
  border-radius: 10px !important;
}

:deep(
    .v-expansion-panels:not(.v-expansion-panels--variant-accordion)
      > :first-child:not(:last-child):not(.v-expansion-panel--active):not(
        .v-expansion-panel--before-active
      )
  ) {
  border-radius: 10px !important;
}
</style>
