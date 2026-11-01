<template>
  <v-autocomplete
    v-model="localValue"
    v-model:search="search"
    placeholder="Search Name"
    :items="items"
    variant="plain"
    class="searchbar"
    item-title="value"
    item-value="id"
    menu-icon=""
    :menu-props="{ offset: '16', class: 'searchbar-menu' }"
    :rules="rules"
    :required="isRequired"
    :hide-details="!isRequired"
  >
    <template v-slot:append-inner v-if="props.showSearchIcon">
      <img :src="require('@/v2/assets/icon/search.svg')" />
    </template>

    <template v-slot:item="{ props, item }">
      <v-list-item :title="item.raw.value" v-bind="props" class="py-3 px-6">
        <template v-slot:prepend>
          <v-avatar color="#eaeaea">
            <img
              v-if="item.raw.type === `person`"
              :src="require(`@/v2/assets/icon/person.svg`)"
            />
            <img v-else :src="require(`@/v2/assets/icon/people.svg`)" />
          </v-avatar>
        </template>
        <template v-slot:append>
          <v-icon style="color: #065695" v-if="props.appendIcon">
            mdi-plus-circle-outline
          </v-icon>
        </template>
        <v-list-item-subtitle v-if="item.raw.department">
          {{ item.raw.department }}
        </v-list-item-subtitle>
      </v-list-item>
    </template>
  </v-autocomplete>
</template>

<script setup lang="ts">
import { ref, computed, watch, PropType } from "vue";

type TItem = {
  id: string | number;
  value: string;
  type: string;
  department: string;
};

const props = defineProps({
  modelValue: {
    type: null as unknown as PropType<string | number | null>,
    default: null,
    required: false,
  },
  search: {
    type: null as unknown as PropType<string | number | null>,
    default: null,
    required: false,
  },
  items: {
    type: Array<TItem>,
  },
  appendIcon: {
    type: Boolean,
    default: true,
  },
  showSearchIcon: {
    type: Boolean,
    default: true,
  },
  rules: {
    type: Array,
  },
  isRequired: {
    type: Boolean,
  },
});
const emit = defineEmits(["update:modelValue", "update:search"]);

const search = ref(props.search);
const localValue = computed({
  get() {
    return props.modelValue;
  },
  set(newValue) {
    emit("update:modelValue", newValue);
  },
});

watch(
  () => search.value as string,
  (val: string) => {
    emit("update:search", val);
  }
);
</script>

<style lang="scss">
.searchbar {
  .v-field {
    box-shadow: 0 3px 7px 0 #85858540;
    border-radius: 0.625rem;
  }
  .v-field__input {
    border: none;
    padding: 0.625rem 1rem;
  }
  .v-field__append-inner {
    padding: 0.625rem !important;
    img {
      width: 24px;
      height: 24px;
      margin: 2px;
    }
  }
}
.searchbar-menu {
  .v-autocomplete__content {
    box-shadow: 0 3px 7px 0 #85858540;
    border-radius: 0.625rem;
  }
}
</style>
