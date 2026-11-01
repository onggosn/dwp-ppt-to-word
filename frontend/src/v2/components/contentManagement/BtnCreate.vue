<template>
  <v-menu transition="slide-y-transition" :disabled="!isCanAccess">
    <template v-slot:activator="{ props }">
      <v-btn
        v-bind="props"
        density="default"
        icon="mdi-plus"
        rounded="lg"
        size="x-small"
        class="primary-gradient"
        style="color: white"
        color="light-blue-darken-3"
        :disabled="!isCanAccess"
        @click="load"
      ></v-btn>
    </template>
    <v-list>
      <!-- wait get id bp finish -->
      <template v-if="!isGetIdBpFinished">
        <v-list-item style="color: #3a416f" class="px-4">
          <v-list-item-title>
            <free-style-shimmer
              v-for="n in 3"
              class="px-2 py-1"
              :key="n"
              height="40px"
              width="15vw"
              border-radius="5px"
              color="#DCDCDC"
              @click.stop
            />
          </v-list-item-title>
        </v-list-item>
      </template>
      <v-list-item v-if="isGetIdBpFinished">
        <v-list-item-title
          v-for="item in listItem"
          :key="item.idBp"
          class="px-4 py-2 item"
          style="cursor: pointer"
          @click="handleCreate(item)"
        >
          {{ item.name }}
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>

  <CreateAIU ref="dialogAIU" @refreshToc="handleRefreshToc" />
  <CreatePNIN ref="dialogPN" title="Add Policy Note" :id-bp="idBpPolicy" />
  <CreatePNIN ref="dialogIN" title="Add Issue Note" :id-bp="idBpIssue" />
</template>
<script lang="ts" setup>
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import CreateAIU from "@v2/components/contentManagement/CreateAIU.vue";
import CreatePNIN from "@v2/components/contentManagement/CreatePNIN.vue";
import { ref, computed, getCurrentInstance } from "vue";
const { root } = getCurrentInstance() as any;

const dialogAIU = ref();
const dialogPN = ref();
const dialogIN = ref();
const isLoading = ref<boolean>(false);
const listItem = ref<any[]>([]);
const store = useStore();
const route = useRoute();

const idEvent = computed((): string => route.params.idEvent as string);
const idBpPolicy = computed(() => {
  const detail = store.state.meetingStore.meetingSummary;
  return { ...detail.policyNote }.idBp;
});

const idBpIssue = computed(() => {
  const detail = store.state.meetingStore.meetingSummary;
  return { ...detail.issueNote }.idBp;
});

const idBpAIU = computed(() => {
  const detail = store.state.meetingStore.meetingSummary;
  return { ...detail.aiu }.idBp;
});

const isCanAccess = computed((): boolean => {
  const form = store.state.collaborationStore.formEditor ?? {};
  return (
    form.isManualAccess ||
    route.params.idDoc === "00000000-0000-0000-0000-000000000000"
  );
});

const isGetIdBpFinished = computed(() => {
  return idBpPolicy.value || idBpIssue.value || idBpAIU.value;
});

const emit = defineEmits(["refreshToc"]);

const handleRefreshToc = () => {
  emit("refreshToc");
};

const getIdbp = () => {
  isLoading.value = true;
  store
    .dispatch("meetingStore/fetchDashboardSummary", {
      idEvent: idEvent.value,
    })
    .catch((err) => {
      root.refs.toast.show({
        message: err.message ?? "Maaf, terjadi kesalahan sistem",
        color: "warning",
        timeout: 3000,
      });
    })
    .finally(() => {
      isLoading.value = false;
    });
};

const handleCreate = (type: { name: string; idBp: string }) => {
  if (type.name === "Analisis indikator utama") {
    store.dispatch("contentStore/getSectorList");
    dialogAIU.value.show();
  } else if (type.name === "Policy Note") {
    store.dispatch("contentStore/getSectorPNINList", type.idBp);
    dialogPN.value.show();
  } else if (type.name === "Issue Note") {
    store.dispatch("contentStore/getSectorPNINList", type.idBp);
    dialogIN.value.show();
  }
};

function load() {
  isLoading.value = true;

  store
    .dispatch("contentStore/getListContentCreate", idEvent.value)
    .then((response) => {
      listItem.value = response;
      getIdbp();
    })
    .finally(() => {
      isLoading.value = false;
    });
}
</script>
<style scoped>
.item:hover {
  background-color: #d6e6f5;
}
</style>
