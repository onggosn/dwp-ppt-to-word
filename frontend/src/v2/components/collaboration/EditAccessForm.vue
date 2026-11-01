<template>
  <v-btn
    size="small"
    variant="outlined"
    :style="
      routeType === 'content' ? 'border-radius: 8px' : 'border-radius: 10px'
    "
    :prepend-icon="
      routeType !== 'content'
        ? props.isAdmin
          ? 'mdi-key'
          : 'mdi-account-multiple-plus'
        : ''
    "
    class="mr-2"
    :class="routeType === 'content' ? 'font-weight-bold' : ''"
    color="#065695"
    :disabled="!buttonState"
    @click="openDialog()"
  >
    <v-icon
      v-if="routeType === 'content'"
      class="mr-2"
      color="#065695"
      small
      style="cursor: pointer; transform: rotateY(180deg)"
      >mdi-key</v-icon
    >
    Edit Access
  </v-btn>

  <EditAccessDialog
    ref="modal"
    :title="props.isAdmin ? 'Edit Access' : 'Edit Access Form'"
  >
    <div v-if="props.isAdmin" style="padding-bottom: 10px; width: 100%">
      <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
        Content Title<span style="color: red"></span>
      </p>
      <v-chip class="border-radius-dwp" style="width: 100%; padding: 30px">
        <span style="width: 100%">{{ props.fromAdmin.bPDocumentName }}</span>
      </v-chip>
    </div>
    <v-tabs v-model="tab" color="#065695">
      <v-tab v-if="!props.isFinal" class="tab-header" :value="1"
        >PENYUSUN</v-tab
      >
      <v-tab v-if="!props.isAdmin" class="tab-header" :value="2"
        >DOKUMEN FINAL</v-tab
      >
      <v-tab v-else class="tab-header" :value="2">DOKUMEN FINAL</v-tab>
      <v-tab v-if="isRisalahDoc" class="tab-header" :value="3"
        >TIM TEKNIS</v-tab
      >
      <v-tab v-if="!props.isFinal" class="tab-header" :value="4"
        >ORGANIZER</v-tab
      >
    </v-tabs>
    <v-window v-model="tab" class="px-1">
      <v-window-item :value="1">
        <div class="d-flex flex-column pt-4">
          <!-- tab penyusun -->
          <SearchBar
            copasable
            :is-admin="props.isAdmin"
            accessType="page"
            :onSubmit="handleAdd"
          />
          <ListDelete
            :data="dataDelete"
            :isLoading="isLoading"
            title="List Access"
            @deleted="validateDelate"
          />
        </div>
      </v-window-item>
      <v-window-item :value="2">
        <div class="d-flex flex-column pt-4">
          <!-- tab dokumen final -->
          <!-- <div v-if="props.isAdmin" style="padding-bottom: 10px">
            <span>{{ props.fromAdmin.bPDocumentName }}</span>
          </div> -->
          <SearchBar copasable :onSubmit="handleAdd" accessType="approved" />
          <ListDelete
            :data="dataDelete"
            :isLoading="isLoading"
            title="List Access"
            @deleted="validateDelate"
          />
        </div>
      </v-window-item>
      <v-window-item :value="3">
        <div class="d-flex flex-column pt-4">
          <!-- tab tim teknis -->
          <!-- <div v-if="props.isAdmin" style="padding-bottom: 10px">
            <span>{{ props.fromAdmin.bPDocumentName }}</span>
          </div> -->
          <SearchBar copasable :onSubmit="handleAdd" accessType="timTeknis" />
          <ListDelete
            v-if="dataDelete.length"
            :data="dataDelete"
            :isLoading="loading"
            title="List Access"
            @deleted="validateDelate"
          />
        </div>
      </v-window-item>
      <v-window-item :value="4">
        <div class="d-flex flex-column pt-4">
          <SearchBar
            copasable
            :onSubmit="handleAdd"
            :is-admin="props.isAdmin"
            accessType="organizer"
          />
          <ListDelete
            :data="dataDelete"
            :isLoading="isLoading"
            title="List Access"
            @deleted="validateDelate"
          />
        </div>
      </v-window-item>
    </v-window>
  </EditAccessDialog>
  <ModalConfirm ref="modalWarning" :form-config="modalConfig">
    <template v-slot:icon-img>
      <v-avatar color="white" size="80" style="margin-top: -60px">
        <img :src="'/images/warningAlert.png'" style="width: 75px" />
      </v-avatar>
    </template>
    <template v-slot:btn-action>
      <div style="text-align: center">
        <v-btn
          @click="handleCloseWarning"
          class="mr-2 rounded-lg btn primary-gradient"
        >
          Close
        </v-btn>
      </div>
    </template>
  </ModalConfirm>
