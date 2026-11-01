<template>
  <div class="faq-panel" :style="{ animationDelay: props.delay }">
    <v-expansion-panels v-model="panel">
      <v-expansion-panel :value="item.topicId">
        <v-expansion-panel-title>
          <v-row align="center">
            <v-col cols="6">
              <p class="font-weight-bold ellipsis-1">
                {{ item?.topicName }}
              </p>
            </v-col>
            <v-col cols="6" class="text-right pr-15">
              <span style="font-size: 13px; color: #828282">
                Last modified by: {{ item?.lastModifiedBy }} | Date:
                {{ formatDate(item?.lastModifiedDate) }}
              </span>
            </v-col>
          </v-row>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-row class="mb-1">
            <v-col cols="12" class="d-flex justify-end">
              <btn-delete
                :title="'Delete Section'"
                :description="'&nbsp;'"
                :btn-title="'Delete Section'"
                :subtitle="'Are you sure delete this section FAQ ?'"
                :append-icon="true"
                :btn-color="'#d6212a'"
                :btn-density="'comfortable'"
                :positiveTextButton="'Delete'"
                btn-class="font-weight-bold text-12"
                @update="deleteTopic(item)"
              />
              <!-- <v-btn
                class="px-4"
                style="border-radius: 8px"
                color="#065695"
                variant="outlined"
                size="small"
                prepend-icon="mdi-pencil-outline"
              >
                Edit
              </v-btn> -->
            </v-col>
          </v-row>

          <v-row
            v-if="
              isLoadingQuestions || topicDetail.description || topicDetail.icon
            "
            class="mb-4"
          >
            <v-col cols="6">
              <p class="mb-2 text-gradient-grey" style="font-size: 14px">
                Description
              </p>
              <div v-if="isLoadingQuestions">
                <div
                  class="shimmer mb-2"
                  style="height: 16px; width: 100%; border-radius: 4px"
                ></div>
                <div
                  class="shimmer"
                  style="height: 16px; width: 80%; border-radius: 4px"
                ></div>
              </div>
              <div v-else style="white-space: pre-line" class="text-13">
                {{ topicDetail.description || "-" }}
              </div>
            </v-col>
            <v-col cols="3">
              <p class="mb-2 text-gradient-grey" style="font-size: 14px">
                Icon
              </p>
              <div v-if="isLoadingQuestions">
                <div
                  class="shimmer"
                  style="height: 56px; width: 100%; border-radius: 8px"
                ></div>
              </div>
              <template v-else>
                <div
                  v-if="topicDetail.icon || topicDetail.topicIconLink"
                  class="d-flex align-center pa-3"
                  style="background-color: #f5f5f5; border-radius: 8px"
                >
                  <!-- <v-icon color="#065695" size="32" class="mr-3"
                    >mdi-file-image</v-icon
                  > -->
                  <img
                    :src="
                      topicDetail.topicIconLink ||
                      require(`@/v2/assets/icon/faq_${topicDetail.icon}.svg`)
                    "
                    width="30"
                    height="30"
                    class="d-flex mr-3 align-center justify-center"
                  />
                  <!-- <img
                    :src="
                      require(`@/v2/assets/icon/faq_${topicDetail.icon}.svg`)
                    "
                    width="30px"
                    height="30px"
                    class="d-flex mr-3 align-center justify-center"
                  /> -->
                  <div class="d-flex align-center">
                    <span class="text-13 mr-2">{{ topicDetail.icon }}</span>
                    <span
                      class="text-13"
                      style="color: #065695; cursor: pointer"
                      @click="openPreviewModal"
                      >• Preview</span
                    >
                  </div>
                </div>
                <div v-else class="text-grey text-13">No icon</div>
              </template>
            </v-col>
          </v-row>

          <v-row class="mt-2">
            <v-col cols="12" class="d-flex justify-end">
              <v-btn
                class="px-4"
                style="border-radius: 8px"
                color="#065695"
                variant="outlined"
                size="small"
                prepend-icon="mdi-plus"
                @click="openAddModal"
              >
                Add Question
              </v-btn>
            </v-col>
          </v-row>

          <!-- Nested Expandable Items -->
          <template v-if="isLoadingQuestions">
            <div
              v-for="n in 3"
              :key="n"
              class="shimmer mt-3"
              style="height: 50px; border-radius: 16px; width: 100%"
            ></div>
          </template>

          <template v-else-if="questions?.length">
            <ListFAQQuestion
              v-for="sub in questions"
              :key="sub.questionId"
              :item="sub"
              @edit="openEditModal"
              @refresh="fetchQuestions"
            />
          </template>
          <div
            v-else-if="!isLoadingQuestions"
            class="text-center py-5 text-grey text-13"
          >
            No questions available for this topic.
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <ModalEditAnswer
      v-model="showEditModal"
      :item="selectedAnswerItem"
      @save="handleSaveAnswer"
      @refresh="fetchQuestions"
    />

    <ModalAddQuestion
      v-model="showAddModal"
      :id-topic="String(item.topicId)"
      @save="handleSaveNewQuestion"
      @refresh="fetchQuestions"
    />

    <ModalPreviewIcon
      v-model="showPreviewModal"
      :icon-name="topicDetail.topicIconLink"
      :icon-src="
        topicDetail.topicIconLink
          ? topicDetail.topicIconLink
          : topicDetail.icon
          ? require(`@/v2/assets/icon/faq_${topicDetail.icon}.svg`)
          : ''
      "
      :topic-name="item?.topicName"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, getCurrentInstance } from "vue";
