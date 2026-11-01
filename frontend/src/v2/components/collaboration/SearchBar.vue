<template>
  <v-autocomplete
    hide-details
    v-model:search="searchName"
    :placeholder="placeHolderSearch"
    :items="items"
    variant="plain"
    class="searchbar"
    item-title="value"
    return-object
    menu-icon=""
    :menu-props="{ offset: '16', class: 'searchbar-menu' }"
    @update:modelValue="handleAdd"
    @input="debouncedSearch"
    :loading="isLoading"
    :multiple="copasable || false"
    :model-value="modelValue"
  >
    <!-- multiple selection if copasable is true, change the "|| false" condition if there any new requirements -->
    <template v-if="hideIcon === false" v-slot:append-inner>
      <img :src="require('@/v2/assets/icon/search.svg')" />
    </template>

    <template v-slot:chip="{ props, item, index }">
      <v-chip
        variant="flat"
        v-bind="props"
        class="px-3 mx-1"
        :style="{
          borderRadius: '0.25rem',
          border: `1px solid ${item.value.id ? '#2279bd' : '#f44336'}`,
          backgroundColor: item.value.id ? '#e9f5ff' : '#f5e9e9',
        }"
      >
        <template v-slot:default>
          <span :style="{ color: item.value.id ? '#2279bd' : '#f44336' }">{{
            item.value.value ?? item.value.inputEmail
          }}</span>
        </template>
        <template v-slot:append>
          <v-btn
            class="pl-2 pr-0"
            @click="() => handleRemoveSelectedItem(index)"
            style="
              min-width: 0;
              box-shadow: none;
              background-color: transparent;
            "
          >
            <v-icon :style="{ color: item.value.id ? '#2279bd' : '#f44336' }"
              >mdi-close</v-icon
            >
          </v-btn>
        </template>
      </v-chip>
    </template>
    <template v-slot:item="{ props, item }">
      <v-list-item v-bind="props" class="py-3 px-6" v-if="item.value.id">
        <template v-slot:prepend>
          <v-avatar color="#eaeaea">
            <img
              v-if="(item as any).raw.isGroup === false"
              :src="require(`@/v2/assets/icon/person.svg`)"
            />
            <img v-else :src="require(`@/v2/assets/icon/people.svg`)" />
          </v-avatar>
        </template>

        <template v-slot:append>
          <v-icon style="color: #065695">mdi-plus-circle-outline</v-icon>
        </template>
      </v-list-item>
    </template>
  </v-autocomplete>

  <div v-if="copasable" class="d-flex justify-end pt-3">
    <v-btn
      class="primary-gradient"
      style="border-radius: 0.5rem"
      @click="submitAll"
      :disabled="!canSubmitAll"
      >Add</v-btn
    >
  </div>
</template>

<script setup lang="ts">
import { ref, PropType, computed, getCurrentInstance } from "vue";
import { TResponseSearchByName, TResponseBase } from "@v2/Type";
import clientv2 from "@v2/library/ApiClient";
import { useRoute } from "vue-router";
import { useStore } from "vuex";
import { debounce } from "lodash";
import { responsePromise } from "@/v2/helpers/utils";
type TAccessType =
  | "page"
  | "approved"
  | "timTeknis"
  | "section"
  | "role"
  | "organizer";

const props = defineProps({
  type: {
    type: String,
    default: "",
  },
  accessType: {
    type: String as PropType<TAccessType>,
    default: "",
  },
  isAdmin: {
    type: Boolean,
    default: false,
  },
  placeHolderSearch: {
    type: String,
    default: "Enter Name",
  },
  hideIcon: {
    type: Boolean,
    default: false,
  },
  copasable: {
    type: Boolean,
    default: false,
  },
  onSubmit: {
    type: Function as PropType<
      (value: TResponseSearchByName[]) => Promise<void>
    >,
    default: null,
  },
});
const emit = defineEmits<{ (e: "selected", value: TResponseSearchByName) }>();
const searchName = ref<any>();
const items = ref<any>();
const route = useRoute();
const store = useStore();
const isLoading = ref(false);
const modelValue = ref<any>();
const { root } = getCurrentInstance() as any;
const response = responsePromise(root);

