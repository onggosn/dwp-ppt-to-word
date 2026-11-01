<template>
  <EditAccessDialog ref="modal" :title="props.title">
    <p class="py-3 px-2" v-html="formattedSectionName(props.sectionName)"></p>

    <v-window v-model="tab" class="px-1">
      <v-window-item :value="1">
        <div class="d-flex flex-column">
          <SearchBar
            copasable
            :onSubmit="handleAddCheckbox"
            accessType="section"
            :placeHolderSearch="
              isAssignmentManagement
                ? 'Enter a name or email address'
                : 'Enter Name'
            "
            :type="'assignment'"
          />
          <v-sheet class="text-grey"> Participant </v-sheet>

          <free-style-shimmer
            v-if="!dataCheckbox.length"
            width="100%"
            height="4.3rem"
            border-radius="10px"
          />
          <ListCheckbox
            v-else
            :title="''"
            :data="dataCheckbox"
            :isLoading="loading"
            :type="'assignment'"
            @edittedMemberType="handleEditMemberAssignment"
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
} from "vue";
import { responsePromise } from "@v2/helpers/utils";
import { TResponseSearchByName } from "@v2/Type";
import { useRoute } from "vue-router";
import SearchBar from "./SearchBar.vue";
import ListDelete from "./ListDelete.vue";
import ListCheckbox from "./ListCheckbox.vue";
import EditAccessDialog from "./EditAccessDialog.vue";
import { useStore } from "vuex";
import { formattedSectionName } from "@/v2/helpers/utils";

defineComponent({
  SearchBar,
  ListDelete,
  ListCheckbox,
  EditAccessDialog,
});

const emit = defineEmits(["onSuccessEdit"]);

const buttonState = computed(
  (): boolean => store.getters["documentStore/getOnloadingButtonState"]
);

const isApprovalInProgress = computed(
  (): boolean => store.getters["collaborationStore/getDocumentStatusId"] == "49"
);

const isAssignmentManagement = computed(() =>
  route.path.includes("assignmentmanagement-new")
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
const route = useRoute();
const loading = ref<boolean>(false);
const store = useStore();
const modal = ref();

const dataCheckbox = ref<
  Array<{
    id: string;
    name: string;
    username: string;
    type: string;
    isEdit: boolean;
    isView: boolean;
    isDownload: boolean;
    isDelete: boolean;
    memberType: number;
    memberTypeName: string;
    idAssignment: string;
  }>
>([]);
const dataDelete = ref<
  Array<{
    idBPDocMember: string;
    name: string;
    type: string;
  }>
>([]);

function loadMemberAssignment() {
  loading.value = true;
  const data = { idAssignment: props.idDoc };

  store
    .dispatch("assignmentStore/getMemberAssignment", data)
    .then((resp) => {
      const temp = resp.responseData;
      dataCheckbox.value = temp.map((e) => {
        const isDeleteValue =
          typeof e?.isDelete !== "undefined" ? e.isDelete : true;
        return {
          idMUser: e.id,
          idMEformMember: e.idAssignment,
          ...e,
          isDelete: isDeleteValue,
        };
      });
    })
    .finally(() => {
      loading.value = false;
    });
}

function handleAddCheckbox(item: TResponseSearchByName[]) {
  const payload = {
    idAssignment: props.idDoc,
    member: item.map((i) =>
      i.isGroup ? { groupName: i.value } : { username: i.username }
    ), // Sementara, API belum ready
  };

  return store
    .dispatch("assignmentStore/InsertListAssignmentMember", payload)
    .then((res) => {
      if (res.responseCode === "011024") {
        root.refs.toast.show({
          message: res.responseMessage,
          color: "warning",
          timeout: 3000,
        });
        return;
      }
      root.refs.toast.show({
        message: res.responseMessage,
        color: "success",
        timeout: 3000,
      });
      loadMemberAssignment();
      return res;
    })
    .finally()
    .catch(response.error);
}

function handleDeleteCheckbox(id: string, idDoc: string) {
  loading.value = true;
  const data = {
    id: id,
    idAssignment: idDoc,
  };
  store
    .dispatch("assignmentStore/DeleteAssignmentMemberByUserName", data)
    .then((res) => {
      if (res.responseCode === "011002") {
        root.refs.toast.show({
          message: res.responseMessage,
          color: "failed",
          timeout: 3000,
        });
        return;
      }

      root.refs.toast.show({
        message: res.responseMessage,
        color: "success",
        timeout: 3000,
      });
      dataCheckbox.value = dataCheckbox.value.filter((d) => d.id !== id);
    })
    .finally(() => {
      loading.value = false;
    });
}

function handleEditMemberAssignment(data, memberType) {
  const payload = {
    id: data.id,
    memberType: memberType,
    idAssignment: props.idDoc,
  };
  store
    .dispatch("assignmentStore/EditAssignmentMemberByUserName", payload)
    .then((res) => {
      if (res.responseCode === "011002") {
        root.refs.toast.show({
          message: res.responseMessage,
          color: "failed",
          timeout: 3000,
        });
        return;
      }
      root.refs.toast.show({
        message: res.responseMessage,
        color: "success",
        timeout: 3000,
      });
      loadMemberAssignment();
      emit("onSuccessEdit");
    })
    .finally()
    .catch(response.error);
}

function openDialog() {
  loadMemberAssignment();
  nextTick(() => {
    modal.value.show();
  });
}

// Expose the openDialog method to the parent
defineExpose({
  openDialog,
});

function hideDialog() {
  modal.value.hide();
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
