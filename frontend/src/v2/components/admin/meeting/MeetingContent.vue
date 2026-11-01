<template>
  <div class="my-2">
    <v-tabs
      v-model="tab"
      align-tabs="left"
      color="#D6212A"
      style="color: #065695"
    >
      <v-tab :value="1" class="tab-item">GENERAL</v-tab>
      <v-tab :value="2" class="tab-item">DESCRIPTION</v-tab>
      <v-tab :value="3" class="tab-item">MEMBER</v-tab>
      <v-tab :value="4" class="tab-item">AGENDA</v-tab>
    </v-tabs>
  </div>
  <div class="mt-5">
    <v-window v-model="tab">
      <v-window-item :value="1">
        <v-row v-if="isLoading">
          <v-col v-for="i in 7" :key="i" cols="12">
            <free-style-shimmer
              width="100%"
              height="40px"
              border-radius="10px"
              color="#d3d3d3"
            />
          </v-col>
        </v-row>
        <div v-else>
          <div class="flex-end-container">
            <AddMeeting
              variant="outlined"
              :btn-style="[]"
              :isEditForm="true"
              :form-data="formGeneral"
              @onSuccess="reloadContent"
            />
          </div>
          <detail-general-meeting :item="formGeneral" :updated="formGeneral" />
        </div>
      </v-window-item>
      <v-window-item :value="2">
        <v-row v-if="isLoading">
          <v-col v-for="i in 7" :key="i" cols="12">
            <free-style-shimmer
              width="100%"
              height="40px"
              border-radius="10px"
              color="#d3d3d3"
            />
          </v-col>
        </v-row>
        <div v-else>
          <div class="flex-end-container">
            <EditDeskripsi
              :form-data="formDeskripsi"
              :idbp="String(item.id)"
              @update="handleUpdateDesc"
            />
          </div>
          <detail-descripsi-meeting :item="formDeskripsi" />
        </div>
      </v-window-item>
      <v-window-item :value="3">
        <list-member-meeting
          :bpId="item.id"
          :refresh="tab"
          @load="emit('load')"
        />
      </v-window-item>
      <v-window-item :value="4">
        <div class="d-flex justify-end my-4">
          <v-btn
            variant="outlined"
            style="border-radius: 10px; font-size: 16px; font-weight: 600"
            prepend-icon="mdi-plus"
            class="mr-2"
            color="#065695"
            @click="
              agenda_form.onOpen({
                event_id: item.id,
                bp_id: bpId,
                dateDefault: agendaList[0]?.startTime.substring(0, 10),
              })
            "
          >
            Add Agenda
          </v-btn>
        </div>
        <div>
          <ListAgenda
            :list="agendaList"
            :is-loading="isLoading"
            @onEdit="openEditAgenda"
            @onDelete="loadAgenda"
          />
        </div>
      </v-window-item>
    </v-window>
    <AgendaForm ref="agenda_form" @onSuccess="loadAgenda" />
  </div>
</template>
<script setup lang="ts">
import AgendaForm from "./AgendaForm.vue";
import AddMeeting from "./AddMeeting.vue";
import EditDeskripsi from "./EditDeskripsi.vue";
import DetailGeneralMeeting from "./DetailGeneralMeeting.vue";
import DetailDescripsiMeeting from "./DetailDescripsiMeeting.vue";
import ListMemberMeeting from "./ListMemberMeeting.vue";
import ListAgenda from "./tab/ListAgenda.vue";
import { ref, watch, onMounted } from "vue";
import { useStore } from "vuex";

const emit = defineEmits(["load"]);
const store = useStore();
const isLoading = ref(false);
const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
  bpId: {
    type: [String, Number],
    required: true,
  },
});

const agenda_form = ref();
const tab = ref<number>(1);
const formDeskripsi = ref<string>("");
const formGeneral = ref<Record<string, any>>({});

onMounted(() => {
  updateStep(1);
  formDeskripsi.value =
    props.item.description === "" ? "<div><div>" : props.item.description;
});

watch(tab, (newValue) => {
  updateStep(newValue);
});

function openEditAgenda(id) {
  agenda_form.value.onOpen(
    {
      event_id: props.item.id,
      bp_id: props.bpId,
      dateDefault: agendaList.value[0]?.startTime.substring(0, 10),
    },
    id
  );
}

function updateStep(temp) {
  // tab 3 inside component
  if (temp === 1) {
    isLoading.value = true;
    const payload = {
      idMEventTemplate: props.item.id,
    };
    store
      .dispatch("adminStore/getGeneralMeeting", payload)
      .then((res: any) => {
        formGeneral.value = {
          time: res.time,
          title: res.title,
          media: res.idMeetingPlatfrom,
          method: res.idMeventMethod,
          timeDifferent: res.timeDifferentMainEvent,
          idEvent: res.idMEventTemplate,
          isTimeType: res.isTimeType,
        };
      })
      .finally(() => {
        isLoading.value = false;
      });
  } else if (temp === 2) {
    isLoading.value = true;

    const payload = {
      idMEventTemplate: props.item.id,
    };
    store
      .dispatch("adminStore/getDeskripsiMeeting", payload)
      .then((res: any) => {
        formDeskripsi.value =
          res.description === "" ? "<div><div>" : res.description;
      })
      .finally(() => {
        isLoading.value = false;
      });
  } else if (temp === 4) {
    loadAgenda();
  }
}

function reloadContent() {
  updateStep(1);
}

function handleUpdateDesc() {
  updateStep(2);
}

const agendaList = ref<any[]>([]);
function loadAgenda() {
  isLoading.value = true;
  const req = {
    idMEventTemplate: props.item.id,
  };
  store
    .dispatch("adminStore/getListAllListAgenda", req)
    .then((res) => {
      agendaList.value = res.responseData;
    })
    .finally(() => {
      isLoading.value = false;
    });
}
watch(props.item, () => {
  updateStep(1);
});
</script>
<style scoped>
.flex-end-container {
  display: flex;
  justify-content: flex-end;
}

.tab-item {
  font-size: 15px;
}
</style>
