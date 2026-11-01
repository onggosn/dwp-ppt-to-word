<template>
  <v-expansion-panels
    @update:modelValue="getListDetail"
    v-model="panel"
    :style="{ animationDelay: props.delay }"
    class="meeting-panel"
  >
    <v-expansion-panel :value="item.idMEventTemplate">
      <v-expansion-panel-title>
        <v-row align="center">
          <v-col cols="7">
            <p class="font-weight-bold ellipsis-1">
              {{ item.title || "-" }}
            </p>
          </v-col>
          <v-col cols="2">
            <div
              v-if="item?.bpName"
              :style="getColorChipTypeRdg(item.bpName)"
              style="
                display: inline-block;
                max-width: 150px;
                padding: 10px 12px;
                border-radius: 16px;
                font-size: 12px;
              "
            >
              <span class="text-truncate d-block">
                {{ item.bpName }}
              </span>
            </div>
          </v-col>
          <v-col cols="3">
            <v-chip
              v-if="item?.rdgbType"
              :style="getColorChipTypeRdg(item.rdgbType)"
            >
              {{ item.rdgbType }}
            </v-chip>
          </v-col>
        </v-row>
      </v-expansion-panel-title>
      <v-expansion-panel-text>
        <div v-if="loading" class="skeleton-inner">
          <div
            v-for="i in 3"
            :key="i"
            class="skeleton-inner-row"
            :style="{ animationDelay: `${(i - 1) * 0.08}s` }"
          >
            <div class="sk-block sk-doc-name"></div>
            <div class="sk-block sk-meta"></div>
            <div class="sk-block sk-action"></div>
          </div>
        </div>
        <div v-else>
          <div class="text-center">
            <img
              v-if="list.length === 0"
              :src="require('@/v2/assets/empty/no_available_state.svg')"
              alt="No Material"
              style="width: 100%; height: 150px; object-fit: contain"
            />
          </div>

          <v-card
            style="max-height: 90px; border-radius: 10px"
            elevation="3"
            class="pa-5 mb-3"
            v-for="child in list"
            :key="child"
          >
            <v-row class="align-center">
              <v-col cols="5">
                <p
                  style="
                    color: #4b4b4b;
                    max-height: 24px;
                    overflow: hidden;
                    padding-right: 32px;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                    font-weight: bold;
                  "
                >
                  {{ child.documentName }}
                </p></v-col
              >
              <v-col
                cols="6"
                style="
                  padding: 2px !important;
                  display: flex;
                  justify-content: start;
                "
              >
                <span class="item-information font-italic"
                  >Last modified by: {{ child.modifiedBy || " - " }}
                  <span style="font-style: normal">|</span> Date:
                  {{ reformatDateEngWithMonthLong(child.lastModified) }}
                  <span style="font-style: normal">|</span> Time:
                  {{ reformatTimes(child.lastModified) }} WIB</span
                >
              </v-col>
              <v-col cols="1">
                <div class="d-flex">
                  <div v-if="child.isEditPredefineMaterial">
                    <editAccessMaterialDialog
                      :id="child.idMEventDocPresentationMaterial"
                    />
                  </div>

                  <btn-delete
                    v-if="child.isDeletePredefineMaterial"
                    :btn-class="'ml-2'"
                    :title="'Delete'"
                    :is-icon-button="true"
                    :subtitle="'Are you sure, you want to delete this presentation material ?'"
                    :description="''"
                    :append-icon="true"
                    :btn-color="'#d6212a'"
                    :btn-icon-color="'#d6212a'"
                    :count-down="0"
                    :btn-density="'compact'"
                    @update="
                      deleteSectionContent(
                        child.idMEventDocPresentationMaterial
                      )
                    "
                  >
                    <v-tooltip activator="parent" location="bottom">
                      Delete
                    </v-tooltip>
                  </btn-delete>
                </div>
              </v-col>
            </v-row>
          </v-card>
        </div>
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script setup lang="ts">
import { ref, getCurrentInstance } from "vue";
import EditAccessMaterialDialog from "@/v2/components/admin/meeting/EditAccessMaterialDialog.vue";

