<template>
  <v-btn
    variant="outlined"
    rounded
    color="#065695"
    class="mr-2"
    size="small"
    @click="startEdit"
    >Access
    <template #prepend>
      <v-icon>mdi-account-multiple-plus</v-icon>
    </template>
  </v-btn>

  <v-dialog v-model="dialog" persistent width="700">
    <v-card class="border-radius-dwp">
      <v-form class="pl-2 pr-2">
        <v-card-title class="text-center mt-3">
          <h3 class="text-h6 font-weight-regular">Edit Access Section</h3>
          <v-btn
            density="default"
            icon="mdi-close"
            variant="text"
            class="btn-close"
            @click="dialog = false"
          />

          <hr class="line mt-5 mb-4" />
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-tabs v-model="tab" bg-color="transparent">
              <v-tab class="tab-header" value="inprogress"> IN PROGRESS </v-tab>
              <v-tab class="tab-header" value="approved"> APPROVED </v-tab>
            </v-tabs>
            <v-window v-model="tab" class="mt-3">
              <v-window-item value="inprogress">
                <v-sheet class="mb-4">
                  1. Ringkasan Eksekutif -> Section
                </v-sheet>

                <v-autocomplete
                  label="Enter a name"
                  v-model:search="search"
                  @update:modelValue="insertParticipant"
                  :items="searchResults"
                  item-title="value"
                  variant="solo"
                  return-object
                  append-inner-icon="mdi-magnify"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props" :title="''" class="pt-5 pb-5">
                      <v-row align="center" class="spacer" no-gutters>
                        <v-col class="text-center">
                          <v-avatar color="#eaeaea" size="42">
                            <v-icon
                              color="#1f75b7"
                              :icon="
                                item?.raw?.isGrup
                                  ? 'mdi-account-multiple'
                                  : 'mdi-account'
                              "
                            ></v-icon>
                          </v-avatar>
                        </v-col>
                        <v-col cols="8" class="text-left ms-2">
                          <p style="color: #3a416f">
                            {{ item?.raw?.value }}
                          </p>
                        </v-col>
                        <v-col class="hidden-xs-only text-center ms-2">
                          <v-icon
                            icon="mdi-plus-circle-outline"
                            color="#1f75b7"
                          >
                          </v-icon>
                        </v-col>
                      </v-row>
                    </v-list-item>
                  </template>
                  <template v-slot:append-inner>
                    <v-icon
                      v-if="store.getters['userStore/getLoading']"
                      color="primary"
                      dark
                      class="mr-2"
                    >
                      mdi-loading mdi-spin
                    </v-icon>
                  </template>
                </v-autocomplete>
                <v-sheet class="text-grey mb-4"> List Access </v-sheet>
                <v-sheet style="height: 60vh; overflow: scroll">
                  <v-sheet class="d-flex flex-nowrap align-self-center mt-4">
                    <v-sheet class="align-self-center" width="10%"></v-sheet>
                    <v-sheet class="align-self-center" width="50%"></v-sheet>
                    <v-sheet class="align-self-center mr-2" width="15%">
                      <v-checkbox
                        v-model="selectAllEdit"
                        label="Select All"
                        @change="selectAllEditItems"
                        color="green"
                      ></v-checkbox>
                    </v-sheet>
                    <v-sheet class="align-self-center mr-2" width="15%">
                      <v-checkbox
                        v-model="selectAllView"
                        label="Select All "
                        @change="selectAllViewItems"
                        color="green"
                      ></v-checkbox>
                    </v-sheet>
                    <v-sheet class="align-self-center" width="10%"></v-sheet>
                  </v-sheet>

                  <template v-for="item in listAccess" :key="item.id">
                    <v-sheet class="d-flex align-center mt-4">
                      <v-sheet class="align-self-center" width="10%">
                        <v-avatar color="#eaeaea" size="42" class="mr-2">
                          <v-icon
                            color="#1f75b7"
                            :icon="
                              item.isGrup
                                ? 'mdi-account-multiple'
                                : 'mdi-account'
                            "
                          ></v-icon>
                        </v-avatar>
                      </v-sheet>
                      <v-sheet class="align-self-center" width="50%">
                        <span>{{ item.name }}</span>
                      </v-sheet>
                      <v-sheet
                        class="align-self-center mr-2"
                        style="text-align: right"
                        width="15%"
                      >
                        <v-checkbox
                          v-model="item.isEdit"
                          label="Edit"
                          class="custom-checkbox"
                          color="green"
                        ></v-checkbox>
                      </v-sheet>
                      <v-sheet class="align-self-center" width="15%">
                        <v-checkbox
                          v-model="item.isView"
                          label="View"
                          class="custom-checkbox"
                          color="green"
                        ></v-checkbox>
                      </v-sheet>
                      <v-sheet
                        class="align-self-center"
                        style="text-align: right; margin-bottom: 20px"
                        width="10%"
                      >
                        <v-btn class="pa-1" min-width="0" variant="text">
                          <v-icon
                            class="table-content-center"
                            color="#267DC2"
                            small
                            style="
                              border: 1px solid;
                              border-radius: 4px;
                              padding: 13px;
                              cursor: pointer;
                            "
                            >mdi-delete</v-icon
                          >
                          <v-tooltip activator="parent" location="top"
                            >Delete</v-tooltip
                          >
                        </v-btn>
                      </v-sheet>
                    </v-sheet>
                  </template>
                </v-sheet>
              </v-window-item>
              <v-window-item value="approved">
                <v-sheet class="mb-4"> 1. Tittle Ckeditor </v-sheet>
                <v-autocomplete
                  label="Enter a name"
                  v-model:search="searchItem"
                  @update:modelValue="insertApprove"
                  :items="searchResultApprove"
                  item-title="value"
                  variant="solo"
                  return-object
                  append-inner-icon="mdi-magnify"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props" :title="''" class="pt-5 pb-5">
                      <v-row align="center" class="spacer" no-gutters>
                        <v-col class="text-center">
                          <v-avatar color="#eaeaea" size="42">
                            <v-icon
                              color="#1f75b7"
                              :icon="
                                item?.raw?.isGrup
                                  ? 'mdi-account-multiple'
                                  : 'mdi-account'
                              "
                            ></v-icon>
                          </v-avatar>
                        </v-col>
                        <v-col cols="8" class="text-left ms-2">
                          <p style="color: #3a416f">
                            {{ item?.raw?.value }}
                          </p>
                        </v-col>
                        <v-col class="hidden-xs-only text-center ms-2">
                          <v-icon
                            icon="mdi-plus-circle-outline"
                            color="#1f75b7"
                          >
                          </v-icon>
                        </v-col>
                      </v-row>
                    </v-list-item>
                  </template>
                </v-autocomplete>
                <v-sheet class="text-grey mb-4"> List Access </v-sheet>
                <v-sheet style="height: 60vh; overflow: scroll">
                  <template v-for="item in listApprove" :key="item.id">
                    <v-sheet class="d-flex align-center mt-4">
                      <v-sheet class="align-self-center" width="10%">
                        <v-avatar color="#eaeaea" size="42" class="mr-2">
                          <v-icon
                            color="#1f75b7"
                            :icon="
                              item.isGrup
                                ? 'mdi-account-multiple'
                                : 'mdi-account'
                            "
                          ></v-icon>
                        </v-avatar>
                      </v-sheet>
                      <v-sheet class="align-self-center" width="80%">
                        <span>{{ item.value }}</span>
                      </v-sheet>
                      <v-sheet class="align-self-center" width="10%">
                        <v-btn class="pa-1" min-width="0" variant="text">
                          <v-icon
                            class="table-content-center"
                            color="#267DC2"
                            small
                            style="
                              border-radius: 4px;
                              padding: 13px;
                              cursor: pointer;
                              color: red;
                            "
                            >mdi-delete</v-icon
                          >
                          <v-tooltip activator="parent" location="top"
                            >Delete</v-tooltip
                          >
                        </v-btn>
                      </v-sheet>
                    </v-sheet>
                  </template>
                </v-sheet>
              </v-window-item>
            </v-window>
            <div class="text-right mt-3 pb-5 pr-5">
              <v-btn class="btn-next" elevation="4" width="100" height="45"
                >Save</v-btn
              >
            </div>
          </v-container>
        </v-card-text>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import { useStore } from "vuex";
