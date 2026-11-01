<template>
  <v-dialog
    v-model="isShow"
    max-width="600"
    class="edit_dialog--wrapper"
    persistent
  >
    <v-card class="border-radius-dwp">
      <v-card-title class="text-center mt-3">
        <h3 class="text-h6 font-weight-regular">Edit Role</h3>
        <v-btn
          density="default"
          icon="mdi-close"
          variant="text"
          class="btn-close"
          @click="cancel"
        />

        <hr class="line mt-5 mb-4" />
      </v-card-title>

      <v-card-text>
        <div class="mb-4">
          <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
            Nama User
          </p>
          <v-chip class="chip-shadow border-radius-dwp ml-2 mr-2">
            {{ userData.name || "-" }}
          </v-chip>
        </div>

        <div class="mb-4">
          <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
            Satker
          </p>
          <v-chip class="chip-shadow border-radius-dwp ml-2 mr-2">
            {{ userData.satkerName || "-" }}
          </v-chip>
        </div>

        <div class="mb-4">
          <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
            Jabatan
          </p>
          <v-chip class="chip-shadow border-radius-dwp ml-2 mr-2">
            {{ userData.jabatanName || "-" }}
          </v-chip>
        </div>

        <div class="mb-4">
          <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">Role</p>
          <v-autocomplete
            v-model="selectedRoles"
            v-model:search="searchText"
            variant="solo"
            placeholder="Select Roles"
            multiple
            chips
            :items="filteredAvailableRoles"
            item-title="name"
            item-value="id"
            hide-selected
            closable-chips
            class="pl-2 pr-2 protected-chips"
            :loading="isLoadingRoles"
            @update:model-value="updateFormData"
            @keydown.capture="preventChipDeletion"
          >
            <template v-slot:item="{ props, item }">
              <v-list-item
                class="mt-2"
                v-bind="props"
                :title="item.raw.name"
              ></v-list-item>
            </template>
            <template v-slot:chip="{ props, item }">
              <v-chip
                size="small"
                class="ml-2"
                :color="item.raw.isDelete ? '' : 'grey'"
                :closable="item.raw.isDelete ? true : false"
                variant="flat"
                v-bind="props"
                >{{ item.raw.name }}</v-chip
              >
            </template>
            <template v-slot:append-inner>
              <v-icon v-if="isLoadingRoles" color="primary" dark class="mr-2">
                mdi-loading mdi-spin
              </v-icon>
            </template>
          </v-autocomplete>
        </div>
      </v-card-text>

      <div class="text-right mt-3 pb-5 pr-5">
        <v-btn
          class="btn-prev mr-3"
          @click="cancel"
          elevation="4"
          width="100"
          height="45"
          :loading="isLoading"
          >Cancel</v-btn
        >
        <v-btn
          class="btn-next"
          elevation="4"
          width="100"
          height="45"
          :loading="isLoading"
          @click="saveUser"
          >Save</v-btn
        >
      </div>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, getCurrentInstance, computed } from "vue";
import { useStore } from "vuex";

const store = useStore();
const { root } = getCurrentInstance() as any;
const emit = defineEmits<{
  (e: "onClose", value?: boolean): void;
}>();

const isShow = ref<boolean>(false);
const isLoading = ref<boolean>(false);
const isLoadingRoles = ref<boolean>(false);
const userData = ref<any>({});
const selectedRoles = ref<string[]>([]);
const userStatus = ref<boolean>(true);
const searchText = ref<string>("");

const formData = ref<any>({
  selectedRoles: [],
});
const availableRoles = ref<any[]>([]);

// Computed property to filter roles based on selected roles' idMRoleType
const filteredAvailableRoles = computed(() => {
  if (!selectedRoles.value.length) {
    return availableRoles.value;
  }

  // Get idMRoleType of selected roles
  const selectedRoleTypes = selectedRoles.value
    .map((selectedId) => {
      const role = availableRoles.value.find((r: any) => r.id === selectedId);
      return role?.idMRoleType;
    })
    .filter(Boolean);

  // Filter available roles
  return availableRoles.value.filter((role: any) => {
    // If role is already selected, show it (for chips display)
    if (selectedRoles.value.includes(role.id)) {
      return true;
    }
    // If role's idMRoleType is not in selected types, show it
    return !selectedRoleTypes.includes(role.idMRoleType);
  });
});

