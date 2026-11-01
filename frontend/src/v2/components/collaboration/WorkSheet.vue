<template>
  <div>
    <p class="font-weight-bold text-darkBlue text-left">
      Title <span class="text-red font-weight-bold">*</span>
    </p>
    <v-chip
      style="height: 56px; border-radius: 10px; width: 100%"
      class="custom-chip"
    >
      <v-tooltip
        v-if="isDocNameOverflowing"
        location="bottom"
        :text="documentName"
      >
        <template v-slot:activator="{ props }">
          <p ref="docName" v-bind="props" class="ellipsis-text">
            {{ documentName }}
          </p>
        </template>
      </v-tooltip>
      <p v-else :key="documentName" ref="docName" class="ellipsis-text">
        {{ documentName }}
      </p>
    </v-chip>
  </div>

  <v-card class="mt-5 paper" min-height="900px">
    <!-- ── Loading (fetch in-progress OR brief transition guard) ── -->
    <v-sheet
      v-if="cardView === 'loading'"
      min-height="400px"
      class="d-flex align-center justify-center"
    >
      <v-progress-circular color="#045695" size="50" width="7" indeterminate />
    </v-sheet>

    <!-- ── CKEditor token still resolving ── -->
    <v-sheet
      v-else-if="cardView === 'waiting'"
      min-height="400px"
      class="text-center"
    >
      <v-progress-circular
        class="mt-3"
        color="#045695"
        size="50"
        width="7"
        indeterminate
      />
      <p class="pt-4 font-weight-bold text-14" style="color: #267dc2">
        Thank you for your patience! Your request is processing,<br />and your
        token CKE will be ready soon.
      </p>
    </v-sheet>

    <!-- ── CKEditor token invalid / error ── -->
    <v-sheet
      v-else-if="cardView === 'invalid'"
      min-height="400px"
      class="text-center"
    >
      <img
        :src="require('@/v2/assets/workspace/access-denied.svg')"
        class="img-no-available"
      />
      <p class="pt-4 font-weight-bold text-14" style="color: #267dc2">
        {{ ckEditorResponseMessage }}
      </p>
    </v-sheet>

    <!-- ── No document available ── -->
    <div v-else-if="cardView === 'empty'" class="text-grey mt-10 text-center">
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

    <!-- ── Inline CKEditor ── -->
    <div v-else-if="cardView === 'editor'" class="worksheet">
      <document-editor />
    </div>

    <!-- ── External material viewer ── -->
    <ViewDocument
      v-else-if="cardView === 'material' && dataMaterial"
      :document="dataMaterial"
      :size="dataMaterial.size"
      type="material"
    />

    <ViewDocument v-else-if="cardView === 'finalisasi'" type="finalisasi" />

    <!-- ── Read-only paper view ── -->
    <PaperView v-else-if="cardView === 'paper'" />
  </v-card>
  <modal-warning ref="modal" :modal-config="modalConfig" />
  <ModalConfirm ref="modalConfirm" :form-config="formPopup">
    <template v-slot:icon-img>
      <v-avatar
        size="80"
        style="margin-top: -38px; filter: drop-shadow(#9b9b9b 2px 2px 3px)"
      >
        <img src="/images/icon/iconWarning.png" style="width: 80px" />
      </v-avatar>
    </template>
    <template v-slot:desc>
      <div v-html="formPopup.message" />
    </template>
    <template v-slot:btn-action>
      <div class="text-center">
        <v-btn class="ml-2 primary-gradient rounded-lg" @click="closeModal"
          >Close</v-btn
        >
      </div>
    </template>
  </ModalConfirm>
</template>

<script setup lang="ts">
/* eslint-disable */
import { useStore } from "vuex";
import {
  ref,
  computed,
  watch,
  nextTick,
  onMounted,
  onBeforeUnmount,
} from "vue";
import DocumentEditor from "./editor/DocumentEditor.vue";
import { useRoute } from "vue-router";
import ModalWarning from "@/v2/components/utils/modal/ModalWarning.vue";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import { TModalWarning, TModalConfirm, TMaterialPreview } from "@/v2/Type";
import PaperView from "./PaperView.vue";
import ViewDocument from "@v2/components/meeting/meetingMaterial/ViewDocument.vue";

const store = useStore();
const route = useRoute();

