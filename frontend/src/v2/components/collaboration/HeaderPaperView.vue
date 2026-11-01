<template>
  <div v-if="canShowHeaderDoc" class="header-paper-view">
    <template v-if="headerState === 'risalah-rapat'">
      <div
        class="d-flex justify-space-between"
        :style="{ fontFamily: `'${getFontFace(documentType)}'` }"
      >
        <img :src="require(`@/v2/assets/cop_logo_bi.svg`)" />
        <div
          v-if="rdgType !== 'RDGTK'"
          class="align-self-center font-weight-bold text-24"
        >
          RAHASIA
        </div>
      </div>
      <div
        v-if="!!noRisalahRapat"
        class="font-weight-bold doc-info"
        :style="{ padding: '15px 0', fontSize: '11pt' }"
      >
        <pre class="doc-number">{{ noRisalahRapat }}</pre>
        <p class="doc-attchment">
          Lampiran:
          <span v-if="rdgType == 'RDGTK'">
            &nbsp;&nbsp;&nbsp;&nbsp; berkas</span
          >
        </p>
      </div>
      <div
        v-html="documentTitle"
        :style="{ fontFamily: `'${getFontFace(documentType)}'` }"
        class="text-24 font-weight-bold mt-6 mb-1 text-center"
      ></div>
    </template>
    <template v-else-if="headerState === 'risalah-komite'">
      <div
        class="d-flex justify-space-between"
        :style="{ fontFamily: `'${getFontFace(documentType)}'` }"
      >
        <img :src="require(`@/v2/assets/cop_logo_bi.svg`)" />
        <div class="align-self-center font-weight-bold text-24">RAHASIA</div>
      </div>
      <div
        v-html="documentTitle"
        :style="{ fontFamily: `'${getFontFace(documentType)}'` }"
        class="text-24 font-weight-bold mt-6 mb-1 text-center"
      ></div>
    </template>
    <template v-else-if="headerState === 'risalah-rapat-komite-gabungan'">
      <div class="d-flex justify-space-between">
        <img :src="require(`@/v2/assets/cop_logo_bi.svg`)" />
        <div class="align-self-center font-weight-bold text-20">RAHASIA</div>
      </div>
      <div
        class="font-weight-bold doc-info"
        :style="{ padding: '15px 0', fontSize: '11pt' }"
      >
        <pre class="doc-number">{{ noRisalahKomiteGabungan }}</pre>
        <p class="doc-attchment">
          Lamp:
          <span v-if="rdgType == 'RDGTK'">
            &nbsp;&nbsp;&nbsp;&nbsp; set dokumen
          </span>
        </p>
      </div>

      <div
        v-html="(documentTitle as string).toUpperCase()"
        class="text-20 font-weight-bold mt-6 mb-1 text-center"
      ></div>
    </template>

    <template
      v-else-if="headerState === 'draft-siaran-pers/konsep-siaran-pers'"
    >
      <div class="d-flex justify-space-between">
        <img :src="require(`@/v2/assets/cop_logo_bi.svg`)" />
      </div>

      <div
        v-html="documentTitle"
        :style="{ fontFamily: `'${getFontFace(documentType)}'` }"
        class="text-24 font-weight-bold mt-6 mb-1 text-center"
      ></div>
    </template>

    <template v-else-if="headerState === 'risalah-rdg'">
      <div
        class="d-flex justify-space-between"
        :style="{ fontFamily: `'${getFontFace(documentType)}'` }"
      >
        <div class="text-grey text-10pt" v-html="noRisalahRdg"></div>
        <div class="text-grey text-10pt" v-html="dateRisalahRdg"></div>
      </div>

      <div class="d-flex justify-space-between">
        <div style="width: 15%">
          <img
            class="float-left d-block"
            :src="require(`@/v2/assets/cop_logo_bi_no_text.svg`)"
          />
        </div>
        <div
          v-html="documentTitle"
          :style="{ fontFamily: `'${getFontFace(documentType)}'` }"
          class="text-20 font-weight-bold mt-6 mb-1 text-center"
        ></div>
        <div style="width: 15%" />
      </div>
    </template>

    <template
      v-else-if="headerState === 'butir-keputusan/siaran-pers/press-release'"
    >
      <div class="d-flex" v-if="documentType === 3">
        <div
          class="text-grey text-17"
          v-html="noBkbs"
          :style="{ fontFamily: `'${getFontFace(documentType)}'` }"
        ></div>
      </div>
      <div class="d-flex justify-space-between">
        <div style="width: 15%">
          <img
            class="float-left d-block"
            :src="require(`@/v2/assets/cop_logo_bi_no_text.svg`)"
          />
        </div>
        <div
          v-html="documentTitle"
          :style="{ fontFamily: `'${getFontFace(documentType)}'` }"
          class="text-20 font-weight-bold mt-8 mb-1 text-center"
        ></div>
        <div style="width: 15%" />
      </div>
    </template>

    <template
      v-else-if="headerState === 'ringkasan-eksekutif' && rdgType === 'RDGTK'"
    >
      <div
        class="d-flex justify-space-between"
        :style="{ fontFamily: `'${getFontFace(documentType)}'` }"
      >
        <img :src="require(`@/v2/assets/cop_logo_bi.svg`)" />
        <div
          class="align-self-center font-weight-bold text-16 border border-opacity-100 pa-1 px-10"
        >
          RAHASIA
        </div>
      </div>
      <div
        v-html="documentTitle"
        :style="{ fontFamily: `'${getFontFace(documentType)}'` }"
        class="text-24 font-weight-bold mt-6 mb-1 text-center"
      ></div>
    </template>

    <template v-else-if="documentTitle">
      <div class="d-flex justify-center">
        <div
          v-html="documentTitle"
          :style="{ fontFamily: `'${getFontFace(documentType)}'` }"
          class="text-20 font-weight-bold mt-8 mb-1 text-center"
        ></div>
      </div>
    </template>

    <template v-else> </template>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useStore } from "vuex";
