<template>
  <v-card
    class="panel-expansion mb-5 rounded-lg"
    :style="panelBorderStyle"
    v-if="route.name !== 'dashboard.document.v2.hasil.search'"
  >
    <div
      class="panel-header"
      :class="{ 'primary-gradient': type === 'type-1' }"
    >
      <v-row class="pr-3" align="center" justify="space-between">
        <v-col cols="6">
          <h6 class="fw-500 text-18 my-2 pl-3 ellipsis-3" :style="titleStyle">
            {{ "List Document" }}
          </h6>
        </v-col>
      </v-row>
    </div>

    <div class="panel-content" :style="contentBorderStyle">
      <v-table class="custom-table">
        <thead>
          <tr>
            <th>No</th>
            <th>Name</th>
            <th>Workspace</th>
            <th>Event</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, idx) in item" :key="idx">
            <td class="text-center">
              <p v-if="page === 1">{{ idx + 1 }}</p>
              <p v-else>{{ (page - 1) * 10 + (idx + 1) }}</p>
            </td>
            <td>{{ data.documentName }}</td>
            <td class="text-center">{{ data.workspace }}</td>
            <td>
              <p class="elipsis">{{ data.event }}</p>
              <v-tooltip
                activator="parent"
                location="bottom"
                scroll-strategy="close"
              >
                {{ data.event }}
              </v-tooltip>
            </td>
            <td class="text-center">
              <v-icon
                size="large"
                class="arrow-right-blue"
                icon="mdi-chevron-right"
                @click="toEventPage(data.destIdEvent)"
              />
            </td>
          </tr>
        </tbody>
      </v-table>
    </div>
  </v-card>
  <template v-else>
    <v-card class="panel-expansion mb-5" v-for="(data, idx) in item" :key="idx">
      <div class="card-custom-container" @click="toEventPage(data.destIdEvent)">
        {{ data.documentName }}
      </div>
    </v-card>
  </template>
</template>

<script setup lang="ts">
import { computed, defineProps } from "vue";
import { useRouter, useRoute } from "vue-router";

const props = defineProps({
  item: {
    type: Object,
    default: () => ({}),
  },
  page: {
    type: Number,
    default: 1,
  },
  type: {
    type: String,
    default: "default",
  },
});

const router = useRouter();
const route = useRoute();

const toEventPage = (id: string) => {
  router.push({
    name: "v2.meeting-detail-result",
    params: {
      idEvent: id,
    },
  });
};

const panelBorderStyle = computed(() =>
  props.type === "default"
    ? {
        "border-left": "5px solid rgb(6, 86, 149)",
        "border-bottom-left-radius": "15px",
      }
    : {}
);

const contentBorderStyle = computed(() =>
  props.type !== "default" ? { "border-left": "5px solid rgb(6, 86, 149)" } : {}
);

const titleStyle = computed(() =>
  props.type === "default"
    ? {
        background: "linear-gradient(90deg, #065695, #267DC2)",
        "-webkit-background-clip": "text",
        "-webkit-text-fill-color": "transparent",
      }
    : {}
);
</script>

<style scoped>
.custom-table {
  border-collapse: collapse;
  width: 100%;
}

.custom-table thead,
.custom-table tbody {
  border: none;
}

.custom-table th {
  color: #3a416f !important;
  text-align: center !important;
  font-size: 13px;
}

.custom-table tr {
  border-bottom: 1px solid #ddd;
}

.custom-table tr:last-child {
  border-bottom: none;
}

.custom-table td {
  color: #4b4b4b !important;
  font-size: 13px !important;
}

.custom-table .elipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 200px;
  margin: 0 auto;
}

.arrow-right-blue {
  color: #065695;
  cursor: pointer;
}

.card-custom-container {
  padding: 16px;
  cursor: pointer;
  color: #3a416f;
  font-weight: 600;
}
</style>
