<template>
  <v-sheet class="bg-transparent ml-5 px-7 py-10">
    <v-row>
      <v-col cols="9">
        <v-btn
          icon
          class="btn-back"
          @click="router.push({ name: 'v2.meeting-management' })"
          ><v-icon icon="mdi-arrow-left" color="#065695"></v-icon
        ></v-btn>
        <span class="ml-2 color-grey">
          Search results displayed {{ list.length }} (total relevant results
          {{ pagination.totalData }} )
        </span>
      </v-col>
      <v-col cols="3">
        <v-text-field
          v-model="keyword"
          density="compact"
          hide-details="auto"
          clearable
          placeholder="Search"
          variant="solo"
          :autofocus="true"
          @keyup.enter="getList(keyword)"
        >
          <template v-slot:prepend-inner>
            <img src="/images/task/searchMagnifier.svg" /></template
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <div v-if="isLoading">
          <free-style-shimmer
            width="100%"
            height="3.5rem"
            border-radius="15px"
            v-for="i in 5"
            :key="i"
            class="pt-4"
          />
        </div>
        <div v-else>
          <div v-if="list.length > 0">
            <CalendarItem
              v-for="(item, idx) in list"
              :key="idx"
              :item="item"
              :query="keyword"
              @click="getDetailMeeting(item.id)"
            ></CalendarItem>
            <div class="text-center mt-7">
              <v-pagination
                rounded="1"
                elevation="2"
                size="small"
                v-model="currentPage"
                :length="pagination.totalPage"
                :total-visible="10"
                @update:model-value="changePage"
              ></v-pagination>
            </div>
          </div>
          <div v-else class="empty-illustration">
            <img
              :src="require('@/v2/assets/empty/no_available_state.svg')"
              class="img-no-available"
            />
          </div>
        </div>
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script setup lang="ts">
import { ref, onBeforeMount, watch, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { getColorChip } from "@/v2/helpers/color";
import CalendarItem from "@/v2/components/meeting-management/CalendarItem.vue";

const isLoading = ref<boolean>(false);

const router = useRouter();
const store = useStore();

const meetingFilter = computed(() => store.state.meetingStore.meetingFilter);
const keyword = ref<string>(meetingFilter.value.eventSearching);

const currentPage = ref<number>(1);
const list = ref<any>([]);
const pagination = ref<any>({
  totalData: 0,
  pageNo: 1,
  nextPageNo: 2,
  totalPage: 1,
  entriesPerPage: 10,
});

function getList(query: string) {
  if (query !== "" && query != null) {
    isLoading.value = true;

    store.commit("meetingStore/setMeetingFilter", {
      eventSearching: query,
      page: pagination.value.pageNo,
    });

    store
      .dispatch("meetingStore/getListEventByCalendarType", meetingFilter.value)
      .then((res: any) => {
        const data = res.responseData.data.map((el) => {
          return {
            ...el,
            color: getColorChip(el.eventTemplateType),
          };
        });
        list.value = data;
        pagination.value.pageNo = res.responseData.infoPage.pageNo;
        pagination.value.totalData = res.responseData.infoPage.totalData;
        pagination.value.totalPage = res.responseData.infoPage.totalPage;
        currentPage.value = pagination.value.pageNo;
      })
      .finally(() => {
        isLoading.value = false;
      });
  }
}
function changePage(curr: number) {
  pagination.value.pageNo = curr;
  getList(keyword.value);
}
function getDetailMeeting(id: string) {
  router.push({
    name: "v2.meeting-detail-description",
    params: { idEvent: id },
  });
}

watch(
  () => keyword.value,
  () => {
    pagination.value.pageNo = 1;
  }
);

onBeforeMount(() => {
  if (!meetingFilter.value.dateFilter) {
    router.replace({ name: "v2.meeting-management" });
    return;
  }
  getList(keyword.value);
});
</script>

<style scoped>
.btn-back {
  box-shadow: 0px 3px 7px 0px #85858540;
}
.empty-illustration {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}
:deep(.v-field) {
  border-radius: 15px;
}
:deep(.v-input--horizontal) {
  display: contents;
}
:deep(.v-pagination__item--is-active) {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%) !important;
  color: white !important;
  border-radius: 10px;
}
:deep(.v-pagination .v-btn) {
  border-radius: 10px;
  font-size: 15px;
  font-weight: bold;
}
:deep(.v-pagination__item) {
  color: #065695;
  border-radius: 10px;
  background: white;
}
:deep(.v-pagination__next) {
  color: #065695;
  border-radius: 10px;
  background: white;
}
:deep(.v-pagination__prev) {
  color: #065695;
  border-radius: 10px;
  background: white;
}
.color-grey {
  color: #4b4b4b;
}
</style>
