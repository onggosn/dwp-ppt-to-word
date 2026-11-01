<template>
  <v-row v-if="isLoading">
    <v-col cols="6" sm="3" v-for="x in 4" :key="x">
      <free-style-shimmer
        :is-loading="true"
        width="100%"
        height="6.5rem"
        border-radius="10px"
      />
    </v-col>
  </v-row>
  <v-row v-else align="center" align-content="center">
    <v-col
      cols="6"
      class="text-center mt-2"
      v-for="(item, idx) in summaryDatas"
      :key="idx"
      :sm="12 / summaryDatas.length"
    >
      <v-row no-gutters>
        <v-col cols="11">
          <h2 class="text-gradient-blue">{{ item.title.toUpperCase() }}</h2>
          <h1 class="my-3 py-3 text-24 text-gradient-red">
            {{ item.value }}
          </h1>
        </v-col>
        <v-col cols="1" v-if="idx < summaryDatas.length - 1">
          <div class="gradient-vertical-line"></div>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { useStore } from "vuex";
import { ref, onMounted, watchEffect } from "vue";

type TSummary = {
  title: string;
  value: string | number;
};

const props = defineProps({
  typeFilter: {
    type: String,
    default: null,
  },
});

const store = useStore();
const isLoading = ref<boolean>(false);
const summaryDatas = ref<TSummary[]>([]);
const defaultSummaryDatas = ref<TSummary[]>([
  {
    title: "Need Approval",
    value: "0",
  },
  {
    title: "In Progress",
    value: "0",
  },
  {
    title: "Done",
    value: "0",
  },
  {
    title: "Not Started",
    value: "0",
  },
]);

function load(type) {
  isLoading.value = true;
  if (type == "penugasan") {
    getSummaryAssignmentPenugasan();
  } else if (type == "arahan") {
    getSummaryAssignmentArahan();
  } else {
    summaryDatas.value = defaultSummaryDatas.value;
    isLoading.value = false;
  }
}

function getSummaryAssignmentPenugasan() {
  store
    .dispatch("assignmentStore/getCounterPenugasanInAssignment")
    .then((result) => {
      summaryDatas.value = result.responseData.data;
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function getSummaryAssignmentArahan() {
  store
    .dispatch("assignmentStore/getCounterArahanInAssignment")
    .then((result) => {
      const allValue = result.responseData?.data?.reduce(
        (n: number, { value }) => n + value,
        0
      );
      summaryDatas.value = [
        {
          title: "Total Arahan ",
          value: allValue,
        },
      ];
    })
    .finally(() => {
      isLoading.value = false;
    });
}

onMounted(() => {
  load(props.typeFilter);
});

watchEffect(() => {
  load(props.typeFilter);
});

defineExpose({
  load,
});
</script>

<style scoped>
.gradient-vertical-line {
  background: linear-gradient(
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
  width: 1px;
  height: 60px;
}

.text-gradient-blue {
  background: -webkit-linear-gradient(#065695, #267dc2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 900;
  font-size: large;
}

.text-gradient-red {
  background: -webkit-linear-gradient(90.85deg, #d6212a 15.38%, #ff000d 81.89%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 900;
  font-size: x-large;
}
</style>