const modal = ref<InstanceType<typeof ModalWarning> | null>(null);
const modalConfirm = ref<InstanceType<typeof ModalConfirm> | null>(null);
const docName = ref<HTMLElement | null>(null);

const showNoDocumentMessage = ref<boolean | null>(null);
const isDocNameOverflowing = ref(false);
const isLoading = ref(true);

const documentName = computed(
  () => store.getters["collaborationStore/getDocumentName"]
);
const isContentMaterial = computed(
  () => store.getters["collaborationStore/getIsContentMaterial"]
);
const isContentFinalisasi = computed(
  () => store.getters["collaborationStore/getIsContentFinalisasi"]
);
const isCKEditorTokenWaiting = computed(
  () => store.getters["userStore/getLoadingTokenCke"]
);
const userLimitError = computed(
  () => store.getters["documentStore/getUserLimitError"]
);
const connectionFailed = computed(
  () => store.getters["documentStore/getConnectionFailed"]
);
const documentVersion = computed(
  () => store.getters["collaborationStore/getDocumentVersion"]
);

const dataMaterial = computed(() => {
  const material = store.getters["collaborationStore/getDataMaterial"];
  if (!material) return null;
  return {
    id: material.idEventPresentationMaterial,
    docExt: material.extension,
    title: material.documentName,
    size: material.size,
  };
});

const isCKEditorTokenNotValid = ref(false);
const ckEditorTokenData = ref<any>(null);

const ckEditorResponseMessage = computed(() => {
  const data = ckEditorTokenData.value;
  if (!data) return "";
  if ("message" in data)
    return "Something went wrong. Request failed with status code 400";
  return data.ResponseMessage ?? "";
});

watch(
  () => store.getters["userStore/getTokenCKEditor"],
  async (tokenPromise) => {
    try {
      const tokenData = await tokenPromise;
      ckEditorTokenData.value = tokenData;
      isCKEditorTokenNotValid.value =
        !tokenData ||
        typeof tokenData !== "object" ||
        !("ResponseCode" in tokenData) ||
        tokenData.ResponseCode !== "011000";
    } catch {
      ckEditorTokenData.value = null;
      isCKEditorTokenNotValid.value = true;
    }
  },
  { immediate: true }
);

type CardView =
  | "loading"
  | "waiting"
  | "invalid"
  | "empty"
  | "editor"
  | "material"
  | "finalisasi"
  | "paper";

const isNotRevision = computed((): boolean => {
  const { isRevision, idStatus } = store.state.documentStore.validasiRevision;
  return (isRevision ?? false) === false && [34, 35, 36].includes(idStatus);
});

const showEditorView = computed(() => {
  const statusId = store.getters["collaborationStore/getDocumentStatusId"];
  return [33, 37, 40, 61].includes(statusId) || isNotRevision.value;
});

const cardView = computed((): CardView => {
  if (isLoading.value) return "loading";
  if (isCKEditorTokenWaiting.value) return "waiting";
  if (isCKEditorTokenNotValid.value) return "invalid";
  if (showNoDocumentMessage.value === true) return "empty";
  if (dataMaterial.value && isContentMaterial.value) return "material";
  if (isContentFinalisasi.value && documentVersion.value.toLowerCase() == 'version 2') return "finalisasi";
  if (showEditorView.value) return "editor";
  if (showNoDocumentMessage.value === false) return "paper";
  return "loading";
});

let transitionTimer: ReturnType<typeof setTimeout> | null = null;

watch(
  () =>
    [
      showEditorView.value,
      isContentMaterial.value,
      dataMaterial.value,
    ] as const,
  () => {
    if (isLoading.value) return;
    isLoading.value = true;
    if (transitionTimer) clearTimeout(transitionTimer);
    transitionTimer = setTimeout(() => {
      isLoading.value = false;
    }, 80);
  }
);

const checkOverflow = async () => {
  await nextTick();
  if (docName.value) {
    isDocNameOverflowing.value =
      docName.value.scrollWidth > docName.value.clientWidth;
  }
};

watch(documentName, () => {
  isDocNameOverflowing.value = false;
  checkOverflow();
});

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

const formPopup = ref<TModalConfirm>({
  title: "Oops, CKEditor License Full",
  btnSubmitLabel: "Close",
  width: 500,
  btnSubmitColor: "primary-gradient",
  message: `<center>The license for CKEditor is currently full.<br>
Please reach out to <b>DMST-MRDG</b> if you need to<br>enable this feature.</center>`,
  messageClass: "text-center",
});

