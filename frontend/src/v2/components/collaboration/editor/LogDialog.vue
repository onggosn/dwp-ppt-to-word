<template>
  <v-dialog v-model="dialog" transition="dialog-bottom-transition" fullscreen>
    <template v-slot:activator="{ props: activatorProps }">
      <v-btn
        size="small"
        variant="outlined"
        style="border-radius: 10px; color: #065695"
        prepend-icon="mdi-file-eye-outline"
        class="mr-2"
        v-bind="activatorProps"
        @click="onOpen"
      >
        Log
      </v-btn>
    </template>

    <v-card>
      <v-toolbar color="#065695" style="color: white">
        <v-btn icon="mdi-close" @click="onClose"></v-btn>
        <v-toolbar-title>Audit Log</v-toolbar-title>
      </v-toolbar>
      <paragraph-shimmer
        v-if="loading"
        width="100%"
        :lines="10"
        :random-size="false"
        border-radius="15px"
        class="pa-8"
      />
      <div class="ma-5" v-else>
        <v-table fixed-header style="min-height: 75vh">
          <thead>
            <tr>
              <th class="text-left">No</th>
              <th class="text-left">Username</th>
              <th class="text-left">Activity</th>
              <th class="text-left">Date</th>
              <th class="text-left">Status</th>
              <th class="text-left">Event Name/Workspace Name</th>
              <th class="text-left">Document Name</th>
              <th class="text-left">Section Name</th>
            </tr>
          </thead>
          <tbody>
            <template v-if="!listlog.length">
              <tr>
                <td colspan="8" class="text-center">no data available...</td>
              </tr>
            </template>
            <template v-else>
              <tr v-for="(item, index) in listlog" :key="index">
                <td>{{ index + 1 }}</td>
                <td>{{ item.authorId }}</td>
                <td>
                  <v-chip :color="getColorChip(item.type)">
                    {{ getTypeInformation(item.type) }}
                  </v-chip>
                </td>
                <td>
                  {{ getDateFromString(item.createdAt) }}
                  {{ formatTimeAddMinutes(item.createdAt, 7) }}
                </td>
                <td>
                  <v-chip
                    class="ma-2"
                    :color="getColorState(item.state)"
                    variant="text"
                  >
                    {{ item.state }}
                  </v-chip>
                </td>
                <td>{{ eventName }}</td>
                <td>{{ documentName }}</td>
                <td>{{ sectionName }}</td>
              </tr>
            </template>
          </tbody>
        </v-table>

        <v-divider class="mt-5 mb-5" />
        <span class="text-danger mt-5">Detail:</span>
        <br />
        <span class="text-danger">
          {{ eventName }} / {{ documentName }} / {{ sectionName }}
        </span>
      </div>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
// import { ExportSuggestion } from "@/v2/library/ApiCKEditor";
import { useStore } from "vuex";
import { ref } from "vue";
import {
  formatTimeAddMinutes,
  getDateFromString,
} from "@/v2/helpers/DateHelper";

const props = defineProps({
  id: {
    type: String,
    default: "",
  },
});

const store = useStore();
const documentName = ref();
const eventName = ref();
const sectionName = ref();
const loading = ref(false);
const listlog = ref<any>([]);
const dialog = ref(false);

const onOpen = async () => {
  loading.value = true;
  store
    .dispatch("eFormStore/getAuditLog", { document_id: props.id })
    .then((res) => {
      if (res.responseCode == "011000") {
        eventName.value = res.responseData.eventName;
        documentName.value = res.responseData.bPDocumentName;
        sectionName.value =
          res.responseData.bPName + " - " + res.responseData.bPEFormLabel;
        listlog.value = res.responseData.data;
      }
    });

  //   let response = await ExportSuggestion(props.id);
  //   if (response.data.length) {
  //     response.data.forEach((element) => {
  //       listlog.value.push({
  //         author: element.author_id,
  //         type: element.type,
  //         created_at: element.created_at,
  //         state: element.state,
  //         workspace: eventName,
  //         document: documentName,
  //         section: "iii",
  //       });
  //     });
  //   }
  loading.value = false;
};

const onClose = () => {
  dialog.value = false;
  listlog.value = [];
};

const getTypeInformation = (value) => {
  if (value.includes("attribute")) return "format change";
  return value;
};

const getColorChip = (value) => {
  switch (value) {
    case "insertion":
      return "green";
    case "deletion":
      return "red";
    default:
      return "primary";
  }
};

const getColorState = (value) => {
  switch (value) {
    case "accepted":
      return "green";
    case "rejected":
      return "red";
    default:
      return "info";
  }
};
</script>