</template>

<script setup lang="ts">
import {
  defineComponent,
  ref,
  nextTick,
  getCurrentInstance,
  watch,
  computed,
} from "vue";
import { useRoute } from "vue-router";
import {
  TResponseSearchByName,
  TModalConfirm,
  TEditAccessDelete,
} from "@v2/Type";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import { responsePromise } from "@v2/helpers/utils";
import SearchBar from "./SearchBar.vue";
import ListDelete from "./ListDelete.vue";
import EditAccessDialog from "./EditAccessDialog.vue";
import fetchData from "@v2/helpers/fetchData";
import clientv2 from "@v2/library/ApiClient";
import { useStore } from "vuex";
import { secureRandomFloat } from "@/v2/helpers/utils";

defineComponent({
  SearchBar,
  ListDelete,
  EditAccessDialog,
});

const buttonState = computed(
  (): boolean => store.getters["documentStore/getOnloadingButtonState"]
);

const props = defineProps({
  isFinal: {
    type: Boolean,
    default: false,
  },
  isAdmin: {
    type: Boolean,
    default: false,
  },
  isRisalahDoc: {
    type: Boolean,
    default: false,
  },
  fromAdmin: {
    type: Object,
    default: null,
  },
});

const dataDelete = ref<TEditAccessDelete[]>([]);

const { root } = getCurrentInstance() as any;
const response = responsePromise(root);
const route = useRoute();
const loading = ref<boolean>(false);
const store = useStore();
const modal = ref();
const modalWarning = ref();
const isLoading = ref(false);
const tab = ref(1);
const modalConfig = ref<TModalConfirm>({
  title: "Warning",
  message:
    "You cannot delete the last penyusun. At least one penyusun must remain to ensure continued access to this document.",
});

const routeType = computed(() => {
  if (route.path.includes("admin-management/content")) return "content";
  return "other";
});

function getAccessType(tabValue: number) {
  if (tabValue === 1) return "Page";
  if (tabValue === 2) return "Approved";
  if (tabValue === 4) return "Organizer";
  return "TimTeknis";
}

function handleAdd(item: TResponseSearchByName[]) {
  const accessType = getAccessType(tab.value);
  const member = item.map((i) =>
    i.isGroup ? { idMGroup: i.id } : { idMUser: i.id }
  );
  if (props.isAdmin) {
    const payload: any = {
      idMBPDoc: props.fromAdmin.idMBPDocumentTemplate,
      accessType,
      member,
    };
    return clientv2
      .addMBPDocMemberTemplateByIdMBPDocTemplate({ data: payload })
      .then((res) => {
        response.success(res, () => {
          if (!props.isAdmin) {
            store.commit("adminStore/setRefreshList", secureRandomFloat());
          }
          load();
        });
        return res;
      })
      .catch(response.error);
  } else {
    const payload: any = {
      member,
      IdBPDoc: route.params.idDoc,
      accessType,
    };
    return clientv2
      .addBPDocMemberByIdBPDoc({ data: payload })
      .then((res) => {
        response.success(res, () => {
          if (!props.isAdmin) {
            store.dispatch(
              "documentStore/fetchFormDocument",
              route.params.idDoc
            );
          }
          load();
        });
        return res;
      })
      .catch(response.error);
  }
}
function handleCloseWarning() {
  modalWarning.value.hide();
  modal.value.show();
}

