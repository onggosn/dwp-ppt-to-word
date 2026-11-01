import { watch, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { responsePromise } from "@/v2/helpers/utils";
import { getCurrentInstance } from "vue";
import { useCreatePNINForm } from "./useCreatePNINForm";
import { useCreatePNINAPI } from "./useCreatePNINAPI";
import { useCreatePNINValidation } from "./useCreatePNINValidation";
import { useCreatePNINDialog } from "./useCreatePNINDialog";

export function useCreatePNIN() {
  const store = useStore();
  const router = useRouter();
  const { root } = getCurrentInstance() as any;
  const response = responsePromise(root);

  // Initialize composables
  const formComposable = useCreatePNINForm();
  const apiComposable = useCreatePNINAPI();
  const dialogComposable = useCreatePNINDialog();

  const {
    state,
    formRequest,
    listMonths,
    resetForm,
    addForm,
    deleteForm,
    addSection,
    deleteSection,
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
    fetchSectorPNINList,
    fetchSectionList,
    createPNINCustom,
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
    listSection,
    limitSection,
    showDialogEvent: showDialog,
    closeDialog,
    nextStep,
    previousStep,
    validateButtonState,
  } = dialogComposable;

  // Check if RDGB
  const isRDGB = computed((): boolean => {
    return (state._rdgType?.value as string) === "RDGB";
  });

  const validationComposable = useCreatePNINValidation(formRequest, isRDGB);
  const {
    v$,
    validateForm,
    resetValidation,
    checkNestedError,
    hasNestedError,
  } = validationComposable;

  // Initialize dialog with API calls
  const showDialogEvent = (titleParam?: string) => {
    showDialog(titleParam);
    v$.value.$reset();
    fetchEventTypes().then((data) => {
      listEventType.value = data;
    });

    const req = {
      sectorName: currentTitle.value,
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
          title: null,
          sections: [
            {
              id: null,
            },
          ],
        },
      ];
      sectorList.value = [];
      if (val) {
        fetchSectorPNINList(state._rdg.idBP).then((res) => {
          sectorList.value = res;
        });
      }
    }
  );

  // Watch for form validation in step 2
  watch(
    [formRequest],
    () => {
      validateButtonState(state, formRequest, step.value);
    },
    { deep: true }
  );

  // Watch for step changes
  watch(step, (val) => {
    validateButtonState(state, formRequest, val);
  });

  // Watch for sector changes
  watch(
    () => formRequest.sector,
    async (val) => {
      store.commit("contentStore/setSectionList", []);
      formRequest.forms = [
        {
          title: null,
          sections: [],
        },
      ];
      if (val) {
        const req = {
          idSector: val.id,
          idBP: state._rdg.idBP,
        };
        await fetchSectionList(req);
        store.state.contentStore.sectionList.map(
          (s: { Id: number; Value: string }) =>
            formRequest.forms[0].sections.push({
              id: s.Id,
            })
        );
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
            idSector: formRequest.sector.id,
            listOutput: formRequest.forms.map((item, idx) => {
              return {
                orderDoc: idx,
                title: item.title,
                idBPSection: item.sections.map((sec) => sec.id),
              };
            }),
          };

          createPNINCustom(req).then((res) => {
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

              // Redirect first, then close modal
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
                  // Close modal after successful navigation
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
    resetValidation();
  };

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
    listSection,
    limitSection,

    // Computed
    isRDGB,

    // Validation
    v$,
    checkNestedError,
    hasNestedError,

    // Utility functions
    getYearPickerData,

    // Main functions
    showDialogEvent,
    onClose,
    positiveClick,
    negativeClick,
    addForm,
    deleteForm,
    addSection,
    deleteSection,
  };
}
