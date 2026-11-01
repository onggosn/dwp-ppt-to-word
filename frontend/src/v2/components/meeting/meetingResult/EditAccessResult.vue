<template>
  <v-btn class="pa-1" min-width="0" variant="text" @click="openDialog">
    <v-icon class="table-content-center btn-default" color="#267DC2" small
      >mdi-key</v-icon
    >
    <v-tooltip activator="parent" location="top"
      >Edit Access Meeting Result</v-tooltip
    >
  </v-btn>

  <EditAccessDialog
    ref="modal"
    title="Edit Access"
    @onClose="handleDialogClose"
  >
    <template v-if="loading">
      <v-row>
        <v-col cols="12" v-for="i in 5" :key="i">
          <free-style-shimmer
            :is-loading="true"
            width="100%"
            height="4.3rem"
            border-radius="10px"
          />
        </v-col>
      </v-row>
    </template>

    <template v-if="!loading">
      <SearchBar copasable :onSubmit="handleAddCheckbox" type="material" />
      <ListCheckbox
        v-if="dataCheckbox.length"
        title="Participant"
        :data="dataCheckbox"
        :isLoading="loading"
        :isAdmin="true"
        @deleted="handleDeleteCheckbox"
        @saveOnChecked="handleSaveChecked"
        type="nonSector"
      />
    </template>
  </EditAccessDialog>
</template>

<script setup lang="ts">
import { getCurrentInstance, ref } from "vue";
import { TResponseSearchByName } from "@v2/Type";
import { useRoute } from "vue-router";
import SearchBar from "@v2/components/collaboration/SearchBar.vue";
import ListCheckbox from "@v2/components/collaboration/ListCheckbox.vue";
import EditAccessDialog from "@v2/components/collaboration/EditAccessDialog.vue";
import { useStore } from "vuex";
type TCheckboxType = {
  id: string;
  name: string;
  type: string;
  isEdit: boolean;
  isView: boolean;
  isDownload: boolean;
  isDelete: boolean;
};

const props = defineProps({
  idEventHasilPembahasan: {
    type: String,
    required: false,
  },
  idDoc: {
    type: String,
    required: false,
  },
  idEform: {
    type: String,
    required: false,
  },
});

const { root } = getCurrentInstance() as any;
const route = useRoute();
const loading = ref<boolean>(false);
const store = useStore();
const modal = ref();
const emit = defineEmits(["onSuccess"]);

const dataCheckbox = ref<TCheckboxType[]>([]);

function handleAddCheckbox(items: TResponseSearchByName[]) {
  const payload = {
    member: items.map((item) => ({
      idMember: item.id,
      isGroup: item.isGroup,
    })),
    idEventHasilPembahasan: props.idEventHasilPembahasan,
  };
  return store
    .dispatch("materialStore/addMemberHasilPembahasan", payload)
    .then((resp) => {
      if (resp.responseCode === "011006") {
        root.refs.toast.show({
          message: "User already added",
          color: "warning",
          timeout: 3000,
        });
      }

      if (resp.responseCode === "011000") {
        root.refs.toast.show({
          message: "Successfully add access",
          color: "success",
          timeout: 3000,
        });
        load();
      }
    });
}

function handleDialogClose() {
  emit("onSuccess");
}

function handleDeleteCheckbox(id: string) {
  loading.value = true;
  const payload = {
    id: id,
  };
  store
    .dispatch("materialStore/deleteMemberHasilPembahasan", payload)
    .then(() => {
      root.refs.toast.show({
        message: "Successfully delete access",
        color: "success",
        timeout: 3000,
      });
      dataCheckbox.value = dataCheckbox.value.filter((d) => d.id !== id);
    })
    .finally(() => {
      loading.value = false;
    });
}

function handleSaveChecked(data: TCheckboxType) {
  if (!Array.isArray(data) || data.length === 0) {
    if (typeof data === "object" && data !== null) {
      const { id, isView, isDownload } = data;
      const payload = { id, isView, isDownload };
      doEditAccess(payload);
    }
  } else {
    data.forEach((obj) => {
      const { id, isView, isDownload } = obj;
      const payload = { id, isView, isDownload };
      doEditAccess(payload);
    });
  }
}

function doEditAccess(payload: any) {
  store
    .dispatch("materialStore/updateMemberHasilPembahasan", payload)
    .then(() => {
      root.refs.toast.show({
        message: "Successfully Update Access",
        color: "success",
        timeout: 3000,
      });
    });
}

function load() {
  loading.value = true;
  const payload = {
    idEvent: route.params.idEvent,
    idEventHasilPembahasan: props.idEventHasilPembahasan,
  };
  store
    .dispatch("materialStore/getListAccessMemberHasilPembahasan", payload)
    .then((resp) => {
      const data = resp.responseData.participantList;
      dataCheckbox.value = data.map((d) => {
        const { participant, access } = d;
        const { id, name, isGroup } = participant;
        const { isView, isDownload } = access;
        const isDeleteValue =
          typeof d?.isDelete !== "undefined" ? d.isDelete : true;

        return {
          id,
          isView,
          isDownload,
          name,
          type: isGroup ? "people" : "person",
          isDelete: isDeleteValue,
        };
      });
    })
    .finally(() => {
      loading.value = false;
    });
}

function openDialog() {
  load();
  modal.value.show();
}
</script>

<style scoped>
.btn-default {
  border: 1px solid;
  border-radius: 4px;
  padding: 13px;
  transform: scaleX(-1);
}
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
