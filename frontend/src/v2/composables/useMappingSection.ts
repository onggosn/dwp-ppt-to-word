import { ref, computed, reactive, getCurrentInstance } from "vue";
import { useStore } from "vuex";

import { InputMapping } from "@/v2/Type";
import GlobalEnum from "@/v2/enum/Enum";

const useMappingSection = (document: any) => {
  const { root: rootInstance } = getCurrentInstance() as any;
  const store = useStore();

  const { MappingStatus } = GlobalEnum;

  const dialog = ref<boolean>(false);
  const dataTemp = ref<any>(null);
  const onLoadingAdd = ref<boolean>(false);
  const showToast = ref<boolean>(false);

  const validationErrors = ref<Record<number, string>>({});

  const idMeForm = ref<string>("");

  const inputMappingDetail = ref({
    contentTitle: "-",
    sectionTitle: "-",
    subSectionTitle: "-",
  });

  const inputStateMutated = ref<InputMapping>({
    sections: [],
  });

  const inputStateCloned = ref<InputMapping>({
    sections: [],
  });

  const visibleSections = computed(() =>
    inputStateMutated.value.sections.filter(
      (section) => section.status !== MappingStatus.deleted
    )
  );

  const isSectionsNotAdded = computed(() => {
    return inputStateMutated.value.sections.length === 0;
  });

  const handleAddInput = () => {
    const { sections: clonedSections } = inputStateMutated.value;

    const payload = {
      id: null,
      sectionName: "",
      status: MappingStatus.new,
    };

    clonedSections.push(reactive({ ...payload }));
  };

  const getDetailMappingPpt = async (item, section) => {
    idMeForm.value = item.idMEFormTemplate;

    const payload = {
      idMeFormTemplate: idMeForm.value,
    };
    inputMappingDetail.value.contentTitle = document.bPDocumentName;
    inputMappingDetail.value.sectionTitle = section
      ? section.bPEFormLabel
      : item.bPEFormLabel;
    inputMappingDetail.value.subSectionTitle = section
      ? item.bPEFormLabel
      : "-";

    const [listSectionNameRes] = await Promise.all([
      store.dispatch("adminStore/getListSectionNamePpt", payload),
    ]);

    if (
      listSectionNameRes.responseData &&
      listSectionNameRes.responseData.length > 0
    ) {
      const { responseData } = listSectionNameRes;

      const statusAdded = responseData.map((item) => ({
        ...item,
        status: MappingStatus.existing,
      }));

      inputStateMutated.value.sections = statusAdded;
      inputStateCloned.value.sections = JSON.parse(JSON.stringify(statusAdded));
    }

    validationErrors.value = {};
  };

  const handleOpenModal = (item, section) => {
    dialog.value = true;
    dataTemp.value = item;
    getDetailMappingPpt(item, section);
  };

  const handleCloseModal = () => {
    dialog.value = false;
    emptySectionInstance();
  };

  const handleDeleteInput = (sectionId: number, idx: number) => {
    const visibleSections_array = visibleSections.value;
    const allSections = inputStateMutated.value.sections;

    // Untuk section baru (id = null), hapus langsung dari array berdasarkan index di visibleSections
    if (sectionId === 0 || sectionId === null) {
      const targetSection = visibleSections_array[idx];
      if (targetSection) {
        // Cari index section ini di array utama (inputStateMutated.value.sections)
        const mainArrayIndex = allSections.findIndex(
          (section) => section === targetSection
        );
        if (mainArrayIndex !== -1) {
          allSections.splice(mainArrayIndex, 1);
        }
      }
      return;
    }

    // Untuk section existing, ubah status menjadi deleted
    const targetedSection = allSections.find(
      (section) => section.id === sectionId
    );

    if (targetedSection && targetedSection.id) {
      targetedSection.status = MappingStatus.deleted;
    }
  };

  const handleInput = (currIndex) => {
    const findSection = visibleSections.value.find(
      (_, index) => index === currIndex
    );

    const clonedSection = inputStateCloned.value.sections.find(
      (section) => section.id === findSection?.id
    );

    const status = ["new"];

    if (
      findSection &&
      findSection.id &&
      !status.includes(findSection.status || "")
    ) {
      findSection.status = MappingStatus.update;
    }

    if (
      clonedSection &&
      clonedSection?.sectionName === findSection?.sectionName &&
      clonedSection.id === findSection?.id
    ) {
      findSection.status = MappingStatus.existing;
    }
  };

  const handleAddNewSection = (idMbpDocumentTemplate) => {
    const { sections: data } = inputStateMutated.value;
    const { value: idMeFormTemplate } = idMeForm;

    const payload = {
      data,
      idMeFormTemplate,
      idMbpDocumentTemplate,
      IdMSector: dataTemp.value.idSector,
    };

    const isValid = validateSections();

    if (!isValid) return;

    onLoadingAdd.value = true;

    store
      .dispatch("adminStore/addMappingSectionPpt", payload)
      .then(() => {
        showToast.value = !showToast.value;
        handleCloseModal();
      })
      .catch((err) => {
        const { responseData } = err.response.data;
        applyApiErrors(responseData);
      })
      .finally(() => {
        onLoadingAdd.value = false;
      });
  };

  const emptySectionInstance = () => {
    inputStateMutated.value.sections = [];
    validationErrors.value = {};
  };

  const validateSections = () => {
    const errors: Record<number, string> = {};
    const nameCounts: Record<string, number[]> = {};

    visibleSections.value.forEach((section, index) => {
      const trimmedName = section.sectionName.trim().toLowerCase() || "";
      if (!trimmedName) {
        errors[index] = "Section Name is required";

        return;
      }

      if (!nameCounts[trimmedName]) {
        nameCounts[trimmedName] = [];
      }

      nameCounts[trimmedName].push(index);
    });

    Object.entries(nameCounts).forEach(([, indexes]) => {
      if (indexes.length > 1) {
        indexes.forEach((i) => {
          errors[i] =
            "This section is already in use. Please select another one";
        });
      }
    });

    validationErrors.value = errors;

    return Object.keys(errors).length === 0;
  };

  const applyApiErrors = (errorSectionNames: string[]) => {
    const errors = { ...validationErrors.value };

    if (errorSectionNames) {
      errorSectionNames.forEach((errorName) => {
        visibleSections.value.forEach((section: any, index: number) => {
          const { sectionName } = section;

          if (sectionName.trim() === errorName.trim()) {
            errors[index] =
              "This section is already in use. Please select another one";
          }
        });
      });
      validationErrors.value = errors;
    }
  };

  return {
    dialog,
    idMeForm,
    inputMappingDetail,
    inputStateMutated,
    visibleSections,
    onLoadingAdd,
    validationErrors,
    isSectionsNotAdded,
    rootInstance,
    showToast,
    handleAddInput,
    getDetailMappingPpt,
    handleOpenModal,
    handleCloseModal,
    handleDeleteInput,
    handleInput,
    handleAddNewSection,
    validateSections,
  };
};

export default useMappingSection;
