<template>
  <template
    v-for="(item, idx) in store.state.meetingStore.materialFlowButton"
    :key="idx"
  >
    <v-btn
      v-if="item.buttonLabel.toLowerCase() == 'send'"
      :loading="isLoading"
      class="mr-4 rounded-lg font-weight-bold primary-gradient"
      width="120"
      @click="openModalPenyetuju(item)"
    >
      {{ item.buttonLabel }}
    </v-btn>
    <v-btn
      v-else-if="item.buttonLabel.toLowerCase() == 'approve'"
      :loading="isLoading"
      class="mr-4 rounded-lg font-weight-bold primary-gradient"
      width="120"
      @click="action(item)"
    >
      {{ item.buttonLabel }}
    </v-btn>
    <v-btn
      v-else-if="item.buttonLabel.toLowerCase() == 'reject'"
      :loading="isLoading"
      class="mr-4 rounded-lg font-weight-bold primary-red-gradient"
      width="120"
      @click="action(item)"
    >
      {{ item.buttonLabel }}
    </v-btn>
  </template>
  <v-dialog
    max-width="800"
    v-model="modalSend"
    transition="dialog-bottom-transition"
    persistent
  >
    <v-card class="py-3 px-6 rounded-12">
      <v-card-title class="d-flex justify-center align-center">
        <div class="text-18 text-blueTheme fw-500 mt-2 mb-2">Assign</div>
        <v-btn
          class="mr-2"
          style="position: absolute; right: 0"
          variant="text"
          icon="mdi-close"
          @click="modalSend = false"
        ></v-btn>
      </v-card-title>
      <div class="separatorHorizontalGradient"></div>
      <v-form @submit.prevent="sendModalPenyutu" class="mt-4">
        <SearchBar
          v-model="sendId"
          v-model:search="search"
          :items="assignList"
          :appendIcon="true"
        />
        <div class="d-flex justify-end mt-4">
          <v-btn
            type="submit"
            class="rounded-lg font-weight-bold primary-gradient"
          >
            Send
          </v-btn>
        </div>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script lang="ts" setup>
import SearchBar from "@v2/components/utils/dialog/SearchBar.vue";
import { ref, watch, onMounted, getCurrentInstance } from "vue";
import { TSelect } from "@/v2/Type";
import { useRoute } from "vue-router";
import { useStore } from "vuex";
import { responsePromise } from "@v2/helpers/utils";

const emit = defineEmits<{ (e: "update", value: boolean): void }>();

const { root } = getCurrentInstance() as any;
const response = responsePromise(root);
const prop = defineProps({
  idDoc: {
    type: String,
    required: true,
  },
});

const store = useStore();
const route = useRoute();

//approval
const modalSend = ref<boolean>(false);
const search = ref<string | null>(null);
const sendId = ref(null);
const assignList = ref<any[]>([]);
const formData = ref<any>({});
const isLoading = ref<boolean>(false);

function openModalPenyetuju(item: any) {
  formData.value = item;
  modalSend.value = true;
}

function sendModalPenyutu() {
  formData.value.userApproval = sendId.value;
  submitForm();
}

function action(item: any) {
  formData.value = item;
  submitForm();
}

function submitForm() {
  isLoading.value = true;
  store
    .dispatch("meetingStore/sendPenyetuju", formData.value)
    .then((res) => {
      response.success(res, function () {
        emit("update", true);
        fetchFlowButton();
        modalSend.value = false;
      });
    })
    .catch(response.error)
    .finally(() => {
      isLoading.value = false;
    });
}

function featchPenyetujuList(name: any) {
  const { materialListDocId } = store.state.meetingStore.materialMetadata;

  const payload = {
    name: name,
    idEvent: route.params.idEvent,
    idMEventDocPresentationMaterialTemplate: materialListDocId,
  };
  store
    .dispatch(
      "materialStore/searchEventPresentationMaterialByUsername",
      payload
    )
    .then((resp: TSelect[]) => {
      assignList.value = resp;
    });
}

function fetchFlowButton() {
  isLoading.value = true;
  store
    .dispatch("meetingStore/getMaterialFlowButton", prop.idDoc)
    .finally(() => {
      isLoading.value = false;
    });
}

onMounted(() => {
  fetchFlowButton();
});

watch(
  () => search.value,
  (val) => {
    featchPenyetujuList(val);
  }
);
</script>
