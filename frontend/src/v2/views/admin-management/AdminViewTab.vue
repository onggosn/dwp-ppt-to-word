<template>
  <div v-if="!modeSearch" class="pt-3 pl-6">
    <BannerAdmin />
  </div>
  <div class="pl-6 pt-3 pb-3 align-center mx-6">
    <div v-if="!modeSearch" class="item-card pt-8">
      <div
        class="d-flex justify-space-between align-center flex-wrap"
        style="gap: 12px"
      >
        <v-tabs
          id="admin-tab"
          v-model="activeTab"
          hide-slider
          :class="{ 'tabs-small': isSmallScreen }"
        >
          <v-tab
            :to="{ name: 'meeting-admin-meeting' }"
            class="tab-header"
            v-if="isMeeting"
          >
            Meeting
          </v-tab>
          <v-tab
            :to="{ name: 'content-admin-predefine' }"
            class="tab-header"
            v-if="isContent"
          >
            Content
          </v-tab>
          <v-tab
            :to="{ name: 'role-admin-user' }"
            class="tab-header"
            v-if="isRole"
          >
            Role
          </v-tab>
          <v-tab
            :to="{ name: 'operasional-admin' }"
            class="tab-header"
            v-if="isOperational"
          >
            Operasional
          </v-tab>
          <v-tab :to="{ name: 'faq-admin' }" class="tab-header" v-if="isFAQ">
            FAQ
          </v-tab>
          <v-tab
            :to="{ name: 'notification-admin' }"
            class="tab-header"
            v-if="isNotification"
          >
            Notification
          </v-tab>
        </v-tabs>

        <div
          :class="[
            'd-flex align-center flex-wrap flex-shrink-0 ml-auto buttons-container',
            { 'small-buttons': isSmallScreen },
          ]"
          style="gap: 6px"
        >
          <ButtonAddMeeting
            v-if="route.name == 'meeting-admin-meeting'"
            @onSuccess="reloadContent"
          />
          <FormCreateContent
            v-if="route.name === 'content-admin-predefine'"
            @onSuccess="reloadContent"
          />
          <FormCreateAdg
            v-if="route.name === 'role-admin-adg' && isAdg"
            @onSuccess="reloadContent"
          />
          <FormCreateFAQ
            v-if="route.name === 'faq-admin'"
            @onSuccess="reloadContent"
          />
          <AddPresentationMaterial
            v-if="
              route.name == 'meeting-admin-presentation-material' &&
              isAddMeetingPredefineMaterial
            "
            @onSuccess="reloadContent"
          />
          <DropDownDownload
            v-if="
              route.name === 'content-admin-predefine' ||
              route.name == 'role-admin-user'
            "
          />
          <FilterButton
            v-if="
              !route.path.includes('operasional') &&
              route.name !== 'notification-admin' &&
              route.name !== 'role-admin-adg'
            "
            @update="updateFilter"
          ></FilterButton>
          <SortingButton
            v-if="
              !route.path.includes('operasional') &&
              route.name !== 'notification-admin' &&
              route.name !== 'role-admin-adg'
            "
            :items="sortType"
            @update="updateSort"
          />

          <SearchButton
            v-if="route.name !== 'role-admin-adg'"
            @update="updateSearchFilter"
          />
        </div>
      </div>
    </div>

    <div class="mt-5">
      <router-view />
    </div>
  </div>
</template>

<script lang="ts" setup>
import BannerAdmin from "@/v2/components/admin/BannerAdmin.vue";
import SortingButton from "@/v2/components/admin/sort/SortingButton.vue";
import FilterButton from "@/v2/components/admin/FilterButton.vue";
import SearchButton from "@/v2/components/search/SearchButton.vue";
import FormCreateContent from "@/v2/components/admin/content/FormCreate.vue";
import FormCreateAdg from "@/v2/components/admin/role/FormCreate.vue";
import FormCreateFAQ from "@/v2/components/admin/faq/FormCreateFAQ.vue";
import DropDownDownload from "@/v2/components/admin/DropDownDownload.vue";
import ButtonAddMeeting from "@/v2/components/admin/meeting/AddMeeting.vue";
import AddPresentationMaterial from "@/v2/components/admin/meeting/AddPresentationMaterial.vue";
import { secureRandomFloat } from "@/v2/helpers/utils";
import { TListSortingType } from "@/v2/Type";
import { SearchRouteName } from "@/v2/enum/Search";
import { useStore } from "vuex";
import { ref, onMounted, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useDisplay } from "vuetify";
import _ from "lodash";

const store = useStore();
const route = useRoute();
const router = useRouter();
const { width } = useDisplay();

const activeTab = ref(0);
const isSmallScreen = computed(() => width.value <= 1400);

const sortType = ref<TListSortingType[]>([]);
const isContent = ref(true);
const isTypeOngoing = ref(false);
const isAddMeetingPredefineMaterial = ref(false);
const isMeetingPredefineMaterial = ref(false);
const isMeeting = ref(true);
const isRole = ref(false);
const isOperational = ref(false);
const isFAQ = ref(false);
const isNotification = ref(false);
const isAdg = ref(false);
const modeSearch = computed(() => store.getters["globalStore/getStatusSearch"]);

