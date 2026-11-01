<template>
  <div>
    <div class="d-flex justify-end mr-4 mt-3" style="gap: 10px">
      <template v-if="isOrder">
        <v-btn
          elevation="3"
          size="small"
          class="font-weight-bold btn-danger"
          style="border-radius: 10px; cursor: pointer"
          @click="cancelOrder"
        >
          Cancel
          <v-tooltip activator="parent" location="top"> Cancel </v-tooltip>
        </v-btn>
        <v-btn
          elevation="3"
          size="small"
          class="font-weight-bold primary-gradient"
          style="border-radius: 10px; cursor: pointer"
          @click="saveOrder"
        >
          Save
          <v-tooltip activator="parent" location="top"> Save </v-tooltip>
        </v-btn>
      </template>
      <div class="d-flex" style="gap: 10px">
        <v-btn
          v-if="canPublish"
          variant="outlined"
          size="small"
          color="#00783E"
          class="font-weight-bold"
          style="border: 1px solid; border-radius: 10px; cursor: pointer"
          :disabled="disableAdd || !canPublish"
          @click="openDialog()"
        >
          <v-icon small>mdi-access-point</v-icon>
          Publish Agenda
          <v-tooltip activator="parent" location="top"
            >Publish Agenda</v-tooltip
          >
        </v-btn>
        <v-btn
          v-if="canAdd"
          variant="outlined"
          size="small"
          :disabled="disableAdd"
          color="#267DC2"
          class="font-weight-bold"
          style="border: 1px solid; border-radius: 10px; cursor: pointer"
          @click="opendAddDialog"
        >
          <v-icon small>mdi-plus</v-icon>
          Add Agenda
          <v-tooltip activator="parent" location="top">Add Agenda</v-tooltip>
        </v-btn>
        <v-btn
          v-if="canOrder"
          variant="outlined"
          size="small"
          class="font-weight-bold"
          style="border: 1px solid; border-radius: 10px; cursor: pointer"
          @click="startOrder"
          color="#267DC2"
          :disabled="!canOrder"
        >
          <v-icon small>mdi-swap-vertical</v-icon>
          Change Order
          <v-tooltip activator="parent" location="top">Change Order</v-tooltip>
        </v-btn>
      </div>
    </div>

    <ListAgenda
      v-model="list"
      :isDraggable="isOrder"
      :isParticipant="canStartAgenda"
      :status-mode="statusMode"
      :loading="isLoading"
      @edit="opendEditDialog"
      @delete="showDelete"
      @set-time="handleStartAgenda"
      @set-stop-time="handleStopAgenda"
    />
  </div>

  <ModalConfirm
    ref="modalPublish"
    :form-config="formPublish"
    @action-confirm="onSubmit()"
  >
    <template v-slot:icon-img>
      <v-avatar
        color="white"
        size="80"
        style="margin-top: -60px; filter: drop-shadow(#9b9b9b 2px 2px 3px)"
      >
        <img
          src="/images/checkNotif2.png
          "
          style="width: 75px"
        />
      </v-avatar>
    </template>
  </ModalConfirm>

  <EditDialog
    v-if="editDialogVisibility"
    :type="modalType"
    :visible="editDialogVisibility"
    :id="idEdit"
    :date="dateAgenda"
    :editStatus="statusEdit"
    :title="modalType === 'edit' ? 'Edit Agenda' : 'Add Agenda'"
    :dateStart="meetingData.eventstart"
    @close="closeEditDialog()"
    @refetch="updateData()"
  />

  <ModalConfirm
    ref="modal"
    :form-config="formDelete"
    @action-confirm="deleteAgenda"
  />
</template>

<script setup lang="ts">
import { ref, getCurrentInstance, onMounted, computed } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";

import { responsePromise } from "@v2/helpers/utils";

import { TAgendaList, TResponseBase, TModalConfirm } from "@v2/Type.d";

import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import ListAgenda from "@/v2/components/agenda/ListAgenda.vue";
import EditDialog from "@/v2/components/agenda/EditAgendaDialog.vue";

type TResponseAgenda = TResponseBase<TAgendaList[]> & {
  responseData: {
    isPublish: boolean;
    isAdd: boolean;
    isOrder: boolean;
    data: TAgendaList[];
    isOrganizer: boolean;
  };
};

const { root } = getCurrentInstance() as any;
const response = responsePromise(root);
const store = useStore();
const route = useRoute();
const idEvent = route.params.idEvent as string;

const modalPublish = ref();

const list = ref<TAgendaList[]>([]);
const orderList = ref<TAgendaList[]>([]);

const isLoading = ref<boolean>(false);
const editDialogVisibility = ref<boolean>(false);
const isOrder = ref<boolean>(false);
const canPublish = ref<boolean>(false);
const canStartAgenda = ref<boolean>(false);
const canOrder = ref<boolean>(false);
const canAdd = ref<boolean>(false);
const dateAgenda = ref<string>("");
const modalType = ref<"edit" | "add">("edit");
const statusMode = ref<number>(0);
const isDisableAllButton = computed(
  () => store.getters["meetingStore/getModeDisableBtn"]
);

