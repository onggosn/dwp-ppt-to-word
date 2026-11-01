import { ref, reactive } from "vue";
import { TRequestCreateAIU, TRequestCreateAIUPNIN } from "@v2/Type.d";
import { monthNames } from "@/v2/mock/Contants";
import { getYearPicker } from "@/v2/helpers/datetime";

export function useCreateAIUForm() {
  // Initial state definitions
  const initialState: TRequestCreateAIUPNIN = {
    _eventType: null,
    _rdgType: null,
    _month: null,
    _year: null,
    _rdg: null,
  };

  const initialFormRequest: TRequestCreateAIU = {
    sector: null,
    forms: [
      {
        id: null,
        name: null,
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

  const addForm = () => {
    formRequest.forms.push({
      id: null,
      name: null,
    });
  };

  const deleteForm = (idx: number) => {
    formRequest.forms.splice(idx, 1);
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
    getYearPickerData,

    // Initial data
    initialState,
    initialFormRequest,
  };
}
