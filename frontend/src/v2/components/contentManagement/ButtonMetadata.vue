<template>
  <v-btn
    @click="openDialog"
    density="default"
    icon="mdi-eye"
    rounded="lg"
    size="x-small"
    class="primary-gradient"
    style="color: white"
  ></v-btn>
  <v-dialog v-model="dialog" max-width="800" persistent>
    <v-card class="border-radius-dwp pb-5">
      <v-card-title class="text-center mt-3">
        <h3 class="text-h6 text-darkBlue font-weight-bold">Metadata</h3>
        <v-btn
          density="default"
          icon="mdi-close"
          variant="text"
          class="btn-close"
          @click="dialog = false"
        />

        <hr class="line mt-5 mb-4" />
      </v-card-title>
      <v-row no-gutters class="ml-2">
        <v-col>
          <p class="ml-4 text-left txt-title font-weight-medium">Title</p>
          <p
            class="ml-4 pb-1 text-left text-black font-weight-medium"
            style="font-size: 18px"
          >
            {{ data.title }}
          </p>
        </v-col>
      </v-row>

      <v-row no-gutters class="ml-2">
        <v-col>
          <p class="ml-4 text-left txt-title font-weight-medium">Status</p>
          <p
            class="ml-4 pb-1 text-left text-black font-weight-bold"
            :class="gradientColor"
          >
            {{ data.statusName ?? "-" }}
          </p>

          <p class="ml-4 text-left txt-title font-weight-medium">Event</p>
          <p class="ml-4 pb-1 text-left text-black font-weight-regular">
            {{ data.eventName ?? "-" }}
          </p>

          <!-- <p class="ml-4 text-left txt-title font-weight-medium">Editor</p>
          <text-ellipsis>
            {{ data.listEditor ?? "-" }}
          </text-ellipsis> -->

          <p class="ml-4 text-left txt-title font-weight-medium">Penyusun</p>
          <text-ellipsis>
            {{ data.listPenyusun ? data.listPenyusun : "-" }}
          </text-ellipsis>

          <p
            v-if="showMetadataTimeline && data.labelPengaju !== ''"
            class="ml-4 text-left txt-title font-weight-medium"
          >
            {{
              typeof data.labelPengaju == "undefined"
                ? "Pengaju"
                : data.labelPengaju
            }}
          </p>
          <p
            v-if="showMetadataTimeline && data.labelPengaju !== ''"
            class="ml-4 pb-1 text-left text-black font-weight-regular"
          >
            {{ data.pengaju ? data.pengaju : "-" }}
          </p>

          <p
            v-if="showMetadataTimeline"
            class="ml-4 text-left txt-title font-weight-medium"
          >
            {{
              typeof data.labelPenyetuju == "undefined"
                ? "Penyetuju"
                : data.labelPenyetuju
            }}
          </p>
          <p
            v-if="showMetadataTimeline"
            class="ml-4 pb-1 text-left text-black font-weight-regular"
          >
            {{ data.penyetuju ? data.penyetuju : "-" }}
          </p>
        </v-col>
        <v-col v-if="showMetadataTimeline">
          <p class="ml-4 text-left txt-title font-weight-medium">Version</p>
          <p class="ml-4 pb-1 text-left text-black font-weight-regular">
            {{ data.version || "-" }}
          </p>

          <div v-if="showMetadataTimeline">
            <p class="ml-4 text-left txt-title font-weight-medium">Progress</p>
            <MetadataTimeline
              :items="data.listApprovals"
              :status="data.statusName"
            />
          </div>
        </v-col>
      </v-row>
    </v-card>
  </v-dialog>
</template>
<script lang="ts" setup>
import { ref, defineComponent, computed } from "vue";
import { GradientStatusClass } from "@/v2/enum/Enum";
import MetadataTimeline from "./MetadataTimeline.vue";
import TextEllipsis from "./TextEllipsis.vue";
import fetchData from "@v2/helpers/fetchData";
import clientv2 from "@v2/library/ApiClient";
import { useRoute } from "vue-router";

const props = defineProps<{
  isRevision?: boolean;
}>();

defineComponent({
  MetadataTimeline,
});

const route = useRoute();
const dialog = ref(false);
const data = ref<any>({});
const lookupTable = ref(GradientStatusClass);

const gradientColor = computed(() => {
  return (
    lookupTable.value[data.value.statusName?.toLowerCase()] ??
    "gradient-text-none"
  );
});

// SPRINT 14  => untuk dokumen ringsek munculkan timeline approval
const showMetadataTimeline = computed(() => {
  return true;
});

const isLoadData = computed((): boolean => {
  return !["00000000-0000-0000-0000-000000000000"].includes(
    route.params.idDoc as string
  );
});

function openDialog() {
  if (isLoadData.value) {
    fetchData(clientv2.getDocumentMetadata, {
      data: {
        id: route.params.idDoc,
        isRevision: props.isRevision ?? false,
      },
    }).then((resp) => {
      data.value = resp;
      dialog.value = true;
    });
  }
}
</script>

<style scoped lang="scss">
.line {
  border: none; /* Remove the default border */
  height: 2px; /* Set the height of the hr */
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}

.btn-close {
  position: absolute;
  right: 0;
  top: 0;
  margin-top: 10px;
  margin-right: 10px;
}

.txt-title {
  background: var(
    --Grey,
    linear-gradient(
      93deg,
      rgba(121, 121, 121, 0.9) 0%,
      rgba(187, 187, 187, 0.9) 152.21%
    )
  );
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-family: Poppins;
  font-size: 15px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
  margin-top: 10px;
}

/* The actual timeline (the vertical ruler) */
.timeline {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
}

/* The actual timeline (the vertical ruler) */
.timeline::after {
  content: "";
  position: absolute;
  width: 6px;
  background-color: white;
  top: 0;
  bottom: 0;
  left: 50%;
  margin-left: -3px;
}

/* Container around content */
.container {
  padding: 10px 40px;
  position: relative;
  background-color: inherit;
  width: 50%;
}

/* The circles on the timeline */
.container::after {
  content: "";
  position: absolute;
  width: 25px;
  height: 25px;
  right: -17px;
  background-color: white;
  border: 4px solid #ff9f55;
  top: 15px;
  border-radius: 50%;
  z-index: 1;
}

/* Place the container to the left */
.left {
  left: 0;
}

/* Place the container to the right */
.right {
  left: 50%;
}

/* Add arrows to the left container (pointing right) */
.left::before {
  content: " ";
  height: 0;
  position: absolute;
  top: 22px;
  width: 0;
  z-index: 1;
  right: 30px;
  border: medium solid white;
  border-width: 10px 0 10px 10px;
  border-color: transparent transparent transparent white;
}

/* Add arrows to the right container (pointing left) */
.right::before {
  content: " ";
  height: 0;
  position: absolute;
  top: 22px;
  width: 0;
  z-index: 1;
  left: 30px;
  border: medium solid white;
  border-width: 10px 10px 10px 0;
  border-color: transparent white transparent transparent;
}

/* Fix the circle for containers on the right side */
.right::after {
  left: -16px;
}

/* The actual content */
.content {
  padding: 20px 30px;
  background-color: white;
  position: relative;
  border-radius: 6px;
}
@mixin gradient-color($color1, $color2) {
  background: linear-gradient(to bottom, $color1, $color2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.gradient-text-none {
  @include gradient-color(#4b4b4b, #4b4b4b);
}
.gradient-text-progress {
  @include gradient-color(#c35b10, #fe7411);
}
.gradient-text-finish {
  @include gradient-color(#00783e, #02aa59);
}
</style>
