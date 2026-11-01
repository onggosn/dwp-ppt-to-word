import { ref, reactive, computed } from "vue";
import { useStore } from "vuex";

export function useCreateAIUDialog() {
  const store = useStore();

  // Dialog state
  const dialog = ref(false);
  const currentTitle = ref("");
  const step = ref(1);
  const buttonNext = ref(false);
  const datePicker = ref<any>();

  // Error state
  const errorState = ref({
    message: "",
    hasError: false,
  });

  // Stepper configuration
  const tabs = reactive([
    {
      title: "Step 1",
      iconSuccess: null,
      isValid: true,
    },
    {
      title: "Step 2",
      iconSuccess: null,
      isValid: true,
    },
  ]);

  // Progress computed
  const progress = computed(() => {
    return store.getters["loadingStore/getProgress"];
  });

  const isShowDialog = computed(() => {
    return progress.value >= 0 && progress.value <= 100;
  });

  // Dialog management functions
  const showDialogEvent = (titleParam?: string) => {
    currentTitle.value = titleParam || "";
    dialog.value = true;
  };

  const closeDialog = () => {
    step.value = 1;
    dialog.value = false;
    datePicker.value = null;
    buttonNext.value = false;
    errorState.value.message = "";
    errorState.value.hasError = false;
    currentTitle.value = "";
  };

  // Step navigation
  const nextStep = () => {
    if (step.value < tabs.length) {
      step.value++;
    }
  };

  const previousStep = () => {
    if (step.value > 1) {
      step.value--;
    }
  };

  const goToStep = (stepNumber: number) => {
    if (stepNumber >= 1 && stepNumber <= tabs.length) {
      step.value = stepNumber;
    }
  };

  // Button validation
  const validateButtonState = (
    state: any,
    formRequest: any,
    currentStep: number
  ) => {
    if (currentStep === 1) {
      buttonNext.value =
        state._eventType !== null &&
        state._rdgType !== null &&
        state._month !== null &&
        state._year !== null &&
        state._rdg !== null;
    } else if (currentStep === 2) {
      const allFormsValid = formRequest.forms.every(
        (form: any) => form.id !== null
      );
      buttonNext.value = formRequest.sector !== null && allFormsValid;
    }
  };

  // Error handling
  const setError = (message: string) => {
    errorState.value.message = message;
    errorState.value.hasError = true;
  };

  const clearError = () => {
    errorState.value.message = "";
    errorState.value.hasError = false;
  };

  return {
    // State
    dialog,
    currentTitle,
    step,
    buttonNext,
    datePicker,
    errorState,
    tabs,

    // Computed
    progress,
    isShowDialog,

    // Methods
    showDialogEvent,
    closeDialog,
    nextStep,
    previousStep,
    goToStep,
    validateButtonState,
    setError,
    clearError,
  };
}
