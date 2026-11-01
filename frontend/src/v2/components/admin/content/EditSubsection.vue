<template>
  <Teleport to="body">
    <v-dialog v-model="isOpen" :max-width="900" persistent>
      <v-card class="mb-5 border-radius-dwp">
        <v-card-title class="d-flex justify-center align-center">
          <div class="text-18 text-blueTheme fw-500 mt-2 mb-2">
            {{ isSubChild ? "Edit Section Title" : "Edit Sub Section Title" }}
          </div>
          <v-btn
            class="mr-2"
            style="position: absolute; right: 0"
            variant="text"
            icon="mdi-close"
            @click="closeDialog"
          ></v-btn>
        </v-card-title>
        <div class="separatorHorizontalGradient"></div>
        <v-card-text class="pb-0">
          <div v-if="!isSubChild">
            <span class="text-darkBlue font-weight-bold form-title"
              >Document Title</span
            >
            <v-text-field
              :value="item?.bPDocumentName"
              variant="solo"
              placeholder="Insert Section Title"
              class="my-3"
              disabled
            ></v-text-field>
          </div>
          <span class="text-darkBlue font-weight-bold form-title">{{
            isSubChild ? "Content Title" : "Section Title"
          }}</span>
          <v-text-field
            v-model="eformTitle"
            variant="solo"
            placeholder="Insert Section Title"
            class="my-3"
            disabled
          ></v-text-field>
          <v-row
            class="rounded-lg px-2 mt-2 mx-2 mb-5"
            style="border: 2px #babcca solid"
          >
            <v-col cols="12">
              <p class="pb-1 text-left text-darkBlue font-weight-bold">
                {{ isSubChild ? "Section Title" : "Sub Section Title"
                }}<span class="text-gradient-red">*</span>
              </p>
              <v-text-field
                v-model="state.title"
                variant="solo"
                placeholder="Insert Section Title"
                :error-messages="
                  getErrorMessages(v$.title, {
                    required: 'Required',
                  })
                "
              ></v-text-field>
              <div v-if="isSectorVisible && !haveChild" class="w-100">
                <span class="text-darkBlue font-weight-bold form-title"
                  >Sector<span class="text-gradient-red">*</span></span
                >
                <v-radio-group
                  v-model="state.idSector"
                  inline
                  class="mt-3"
                  :error-messages="v$.idSector.$errors.map((e) => 'Required')"
                >
                  <div class="w-100">
                    <v-radio
                      v-for="(sectorItem, index) in listSector"
                      :key="index"
                      :value="sectorItem.id"
                      :label="sectorItem.value"
                      color="#065695"
                      class="me-5"
                    />
                  </div>
                </v-radio-group>
              </div>
              <div v-if="isSection">
                <span class="text-darkBlue font-weight-bold form-title"
                  >Do you want to make it as a header?<span
                    class="text-gradient-red"
                    >*</span
                  ></span
                >
                <v-radio-group
                  v-model="state.isHeader"
                  class="mt-3"
                  :error-messages="v$.isHeader.$errors.map((e) => 'Required')"
                >
                  <div class="d-flex w-50">
                    <v-radio :value="true" label="Yes" color="#065391" />
                    <v-radio :value="false" label="No" color="#065391" />
                  </div>
                </v-radio-group>
              </div>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions class="d-flex justify-end px-6 pb-4 pt-0 form-action">
          <v-btn
            elevation="3"
            style="color: #065695"
            class="item-btn font-weight-medium"
            @click="closeDialog"
          >
            Cancel
          </v-btn>
          <v-btn
            elevation="3"
            color="#065695"
            size="large"
            class="item-btn item-add"
            style="color: white"
            @click="handleCreate"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </Teleport>
</template>
<script setup lang="ts">
import { reactive, ref, getCurrentInstance, computed } from "vue";
import useVuelidate from "@vuelidate/core";
import { helpers, required, requiredIf } from "@vuelidate/validators";
import { useStore } from "vuex";
import { semicolonRegex, getErrorMessages } from "@/v2/helpers/validation";
import { secureRandomFloat } from "@/v2/helpers/utils";
import { DocTypeToSectorMap } from "@/v2/enum/Enum";
const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
});

const isOpen = ref<boolean>(false);
const idMEFormTemplate = ref<number>(0);
const eformTitle = ref<string>("");
const isSection = ref<string>("");
const haveChild = ref<boolean>(false);
const isSubChild = ref<boolean>(false);
const listSector = ref<any[]>([]);
const { root } = getCurrentInstance() as any;
const store = useStore();
const emit = defineEmits(["onSuccess"]);
const isSectorVisible = computed(() =>
  Object.keys(DocTypeToSectorMap).some((key) => props.item[key])
);
const state = reactive({
  title: "",
  isHeader: false,
  idSector: null,
});
const rules = computed(() => {
  const localRule = {
    title: {
      required,
      semicolonRegex: helpers.withMessage(
        "Invalid input. Avoid using semicolon (;)",
        semicolonRegex
      ),
    },
    isHeader: { required },
    idSector: {
      required: requiredIf(() => isSectorVisible.value && !haveChild.value),
    },
  };

  return localRule;
});

function openDialog(list: any, title: string) {
  isSubChild.value = list.isSection;
  eformTitle.value = isSubChild.value ? props.item.bPDocumentName : title;
  idMEFormTemplate.value = list.idMEFormTemplate;
  isSection.value = list.isSection;
  haveChild.value = list.childSection?.length > 0;
  state.title = list.bPEFormLabel;
  state.isHeader = list.isHeader;
  state.idSector = list.idSector;
  isOpen.value = true;
}

function closeDialog() {
  isOpen.value = false;
}

const v$ = useVuelidate(rules, state);

store.dispatch("eFormStore/getListSectorPredefine").then(({ responseData }) => {
  const matchedEntry = Object.entries(DocTypeToSectorMap).find(
    ([key]) => props.item[key]
  );
  if (matchedEntry) {
    listSector.value = responseData.filter(
      (item) => item.type === matchedEntry[1]
    );
  }
});

async function handleCreate() {
  const result = await v$.value.$validate();
  if (!result) return;

  const payload = {
    idMEformTemplate: idMEFormTemplate.value,
    name: state.title,
    isSection: isSection.value,
    isHeader: state.isHeader,
    idSector: state.idSector,
    idMBPDocumentTemplate: props.item?.idMBPDocumentTemplate,
  };

  store
    .dispatch("adminStore/updateContentChildList", payload)
    .then(() => {
      store.commit("adminStore/setRefreshList", secureRandomFloat());
      root.refs.toast.show({
        message: "Successfully Changed",
        color: "success",
        timeout: 3000,
      });
    })
    .catch(() => {
      root.refs.toast.show({
        message: "Failed edit Section",
        color: "error",
        timeout: 3000,
      });
    })
    .finally(() => {
      emit("onSuccess", true);
      closeDialog();
    });
}

defineExpose({ openDialog });
</script>
<style scoped>
:deep(.v-field--variant-solo, .v-field.v-field--appended) {
  border-radius: 12px !important;
}
:deep(.v-field--disabled) {
  background-color: rgb(196, 186, 186) !important;
}
.form-action {
  gap: 0.5rem;
  display: flex;
  justify-content: end;
  align-items: center;
  button {
    border-radius: 10px !important;
  }
}
.item-btn {
  height: 45px !important;
  font-size: 15px !important;
  padding-left: 1rem;
  padding-right: 1rem;
}
.item-btn.item-add {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
}
</style>