import BtnDelete from "@/v2/components/utils/dialog/DeleteDialog.vue";
import {
  reformatDateEngWithMonthLong,
  reformatTimes,
} from "@/v2/helpers/DateHelper";
import { useStore } from "vuex";
import { TPresentationDetail } from "@/v2/Type";
import { useRoute } from "vue-router";
import { getColorChipTypeRdg } from "@/v2/helpers/color";

const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
  itemLength: {
    type: Number,
    default: 0,
  },
  delay: {
    type: String,
    default: "0s",
  },
});

const list = ref<TPresentationDetail[]>([]);
const store = useStore();
const panel = ref<number[]>([]);
const loading = ref(false);
const instance = ref<any>(getCurrentInstance()?.root.refs);
const route = useRoute();

const getListDetail = (id) => {
  if (!id) return;
  loading.value = true;
  const payload = {
    documentSearching: "",
    idMEventTemplate: id,
    sortBy: parseInt((route.query.eventSort as string) ?? 0),
    dateSince:
      store.getters["adminStore/getItemsFilter"].dateSince == ""
        ? null
        : store.getters["adminStore/getItemsFilter"].dateSince,
    dateTo:
      store.getters["adminStore/getItemsFilter"].dateTo == ""
        ? null
        : store.getters["adminStore/getItemsFilter"].dateTo,
  };

  store
    .dispatch("adminStore/getPresentationMaterialDetail", payload)
    .then((res) => {
      if (res.responseCode === "011000") {
        list.value = res.responseData;
      }
    })
    .finally(() => {
      loading.value = false;
    });
};

const deleteSectionContent = (idMEventDocPresentationMaterial) => {
  store
    .dispatch("adminStore/deletePresentationMaterial", {
      idMEventDocPresentationMaterial: idMEventDocPresentationMaterial,
    })
    .then((res) => {
      if (res.responseCode === "011000") {
        instance.value.toast.show({
          message: "Successfully deleted",
          color: "success",
          timeout: 3000,
          icon: "mdi-check",
        });
      } else {
        instance.value.toast.show({
          message: "Failed to delete section",
          color: "error",
          timeout: 3000,
          icon: "mdi-close",
        });
      }
    })
    .catch(() => {
      instance.value.toast.show({
        message: "An error occurred while deleting",
        color: "error",
        timeout: 3000,
        icon: "mdi-close",
      });
    })
    .finally(() => {
      getListDetail(props.item.idMEventTemplate);
    });
};
</script>

<style scoped>
:deep(
    .v-expansion-panel-title--active > .v-expansion-panel-title__overlay,
    .v-expansion-panel-title[aria-haspopup="menu"][aria-expanded="true"]
      > .v-expansion-panel-title__overlay
  ) {
  opacity: 0 !important;
}
:deep(.v-expansion-panel) {
  border-radius: 16px;
}
:deep(.v-expansion-panel__shadow) {
  box-shadow: 0px 2px 4px 0px #0000001f !important;
}
.item-information {
  color: #797979e5;
  font-size: 13px;
  line-height: 19.5px;
}
:deep(.v-expansion-panel-title) {
  min-height: 60px;
}

/* Entrance animation */
.meeting-panel {
  animation: fadeSlideUp 0.45s ease-out both;
}

/* ── Inner skeleton rows ──────────────────────────── */
.skeleton-inner {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 12px 16px;
}

.skeleton-inner-row {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #fafafa;
  border-radius: 10px;
  padding: 10px 14px;
  animation: fadeSlideUp 0.35s ease-out both;
}

.sk-block {
  border-radius: 6px;
  background: #e8e8e8;
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}

.sk-block::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.7) 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: shimmerSweep 1.4s ease-in-out infinite;
}

/* mirrors col-5 name | col-6 meta | col-1 action */
.sk-doc-name {
  flex: 1;
  height: 12px;
  max-width: 40%;
}
.sk-meta {
  flex: 1;
  height: 12px;
}
.sk-action {
  width: 28px;
  height: 28px;
  border-radius: 50%;
}

.sk-meta::after {
  animation-delay: 0.12s;
}
.sk-action::after {
  animation-delay: 0.24s;
}

@keyframes shimmerSweep {
  from {
    background-position: -200% 0;
  }
  to {
    background-position: 200% 0;
  }
}

@keyframes fadeSlideUp {
  from {
    opacity: 0;
    translate: 0 14px;
  }
  to {
    opacity: 1;
    translate: 0 0;
  }
}
</style>
