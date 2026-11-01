<template>
  <Teleport to="body">
    <v-dialog v-model="dialog" max-width="800" persistent>
      <v-card class="py-3 px-6 rounded-12">
        <div class="d-flex justify-space-between align-center border-bottom">
          <div></div>
          <div class="text-darkBlue font-weight-bold">Add Member</div>
          <div>
            <v-btn icon="mdi-close" variant="plain" @click="onClose()"></v-btn>
          </div>
        </div>
        <div class="pt-3">
          <SearchBar
            v-model="selected_item"
            v-model:search="search_item"
            :items="listItems"
            :appendIcon="true"
            :isRequired="true"
          />
          <v-list class="py-0 px-2">
            <span class="text-sm mb-3" style="color: #a6abc7">List Member</span>
            <v-list-item
              v-for="(item, i) in listMembers"
              :key="i"
              :title="item.name"
              class="px-0 py-2 text-lg"
            >
              <template v-slot:prepend>
                <v-avatar color="#eaeaea" class="avatar-big">
                  <img
                    v-if="item.type === `person`"
                    :src="require(`@/v2/assets/icon/person.svg`)"
                  />
                  <img v-else :src="require(`@/v2/assets/icon/people.svg`)" />
                </v-avatar>
              </template>
            </v-list-item>
          </v-list>
        </div>
      </v-card>
    </v-dialog>

    <ModalConfirm ref="modalWarning" :form-config="modalConfig">
      <template v-slot:icon-img>
        <v-avatar color="white" size="80" style="margin-top: -60px">
          <img :src="'/images/warningAlert.png'" style="width: 75px" />
        </v-avatar>
      </template>
      <template v-slot:btn-action>
        <div style="text-align: center">
          <v-btn
            @click="modalWarning.hide()"
            class="mr-2 rounded-lg btn primary-gradient"
          >
            Close
          </v-btn>
        </div>
      </template>
    </ModalConfirm>
  </Teleport>
</template>
<script lang="ts" setup>
import SearchBar from "@v2/components/utils/dialog/SearchBar.vue";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";

import { TModalConfirm } from "@/v2/Type";
import { getCurrentInstance, ref, watch } from "vue";
import { useStore } from "vuex";

const emit = defineEmits(["onClose"]);
const store = useStore();
const instance: any = getCurrentInstance()?.root.refs;

const dialog = ref<boolean>(false);
const role_id = ref<number>(0);
const selected_item = ref<number | null>(null);
const search_item = ref<string | null>(null);
const listItems = ref([]);
const listMembers = ref<any[]>([]);
const modalWarning = ref();
const modalConfig = ref<TModalConfirm>({
  title: "Warning",
  message:
    "You cannot delete the last penyusun. At least one penyusun must remain to ensure continued access to this document.",
});

function onOpen(roleId: number) {
  role_id.value = roleId;
  search_item.value = null;
  selected_item.value = null;
  fetchMember(roleId);
  dialog.value = true;
}

function onClose() {
  emit("onClose", true);
  dialog.value = false;
}

function fetchMember(role_id: number) {
  const payload = {
    roleSearching: "",
    idMrole: role_id,
    sortBy: 3,
    satkerFilter: store.getters["adminStore/getItemsFilter"].satkerFilter ?? [
      0,
    ],
    gradeFilter: store.getters["adminStore/getItemsFilter"].gradeFilter ?? [0],
  };
  store
    .dispatch("adminStore/getListAllMemberbyMRoleId", payload)
    .then((res) => {
      listMembers.value = res;
    });
}

watch(
  () => search_item.value,
  (val) => {
    if (val) {
      store
        .dispatch("userStore/fetchSearchUserNew", {
          query: val,
          isEvent: false,
        })
        .then((res) => {
          const tmp = res
            .filter((r: any) => r.isGroup === false)
            .map((r: any) => {
              return {
                id: r.id,
                value: r.value,
                type: "person",
              };
            });
          listItems.value = tmp;
        });
    }
  }
);

watch(
  () => selected_item.value,
  (val) => {
    if (val) {
      const req = {
        idMUser: val,
        idMRole: role_id.value,
      };
      store
        .dispatch("RoleMemberStore/storeRoleMember", req)
        .then(({ responseMessage }) => {
          instance.toast.show({
            message: responseMessage,
            color: "success",
            timeout: 3000,
          });
          fetchMember(role_id.value);
        })
        .catch((error) => {
          if (error.response.data.responseCode == "011051") {
            modalConfig.value.message =
              error.response.data.responseMessage ?? "internal server error";
            modalWarning.value.show({});
          } else {
            instance.toast.show({
              message:
                error.response.data.responseMessage ?? "internal server error",
              color: "success",
              timeout: 3000,
            });
          }
        });
    }
  }
);

defineExpose({
  onOpen,
});
</script>