function getDeleteWarningMessage(tabValue: number): string {
  switch (tabValue) {
    case 1:
      return "You cannot delete the last penyusun. At least one<br>penyusun must remain to ensure continued<br>access to this document.";
    case 2:
      return "You cannot delete the last Document Final. At<br>least one Document Final must remain to ensure<br>continued access to this document.";
    case 3:
      return "You cannot delete the last Tim Teknis. At least<br>one Tim Teknis must remain to ensure continued<br>access to this document.";
    default:
      return "You cannot delete the last item. At least one must remain to ensure continued access to this document.";
  }
}

function validateDelate(id: string) {
  if (dataDelete.value.length === 1 && tab.value !== 4) {
    modalConfig.value.message = getDeleteWarningMessage(tab.value);
    modalWarning.value.show({});
    modal.value.hide();
  } else {
    handleDelete(id);
  }
}

function handleDelete(id: string) {
  if (props.isAdmin) {
    loading.value = true;
    fetchData(clientv2.deleteListMBPDocMemberTemplateByIdMBPDocMemberTemplate, {
      data: {
        id: id,
      },
    })
      .then(() => {
        root.refs.toast.show({
          message: "Successfully Deleted",
          color: "success",
          timeout: 3000,
        });
        if (!props.isAdmin)
          store.commit("adminStore/setRefreshList", secureRandomFloat());

        nextTick(() => {
          load();
        });
      })
      .finally(() => {
        loading.value = false;
      });
  } else {
    loading.value = true;
    fetchData(clientv2.deleteListBPDocMemberByIdBPDocMember, {
      data: {
        id: id,
      },
    })
      .then(() => {
        root.refs.toast.show({
          message: "Successfully Deleted",
          color: "success",
          timeout: 3000,
        });
        store.dispatch("documentStore/fetchFormDocument", route.params.idDoc);
        load();
      })
      .finally(() => {
        loading.value = false;
      });
  }
}

function mapDeleteData(isAdmin: boolean, d: any) {
  const isDeleteValue = typeof d?.isDelete !== "undefined" ? d.isDelete : true;
  if (isAdmin) {
    return {
      idBPDocMember: d.Id,
      name: d.Name,
      type: d.IdMGroup === null ? "person" : "people",
      isDelete: isDeleteValue,
    };
  } else {
    return {
      idBPDocMember: d.IdBPDocMember,
      name: d.idGroup === null ? d.username : d.groupName,
      type: d.idGroup === null ? "person" : "people",
      isDelete: isDeleteValue,
    };
  }
}

function load() {
  isLoading.value = true;
  dataDelete.value = [];
  store.commit("collaborationStore/setDocumentFlowCheck", secureRandomFloat());
  const isAdmin = props.isAdmin;
  const payload = isAdmin
    ? {
        IdMBPDocTemplate: props.fromAdmin.idMBPDocumentTemplate,
        accessType: getAccessType(tab.value),
      }
    : {
        idBPDoc: route.params.idDoc,
        accessType: getAccessType(tab.value),
      };
  const fetchAPI = isAdmin
    ? clientv2.getListMBPDocMemberTemplateByIdMBPDocTemplate
    : clientv2.getListBPDocMemberByIdBPDoc;
  fetchData(fetchAPI, {
    data: payload,
  })
    .then((resp) => {
      if (!resp.length) {
        dataDelete.value = [];
        return;
      }
      dataDelete.value = resp.map((d: any) => mapDeleteData(isAdmin, d));
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function openDialog() {
  load();
  nextTick(() => {
    modal.value.show();
  });
}

watch(route, () => {
  load();
});

watch(tab, () => {
  load();
});
</script>

<style scoped lang="scss">
:deep(.rounded-12) {
  border-radius: 12px !important;
}

.border-bottom {
  border: 1px solid;
  border-image-slice: 1;
  border-image-source: linear-gradient(to left, #fffffc, #a6abc7, #fffffc);
  border-left: 0;
  border-right: 0;
  border-top: 0;
}
.shadow {
  box-shadow: 0 3px 7px 0 #85858540;
}
</style>