import { getFontFace } from "@/v2/helpers/utils";

const store = useStore();
const documentType = computed(
  () => store.getters["collaborationStore/getDocumentTypeId"]
);
const noRisalahKomiteGabungan = computed(
  () => store.getters["collaborationStore/getNoRisalahKomiteGabungan"]
);
const noRisalahRapat = computed(
  () => store.getters["collaborationStore/getNoRisalahRapat"]
);
const rdgType = computed(() => store.getters["collaborationStore/getRdgType"]);

const headerState = computed(() => {
  if ([1].includes(documentType.value)) return "risalah-rapat";
  if ([2].includes(documentType.value)) return "risalah-komite";
  if ([10, 11, 18].includes(documentType.value))
    return "draft-siaran-pers/konsep-siaran-pers";
  if ([3, 7, 12].includes(documentType.value))
    return "butir-keputusan/siaran-pers/press-release";
  if ([5].includes(documentType.value)) return "ringkasan-eksekutif";
  if ([9].includes(documentType.value)) return "risalah-rdg";
  if ([19].includes(documentType.value)) return "risalah-rapat-komite-gabungan";
  return "unknown";
});
const listForm = computed(
  () => store.getters["collaborationStore/getListForm"]
);
const noBkbs = computed(() => store.getters["collaborationStore/getNoBkbs"]);
const noRisalahRdg = computed(
  () => store.getters["collaborationStore/getNoRisalahRdg"]
);
const dateRisalahRdg = computed(
  () => store.getters["collaborationStore/getDateRisalahRdg"]
);

const canShowHeaderDoc = computed(
  () =>
    store.getters["collaborationStore/getViewTitle"] &&
    listForm.value.length > 0
);

const documentTitle = computed(
  () => store.getters["collaborationStore/getTitle"]
);
</script>

<style scoped>
.doc-number {
  font-family: "Optima";
}
.doc-number,
.doc-attchment {
  font-family: "Frutiger 45 Light" !important;
  font-weight: 600 !important;
}
</style>
