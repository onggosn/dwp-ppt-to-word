<template>
  <div class="container">
    <v-row v-if="isLoading" class="d-flex">
      <v-col cols="6" v-for="n in 6" :key="n">
        <v-card style="border-radius: 12px; height: 185px" class="pl-3">
          <paragraph-shimmer
            v-if="isLoading"
            :is-loading="true"
            :lines="8"
            :random-size="true"
            class="mt-5 mr-5"
          />
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="!isLoading">
      <v-col
        v-if="itemSection?.aiu?.isvisible"
        cols="6"
        :order="itemSection?.aiu?.orderBP ?? '0'"
      >
        <div>
          <div
            @click="handleCardClick(itemSection.aiu)"
            style="cursor: pointer"
          >
            <v-card style="border-radius: 12px; height: 185px" class="pl-3">
              <v-sheet class="d-flex ml-2 mr-4 mt-5">
                <v-sheet class="me-auto">
                  {{ itemSection.aiu?.bp || "Analisis Indikator Utama" }}
                </v-sheet>
                <v-sheet class="ml-9">
                  <img
                    :src="require('@/v2/assets/workspace/aiudashboard.svg')"
                  />
                </v-sheet>
              </v-sheet>
              <v-sheet class="d-flex ml-2 mr-4 mt-8">
                <v-sheet class="persentase me-auto">
                  {{ (itemSection.aiu?.bpValuePercentage || "0") + " % " }}
                </v-sheet>
                <v-sheet class="count ml-9 mt-3"
                  >{{ itemSection.aiu.bpValue1 || "0" }}
                  <span class="approve-of">Approve Of</span>
                  {{ itemSection.aiu.bpValue2 || "0" }}</v-sheet
                >
              </v-sheet>
            </v-card>
          </div>
        </div>
      </v-col>
      <v-col
        v-if="itemSection?.policyNote?.isvisible"
        cols="6"
        :order="itemSection?.policyNote?.orderBP ?? '0'"
      >
        <div>
          <div
            @click="handleCardClick(itemSection.policyNote)"
            style="cursor: pointer"
          >
            <v-card style="border-radius: 12px; height: 185px" class="pl-3">
              <v-sheet class="d-flex ml-2 mr-4 mt-5">
                <v-sheet class="me-auto">
                  {{ itemSection.policyNote?.bp || "Policy Note" }}
                </v-sheet>
                <v-sheet class="ml-9">
                  <img
                    :src="require('@/v2/assets/workspace/pn_dashboard.svg')"
                  />
                </v-sheet>
              </v-sheet>
              <v-sheet class="d-flex ml-2 mr-4 mt-8">
                <v-sheet class="persentase me-auto">
                  {{
                    (itemSection.policyNote?.bpValuePercentage || "0") + " % "
                  }}
                </v-sheet>
                <v-sheet class="count ml-9 mt-3"
                  >{{ itemSection.policyNote.bpValue1 || "0" }}
                  <span class="approve-of">Approve Of</span>
                  {{ itemSection.policyNote.bpValue2 || "0" }}</v-sheet
                >
              </v-sheet>
            </v-card>
          </div>
        </div>
      </v-col>
      <v-col
        v-if="itemSection?.issueNote?.isvisible"
        cols="6"
        :order="itemSection?.issueNote?.orderBP ?? '0'"
      >
        <div>
          <div
            @click="handleCardClick(itemSection.issueNote)"
            style="cursor: pointer"
          >
            <v-card style="border-radius: 12px; height: 185px" class="pl-3">
              <v-sheet class="d-flex ml-2 mr-4 mt-5">
                <v-sheet class="me-auto">
                  {{ itemSection.issueNote?.bp || "Issue Note" }}</v-sheet
                >
                <v-sheet class="ml-10">
                  <img :src="require('@/v2/assets/workspace/in_dashboard.svg')"
                /></v-sheet>
              </v-sheet>
              <v-sheet class="d-flex ml-2 mr-4 mt-8">
                <v-sheet class="persentase me-auto">
                  {{
                    (itemSection.issueNote?.bpValuePercentage || "0") + " % "
                  }}
                </v-sheet>
                <v-sheet class="count ml-9 mt-3"
                  >{{ itemSection.issueNote.bpValue1 || "0" }}
                  <span class="approve-of">Approve Of</span>
                  {{ itemSection.issueNote.bpValue2 || "0" }}</v-sheet
                >
              </v-sheet>
            </v-card>
          </div>
        </div>
      </v-col>
      <v-col
        v-if="itemSection?.publikasi?.isvisible"
        cols="6"
        :order="itemSection?.publikasi?.orderBP ?? '0'"
      >
        <div>
          <div
            @click="handleCardClick(itemSection.publikasi)"
            style="cursor: pointer"
          >
            <v-card style="border-radius: 12px; height: 185px" class="pl-3">
              <v-sheet class="d-flex ml-2 mr-4 mt-5">
                <v-sheet class="me-auto"> Publikasi </v-sheet>
                <v-sheet class="ml-10">
                  <img
                    :src="
                      require('@/v2/assets/workspace/publikasi_dashboard.svg')
                    "
                /></v-sheet>
              </v-sheet>
              <v-sheet class="d-flex ml-2 mr-4 mt-8">
                <v-sheet class="persentase me-auto">
                  {{ itemSection.publikasi.value || "0" }}
                </v-sheet>
              </v-sheet>
            </v-card>
          </div>
        </div>
      </v-col>
      <v-col
        v-if="itemSection?.chartpack?.isvisible"
        cols="6"
        :order="itemSection?.chartpack?.orderBP ?? '0'"
      >
        <div>
          <v-card style="border-radius: 12px; height: 185px" class="pl-3">
            <v-sheet class="d-flex ml-2 mr-4 mt-5">
              <v-sheet class="me-auto"> Chartpack </v-sheet>
              <v-sheet class="ml-10">
                <img :src="require('@/v2/assets/workspace/chartpack.svg')"
              /></v-sheet>
            </v-sheet>
            <v-sheet class="d-flex ml-2 mr-4 mt-8">
              <v-sheet class="persentase me-auto">
                {{ itemSection.chartpack.totalChartpack || "0" }}
              </v-sheet>
            </v-sheet>
          </v-card>
        </div>
      </v-col>
      <v-col
        v-if="itemSection?.assignment?.isvisible"
        cols="6"
        :order="itemSection?.assignment?.orderBP ?? '0'"
      >
        <div>
          <div
            style="cursor: pointer"
            @click="handleRedirectClick(itemSection.assignment)"
          >
            <v-card style="border-radius: 12px; height: 185px" class="pl-3">
              <v-sheet class="d-flex ml-2 mr-4 mt-5">
                <v-sheet class="me-auto">
                  {{ itemSection.assignment?.bp || "Assignment" }}</v-sheet
                >
                <v-sheet class="ml-10">
                  <img
                    :src="require('@/v2/assets/workspace/ic_assignment.svg')"
                /></v-sheet>
              </v-sheet>
              <v-sheet class="d-flex ml-2 mr-4 mt-8">
                <v-sheet class="persentase me-auto">
                  {{
                    (itemSection.assignment?.bpValuePercentage || "0") + " % "
                  }}
                </v-sheet>
                <v-sheet class="count ml-9 mt-3"
                  >{{ itemSection.assignment?.bpValue1 || "0" }}
                  <span class="approve-of">Approve Of</span>
                  {{ itemSection.assignment.bpValue2 || "0" }}</v-sheet
                >
              </v-sheet>
            </v-card>
          </div>
        </div>
      </v-col>
    </v-row>
    <modal-warning ref="modal" :modal-config="modalConfig" />
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
// import { useStore } from "vuex";
import { TModalWarning } from "@/v2/Type";
import { useStore } from "vuex";
import ModalWarning from "@/v2/components/utils/modal/ModalWarning.vue";
const route = useRoute();
const router = useRouter();
const idEvent = computed(() => route.params.idEvent as string);
// eslint-disable-next-line
const prop = defineProps({
  isLoading: {
    type: Boolean,
    default: false,
  },
  itemSection: {
    type: Object,
    default: () => {
      return {};
    },
  },
  title: {
    type: String,
    default: "",
  },
});
const modal = ref();
const store = useStore();
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
function handleCardClick(item) {
  if (item.isAllowNext) {
    router.push({
      name: "om.rdg-collaboration",
      params: {
        typeRDG: "rdgm",
        idEvent: idEvent.value,
        idDoc: item.idBpDocument as string,
      },
    });
  } else {
    modal.value.show();
  }
}
function handleRedirectClick(item: any): void {
  const navigationMap: Record<string, string> = {
    assignment: "dashboard.assignment.v2.penugasan.search",
    default: "v2.mydashboard",
  };

  const isAssignment = item?.bp?.toLowerCase() === "assignment";
  const routeName = isAssignment
    ? navigationMap.assignment
    : navigationMap.default;

  if (isAssignment) {
    store.commit("globalStore/setStatusSearch", true);
    store.commit("globalStore/setSearch", prop.title);

    router.push({
      name: routeName,
      query: { q: prop.title, searchMode: "true" },
    });

    return;
  }

  if (item.isAllowNext) {
    store.commit("assignmentStore/setItemsFilter", {
      yearPeriod: [item.yearRDG],
      monthPeriod: [item.monthRDG],
      workspaceType: [item.idRDGType],
      satkerKoordinator: [],
      status: [],
      dueYear: [],
    });
  }

  router.push({ name: routeName });
}
</script>

<style scoped>
::-webkit-scrollbar {
  margin-top: 20px;
  margin-right: 2px;
  width: 8px;
  height: 15px;
}
.container {
  margin-top: 20px;
  max-height: 400px;
  overflow-y: scroll;
  padding-bottom: 10px;
  padding-right: 10px;
  padding-left: 1px;
  overflow-x: hidden;
}
.container-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.persentase {
  font-family: Poppins;
  font-size: 34px;
  font-weight: 1000;
  line-height: 51px;
  text-align: left;
  height: 51px;
}
.count {
  font-family: Poppins;
  font-size: 17px;
  font-weight: 600;
  line-height: 34.5px;
  text-align: right;
}
.approve-of {
  font-family: Poppins;
  font-size: 14px;
  font-weight: 500;
  line-height: 21px;
  text-align: right;
}
:deep(a:-webkit-any-link) {
  text-decoration: none;
}
</style>
