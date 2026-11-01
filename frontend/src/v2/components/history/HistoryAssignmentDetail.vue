<template>
  <template v-if="isLoading">
    <paragraph-shimmer :is-loading="true" :lines="4" :random-size="true" />
  </template>
  <v-row v-else>
    <v-col lg="6" md="5">
      <div class="label-title text-13">Workspace Type</div>
      <div class="label-subtitle text-13 pb-4">
        {{ item?.workspaceTypeName != "" ? item?.workspaceTypeName : "-" }}
      </div>
      <div class="label-title text-13">Workspace Name</div>
      <div class="label-subtitle text-13 pb-4">
        {{ item?.workspaceName != "" ? item?.workspaceName : "-" }}
      </div>
      <div class="label-title text-13">Task Name</div>
      <div class="label-subtitle text-13 pb-4">
        {{ item?.taskName != "" ? item?.taskName : "-" }}
      </div>
      <div class="label-title text-13">Tanggal Pelaksanaan</div>
      <div class="label-subtitle text-13 pb-4">
        {{
          item?.workDate != null ? formatTimeEngToMonthInd(item?.workDate) : "-"
        }}
      </div>
      <div class="label-title text-13">Topik Penugasan</div>
      <div class="label-subtitle text-13 pb-4">
        {{ item?.assignmentName != "" ? item?.assignmentName : "-" }}
      </div>
      <div class="label-title text-13">Isi Penugasan</div>
      <div class="label-subtitle text-13 pb-4">
        {{ item?.description != "" ? item?.description : "-" }}
      </div>
      <div class="label-title text-13">Tipe Penugasan</div>
      <div class="label-subtitle text-13 pb-4">
        {{ item?.tipePenugasan != "" ? item?.tipePenugasan : "-" }}
      </div>
    </v-col>
    <v-col lg="4" md="5">
      <div class="label-title text-13">Satker Koordinator</div>
      <div class="label-subtitle text-13 pb-4">
        {{
          item?.listSatkerKoordinator != "" ? item?.listSatkerKoordinator : "-"
        }}
      </div>
      <div class="label-title text-13">Satker Pendukung</div>
      <div class="label-subtitle text-13 pb-4">
        {{ item?.listSatkerPendukung != "" ? item?.listSatkerPendukung : "-" }}
      </div>
      <div class="label-title text-13">Ditugaskan Kepada</div>
      <div class="label-subtitle text-13 pb-4">
        {{
          item?.listDitugaskanKepada != "" ? item?.listDitugaskanKepada : "-"
        }}
      </div>
      <div class="label-title text-13">ADG Bidang yang Membawahi</div>
      <div class="label-subtitle text-13 pb-4">
        {{ item?.listADGBidang != "" ? item?.listADGBidang : "-" }}
      </div>
      <div class="label-title text-13">Batas Waktu</div>
      <div class="label-subtitle text-13 pb-4">
        {{
          item?.dueDate != null ? formatTimeEngToMonthInd(item?.dueDate) : "-"
        }}
      </div>
      <div class="label-title text-13">Periode Reminder</div>
      <div class="label-subtitle text-13 pb-4">
        {{ item?.reminderPeriod != null ? item?.reminderPeriod : "-" }}
      </div>
      <div class="label-title text-13">Created By</div>
      <div class="label-subtitle text-13 pb-4">
        {{
          item?.createdDate
            ? formatTimeEngToMonthandTimeInd(item?.createdDate)
            : "-"
        }}
        ;
        {{ item?.name ? setName(item?.name) : "-" }}
      </div>
    </v-col>
    <v-col lg="2" md="2" align="left" style="margin-left: -45px">
      <template v-if="item?.listApproval && item?.listApproval.length">
        <template v-for="(row, idx) in item.listApproval" :key="idx">
          <v-btn
            :color="getColorBtn(row.label)"
            density="comfortable"
            width="auto"
            height="auto"
            variant="outlined"
            class="btn-outline-rounded pa-1 pl-2 pr-2"
            @click="action(row)"
          >
            {{ row.label }}
          </v-btn>
        </template>
      </template>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import {
  formatTimeEngToMonthInd,
  formatTimeEngToMonthandTimeInd,
} from "@/helpers/date";

import { ListApproval } from "@v2/Type";
import ActionApproval from "@/v2/enum/ActionApproval";

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const router = useRouter();
const store = useStore();
const isLoading = ref<boolean>(false);
const item = ref<any>();

function getList() {
  isLoading.value = true;
  const payload = {
    id: props.id,
    source: "History-Assignment",
  };

  store
    .dispatch("historyStore/getDetailAssignmentById", payload)
    .then((result) => {
      item.value = result.responseData;
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function getColorBtn(label: string) {
  const color = {
    "go to penugasan": "#1976d3",
    "view assignment": "#1976d2",
    "go to workspace": "#1976d3",
    edit: "success",
    delete: "red",
    close: "red",
  };
  return color[label.toLowerCase()] ?? "success";
}

function setName(name: any) {
  let createdByName = name;
  let splitName = createdByName?.toLowerCase().split(" ");
  for (var i = 0; i < splitName.length; i++) {
    splitName[i] =
      splitName[i].charAt(0).toUpperCase() + splitName[i].substring(1);
  }
  return splitName.join(" ") ?? "-";
}

function action(row: ListApproval) {
  row.idPenugasan = item.value?.id;
  let label = row.label.toLowerCase();

  // go to assignment
  if (label == ActionApproval.viewAssignment) {
    router.push({
      name: "assignment-detail",
      params: {
        id: item.value?.id,
      },
    });
  }
}

onMounted(() => {
  getList();
});
</script>

<style scoped>
.text-danger {
  background: -webkit-linear-gradient(90.85deg, #d6212a 15.38%, #ff000d 81.89%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-waring {
  background: -webkit-linear-gradient(90.05deg, #c45b10 0.05%, #fe7411 99.96%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-success {
  background: -webkit-linear-gradient(180deg, #00783e 0%, #02aa59 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.text-gradient-blue {
  background: -webkit-linear-gradient(#065695, #267dc2);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 900;
  font-size: 15px;
}

.btn-outline-rounded {
  border-radius: 10px;
  letter-spacing: -0.5px;
}
.dotted {
  border: 2px dashed #065695;
  border-style: none none dashed;
  color: #fff;
  background-color: #fff;
}
:deep(.tab-header.v-slide-group-item--active) {
  color: #065695;
  background: transparent;
  border: 0px;
  border-radius: 0px;
  border-bottom: 1.2px solid;
}
.col-button {
  text-align: right;
  padding-right: 35px;
}
.label-title {
  font-weight: 500;
  color: #a6abc7;
}
.label-subtitle {
  font-weight: 400;
  color: #4b4b4b;
}
</style>
