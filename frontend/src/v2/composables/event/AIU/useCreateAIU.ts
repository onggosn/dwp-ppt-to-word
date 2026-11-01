import { watch, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { responsePromise } from "@/v2/helpers/utils";
import { getCurrentInstance } from "vue";
import { useCreateAIUForm } from "./useCreateAIUForm";
import { useCreateAIUAPI } from "./useCreateAIUAPI";
import { useCreateAIUValidation } from "./useCreateAIUValidation";
import { useCreateAIUDialog } from "./useCreateAIUDialog";

export function useCreateAIU() {
  const store = useStore();
  const router = useRouter();
  const { root } = getCurrentInstance() as any;
  const response = responsePromise(root);

  // Initialize composables
  const formComposable = useCreateAIUForm();
  const apiComposable = useCreateAIUAPI();
  const dialogComposable = useCreateAIUDialog();
  const validationComposable = useCreateAIUValidation(
    formComposable.formRequest
  );

  const {
    state,
    formRequest,
    listMonths,
    resetForm,
    addForm,
    deleteForm,
    getYearPickerData,
  } = formComposable;

  const {
    isLoading,
    loadingList,
    listEventType,
    listRDGType,
    listRDG,
    sectorList,
    fetchEventTypes,
    fetchRDGTypes,
    fetchRDGList,
    fetchSectorList,
    fetchFormList,
    createAIUCustom,
    resetAPIData,
  } = apiComposable;

  const {
    dialog,
    currentTitle,
    step,
    buttonNext,
    datePicker,
    errorState,
    tabs,
    progress,
    isShowDialog,
    showDialogEvent: showDialog,
    closeDialog,
    nextStep,
    previousStep,
    validateButtonState,
  } = dialogComposable;

  const { v$, isManualAIU, validateForm, resetValidation, getErrorMessages } =
    validationComposable;

  // Initialize dialog with API calls
  const showDialogEvent = (titleParam?: string) => {
    showDialog(titleParam);
    fetchEventTypes().then((data) => {
      listEventType.value = data;
    });

    const req = {
      sectorName: "",
    };

    fetchRDGTypes(req).then((data) => {
      listRDGType.value = data;
    });
  };

  // Watch for form validation in step 1
  watch([state], () => {
    validateButtonState(state, formRequest, step.value);
  });

  // Watch for changes in step 1 form fields
  watch(
    [
      () => state._eventType,
      () => state._rdgType,
      () => state._month,
      () => state._year,
    ],
    () => {
      if (
        step.value === 1 &&
        state._eventType !== null &&
        state._rdgType !== null &&
        state._month !== null &&
        state._year !== null
      ) {
        state._rdg = null;
        listRDG.value = [];
        const payload = {
          rdgType: state._rdgType.id,
          month: state._month.id,
          year: state._year,
          BPName: currentTitle.value,
        };

        fetchRDGList(payload).then((data) => {
          listRDG.value = data;
        });
      }
    }
  );

  // Watch for RDG changes
  watch(
    () => state._rdg,
    (val) => {
      formRequest.sector = null;
      formRequest.forms = [
        {
          id: null,
          name: null,
        },
      ];
      sectorList.value = [];
      if (val) {
        fetchSectorList().then((res) => {
          sectorList.value = res;
        });
      }
    }
  );

  // Watch for form validation in step 2
  watch([formRequest], () => {
    validateButtonState(state, formRequest, step.value);
  });

  // Watch for step changes
  watch(step, (val) => {
    validateButtonState(state, formRequest, val);
  });

  // Watch for sector changes
  watch(
    () => formRequest.sector,
    (val) => {
      if (val) {
        loadingList.value = true;
        store.commit("contentStore/setFormList", []);
        formRequest.forms = [
          {
            id: null,
            name: null,
          },
        ];

        const req = {
          idSector: val.id,
          idBP: state._rdg.idBP,
        };
        fetchFormList(req).finally(() => {
          loadingList.value = false;
        });
      }
    }
  );

  // Navigation functions
  const positiveClick = () => {
    if (step.value === 2) {
      validateForm().then((res) => {
        if (res) {
          isLoading.value = true;
          const req = {
            idBP: state._rdg.idBP,
            idEvent: state._rdg.idEvent,
            idSector: formRequest.sector.id,
            listForm: [...formRequest.forms].map((item: any) => {
              const name = isManualAIU.value(item.id) ? item.name : "manual";
              return {
                idBPDocTemplate: item.id,
                bpDocName: name,
              };
            }),
          };

          createAIUCustom(req).then((res) => {
            response.success(res, function () {
              let redirectTo: string;
              switch (state._rdgType.value) {
                case "RDGB":
                case "RDGTK":
                  redirectTo = "v2.rdg-collaboration";
                  break;
                case "RDGM":
                  redirectTo = "om.rdg-collaboration";
                  break;
                default:
                  redirectTo = "";
                  break;
              }

              router
                .push({
                  name: redirectTo,
                  params: {
                    typeRDG: state._rdgType.value,
                    idEvent: state._rdg.idEvent,
                    idDoc: res.responseData.idBPDocument,
                  },
                })
                .then(() => {
                  onClose();
                });
            });
          });
        }
      });
    } else {
      nextStep();
      resetValidation();
    }
  };

  const negativeClick = () => {
    if (step.value > 1) {
      previousStep();
    } else {
      onClose();
    }
  };

  const onClose = () => {
    closeDialog();
    resetForm();
    resetAPIData();
    isLoading.value = false;
  };

  // Get computed values from store
  const itemList = computed(() => {
    const items = store.state.contentStore.formList;
    return items;
  });

  return {
    // Form state
    state,
    formRequest,
    listMonths,

    // API state
    isLoading,
    loadingList,
    listEventType,
    listRDGType,
    listRDG,
    sectorList,
    itemList,

    // Dialog state
    dialog,
    currentTitle,
    step,
    buttonNext,
    datePicker,
    errorState,
    tabs,
    progress,
    isShowDialog,

    // Validation
    v$,
    isManualAIU,
    getErrorMessages,

    // Utility functions
    getYearPickerData,

    // Main functions
    showDialogEvent,
    onClose,
    positiveClick,
    negativeClick,
    addForm,
    deleteForm,
  };
}
