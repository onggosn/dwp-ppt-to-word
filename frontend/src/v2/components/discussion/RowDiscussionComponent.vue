<template>
  <div
    class="d-flex align-item-center"
    :class="isMe ? 'flex-row-reverse' : 'flex-row'"
  >
    <img :src="avatarImg" style="height: 5vh" class="ma-2 mt-4" />
    <v-card class="box-chat">
      <v-card-text :class="isMe ? 'text-end' : 'text-left'">
        <div
          class="text-18 mb-2"
          :class="isMe ? 'text-name-sender' : 'text-name-receiver'"
        >
          {{
            item.sender != ""
              ? stringToCapitalize(item.sender.toLowerCase())
              : "not found"
          }}
        </div>

        <template v-if="item.document">
          <div
            class="d-flex align-item-center align-center"
            style="cursor: pointer"
            :class="isMe ? 'flex-row-reverse' : 'flex-row'"
            @click="downloadFile"
          >
            <img :src="getDocumentImg()" class="mx-2" />
            <span class="text-20">{{ docName }}</span>
          </div>
        </template>
        <div v-else class="text-18 my-1">{{ item.message }}</div>

        <div class="text-13 mt-2">
          {{
            reformatDate(item.datetime) + " - " + reformatTime(item.datetime)
          }}
        </div>
      </v-card-text>
    </v-card>
  </div>
  <custom-loading
    v-if="fileLoading.isLoading"
    :title="fileLoading.bandwithTxt"
    :progress="fileLoading.downloadProgress"
    :totalProgress="fileLoading.sizeDocument"
    :hasProgress="fileLoading.hasProgress"
  />
</template>

<script>
import { v4 as uuidv4 } from "uuid";

import { reformatDate, reformatTime } from "@/library/DateHelper";
import client from "@/library/ApiClient";

import CustomLoading from "@v2/components/loading/CustomLoading.vue";

import { formatBytes, capitalize } from "@/helpers/utils";

export default {
  name: "rowDiscutionComponent",
  components: { CustomLoading },
  props: {
    item: {
      type: Object,
      required: true,
      default: function () {
        return {};
      },
    },
  },
  data() {
    return {
      fileLoading: {
        isLoading: false,
        hasProgress: false,
        sizeDocument: 0,
        downloadProgress: 0,
        bandwithTxt: "waiting for server response",
      },
    };
  },
  methods: {
    formatBytes: formatBytes,
    reformatDate: reformatDate,
    reformatTime: reformatTime,
    getDocumentImg() {
      let imgDoc = {
        pdf: "/images/docImage/iconPdf.png",
        docx: "/images/docImage/iconDoc.png",
        doc: "/images/docImage/iconDoc.png",
        xls: "/images/docImage/iconExcel.png",
        xlsx: "/images/docImage/iconExcel.png",
        ppt: "/images/docImage/iconPpt.png",
        pptx: "/images/docImage/iconPpt.png",
      };
      return imgDoc[this.docExt] ?? "/images/docImage/iconOther.png";
    },
    downloadFile() {
      if (this.item.document.tag == "assignment") {
        this.downloadFileAssignment();
      }
    },
    downloadFileAssignment() {
      let traceId = uuidv4();
      let fileDoc = this.item.document ?? {};

      this.fileLoading.isLoading = true;
      this.fileLoading.sizeDocument = fileDoc.sizeDocument ?? 0;
      this.fileLoading.hasProgress = fileDoc.sizeDocument ? true : false;
      client
        .downloadFileAssignmentNew({
          store: this.$store,
          data: {
            id: fileDoc.idDocument,
            traceId: traceId,
          },
          onDownloadProgress: (progressEvent) => {
            this.fileLoading.bandwithTxt =
              "Download progress: " + this.formatBytes(progressEvent.loaded);
            this.fileLoading.downloadProgress = progressEvent.loaded;
          },
        })
        .then((response) => {
          const link = document.createElement("a");
          link.href = window.URL.createObjectURL(new Blob([response.data]));
          link.setAttribute("download", fileDoc.documentName);
          document.body.appendChild(link);
          link.click();
        })
        .finally(() => {
          this.fileLoading.isLoading = false;
          this.fileLoading.bandwithTxt = "waiting for server response";
        });
    },
    stringToCapitalize(str) {
      return capitalize(str);
    },
  },
  computed: {
    isMe() {
      return this.item.username == this.$store.state.username;
    },
    avatarImg() {
      if (this.isMe) return "/images/task/dummyRed.png";
      return "/images/task/dummyBlue.png";
    },
    docExt() {
      if (this.item.document) {
        let temp = this.item.document.documentName.split(".");
        return temp[temp.length - 1];
      }
      return "other";
    },
    docName() {
      if (this.item.document) {
        let temp = this.item.document.documentName.split(".");
        temp.pop();
        return temp.join(".");
      }
      return "unknow";
    },
  },
};
</script>

<style scoped>
.text-name-sender {
  background: linear-gradient(90.85deg, #d6212a 15.38%, #ff000d 81.89%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 600;
}

.text-name-receiver {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 600;
}

.box-chat {
  margin: 1vh;
  max-width: 60%;
  border-radius: 10px;
  font-weight: 800;
  box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
}
</style>
