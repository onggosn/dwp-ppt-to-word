<template>
  <div>
    <p class="font-weight-bold text-darkBlue text-left">
      Title <span class="text-red font-weight-bold">*</span>
    </p>
    <v-chip style="height: 56px; border-radius: 10px; width: 100%">
      {{ documentName }}
    </v-chip>
  </div>
  <div class="d-flex justify-center">
    <v-card class="mt-5 pb-10 paper" width="21.01cm" min-height="29.7cm">
      <template v-if="loading">
        <p class="text-grey mt-5 mb-5 text-center">
          loading document, please wait...
        </p>
        <v-progress-linear color="grey" indeterminate />
      </template>

      <template v-else>
        <!-- kalo limit ckeditor melibihi threshold muncul pesan  User not registered to CK Editor, please contact admin-->
        <template v-if="isCKEditorTokenNotValid">
          <v-sheet min-height="400px" class="text-center">
            <img
              :src="require('@/v2/assets/workspace/access-denied.svg')"
              class="img-no-available"
            />
            <p class="pt-4 font-weight-bold text-14" style="color: #267dc2">
              {{ ckEditorResponseMessage }}
            </p>
          </v-sheet>
        </template>
        <template
          v-else-if="
            [33, 37].includes(
              store.getters['collaborationStore/getDocumentStatusId']
            ) || isNotRevision
          "
        >
          <!-- buat kondisi, untuk menampilkan preview document dimana, 
      (isRevisi == false dan idStatus == 33) Atau isRevisi == true dan idStatus == 37 -->
          <div v-if="showNoDocumentMessage" class="text-grey mt-10 text-center">
            <div class="d-flex justify-center">
              <img
                :src="require('@/v2/assets/empty/empty_box.svg')"
                class="img-no-available"
                width="400"
                style="margin-bottom: -50px"
              />
            </div>
            <p class="text-grey text-center">Don't have any document</p>
          </div>
          <template v-else>
            <!-- this document is already Approved, show preview mode -->
            <document-editor />
          </template>
        </template>
        <template v-else>
          <div v-if="showNoDocumentMessage" class="text-grey mt-10">
            <div class="d-flex justify-center">
              <img
                :src="require('@/v2/assets/empty/empty_box.svg')"
                class="img-no-available"
                width="400"
                style="margin-bottom: -50px"
              />
            </div>
            <p class="text-grey text-center">Don't have any document</p>
          </div>

          <div v-if="isDocumentTypeValid">
            <div class="d-flex justify-space-between">
              <img :src="require(`@/v2/assets/cop_logo_bi.svg`)" />
              <div class="align-self-center font-weight-bold text-24">
                RAHASIA
              </div>
            </div>
            <div>
              <p class="text-24 font-weight-bold mt-6 mb-6 text-center">
                RISALAH RAPAT
              </p>
            </div>
          </div>
          <template v-for="(item, index) in listForm" :key="item">
            <div
              class="text-left font-weight-bold"
              style="font-size: 0.9167em"
              v-if="item.isView"
            >
              {{ item.sectionName }}
            </div>
            <template v-if="item.isView">
              <template v-for="childItem in item.children" :key="childItem">
                <div
                  class="text-left font-weight-bold"
                  style="font-size: 0.9167em"
                  :style="{
                    'margin-left': getTitleLevel(childItem.bPEFormLabel),
                  }"
                  v-if="childItem.isLabelVisible"
                >
                  {{ childItem.bPEFormLabel }}
                </div>
                <form-editor
                  v-if="childItem.isView && childItem.idFormEditor"
                  :formIndex="index + 1"
                  :channelId="childItem.idFormEditor"
                  :sectionName="childItem.bPEFormLabel"
                  :eformId="childItem.idEForm"
                  :detailForm="childItem"
                  :key="childItem.idEForm"
                />
              </template>
            </template>
          </template>
        </template>
      </template>
    </v-card>
  </div>
  <modal-warning ref="modal" :modal-config="modalConfig" />
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed, defineAsyncComponent } from "vue";
import DocumentEditor from "./editor/DocumentEditor.vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import ModalWarning from "@/v2/components/utils/modal/ModalWarning.vue";
import { TModalWarning } from "@/v2/Type";
import LoaderComponent from "./loader/LoaderComponent.vue";

const FormEditor = defineAsyncComponent({
  loader: () => import("./editor/FormEditor.vue"),
  loadingComponent: LoaderComponent,
  errorComponent: {
    template: "<div>Error loading component</div>",
  },
  suspensible: false,
});

const loading = ref(false);
const showNoDocumentMessage = ref(false);
const store = useStore();
const route = useRoute();
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

const documentName = computed(
  () => store.getters["collaborationStore/getDocumentName"]
);
const listForm = computed(
  () => store.getters["collaborationStore/getListForm"]
);
const ckEditorResponseMessage = computed(
  () => store.getters["userStore/getTokenCKEditor"].ResponseMessage
);
const isCKEditorTokenNotValid = computed(
  () => store.getters["userStore/getTokenCKEditor"].ResponseCode !== "011000"
);
const isDocumentTypeValid = computed(
  () =>
    store.getters["collaborationStore/getDocumentTypeId"] === 1 &&
    listForm.value.length > 0
);

const isNotRevision = computed((): boolean => {
  const inStatusRevision = [34, 35, 36].includes(
    store.state.documentStore.validasiRevision.idStatus
  );
  return (
    (store.state.documentStore.validasiRevision.isRevision ?? false) == false &&
    inStatusRevision
  );
});

function loadData() {
  loading.value = true; // Start loading
  const timeout = setTimeout(() => {
    loading.value = false; // Stop loading after timeout
    // Show modal if data is still not loaded (optional)
    if (!store.getters["collaborationStore/getListForm"]?.length) {
      modal.value.show();
    }
  }, 15000); // Set timeout for 15 seconds

  store
    .dispatch("documentStore/fetchFormDocument", route.params.idDoc)
    .then((data) => {
      clearTimeout(timeout); // Clear timeout if data is fetched
      loading.value = false; // Stop loading
      if (!data.responseData.children?.length) {
        showNoDocumentMessage.value = true;
        modal.value.show();
      }
    })
    .catch(() => {
      loading.value = false; // Stop loading in case of an error
      clearTimeout(timeout); // Clear timeout in case of an error
      showNoDocumentMessage.value = true;
      modal.value.show(); // Show modal in case of an error
    });
}

onMounted(() => {
  loadData();
});

watch(
  () => listForm.value.length,
  (newVal) => {
    if (!newVal) {
      showNoDocumentMessage.value = true;
      modal.value.show();
    }
  }
);

const getTitleLevel = (value: string) => {
  const level = value.split(" ")[0].split(".").length;
  switch (level) {
    case 2:
      return "14px";
    case 3:
      return "36px";
    case 4:
      return "74px";
    case 5:
      return "104px";
    default:
      return "14px";
  }
};
</script>

<style scoped>
.documentStyle {
  border-radius: 8px;
  margin-top: 20px;
  width: 21.01cm;
  padding-top: 1cm;
  padding-left: 1cm;
  padding-right: 1cm;
  padding-bottom: 1cm;
}
.paper {
  border-radius: 8px;
  padding-left: 1cm;
  padding-right: 1cm;
  padding-top: 1cm;
}
</style>
