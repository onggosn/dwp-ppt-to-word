<template>
  <free-style-shimmer
    :is-loading="true"
    width="100px"
    height="24px"
    border-radius="15px"
    class="pr-4"
    v-if="isLoading"
  />
  <v-btn
    v-else-if="route.params.idDoc !== '00000000-0000-0000-0000-000000000000'"
    variant="outlined"
    rounded
    color="#065695"
    class="mr-2"
    size="small"
    :disabled="!buttonState"
    style="border-radius: 10px"
  >
    <span
      style="
        overflow: hidden;
        max-width: 150px;
        text-overflow: ellipsis;
        white-space: nowrap;
      "
      class="text-newBlack"
    >
      {{ documentVersion }}
    </span>
    <v-tooltip activator="parent" location="top">
      {{ documentVersion }}
    </v-tooltip>
    <template #prepend>
      <img :src="require('@/v2/assets/icon/version.svg')" />
    </template>
    <template v-slot:append>
      <v-icon>mdi-chevron-down</v-icon>
    </template>

    <v-menu activator="parent">
      <v-list>
        <v-list-item
          v-for="(item, index) in listDocumentVersion"
          :key="index"
          :value="index"
          style="cursor: pointer"
          :class="{
            'disabled-item': disableChip(item),
          }"
          @click="
            item.canClick &&
              handleChipClick(item.idBPDocumentVersion, item.versionName)
          "
        >
          <v-list-item-title>{{ item.versionName }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-btn>
</template>
<script setup lang="ts">
import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";

const router = useRouter();
const buttonState = computed(
  (): boolean => store.getters["documentStore/getOnloadingButtonState"]
);
const route = useRoute();
const store = useStore();
const isLoading = ref(false);

const documentVersion = computed(
  () => store.getters["collaborationStore/getDocumentVersion"]
);

const listDocumentVersion = computed(
  () => store.getters["collaborationStore/getListVersion"]
);

const isContentFinalisasi = computed(
  () => store.getters["collaborationStore/getIsContentFinalisasi"]
);

function disableChip(item: any) {
  return !item.canClick || documentVersion.value === item.versionName;
}

function handleChipClick(id: string, versionName: string) {
  //change document version in store if the content is finalisasi, untuk render di component bukan ke modal
  if (isContentFinalisasi.value) {
    store.commit("collaborationStore/setDocumentVersion", versionName);
    return;
  }

  router.push({
    name: "version.doc",
    params: {
      typeRDG: router.currentRoute.value.params?.typeRDG ?? "rdgm",
      idEvent: router.currentRoute.value.params?.idEvent,
      idDoc: router.currentRoute.value.params?.idDoc,
      versionId: id,
    },
  });
}
</script>
<style scoped>
.disabled-item {
  color: gray;
  cursor: not-allowed;
  pointer-events: none;
}
.btn-close {
  position: absolute;
  right: 0;
  top: 0;
  margin-top: 10px;
  margin-right: 10px;
}
.btn-go-to {
  color: #065695;
}
.btn-go-next {
  color: #065695;
}
:deep(
    .v-input--density-compact .v-field--variant-outlined,
    .v-input--density-compact .v-field--single-line,
    .v-input--density-compact .v-field--no-label
  ) {
  --v-field-padding-bottom: 1px;
}
:deep(.v-field--variant-outlined, .v-field--variant-outlined-filled) {
  border-radius: 15px;
  color: #065695;
  font-size: 15px;
  box-shadow: 0px 3px 7px 0px #85858540 !important;
}
:deep(.v-text-field .v-input__details) {
  padding-inline-start: 0;
  padding-inline-end: 0;
}
</style>
