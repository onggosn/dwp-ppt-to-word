<template>
  <v-card class="container">
    <h1 class="txt-header">Analysis</h1>
    <div else style="margin: auto; width: 80%">
      <div style="margin: auto; width: 300px; height: 300px">
        <apexchart
          type="radialBar"
          height="250"
          :options="chartOptions"
          :series="percentage"
        ></apexchart>
      </div>
      <div class="d-flex flex-row container-label-stage-indicator">
        <div
          v-for="(item, idx) in label"
          :key="item"
          class="d-flex flex-row align-center"
          style="column-gap: 8px"
        >
          <div
            class="stage-indicator"
            :style="{ background: color[idx] }"
          ></div>
          <span class="label-stage-indicator">{{ item }}</span>
        </div>
      </div>
    </div>
  </v-card>
</template>

<script setup lang="ts">
import { ref, defineProps, watchEffect } from "vue";

const props = defineProps({
  asesmenRekomendasi: {
    type: Number,
    default: 0,
  },
  persetujuan: {
    type: Number,
    default: 0,
  },
  total: {
    type: Number,
    default: 0,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
});

const label = ref<string[]>(["Asesmen & Rekomendasi", "Persetujuan"]);
const color = ref<string[]>(["#e3b43b", "#21cc44"]);
const percentage = ref<number[]>([]);
let chartOptions = ref({});
watchEffect(() => {
  chartOptions.value = {
    chart: {
      height: 350,
      type: "radialBar",
    },
    plotOptions: {
      radialBar: {
        dataLabels: {
          name: {
            show: true,
            fontSize: "12px",
            colors: undefined,
            offsetY: 18,
            fontFamily: "Poppins",
          },
          value: {
            show: true,
            offsetY: -18,
            color: "#030229",
            fontSize: "24px",
            fontWeight: 800,
            fontFamily: "Poppins",
          },
          total: {
            show: true,
            color: "#030229",
            label: props.isLoading ? "Loading.." : "Complete",
            fontWeight: 400,
            fontSize: "12px",
            formatter: function () {
              return props.total + "%";
            },
            fontFamily: "Poppins",
          },
        },
      },
    },
    colors: color.value,
    labels: label.value,
  };
  percentage.value = [];
  percentage.value.push(props.asesmenRekomendasi);
  percentage.value.push(props.persetujuan);
});
</script>

<style scoped>
.container {
  background: white;
  border-radius: 12px;
  padding: 12px 24px;
}
.txt-header {
  font-family: Poppins;
  font-size: 24px;
  font-weight: 600;
  line-height: 36px;
  text-align: left;
  color: #4b4b4b;
  margin-bottom: 71px;
}
.stage-indicator {
  width: 15px;
  height: 15px;
  gap: 0px;
  border-radius: 5px;
}
.container-label-stage-indicator {
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 60px;
  column-gap: 16px;
}
.label-stage-indicator {
  font-size: 16px;
  font-weight: 500;
  line-height: 21.82px;
  text-align: left;
}
</style>
