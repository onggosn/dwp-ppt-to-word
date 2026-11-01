<template>
  <v-dialog
    persistent
    v-model="dialog"
    content-class="overflowyhid"
    width="80vw"
  >
    <v-card class="rounded-lg">
      <v-card-title class="d-flex justify-center align-center">
        <div class="text-18 text-blueTheme fw-500">IKU-ICK</div>
        <v-btn
          class="mr-2"
          style="position: absolute; right: 0"
          variant="text"
          icon="mdi-close"
          @click="hide()"
        ></v-btn>
      </v-card-title>
      <div class="separatorHorizontal"></div>
      <p
        class="text-15 pa-1 mb-1 pl-2 text-white font-weight-bold gradient-blue"
        style="margin: 0 10px"
      >
        Penyusun and Kode Rangkaian IKU-ICK
      </p>
      <div v-if="isLoading" class="mx-6 mt-3">
        <v-row>
          <v-col cols="12" v-for="idx in 4" :key="idx">
            <paragraph-shimmer
              :is-loading="true"
              :lines="2"
              :random-size="false"
            />
          </v-col>
        </v-row>
      </div>
      <v-col
        cols="12"
        class="py-1 mb-2"
        v-for="(section, sectionIndex) in sectionsData"
        :key="sectionIndex"
        v-else
      >
        <fieldset class="fieldset-form">
          <legend>
            <div class="text-14 text-blueTheme fw-400">
              Section {{ sectionIndex + 1 }}
            </div>
          </legend>
          <v-col cols="12">
            <div class="text-15 text-grey fw-400 mt-2">Title Section</div>
            <div class="text-15 text-black fw-500">
              {{ section.sectionName }}
            </div>
          </v-col>
          <v-col cols="12">
            <v-row>
              <v-col cols="6">
                <div class="text-15 text-grey fw-400 mt-2">
                  Penyusun Section
                </div>
                <div class="text-15 text-black fw-500">
                  {{ section.penyusunSection }}
                </div>
              </v-col>
              <v-col cols="6">
                <div>
                  <div class="text-15 text-grey fw-400 mt-2">
                    Kode Rangkaian IKU BI-ICK
                  </div>
                  <div class="text-15 text-black fw-500 d-flex flex-wrap">
                    <template
                      v-for="(item, index) in section.listKodeIKUICK"
                      :key="index"
                    >
                      <p>
                        <v-tooltip activator="parent" location="bottom">
                          Deskripsi Indikator ICK:<br />
                          {{ item.description }} </v-tooltip
                        >{{ item.value }};&nbsp;
                      </p>
                    </template>
                  </div>
                </div>
              </v-col>
            </v-row>
          </v-col>
        </fieldset>
      </v-col>
      <v-card-actions class="justify-end pr-6 pt-0 pb-4">
        <v-btn class="btn-action btn-action-close" @click="hide()">
          Back
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { getDocumentDetailIkuIck } from "@/models/document";
export default {
  name: "seeDocument",
  data() {
    return {
      dialog: false,
      isLoading: false,
      sectionsData: [],
    };
  },
  methods: {
    open(idDocumentSupportType) {
      this.getDetailIkuIck(idDocumentSupportType);
      this.dialog = true;
    },
    hide() {
      this.dialog = false;
    },
    getDetailIkuIck(idDocumentSupportType) {
      this.isLoading = true;
      this.sectionsData = [];
      getDocumentDetailIkuIck(idDocumentSupportType)
        .then((result) => {
          this.sectionsData = result.listSection;
        })
        .finally(() => {
          this.isLoading = false;
        });
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
</style>