//modal delete
const modal = ref();
const formDelete = ref<TModalConfirm>({
  title: "Delete Agenda",
  message: "Are you sure delete this Agenda ? ",
  btnSubmitLabel: "Yes",
  usingTimeOut: true,
});

const formPublish = ref<TModalConfirm>({
  title: "Publish Agenda",
  btnSubmitLabel: "Yes",
  width: 450,
  btnSubmitColor: "primary-gradient",
  message: "Are you sure to publish this agenda?",
  messageClass: "text-left",
});

const emit = defineEmits<{
  (e: "refresh", value: unknown);
}>();

const meetingData = computed((): any => {
  return store.state.meetingStore.meetingItem ?? {};
});

const load = () => {
  store
    .dispatch("meetingStore/fetchAgendaById", idEvent)
    .then((response: TResponseAgenda) => {
      list.value = response.responseData?.data;
      canStartAgenda.value = response.responseData.isOrganizer ?? false;
      canPublish.value = response.responseData.isPublish ?? false;
      canOrder.value = response.responseData.isOrder ?? false;
      canAdd.value = response.responseData.isAdd ?? false;
    });
};

const onSubmit = () => {
  store
    .dispatch("meetingStore/publishMeetingAgenda", idEvent)
    .then((res) => {
      response.success(res, function () {
        load();
        onClose();
      });
    })
    .catch(response.error);
};

// delete agenda
const deleteAgenda = () => {
  store
    .dispatch("meetingStore/deleteAgenda", {
      id: idEdit.value,
    })
    .then((res) => {
      response.success(res, function () {
        load();
        emit("refresh", true);
        modal.value.hide();
      });
    })
    .catch(response.error);
};

onMounted(() => {
  store.commit("meetingStore/setModeDisableBtn", false);
  load();
});

const updateData = () => {
  load();
  emit("refresh", true);
};

// modals start
const openDialog = () => {
  modalPublish.value.show({});
};

const onClose = () => {
  modalPublish.value.hide({});
};

const idEdit = ref<string>("");
const statusEdit = ref<string>("");

const opendEditDialog = (value) => {
  modalType.value = "edit";
  idEdit.value = value.id;
  dateAgenda.value = value.date;
  statusEdit.value = value.status;
  editDialogVisibility.value = true;
};

const opendAddDialog = () => {
  modalType.value = "add";
  //dateMeeting = meetingData.value.eventstart;
  editDialogVisibility.value = true;
  statusEdit.value = "Waiting";
};

const closeEditDialog = () => {
  editDialogVisibility.value = false;
};

function showDelete(id: string) {
  idEdit.value = id;
  modal.value.show({}, 10);
}

function handleStartAgenda(temp) {
  const now = new Date();
  const intervalTime = parseInt(temp.intervalTime) || 10;

  const endDate = new Date(now);
  endDate.setMinutes(now.getMinutes() + intervalTime);

  const request = {
    idEventAgenda: temp.id,
    startTime: now.toLocaleString("sv-SE").replace(" ", "T"),
    endTime: endDate.toLocaleString("sv-SE").replace(" ", "T"),
  };
  store
    .dispatch("meetingStore/submitSetAgenda", request)
    .then((res) => {
      response.success(res, function () {
        // isOrder.value = false;
        load();
        emit("refresh", true);
      });
    })
    .catch(response.error);
}

const disableAdd = computed(() => isDisableAllButton.value);

function handleStopAgenda(temp) {
  isLoading.value = true;
  const now = new Date();
  const [day, month, year] = temp.date.split("/").map(Number);
  const [hours, minutes] = temp.startTime.split(":").map(Number);

  const startDate = new Date(year, month - 1, day, hours, minutes);

  const request = {
    idEventAgenda: temp.id,
    startTime: startDate.toLocaleString("sv-SE").replace(" ", "T"),
    endTime: now.toLocaleString("sv-SE").replace(" ", "T"),
  };
  store
    .dispatch("meetingStore/submitSetAgenda", request)
    .then((res) => {
      response.success(res, function () {
        // isOrder.value = false;
        load();
        emit("refresh", true);
      });
    })
    .catch(response.error)
    .finally(() => {
      isLoading.value = false;
    });
}

function startOrder(): void {
  orderList.value = list.value;
  isOrder.value = true;
  store.commit("meetingStore/setModeDisableBtn", true);
}

function cancelOrder(): void {
  list.value = orderList.value;
  isOrder.value = false;
  store.commit("meetingStore/setModeDisableBtn", false);
}

function saveOrder(): void {
  const request = list.value.map((el: TAgendaList, idx: number) => {
    return {
      id: el.id,
      order: idx + 1,
    };
  });
  store
    .dispatch("meetingStore/submitOrderAgenda", { data: request })
    .then((res) => {
      store.commit("meetingStore/setModeDisableBtn", false);
      response.success(res, function () {
        isOrder.value = false;
        load();
      });
    })
    .catch(response.error);
}
</script>