const dialog = ref(false);
const store = useStore();
const startEdit = () => {
  dialog.value = true;
};
const tab = ref("inprogress");
const search = ref("");
const loading = false;
const searchResults = ref<any[]>([]);
const searchItem = ref("");
const selectedItems = ref({});
const selectAll = ref(false);
const selectAllEdit = ref(false);
const selectAllView = ref(false);
const listApprove = ref([]);

const initializeCheckboxes = () => {
  listAccess.value.forEach((item) => {
    selectedItems.value[item.id] = false;
  });
};
const selectAllEditItems = () => {
  listAccess.value.forEach((item) => {
    item.isEdit = selectAllEdit.value;
  });
};

const selectAllViewItems = () => {
  listAccess.value.forEach((item) => {
    item.isView = selectAllView.value;
  });
};
watch(selectAllEdit, () => {
  selectAllEditItems();
});

watch(selectAllView, () => {
  selectAllViewItems();
});
watch(search, (val) => {
  store
    .dispatch("userStore/fetchSearchUserNew", {
      query: val,
      isEvent: false,
    })
    .then((result) => {
      searchResults.value = result;
    });
});
const listAccess = ref([
  {
    id: 1,
    name: "John Doe",
    memberType: 2,
    email: "john@example.com",
    isEdit: true,
    isView: false,
    isGroup: true,
  },
  {
    id: 2,
    name: "Alice Smith",
    memberType: 1,
    email: "alice@example.com",
    isEdit: false,
    isView: true,
    isGroup: true,
  },
  {
    id: 3,
    name: "Chaterine Tamara",
    memberType: 2,
    email: "cathe@example.com",
    isEdit: false,
    isView: false,
    isGroup: false,
  },
  {
    id: 4,
    name: "Donna Terra",
    memberType: 1,
    email: "donna@example.com",
    isEdit: false,
    isView: false,
    isGroup: false,
  },
]);
watch(selectAll, (newValue) => {
  listAccess.value.forEach((item) => {
    selectedItems.value[item.id] = newValue;
  });
});

