<template>
  <v-card class="pa-2" elevation="3" :style="{ animationDelay: props.delay }">
    <v-row
      align="center"
      :class="mfaLoading || lockLoading ? 'loading-state' : ''"
    >
      <v-col cols="12" md="3">
        <div class="field-section ml-5">
          <p class="field-value">{{ item.name || "N/A" }}</p>
        </div>
      </v-col>
      <v-col cols="12" md="3">
        <div class="field-section">
          <p class="field-value">{{ item.satker || "N/A" }}</p>
        </div>
      </v-col>
      <v-col cols="12" md="3">
        <div class="field-section">
          <p class="field-value">{{ item.jabatan || "N/A" }}</p>
        </div>
      </v-col>
      <v-col cols="12" md="1">
        <div class="checkbox-section">
          <div class="checkbox-container">
            <v-checkbox
              v-if="!mfaLoading"
              class="mfa-checkbox"
              v-model="mfaValue"
              density="compact"
              hide-details
              :disabled="mfaLoading"
              @change="showMFAConfirmation"
            ></v-checkbox>
            <v-progress-circular
              v-if="mfaLoading"
              indeterminate
              size="16"
              width="2"
              color="#065391"
              class="checkbox-loader"
            >
            </v-progress-circular>
            <span class="loading-text ml-2 mr-10">MFA</span>
          </div>
        </div>
      </v-col>
      <v-col cols="12" md="2">
        <div class="checkbox-section">
          <div class="checkbox-container">
            <div
              v-if="!lockValue && !lockLoading"
              class="custom-lock-indicator"
              style="margin-left: 5px !important"
            ></div>
            <span
              v-if="!lockValue && !lockLoading"
              class="ml-2"
              style="font-size: 13px !important"
              >Lock</span
            >
            <v-checkbox
              v-show="lockValue"
              v-if="!lockLoading && item.isLock !== 0"
              v-model="lockValue"
              label="Lock"
              :disabled="item.isLock === 0"
              density="compact"
              hide-details
              @change="showLockConfirmation"
            ></v-checkbox>
            <v-progress-circular
              v-if="lockLoading"
              indeterminate
              size="16"
              width="2"
              color="#065391"
              class="checkbox-loader"
            ></v-progress-circular>
            <span v-if="lockLoading" class="loading-text ml-2">Lock</span>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Confirmation Dialog -->
    <v-dialog v-model="showConfirmDialog" max-width="550" persistent>
      <v-card class="pa-5">
        <v-card-title class="text-h6 font-weight-bold dialog-title">
          <v-btn
            class="close-btn"
            icon
            size="small"
            variant="text"
            @click="cancelConfirmation"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <div class="font-weight-bold text-center mt-5 text-20">
          {{ confirmationTitle }}
        </div>
        <v-card-text class="confirmation-text">
          <p v-html="confirmationMessage"></p>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            class="cancel-btn rounded-lg"
            color="white"
            variant="flat"
            elevation="2"
            @click="cancelConfirmation"
          >
            Cancel
          </v-btn>
          <v-btn
            class="confirm-btn rounded-lg"
            variant="flat"
            elevation="3"
            @click="proceedWithChange"
          >
            {{ getConfirmButtonLabel() }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup lang="ts">
import { ref, watch, getCurrentInstance } from "vue";
import { useStore } from "vuex";

interface Props {
  item: any;
  isLoading?: boolean;
  delay?: string;
}

const props = defineProps<Props>();
const store = useStore();
const instance: any = getCurrentInstance()?.root.refs;

// Reactive variables for checkboxes
const mfaValue = ref(props.item.isMFA === 1);
const lockValue = ref(props.item.isLock === 1);

// Loading states
const mfaLoading = ref(false);
const lockLoading = ref(false);

// Dialog state
const showConfirmDialog = ref(false);
const confirmationTitle = ref("");
const confirmationMessage = ref("");
const pendingChange = ref<"mfa" | "lock" | null>(null);
const previousMfaValue = ref(mfaValue.value);
const previousLockValue = ref(lockValue.value);

// Watch for prop changes to update local state
watch(
  () => props.item.isMFA,
  (newValue) => {
    mfaValue.value = newValue === 1;
  }
);

watch(
  () => props.item.isLock,
  (newValue) => {
    lockValue.value = newValue === 1;
  }
);

// Show MFA confirmation dialog
const showMFAConfirmation = () => {
  // Store the previous value before showing dialog
  previousMfaValue.value = !mfaValue.value;

  confirmationTitle.value = mfaValue.value ? "Enable MFA" : "Disable MFA";
  if (mfaValue.value) {
    confirmationMessage.value = `Are you sure you want to enable <b> Multi-Factor Authentication (MFA) </b> for this user?\nThe user will be required to verify their identity using\nMFA during login.`;
  } else {
    confirmationMessage.value = `Are you sure you want to disable <b> Multi-Factor Authentication (MFA) </b> for this user?\nThe user will no longer be required to verify their identity using MFA during login.`;
  }
  pendingChange.value = "mfa";
  showConfirmDialog.value = true;
};

// Show Lock confirmation dialog
const showLockConfirmation = () => {
  // Store the previous value before showing dialog
  previousLockValue.value = !lockValue.value;

  confirmationTitle.value = "Unlock User";
  confirmationMessage.value =
    "Are you sure you want to unlock this user?\nThe user will regain access to the system.";
  pendingChange.value = "lock";
  showConfirmDialog.value = true;
};

// Cancel confirmation and revert checkbox
const cancelConfirmation = () => {
  if (pendingChange.value === "mfa") {
    mfaValue.value = previousMfaValue.value;
  } else if (pendingChange.value === "lock") {
    lockValue.value = previousLockValue.value;
  }

  showConfirmDialog.value = false;
  pendingChange.value = null;
};

// Get dynamic confirm button label
const getConfirmButtonLabel = () => {
  if (pendingChange.value === "mfa") {
    return mfaValue.value ? "Yes, Enable" : "Yes, Disable";
  } else if (pendingChange.value === "lock") {
    return lockValue.value ? "Yes, Lock" : "Yes, Activate";
  }
  return "Confirm";
};

// Proceed with the change
const proceedWithChange = async () => {
  showConfirmDialog.value = false;

  if (pendingChange.value === "mfa") {
    await updateMFA();
  } else if (pendingChange.value === "lock") {
    await updateLock();
  }

  pendingChange.value = null;
};

const updateMFA = async () => {
  mfaLoading.value = true;
  await new Promise((resolve) => setTimeout(resolve, 1000));
  try {
    const response = await store.dispatch("adminStore/updateMFA", {
      username: props.item.username || props.item.name,
      isMFA: mfaValue.value ? 1 : 0,
    });
    if (response?.responseCode == "011000") {
      instance.toast.show({
        message:
          response?.responseMessage ??
          "Successfully Enabled MFA for selected user",
        color: "success",
        timeout: 3000,
      });
    } else {
      mfaValue.value = !mfaValue.value;
      instance.toast.show({
        message:
          response?.responseMessage ??
          "Successfully Disabled MFA for selected user",
        color: "error",
        timeout: 3000,
      });
    }
  } catch (error) {
    mfaValue.value = !mfaValue.value;
    instance.toast.show({
      message: "An error occurred while updating MFA status",
      color: "error",
      timeout: 3000,
    });
  } finally {
    mfaLoading.value = false;
  }
};

const updateLock = async () => {
  lockLoading.value = true;
  await new Promise((resolve) => setTimeout(resolve, 1000));
  try {
    const response = await store.dispatch("adminStore/updateUserLock", {
      username: props.item.username,
    });

    if (response.responseCode == "011000") {
      instance.toast.show({
        message: "Successfully Unlock User",
        color: "success",
        timeout: 3000,
      });
    } else {
      lockValue.value = !lockValue.value;
      instance.toast.show({
        message: "Failed to Unlock User",
        color: "error",
        timeout: 3000,
      });
    }
  } catch (error) {
    lockValue.value = !lockValue.value;
    instance.toast.show({
      message: "An error occurred",
      color: "error",
      timeout: 3000,
    });
  } finally {
    lockLoading.value = false;
  }
};
</script>

<style scoped>
.field-section {
  font-weight: 900;
}

.field-label {
  font-size: 12px;
  font-weight: 600;
  color: #065695;
  margin-bottom: 4px;
  display: block;
}

.field-value {
  font-size: 14px;
  font-weight: 900;
  color: #333;
  margin: 0;
  word-wrap: break-word;
}

.checkbox-section {
  display: flex;
  flex-direction: row;
  gap: 12px;
  align-items: center;
}

.checkbox-container {
  position: relative;
  display: flex;
  align-items: center;
}

.checkbox-loader {
  position: absolute;
  right: -20px;
  top: 50%;
  transform: translateY(-50%);
}

.loading-text {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 13px;
  font-weight: 500;
  color: black;
}

.custom-lock-indicator {
  width: 1.1em;
  height: 1.1em;
  background: #dfdfdf;
  border: 2px solid #9e9e9e;
  border-radius: 3px;
}

.custom-lock-indicator-active {
  width: 1.2em;
  height: 1.2em;
  background: #065695;
  border: 2px solid #065695;
  border-radius: 3px;
  position: relative;
}

.custom-lock-indicator-active::after {
  content: "";
  position: absolute;
  top: 2px;
  left: 4px;
  width: 6px;
  height: 8px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.loading-state {
  opacity: 0.7;
  pointer-events: none;
  position: relative;
}

.loading-state::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(2, 138, 249, 0.1),
    transparent
  );
  animation: shimmer 1.5s infinite;
  z-index: 1;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.v-card {
  transition: box-shadow 0.2s ease-in-out;
  border-radius: 10px !important;

  /* Entrance animation */
  animation: fadeSlideUp 0.45s ease-out both;
}

.v-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

@keyframes fadeSlideUp {
  from {
    opacity: 0;
    translate: 0 14px;
  }
  to {
    opacity: 1;
    translate: 0 0;
  }
}

:deep(.v-checkbox .v-label) {
  font-size: 13px;
  font-weight: 500;
}

:deep(.v-checkbox .v-selection-control__input) {
  color: #065391;
}

:deep(.v-checkbox .v-selection-control__wrapper) {
  color: #065391;
}

:deep(.mdi-checkbox-blank-outline .v-icon) {
  height: 0.5em;
  width: 0.5em;
}

:deep(.mfa-checkbox .mdi-checkbox-blank-outline) {
  color: #9e9e9e;
  background-color: #fff;
  border-radius: 3px;
  border: 3px solid #fff;
}

.confirm-btn {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%) !important;
  color: white !important;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2) !important;
  font-weight: 800;
  /* border: 1px solid #065695 !important; */
}

