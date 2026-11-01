<template>
  <template v-if="isLoading">
    <v-row>
      <v-col cols="12" v-for="i in 5" :key="i">
        <free-style-shimmer
          :is-loading="true"
          width="100%"
          height="4.3rem"
          border-radius="10px"
        />
      </v-col>
    </v-row>
  </template>

  <v-list v-if="!isLoading" class="pa-0">
    <span class="text-sm mb-3">{{ props.title }}</span>
    <div class="py-2" v-if="!isAssignment">
      <v-list-item class="px-0 py-2 text-lg">
        <template v-slot:append>
          <v-checkbox
            v-if="data[0].hasOwnProperty('isEdit')"
            label="Select All"
            color="success"
            hide-details
            class="mr-1"
            :disabled="disableCheckAll"
            v-model="selectAllEdit"
            @update:modelValue="handleCheckboxAllEdit"
          ></v-checkbox>
          <v-checkbox
            v-if="data[0].hasOwnProperty('isView')"
            label="Select All"
            color="success"
            hide-details
            class="mr-3"
            :disabled="props.isAdmin ? false : true"
            v-model="selectAllView"
            @update:modelValue="handleCheckboxAllView"
          ></v-checkbox>
          <v-checkbox
            v-if="data[0].hasOwnProperty('isDownload')"
            label="Select All"
            color="success"
            hide-details
            class="mr-3"
            v-model="selectAllDownload"
            @update:modelValue="handleCheckboxAllDownload"
          ></v-checkbox>
          <div class="spacer"></div>
        </template>
      </v-list-item>
    </div>

    <v-list-item v-for="item in data" :key="item.id" class="px-0 py-2 text-lg">
      <template v-slot:title>
        <span
          :class="[
            item.isDelete === true ? 'text-default' : 'text-grey',
            'text-18',
          ]"
          >{{ item.name }}
        </span>
        <span
          v-if="item.memberTypeName"
          :class="[getClass(item.memberTypeName), 'member-type']"
        >
          {{ item.memberTypeName }}
        </span>
      </template>
      <template v-slot:prepend>
        <v-avatar color="#eaeaea" class="avatar-big">
          <img
            v-if="item.type === `person`"
            :src="
              item.isDelete === true
                ? require(`@/v2/assets/icon/person.svg`)
                : require(`@/v2/assets/icon/person-disable.svg`)
            "
          />
          <img
            v-else
            :src="
              item.isDelete === true
                ? require(`@/v2/assets/icon/people.svg`)
                : require(`@/v2/assets/icon/people-disable.svg`)
            "
          />
        </v-avatar>
      </template>

      <template v-slot:append>
        <v-checkbox
          v-if="item.hasOwnProperty('isEdit')"
          label="Edit"
          color="success"
          v-model="isEdit"
          :value="item.id"
          hide-details
          class="mr-1"
          :disabled="!canDelete(item)"
          @update:modelValue="handleCheckboxEdit($event, item.id)"
        ></v-checkbox>
        <v-checkbox
          v-if="item.hasOwnProperty('isView')"
          label="View"
          color="success"
          v-model="isView"
          :value="item.id"
          hide-details
          class="mr-3"
          :disabled="props.isAdmin && item.isDelete === true ? false : true"
          @update:modelValue="handleCheckboxView($event, item.id)"
        ></v-checkbox>
        <v-checkbox
          v-if="item.hasOwnProperty('isDownload')"
          label="Download"
          color="success"
          v-model="isDownload"
          :value="item.id"
          hide-details
          class="mr-1"
          @update:modelValue="handleCheckboxDownload($event, item.id)"
          :disabled="!item.isDelete"
        ></v-checkbox>
        <v-menu
          v-if="isAssignment"
          location="bottom"
          transition="slide-y-transition"
          bottom
        >
          <template v-slot:activator="{ props }">
            <v-btn
              v-bind="props"
              color="#fff"
              class="pa-2 mr-2 shadow"
              elevation="1"
              min-width="0"
            >
              <v-icon icon="mdi-cog" color="#065695"></v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-btn
              :disabled="item.memberTypeName === 'Contributor'"
              block
              density="default"
              variant="text"
              style="letter-spacing: -0.1px"
              @click="changeStatus(item, 2)"
              >Make as Contributor</v-btn
            >
            <v-btn
              :disabled="item.memberTypeName === 'Participant'"
              block
              density="default"
              variant="text"
              style="letter-spacing: -0.1px"
              @click="changeStatus(item, 3)"
              >Make as Participant</v-btn
            >
          </v-list>
        </v-menu>
        <btn-delete
          v-if="isAssignment"
          :isIconButton="true"
          :title="'Delete Participant'"
          :btn-title="'Delete Participant'"
          :subtitle="'Are you sure delete this participant ?'"
          :description="''"
          :type="'assignment'"
          :positiveTextButton="'Delete'"
          @update="handleDelete(item.id, item.idAssignment)"
        />
        <v-btn
          v-else-if="!isAssignment && canDelete(item)"
          class="pa-2 mr-2 shadow"
          min-width="0"
          @click="
            props.type === 'admin'
              ? handleDelete(
                  item.username != null ? item.username : item.name,
                  item.id
                )
              : handleDelete(item.id, null)
          "
        >
          <v-icon>mdi-delete</v-icon>
        </v-btn>
        <div v-else class="mx-5" />
      </template>
    </v-list-item>
  </v-list>
  <v-btn
    v-if="props.type == ''"
    variant="flat"
    class="primary-gradient align-self-end mt-3"
    rounded="10"
    height="fit-content"
    @click="handleSave"
  >
    <div class="pa-3">Save</div>
  </v-btn>
