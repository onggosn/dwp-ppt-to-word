import { computed } from "vue";
import { useStore } from "vuex";
import useVuelidate from "@vuelidate/core";
import { required, helpers } from "@vuelidate/validators";
import { getErrorMessages } from "@v2/helpers/validation";

export function useCreateAIUValidation(formRequest: any) {
  const store = useStore();

  // Check if form is manual AIU
  const isManualAIU = computed(() => {
    const list = store.state.contentStore.formList;
    return (id: any): boolean => {
      const item = list.find((e: any) => e.id === id);
      return item && item.templateType === "free-text";
    };
  });

  // Validation rules
  const rules = computed(() => {
    return {
      sector: { required },
      forms: {
        $each: helpers.forEach({
          id: {
            required,
            unique: (value: any) => {
              const isManual = isManualAIU.value(value);
              const validate =
                formRequest.forms.filter((item: any) => item.id === value)
                  .length <= 1 || value === null;
              return isManual || validate;
            },
          },
          name: {
            required: (value: any, meta: any) => {
              const isManual = isManualAIU.value(meta.id);
              if (isManual) return value !== null;
              return true;
            },
            unique: (value: any) => {
              const validate =
                formRequest.forms.filter((item: any) => item.name === value)
                  .length <= 1 || value === null;
              return validate;
            },
          },
        }),
      },
    };
  });

  // Initialize vuelidate
  const v$ = useVuelidate(rules, formRequest);

  // Validation function
  const validateForm = async (): Promise<boolean> => {
    return await v$.value.$validate();
  };

  // Reset validation
  const resetValidation = () => {
    v$.value.$reset();
  };

  return {
    // Validation instance
    v$,

    // Computed
    isManualAIU,

    // Methods
    validateForm,
    resetValidation,
    getErrorMessages,
  };
}
