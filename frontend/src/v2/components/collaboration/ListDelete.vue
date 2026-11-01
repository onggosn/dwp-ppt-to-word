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
    <v-list-item
      v-for="item in data"
      :key="item.idBPDocMember"
      class="px-0 py-2 text-lg"
    >
      <template v-slot:title
        ><span
          :class="[
            item.isDelete ? 'text-default' : 'text-grey',
            'font-weight-400',
            'text-18',
          ]"
          >{{ item.name }}</span
        ></template
      >
      <template v-slot:prepend>
        <v-avatar color="#eaeaea" class="avatar-big">
          <img
            v-if="item.type === `person`"
            :src="
              item.isDelete
                ? require(`@/v2/assets/icon/person.svg`)
                : require(`@/v2/assets/icon/person-disable.svg`)
            "
          />
          <img
            v-else
            :src="
              item.isDelete
                ? require(`@/v2/assets/icon/people.svg`)
                : require(`@/v2/assets/icon/people-disable.svg`)
            "
          />
        </v-avatar>
      </template>

      <template v-slot:append>
        <v-btn
          class="pa-2 mr-2 shadow"
          min-width="0"
          @click="handleDelete(item.idBPDocMember)"
          :disabled="!item.isDelete"
        >
          <v-progress-circular
            v-if="isLoading && selected === item.idBPDocMember"
            indeterminate
            color="primary"
            :size="20"
          ></v-progress-circular>
          <v-icon v-else :color="item.isDelete ? 'red' : ''">mdi-delete</v-icon>
        </v-btn>
      </template>
    </v-list-item>
  </v-list>
</template>

<script setup lang="ts">
import { ref } from "vue";
const props = defineProps<{
  data: Array<{
    idBPDocMember: string;
    name: string;
    type: string;
    isDelete: boolean;
  }>;
  title: string;
  isLoading: boolean;
}>();
const emit = defineEmits(["deleted"]);
const selected = ref<string>();

function handleDelete(val: string) {
  selected.value = val;
  emit("deleted", val);
}
</script>

<style scoped>
.text-sm {
  display: block;
  font-size: 0.875rem;
  color: #a6abc7;
}

.text-grey {
  color: #9e9e9e;
}

.text-default {
  color: #3a416f;
}
.avatar-big {
  width: 50px;
  height: 50px;
}
</style>
