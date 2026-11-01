<template>
  <!-- Admin Management Button -->
  <v-btn
    v-if="route.path.includes('admin-management')"
    class="rounded-lg px-2 py-2"
    min-width="0"
    color="#065695"
    variant="outlined"
    @click="openDialog()"
  >
    <v-icon
      color="#065695"
      small
      style="cursor: pointer; transform: rotateY(180deg)"
      >mdi-key</v-icon
    >
    <v-tooltip activator="parent" location="bottom">Edit Access</v-tooltip>
  </v-btn>
  <!-- Default Button -->
  <v-btn
    v-else
    size="small"
    variant="outlined"
    style="border-radius: 10px"
    prepend-icon="mdi-account-multiple-plus"
    class="mr-2"
    color="#065695"
    :disabled="!buttonState || isApprovalInProgress"
    @click="openDialog()"
  >
    Access
  </v-btn>
  <EditAccessDialog ref="modal" :title="props.title ?? 'Edit Access Section'">
    <v-tabs v-model="tab" color="#065695">
      <v-tab class="tab-header" :value="1">EDITOR</v-tab>
    </v-tabs>

    <p class="py-3 px-2" v-html="formattedSectionName(props.sectionName)"></p>

    <v-window v-model="tab" class="px-1">
      <v-window-item :value="1">
        <div class="d-flex flex-column">
          <SearchBar
            copasable
            :onSubmit="handleAddCheckbox"
            accessType="section"
          />
          <ListCheckbox
            v-if="dataCheckbox.length"
            :title="'List Access'"
            :data="dataCheckbox"
            :isLoading="loading"
            :type="isAdminManagement ? 'admin' : ''"
            @editted="handleEdit"
            @saveOnChecked="HandleSaveOnChecked"
            @deleted="handleDeleteCheckbox"
          />
        </div>
      </v-window-item>
    </v-window>
  </EditAccessDialog>
</template>

<script setup lang="ts">
/* eslint-disable */
import {
  defineComponent,
  getCurrentInstance,
  ref,
  nextTick,
  computed,
  inject,
} from "vue";
import { responsePromise } from "@v2/helpers/utils";
import {
  TResponseSearchByName,
  TEditAccessCheckbox,
  TEditAccessDelete,
} from "@v2/Type";
import { useRoute } from "vue-router";
import SearchBar from "./SearchBar.vue";
import ListCheckbox from "./ListCheckbox.vue";
import EditAccessDialog from "./EditAccessDialog.vue";
import fetchData from "@v2/helpers/fetchData";
import clientv2 from "@v2/library/ApiClient";
import { useStore } from "vuex";
import { formattedSectionName } from "@/v2/helpers/utils";
import { secureRandomFloat } from "@/v2/helpers/utils";
defineComponent({
  SearchBar,
  ListCheckbox,
  EditAccessDialog,
});

const buttonState = computed(
  (): boolean => store.getters["documentStore/getOnloadingButtonState"]
);

const isApprovalInProgress = computed(
  (): boolean => store.getters["collaborationStore/getDocumentStatusId"] == "49"
);
const isAdminManagement = computed(() =>
  route.path.includes("admin-management")
);

const props = defineProps({
  sectionName: {
    type: String,
    default: null,
  },
  idDoc: {
    type: String,
    default: null,
  },
  idEform: {
    type: String,
    default: null,
  },
  idMEform: {
    type: Number,
    default: null,
  },
  title: {
    type: String,
    default: null,
  },
});
const tab = ref(null);
const { root } = getCurrentInstance() as any;
const response = responsePromise(root);
function showToast(
  message: string,
  color: "success" | "warning" | "error" = "success",
  timeout = 3000
) {
  root?.refs?.toast?.show?.({
    message,
    color,
    timeout,
  });
}
const route = useRoute();
const loading = ref<boolean>(false);
const store = useStore();
const modal = ref();

const dataCheckbox = ref<TEditAccessCheckbox[]>([]);
const dataDelete = ref<TEditAccessDelete[]>([]);

//inject semua doc list dari provide ListItem.vue
const documentList: any = inject("documentList", ref([]));

const api = computed(() => ({
  getList: isAdminManagement.value
    ? (params) => clientv2.GetListMEFormMemberByIdMEForm({ data: params })
    : (params) => clientv2.getListEFormMemberByIdEForm({ data: params }),
  addMember: isAdminManagement.value
    ? (payload) => clientv2.addMEformMemberTemplate({ data: payload })
    : (payload) => clientv2.addEFormMemberByIdEForm({ data: payload }),
  deleteMember: isAdminManagement.value
    ? (params) =>
        clientv2.deleteListMEformMemberTemplateByIdMEFormTemplate({
          data: params,
        })
    : (params) => clientv2.deleteEFormMemberByIdEForm({ data: params }),
}));