import ModalEditAnswer from "./ModalEditAnswer.vue";
import ModalAddQuestion from "./ModalAddQuestion.vue";
import ModalPreviewIcon from "./ModalPreviewIcon.vue";
import ListFAQQuestion from "./ListFAQQuestion.vue";
import BtnDelete from "@v2/components/utils/dialog/DeleteEventDialog.vue";
import { useStore } from "vuex";

const store = useStore();
const { root } = getCurrentInstance() as any;

const emit = defineEmits(["refreshTopicList"]);

const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
  delay: {
    type: String,
    default: "0s",
  },
});

const panel = ref<number[]>([]);
const questions = ref<any[]>([]);
const topicDetail = ref({ description: "", icon: "", topicIconLink: "" });
const isLoadingQuestions = ref(false);
const isFetched = ref(false);
const showEditModal = ref(false);
const showAddModal = ref(false);
const showPreviewModal = ref(false);
const selectedAnswerItem = ref<any>({ question: "", answer: "" });
function formatDate(date: string) {
  if (!date) return "-";
  const d = new Date(date);
  if (isNaN(d.getTime())) return date;

  return (
    new Intl.DateTimeFormat("en-US", {
      month: "long",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    }).format(d) + " WIB"
  );
}

watch(panel, (newVal) => {
  //   if (newVal.includes(props.item?.topicId as never)) {
  fetchQuestions();
  //   }
});

async function fetchQuestions() {
  isLoadingQuestions.value = true;
  try {
    const res = await store.dispatch("adminStore/getFAQTopicDetail", {
      FAQTopicID: props.item?.topicId,
    });
    questions.value = res.responseData?.questionList || [];
    topicDetail.value = {
      description: res.responseData?.description || "",
      icon: res.responseData?.icon || "",
      topicIconLink: res.responseData?.topicIconLink || "",
    };
  } finally {
    isLoadingQuestions.value = false;
  }
}

const openEditModal = (subItem: any) => {
  selectedAnswerItem.value = {
    questionId: subItem.questionId,
    topicId: props.item?.topicId,
    question: subItem.questionDetail,
    answer: subItem.answer || "",
  };
  showEditModal.value = true;
};

const openAddModal = () => {
  showAddModal.value = true;
};

const openPreviewModal = () => {
  showPreviewModal.value = true;
};

const handleSaveAnswer = () => {
  fetchQuestions();
  emit("refreshTopicList");
};

const handleSaveNewQuestion = () => {
  fetchQuestions();
  emit("refreshTopicList");
};

const deleteTopic = async (item: any) => {
  const payload = { idTopic: item.topicId };
  try {
    const res = await store.dispatch("adminStore/deleteFAQTopic", payload);
    if (res?.responseCode === "011000") {
      root.refs.toast.show({
        message: res.responseMessage || "Successfully Deleted",
        color: "success",
        timeout: 3000,
      });
      emit("refreshTopicList");
      fetchQuestions();
    } else {
      root.refs.toast.show({
        message: res?.responseMessage || "Failed to delete",
        color: "error",
        timeout: 3000,
      });
    }
  } catch {
    root.refs.toast.show({
      message: "Failed to delete",
      color: "error",
      timeout: 3000,
    });
  }
};
</script>

<style scoped>
:deep(
    .v-expansion-panel-title--active > .v-expansion-panel-title__overlay,
    .v-expansion-panel-title[aria-haspopup="menu"][aria-expanded="true"]
      > .v-expansion-panel-title__overlay
  ) {
  opacity: 0 !important;
}
:deep(.v-expansion-panel) {
  border-radius: 16px;
}
:deep(.v-expansion-panel__shadow) {
  box-shadow: 0px 2px 4px 0px #0000001f !important;
}
:deep(.v-expansion-panel-title) {
  min-height: 60px;
}

.shimmer {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* Entrance animation */
.faq-panel {
  animation: fadeSlideUp 0.45s ease-out both;
}

@keyframes fadeSlideUp {
  from {
    opacity: 0;
    translate: 0 14px;
  }
  to {
    opacity: 1;
    translate: 0 0;
  }
}
</style>
