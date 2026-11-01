<template>
  <free-style-shimmer
    width="60%"
    height="2.5rem"
    border-radius="10px"
    v-if="isLoading"
  />
  <template v-for="(item, index) in dataApprovalButton" :key="index">
    <ApprovalButton
      :approval-data="dataApprovalButton[0]"
      :data="item"
      :isDocSectoral="isDocSec"
    />
  </template>
</template>
<script setup lang="ts">
/* eslint-disable */
import { ref, onMounted } from "vue";
import { useStore } from "vuex";
import ApprovalButton from "@v2/components/collaboration/approval/ApprovalButton.vue";
import { useRoute } from "vue-router";
const props = defineProps({
  isDocSec: {
    type: Boolean,
    required: false,
  },
});
onMounted(() => {
  getButtonApprovalForm();
});

const dataApprovalButton = ref<any>();
const route = useRoute();
const store = useStore();
const isLoading = ref(false);
function getButtonApprovalForm() {
  isLoading.value = true;
  const reqData = {
    id: route.params.idDoc,
  };
  store
    .dispatch("eFormStore/GetListFlowDetail", reqData)
    .then((response) => {
      dataApprovalButton.value = response.responseData;
      if (
        response.responseData.length > 1 &&
        [31, 32].includes(response.responseCode.currentStatus)
      ) {
        // edit form enable untuk user approval
        store.commit("collaborationStore/setStartEditEForm", false);
      } else if (
        [31, 32].includes(store.getters["collaborationStore/setDocumentStatus"])
      ) {
        // jika status need for review atau need for approval -> form editor disabled
        store.commit("collaborationStore/setStartEditEForm", true);
      }
    })
    .finally(() => {
      isLoading.value = false;
    });
}
</script>