const buildModalConfig = (
  overrides: Partial<TModalWarning> & { imgLocation?: string }
): TModalWarning => ({
  img: {
    location: overrides.imgLocation ?? "workspace/access-denied.svg",
    width: overrides.img?.width ?? "395px",
    height: overrides.img?.height ?? "311px",
  },
  title: overrides.title ?? "",
  description: overrides.description ?? "",
  btnBackgroundStyle: "linear-gradient(to right, #065695, #267DC2)",
  textBtn: "Close",
  textWeight: 600,
  textStyle: "italic",
});

const showModalWarning = () => modalConfirm.value?.show({});
const closeModal = () => modalConfirm.value?.hide();

const fetchData = () => {
  isLoading.value = true;
  store
    .dispatch("documentStore/fetchFormDocument", route.params.idDoc)
    .then((data) => {
      const res = data.responseData;

      if (!res?.children?.length) {
        if (res?.idBpDocumentStatus === 43) {
          modalConfig.value = buildModalConfig({
            imgLocation: "workspace/fileIsDelete.svg",
            description:
              "Sorry, document that you've requested has been deleted",
          });
          showNoDocumentMessage.value = false;
        } else {
          showNoDocumentMessage.value = true;
        }
        modal.value?.show();
        return;
      }
      /**
       * (Bug BE Jason) Ketika document sudah approve, isNoDataMaterial malah jadi true
       * jadinya kondisinya ditambah isAksesMaterial || dataMaterial null
       */
      if (
        ((res.isNoDataMaterial && !res.isAksesMaterial) ||
          res.dataMaterial == null) &&
        res.isContentMaterial
      ) {
        modalConfig.value = buildModalConfig({
          imgLocation: "empty/no_available_state.svg",
          img: {
            location: "empty/no_available_state.svg",
            width: "300px",
            height: "311px",
          },
        });
        showNoDocumentMessage.value = true;
        modal.value?.show();
        return;
      }

      if (
        !res.isAksesMaterial &&
        res.isContentMaterial &&
        !res.isNoDataMaterial
      ) {
        showNoDocumentMessage.value = true;
        modal.value?.show();
        return;
      }

      showNoDocumentMessage.value = false;
    })
    .catch(() => {
      showNoDocumentMessage.value = true;
      modal.value?.show();
    })
    .finally(() => {
      isLoading.value = false;
    });
};

watch(
  () => store.getters["collaborationStore/getSectionActive"],
  (val: string) => {
    if (!val) return;
    const byId = document.getElementById(`section-form-${val}`);
    if (byId) {
      byId.scrollIntoView({ behavior: "smooth" });
    } else {
      const match = Array.from(
        document.querySelectorAll("#readonlyeditor .title-level-1 strong")
      ).find((el) => el.innerHTML === val);
      match?.scrollIntoView({
        behavior: "auto",
        block: "start",
        inline: "nearest",
      });
    }
    store.commit("collaborationStore/setSectionActive", null);
  }
);

watch(
  () => store.getters["collaborationStore/getFlagAccessDoc"],
  (val) => {
    showNoDocumentMessage.value = !!val;
    if (val) modal.value?.show();
  }
);

watch(userLimitError, (val) => {
  if (!val) return;
  formPopup.value.title = "Oops, CKEditor License Full";
  formPopup.value.message = `<center>The license for CKEditor is currently full.<br>Please reach out to <b>DMST-MRDG</b> if you need to<br>enable this feature.</center>`;
  showModalWarning();
});

watch(connectionFailed, (val) => {
  if (!val) return;
  formPopup.value.title = "Connection Lost";
  formPopup.value.message = `<center>Your connection to the server was lost. Please<br><b>reload the page</b> to continue your work.<br>If this keeps happening, please contact the<br><b>Helpdesk Call Center.</b></center>`;
  showModalWarning();
});

onMounted(() => {
  fetchData();
  checkOverflow();
  window.addEventListener("resize", checkOverflow);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", checkOverflow);
  if (transitionTimer) clearTimeout(transitionTimer);
});
</script>
<style scoped>
.paper {
  border-radius: 8px;
  padding: 1cm;
  min-height: 200px;
}

.custom-chip :deep(.v-chip__content) {
  min-width: 0;
}

.ellipsis-text {
  margin: 0;
  width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}
</style>
