<template>
  <div class="playground-view">
    <div v-if="!isAuthenticated">
      <v-container class="fill-height" fluid>
        <v-row justify="center" align="center" class="fill-height">
          <v-col cols="12" sm="8" md="6" lg="4" xl="3">
            <v-card class="auth-card" elevation="8">
              <v-card-title class="auth-title">
                <div class="text-center w-100">
                  <v-icon
                    icon="mdi-lock-outline"
                    size="48"
                    class="auth-icon mb-3"
                  />
                  <h2 class="text-h5 font-weight-bold">DDM Playground</h2>
                  <p class="text-subtitle-1 text-medium-emphasis mt-2">
                    Enter password to access this area
                  </p>
                </div>
              </v-card-title>

              <v-card-text class="auth-form">
                <div class="d-flex flex-column" style="width: 100%">
                  <v-form ref="authForm" @submit.prevent="handlePasswordSubmit">
                    <v-text-field
                      v-model="password"
                      label="Password"
                      type="password"
                      variant="outlined"
                      density="default"
                      prepend-inner-icon="mdi-key"
                      :error="!!errorMessage"
                      :loading="isLoading"
                      :disabled="isLoading"
                      class="mb-2"
                      @keyup.enter="handlePasswordSubmit"
                      @input="clearError"
                      autofocus
                      hide-details="auto"
                    />

                    <div v-if="errorMessage" class="error-message mb-4">
                      <v-alert
                        :text="errorMessage"
                        type="error"
                        density="compact"
                        variant="tonal"
                        class="text-body-2"
                      >
                        <template v-slot:prepend>
                          <v-icon size="small">mdi-alert-circle</v-icon>
                        </template>
                      </v-alert>
                    </div>

                    <v-btn
                      type="submit"
                      :loading="isLoading"
                      :disabled="!password || isLoading"
                      color="#065695"
                      size="large"
                      block
                      class="auth-button primary-gradient"
                    >
                      <v-icon icon="mdi-login" class="mr-2" />
                      Access Playground
                    </v-btn>
                  </v-form>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>

    <!-- Main Playground Content -->
    <div v-else class="playground-content">
      <v-container class="playground-container">
        <v-row justify="center" align="center" class="fill-height">
          <v-col cols="12" md="8" lg="6" xl="5">
            <v-card class="rounded-xl" elevation="2">
              <!-- Card Content -->
              <v-card-text class="card-content">
                <!-- Search Section -->
                <div class="search-section mb-6">
                  <h4 class="section-title mb-3">
                    <v-icon icon="mdi-magnify" size="20" class="mr-2" />
                    Search & Add Users
                  </h4>

                  <div class="search-container position-relative">
                    <SearchBar
                      placeHolderSearch="Search users"
                      type="global"
                      @selected="handleUserSelected"
                      :disabled="isAddingUser"
                    />
                  </div>

                  <!-- Search Info -->
                  <div class="search-info mt-2">
                    <v-chip size="small" variant="outlined" color="info">
                      <v-icon
                        icon="mdi-information-outline"
                        start
                        size="small"
                      />
                      Type at least 3 characters to search
                    </v-chip>
                    <v-chip
                      v-if="isAddingUser"
                      size="small"
                      variant="tonal"
                      color="warning"
                      class="ml-2"
                    >
                      <v-progress-circular
                        indeterminate
                        size="15"
                        width="3"
                        color="info"
                        class="mr-2"
                      />
                      Adding user...
                    </v-chip>
                  </div>
                </div>

                <!-- Users List Section -->
                <div class="users-list-section">
                  <div class="d-flex justify-space-between align-center mb-4">
                    <h4 class="section-title">
                      <v-icon icon="mdi-account-group" size="20" class="mr-2" />
                      Added Users ({{
                        isLoadingUsers ? "..." : selectedUsers.length
                      }})
                    </h4>

                    <!-- Action Buttons -->
                    <div class="d-flex gap-2">
                      <!-- Refresh Button -->
                      <v-btn
                        variant="outlined"
                        size="small"
                        color="info"
                        @click="refreshUsers"
                        :loading="isLoadingUsers"
                        prepend-icon="mdi-refresh"
                      >
                        Refresh
                      </v-btn>
                    </div>
                  </div>

                  <div v-if="isLoadingUsers" class="users-shimmer">
                    <v-card
                      v-for="i in 5"
                      :key="`shimmer-${i}`"
                      class="user-item-shimmer mb-3"
                      variant="outlined"
                      :style="{ animationDelay: `${(i - 1) * 0.08}s` }"
                    >
                      <v-card-text class="pa-4">
                        <div class="d-flex align-center">
                          <!-- Avatar Shimmer -->
                          <div class="shimmer-avatar mr-4"></div>

                          <!-- Content Shimmer -->
                          <div class="flex-grow-1">
                            <div class="shimmer-line shimmer-title mb-2"></div>
                            <div
                              class="shimmer-line shimmer-subtitle mb-1"
                            ></div>
                            <div class="shimmer-line shimmer-email"></div>
                          </div>

                          <!-- Actions Shimmer -->
                          <div class="d-flex gap-1">
                            <div class="shimmer-button"></div>
                            <div class="shimmer-button"></div>
                          </div>
                        </div>
                      </v-card-text>
                    </v-card>
                  </div>

                  <!-- Empty State -->
                  <div
                    v-else-if="selectedUsers.length === 0"
                    class="empty-state"
                  >
                    <v-card
                      variant="tonal"
                      color="grey-lighten-4"
                      class="pa-8 text-center"
                    >
                      <v-icon
                        icon="mdi-account-off"
                        size="64"
                        class="mb-4 text-grey"
                      />
                      <h4 class="text-grey-darken-1 mb-2">No Users Found</h4>
                      <p class="text-grey">
                        No users are currently in the system. Add users using
                        the search bar above.
                      </p>
                    </v-card>
                  </div>

                  <!-- Users List -->
                  <div v-else class="users-list">
                    <v-card
                      v-for="(user, index) in selectedUsers"
                      :key="user.id"
                      class="user-item mb-3"
                      variant="outlined"
                      hover
                      :style="{ animationDelay: `${index * 0.08}s` }"
                    >
                      <v-card-text>
                        <div class="d-flex align-center">
                          <v-avatar size="50" class="mr-2">
                            <v-icon
                              icon="mdi-account-circle"
                              size="40"
                            ></v-icon>
                          </v-avatar>

                          <!-- User Info -->
                          <div class="user-info flex-grow-1">
                            <div class="d-flex align-center mb-1">
                              <h5 class="user-name">{{ user.value }}</h5>
                              <v-chip
                                v-if="user.isGroup"
                                size="x-small"
                                color="primary"
                                variant="outlined"
                                class="ml-2"
                              >
                                Group
                              </v-chip>
                              <v-chip
                                v-else
                                size="x-small"
                                color="success"
                                variant="outlined"
                                class="ml-2"
                              >
                                User
                              </v-chip>

                              <v-chip
                                v-if="user.status"
                                size="x-small"
                                :color="
                                  user.status === 'active'
                                    ? 'success'
                                    : 'warning'
                                "
                                variant="tonal"
                                class="ml-2"
                              >
                                {{ user.status }}
                              </v-chip>
                            </div>

                            <!-- Organization/Email -->
                            <p
                              v-if="
                                user.organizationName &&
                                user.organizationName !== 'N/A'
                              "
                              class="user-org text-caption"
                            >
                              <v-icon
                                icon="mdi-office-building"
                                size="small"
                                class="mr-1"
                              />
                              {{ user.organizationName }}
                            </p>
                            <p
                              v-if="user.inputEmail"
                              class="user-email text-caption"
                            >
                              <v-icon
                                icon="mdi-email"
                                size="small"
                                class="mr-1"
                              />
                              {{ user.inputEmail }}
                            </p>
                          </div>
                        </div>
                      </v-card-text>
                    </v-card>
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, getCurrentInstance } from "vue";
import SearchBar from "@/v2/components/collaboration/SearchBar.vue";
import { useStore } from "vuex";
const { root } = getCurrentInstance() as any;

