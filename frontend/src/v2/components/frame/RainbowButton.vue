<template>
  <v-menu
    v-model="isMenuOpen"
    transition="slide-y-transition"
    location="bottom end"
    :offset="[10, 0]"
    width="250"
  >
    <template v-slot:activator="{ props }">
      <div class="d-flex flex-row px-2 gradient-box mr-6">
        <v-btn v-bind="props" @click="handleMenuClick">
          <img :src="require('@/v2/assets/edit_icon.svg')" />
          <span
            class="text-blueRedTheme-gradien ml-3"
            style="font-size: 14px; font-weight: 600"
          >
            Create
          </span>
          <template v-slot:append>
            <v-icon color="#ff000d">mdi-chevron-down</v-icon>
          </template>
        </v-btn>
      </div>
    </template>
    <v-list style="border-radius: 16px">
      <template v-if="isLoading">
        <v-list-item style="color: #3a416f" class="px-4">
          <v-list-item-title>
            <free-style-shimmer
              v-for="n in 3"
              class="px-2 py-1"
              :key="n"
              height="40px"
              width="15vw"
              border-radius="5px"
              color="#DCDCDC"
              @click.stop
            />
          </v-list-item-title>
        </v-list-item>
      </template>
      <template v-else>
        <v-list-item
          v-for="item in listItem"
          :key="item.id"
          :title="item.value"
          class="text-black font-weight-bold text-left text-subtitle-2 pl-5 pt-2 pb-2 pr-10 item poppins-font"
          style="cursor: pointer"
          @click="showDialog(item.value)"
        >
          <template v-slot:prepend>
            <img
              :src="getIcon(item.value)"
              width="20"
              height="20"
              style="margin-right: 16px"
            />
          </template>
        </v-list-item>
      </template>
    </v-list>
  </v-menu>
  <create-event-dialog ref="createEventDialog" />
  <create-AIU-dialog ref="createAIUDialogRef" />
  <create-PNIN-dialog ref="createPNINDialogRef" />
</template>
<script setup lang="ts">
import { ref, defineComponent } from "vue";
import CreateEventDialog from "@/v2/components/event/CreateEventDialog.vue";
import CreateAIUDialog from "@/v2/components/event/CreateAIUDialog.vue";
import CreatePNINDialog from "@/v2/components/event/CreatePNINDialog.vue";

import { useStore } from "vuex";

defineComponent({
  components: {
    CreateEventDialog,
    CreateAIUDialog,
    CreatePNINDialog,
  },
});

const isLoading = ref<boolean>(false);
const isMenuOpen = ref<boolean>(false);
const listItem = ref<any[]>([]);
const createEventDialog = ref();
const createAIUDialogRef = ref();
const createPNINDialogRef = ref();
const store = useStore();

const showDialog = (item: any) => {
  if (item === "Event") {
    createEventDialog.value.showDialogEvent();
  } else if (item === "AIU") {
    createAIUDialogRef.value.showDialogEvent(item);
  } else if (item === "Policy Note" || item === "Issue Note") {
    createPNINDialogRef.value.showDialogEvent(item);
  }
};

const getIcon = (item: any) => {
  switch (item) {
    case "Event":
      return "/images/icon/create-event.svg";
    default:
      return "/images/icon/paper-plus.svg";
  }
};

const handleMenuClick = () => {
  if (isMenuOpen.value) {
    getDropdownCreate();
  }
};

const getDropdownCreate = () => {
  isLoading.value = true;
  store.dispatch("eventStore/getDropdownCreate").then((data) => {
    listItem.value = data;
    isLoading.value = false;
  });
};
</script>

<style lang="scss" scoped>
.item:hover {
  background-color: #d6e6f5;
}

.poppins-font {
  font-family: "Poppins", sans-serif !important;
}

.gradient-box {
  display: flex;
  align-items: center;
  margin: auto;

  position: relative;
  box-sizing: border-box;

  $border: 2px;
  background: #fff;
  background-clip: padding-box; /* !important */
  border: solid $border transparent; /* !important */
  border-radius: 10px;

  &:before {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: -1;
    margin: -$border; /* !important */
    border-radius: inherit; /* !important */
    background: linear-gradient(to right, #267dc2, #ff000d);
  }
}

.text-blueRedTheme-gradien {
  background: -webkit-linear-gradient(left, #267dc2, #ff000d);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.btn-close {
  position: absolute;
  right: 0;
  top: 0;
  margin-top: 10px;
  margin-right: 10px;
}
</style>