</template>

<script setup lang="ts">
import { ref, toRaw, computed, watch, PropType } from "vue";
import { useRoute } from "vue-router";
import BtnDelete from "@/v2/components/utils/dialog/DeleteEventDialog.vue";
const props = defineProps({
  data: {
    type: Array as PropType<
      Array<{
        id: string;
        name: string;
        username: string;
        type: string;
        isEdit: boolean;
        isView: boolean;
        isDownload: boolean;
        isDelete: boolean;
        memberType: number;
        memberTypeName: string;
        idAssignment: string;
      }>
    >,
    default: () => [],
  },
  title: {
    type: String,
  },
  isLoading: {
    type: Boolean,
  },
  type: {
    type: String,
    default: "",
  },
  isAdmin: {
    type: Boolean,
    default: false,
  },
});

type MemberItem = {
  id: string;
  name: string;
  username: string;
  type: string;
  isEdit: boolean;
  isView: boolean;
  isDownload: boolean;
  isDelete: boolean;
  memberType: number;
  memberTypeName: string;
  idAssignment: string;
};

const route = useRoute();

watch(
  () => props.data,
  (newData) => {
    if (newData?.some((d) => d.isDownload)) {
      selectAllDownload.value = newData?.every((d) => d.isDownload);
    }
    if (newData?.some((d) => d.isView)) {
      selectAllView.value = newData?.every((d) => d.isView);
    }
    if (newData?.some((d) => d.isEdit)) {
      selectAllEdit.value = newData?.every((d) => d.isEdit);
    }
  }
);
const emit = defineEmits([
  "deleted",
  "editted",
  "saveOnChecked",
  "edittedMemberType",
]);

const selectAllEdit = ref(
  props.data.filter((d) => d.isEdit).length === props.data.length
);
const selectAllView = ref(
  props.data.filter((d) => d.isView).length === props.data.length
);
const selectAllDownload = ref(
  props.data.filter((d) => d.isDownload).length === props.data.length
);
const isEdit = ref<any>(props.data.filter((d) => d.isEdit).map((d) => d.id));
const isView = ref(props.data.filter((d) => d.isView).map((d) => d.id));
const isDownload = ref(props.data.filter((d) => d.isDownload).map((d) => d.id));

const disableCheckAll = computed(() => {
  const canDeleteCheck = props.data?.filter((d) => d.isDelete === false);
  if (props.data) return props.data.length === canDeleteCheck?.length;

  return false;
});

const isAssignment = computed(() => route.path.includes("assignment"));

function canDelete(item) {
  return !Object.hasOwnProperty.call(item, "isDelete") || item.isDelete;
}

function handleCheckboxEdit(data: string[], id: string) {
  const check = Object.values(isView.value);
  if (!check.includes(id) && data.includes(id)) isView.value.push(id);

  if (data.length === props.data.length) {
    selectAllEdit.value = true;
  } else {
    selectAllEdit.value = false;
  }

  if (props.type == "admin") {
    //save on checked
    props.data.map((d) => {
      d.isEdit = isEdit.value.includes(d.id);
      return d;
    });
    const findObjectById = (id) => props.data.find((obj) => obj.id === id);
    const object = findObjectById(id);
    emit("saveOnChecked", object);
  }
}
function handleCheckboxView(data: Array<string>, item: string) {
  if (data.length === props.data.length) {
    selectAllView.value = true;
  } else {
    selectAllView.value = false;
  }

  if (props.type == "nonSector") {
    //save on checked
    props.data.map((d) => {
      d.isView = isView.value.includes(d.id);
      return d;
    });
    const findObjectById = (id) => props.data.find((obj) => obj.id === id);
    const object = findObjectById(item);
    emit("saveOnChecked", object);
  }
}