// Authentication state
const isAuthenticated = ref(false);
const password = ref("");
const errorMessage = ref("");
const isLoading = ref(false);
const store = useStore();

// Correct password
const CORRECT_PASSWORD = "M4nt4p";

const selectedUsers = ref([]);
const isLoadingUsers = ref(false);
const isAddingUser = ref(false);

// Authentication methods
const handlePasswordSubmit = async () => {
  if (!password.value) {
    errorMessage.value = "Password is required";
    return;
  }

  isLoading.value = true;
  errorMessage.value = "";

  if (password.value === CORRECT_PASSWORD) {
    isAuthenticated.value = true;
    password.value = "";
    await getList();
  } else {
    errorMessage.value = "Invalid password. Please try again.";
    password.value = "";
  }

  isLoading.value = false;
};

const clearError = () => {
  errorMessage.value = "";
};

const getList = async () => {
  isLoadingUsers.value = true;

  try {
    const resp = await store.dispatch(
      "adminStore/mappingPasswordManualGetList"
    );

    if (resp.responseData.data) {
      selectedUsers.value = resp.responseData.data.map((user, index) => ({
        id: user.id || `user_${index}`,
        value:
          user.username || user.name || user.displayName || `User ${index + 1}`,
        username: user.username,
        inputEmail: user.email || user.inputEmail,
        isGroup: user.isGroup || false,
        organizationName: user.organizationName || user.organization || "N/A",
        addedAt: user.createdAt || user.addedAt || new Date().toISOString(),
        lastLogin: user.lastLogin,
        status: user.status || "active",
        role: user.role || "user",
      }));
    } else {
      selectedUsers.value = [];
    }
  } catch (error) {
    selectedUsers.value = [];
    root.refs.toast.show({
      message: "Failed to load user list",
      color: "error",
      timeout: 3000,
    });
  } finally {
    isLoadingUsers.value = false;
  }
};

