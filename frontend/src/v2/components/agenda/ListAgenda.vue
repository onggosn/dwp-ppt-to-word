<template>
  <div>
    <v-card
      v-if="localModelValue.length"
      class="pb-10 mt-5 mx-2"
      style="
        box-shadow: 0px 4px 18px rgba(192, 192, 192, 0.25);
        border-radius: 10px;
      "
    >
      <v-table>
        <thead>
          <tr>
            <th
              v-if="isDraggable"
              class="text-left header font-weight-bold"
              style="width: 40px"
            ></th>
            <th class="text-left header font-weight-bold" style="width: 40px">
              No
            </th>
            <th class="text-left header font-weight-bold" width="15%">
              Agenda
            </th>
            <th class="text-left header font-weight-bold">Satker Penyaji</th>
            <th class="text-left header font-weight-bold">Satker Diundang</th>
            <th class="text-left header font-weight-bold">ADG Koordinator</th>
            <th class="text-left header font-weight-bold">Kehadiran ADG</th>
            <th class="text-left header font-weight-bold">Date</th>
            <th class="text-left header font-weight-bold">Room</th>
            <th class="text-left header font-weight-bold">Start Time (WIB)</th>
            <th class="text-left header font-weight-bold">Finish Time (WIB)</th>
            <th class="text-left header font-weight-bold">Minutes</th>
            <th class="text-left header font-weight-bold">Status</th>
            <th v-if="isParticipant" class="text-left header font-weight-bold">
              Control
            </th>
            <th class="text-left header font-weight-bold" width="5%"></th>
          </tr>
        </thead>
        <draggable
          v-model="localModelValue"
          :disabled="!isDrag"
          @start="onDragStart"
          @end="onDragEnd"
          @change="onChange"
          tag="tbody"
          item-key="id"
        >
          <template #item="{ element, index }">
            <tr
              style="font-size: 13px"
              :style="isDrag ? 'cursor: pointer' : ''"
            >
              <td
                v-if="isDrag"
                class="btn-dragable"
                style="width: 40px; margin-top: 15px"
              >
                <img
                  :src="require('@v2/assets/icon/drag.svg')"
                  :class="{
                    'btn-disabled': isAgendaDraggable(element),
                  }"
                  alt=""
                  width="30"
                />
              </td>
              <td>{{ index + 1 }}</td>
              <td class="text-left my-2">{{ element.agendaName || "-" }}</td>
              <td class="text-left">{{ element.presentingUnit || "-" }}</td>
              <td class="text-left">{{ element.invitedUnit || "-" }}</td>
              <td class="text-left">{{ element.adgBidang || "-" }}</td>
              <td class="text-left">
                {{ element.adgBidangAttendance || "-" }}
              </td>
              <td class="text-left">{{ element.date || "-" }}</td>
              <td class="text-left">{{ element.agendaPlace || "-" }}</td>
              <td class="text-left">{{ element.startTime || "-" }}</td>
              <td class="text-left">{{ element.endTime || "-" }}</td>
              <td class="text-left">{{ element.intervalTime || "-" }}</td>
              <td class="text-left">{{ element.status || "-" }}</td>
              <td v-if="isParticipant" class="text-left">
                <div
                  v-if="element.status == 'Waiting' || element.status == 'Done'"
                >
                  <v-btn
                    variant="text"
                    :disabled="setDisable(element)"
                    @click="handleSetAgenda(element)"
                  >
                    <v-icon class="table-content-center" color="#267DC2" small>
                      mdi-play
                    </v-icon>
                  </v-btn>
                  <v-tooltip activator="parent" location="top">
                    {{
                      setDisable(element) == false
                        ? "Start Agenda"
                        : element.status == "Done"
                        ? "The agenda cannot be restarted because it has already been finalized"
                        : "The current agenda cannot begin until the previous agenda has been finalized"
                    }}
                  </v-tooltip>
                </div>
                <v-btn
                  :loading="loading"
                  v-else-if="element.status == 'In Progress'"
                  variant="text"
                  @click="handleStopAgenda(element)"
                >
                  <v-icon class="table-content-center" color="#267DC2" small>
                    mdi-checkbox-blank
                  </v-icon>
                  <v-tooltip activator="parent" location="top">
                    Stop Agenda
                  </v-tooltip>
                </v-btn>
              </td>
              <td class="text-left">
                <div class="d-flex">
                  <v-btn
                    v-if="element.isDelete"
                    variant="text"
                    :disabled="handleDisableButton(element.status)"
                    @click="deleteAgenda(element.id)"
                  >
                    <v-icon class="table-content-center" color="#267DC2" small>
                      mdi-delete
                    </v-icon>
                    <v-tooltip activator="parent" location="top">
                      Delete Agenda
                    </v-tooltip>
                  </v-btn>
                  <v-btn
                    v-if="element.isEdit"
                    variant="text"
                    :disabled="element.status == 'Done'"
                    @click="
                      editAgenda(element.id, element.date, element.status)
                    "
                  >
                    <v-icon class="table-content-center" color="#267DC2" small
                      >mdi-pencil</v-icon
                    >
                    <v-tooltip activator="parent" location="top"
                      >Edit Agenda</v-tooltip
                    >
                  </v-btn>
                </div>
              </td>
            </tr>
          </template>
        </draggable>
      </v-table>
    </v-card>

    <v-card
      v-if="isLoading"
      class="pb-10 mt-5 mx-5"
      style="
        box-shadow: 0px 4px 18px rgba(192, 192, 192, 0.25);
        border-radius: 10px;
      "
    >
      <v-row>
        <v-col cols="12" v-for="idx in 4" :key="idx">
          <paragraph-shimmer
            :is-loading="true"
            :lines="2"
            :random-size="false"
          />
        </v-col>
      </v-row>
    </v-card>

    <template v-if="!localModelValue.length">
      <img
        :src="require('@/v2/assets/empty/no_available_state.svg')"
        class="img-no-available"
      />
    </template>
  </div>
  <ModalWarning ref="modalWarning" :modal-config="modalConfig" />