const trimSearch = () => {
  return (searchName.value as string)
    .replace(/"/g, "")
    .split(";")
    .map((part) => {
      if (part.trim() === "") return; // Skip empty parts
      const regex = /<[^>]*@[^>]*>/;
      const matchingMail = part.match(regex);
      if (matchingMail !== null) {
        return matchingMail[0].slice(1, -1);
      } else {
        return part.trim();
      }
    })
    .filter((v): v is string => !!v);
};

const matchingTrimmedSearch = (trimmed: string[], target: any[]) => {
  if (modelValue.value == undefined || modelValue.value == null) {
    modelValue.value = [];
  }
  searchName.value.includes(";") &&
    trimmed.forEach((searchItem) => {
      const matchedItem = (target as Array<any>).find(
        (item: any) =>
          item.value.toLowerCase().includes(searchItem.toLowerCase()) ||
          item.inputEmail.toLowerCase().includes(searchItem.toLowerCase())
      );

      if (matchedItem) modelValue.value.push(matchedItem);
      if (target && !matchedItem) {
        modelValue.value.push({
          id: null,
          value: searchItem.includes("@") ? null : searchItem,
          inputEmail: searchItem.includes("@") ? searchItem : null,
          isGroup: false,
          organizationName: "",
        });
      }
    });
};

function handleAdd(val: TResponseSearchByName | null) {
  if (val !== null) {
    if (props.copasable) {
      searchName.value = ""; // Clear the search input after selecting an item
      items.value = []; // Clear the items list after selecting an item

      modelValue.value = val; // Set the model value to the selected item
      return; // If copasable is true, we set the model value to the selected item and return early to allow multiple selections without emitting the event immediately
    }
    emit("selected", val);
  }
}

const canSubmitAll = computed(() => {
  if (!props.copasable) return false; // If copasable is false, the submit button should not be enabled
  return (
    modelValue.value &&
    modelValue.value.length > 0 &&
    !modelValue.value.some((item: any) => !item.id)
  ); // Enable submit if there are selected items
});
const submitAll = () => {
  if (!props.copasable) return; // If copasable is false, do nothing on submit
  modelValue.value &&
    props.onSubmit &&
    props
      .onSubmit(modelValue.value)
      .then(() => {
        // Handle any post-submit logic if needed
        items.value = []; // Clear the items list after submission if needed
        modelValue.value = []; // Clear the selected items after successful submission
      })
      .catch(response.error); // Call the onSubmit prop with the selected items
};

const handleRemoveSelectedItem = (index: number) => {
  if (Array.isArray(modelValue.value)) {
    modelValue.value.splice(index, 1);
  }
};

const debouncedSearch = debounce(function () {
  if (searchName.value.length <= 1) {
    items.value = [];
    return;
  }

  isLoading.value = true;
  if (props.isAdmin) {
    if (props.accessType === "role") {
      searchAdmin();
    } else if (
      props.accessType === "page" ||
      props.accessType === "approved" ||
      props.accessType === "timTeknis" ||
      props.accessType === "organizer"
    ) {
      searchBySector();
    } else {
      searchByNonSector();
    }
  } else {
    if (props.type === "assignment") {
      searchMemberAssignment();
    } else if (props.type === "nonSector") {
      searchByNonSector();
    } else if (props.type === "global") {
      searchByGlobal();
    } else if (props.type === "user-group") {
      searchUserGroup();
    } else if (props.type === "material") {
      searchByUserAndGroupMaterial();
    } else {
      searchBySector();
    }
  }
}, 500);

function searchByGlobal() {
  store
    .dispatch("userStore/fetchSearchUserNew", {
      query: searchName.value,
      isEvent: false,
    })
    .then((res) => {
      items.value = res;
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function searchUserGroup() {
  store
    .dispatch("userStore/fetchSearchUser", {
      query: searchName.value,
      isEvent: false,
    })
    .then((res) => {
      items.value = res;
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function searchByNonSector() {
  if (props.isAdmin) {
    const reqData = {
      name: searchName.value,
      type: "Page",
    };
    clientv2
      .SearchUserAndGrupIdByNameAndSectorTemplate({ data: reqData })
      .then((res: TResponseBase<TResponseSearchByName>) => {
        items.value = res.responseData;
      })
      .finally(() => {
        isLoading.value = false;
      });
  } else {
    const payload = {
      name: searchName.value,
      idEvent: route.params.idEvent,
    };
    store
      .dispatch(
        "materialStore/searchEventPresentationMaterialByUsernameAndGroupId",
        payload
      )
      .then((resp: TResponseBase<string[]>) => {
        items.value = resp;
      })
      .finally(() => {
        isLoading.value = false;
      });
  }
}

function searchBySector() {
  const trimmedSearch: string[] = trimSearch();

  const reqData = {
    name: trimmedSearch.length > 0 ? trimmedSearch : searchName.value,
    idbpDocument: route.params.idDoc,
    type: props.accessType,
  };

  clientv2
    .SearchUserAndGrupIdByNameAndSector({ data: reqData })
    .then((res) => {
      items.value = [...(res as Array<any>)];
      matchingTrimmedSearch(trimmedSearch, [...res]); // Check for matches with the trimmed search terms and add them to the model value if they don't exist in the search results
      searchName.value.includes(";") && (searchName.value = ""); // Clear the search input after getting results
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function searchByUserAndGroupMaterial() {
  const trimmedSearch: string[] = trimSearch();

  const reqData = {
    name: trimmedSearch,
    idEvent: route.params.idEvent,
  };

  clientv2
    .SearchUserAndGroupMaterial({ data: reqData })
    .then((res) => {
      items.value = [...(res as Array<any>)];
      matchingTrimmedSearch(trimmedSearch, [...res]); // Check for matches with the trimmed search terms and add them to the model value if they don't exist in the search results
      searchName.value.includes(";") && (searchName.value = ""); // Clear the search input after getting results
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function searchAdmin() {
  if (props.type === "satker") {
    const reqData = {
      satkerPembuat: searchName.value,
    };
    clientv2
      .SearchSatker({ data: reqData })
      .then((res) => {
        const transformedData = res.responseData?.data.map((item) => ({
          id: item.id,
          value: item.organizationName,
          isGroup: item.isGroup,
          organizationName: item.organizationName,
        }));
        items.value = transformedData;
      })
      .finally(() => {
        isLoading.value = false;
      });
  } else if (props.type === "doctype") {
    const reqData = {
      documentType: searchName.value,
    };
    store
      .dispatch("documentsStore/SearchDocumentType", reqData)
      .then((resp) => {
        const transformedData = resp.responseData.map((item) => ({
          id: item.id,
          value: item.id,
          documentName: item.documentName,
        }));
        items.value = transformedData;
      })
      .finally(() => {
        isLoading.value = false;
      });
  } else if (props.type === "jabatan") {
    const reqData = {
      jabatanname: searchName.value,
    };
    clientv2
      .SearchJabatan({ data: reqData })
      .then((res) => {
        const transformedData = res.responseData.data.map((item) => ({
          id: item.id,
          value: item.JabatanName,
          JabatanName: item.JabatanName,
        }));
        items.value = transformedData;
      })
      .finally(() => {
        isLoading.value = false;
      });
  } else if (props.type === "role") {
    const reqData = {
      rolename: searchName.value,
    };
    clientv2
      .SearchRole({ data: reqData })
      .then((res) => {
        const transformedData = res.responseData.data.map((item) => ({
          id: item.id,
          value: item.RoleName,
          RoleName: item.RoleName,
        }));
        items.value = transformedData;
      })
      .finally(() => {
        isLoading.value = false;
      });
  }
}

function searchMemberAssignment() {
  const trimmedSearch: string[] = trimSearch();
  const reqData = {
    name: trimmedSearch,
    isEvent: false, // mengikuti parameter di edit Event (?)
  };

  clientv2
    .SearchUserAndGroupNew({ data: reqData })
    .then((res) => {
      if (Array.isArray(res)) {
        items.value = [...res];
        matchingTrimmedSearch(trimmedSearch, [...res]); // Check for matches with the trimmed search terms and add them to the model value if they don't exist in the search results
        searchName.value.includes(";") && (searchName.value = ""); // Clear the search input after getting results
      }
    })
    .finally(() => {
      isLoading.value = false;
    });
}
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
*.v-btn--disabled {
  pointer-events: auto !important;
  cursor: not-allowed !important;
}
</style>
