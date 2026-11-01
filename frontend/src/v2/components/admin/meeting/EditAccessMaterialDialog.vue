<template>
  <v-btn class="pa-1" min-width="0" variant="text" @click="openDialog">
    <v-icon class="btn-default" color="#267DC2" small>mdi-key</v-icon>
    <v-tooltip activator="parent" location="top">Edit Access</v-tooltip>
  </v-btn>
  <EditAccessDialog ref="modal" title="Edit Access" maxWidth="1100">
    <!-- NOTE: sementara `type = assignment` karena payload nya sama dengan type assignment -->
    <SearchBar
      copasable
      :onSubmit="handleAddCheckbox"
      type="assignment"
      placeHolderSearch="Search Name"
    />
    <span class="text-sm mb-3">List Access</span>
    <template v-if="loading">
      <v-row>
        <v-col cols="12" v-for="i in 3" :key="i">
          <free-style-shimmer
            :is-loading="true"
            width="100%"
            height="4rem"
            border-radius="10px"
          />
        </v-col>
      </v-row>
    </template>
    <template v-else>
      <v-row v-if="dataCheckbox.length === 0">
        <v-col cols="12" class="text-center">
          <span class="text-sm mb-2"
            >Data not found, please add new access</span
          >
        </v-col>
      </v-row>
      <v-list v-else>
        <v-list-item>
          <template v-slot:append>
            <div class="col">
              <v-checkbox
                v-model="selectAllEdit"
                label="Select All"
                color="#065391"
                hide-details
                class="mr-1"
              />
            </div>
            <div class="col">
              <v-checkbox
                v-model="selectAllPreview"
                label="Select All"
                color="#065391"
                hide-details
                class="mr-1"
              />
            </div>
            <div class="col">
              <v-checkbox
                v-model="selectAllDownload"
                label="Select All"
                color="#065391"
                hide-details
                class="mr-1"
              />
            </div>
            <div class="col">
              <v-checkbox
                v-model="selectAllMetadata"
                label="Select All"
                color="#065391"
                hide-details
                class="mr-1"
              />
            </div>
            <div class="col">
              <v-checkbox
                v-model="selectAllDelete"
                label="Select All"
                color="#065391"
                hide-details
                class="mr-1"
              />
            </div>
            <div class="spacer"></div>
          </template>
        </v-list-item>
        <v-list-item v-for="item in dataCheckbox" :key="item.id">
          <template v-slot:prepend>
            <v-avatar color="#eaeaea" size="40">
              <img
                v-if="item.type === `person`"
                :src="require(`@/v2/assets/icon/person.svg`)"
              />
              <img v-else :src="require(`@/v2/assets/icon/people.svg`)" />
            </v-avatar>
          </template>
          <template v-slot:title> {{ item.name }} </template>
          <template v-slot:append>
            <div class="col">
              <v-checkbox
                v-model="item.isEdit"
                label="Edit Access"
                color="#065391"
                hide-details
                class="mr-1"
                @change="handleUpdateCheckbox(item)"
              />
            </div>
            <div class="col">
              <v-checkbox
                v-model="item.isPreview"
                label="Preview"
                color="#065391"
                hide-details
                class="mr-1"
                @change="handleUpdateCheckbox(item)"
              />
            </div>
            <div class="col">
              <v-checkbox
                v-model="item.isDownload"
                label="Download"
                color="#065391"
                hide-details
                class="mr-1"
                @change="handleUpdateCheckbox(item)"
              />
            </div>
            <div class="col">
              <v-checkbox
                v-model="item.isMetadata"
                label="Metadata"
                color="#065391"
                hide-details
                class="mr-1"
                @change="handleUpdateCheckbox(item)"
              />
            </div>
            <div class="col">
              <v-checkbox
                v-model="item.isDelete"
                label="Delete"
                color="#065391"
                hide-details
                class="mr-1"
                @change="handleUpdateCheckbox(item)"
              />
            </div>
            <div class="spacer d-flex justify-end align-center">
              <span>
                <v-btn
                  size="small"
                  min-width="0"
                  class="px-2"
                  @click="handleDelete(item)"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </span>
            </div>
          </template>
        </v-list-item>
      </v-list>
    </template>
  </EditAccessDialog>
</template>
<script setup lang="ts">
import { ref, getCurrentInstance, computed, defineProps } from "vue";
import EditAccessDialog from "@v2/components/collaboration/EditAccessDialog.vue";
import SearchBar from "@v2/components/collaboration/SearchBar.vue";
import { TResponseCbAccess, TResponseSearchByName } from "@v2/Type";
import { useStore } from "vuex";

const modal = ref();
const store = useStore();
const { root } = getCurrentInstance() as any;
const loading = ref(false);
const dataCheckbox = ref<TResponseCbAccess[]>([]);
const props = defineProps({
  id: {
    type: Number,
    default: 0,
  },
});

const selectAllEdit = computed({
  get: () =>
    dataCheckbox.value.length > 0 &&
    dataCheckbox.value.every((item) => item.isEdit),
  set: (val: boolean) => {
    dataCheckbox.value = dataCheckbox.value.map((item) => ({
      ...item,
      isEdit: val,
    }));
    saveAccess();
  },
});

const selectAllPreview = computed({
  get: () =>
    dataCheckbox.value.length > 0 &&
    dataCheckbox.value.every((item) => item.isPreview),
  set: (val: boolean) => {
    dataCheckbox.value = dataCheckbox.value.map((item) => ({
      ...item,
      isPreview: val,
    }));
    saveAccess();
  },
});

