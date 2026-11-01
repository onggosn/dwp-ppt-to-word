<template>
  <v-sheet height="100%">
    <v-sheet class="mb-5 mr-5" style="justify-self: end">
      <btn-edit :isNewData="true" :idbp="String(bpId)" @load="handleLoad" />
    </v-sheet>

    <v-row v-if="isLoading">
      <v-col v-for="i in 7" :key="i" cols="12">
        <free-style-shimmer
          width="100%"
          height="40px"
          border-radius="10px"
          color="#d3d3d3"
        />
      </v-col>
    </v-row>

    <template v-if="list?.length && !isLoading">
      <v-card
        v-for="(item, idx) in list"
        :key="idx"
        class="bg-white mb-4 mr-3 ml-3 rounded-lg elevation-2"
      >
        <v-row no-gutters style="align-items: center">
          <v-col cols="5">
            <v-sheet class="pa-2 ma-2 text-13"> {{ item.name }}</v-sheet>
          </v-col>
          <v-col>
            <v-sheet class="pa-2 ma-2 text-13">
              {{ item.organizationName }}
            </v-sheet>
          </v-col>
          <v-col>
            <v-sheet class="pa-2 ma-2 text-13"> {{ item.gradeName }}</v-sheet>
          </v-col>
          <v-col>
            <v-sheet class="pa-2 ma-2 text-13"> {{ item.accessType }} </v-sheet>
          </v-col>
          <v-col>
            <v-sheet class="pa-2 ma-2">
              <div
                class="d-flex flex-wrap ml-auto ga-2"
                style="justify-content: center"
              >
                <div class="pr-2">
                  <!-- check if last member of the meeting list.length == currentPage -->
                  <btn-delete
                    :title="'Delete Member'"
                    :is-icon-button="true"
                    :subtitle="'Are you sure delete this member ?'"
                    :description="''"
                    :append-icon="true"
                    :btn-color="'#d6212a'"
                    :btn-icon-color="'#d6212a'"
                    :disabled-delete-last-item="list.length == currentPage"
                    :warning-message="'You cannot delete the last member meeting. At least one member must remain'"
                    @update="deleteMemberMeeting(item.id)"
                  />
                </div>

                <!-- tambah button edit disini mas abi -->
                <div>
                  <btn-edit
                    :idbp="String(bpId)"
                    :item="item"
                    @load="handleLoad"
                  />
                </div>
              </div>
            </v-sheet>
          </v-col>
        </v-row>
      </v-card>

      <div class="text-center mt-7">
        <v-pagination
          v-if="list?.length && !isLoading"
          rounded="1"
          elevation="2"
          size="small"
          v-model="currentPage"
          :length="pagination.totalPage"
          :total-visible="10"
          @update:model-value="changePage"
        />
      </div>
    </template>
    <template v-if="!list?.length && !isLoading">
      <v-card class="bg-white mb-4 mr-3 ml-3 rounded-lg elevation-0">
        No member meeting...
      </v-card>
    </template>
  </v-sheet>
</template>

<script setup lang="ts">
import { onMounted, ref, getCurrentInstance, watch } from "vue";
import { useStore } from "vuex";
import BtnDelete from "@/v2/components/utils/dialog/DeleteEventDialog.vue";
import BtnEdit from "@/v2/components/admin/meeting/EditMemberMeeting.vue";
import { TListMemberMeeting, TInfoPage } from "@/v2/Type";

const store = useStore();
const isLoading = ref(false);
const props = defineProps({
  bpId: {
    type: [String, Number],
    required: true,
  },
  refresh: {
    type: Number,
    default: 1,
  },
});
const list = ref<TListMemberMeeting[]>([]);
const instance = ref<any>(getCurrentInstance()?.root.refs);

const emit = defineEmits(["load"]);

const handleLoad = () => {
  loadListMember();
  emit("load");
};
const pagination = ref<TInfoPage>({
  totalData: 0,
  prevPageNo: 0,
  pageNo: 1,
  nextPageNo: 2,
  totalPage: 1,
  entriesPerPage: 10,
});
const currentPage = ref<number>(1);

const deleteMemberMeeting = (id) => {
  store
    .dispatch("adminStore/deleteMemberMeeting", {
      id: id,
    })
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
      loadListMember();
    });
};

const loadListMember = () => {
  isLoading.value = true;
  store
    .dispatch("adminStore/getListMemberMeeting", {
      pageSize: pagination.value.entriesPerPage,
      page: pagination.value.pageNo ?? currentPage.value,
      idMEventTemplate: props.bpId,
    })
    .then((res) => {
      list.value = res.responseData?.data;
      pagination.value.pageNo = res.responseData.infoPage?.pageNo ?? 1;
      pagination.value.totalData = res.responseData.infoPage?.totalData ?? 10;
      pagination.value.totalPage = res.responseData.infoPage?.totalPage ?? 10;
    })
    .finally(() => {
      isLoading.value = false;
    });
};

const changePage = (current: number) => {
  pagination.value.pageNo = current;
  loadListMember();
};
watch(
  () => props.refresh,
  (newValue) => {
    if (newValue == 3) {
      loadListMember();
    }
  }
);
onMounted(() => {
  loadListMember();
});
</script>