const getListSortingType = () => {
  let payload = {
    id: ["content-admin-ongoing", "faq-admin"].includes(route.name as string)
      ? 2
      : 1,
  };

  store.dispatch("adminStore/getListSortingType", payload).then((res) => {
    const data = res.responseData;
    sortType.value = data[0]?.value;
  });
};

const getAdminTabMenu = () => {
  store.dispatch("adminStore/getAdminTabMenu").then((res) => {
    isTypeOngoing.value = res.isOnGoingAccess;
    isContent.value = res.isContent;
    isMeeting.value = res.isMeeting;
    isAddMeetingPredefineMaterial.value = res.isAddMeetingPredefineMaterial;
    isMeetingPredefineMaterial.value = res.isMeetingPredefineMaterial;
    isRole.value = res.isRole;
    isOperational.value = res.isOperational;
    isFAQ.value = res.isFAQ;
    isNotification.value = res.isNotification;
    isAdg.value = res.isAdg;
    const routeData = [
      {
        id: 0,
        name: "content-admin-predefine",
        isActive: isContent.value,
      },
      {
        id: 1,
        name: "meeting-admin-meeting",
        isActive: isMeeting.value,
      },
      {
        id: 2,
        name: "role-admin",
        isActive: isRole.value,
      },
      {
        id: 3,
        name: "operasional-admin",
        isActive: isOperational.value,
      },
    ];
    routeRedirectFirst(routeData);
    store.commit(
      "adminStore/setIsAddMeetingPredefineMaterial",
      isAddMeetingPredefineMaterial.value
    );
    store.commit(
      "adminStore/setIsMeetingPredefineMaterial",
      isMeetingPredefineMaterial.value
    );
    store.commit("adminStore/setTypeOngoing", isTypeOngoing.value);
    store.commit("adminStore/setAdgAccess", isAdg.value);
  });
};

function routeRedirectFirst(routeData) {
  const firstActiveRoute = routeData.find((item) => item.isActive === true);
  if (firstActiveRoute) {
    router.push({ name: firstActiveRoute.name });
  }
}

function load() {
  getListSortingType();
  getAdminTabMenu();
}

onMounted(() => {
  store.commit("globalStore/setStatusSearch", false);
  store.commit("globalStore/setSearch", "");
  load();
});

function updateSort(sortId) {
  router.replace({
    query: _.assign({}, route.query, {
      eventSort: sortId,
    }),
  });
}

function reloadContent() {
  store.commit("adminStore/setRefreshList", secureRandomFloat());
}

function updateFilter(item) {
  store.commit("adminStore/setItemsFilter", item);
}

function updateSearchFilter(item) {
  const routeName = route.name ? SearchRouteName[route.name] : undefined;
  if (item && routeName) {
    router.push({ name: routeName });
  }
  store.commit("globalStore/setStatusSearch", item);
}

watch(
  () => route.path,
  (newValue) => {
    if (!newValue.includes("search")) {
      store.commit("globalStore/setStatusSearch", false);
      store.commit("globalStore/setSearch", "");
    }
    getListSortingType();
  }
);
</script>

<style scoped>
.v-input__control {
  border-radius: 16px;
  height: 10px;
}
.item-card {
  padding: 23px 30px;
  background-color: rgba(255, 255, 255, 1);

  /* Shadow 1 */
  border-radius: 16px;
  box-shadow: 0px 3px 10px 0px rgba(0, 0, 0, 0.12);
}
:deep(.tab-header.v-slide-group-item--active) {
  background-color: #f44336 !important;
  color: #ffff !important;
  border: none !important;
  border-radius: 12px;
  background-clip: border-box;
  -webkit-background-clip: border-box !important;
}
.tab-header {
  color: #065695;
  font-weight: 600;
  max-height: 40px;
}
.btn-add {
  display: flex;
  height: 36px;
  color: #ffff;
  padding: 8px 14px;
  align-items: flex-end;
  justify-content: flex-end;
  border-radius: 8px;
  background: var(
    --Gradient-Blue,
    linear-gradient(180deg, #065695 0%, #267dc2 100%)
  );
}

.small-buttons :deep(.v-btn) {
  height: 32px !important;
  min-height: 32px !important;
  font-size: 13px !important;
  padding: 0 12px !important;
}

.small-buttons :deep(.v-btn__content .v-icon),
.small-buttons :deep(.v-btn__content img) {
  font-size: 16px !important;
  width: 16px !important;
  height: 16px !important;
}

.tabs-small :deep(.v-tab) {
  font-size: 13px !important;
  min-width: auto !important;
  padding: 0 12px !important;
}
</style>

<!-- /* UNSCOPED Styles */ -->
<style>
#admin-tab {
  & .v-slide-group__content {
    align-items: center;
  }
}
</style>
