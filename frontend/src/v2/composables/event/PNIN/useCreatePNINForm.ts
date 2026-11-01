import { ref, reactive } from "vue";
import { TRequestCreatePN, TRequestCreateAIUPNIN } from "@v2/Type.d";
import { monthNames } from "@/v2/mock/Contants";
import { getYearPicker } from "@/v2/helpers/datetime";
import { useStore } from "vuex";

export function useCreatePNINForm() {
  // Initial state definitions
  const initialState: TRequestCreateAIUPNIN = {
    _eventType: null,
    _rdgType: null,
    _month: null,
    _year: null,
    _rdg: null,
  };

  const initialFormRequest: TRequestCreatePN = {
    sector: null,
    forms: [
      {
        title: null,
        sections: [
          {
            id: null,
          },
        ],
      },
    ],
  };

  // Reactive state
  const state = reactive({ ...initialState });
  const formRequest = reactive({ ...initialFormRequest });

  // Static data
  const listMonths = ref(monthNames);

  // Form management functions
  const resetForm = () => {
    Object.assign(state, initialState);
    Object.assign(formRequest, initialFormRequest);
  };

  const store = useStore();
  const addForm = () => {
    formRequest.forms.push({
      title: null,
      sections: store.state.contentStore.sectionList.map(
        (s: { Id: number; Value: string }) => ({ id: s.Id })
      ),
    });
  };

  const deleteForm = (idx: number) => {
    formRequest.forms.splice(idx, 1);
  };

  const addSection = (idxForm: number) => {
    const form = formRequest.forms[idxForm];
    if (form) {
      form.sections.push({
        id: null,
      });
    }
  };

  const deleteSection = (idxForm: number, idxSection: number) => {
    const form = formRequest.forms[idxForm];
    if (form) {
      form.sections.splice(idxSection, 1);
    }
  };

  // Utility functions
  const getYearPickerData = () => getYearPicker();

  return {
    // State
    state,
    formRequest,
    listMonths,

    // Methods
    resetForm,
    addForm,
    deleteForm,
    addSection,
    deleteSection,
    getYearPickerData,

    // Initial data
    initialState,
    initialFormRequest,
  };
}