function mapToStandardFormat(item: any) {
  if (isAdminManagement.value) {
    const isGroup = item.idMGroup !== null && item.idMGroup !== 0;
    return {
      ...item,
      id: item.idMEformMember,
      name: isGroup ? item.groupName : item.name,
      username: item.username,
      type: isGroup ? "people" : "person",
      idMUser: item.idMUser,
      idMGroup: item.idMGroup,
      isEdit: item.isEdit,
      isView: item.isView,
    };
  } else {
    const isGroup = item.idGroup !== null;
    return {
      ...item,
      id: item.idEFormMember,
      name: isGroup ? item.groupName : item.username,
      type: isGroup ? "people" : "person",
      idUser: item.idUser,
      idGroup: item.idGroup,
      isEdit: item.isEdit,
      isView: item.isView,
    };
  }
}

function load() {
  loading.value = true;
  const data = isAdminManagement.value
    ? { idMEFormTemplate: props.idMEform }
    : { id: props.idEform, idbpdocument: route.params?.idDoc };

  api.value
    .getList(data)
    .then((resp) => {
      dataCheckbox.value = resp.responseData.map(mapToStandardFormat);
    })
    .finally(() => {
      loading.value = false;
    });
}

function handleAddCheckbox(items: TResponseSearchByName[]) {
  const member = items.map((item) =>
    item.isGroup ? { idMGroup: item.id } : { idMUser: item.id }
  );
  const payload = isAdminManagement.value
    ? {
        member,
        idMEFormTemplate: props.idMEform,
        idMBPDocumentTemplate: documentList?.idMBPDocumentTemplate,
      }
    : {
        member,
        IdEForm: props.idEform,
      };
  return api.value
    .addMember(payload)
    .then((res) => {
      if (res.responseCode === "011024") {
        showToast(res.responseMessage, "warning");
        return;
      }
      root.refs.toast.show({
        message: res.responseMessage,
        color: "success",
        timeout: 3000,
      });
      reloadOtherData();
      load();
      return res;
    })
    .catch(response.error);
}

function handleDeleteCheckbox(id: string, idDoc: string) {
  loading.value = true;
  const data = isAdminManagement.value ? { id: idDoc, username: id } : { id };
  api.value
    .deleteMember(data)
    .then((res) => {
      if (!isAdminManagement.value) reloadOtherData();
      showToast(res.responseMessage, "success");
      dataCheckbox.value = dataCheckbox.value.filter((d) =>
        isAdminManagement.value ? d.id !== idDoc : d.id !== id
      );
    })
    .finally(() => {
      loading.value = false;
    });
}

function handleEdit(data: Array<any>) {
  fetchData(clientv2.updateListEFormMemberByIdEForm, {
    data: {
      id: props.idEform,
      listEFormMember: data,
    },
  }).then(() => {
    reloadOtherData();
    showToast("Successfully Saved", "success");
    modal.value.hide();
  });
}

function HandleSaveOnChecked(data: Array<any>) {
  const listEFormMemberTemplate = Array.isArray(data)
    ? data
    : typeof data === "object" && data !== null
    ? [data]
    : [];

  const transformedList = listEFormMemberTemplate.map((item) => ({
    idMEFormMember: item.id,
    isEdit: item.isEdit,
    isView: item.isView,
    ...(item.type == "person"
      ? { idUser: item.idMUser, username: item.username }
      : { idGroup: item.idMGroup, groupName: item.name }),
  }));
  fetchData(clientv2.updateListMEFormMemberTemplateByIdMEForm, {
    data: {
      idMEformTemplate: props.idMEform,
      listEFormMemberTemplate: transformedList,
    },
  })
    .then()
    .catch(response.error);
}

function loadListBpdocMember() {
  loading.value = true;

  fetchData(clientv2.getListBPDocMemberByIdBPDoc, {
    data: {
      idBPDoc: route.params.idDoc,
      accessType: "Approved",
    },
  })
    .then((resp) => {
      dataDelete.value = resp.map((d) => ({
        idBPDocMember: d.IdBPDocMember,
        name: d.idGroup === null ? d.username : d.groupName,
        type: d.idGroup === null ? "person" : "people",
      }));
    })

    .finally(() => {
      loading.value = false;
    });
}

function openDialog() {
  load();
  loadListBpdocMember();
  nextTick(() => {
    modal.value.show();
  });
}

function reloadOtherData() {
  if (!isAdminManagement.value) {
    store.dispatch("documentStore/fetchFormDocument", route.params.idDoc);
    store.dispatch("eFormStore/GetListFlowDetail", {
      id: route.params.idDoc,
    });

    store.commit(
      "collaborationStore/setDocumentFlowCheck",
      secureRandomFloat()
    );
  }
}
</script>

<style scoped>
:deep(.v-window) {
  padding: 0 0.5rem;
  margin: 0 -0.5rem;
}

:deep(.rounded-10) {
  border-radius: 10px;
}
.tab-header {
  color: #bcbcbc;
  font-weight: 600;
}
:deep(.tab-header.v-slide-group-item--active) {
  background: none !important;
  color: #065695 !important;
  border: none !important;
  background-clip: text !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: #065695 !important;
}
.btn-save {
  background: linear-gradient(to right, #065695, #267dc2);
  color: white;
  font-weight: 500;
}
</style>
