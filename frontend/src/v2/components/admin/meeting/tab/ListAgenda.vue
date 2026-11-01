<template>
  <div>
    <v-card v-if="list.length && !isLoading">
      <v-table>
        <thead>
          <tr>
            <th class="text-left header font-weight-bold" style="width: 40px">
              No
            </th>
            <th class="text-left header font-weight-bold" width="15%">
              Agenda
            </th>
            <th class="text-left header font-weight-bold">Satker Penyaji</th>
            <th class="text-left header font-weight-bold">Satker Diundang</th>
            <th class="text-left header font-weight-bold">Day Order</th>
            <th class="text-left header font-weight-bold">Room</th>
            <th class="text-left header font-weight-bold">Start Time</th>
            <th class="text-left header font-weight-bold">Finish Time</th>
            <th class="text-left header font-weight-bold">Minutes</th>
            <th class="text-left header font-weight-bold">Status</th>
            <th class="text-left header font-weight-bold" width="5%"></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(item, index) in list"
            style="font-size: 17px; color: #3a416f"
            :key="index"
          >
            <td>{{ index + 1 }}</td>
            <td class="text-left my-2">{{ item.agendaName || "-" }}</td>
            <td class="text-left">{{ item.satkerPenyaji || "-" }}</td>
            <td class="text-left">{{ item.satkerDiundang || "-" }}</td>
            <td class="text-left">{{ item.dayOrder || "-" }}</td>
            <td class="text-left">{{ item.room || "-" }}</td>
            <td class="text-left">
              {{ reformatTimes(item.startTime) || "-" }}
            </td>
            <td class="text-left">
              {{ reformatTimes(item.endTime) || "-" }}
            </td>
            <td class="text-left">{{ item.minutes || "-" }}</td>
            <td class="text-left">{{ item.status || "-" }}</td>
            <td class="text-left">
              <div class="d-flex">
                <btn-delete
                  v-if="item.isDelete"
                  :title="'Delete Agenda'"
                  :is-icon-button="true"
                  :subtitle="'Are you sure delete this agenda ?'"
                  :description="''"
                  :append-icon="true"
                  :btn-color="'#267DC2'"
                  :btn-icon-color="'#267DC2'"
                  :btn-variant="'text'"
                  :disabled-delete-last-item="false"
                  @update="deleteAgenda(item.idMeventAgendaTemplate)"
                >
                  <v-tooltip activator="parent" location="top">
                    Delete Agenda
                  </v-tooltip></btn-delete
                >
                <v-btn
                  v-if="item.isEdit"
                  variant="text"
                  @click="emit('onEdit', item.idMeventAgendaTemplate)"
                >
                  <v-icon class="table-content-center" color="#267DC2" small>
                    mdi-pencil
                  </v-icon>
                  <v-tooltip activator="parent" location="top">
                    Edit Agenda
                  </v-tooltip>
                </v-btn>
              </div>
            </td>
          </tr>
        </tbody>
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

    <template v-if="!list.length">
      <img
        :src="require('@/v2/assets/empty/no_available_state.svg')"
        class="img-no-available"
      />
    </template>
  </div>
</template>

<script lang="ts" setup>
import { ref, getCurrentInstance } from "vue";
import { useStore } from "vuex";
import { reformatTimes } from "@/v2/helpers/DateHelper";
import BtnDelete from "@/v2/components/utils/dialog/DeleteEventDialog.vue";
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const prop = defineProps({
  list: {
    type: Object,
    default: () => ({}),
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["onEdit", "onDelete"]);
const store = useStore();
const instance = ref<any>(getCurrentInstance()?.root.refs);

const deleteAgenda = (id) => {
  const payload = {
    id: id,
  };
  store
    .dispatch("adminStore/deletePredefinedAgenda", payload)
    .then((res) => {
      if (res.responseCode == "011000") {
        instance.value.toast.show({
          message: res.responseMessage,
          color: "success",
          timeout: 3000,
          icon: "mdi-check",
        });
      } else {
        instance.value.toast.show({
          message: res.responseMessage,
          color: "error",
          timeout: 3000,
          icon: "mdi-check",
        });
      }
    })
    .catch(() => {
      instance.value.toast.show({
        message: "Failed deleting agenda",
        color: "error",
        timeout: 3000,
        icon: "mdi-check",
      });
    })
    .finally(() => emit("onDelete"));
};
</script>

<style scoped>
.header {
  font-size: 17px;
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

:deep(.v-table__wrapper > table) {
  width: 1853px;
}
</style>
