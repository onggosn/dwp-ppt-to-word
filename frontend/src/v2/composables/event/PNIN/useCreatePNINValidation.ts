import { computed } from "vue";
import useVuelidate from "@vuelidate/core";
import { required, helpers } from "@vuelidate/validators";
import { notHasTagHtml } from "@/v2/helpers/validation";

export function useCreatePNINValidation(formRequest: any, isRDGB: any) {
  // Validation rules
  const rules = computed(() => {
    const localRule = {
      sector: {},
      forms: {
        $each: helpers.forEach({
          title: {
            required,
            unique: (value: any, obj: any, idx: any, parent: any) => {
              const validate =
                parent.forms.filter(
                  (form: any) =>
                    form.title?.toLowerCase() === value?.toLowerCase()
                ).length <= 1 || value === null;
              return validate;
            },
            notHasTagHtml,
          },
          sections: {
            $each: helpers.forEach({
              id: {
                required,
                unique: (value: any, obj: any, idx: any, parent: any) => {
                  const validate =
                    parent.sections.filter((sec: any) => sec.id === value)
                      .length <= 1 || value === null;
                  return validate;
                },
              },
            }),
          },
        }),
      },
    };
    if (isRDGB.value) localRule.sector = { required };
    return localRule;
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

  // Helper functions for error handling
  const checkNestedError = (item: any[], customMessage = {}) => {
    const messages = {
      required: "Wajib diisi",
      unique: "Section tidak boleh ada yang sama",
      notHasTagHtml: "tidak boleh mengandung simbol html",
      ...customMessage,
    };
    return item.map((d) => {
      return messages[d.$validator] ?? d.$message;
    });
  };

  const hasNestedError = (item: any[]): boolean => {
    return v$.value.$dirty && item.length !== 0;
  };

  return {
    // Validation instance
    v$,

    // Methods
    validateForm,
    resetValidation,
    checkNestedError,
    hasNestedError,
  };
}
