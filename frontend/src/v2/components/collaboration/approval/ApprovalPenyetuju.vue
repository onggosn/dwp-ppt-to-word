<template>
  <div v-for="(memberAdg, idx) in listAdg" :key="idx">
    <div class="d-flex justify-space-between mb-2">
      <div class="d-flex">
        <v-avatar class="mr-2 my-auto" color="#eaeaea">
          <img :src="require(`@/v2/assets/icon/person.svg`)" />
        </v-avatar>
        <div class="name-container my-auto text-left">
          <p class="name-primary">{{ memberAdg.name }}</p>
          <p class="name-jabatan">
            {{ memberAdg.grade }}
            <span
              v-if="
                isCheckedMembersAvailable &&
                memberAdg.name === meetingLeader.name &&
                memberAdg.id === meetingLeader.id
              "
            >
              (Pimpinan Rapat)
            </span>
          </p>
        </div>
      </div>
      <div class="my-auto">
        <input
          :checked="memberAdg.isPresent"
          @change="checkIsChecked($event, memberAdg.id, idx)"
          class="present-checkbox"
          type="checkbox"
          name=""
          id=""
        />
        <label class="pl-2" for="">Hadir</label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/* eslint-disable */
import { defineProps, defineEmits, PropType } from "vue";
import { TApprovalPenyetuju } from "@/v2/Type";

const props = defineProps({
  listAdg: {
    type: Array<TApprovalPenyetuju>,
    default: () => [],
  },
  meetingLeader: {
    type: Object,
    default: null,
  },
  isCheckedMembersAvailable: {
    type: Boolean,
    default: false,
  },
});

const emits = defineEmits(["handleChecked"]);

const checkIsChecked = (e, id, idx) => {
  const { checked } = e.target;
  emits("handleChecked", { checked, id, idx });
};
</script>

<style scoped>
.present-checkbox {
  accent-color: #02aa59;
}
.name-container > .name-primary {
  color: #3a416f;
  font-size: 20px;
}
.name-container > .name-jabatan {
  color: #babcca;
  font-size: 15px;
}
</style>