</template>

<script lang="ts" setup>
/* eslint-disable */
import { PropType, ref, computed } from "vue";

import draggable from "vuedraggable";

import { TAgendaList, TModalWarning } from "@v2/Type.d";

import { convertDate } from "@/v2/helpers/DateHelper";

import ModalWarning from "../utils/modal/ModalWarning.vue";

type TPropsEdit = {
  id: string;
  date: string;
  status: string;
};

const prop = defineProps({
  modelValue: {
    type: Array as PropType<TAgendaList[]>,
    required: true,
    default: () => [],
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  isDraggable: {
    type: Boolean,
    default: false,
  },
  statusMode: {
    type: Number,
    default: 0,
  },
  isParticipant: {
    type: Boolean,
    default: false,
  },
});

const modalConfig = ref<TModalWarning>({
  img: {
    location: "workspace/warningAlert.png",
    width: "80px",
    height: "80px",
  },
  title: "Warning",
  description:
    "You can’t change the order of agendas with agendas that are already “done” or “In Progress”",
  btnBackgroundStyle: "linear-gradient(to right, #065695, #267DC2)",
  textBtn: "Close",
  textWeight: 400,
  textStyle: "normal",
});

const emit = defineEmits<{
  (e: "delete", value: string): void;
  (e: "edit", value: TPropsEdit): void;
  (e: "update:modelValue", value: TAgendaList[]): TAgendaList[];
  (e: "setTime", value: string): void;
  (e: "setStopTime", value: string): void;
}>();

const dragging = ref<boolean>(false);

const modalWarning = ref();

const isDrag = computed((): boolean => {
  return prop.isDraggable;
});

const localModelValue = computed({
  get(): TAgendaList[] {
    return prop.modelValue;
  },
  set(val: TAgendaList[]) {
    emit("update:modelValue", val);
  },
});

const originalModelValue = ref<TAgendaList[]>([]);
const newIndexRef = ref<number | null>(null);
const oldIndexRef = ref<number | null>(null);
const onDragStart = () => {
  originalModelValue.value = [...localModelValue.value];
};

const onDragEnd = () => {
  if (
    newIndexRef.value !== null &&
    oldIndexRef.value !== null &&
    !checkOrder(newIndexRef.value, oldIndexRef.value)
  ) {
    localModelValue.value = [...originalModelValue.value];
  }
};
const onChange = (evt: any) => {
  const { newIndex, oldIndex } = evt.moved;
  const { value: agendaData } = originalModelValue;

  const { status: prevDataStatus } = agendaData[oldIndex];
  const { status: nextDataStatus } = agendaData[newIndex];

  const agendaStatus = ["done", "in progress"];

  const isDraggable =
    !agendaStatus.includes(prevDataStatus.toLowerCase()) &&
    !agendaStatus.includes(nextDataStatus.toLowerCase());

  if (!checkOrder(newIndex, oldIndex) || !isDraggable) {
    modalWarning.value.show();
    localModelValue.value = [...originalModelValue.value];
  }
};

const checkOrder = (newIndex: number, oldIndex: number): boolean => {
  const items = [...localModelValue.value];
  for (let i = 1; i < items.length; i++) {
    const date1 = convertDate(items[i - 1].date);
    const date2 = convertDate(items[i].date);

    if (date1 > date2) {
      return false;
    }
  }
  return true;
};

const isAgendaDraggable = (agenda) => {
  const { status } = agenda;

  if (
    status.toLowerCase() === "waiting" ||
    status.toLowerCase() === "in progress"
  )
    return false;

  return true;
};

const deleteAgenda = (value: string) => {
  emit("delete", value);
};
const editAgenda = (idAgenda: string, dateAgenda: string, status: string) => {
  emit("edit", { id: idAgenda, date: dateAgenda, status: status });
};
const handleSetAgenda = (idAgenda: string) => {
  emit("setTime", idAgenda);
};
const handleStopAgenda = (idAgenda: string) => {
  emit("setStopTime", idAgenda);
};
function setDisable(temp) {
  if (!temp.isBtnPlayEnable) {
    return true;
  } else {
    if (prop.isDraggable) {
      return true;
    } else {
      return false;
    }
  }
}
function handleDisableButton(status) {
  return ["Done", "In Progress"].includes(status) || prop.isDraggable
}
</script>

<style scoped>
.header {
  font-size: 13px;
  font-weight: 500;
  color: #065695 !important;
  background: #f7fbfe;
}

.img-no-available {
  margin-top: 10vh;
  width: 100%;
  height: 20vh;
  margin-bottom: 5vh;
}

.btn-dragable {
  text-align: center;
  vertical-align: middle;
}

.btn-dragable > .btn-disabled {
  filter: grayscale(100%);
}

:deep(.v-table__wrapper > table) {
  width: 1853px;
}
</style>