function handleCheckboxDownload(data: Array<string>, item: string) {
  if (data.length === props.data.length) {
    selectAllDownload.value = true;
  } else {
    selectAllDownload.value = false;
  }
  //save on checked
  props.data.map((d) => {
    d.isDownload = isDownload.value.includes(d.id);
    return d;
  });
  const findObjectById = (id) => props.data.find((obj) => obj.id === id);
  const object = findObjectById(item);
  emit("saveOnChecked", object);
}

function handleCheckboxAllEdit(val: boolean | null) {
  if (props.type === "admin") {
    if (val) {
      // When "Select All" is checked, add IDs of items with isDelete: true to isEdit.value
      const deletableIds = props.data
        .filter((d) => d.isDelete)
        .map((d) => d.id);
      isEdit.value = [...new Set([...isEdit.value, ...deletableIds])]; // Avoid duplicates
    } else {
      // When "Select All" is unchecked, remove IDs of items with isDelete: true from isEdit.value
      const deletableIds = props.data
        .filter((d) => d.isDelete)
        .map((d) => d.id);
      isEdit.value = isEdit.value.filter((id) => !deletableIds.includes(id));
    }

    // Update selectAllEdit to reflect if all items with isDelete: true are selected
    const allDeletableSelected = props.data
      .filter((d) => d.isDelete)
      .every((d) => isEdit.value.includes(d.id));
    selectAllEdit.value = allDeletableSelected;

    props.data.forEach((d) => {
      if (d.isDelete) {
        d.isEdit = val ?? false;
      }
    });
    // Emit the updated props.data
    emit("saveOnChecked", props.data);
  } else {
    if (val) {
      isEdit.value = props.data.map((d) => d.id);
      isView.value = isEdit.value;
      selectAllView.value = true;
    } else {
      isEdit.value = props.data.map((item) => {
        if (!item.isDelete) return item.id;

        return;
      });
    }
  }
}
function handleCheckboxAllView(val: boolean | null) {
  if (val) {
    isView.value = props.data.map((d) => d.id);
  } else if (isEdit.value.length > 0) {
    isView.value = isEdit.value;
  } else {
    isView.value = [];
  }
  if (props.type == "nonSector") {
    //save on checked
    const newData = toRaw(props.data).map((d) => {
      d.isView = isView.value.includes(d.id);
      return d;
    });
    emit("saveOnChecked", newData);
  }
}

function handleCheckboxAllDownload(val: boolean | null) {
  if (val) {
    isDownload.value = props.data.map((d) => d.id);
  } else {
    isDownload.value = [];
  }
  //save on checked
  const newData = toRaw(props.data).map((d) => {
    d.isDownload = isDownload.value.includes(d.id);
    return d;
  });
  emit("saveOnChecked", newData);
}

function handleSave() {
  const newData = toRaw(props.data).map((item) => {
    const { id, ...rest } = item;
    return {
      ...rest,
      idEFormMember: id,
      isEdit: isEdit.value.includes(id),
      isView: isView.value.includes(id),
    };
  });
  emit("editted", newData);
}

function changeStatus(data: MemberItem, memberType: number) {
  emit("edittedMemberType", data, memberType);
}

function getDisableCondition(id: string) {
  const check = Object.values(isEdit.value);
  if (check.includes(id)) return true;

  return false;
}

function handleDelete(val: string, val2: string | null) {
  emit("deleted", val, val2);
}

function getClass(memberType) {
  switch (memberType) {
    case "Contributor":
      return "contributor";
    case "Participant":
      return "participant";
    default:
      return "";
  }
}

watch(
  () => props.data,
  (newData) => {
    isEdit.value = newData.filter((d) => d.isEdit).map((d) => d.id);
    isView.value = newData.filter((d) => d.isView).map((d) => d.id);
    isDownload.value = newData.filter((d) => d.isDownload).map((d) => d.id);
  }
);
</script>

<style scoped>
.text-sm {
  display: block;
  font-size: 0.875rem;
  color: #a6abc7;
}

:deep(.v-list-item-title) {
  font-size: 1.25rem;
  color: #3a416f;
}

.avatar-big {
  width: 50px;
  height: 50px;
}

:deep(.mdi-delete) {
  background: linear-gradient(#d6212a, #ff000d);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.spacer {
  width: 42px;
  height: 36px;
}

:deep(.v-label) {
  width: 90px;
  color: #3a416f;
  opacity: 1;
}

.member-type {
  display: inline-block;
  border-radius: 16px !important;
  margin-left: 8px !important;
  font-size: 14px !important;
  padding: 4px 8px 4px 8px !important;
}

.contributor {
  background-color: #ffedfe !important;
  color: #ab0fa6 !important;
}
.participant {
  background-color: #e9f5ff !important;
  color: #2279bd !important;
}
.text-grey {
  color: #9e9e9e;
}
.text-default {
  color: #3a416f;
}
</style>
