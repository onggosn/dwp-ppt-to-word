<template>
  <v-menu
    transition="slide-y-transition"
    bottom
    :close-on-content-click="false"
  >
    <template v-slot:activator="{ props }">
      <v-btn
        icon=""
        size="small"
        v-bind="props"
        class="ml-2"
        style="position: right; top: 0; margin-right: 8px"
      >
        <img
          :src="require('@/v2/assets/icon/search.png')"
          :width="21"
          :height="21"
        />
      </v-btn>
    </template>
    <v-card min-width="300" class="rounded-lg">
      <v-form ref="form" type="submit" @submit.prevent="searchEvent">
        <v-list>
          <v-list-item>
            <v-text-field
              v-model="keyword"
              hide-details="auto"
              style="border-radius: 10px"
              placeholder="Search"
              variant="outlined"
              clearable
              @keyup.enter="searchEvent()"
              :rules="[rules.required]"
              :autofocus="true"
            ></v-text-field>
          </v-list-item>
        </v-list>
        <v-list-item>
          <v-list-item-title class="text-right">
            <v-btn
              class="btn-primary blue-gradient text-right mb-2"
              @click="searchEvent"
              >Search</v-btn
            >
          </v-list-item-title>
        </v-list-item>
      </v-form>
    </v-card>
  </v-menu>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

const props = defineProps({
  typeSearch: {
    type: String,
    default: "",
  },
  typeFilter: {
    type: Object,
    default: () => ({}),
  },
});

const router = useRouter();
const store = useStore();

const keyword = ref<string>("");
const form = ref<any>();
const rules = reactive({
  required: (value) => !!value || "Please input your keywords",
});
async function searchEvent() {
  const valid = form.value.isValid;
  if (valid) {
    const filter = props.typeFilter;
    filter.calendarType = "range"; // set pencarian 2 tahun ke belakang

    if (props.typeSearch === "calendar") {
      store.commit("meetingStore/setMeetingFilter", {
        ...filter,
        eventSearching: keyword.value,
      });
      router.push({
        name: "v2.meeting-management.search",
      });
    } else {
      router.push({
        name: "v2.search-result",
        params: {
          keyword: keyword.value,
          typeRDG: props.typeSearch,
        },
      });
    }
  }
}
</script>

<style scoped>
.blue-gradient {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: white !important;
  border-radius: 10px;
}
</style>
