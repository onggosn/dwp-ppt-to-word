import { computed } from "vue";
import { useStore } from "vuex";

export function useInitializeConfig() {
  const store = useStore();

  const initializeConfig = computed(
    () => store.getters["userStore/getInitializeConfig"]
  );

  const firebaseConfig = computed(() => initializeConfig.value?.firebase ?? {});
  const dataDogConfig = computed(() => initializeConfig.value?.dataDog ?? {});
  const ckEditorConfig = computed(() => initializeConfig.value?.ckEditor ?? {});

  const ckEditorLicense = computed(() => ckEditorConfig.value?.license || "");

  return {
    initializeConfig,
    firebaseConfig,
    dataDogConfig,
    ckEditorConfig,
    ckEditorLicense,
  };
}
