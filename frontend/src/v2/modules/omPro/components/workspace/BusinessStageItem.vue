<template>
  <div
    class="d-flex flex-row align-center"
    style="cursor: pointer"
    @click="showDetail"
  >
    <div class="d-flex">
      <free-style-shimmer
        v-if="isLoading"
        height="43px"
        width="43px"
        border-radius="5px"
        color="#DCDCDC"
      />
      <img
        v-else
        :src="require('@/v2/assets/workspace/bp.svg')"
        width="43"
        height="43"
      />
    </div>
    <div style="flex-grow: 1; margin-left: 22px">
      <paragraph-shimmer
        v-if="isLoading"
        style="width: 80px"
        :lines="1"
        :random-size="false"
      />
      <h2 v-else class="txt-title">{{ item.bp }}</h2>
      <paragraph-shimmer
        v-if="isLoading"
        style="width: 100%"
        :lines="1"
        :random-size="false"
      />
      <v-progress-linear
        v-else
        :model-value="percentage"
        :v-model="percentage"
        :color="getBusinessStageProgressColor(stage)"
        height="10"
        rounded
      ></v-progress-linear>
    </div>
    <div v-if="!isLoading" class="d-flex flex-column" style="margin-left: 16px">
      <h3 class="txt-percentage">{{ percentage }}%</h3>
      <div
        class="chip-status"
        :style="{
          background: getEventStatusColor(item.bpStatus)?.background,
          color: getEventStatusColor(item.bpStatus)?.color,
        }"
      >
        {{ item.bpStatus }}
      </div>
    </div>
    <div v-if="props.item.isAllowNext" style="margin-left: 10px">
      <img :src="require('@/v2/assets/icon/keyboard-arrow-left.svg')" />
    </div>
    <div v-else style="margin-left: 10px">
      <img :src="require('@/v2/assets/icon/keyboard-arrow-left-copy.svg')" />
    </div>
  </div>
  <modal-warning ref="modal" :modal-config="modalConfig" />
</template>

<script setup lang="ts">
import { defineProps, PropType, ref, computed } from "vue";
// import { useRoute, useRouter } from "vue-router";
import {
  getEventStatusColor,
  getBusinessStageProgressColor,
} from "@/v2/helpers/color";
import { TDetailRDGItem, TModalWarning } from "@/v2/Type";
import ModalWarning from "@/v2/components/utils/modal/ModalWarning.vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
// import { useStore } from "vuex";

const props = defineProps({
  stage: {
    type: String,
    default: "",
  },
  item: {
    type: Object as PropType<TDetailRDGItem>,
    required: true,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
});

const store = useStore();
const modal = ref();

const modalConfig = ref<TModalWarning>({
  img: {
    location: "workspace/access-denied.svg",
    width: "395px",
    height: "311px",
  },
  title: "Access Denied",
  description:
    "You can't open this document. Speak to your administrator to open this document.",
  btnBackgroundStyle: "linear-gradient(to right, #065695, #267DC2)",
  textBtn: "Close",
  textWeight: 400,
  textStyle: "normal",
});
const progress = computed(
  () => store.getters["contentStore/getDocumentProgress"]
);

const route = useRoute();
const router = useRouter();

const percentage = computed((): number => props.item.bpValue ?? 0);
const idEvent = computed(() => route.params.idEvent as string);

function showDetail() {
  if (props.item.isAllowNext) {
    if (progress.value)
      router.push({
        name: "om.rdg-collaboration-all",
        params: {
          idEvent: idEvent.value,
        },
        hash: `#${props.item.idBpDocument}`,
      });
    else
      router.push({
        name: "om.rdg-collaboration",
        params: {
          idEvent: idEvent.value,
          idDoc: props.item.idBpDocument as string,
        },
      });
  } else {
    modal.value.show();
  }
}
</script>

<style scoped>
.txt-title {
  margin-bottom: 8px;
  color: #000;
  font-size: 14px;
  font-weight: 600;
  line-height: 18px;
  text-align: left;
}
.txt-percentage {
  color: #000;
  opacity: 70%;
  font-size: 14px;
  font-weight: 700;
  line-height: 18px;
  text-align: center;
}
.txt-status {
  font-size: 11px;
  font-weight: 600;
  line-height: 11px;
  text-align: left;
  color: #5b5d5f;
}
.chip-status {
  margin-top: 4px;
  width: 90px;
  padding: 6px 0;
  border-radius: 16px;
  text-align: center;
  font-weight: 600;
  font-size: 11px;
}
</style>