async function show(user?: any) {
  isShow.value = true;
  if (user) {
    userData.value = { ...user };
    await getMasterRoles();

    selectedRoles.value =
      user.listMRole?.map((role: any) => role.idMRole) || [];
    formData.value.selectedRoles = selectedRoles.value;
    userStatus.value = user.isActive ?? true;
  }
}

function hide() {
  isShow.value = false;
  userData.value = {};
  selectedRoles.value = [];
  formData.value.selectedRoles = [];
  userStatus.value = true;
  searchText.value = "";
  emit("onClose");
}

function cancel() {
  isShow.value = false;
  userData.value = {};
  selectedRoles.value = [];
  formData.value.selectedRoles = [];
  userStatus.value = true;
  searchText.value = "";
}

function updateFormData() {
  formData.value.selectedRoles = selectedRoles.value;
  searchText.value = ""; // Clear search
}

function saveUser() {
  formData.value.selectedRoles = selectedRoles.value;
  isLoading.value = true;

  const payload = {
    idMuser: userData.value.idMuser,
    roleId: selectedRoles.value,
  };
  store
    .dispatch("adminStore/UpdateUserAndRole", payload)
    .then((res: any) => {
      if (res.responseCode === "011000") {
        root.refs.toast.show({
          message: "User roles updated successfully.",
          color: "success",
          timeout: 5000,
        });
        hide();
      } else {
        root.refs.toast.show({
          message: res.responseMessage || "Failed to update user roles.",
          color: "error",
          timeout: 5000,
        });
      }
    })
    .catch((error: any) => {
      root.refs.toast.show({
        message: "Failed to update user roles.",
        color: "error",
        timeout: 5000,
      });
      throw error;
    })
    .finally(() => {
      isLoading.value = false;
    });
}

const getMasterRoles = () => {
  isLoadingRoles.value = true;
  return store
    .dispatch("adminStore/getDropdownMRole", {
      chosenUsername: userData.value.username,
    })
    .then((res: any) => {
      let list = res.responseData || [];

      if (res.responseCode === "011000") {
        availableRoles.value = list.map((role: any) => {
          const userRole = userData.value.listMRole?.find(
            (uRole: any) => uRole.idMRole === role.id
          );
          return {
            id: role.id,
            name: role.name,
            isDelete: userRole?.isDelete ?? true,
            idMRoleType: role.idMRoleType,
          };
        });
      }
    })
    .catch((error) => {
      root.refs.toast.show({
        message: "Failed to fetch roles. Please try again later.",
        color: "error",
        timeout: 5000,
      });
      throw error;
    })
    .finally(() => {
      isLoadingRoles.value = false;
    });
};

const preventChipDeletion = (event: KeyboardEvent) => {
  if (event.key === "Backspace" || event.key === "Delete") {
    const target = event.target as HTMLInputElement;
    const hasText = searchText.value && searchText.value.length > 0;
    const cursorAtStart = target.selectionStart === 0;

    if (!hasText || cursorAtStart) {
      event.preventDefault();
      event.stopPropagation();
      return false;
    }
  }
};

defineExpose({
  show,
  hide,
});
</script>

<style lang="scss" scoped>
.edit_dialog--wrapper {
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

  :deep(.v-chip.v-chip--density-default.chip-shadow) {
    box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
      0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
      0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12));
    height: 56px;
    width: 98%;
    color: grey !important;
    border: none;
    background: #dfdfdf !important;
    font-size: 16px;
    margin: 10px;
  }

  .btn-next {
    background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
    border-radius: 10px !important;
    border-color: #267dc2 !important;
    padding-left: 16px !important;
    padding-right: 16px !important;
    font-size: 14px !important;
    color: white;
    font-weight: 900;
  }

  .btn-prev {
    background: white;
    border-radius: 10px !important;
    padding-left: 16px !important;
    padding-right: 16px !important;
    font-size: 14px !important;
    color: #d6212a;
    font-weight: 900;
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

  :deep(.protected-chips .v-field__input) {
    .v-chip {
      pointer-events: auto !important;
    }
  }
}
</style>
