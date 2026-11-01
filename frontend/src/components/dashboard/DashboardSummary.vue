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
      :sm="12 / this.summaryDatas.length"
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

<script>
import client from "@/library/ApiClient";

export default {
  name: "dashboardSummaryComponent",
  props: {
    typeFilter: {
      type: String,
      default: null,
    },
    subFilter: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      isLoading: false,
      summaryDatas: [],
      defaultSummaryDatas: [
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
      ],
    };
  },
  methods: {
    loadData(type) {
      this.isLoading = true;
      if (type == "dashboard.workspace") {
        this.getSummaryWorkspace();
      } else if (type == "dashboard.task") {
        this.getSummaryTask();
      } else if (type == "dashboard.persetujuan") {
        if (this.subFilter == "task") {
          this.getSummaryPersetujuanTask();
        } else {
          this.getSummaryPersetujuanWorkspace();
        }
      } else if (type == "dashboard.pengajuan") {
        if (this.subFilter == "task") {
          this.getSummaryPengajuanTask();
        } else {
          this.getSummaryPengajuanWorkspace();
        }
      } else if (type == "dashboard.document") {
        if (this.subFilter == "materi") {
          this.getSummaryDocumentSupport();
        } else {
          this.getSummaryDocument();
        }
      } else if (type == "dashboard.assignment") {
        if (this.subFilter == "penugasan") {
          this.getSummaryAssignmentPenugasan();
        } else {
          this.getSummaryAssignmentArahan();
        }
      } else {
        this.summaryDatas = this.defaultSummaryDatas;
        this.isLoading = false;
      }
    },
    getSummaryWorkspace() {
      client
        .getWorkspaceStatusByUsername({
          store: this.$store,
          data: { username: this.$store.state.username },
        })
        .then((result) => {
          this.summaryDatas = result.plainData.responseData.data;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getSummaryTask() {
      client
        .getTaskStatusByUsername({
          store: this.$store,
          data: { username: this.$store.state.username },
        })
        .then((result) => {
          this.summaryDatas = result.plainData.responseData.data;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getSummaryPersetujuanWorkspace() {
      client
        .getWorkspaceStatusByUsernameApproval({
          store: this.$store,
          data: { username: this.$store.state.username },
        })
        .then((result) => {
          this.summaryDatas = result.plainData.responseData.data;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getSummaryPersetujuanTask() {
      client
        .getTaskStatusByUsernameApproval({
          store: this.$store,
          data: { username: this.$store.state.username },
        })
        .then((result) => {
          this.summaryDatas = result.plainData.responseData.data;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getSummaryPengajuanWorkspace() {
      client
        .getWorkspaceStatusByUsernameSubmission({
          store: this.$store,
          data: { username: this.$store.state.username },
        })
        .then((result) => {
          this.summaryDatas = result.plainData.responseData.data;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getSummaryPengajuanTask() {
      client
        .getTaskStatusByUsernameSubmission({
          store: this.$store,
          data: { username: this.$store.state.username },
        })
        .then((result) => {
          this.summaryDatas = result.plainData.responseData.data;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getSummaryDocument() {
      client
        .getTaskDocumentCounterByUsername({
          store: this.$store,
          data: { username: this.$store.state.username },
        })
        .then((result) => {
          this.summaryDatas = result.plainData.responseData.data;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getSummaryDocumentSupport() {
      client
        .getTaskDocumentSupportCounterByUsername({
          store: this.$store,
          data: { username: this.$store.state.username },
        })
        .then((result) => {
          this.summaryDatas = result.plainData.responseData.data;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getSummaryAssignmentPenugasan() {
      client
        .getListCounterAssignmentbyTipePenugasan({
          store: this.$store,
          data: { username: this.$store.state.username },
        })
        .then((result) => {
          this.summaryDatas = result.plainData.responseData.data;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getSummaryAssignmentArahan() {
      client
        .getListCounterAssignmentbyTipeArahan({
          store: this.$store,
          data: { username: this.$store.state.username },
        })
        .then((result) => {
          this.summaryDatas = result.plainData.responseData.data;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
  },
  created() {
    this.loadData(this.typeFilter);
  },
  watch: {
    typeFilter(value) {
      this.loadData(value);
    },
    subFilter() {
      this.loadData(this.typeFilter);
    },
  },
};
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
