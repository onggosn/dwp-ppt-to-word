<script setup lang="ts">
import { ref, defineProps } from "vue";
import {
  mWorkspaceInProgress,
  mWorkspaceNotStarted,
  mWorkspacePast,
} from "@/models/workspace";
import { reformatDateCard } from "@/library/DateHelper";
import { onMounted } from "vue";

const props = defineProps({
  workspaceLevel: { type: Number, required: true, default: 1 },
  type: { type: Number, required: true, default: 1 },
});
const items = ref<any>([]);
const isCanSeeAll = ref<boolean>(false);
const isLoading = ref<boolean>(false);
const level = ref<number>(props.workspaceLevel);

onMounted(() => getList(level.value));

const getList = (level) => {
  isLoading.value = true;
  switch (props.type) {
    case 1: {
      mWorkspaceInProgress(level)
        .then((result) => {
          items.value = result.list;
          isCanSeeAll.value = result.seeAll;
        })
        .finally(() => (isLoading.value = false));
      break;
    }
    case 2: {
      mWorkspaceNotStarted(level)
        .then((result) => {
          items.value = result.list;
          isCanSeeAll.value = result.seeAll;
        })
        .finally(() => (isLoading.value = false));
      break;
    }
    case 3: {
      mWorkspacePast(level)
        .then((result) => {
          items.value = result.list;
          isCanSeeAll.value = result.seeAll;
        })
        .finally(() => (isLoading.value = false));
      break;
    }
  }
};

const buttonAction = (level, type, action) => {
  isLoading.value = true;
  switch (type) {
    case 1: {
      mWorkspaceInProgress(level, action)
        .then((result) => (items.value = result.list))
        .finally(() => {
          isCanSeeAll.value = !action;
          isLoading.value = false;
        });
      break;
    }
    case 2: {
      mWorkspaceNotStarted(level, action)
        .then((result) => (items.value = result.list))
        .finally(() => {
          isCanSeeAll.value = !action;
          isLoading.value = false;
        });
      break;
    }
    case 3: {
      mWorkspacePast(level, action)
        .then((result) => (items.value = result.list))
        .finally(() => {
          isCanSeeAll.value = !action;
          isLoading.value = false;
        });
      break;
    }
  }
};
</script>
<template>
  <slot name="title" />
  <v-sheet
    class="d-flex flex-wrap ml-5"
    style="background: transparent"
    v-if="isLoading"
  >
    <free-style-shimmer
      v-for="n in 3"
      :key="n"
      :is-loading="true"
      :width="$vuetify.display.smAndDown ? '55vw' : '22vw'"
      :height="$vuetify.display.smAndDown ? '12vh' : '15vh'"
      border-radius="10px"
      color="#DCDCDC"
      class="ml-md-2 mt-2"
    />
  </v-sheet>
  <p v-if="!items.length && !isLoading" class="ml-md-7 mb-10 text-14 text-grey">
    There is no workspace data...
  </p>
  <v-sheet
    class="d-flex align-content-start flex-wrap ml-md-5 bg-transparent"
    v-else-if="!isLoading"
  >
    <v-card
      v-for="item in items"
      :key="item"
      class="ma-2 pa-2 text-center rounded-lg"
      :width="$vuetify.display.smAndDown ? '55vw' : '22vw'"
      :height="$vuetify.display.smAndDown ? '12vh' : '15vh'"
      elevation="4"
      :class="type == 1 ? 'card-blue' : 'card-grey'"
      :to="{
        name: 'workspace-detail',
        params: { workspaceId: item.idWorkspace },
      }"
    >
      <p
        class="mt-2 pl-1 pr-1"
        :class="type == 1 ? 'title-red-gradient' : 'title-grey-gradient'"
      >
        {{ item.workspaceName }}
      </p>
      <p class="mt-1 subtitle-darkblue" v-if="type == 1">
        Due: {{ reformatDateCard(item.endDate) }}
      </p>
    </v-card>
  </v-sheet>

  <div class="text-end">
    <v-btn
      v-if="isCanSeeAll"
      class="pa-2 text-red mt-5 font-weight-bold bg-transparent"
      style="cursor: pointer; margin-right: 5vw"
      variant="text"
      @click="buttonAction(workspaceLevel, type, true)"
    >
      See more >>
    </v-btn>
  </div>
  <div class="text-end">
    <v-btn
      v-if="!isCanSeeAll && items.length > 3"
      class="pa-2 text-red mt-5 font-weight-bold bg-transparent"
      variant="text"
      style="cursor: pointer; margin-right: 5vw"
      @click="buttonAction(workspaceLevel, type, false)"
    >
      See Less &#60;&#60;
    </v-btn>
  </div>
</template>

<style scoped>
.subtitle-darkblue {
  color: #3a416f;
  text-align: center;
  font-size: 10px;
}
.title-red-gradient {
  background: -webkit-linear-gradient(#d6212a, #ff000d);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 15px;
  font-weight: bold;
}

.title-grey-gradient {
  background: -webkit-linear-gradient(#797979, #bbbbbb);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 15px;
  font-weight: bold;
}

.card-blue {
  border-left: solid 5px #0a5b9a;
  cursor: pointer;
}
.card-grey {
  border-left: solid 5px grey;
  cursor: pointer;
}
</style>