const selectAllDownload = computed({
  get: () =>
    dataCheckbox.value.length > 0 &&
    dataCheckbox.value.every((item) => item.isDownload),
  set: (val: boolean) => {
    dataCheckbox.value = dataCheckbox.value.map((item) => ({
      ...item,
      isDownload: val,
    }));
    saveAccess();
  },
});

const selectAllMetadata = computed({
  get: () =>
    dataCheckbox.value.length > 0 &&
    dataCheckbox.value.every((item) => item.isMetadata),
  set: (val: boolean) => {
    dataCheckbox.value = dataCheckbox.value.map((item) => ({
      ...item,
      isMetadata: val,
    }));
    saveAccess();
  },
});

const selectAllDelete = computed({
  get: () =>
    dataCheckbox.value.length > 0 &&
    dataCheckbox.value.every((item) => item.isDelete),
  set: (val: boolean) => {
    dataCheckbox.value = dataCheckbox.value.map((item) => ({
      ...item,
      isDelete: val,
    }));
    saveAccess();
  },
});

const openDialog = () => {
  loadData();
  modal.value.show();
};

const handleAddCheckbox = (items: TResponseSearchByName[]) => {
  const payload = {
    idMEventDocPresentationMaterialTemplate: props.id,
    member: items.map((item) => ({
      idMGroup: item.isGroup ? item.id : null,
      idMUser: item.isGroup ? null : item.id,
      isEditAccess: false,
      isDownload: false,
      isPreview: false,
      isMetadata: false,
      isDelete: false,
    })),
  };

  return store
    .dispatch("adminStore/addMemberPresentationMaterial", payload)
    .then((resp) => {
      if (resp.responseCode === "011000") {
        root.refs.toast.show({
          message: "Successfully add access",
          color: "success",
          timeout: 3000,
        });
        loadData();
      }
    })
    .catch(() => {
      root.refs.toast.show({
        message: "Failed to add access",
        color: "error",
        timeout: 3000,
      });
    });
};

const loadData = () => {
  loading.value = true;
  const payload = {
    idMEventDocPresentationMaterialTemplate: props.id,
  };
  store
    .dispatch("adminStore/getListAccessMemberPresentationMaterial", payload)
    .then((resp) => {
      dataCheckbox.value = resp.responseData.map(({ participant, access }) => ({
        id: participant.idMEventPresentationMaterialMapping,
        isEdit: access.isEditAccess,
        isDownload: access.isDownload,
        isPreview: access.isPreview,
        isMetadata: access.isMetadata,
        isDelete: access.isDelete,
        name: participant.name,
        type: participant.isGroup ? "people" : "person",
        isGroup: participant.isGroup,
      }));
    })
    .finally(() => {
      loading.value = false;
    });
};

const handleDelete = (item: TResponseCbAccess) => {
  loading.value = true;
  const payload = {
    idMEventPresentationMaterialMapping: item.id,
  };

  store
    .dispatch("adminStore/deleteMemberPresentationMaterial", payload)
    .then((resp) => {
      if (resp.responseCode === "011000") {
        root.refs.toast.show({
          message: resp.responseMessage || "Successfully delete access",
          color: "success",
          timeout: 3000,
        });
        dataCheckbox.value = dataCheckbox.value.filter((d) => d.id !== item.id);
      }
    })
    .catch(() => {
      root.refs.toast.show({
        message: "Failed to delete access",
        color: "error",
        timeout: 3000,
      });
    })
    .finally(() => {
      loading.value = false;
    });
};

const saveAccess = () => {
  const payload = dataCheckbox.value.map((item) => ({
    idMEventPresentationMaterialMapping: item.id,
    isEditAccess: item.isEdit,
    isDownload: item.isDownload,
    isPreview: item.isPreview,
    isMetadata: item.isMetadata,
    isDelete: item.isDelete,
  }));
  store
    .dispatch("adminStore/updateMemberPresentationMaterial", payload)
    .then((resp) => {
      if (resp.responseCode === "011000") {
        root.refs.toast.show({
          message: "Access updated successfully",
          color: "success",
          timeout: 3000,
        });
      }
    })
    .catch(() => {
      root.refs.toast.show({
        message: "Failed to update access",
        color: "error",
        timeout: 3000,
      });
    });
};

const handleUpdateCheckbox = (item: TResponseCbAccess) => {
  const payload = [
    {
      idMEventPresentationMaterialMapping: item.id,
      isEditAccess: item.isEdit,
      isDownload: item.isDownload,
      isPreview: item.isPreview,
      isMetadata: item.isMetadata,
      isDelete: item.isDelete,
    },
  ];

  store
    .dispatch("adminStore/updateMemberPresentationMaterial", payload)
    .then((resp) => {
      if (resp.responseCode === "011000") {
        root.refs.toast.show({
          message: "Access updated successfully",
          color: "success",
          timeout: 3000,
        });
      }
    })
    .catch(() => {
      root.refs.toast.show({
        message: "Failed to update access",
        color: "error",
        timeout: 3000,
      });
    });
};
</script>
<style scoped>
.btn-default {
  border: 1px solid;
  border-radius: 4px;
  padding: 13px;
  transform: scaleX(-1);
}
.text-sm {
  display: block;
  font-size: 0.875rem;
  color: #a6abc7;
}
.spacer {
  width: 50px;
  height: 36px;
}

:deep(.mdi-delete) {
  background: linear-gradient(#d6212a, #ff000d);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
:deep(.v-selection-control .v-label) {
  font-size: 13px;
}
:deep(.v-list-item-title) {
  color: #3a416f;
}
.col {
  flex: 1;
  width: 120px;
}
</style>