.confirm-btn:hover {
  background: linear-gradient(180deg, #054a82 0%, #2070b0 100%) !important;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3) !important;
}

.cancel-btn {
  /* border: 1px solid #9e9e9e !important; */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15) !important;
  color: #065695 !important;
  font-weight: 800;
  /* color: #666 !important; */
}

.cancel-btn:hover {
  /* border-color: #666 !important; */
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2) !important;
  /* background-color: rgba(0, 0, 0, 0.04) !important; */
}

.dialog-title {
  text-align: center !important;
  justify-content: center !important;
  position: relative !important;
}

.close-btn {
  position: absolute !important;
  right: 8px !important;
  top: 50% !important;
  transform: translateY(-50%) !important;
  color: #666 !important;
}

.close-btn:hover {
  color: #333 !important;
  background-color: rgba(0, 0, 0, 0.04) !important;
}

.confirmation-text {
  font-family: Poppins !important;
  font-weight: 400 !important;
  font-style: normal !important;
  font-size: 16px !important;
  line-height: 140% !important;
  letter-spacing: 0% !important;
  background: linear-gradient(
    92.72deg,
    rgba(121, 121, 121, 0.9) 0%,
    rgba(187, 187, 187, 0.9) 152.21%
  ) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
  text-align: left !important;
  white-space: pre-line !important;
  margin-bottom: 10px;
}

:deep(.v-checkbox .v-label) {
  font-size: 13.5px;
  font-weight: 500;
  color: black;
}
</style>
