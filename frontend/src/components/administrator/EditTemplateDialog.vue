<template>
  <v-dialog
    persistent
    v-model="dialog"
    content-class="overflowyhid"
    :max-width="800"
  >
    <v-card class="rounded-lg" :style="{ padding: '5px' }">
      <v-card-title class="d-flex justify-center align-center">
        <div class="text-18 text-blueTheme fw-500">Edit Metadata</div>
        <v-btn
          class="mr-2"
          style="position: absolute; right: 0"
          variant="text"
          icon="mdi-close"
          @click="hide()"
        ></v-btn>
      </v-card-title>
      <v-card-text class="pb-4">
        <div
          class="separatorHorizontalGradient"
          style="margin-top: -16px"
        ></div>
      </v-card-text>
      <p
        class="text-15 pa-1 mb-1 pl-2 text-white font-weight-bold gradient-blue"
        style="margin: 0 10px"
      >
        Metadata
      </p>
      <v-col cols="12" class="py-1">
        <div class="text-15 text-blueTheme fw-500 mt-3 mb-1">Task</div>
        <v-text-field
          variant="solo"
          disabled
          v-model="formData.taskName"
        ></v-text-field>
      </v-col>
      <v-col cols="12" class="py-1">
        <div class="text-15 text-blueTheme fw-500 mb-1">Document Type</div>
        <v-text-field
          variant="solo"
          disabled
          v-model="formData.documentType"
        ></v-text-field>
      </v-col>
      <div class="text-15 text-blueTheme fw-600 mb-1" style="margin-left: 20px">
        Penyusunan dan Kode Rangkaian IKU - ICK
      </div>

      <template v-if="formData.listSection.length > 0">
        <v-col
          cols="12"
          class="py-1 mb-2"
          v-for="(section, sectionIndex) in formData.listSection"
          :key="sectionIndex"
        >
          <fieldset class="fieldset-form">
            <legend>
              <div class="text-14 text-blueTheme fw-400">
                Section {{ sectionIndex + 1 }}
              </div>
            </legend>
            <div class="text-15 text-grey fw-500 mt-2">Title Section</div>
            <v-text-field
              variant="solo"
              placeholder="Please Input Title Section"
              v-model="section.sectionName"
              :error-messages="
                e(v$.formData.listSection[sectionIndex].sectionName)
              "
            ></v-text-field>
            <div>
              <div class="text-14 text-grey fw-500">Penyusun Section</div>
            </div>
            <v-autocomplete
              :id="'selectPenyusunID-' + (sectionIndex + 1)"
              multiple
              chips
              single-line
              item-title="value"
              item-value="id"
              variant="solo"
              density="comfortable"
              placeholder="Please Input Penyusun Section"
              clearable
              hide-selected
              closable-chips
              :error-messages="
                e(v$.formData.listSection[sectionIndex].listPenyusunSection)
              "
              :items="listPenyusunSection"
              v-model="section.listPenyusunSection"
              @update:modelValue="afterSelect(sectionIndex + 1)"
            >
            </v-autocomplete>
            <div class="d-flex justify-space-between align-center">
              <div class="text-14 text-grey fw-400">
                Kode Rangkaian IKU BI-ICK
              </div>
              <v-btn
                class="btn-create px-5 py-2 mb-3"
                @click="addMore(sectionIndex)"
              >
                + Add More
              </v-btn>
            </div>
            <div
              v-for="(field, index) in section.listKodeIKUICK"
              :key="index"
              class="d-flex justify-space-between align-center"
            >
              <v-col>
                <v-text-field
                  variant="solo"
                  v-model="field.value"
                  :placeholder="'Please Input IKU BI-ICK '"
                  :error-messages="
                    e(
                      v$.formData.listSection[sectionIndex].listKodeIKUICK[
                        index
                      ].value
                    )
                  "
                >
                  <template v-slot:append>
                    <v-btn
                      icon
                      small
                      color="#fff"
                      style="border-radius: 5px; border: 0.5px solid #d3d3d3"
                      @click="deleteKodeIku(sectionIndex, index)"
                    >
                      <v-icon icon="mdi-delete" color="red"></v-icon>
                    </v-btn>
                  </template>
                </v-text-field>
                <v-textarea
                  rows="2"
                  max-rows="3"
                  placeholder="Please Input Description"
                  v-model="field.description"
                  variant="solo"
                  :error-messages="
                    e(
                      v$.formData.listSection[sectionIndex].listKodeIKUICK[
                        index
                      ].description
                    )
                  "
                ></v-textarea>
              </v-col>
            </div>
          </fieldset>
          <div
            v-if="
              !(formData.listSection.length > 1 && sectionIndex > 0) &&
              !(sectionIndex === formData.listSection.length - 1)
            "
          ></div>

          <v-card-actions v-else class="justify-start pr-6 pt-0 pb-0 mt-3">
            <v-btn
              class="btn-delete px-5 py-2 mb-3"
              @click="removeSection(sectionIndex)"
              v-if="formData.listSection.length > 1 && sectionIndex > 0"
            >
              Delete
            </v-btn>

            <v-btn
              class="btn-create px-5 py-2 mb-3"
              @click="addSection(sectionIndex)"
              v-if="sectionIndex === formData.listSection.length - 1"
            >
              + Add Section
            </v-btn>
          </v-card-actions>
        </v-col>
      </template>
      <template v-else>
        <v-card-actions class="justify-start pr-6 pt-0 pb-0 mt-3">
          <v-btn class="btn-create px-5 py-2 mb-3" @click="addSection(0)">
            + Add Section
          </v-btn>
        </v-card-actions>
      </template>
      <v-card-actions class="justify-end pr-6 pt-0 pb-4">
        <v-btn class="btn-action btn-action-close" @click="hide()">
          Back
        </v-btn>
        <v-btn
          :disabled="formData.listSection.length === 0"
          class="btn-action btn-action-create"
          @click="save()"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import { getDocumentDetailIkuIck } from "@/models/document";
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";
import { getErrorMessages, isError } from "@/library/ValidationHelper";
import { getListSectionPenyusun } from "@/models/Administrator";
import client from "@/library/ApiClient";
export default {
  name: "editTemplate",
  components: {},
  setup: () => ({ v$: useVuelidate() }),
  validations() {
    return {
      formData: {
        listSection: this.formData.listSection.map((section) => ({
          sectionName: { required },
          listPenyusunSection: { required },
          listKodeIKUICK: section.listKodeIKUICK.map(() => ({
            value: { required },
            description: { required },
          })),
        })),
      },
    };
  },
  data() {
    return {
      formData: {
        idTaskTemplate: null,
        taskName: null,
        idDocumentSupportType: null,
        documentType: null,
        listSection: [
          {
            sectionName: null,
            listPenyusunSection: [
              {
                id: null,
                value: null,
              },
            ],
            listKodeIKUICK: [],
          },
        ],
      },
      dialog: false,
      selectedItem: null,
      listPenyusunSection: [],
    };
  },
  methods: {
    e: getErrorMessages,
    isError: isError,
    show(item) {
      this.getDetailIkuIck(item.idDocumentSupportType);
      this.dialog = true;
    },
    hide() {
      this.dialog = false;
    },
    addMore(sectionIndex) {
      const hashAction = this.formData.listSection[sectionIndex];
      if (hashAction) {
        this.formData.listSection[sectionIndex].listKodeIKUICK.push({
          value: null,
        });
      }
    },
    deleteKodeIku(sectionIndex, index) {
      this.formData.listSection[sectionIndex].listKodeIKUICK.splice(index, 1);
    },
    addSection() {
      const hashAction = this.formData;
      if (hashAction) {
        this.formData.listSection.push({
          sectionName: null,
          listPenyusunSection: [],
          listKodeIKUICK: [
            {
              value: null,
              description: null,
            },
          ],
        });
      }
    },
    removeSection(sectionIndex) {
      if (
        sectionIndex >= 0 &&
        sectionIndex < this.formData.listSection.length
      ) {
        this.formData.listSection.splice(sectionIndex, 1);
      }
    },
    getDetailIkuIck(idDocumentSupportType) {
      this.isLoading = true;
      getDocumentDetailIkuIck(idDocumentSupportType)
        .then((result) => {
          this.getPenyusunSection();
          result.listSection.map((section) => {
            delete section.penyusunSection;
            section.listPenyusunSection = section.listPenyusunSection.map(
              (item) => item.id
            );
            return section;
          });
          this.formData = result;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getPenyusunSection() {
      getListSectionPenyusun().then((result) => {
        this.listPenyusunSection = result;
      });
    },
    save() {
      this.v$.$validate().then((res) => {
        if (res) {
          this.loading = true;
          let data = {
            idDocumentSupportType: this.formData.idDocumentSupportType,
            listSection: this.formData.listSection,
            username: this.$store.state.username,
          };
          client
            .updateTemplateMetadata({
              store: this.$store,
              data: data,
            })
            .then((res) => {
              this.$root.toast.show({
                message: res.plainData.responseMessage,
                color:
                  res.plainData.responseCode == "011000" ? "success" : "error",
                timeout: 5000,
              });
              this.hide();
            })
            .catch((err) => {
              this.$root.toast.show({
                message: err.message ?? "Maaf, terjadi kesalahan sistem",
                color: "error",
                timeout: 500000,
              });
            })
            .finally(() => {
              this.loading = false;
            });
        }
      });
    },
    afterSelect(sectionIndex) {
      document.getElementById("selectPenyusunID-" + sectionIndex)?.blur();
    },
  },
};
</script>
<style scoped>
.separatorHorizontal {
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
  height: 1.2px;
  width: 100%;
  margin: 10px;
}
.gradient-blue {
  background: linear-gradient(
    90deg,
    #065695 35.16%,
    rgba(255, 255, 255, 0) 101.03%
  );
}
.fieldset-form {
  border-style: groove;
  border-color: rgb(192, 192, 192);
  border-image: initial;
  border-radius: 10px;
  border: 1px solid var(--Placeholder, #babcca);
  padding-left: 10px;
  padding-right: 10px;
  padding-bottom: 10px;
}
:deep(.v-autocomplete__selection .v-chip) {
  background: #267dc2 !important;
  color: white !important;
}
.btn-create {
  color: #fff;
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%);
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.25);
  border-radius: 10px;
  letter-spacing: 0.1px;
  font-weight: 900;
}
.btn-delete {
  color: #fff;
  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.25);
  border-radius: 10px;
  letter-spacing: 0.1px;
  font-weight: 900;
}
.error-message {
  color: red; /* Customize the error message text color */
  font-size: 12px; /* Customize the error message font size */
  margin-top: 4px; /* Adjust the margin for spacing */
}
</style>
