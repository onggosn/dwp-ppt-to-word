<template>
  <template v-if="isLoading">
    <paragraph-shimmer :is-loading="true" :lines="4" :random-size="true" />
  </template>
  <v-row v-else class="mx-2">
    <v-col cols="9" class="mt-2">
      <v-row>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Workspace Type</div>
          <div class="text-black-theme text-13">
            {{ item.workspaceTypeName ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Satker Koordinator</div>
          <div class="text-black-theme text-13">
            {{ item.listSatkerKoordinator ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Workspace Name</div>
          <div class="text-black-theme text-13">
            {{ item.workspaceName ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Satker Pendukung</div>
          <div class="text-black-theme text-13">
            {{ item.listSatkerPendukung ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Task Name</div>
          <div class="text-black-theme text-13">
            {{ item.taskName ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Ditugaskan Kepada</div>
          <div class="text-black-theme text-13">
            {{ item.listDitugaskanKepada ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Tanggal Pelaksanaan</div>
          <div class="text-black-theme text-13">
            {{
              item.workDate != null
                ? formatTimeEngToMonthInd(item.workDate)
                : "-"
            }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">ADG yang Membawahi</div>
          <div class="text-black-theme text-13">
            {{ item.listADGBidang ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Nama Penugasan</div>
          <div class="text-black-theme text-13">
            {{ item.assignmentName ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Batas Waktu</div>
          <div class="text-black-theme text-13">
            {{ "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Deskripsi Penugasan</div>
          <div class="text-black-theme text-13">
            {{ item.description ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Periode Reminder</div>
          <div class="text-black-theme text-13">
            {{ "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Tipe Penugasan</div>
          <div class="text-black-theme text-13">
            {{ item.tipePenugasan ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Created By</div>
          <div class="text-black-theme text-13">
            {{
              item.createdDate != ""
                ? formatTimeEngToMonthandTimeInd(item.createdDate)
                : "-"
            }}
            ;
            {{ item.name != "" ? setName(item.name) : "-" }}
          </div>
        </v-col>
      </v-row>
    </v-col>
    <v-col cols="3" class="mt-2 text-right">
      <template v-if="item.listApproval && item.listApproval.length">
        <div v-for="(row, idx) in item.listApproval" :key="idx">
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
        </div>
      </template>
    </v-col>
    <edit-access-assignment-dialog
      ref="modal_edit_assignment_member"
      @closeModal="getArahan"
    />
  </v-row>
</template>

<script>
import client from "@/library/ApiClient";
import EditAccessAssignmentDialog from "../assignment/EditAccessAssignmentDialog.vue";
import {
  formatTimeEngToMonthInd,
  formatTimeEngToMonthandTimeInd,
} from "@/helpers/date";

export default {
  name: "dashDetArahanComponent",
  props: {
    idAssignment: {
      type: String,
      default: null,
      required: true,
    },
  },
  components: { EditAccessAssignmentDialog },
  data() {
    return {
      isLoading: false,
      item: {},
    };
  },
  methods: {
    formatTimeEngToMonthInd: formatTimeEngToMonthInd,
    formatTimeEngToMonthandTimeInd: formatTimeEngToMonthandTimeInd,
    getArahan() {
      this.isLoading = true;
      client
        .getAssignmentDetail({
          store: this.$store,
          data: {
            id: this.idAssignment,
            source: "dashboard-assignment",
          },
        })
        .then((result) => {
          // debugger;
          let plainData = result.plainData.responseData;
          // plainData.listApproval = [{ label: "View Assignment" }];
          this.item = plainData;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getColorBtn(label) {
      label = label.toLowerCase();
      const color = {
        "view assignment": "#1976d2",
      };
      return color[label] ?? "success";
    },
    setName() {
      let createdByName = this.item.name;
      let splitName = createdByName.toLowerCase().split(" ");
      for (var i = 0; i < splitName.length; i++) {
        splitName[i] =
          splitName[i].charAt(0).toUpperCase() + splitName[i].substring(1);
      }
      return splitName.join(" ") ?? "-";
    },
    action(row) {
      let label = row.label.toLowerCase();
      // go to assignment
      if (label == "view assignment") {
        this.$router.push({
          name: "assignment-detail",
          params: {
            id: this.item.id,
          },
        });
      } else if (label == "edit access") {
        this.$refs.modal_edit_assignment_member.show(this.item.id);
      }
    },
  },
  created() {
    this.getArahan();
  },
};
</script>

<style scoped>
.text-danger {
  background: -webkit-linear-gradient(90.85deg, #d6212a 15.38%, #ff000d 81.89%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-waring {
  background: -webkit-linear-gradient(90.05deg, #c45b10 0.05%, #fe7411 99.96%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-success {
  background: -webkit-linear-gradient(180deg, #00783e 0%, #02aa59 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-grey-theme {
  color: #a6abc7;
}
.text-black-theme {
  color: #4b4b4b;
}

.text-gradient-blue {
  background: -webkit-linear-gradient(#065695, #267dc2);
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
</style>