const insertParticipant = (value) => {
  /*  let requestData = {
    idAssignment: this.idAssignment,
    username: item.isGrup ? "" : item.inputId,
    groupName: item.isGrup ? item.inputId : "",
    memberType: 3,
  };
  client
    .insertListAssignmentMember({
      store: this.$store,
      data: requestData,
    })
    .then(() => {
      this.$root.toast.show({
        message: "User successfully added",
        color: "success",
        timeout: 3000,
        icon: "mdi-check",
      });
      this.selected_participant = null;
      this.$refs.memberLoader.callApi();
    })
    .catch(() => {
      this.$root.toast.show({
        message: "Something went wrong",
        color: "error",
        timeout: 3000,
        icon: "mdi-check",
      });
    })
    .finally(() => {
      this.isLoading = false;
      this.search = null;
    }); */
};
const searchResultApprove = ref([
  { id: 1, value: "John Doe", isGrup: false },
  { id: 2, value: "Alice Smith", isGrup: false },
  // Add more items as needed
]);
const insertApprove = (value) => {
  if (!listApprove.value.some((participant) => participant.id === value.id)) {
    listApprove.value.push(value);
  }
};
onMounted(() => {
  initializeCheckboxes();
});
</script>

<style scoped>
:deep(.v-textarea .v-field__input) {
  height: 1px !important;
  background: red !important;
  display: contents;
}
:deep(.ck.ck-toolbar.ck-toolbar_grouping) {
  display: none;
}

:deep(.ck.ck-content.ck-editor__editable) {
  border: 1px solid #dfdfdf;
  border-radius: 11px;
  padding: 10px;
  margin-left: 9px;
  margin-right: 5px;
  /* margin-bottom: 20px; */
  height: 200px;
  width: 98%;
  box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
    0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
    0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12));
}
:deep(.v-chip.v-chip--density-default.chip-shadow) {
  box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
    0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
    0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12));
  height: 56px;
  width: 98%;
  color: grey !important;
  border: none;
  background: #dfdfdf;
  font-size: 16px;
  margin: 10px;
}

:deep(.v-chip.v-chip--density-default) {
  height: calc(var(--v-chip-height) + 0px);
  border-radius: 5px;
  background: #e9f5ff;
  border: 1px solid #6eb3ea;
  color: #065391;
  padding: 10px;
  margin-right: 5px;
  margin-bottom: 5px;
}

:deep(.dp__overlay) {
  border-radius: 10px;
}
:deep(.dp__instance_calendar) {
  box-shadow: 1px 1px 7px 3px #7393b3;
  border-radius: 5px;
  padding: 10px;
}

:deep(.dp__arrow_top) {
  display: none;
}

:deep(.v-textarea .v-field) {
  --v-textarea-control-height: var(--v-input-control-height);
  background: white;
  border-radius: 12px;
}
:deep(.v-field.v-field--appended) {
  border-radius: 12px !important;
}

:deep(.v-text-field .v-field) {
  border-radius: 12px;
}
:deep(.tab-header.v-slide-group-item--active) {
  background: none !important;
  color: #065695 !important;
  border: none !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: #065695 !important;
}
:deep(.v-selection-control .v-label) {
  white-space: normal;
  word-break: break-word;
  height: 100%;
  width: 100%;
  font-size: 15px;
}
.tab-header {
  color: #bcbcbc;
  font-weight: 600;
}

:deep(.v-tab--selected .v-tab__slider) {
  height: 2px;
  border-radius: 10px;
  color: #065695;
}

:deep(.v-tab.v-tab) {
  height: 35px;
  font-weight: 900;
  color: #bcbcbc !important;
}
:deep(.mdi-delete::before) {
  color: red;
}

.btn-close {
  position: absolute;
  right: 0;
  top: 0;
  margin-top: 10px;
  margin-right: 10px;
}

.line {
  border: none;
  height: 2px;
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}
.custom-checkbox
  input[type="checkbox"]:checked
  + .v-label
  .v-input--selection-controls__input::before {
  border-color: green;
  background-color: green;
}
.mdi-delete {
  border: 0px solid !important;
  border-radius: 4px;
  padding: 13px;
  cursor: pointer;
  box-shadow: 0px 3px 7px 0px #85858540 !important;
}
</style>