// User management methods
const handleUserSelected = async (user) => {
  // Check if user already exists
  const existingUser = selectedUsers.value.find((u) => u.id === user.id);
  if (existingUser) {
    root.refs.toast.show({
      message: "User already added to the list",
      color: "error",
      timeout: 3000,
    });
    return;
  }

  isAddingUser.value = true;

  try {
    // Add user to selected list
    const resp = await store.dispatch(
      "adminStore/mappingPasswordManualLoginAdd",
      {
        username: user.username,
      }
    );

    if (resp.responseCode === "011000") {
      root.refs.toast.show({
        message: `${user.isGroup ? "Group" : "User"} "${
          user.value
        }" added successfully`,
        color: "success",
        timeout: 3000,
      });

      await getList();
    } else {
      throw new Error("Failed to add user - Invalid response");
    }
  } catch (error) {
    root.refs.toast.show({
      message: `Failed to add "${user.value}". Please try again.`,
      color: "error",
      timeout: 3000,
    });
  } finally {
    isAddingUser.value = false;
  }
};

const refreshUsers = async () => {
  await getList();
};
</script>

<style lang="scss" scoped>
:deep(.v-container) {
  min-height: 80vh;
}
.auth-card {
  border-radius: 16px !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
}

.auth-title {
  padding: 32px 24px 16px !important;
  text-align: center;
}

.auth-icon {
  color: #667eea;
}

.auth-form {
  padding: 16px 32px 32px !important;
}

.auth-button {
  border-radius: 12px !important;
  height: 48px !important;
  font-weight: 600 !important;
  text-transform: none !important;
}

// Playground Styles
.playground-content {
  min-height: 100vh;
  background: #f8fafc;
}

.playground-header {
  background: white;
  padding: 24px 32px;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.playground-title {
  font-size: 2rem;
  font-weight: 700;
  color: #065695;
  margin: 0;
}

.playground-subtitle {
  color: #64748b;
  font-size: 1rem;
  margin: 8px 0 0 0;
}

.playground-container {
  height: 80vh;
  padding: 24px !important;
}

.playground-menu {
  border-radius: 12px !important;

  .v-list-item {
    border-radius: 8px !important;
    margin: 4px 8px !important;

    &.v-list-item--active {
      background: linear-gradient(135deg, #065695 0%, #267dc2 100%) !important;
      color: white !important;

      .v-list-item-title,
      .v-icon {
        color: white !important;
      }
    }
  }
}

.playground-workspace {
  border-radius: 12px !important;
  min-height: 600px;
}

.workspace-content {
  padding: 24px !important;
}

.section-content {
  h3 {
    color: #065695;
    font-weight: 600;
  }
}

.sql-result {
  background: #1e293b;
  color: #e2e8f0;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  font-family: "Consolas", "Monaco", "Courier New", monospace;
}

.users-shimmer {
  .user-item-shimmer {
    border-radius: 12px !important;

    .v-skeleton-loader {
      background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
      background-size: 200% 100%;
      animation: shimmer 1.5s infinite;
    }
  }
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.user-item {
  .user-last-login {
    color: #9ca3af;
    margin: 2px 0 0 0;
    display: flex;
    align-items: center;
  }
}

.gap-2 {
  gap: 8px !important;
}

// Responsive
@media (max-width: 768px) {
  .auth-form {
    padding: 16px 24px 24px !important;
  }

  .playground-header {
    padding: 16px;
    text-align: center;

    .d-flex {
      flex-direction: column;
      gap: 16px;
    }
  }

  .playground-title {
    font-size: 1.5rem;
  }

  .playground-container {
    padding: 16px !important;
  }
}

.text-medium-emphasis {
  color: rgba(0, 0, 0, 0.6) !important;
}

.gap-2 {
  gap: 8px !important;
}

.w-100 {
  width: 100% !important;
}

@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(18px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.user-item-shimmer,
.user-item {
  animation: fadeSlideUp 0.6s ease-out both;
  border-radius: 12px !important;
}

.user-item {
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1) !important;
  }
}

.users-shimmer {
  .shimmer-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
  }

  .shimmer-line {
    height: 12px;
    border-radius: 6px;
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
  }

  .shimmer-title {
    width: 160px;
    height: 16px;
  }

  .shimmer-subtitle {
    width: 100px;
    height: 12px;
  }

  .shimmer-email {
    width: 120px;
    height: 12px;
  }

  .shimmer-button {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
  }
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.user-item {
  .user-avatar {
    border: 2px solid #e2e8f0;
  }

  .user-name {
    font-weight: 600;
    color: #065695;
    margin: 0;
  }

  .user-org,
  .user-email,
  .user-last-login {
    color: #64748b;
    margin: 2px 0 0 0;
    display: flex;
    align-items: center;
  }

  .user-actions {
    display: flex;
    gap: 4px;
  }
}

.gap-2 {
  gap: 8px !important;
}
</style>
