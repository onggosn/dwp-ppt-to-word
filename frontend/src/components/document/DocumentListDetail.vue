<script setup lang="ts">
import { onMounted } from "vue";
import { defineProps } from "vue";
import { getDocumentDetail } from "@/models/document";
import { ref } from "vue";
import seeDocumentDialog from "@/components/document/SeeDocumentDialog.vue";

const props = defineProps({
  document: { type: Object, required: true },
  isOpen: { type: Boolean },
});

const isLoading = ref(false);
const detail = ref({});
const modalSeeDocument = ref();
let idDocumentSupportType = 0;
onMounted(() => {
  isLoading.value = true;
  if (props.isOpen) {
    getDocumentDetail(props.document.id, props.document.typeDocument)
      .then((result) => {
        detail.value = result;
        idDocumentSupportType = result.idDocumentSupportType;
        return result;
      })
      .finally(() => {
        isLoading.value = false;
      });
  }
});

const getStyles = (_item) => {
  if (_item.title == "Status") {
    switch (_item.value) {
      case "In Progress": {
        return {
          color: "#fe7411",
          "font-weight": 900,
        };
      }
      case "Approved": {
        return {
          color: "#02aa59",
          "font-weight": 900,
        };
      }
      case "Rejected": {
        return {
          color: "red",
          "font-weight": 900,
        };
      }
      case "Need For Approval": {
        return {
          color: "#fe7411",
          "font-weight": 900,
        };
      }
    }
  } else if (_item.title == "Status Penyelesaian") {
    switch (true) {
      case _item.value.includes("100%"): {
        return {
          color: "#02AA59 !important",
          "font-weight": 900,
        };
      }
      default: {
        return {
          color: "#fe7411 !important",
          "font-weight": 400,
        };
      }
    }
  }
};
const seeIkuIck = () => {
  modalSeeDocument.value.open(idDocumentSupportType);
};
</script>
<template>
  <v-sheet class="mr-3 text-12 bg-transparent">
    <paragraph-shimmer
      :is-loading="isLoading"
      :lines="6"
      :random-size="false"
      color="red"
    />
  </v-sheet>
  <v-sheet
    v-if="!isLoading"
    class="d-flex flex-wrap rounded-lg pa-5"
    style="background-color: #f7fbfe"
  >
    <template v-for="(item, index) in detail.data" :key="index">
      <template v-if="item.title != '-'">
        <v-sheet
          class="mr-3 text-12 bg-transparent"
          :width="
            item.title == 'Detail Dokumen' || item.title == 'Keterangan'
              ? '100%'
              : '47%'
          "
          :class="
            item.title == 'Detail Dokumen'
              ? 'text-13 font-weight-bold textBlackGrey mb-2'
              : ''
          "
        >
          <p class="d-block font-weight-bold text-left textGrey pa-1">
            {{ item.title }}
          </p>
          <p class="d-block text-left pa-1" :style="getStyles(item)">
            {{ item.value }}
          </p>
        </v-sheet>
      </template>
    </template>
    <template v-if="detail.isIKUICK === true">
      <v-sheet style="background-color: #f7fbfe" width="47%"></v-sheet>
      <v-sheet style="background-color: #f7fbfe">
        <div
          class="font-weight-500 text-blueTheme-gradien click-effect mt-2 pl-4"
          @click="seeIkuIck"
        >
          See IKU-ICK
          <span class="mdi mdi-chevron-right-circle"></span>
        </div>
      </v-sheet>
    </template>
  </v-sheet>
  <see-document-dialog ref="modalSeeDocument" />
</template>

<style scoped>
.textGrey {
  color: rgb(166, 171, 199);
}

.textBlackGrey {
  color: #4b4b4b !important;
}
.click-effect {
  cursor: pointer;
}

.click-effect:active {
  background-color: #f0f0f0; /* Change the background color when clicked */
}
</style>
