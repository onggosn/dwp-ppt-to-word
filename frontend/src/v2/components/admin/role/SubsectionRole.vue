<template>
  <v-sheet class="my-3">
    <v-expansion-panels v-model="panel">
      <v-expansion-panel :value="item.username">
        <v-expansion-panel-title>
          <v-row align="center" style="cursor: pointer !important">
            <v-col cols="5" style="padding: 0 !important">
              <p
                class="font-weight-bold"
                style="
                  color: #4b4b4b;
                  max-height: 24px;
                  overflow: hidden;
                  padding-right: 32px;
                  text-overflow: ellipsis;
                  white-space: nowrap;
                "
              >
                {{ item.name || item.formasiName }}
              </p>
            </v-col>
            <v-col cols="2" style="padding: 0 !important">
              <span
                class="font-weight-bold"
                style="
                  color: #4b4b4b;
                  max-height: 24px;
                  overflow: hidden;
                  padding-right: 32px;
                  text-overflow: ellipsis;
                  white-space: nowrap;
                "
                >{{ item?.satker }}</span
              >
            </v-col>
            <v-col
              cols="5"
              style="
                padding: 2px !important;
                display: flex;
                justify-content: start;
              "
            >
              <span class="item-information font-italic"
                >Last modified by: {{ item.lastUpdatedBy || " - " }}
                <span style="font-style: normal">|</span> Date:
                {{
                  reformatDateEngWithMonthLong(item.lastUpdatedDate) || " - "
                }}
                <span style="font-style: normal">|</span> Time:
                {{ reformatTimes(item.lastUpdatedDate) || " - " }} WIB</span
              >
            </v-col>
          </v-row>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-divider class="my-5" thickness="3" />
          <div
            class="d-flex flex-wrap ml-auto ga-2"
            style="justify-content: flex-end"
          >
            <btn-delete
              v-if="item.isDelete"
              :btn-title="'Delete Role'"
              :title="'Delete Member'"
              :subtitle="'Are you sure delete this Member ?'"
              :description="''"
              :append-icon="true"
              :btn-color="'#d6212a'"
              :btn-icon-color="'#d6212a'"
              @update="deleteRole(item.idMuserRole)"
            />
          </div>
          <div>
            <UserInfo :item="data" :is-loading="isLoading" />
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-sheet>
</template>
<script setup lang="ts">
import {
  reformatTimes,
  reformatDateEngWithMonthLong,
} from "@/v2/helpers/DateHelper";
import UserInfo from "@/v2/components/admin/role/UserRoleInfo.vue";
import { ref, watch, getCurrentInstance, onMounted } from "vue";
import { TUserRoleDetail } from "@/v2/Type";
import BtnDelete from "@/v2/components/utils/dialog/DeleteEventDialog.vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
});

const emit = defineEmits(["on-delete-role"]);
const store = useStore();
const router = useRouter();
const isLoading = ref<boolean>(false);
const panel = ref<number[] | string[]>([]);
const data = ref<TUserRoleDetail[]>([]);

function load() {
  isLoading.value = true;

  const payload = {
    username: props.item.username,
  };

  store
    .dispatch("adminStore/getUserRoleDetail", payload)
    .then((res: any) => {
      data.value = res.responseData?.data[0]; //ngambil index pertama dulu
    })
    .finally(() => {
      isLoading.value = false;
    });
}

watch(panel, (newValue) => {
  if (newValue) load();
});

const instance = ref<any>(getCurrentInstance()?.root.refs);
const deleteRole = (id) => {
  store
    .dispatch("adminStore/deleteRole", { id: id })
    .then((res) => {
      if (res.responseCode == "011000") {
        instance.value.toast.show({
          message: res.responseMessage,
          color: "success",
          timeout: 3000,
          icon: "mdi-check",
        });
      } else {
        instance.value.toast.show({
          message: res.responseMessage,
          color: "error",
          timeout: 3000,
          icon: "mdi-check",
        });
      }
    })
    .catch(() => {
      instance.value.toast.show({
        message: "Failed to delete member",
        color: "error",
        timeout: 3000,
        icon: "mdi-check",
      });
    })
    .finally(() => {
      if (store.state.username == props.item.username) {
        router.push({ name: "v2.home" }).then(() => {
          window.location.reload();
        });
      } else {
        emit("on-delete-role");
      }
    });
};
</script>
<style scoped>
.item-information {
  color: #797979e5;
  font-size: 13px;
  line-height: 19.5px;
}
</style>
