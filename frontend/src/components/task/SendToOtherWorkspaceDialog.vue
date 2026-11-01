<template>
  <v-dialog v-model="dialog" persistent width="1024">
    <v-card style="border-radius: 15px">
      <v-card-title class="text-15">
        <v-sheet class="d-block pt-3 pr-5 text-end" style="align-self: end">
          <v-btn
            icon="mdi-close"
            color="white"
            elevation="0"
            size="small"
            @click="close()"
          ></v-btn>
        </v-sheet>
        <v-sheet class="bg-white d-block text-center mt-n9">
          Send to Other Workspace</v-sheet
        >
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12">
            <div class="text-15 text-blueTheme fw-500 mb-1">
              Document Name<span class="text-redTheme">*</span>
            </div>
            <v-text-field
              solo
              style="font-size: 14px"
              placeholder="Masukan Nama Document"
              v-model="formData.documentName"
              disabled
            />
          </v-col>
        </v-row>
        <fieldset class="fieldset-form">
          <legend>To 1</legend>
          <v-row>
            <v-col cols="6">
              <div class="text-15 text-blueTheme fw-500 mb-1">Workspace</div>
              <v-select
                single-line
                variant="solo"
                density="comfortable"
                placeholder="Choose Workspace"
                v-model="formData.idWorkspace"
                :error-messages="e(v$.formData.idWorkspace)"
                :loading="loading"
                :items="listWorkspace"
                :menu-props="{ 'max-width': 200 }"
                item-title="workspaceName"
                item-value="id"
                @update:modelValue="getTask"
                return-object
              />
            </v-col>
            <v-col cols="6">
              <div class="text-15 text-blueTheme fw-500 mb-1">Task</div>
              <v-select
                single-line
                variant="solo"
                density="comfortable"
                placeholder="Choose Task"
                v-model="formData.idTask"
                :error-messages="e(v$.formData.idTask)"
                :loading="loading"
                :items="listTask"
                :menu-props="{ 'max-width': 200 }"
                item-title="taskName"
                item-value="idTasks"
              />
            </v-col>
          </v-row>
        </fieldset>
        <v-row class="mt-2">
          <v-col cols="12">
            <div class="text-15 text-blueTheme fw-500 mb-1">
              Jenis Dokumen<span class="text-redTheme">*</span>
            </div>
            <v-select
              variant="solo"
              placeholder="Choose Jenis Dokumen"
              v-model="formData.idDocumentType"
              :error-messages="e(v$.formData.idDocumentType)"
              :loading="loading"
              :items="listDocumentType"
              item-title="categoryDocument"
              item-value="idCategoryDocument"
            />
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="mr-4, mb-2">
        <v-spacer></v-spacer>
        <v-btn
          elevation="3"
          style="
            background: linear-gradient(#fff -46.47%, #fff 157.9%);
            border-radius: 10px;
            padding-left: 15px;
            padding-right: 15px;
            font-weight: 800;
            color: red;
          "
          @click="close"
        >
          Cancel
        </v-btn>
        <v-btn
          elevation="3"
          class="btn-color-process"
          style="
            border-radius: 10px;
            padding-left: 15px;
            padding-right: 15px;
            margin-left: 10px;
            font-weight: 800;
          "
          @click="send"
        >
          Send
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";
import { getErrorMessages, isError } from "@/library/ValidationHelper";
import client from "@/library/ApiClient";

export default {
  setup: () => ({ v$: useVuelidate() }),
  validations() {
    let formData = {
      idWorkspace: { required },
      idTask: { required },
      idDocumentType: { required },
    };
    return { formData };
  },
  data() {
    return {
      row: [],
      listWorkspace: [],
      listTask: [],
      listDocumentType: [],
      loading: true,
      reset: true,
      dialog: false,
      formData: {
        documentName: null,
        idWorkspace: null,
        idTask: null,
        idDocumentType: null,
      },
    };
  },
  methods: {
    start(item) {
      this.row = item;
      this.formData.documentName = item.name;
      this.getListWorkspace();
      this.dialog = true;
      document.getElementById("DetailTaskDialog").style.visibility = "hidden";
    },
    getListWorkspace() {
      return client
        .getListWorkspaceInProgressByUsername({
          store: this.$store,
          data: {
            username: this.$store.state.username,
          },
        })
        .then((res) => {
          this.listWorkspace = res.plainData.responseData.listWorkspace;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    getTask() {
      this.formData.idTask = null;
      return client
        .getTaskByWorkspaceAndUsername({
          store: this.$store,
          data: {
            username: this.$store.state.username,
            idWorkspace: this.formData.idWorkspace.id,
          },
        })
        .then((res) => {
          this.listTask = res.plainData.responseData.listTask;
          this.listDocumentType =
            res.plainData.responseData.listCategoryDocument;
        })
        .finally(() => (this.loading = false));
    },
    e: getErrorMessages,
    isError: isError,
    resetForm() {
      this.v$.$reset();
      this.formData.documentName = null;
      this.formData.idWorkspace = null;
      this.formData.idTask = null;
      this.formData.idDocumentType = null;
    },
    send() {
      this.v$.$validate().then((res) => {
        if (res) {
          let reqData = {
            taskId: this.formData.idTask,
            taskDocumentId: this.row.id,
            createdBy: this.$store.state.username,
            linkDocumentType: this.formData.idDocumentType,
          };

          client
            .insertSendToOtherWorkspace({
              store: this.$store,
              data: reqData,
            })
            .then((res) => {
              if (res.plainData.responseCode == "011000") {
                //Berhasil
                this.$root.toast.show({
                  message: "Successfully Sent",
                  color: "success",
                  timeout: 3000,
                });

                this.close();
              } else {
                this.$root.toast.show({
                  message: res.plainData.responseMessage,
                  color: "error",
                  timeout: 3000,
                });
              }
            })
            .catch(() => {
              this.$root.toast.show({
                message: "Maaf, terjadi kesalahan sistem",
                color: "error",
                timeout: 3000,
              });
            });
        }
      });
    },
    close() {
      this.resetForm();
      this.dialog = false;
      document.getElementById("DetailTaskDialog").style.visibility = "visible";
      this.$emit("doneUpload");
    },
  },
};
</script>
<style scoped>
.fieldset-form {
  border-width: 2px;
  border-style: groove;
  border-color: rgb(192, 192, 192);
  border-image: initial;
  border-radius: 5px;
  padding-left: 20px;
  padding-right: 20px;
  padding-bottom: 20px;
}
:deep(.fieldset) {
  border-width: 2px !important;
  border-style: groove !important;
  border-color: rgb(192, 192, 192) !important;
  border-image: initial !important;
}
.btn-color-process {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: #fdfdfd;
}
</style>
