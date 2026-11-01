<template>
  <div>
    <div class="d-block font-weight-bold mb-2 mt-1 text-blueTheme">
      Document Progress
    </div>
    <v-timeline
      side="end"
      align="start"
      truncate-line="both"
      line-color="#045695"
      style="margin-left: -20px"
      class="mb-10"
    >
      <template v-for="item in listFlow" :key="item.id">
        <v-timeline-item
          v-if="item.status == 0 && !item.approvalDate"
          dot-color="grey"
          icon="mdi-record"
          icon-color="white"
          size="small"
          line-inset="1"
        >
          <div class="d-flex">
            <p
              class="me-4 text-13 font-weight-medium text-capitalize"
              style="color: grey"
            >
              {{ item.mDocumentApprovalName }}
            </p>
          </div>
          <div class="d-flex mt-1">
            <p class="me-4 text-11 text-capitalize" style="white-space: nowrap">
              <v-icon color="grey">mdi-account </v-icon>by {{ item.name }}
            </p>
          </div>
          <div class="d-flex"></div>
        </v-timeline-item>
        <v-timeline-item
          v-else-if="item.status == 1"
          dot-color="red"
          icon="mdi-close"
          icon-color="white"
          size="small"
        >
          <div class="d-flex">
            <strong class="me-4 text-13 text-capitalize" style="color: red">{{
              item.mDocumentSupportApprovalName
            }}</strong>
          </div>
          <div class="d-flex mt-1">
            <p class="me-4 text-11 text-capitalize" style="white-space: nowrap">
              <v-icon color="grey">mdi-account </v-icon>by {{ item.name }}
            </p>
          </div>
          <div class="d-flex">
            <p class="me-4 text-11">
              <v-icon color="grey">mdi-clock </v-icon
              >{{ reformatDateCard(item.approvalDate) }} -
              {{ reformatTime(item.approvalDate) }}
            </p>
          </div>
        </v-timeline-item>
        <v-timeline-item
          v-else
          dot-color="#045695"
          icon="mdi-check"
          icon-color="white"
          size="small"
        >
          <div class="d-flex">
            <strong
              class="me-4 text-13 text-capitalize"
              style="color: #045695"
              >{{ item.mDocumentSupportApprovalName }}</strong
            >
          </div>
          <div class="d-flex mt-1">
            <p class="me-4 text-11 text-capitalize" style="white-space: nowrap">
              <v-icon color="grey">mdi-account </v-icon>by {{ item.name }}
            </p>
          </div>
          <div class="d-flex">
            <p class="me-4 text-11">
              <v-icon color="grey">mdi-clock </v-icon
              >{{ reformatDateCard(item.approvalDate) }} -
              {{ reformatTime(item.approvalDate) }}
            </p>
          </div>
        </v-timeline-item>
      </template>
    </v-timeline>
  </div>
</template>
<script setup lang="ts">
import { defineProps } from "vue";
import { reformatDateCard, reformatTime } from "@/library/DateHelper";

defineProps({
  listFlow: Object,
});
</script>

<!-- <template>
  <api-loader :apiMethod="getDocumentDetail" @loadingEnded="handleLoadingEnded">
    <template v-slot:default="props">
      <v-timeline
        side="end"
        align="start"
        truncate-line="both"
        line-color="#045695"
        style="margin-left: -20px"
        class="mb-10"
      >
        <template
          v-for="item in props.response.plainData.trackingDocument"
          :key="item.id"
        >
          <v-timeline-item
            v-if="item.status == 0 && !item.approvalDate"
            dot-color="grey"
            icon="mdi-record"
            icon-color="white"
            size="small"
            line-inset="1"
          >
            <div class="d-flex">
              <p
                class="me-4 text-13 font-weight-medium text-capitalize"
                style="color: grey"
              >
                {{ item.mDocumentApprovalName }}
              </p>
            </div>
            <div class="d-flex mt-1">
              <p
                class="me-4 text-11 text-capitalize"
                style="white-space: nowrap"
              >
                <v-icon color="grey">mdi-account </v-icon>by {{ item.name }}
              </p>
            </div>
            <div class="d-flex"></div>
          </v-timeline-item>
          <v-timeline-item
            v-else-if="item.status == 1"
            dot-color="red"
            icon="mdi-close"
            icon-color="white"
            size="small"
          >
            <div class="d-flex">
              <strong class="me-4 text-13 text-capitalize" style="color: red">{{
                item.mDocumentApprovalName
              }}</strong>
            </div>
            <div class="d-flex mt-1">
              <p
                class="me-4 text-11 text-capitalize"
                style="white-space: nowrap"
              >
                <v-icon color="grey">mdi-account </v-icon>by {{ item.name }}
              </p>
            </div>
            <div class="d-flex">
              <p class="me-4 text-11">
                <v-icon color="grey">mdi-clock </v-icon
                >{{ reformatDateCard(item.approvalDate) }} -
                {{ reformatTime(item.approvalDate) }}
              </p>
            </div>
          </v-timeline-item>
          <v-timeline-item
            v-else
            dot-color="#045695"
            icon="mdi-check"
            icon-color="white"
            size="small"
          >
            <div class="d-flex">
              <strong
                class="me-4 text-13 text-capitalize"
                style="color: #045695"
                >{{ item.mDocumentApprovalName }}</strong
              >
            </div>
            <div class="d-flex mt-1">
              <p
                class="me-4 text-11 text-capitalize"
                style="white-space: nowrap"
              >
                <v-icon color="grey">mdi-account </v-icon>by {{ item.name }}
              </p>
            </div>
            <div class="d-flex">
              <p class="me-4 text-11">
                <v-icon color="grey">mdi-clock </v-icon
                >{{ reformatDateCard(item.approvalDate) }} -
                {{ reformatTime(item.approvalDate) }}
              </p>
            </div>
          </v-timeline-item>
        </template>
      </v-timeline>
    </template>
    <template v-slot:loading>
      <paragraph-shimmer :is-loading="true" :lines="20" :random-size="true" />
    </template>
  </api-loader>
</template>
<script lang="js">
import { defineComponent } from "vue";
import client from "@/library/ApiClient";
import ApiLoader from "@/components/ApiLoader.vue";
import { reformatDateCard, reformatTime } from "@/library/DateHelper";

export default defineComponent({
  name: "DocumentDetail",
  components: {
    ApiLoader,
  },
  props:{},
  data: function () {
    return {
      labelStatus: {
        1: { label: "Not Started" },
        2: { label: "In Progress" },
        3: { label: "Done" },
        14: { label: "Need for Approval" },
        15: { label: "Not Started" },
        16: { label: "In Progress" },
        17: { label: "Done" },
      },
    };
  },
  methods:{
    getDocumentDetail() {
      return client.GetTaskDocumentByIdDocument({
          store: this.$store,
          data: {
            id: this.$route.params.documentId,
          },
        });
    },
    handleLoadingEnded({ success, response }) {
      if(success){
        this.$emit('documentName', response.plainData.documentNameDisplay);
      }
    },
    reformatDateCard(item) {
      return reformatDateCard(item);
    },
    reformatTime(item) {
      return reformatTime(item);
    },
  }
});
</script> -->
