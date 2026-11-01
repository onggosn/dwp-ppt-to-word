<template>
  <v-row
    no-gutters
    class="border-box-document border-radius-lg shadow-10 d-flex justify-space-between pr-5 pl-1 bg-white"
    style="
      height: 64px;
      align-items: center;
      margin-top: 3vh !important;
      max-width: 820px;
    "
  >
    <v-col lg="6" md="4" sm="6" cols="6">
      <h6
        class="fw-600 text-15 text-blackTheme pl-2"
        style="text-overflow: ellipsis; overflow: hidden; white-space: nowrap"
        @click="openDetail(item)"
        :style="{
          cursor: $vuetify.display.mobile == true ? 'pointer' : 'default',
          pointerEvents: $vuetify.display.mobile == true ? 'auto' : 'none',
        }"
      >
        {{ item.documentNameDisplay }}
      </h6>
    </v-col>

    <v-col lg="1" md="0" sm="0" cols="1" class="d-none d-md-flex">
      <img
        style="width: 24px; height: 30px"
        :src="getImage($filters.getDocumentExtension(item.documentNameDisplay))"
      />
    </v-col>

    <v-col lg="3" md="4" sm="6" cols="6">
      <div
        class="text-13 fw-700 text-orange"
        style="line-height: 40px; padding-top: 1px; text-align: center"
      >
        <b
          :style="getStyles(item.statusDoc)"
          style="padding-top: 1px; white-space: nowrap"
          >{{ item.statusDoc }}</b
        >
      </div>
    </v-col>

    <v-col lg="2" md="3" sm="6" cols="6" class="d-none d-md-flex">
      <v-btn
        rounded="lg"
        size="small"
        class="button-red"
        @click="openDetail(item)"
        >See Detail
      </v-btn>
    </v-col>
  </v-row>
</template>
<script setup lang="ts">
import { defineProps } from "vue";
import { useRouter } from "vue-router";

const props = defineProps({
  item: Object,
});

// const status = ref("");
const router = useRouter();

const openDetail = () => {
  if (props.item.typeDocument == "utama") {
    router.push({
      name: "preview-document",
      params: {
        documentId: props.item.id,
        taskId: props.item.taskId,
        workspaceId: props.item.idWorkspace,
        pageId: 1,
      },
    });
  } else {
    router.push({
      name: "preview-document-support",
      params: {
        documentId: props.item.id,
        taskId: props.item.taskId,
        workspaceId: props.item.idWorkspace,
        pageId: 1,
      },
    });
  }
};

const getStyles = (status) => {
  switch (status) {
    case "In Progress": {
      return {
        color: "#fe7411",
      };
    }
    case "Approved": {
      return {
        color: "#02aa59",
      };
    }
    case "Rejected": {
      return {
        color: "red",
      };
    }
    case "Need For Approval": {
      return {
        color: "#fe7411",
      };
    }
    case "Need For Review": {
      return {
        color: "#fe7411",
      };
    }
    default: {
      return {
        color: "#BABCCA",
      };
    }
  }
};

const getImage = (extension) => {
  switch (extension) {
    case "pptx":
      return "/images/docImage/iconPpt.png";
    case "ppt":
      return "/images/docImage/iconPpt.png";
    case "docx":
      return "/images/docImage/iconDoc.png";
    case "doc":
      return "/images/docImage/iconDoc.png";
    case "pdf":
      return "/images/docImage/iconPdf.png";
    default:
      return "/images/docImage/iconPdf.png";
  }
};

// export default {
//   props: {
//     item: Object,
//   },
//   data() {
//     return {};
//   },
//   methods: {
//     openDetail(item) {
//       this.resetApprove = true;
//       if (item.typeDocument == "utama") {
//         this.$router.push({
//           name: "preview-document",
//           params: {
//             documentId: item.id,
//             taskId: item.taskId,
//             workspaceId: item.idWorkspace,
//             pageId: 1,
//           },
//         });
//       } else {
//         this.$router.push({
//           name: "preview-document-support",
//           params: {
//             documentId: item.id,
//             taskId: item.taskId,
//             workspaceId: item.idWorkspace,
//             pageId: 1,
//           },
//         });
//       }
//     },

//     getImage(extension) {
//       switch (extension) {
//         case "pptx":
//           return "/images/docImage/iconPpt.png";
//         case "ppt":
//           return "/images/docImage/iconPpt.png";
//         case "docx":
//           return "/images/docImage/iconDoc.png";
//         case "doc":
//           return "/images/docImage/iconDoc.png";
//         case "pdf":
//           return "/images/docImage/iconPdf.png";
//         default:
//           return "/images/docImage/iconPdf.png";
//       }
//     },
//   },
// };
</script>
<style scoped>
.button-red {
  color: #fff;
  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.25);
  border-radius: 10px;
  padding: 5px 15px;
}

.shadow-10 {
  box-shadow: 0 4px 7px rgba(0, 0, 0, 0.1) !important;
  margin-bottom: -4px !important;
}
</style>
