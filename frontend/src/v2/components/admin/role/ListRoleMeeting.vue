<template>
  <v-expansion-panels v-model="panel">
    <v-expansion-panel :value="item.id">
      <v-expansion-panel-title>
        <v-row align="center">
          <v-col cols="7">
            <p class="font-weight-bold ellipsis-1">
              {{ item?.name }}
            </p>
          </v-col>
        </v-row>
      </v-expansion-panel-title>
      <v-expansion-panel-text>
        <v-row v-if="loading" class="mx-5 my-5">
          <v-col v-for="i in 3" :key="i" cols="12">
            <free-style-shimmer
              width="100%"
              height="40px"
              border-radius="10px"
              color="#d3d3d3"
            />
          </v-col>
        </v-row>
        <template v-else>
          <div
            class="d-flex flex-wrap ml-auto ga-2"
            style="justify-content: flex-end"
          >
            <div class="pr-2">
              <v-btn
                class="rounded-lg px-2 font-weight-bold"
                min-width="0"
                color="#065695"
                variant="outlined"
                @click="form_create_member.onOpen(item.id)"
              >
                + Add Member
              </v-btn>
            </div>
          </div>
          <div v-for="(list, index) in items" :key="index">
            <SubsectionRole
              :item="list"
              @on-delete-role="onDeleteRole(item?.id)"
            />
          </div>

          <FormCreateMember
            ref="form_create_member"
            @onClose="getListAllMemberbyMRoleId(panel)"
          />
        </template>
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script setup lang="ts">
import SubsectionRole from "@/v2/components/admin/role/SubsectionRole.vue";
import FormCreateMember from "@/v2/components/admin/roleMember/FormCreate.vue";
import { defineProps, ref, watch } from "vue";
import { useStore } from "vuex";
import { TUserInfoAdmin } from "@/v2/Type";
import { useRoute } from "vue-router";
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
});

const form_create_member = ref();
const loading = ref<boolean>(false);
const panel = ref<number[]>([]);
const items = ref<TUserInfoAdmin[]>([]);

const store = useStore();
const route = useRoute();

watch(panel, (newValue) => {
  if (newValue) getListAllMemberbyMRoleId(newValue);
});

const getListAllMemberbyMRoleId = async (id: number | number[]) => {
  loading.value = true;
  const payload = {
    roleSearching: store.getters["globalStore/getSearch"],
    idMrole: id,
    sortBy: parseInt((route.query.eventSort as string) ?? 0),
    satkerFilter: store.getters["adminStore/getItemsFilter"].satkerFilter ?? [
      0,
    ],
    gradeFilter: store.getters["adminStore/getItemsFilter"].gradeFilter ?? [0],
  };

  items.value = await store.dispatch(
    "adminStore/getListAllMemberbyMRoleId",
    payload
  );
  loading.value = false;
};

const onDeleteRole = (id) => {
  getListAllMemberbyMRoleId(id);
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
:deep(.v-expansion-panel-title) {
  min-height: 60px;
}
</style>
