<template>
  <v-dialog
    v-model="isShow"
    max-width="800"
    class="edit_dialog--wrapper"
    persistent
  >
    <v-card class="border-radius-dwp">
      <v-card-title class="text-center mt-3">
        <h3 class="text-h6 font-weight-regular">Edit Notification</h3>
        <v-btn
          density="default"
          icon="mdi-close"
          variant="text"
          class="btn-close"
          @click="isShow = false"
        />

        <hr class="line mt-5 mb-4" />
      </v-card-title>

      <v-card-text>
        <div v-if="isLoading" class="pa-2">
          <div class="shimmer mb-4" style="height: 18px; width: 60px"></div>
          <div
            class="shimmer mb-6 border-radius-dwp"
            style="height: 40px; width: 100%"
          ></div>

          <div
            class="shimmer mb-4 mt-6"
            style="height: 18px; width: 80px"
          ></div>
          <div
            class="shimmer mb-8 border-radius-dwp"
            style="height: 40px; width: 100%"
          ></div>

          <div class="shimmer mb-4" style="height: 18px; width: 150px"></div>
          <div class="shimmer mb-4" style="height: 24px; width: 100%"></div>
          <div class="shimmer mb-4" style="height: 24px; width: 100%"></div>
          <div class="shimmer mb-8" style="height: 24px; width: 100%"></div>

          <div class="shimmer mb-4" style="height: 18px; width: 100px"></div>
          <div class="shimmer mb-4" style="height: 80px; width: 100%"></div>
          <div class="shimmer mb-4" style="height: 24px; width: 40%"></div>
        </div>

        <div v-show="!isLoading">
          <div>
            <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
              Fitur<span style="color: red">*</span>
            </p>
            <div class="info-chip-wrap ml-2 mr-2">
              {{ formData.fitur }}
            </div>
          </div>
          <div>
            <p class="ml-2 pb-1 mt-3 text-left text-darkBlue font-weight-bold">
              Trigger<span style="color: red">*</span>
            </p>
            <div class="info-chip-wrap ml-2 mr-2">
              {{ formData.trigger }}
            </div>
          </div>

          <div class="mt-4 ml-2 mr-2">
            <p class="pb-1 text-left text-darkBlue font-weight-bold">
              Receiver<span style="color: red">*</span>
            </p>

            <div
              v-for="(rec, index) in formData.receiver"
              :key="rec.receiverId || index"
              class="mb-3 mt-1"
            >
              <p
                class="text-left text-darkBlue mb-0 font-weight-medium"
                style="font-size: 13px"
              >
                {{ rec.receiverName }}
              </p>
              <div
                class="d-flex align-center custom-checkbox-group"
                style="width: 50%"
              >
                <v-checkbox
                  v-model="rec.isPush"
                  label="Push"
                  color="#065391"
                  hide-details
                  density="compact"
                  class="mr-4 custom-check"
                ></v-checkbox>
                <v-checkbox
                  v-model="rec.isLonceng"
                  label="In App"
                  color="#065391"
                  hide-details
                  density="compact"
                  class="mr-4 custom-check"
                ></v-checkbox>
                <v-checkbox
                  v-model="rec.isEmail"
                  label="Email"
                  color="#065391"
                  hide-details
                  density="compact"
                  class="custom-check"
                ></v-checkbox>
              </div>
            </div>
          </div>

          <p class="ml-2 pb-1 mt-5 text-left text-darkBlue font-weight-bold">
            Wording<span style="color: red">*</span>
          </p>

          <!-- Push Wording -->
          <div>
            <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
              Push<span style="color: red">*</span>
            </p>
            <div style="padding: 10px 10px">
              <v-card
                class="rounded-lg overflow-hidden mb-3"
                elevation="0"
                style="border: 1px solid #9e9e9e"
              >
                <div class="editor-wrapper">
                  <div
                    ref="pushEditorRef"
                    id="push-email-editor"
                    style="min-height: 120px; padding: 10px"
                  ></div>
                </div>
              </v-card>
              <div>
                <v-chip
                  v-for="(param, idx) in formData.pushParameter"
                  :key="'push-' + idx"
                  class="custom-param-chip"
                  color="#065391"
                  variant="outlined"
                  draggable
                  append-icon="mdi-plus"
                  @dragstart="
                    $event.dataTransfer?.setData('text/param-source', 'push');
                    $event.dataTransfer?.setData(
                      'text/html',
                      getParamChipHtml(param.description)
                    );
                    $event.dataTransfer?.setData(
                      'text/plain',
                      ` ${param.description} `
                    );
                  "
                  @click="insertParaToPushEditor(param.description)"
                >
                  {{ param.description }}
                </v-chip>
                <div
                  v-if="!formData.pushParameter?.length"
                  class="text-caption text-grey"
                >
                  No parameters available
                </div>
              </div>
            </div>
          </div>

          <!-- In App (Lonceng) Wording -->
          <div>
            <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
              In App<span style="color: red">*</span>
            </p>
            <div style="padding: 10px 10px">
              <v-card
                class="rounded-lg overflow-hidden mb-3"
                elevation="0"
                style="border: 1px solid #9e9e9e"
              >
                <div class="editor-wrapper">
                  <div
                    ref="loncengEditorRef"
                    id="lonceng-email-editor"
                    style="min-height: 120px; padding: 10px"
                  ></div>
                </div>
              </v-card>
              <div>
                <v-chip
                  v-for="(param, idx) in formData.loncengParameter"
                  :key="'lonceng-' + idx"
                  class="custom-param-chip"
                  color="#065391"
                  variant="outlined"
                  draggable
                  append-icon="mdi-plus"
                  @dragstart="
                    $event.dataTransfer?.setData(
                      'text/param-source',
                      'lonceng'
                    );
                    $event.dataTransfer?.setData(
                      'text/html',
                      getParamChipHtml(param.description)
                    );
                    $event.dataTransfer?.setData(
                      'text/plain',
                      ` ${param.description} `
                    );
                  "
                  @click="insertParaToLoncengEditor(param.description)"
                >
                  {{ param.description }}
                </v-chip>
                <div
                  v-if="!formData.loncengParameter?.length"
                  class="text-caption text-grey"
                >
                  No parameters available
                </div>
              </div>
            </div>
          </div>

          <!-- Email Wording -->
          <div class="mb-5">
            <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
              Subject Email<span style="color: red">*</span>
            </p>
            <div style="padding: 10px 10px">
              <v-card
                class="rounded-lg overflow-hidden mb-3"
                elevation="0"
                style="border: 1px solid #9e9e9e"
              >
                <div class="editor-wrapper">
                  <div
                    ref="subjectEditorRef"
                    id="subject-email-editor"
                    style="min-height: 60px; padding: 10px"
                  ></div>
                </div>
              </v-card>
              <div class="mb-5">
                <v-chip
                  v-for="(param, idx) in formData.subjectParameter"
                  :key="'subj-' + idx"
                  class="custom-param-chip"
                  color="#065391"
                  variant="outlined"
                  draggable
                  append-icon="mdi-plus"
                  @dragstart="
                    $event.dataTransfer?.setData(
                      'text/param-source',
                      'subject'
                    );
                    $event.dataTransfer?.setData(
                      'text/html',
                      getParamChipHtml(param.description)
                    );
                    $event.dataTransfer?.setData(
                      'text/plain',
                      ` ${param.description} `
                    );
                  "
                  @click="insertParaToSubjectEditor(param.description)"
                >
                  {{ param.description }}
                </v-chip>
                <div
                  v-if="!formData.subjectParameter?.length"
                  class="text-caption text-grey"
                >
                  No parameters available
                </div>
              </div>

              <p class="pb-2 text-left text-darkBlue font-weight-bold">
                Body Email<span style="color: red">*</span>
              </p>
              <v-card
                class="rounded-lg overflow-hidden mb-3"
                elevation="0"
                style="border: 1px solid #9e9e9e"
              >
                <div class="editor-wrapper">
                  <div
                    ref="bodyEditorRef"
                    id="body-email-editor"
                    style="z-index: 1000; min-height: 120px; padding: 10px"
                  ></div>
                </div>
              </v-card>
              <div class="mb-5">
                <v-chip
                  v-for="(param, idx) in formData.bodyParameter"
                  :key="'body-' + idx"
                  class="custom-param-chip"
                  color="#065391"
                  variant="outlined"
                  draggable
                  append-icon="mdi-plus"
                  @click="insertParaToEditor(param.description)"
                  @dragstart="
                    $event.dataTransfer?.setData('text/param-source', 'body');
                    $event.dataTransfer?.setData(
                      'text/html',
                      getParamChipHtml(param.description)
                    );
                    $event.dataTransfer?.setData(
                      'text/plain',
                      ` ${param.description} `
                    );
                  "
                >
                  {{ param.description }}
                </v-chip>
                <div
                  v-if="!formData.bodyParameter?.length"
                  class="text-caption text-grey"
                >
                  No parameters available
                </div>
              </div>

              <p class="pb-2 text-left text-darkBlue font-weight-bold">
                Footer Email<span style="color: red">*</span>
              </p>
              <v-card
                class="rounded-lg overflow-hidden mb-3"
                elevation="0"
                style="border: 1px solid #9e9e9e"
              >
                <div class="editor-wrapper">
                  <div
                    ref="footerEditorRef"
                    id="footer-email-editor"
                    style="min-height: 120px; padding: 10px"
                  ></div>
                </div>
              </v-card>
              <div class="mb-3">
                <v-chip
                  v-for="(param, idx) in formData.footerParameter"
                  :key="'foot-' + idx"
                  class="custom-param-chip"
                  color="#065391"
                  variant="outlined"
                  draggable
                  prepend-icon="mdi-plus"
                  @dragstart="
                    $event.dataTransfer?.setData('text/param-source', 'footer');
                    $event.dataTransfer?.setData(
                      'text/html',
                      getParamChipHtml(param.description)
                    );
                    $event.dataTransfer?.setData(
                      'text/plain',
                      ` ${param.description} `
                    );
                  "
                  @click="insertParaToFooterEditor(param.description)"
                >
                  {{ param.description }}
                </v-chip>
                <div
                  v-if="!formData.footerParameter?.length"
                  class="text-caption text-grey"
                >
                  No parameters available
                </div>
              </div>
            </div>

            <div>
              <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
                Status Notification<span style="color: red">*</span>
              </p>
              <v-radio-group v-model="formData.isActive" inline class="ml-2">
                <v-radio color="#065391" label="Active" :value="true"></v-radio>
                <v-radio
                  color="#065391"
                  label="In Active"
                  :value="false"
                ></v-radio>
              </v-radio-group>
            </div>
          </div>
        </div>
      </v-card-text>
      <div class="text-right mt-3 pb-5 pr-5">
        <v-btn
          class="btn-prev mr-3"
          @click="isShow = false"
          elevation="4"
          width="100"
          height="45"
          :loading="isLoading"
          >Cancel</v-btn
        >
        <v-btn
          class="btn-next"
          elevation="4"
          width="100"
          height="45"
          :loading="isLoading"
          @click="saveHandler"
          >Save</v-btn
        >
      </div>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import {
  ref,
  reactive,
  nextTick,
  onBeforeUnmount,
  getCurrentInstance,
} from "vue";
import { useStore } from "vuex";
import { convert } from "html-to-text";
import Editor from "@/v2/components/side-project/ckeditor/build/ckeditor";
import { getEditorFAQConfig } from "@/v2/helpers/utils";
import { v4 as uuidv4 } from "uuid";
import ToastLabel from "@/v2/label/LabelToast";

const { LabelToast } = ToastLabel;
const { root } = getCurrentInstance() as any;

const store = useStore();

const emit = defineEmits<{
  (e: "onClose", value?: boolean): void;
  (e: "onSave", value?: any): void;
}>();

const isShow = ref<boolean>(false);
const isLoading = ref<boolean>(false);
const bodyEditorRef = ref<HTMLElement>();
let bodyEditorInstance: any = null;
const footerEditorRef = ref<HTMLElement>();
let footerEditorInstance: any = null;
const subjectEditorRef = ref<HTMLElement>();
let subjectEditorInstance: any = null;
const loncengEditorRef = ref<HTMLElement>();
let loncengEditorInstance: any = null;
const pushEditorRef = ref<HTMLElement>();
let pushEditorInstance: any = null;

const formData = reactive({
  idNotificationType: 0,
  fitur: "",
  trigger: "",
  receiver: [] as any[],
  pushWording: "",
  pushParameter: [] as any[],
  loncengWording: "",
  loncengParameter: [] as any[],
  subjectWording: "",
  subjectParameter: [] as any[],
  bodyWording: "",
  bodyParameter: [] as any[],
  footerWording: "",
  footerParameter: [] as any[],
  isActive: true,
});

function show(id: number) {
  isShow.value = true;
  isLoading.value = true;
  formData.idNotificationType = id;
  document.body.classList.add("notification-editor-scoped");
  store
    .dispatch("adminStore/getNotificationDataEdit", {
      idNotificationType: id,
    })
    .then((res: any) => {
      const data = res?.responseData || res?.data?.responseData || res;
      if (data) {
        formData.fitur = data.fitur || "";
        formData.trigger = data.trigger || "";
        formData.receiver = data.receiver || [];
        formData.pushParameter = data.pushParameter || [];
        formData.pushWording = mapMarkToRichDescription(
          data.pushWording || "",
          formData.pushParameter
        );

        formData.loncengParameter = data.loncengParameter || [];
        formData.loncengWording = mapMarkToRichDescription(
          data.loncengWording || "",
          formData.loncengParameter
        );

        formData.subjectParameter = data.subjectParameter || [];
        formData.subjectWording = mapMarkToRichDescription(
          data.subjectWording || "",
          formData.subjectParameter
        );

        formData.bodyParameter = data.bodyParameter || [];
        formData.bodyWording = mapMarkToRichDescription(
          data.bodyWording || "",
          formData.bodyParameter
        );

        formData.footerParameter = data.footerParameter || [];
        formData.footerWording = mapMarkToRichDescription(
          data.footerWording || "",
          formData.footerParameter
        );
        formData.isActive = data.isActive !== false;
      }
    })
    .catch((err: any) => {
      console.error(err);
    })
    .finally(() => {
      isLoading.value = false;
      nextTick(() => {
        initBodyEditor();
        initFooterEditor();
        initSubjectEditor();
        initLoncengEditor();
        initPushEditor();
      });
    });
}

function hide() {
  isShow.value = false;
  document.body.classList.remove("notification-editor-scoped");
  destroyBodyEditor();
  destroyFooterEditor();
  destroySubjectEditor();
  destroyLoncengEditor();
  destroyPushEditor();
  emit("onClose");
}

async function initBodyEditor() {
  if (bodyEditorInstance) {
    await bodyEditorInstance.destroy();
    bodyEditorInstance = null;
  }
  if (!bodyEditorRef.value) return;

  try {
    const channelId = uuidv4();
    const config = (getEditorFAQConfig as any)(store, channelId);

    config.initialData = formData.bodyWording;
    // config.removePlugins = ["Table"];
    config.htmlSupport = {
      allow: [
        {
          name: /^(span|div|button|parameter-chip)$/,
          attributes: true,
          classes: true,
          styles: true,
        },
      ],
    };

    bodyEditorInstance = await Editor.CustomClassic.create(
      bodyEditorRef.value,
      config
    );

    // Ensure editor is not focused on initial load
    nextTick(() => {
      if (document.activeElement instanceof HTMLElement) {
        document.activeElement.blur();
      }
    });

    bodyEditorInstance.model.document.on("change:data", () => {
      formData.bodyWording = bodyEditorInstance.getData();
    });

    bodyEditorInstance.editing.view.document.on(
      "drop",
      (evt: any, data: any) => {
        const source = data.dataTransfer.getData("text/param-source");
        if (source && source !== "body") {
          evt.stop();
          root.refs.toast.show(
            LabelToast("Parameter cannot be used in different section").warning
          );
        }
        setTimeout(() => {
          if (document.activeElement instanceof HTMLElement) {
            document.activeElement.blur();
          }
        }, 50);
      }
    );

    bodyEditorInstance.editing.view.document.on("focus", () => {
      clearDropTargetUI();
    });
  } catch (error) {
    console.error("CKEditor initialization failed:", error);
    root.refs.toast.show(
      LabelToast("Failed to connect to the editor. Please try again.").oopss
    );
    hide();
  }
}

async function initFooterEditor() {
  if (footerEditorInstance) {
    await footerEditorInstance.destroy();
    footerEditorInstance = null;
  }
  if (!footerEditorRef.value) return;

  try {
    const channelId = uuidv4();
    const config = (getEditorFAQConfig as any)(store, channelId);

    config.initialData = formData.footerWording;
    config.htmlSupport = {
      allow: [
        {
          name: /^(span|div|button|parameter-chip)$/,
          attributes: true,
          classes: true,
          styles: true,
        },
      ],
    };

    footerEditorInstance = await Editor.CustomClassic.create(
      footerEditorRef.value,
      config
    );

    // Ensure editor is not focused on initial load
    nextTick(() => {
      if (document.activeElement instanceof HTMLElement) {
        document.activeElement.blur();
      }
    });

    footerEditorInstance.model.document.on("change:data", () => {
      formData.footerWording = footerEditorInstance.getData();
    });

    footerEditorInstance.editing.view.document.on(
      "drop",
      (evt: any, data: any) => {
        const source = data.dataTransfer.getData("text/param-source");
        if (source && source !== "footer") {
          evt.stop();
          root.refs.toast.show(
            LabelToast("Parameter cannot be used in different section").warning
          );
        }
        setTimeout(() => {
          if (document.activeElement instanceof HTMLElement) {
            document.activeElement.blur();
          }
        }, 50);
      }
    );

    footerEditorInstance.editing.view.document.on("focus", () => {
      clearDropTargetUI();
    });
  } catch (error) {
    console.error("CKEditor initialization failed:", error);
    root.refs.toast.show(
      LabelToast("Failed to connect to the editor. Please try again.").oopss
    );
    hide();
  }
}

async function initLoncengEditor() {
  if (loncengEditorInstance) {
    await loncengEditorInstance.destroy();
    loncengEditorInstance = null;
  }
  if (!loncengEditorRef.value) return;

  try {
    const channelId = uuidv4();
    const config = (getEditorFAQConfig as any)(store, channelId);

    config.initialData = formData.loncengWording;
    config.htmlSupport = {
      allow: [
        {
          name: /^(span|div|button|parameter-chip)$/,
          attributes: true,
          classes: true,
          styles: true,
        },
      ],
    };

    loncengEditorInstance = await Editor.CustomClassic.create(
      loncengEditorRef.value,
      config
    );

    // Ensure editor is not focused on initial load
    nextTick(() => {
      if (document.activeElement instanceof HTMLElement) {
        document.activeElement.blur();
      }
    });

    loncengEditorInstance.model.document.on("change:data", () => {
      formData.loncengWording = loncengEditorInstance.getData();
    });

    loncengEditorInstance.editing.view.document.on(
      "drop",
      (evt: any, data: any) => {
        const source = data.dataTransfer.getData("text/param-source");
        if (source && source !== "lonceng") {
          evt.stop();
          root.refs.toast.show(
            LabelToast("Parameter cannot be used in different section").warning
          );
        }
        setTimeout(() => {
          if (document.activeElement instanceof HTMLElement) {
            document.activeElement.blur();
          }
        }, 50);
      }
    );

    loncengEditorInstance.editing.view.document.on("focus", () => {
      clearDropTargetUI();
    });

    loncengEditorInstance.editing.view.document.on(
      "enter",
      (evt: any, data: any) => {
        data.preventDefault();
        evt.stop();
        root.refs.toast.show(
          LabelToast("Enter is not allowed, wording has to be one line").warning
        );
      },
      { priority: "high" }
    );
  } catch (error) {
    console.error("CKEditor initialization failed:", error);
    root.refs.toast.show(
      LabelToast("Failed to connect to the editor. Please try again.").oopss
    );
    hide();
  }
}

async function initPushEditor() {
  if (pushEditorInstance) {
    await pushEditorInstance.destroy();
    pushEditorInstance = null;
  }
  if (!pushEditorRef.value) return;

  try {
    const channelId = uuidv4();
    const config = (getEditorFAQConfig as any)(store, channelId);

    config.initialData = formData.pushWording;
    config.htmlSupport = {
      allow: [
        {
          name: /^(span|div|button|parameter-chip)$/,
          attributes: true,
          classes: true,
          styles: true,
        },
      ],
    };

    pushEditorInstance = await Editor.CustomClassic.create(
      pushEditorRef.value,
      config
    );

    // Ensure editor is not focused on initial load
    nextTick(() => {
      if (document.activeElement instanceof HTMLElement) {
        document.activeElement.blur();
      }
    });

    pushEditorInstance.model.document.on("change:data", () => {
      formData.pushWording = pushEditorInstance.getData();
    });

    pushEditorInstance.editing.view.document.on(
      "drop",
      (evt: any, data: any) => {
        const source = data.dataTransfer.getData("text/param-source");
        if (source && source !== "push") {
          evt.stop();
          root.refs.toast.show(
            LabelToast("Parameter cannot be used in different section").warning
          );
        }
        setTimeout(() => {
          if (document.activeElement instanceof HTMLElement) {
            document.activeElement.blur();
          }
        }, 50);
      }
    );

    pushEditorInstance.editing.view.document.on("focus", () => {
      clearDropTargetUI();
    });

    pushEditorInstance.editing.view.document.on(
      "enter",
      (evt: any, data: any) => {
        data.preventDefault();
        evt.stop();
        root.refs.toast.show(
          LabelToast("Enter is not allowed, wording has to be one line").warning
        );
      },
      { priority: "high" }
    );
  } catch (error) {
    console.error("CKEditor initialization failed:", error);
    root.refs.toast.show(
      LabelToast("Failed to connect to the editor. Please try again.").oopss
    );
    hide();
  }
}

function destroyBodyEditor() {
  if (bodyEditorInstance) {
    bodyEditorInstance.destroy().then(() => {
      bodyEditorInstance = null;
    });
  }
}

function destroyFooterEditor() {
  if (footerEditorInstance) {
    footerEditorInstance.destroy().then(() => {
      footerEditorInstance = null;
    });
  }
}

async function initSubjectEditor() {
  if (subjectEditorInstance) {
    await subjectEditorInstance.destroy();
    subjectEditorInstance = null;
  }
  if (!subjectEditorRef.value) return;

  try {
    const channelId = uuidv4();
    const config = (getEditorFAQConfig as any)(store, channelId);

    config.initialData = formData.subjectWording;
    config.htmlSupport = {
      allow: [
        {
          name: /^(span|div|button|parameter-chip)$/,
          attributes: true,
          classes: true,
          styles: true,
        },
      ],
    };

    subjectEditorInstance = await Editor.CustomClassic.create(
      subjectEditorRef.value,
      config
    );

    // Ensure editor is not focused on initial load
    nextTick(() => {
      if (document.activeElement instanceof HTMLElement) {
        document.activeElement.blur();
      }
    });

    subjectEditorInstance.model.document.on("change:data", () => {
      formData.subjectWording = subjectEditorInstance.getData();
    });

    subjectEditorInstance.editing.view.document.on(
      "drop",
      (evt: any, data: any) => {
        const source = data.dataTransfer.getData("text/param-source");
        if (source && source !== "subject") {
          evt.stop();
          root.refs.toast.show(
            LabelToast("Parameter cannot be used in different section").warning
          );
        }
        setTimeout(() => {
          if (document.activeElement instanceof HTMLElement) {
            document.activeElement.blur();
          }
        }, 50);
      }
    );

    subjectEditorInstance.editing.view.document.on("focus", () => {
      clearDropTargetUI();
    });
  } catch (error) {
    console.error("CKEditor initialization failed:", error);
    root.refs.toast.show(
      LabelToast("Failed to connect to the editor. Please try again.").oopss
    );
    hide();
  }
}

function destroySubjectEditor() {
  if (subjectEditorInstance) {
    subjectEditorInstance.destroy().then(() => {
      subjectEditorInstance = null;
    });
  }
}

function destroyLoncengEditor() {
  if (loncengEditorInstance) {
    loncengEditorInstance.destroy().then(() => {
      loncengEditorInstance = null;
    });
  }
}

function destroyPushEditor() {
  if (pushEditorInstance) {
    pushEditorInstance.destroy().then(() => {
      pushEditorInstance = null;
    });
  }
}

onBeforeUnmount(() => {
  document.body.classList.remove("notification-editor-scoped");
  destroyBodyEditor();
  destroyFooterEditor();
  destroySubjectEditor();
  destroyLoncengEditor();
  destroyPushEditor();
});

function insertParaToPushEditor(description: string) {
  if (pushEditorInstance) {
    const htmlSnippet = getParamChipHtml(description);
    const viewFragment = pushEditorInstance.data.processor.toView(htmlSnippet);
    const modelFragment = pushEditorInstance.data.toModel(viewFragment);
    pushEditorInstance.model.insertContent(modelFragment);

    // blur the editor if needed
    setTimeout(() => {
      if (document.activeElement instanceof HTMLElement) {
        document.activeElement.blur();
      }
    }, 50);
  }
}

function insertParaToLoncengEditor(description: string) {
  if (loncengEditorInstance) {
    const htmlSnippet = getParamChipHtml(description);
    const viewFragment =
      loncengEditorInstance.data.processor.toView(htmlSnippet);
    const modelFragment = loncengEditorInstance.data.toModel(viewFragment);
    loncengEditorInstance.model.insertContent(modelFragment);

    // blur the editor if needed
    setTimeout(() => {
      if (document.activeElement instanceof HTMLElement) {
        document.activeElement.blur();
      }
    }, 50);
  }
}

function insertParaToEditor(description: string) {
  if (bodyEditorInstance) {
    const htmlSnippet = getParamChipHtml(description);
    const viewFragment = bodyEditorInstance.data.processor.toView(htmlSnippet);
    const modelFragment = bodyEditorInstance.data.toModel(viewFragment);
    bodyEditorInstance.model.insertContent(modelFragment);

    // blur the editor if needed
    setTimeout(() => {
      if (document.activeElement instanceof HTMLElement) {
        document.activeElement.blur();
      }
    }, 50);
  }
}

function insertParaToSubjectEditor(description: string) {
  if (subjectEditorInstance) {
    const htmlSnippet = getParamChipHtml(description);
    const viewFragment =
      subjectEditorInstance.data.processor.toView(htmlSnippet);
    const modelFragment = subjectEditorInstance.data.toModel(viewFragment);
    subjectEditorInstance.model.insertContent(modelFragment);

    // blur the editor if needed
    setTimeout(() => {
      if (document.activeElement instanceof HTMLElement) {
        document.activeElement.blur();
      }
    }, 50);
  }
}

function insertParaToFooterEditor(description: string) {
  if (footerEditorInstance) {
    const htmlSnippet = getParamChipHtml(description);
    const viewFragment =
      footerEditorInstance.data.processor.toView(htmlSnippet);
    const modelFragment = footerEditorInstance.data.toModel(viewFragment);
    footerEditorInstance.model.insertContent(modelFragment);

    // blur the editor if needed
    setTimeout(() => {
      if (document.activeElement instanceof HTMLElement) {
        document.activeElement.blur();
      }
    }, 50);
  }
}

async function saveHandler() {
  isLoading.value = true;
  try {
    const payload = {
      idNotificationType: formData.idNotificationType,
      receiver: formData.receiver.map((r: any) => ({
        receiverId: r.receiverId,
        receiverName: r.receiverName,
        isPush: !!r.isPush,
        isLonceng: !!r.isLonceng,
        isEmail: !!r.isEmail,
      })),
      pushWording: stripHtml(
        mapRichDescriptionToMark(formData.pushWording, formData.pushParameter)
      ),
      loncengWording: stripHtml(
        mapRichDescriptionToMark(
          formData.loncengWording,
          formData.loncengParameter
        )
      ),
      subjectWording: stripHtml(
        mapRichDescriptionToMark(
          formData.subjectWording,
          formData.subjectParameter
        )
      ),
      bodyWording: mapRichDescriptionToMark(
        formData.bodyWording,
        formData.bodyParameter
      ),
      footerWording: mapRichDescriptionToMark(
        formData.footerWording,
        formData.footerParameter
      ),
      isActive: formData.isActive,
    };

    const res: any = await store.dispatch(
      "adminStore/updateNotification",
      payload
    );

    if (res.responseCode === "011000") {
      root.refs.toast.show(
        LabelToast(res.responseMessage || "Notification updated successfully")
          .success
      );
      emit("onSave", payload);
      hide();
    } else {
      root.refs.toast.show(
        LabelToast(res.responseMessage || "Failed to update notification").oopss
      );
    }
  } catch (err: any) {
    console.error("Error updating notification:", err);
    const errMessage =
      err.response?.data?.responseMessage ||
      "An error occurred while updating the notification";
    root.refs.toast.show(LabelToast(errMessage).oopss);
  } finally {
    isLoading.value = false;
  }
}

// No remaining legacy backdrops needed

function getParamChipHtml(description: string) {
  return `<button contenteditable='false' class='custom-param-chip' style='display: inline-block; background-color: #e9f5ff; border: 1px solid #6eb3ea; border-radius: 4px; padding: 2px 10px; color: #065391; font-weight: 500; font-family: sans-serif; font-size: 13px; vertical-align: middle; margin: 0 2px; outline: none; cursor: default;'>${description}</button>`;
}

function mapMarkToDescription(text: string, params: any[]) {
  if (!text || !params || !params.length) return text;
  let result = text;
  params.forEach((p) => {
    if (p.mark && p.description) {
      const escapedMark = p.mark.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      result = result.replace(new RegExp(escapedMark, "g"), p.description);
    }
  });
  return result;
}

function mapDescriptionToMark(text: string, params: any[]) {
  if (!text || !params || !params.length) return text;
  let result = text;
  params.forEach((p) => {
    if (p.mark && p.description) {
      const escapedDesc = p.description.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      result = result.replace(new RegExp(escapedDesc, "g"), p.mark);
    }
  });
  return result;
}

function mapMarkToRichDescription(text: string, params: any[]) {
  if (!text || !params || !params.length) return text;
  let result = text;
  params.forEach((p) => {
    if (p.mark && p.description) {
      const escapedMark = p.mark.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      const htmlSnippet = getParamChipHtml(p.description);
      result = result.replace(new RegExp(escapedMark, "g"), htmlSnippet);
    }
  });
  return result;
}

function mapRichDescriptionToMark(text: string, params: any[]) {
  if (!text || !params || !params.length) return text;
  let result = text;
  params.forEach((p) => {
    if (p.mark && p.description) {
      const escapedDesc = p.description.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      // Match button, span, div, or parameter-chip tags regardless of style order
      const chipRegex = new RegExp(
        `<(button|span|div|parameter-chip)[^>]*>${escapedDesc}</(button|span|div|parameter-chip)>(&nbsp;)?`,
        "g"
      );
      result = result.replace(chipRegex, p.mark);
    }
  });
  return result;
}

function stripHtml(html: string) {
  if (!html) return "";
  return convert(html, {
    wordwrap: false,
    preserveNewlines: false,
  }).trim();
}

function clearDropTargetUI() {
  const targets = document.querySelectorAll(
    ".ck-clipboard-drop-target-line, .ck-clipboard-drop-target-position"
  );
  targets.forEach((el) => {
    (el as HTMLElement).style.display = "none";
  });
}

defineExpose({
  show,
  hide,
});
</script>

<style lang="scss" scoped>
.edit_dialog--wrapper {
  .btn-close {
    position: absolute;
    right: 0;
    top: 0;
    margin-top: 10px;
    margin-right: 10px;
  }

  .line {
    border: none;
    height: 2px;
    background: linear-gradient(
      270deg,
      rgba(255, 255, 252, 0.8) 0%,
      #a6abc7 51.56%,
      rgba(255, 255, 252, 0.8) 100%
    );
  }

  :deep(.v-chip.v-chip--density-default.chip-shadow) {
    box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
      0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
      0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12));
    height: 56px;
    width: 98%;
    color: grey !important;
    border: none;
    background: #dfdfdf !important;
    font-size: 16px;
    margin: 10px;
  }

  .info-chip-wrap {
    box-shadow: 0px 3px 1px -2px rgba(0, 0, 0, 0.2),
      0px 2px 2px 0px rgba(0, 0, 0, 0.14), 0px 1px 5px 0px rgba(0, 0, 0, 0.12);
    min-height: 56px;
    width: 98%;
    color: grey;
    border: none;
    background: #dfdfdf;
    font-size: 16px;
    margin: 10px;
    border-radius: 20px;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    white-space: normal;
    word-break: break-word;
    line-height: 1.5;
  }

  .btn-next {
    background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
    border-radius: 10px !important;
    border-color: #267dc2 !important;
    padding-left: 16px !important;
    padding-right: 16px !important;
    font-size: 14px !important;
    color: white;
    font-weight: 900;
  }

  .btn-prev {
    background: white;
    border-radius: 10px !important;
    padding-left: 16px !important;
    padding-right: 16px !important;
    font-size: 14px !important;
    color: #267dc2;
    font-weight: 900;
  }

  .custom-param-chip {
    // display: inline-flex !important;
    // align-items: center !important;
    // justify-content: center !important;
    // height: 28px !important;
    outline: none;
    border: none;
    margin-right: 8px;
    margin-bottom: 8px;
    border-radius: 4px !important;
    padding: 4px 10px !important;
    font-weight: 500 !important;
    letter-spacing: normal !important;
    transition: all 0.2s ease;
    cursor: grab;
    background-color: #e9f5ff !important;
    border: 1px solid #6eb3ea !important;
    font-size: 12px !important;
    color: #065391 !important;

    &:hover {
      background-color: #d8ecff !important;
      border-color: #065391 !important;
      color: #003a6d !important;
      transform: translateY(-1px);
      box-shadow: 0 4px 6px rgba(6, 83, 145, 0.1);
    }

    &:active {
      cursor: grabbing;
      transform: translateY(0);
      box-shadow: 0 1px 3px rgba(6, 83, 145, 0.2);
    }

    :deep(.v-chip__content) {
      display: flex !important;
      align-items: center !important;
      // line-height: 1 !important;
      padding-bottom: -1px !important; /* Visual nudge for vertical centering */
    }

    :deep(.v-chip__append) {
      display: flex !important;
      align-items: center !important;
      // margin-left: 1px !important;
      // margin-right: -2px !important;
    }

    :deep(.v-icon) {
      font-size: 16px !important;
      height: 16px !important;
      width: 16px !important;
    }
  }

  .custom-checkbox-group :deep(.v-selection-control) {
    min-height: 24px !important;
  }
  .custom-checkbox-group :deep(.v-label) {
    font-size: 13px !important;
    font-weight: 400 !important;
    color: #444;
    opacity: 1 !important;
    margin-left: 2px;
  }
  .custom-checkbox-group :deep(.v-selection-control__wrapper) {
    margin-right: -4px;
  }

  .editor-wrapper :deep(.ck-editor__editable),
  .editor-wrapper :deep(.ck-editor),
  .editor-wrapper :deep(.ck-editor__main) {
    min-height: 40px;
    border: none !important;
    box-shadow: none !important;
  }

  /* Specific height for Body, Footer, Push, and In App Email */
  .editor-wrapper:has(#body-email-editor) :deep(.ck-editor__editable),
  .editor-wrapper:has(#footer-email-editor) :deep(.ck-editor__editable),
  .editor-wrapper:has(#push-email-editor) :deep(.ck-editor__editable),
  .editor-wrapper:has(#lonceng-email-editor) :deep(.ck-editor__editable) {
    min-height: 120px;
    padding-bottom: 10px;
  }

  .editor-wrapper:has(#subject-email-editor) :deep(.ck-editor__editable) {
    min-height: 40px;
    padding-bottom: 10px;
  }

  .editor-wrapper :deep(.ck-toolbar),
  .editor-wrapper :deep(.ck-editor__top) {
    display: none !important;
    border: none !important;
  }

  :deep(.ck-content figure.table:not(.layout-table) > table) {
    border: none;
  }

  :deep(.ck .ck-toolbar__items) {
    display: none !important;
  }

  :deep(.ck.ck-editor__top .ck-sticky-panel .ck-sticky-panel__content) {
    border: none !important;
  }

  :deep(.ck .ck-evaluation-badge__label),
  :deep(.ck-widget__label),
  :deep(.ck-html-object-label),
  :deep(.ck-html-object-embed__label),
  :deep(.ck-widget__type-around),
  :deep(.ck-balloon-panel),
  :deep(.ck-widget__selection-handle),
  :deep(
      .ck-widget.ck-widget_with-selection-handle:hover
        > .ck-widget__selection-handle
    ),
  :deep(
      .ck-widget.ck-widget_with-selection-handle.ck-widget_selected
        > .ck-widget__selection-handle
    ),
  :deep([data-html-object-embed-label])::before {
    display: none !important;
    content: "" !important;
    opacity: 0 !important;
    visibility: hidden !important;
  }

  :deep(.ck-widget.html-object-embed) {
    padding: 0 !important;
    background-color: transparent !important;
  }

  :deep(.ck .ck-widget.ck-widget_selected),
  :deep(.ck .ck-widget:hover),
  :deep(.ck .ck-widget.table),
  :deep(.ck .ck-widget.table:hover) {
    border-radius: 4px !important;
    outline: none !important;
    border: none !important;
    box-shadow: none !important;
    background-color: transparent !important;
  }

  :deep(.ck-widget.html-object-embed),
  :deep(.ck-widget.html-object-embed:hover),
  :deep(.ck-widget.html-object-embed.ck-widget_selected) {
    padding: 0 !important;
    outline: none !important;
    border: none !important;
    background-color: transparent !important;
    transition: all 0.2s ease;
  }

  :deep(.ck-widget.html-object-embed.ck-widget_selected .custom-param-chip) {
    background-color: #065391 !important;
    color: #fff !important;
  }

  :deep(.ck-widget.html-object-embed:hover) {
    transform: translateY(-1px);
    cursor: grab;
  }

  :deep(.ck.ck-toolbar),
  :deep(.ck.ck-editor__top) {
    display: none !important;
    border: none !important;
  }
  :deep(.ck-editor__editable.ck-editor__nested-editable) {
    min-height: 200px;
    border: none !important;
    box-shadow: none !important;
  }

  // :deep(.v-chip__append .mdi-plus) {
  //   // display: none !important;
  //   vertical-align: baseline !important;
  // }

  // :deep(.v-chip__content) {
  //   margin-bottom: 4px !important;
  // }
}

/* Scoped CKEditor Overrides (State-based) */
</style>

<style>
.notification-editor-scoped .ck-balloon-panel,
.notification-editor-scoped .ck-body-wrapper .ck-balloon-panel,
.notification-editor-scoped .ck.ck-balloon-panel_visible,
.notification-editor-scoped .ck-widget__selection-handle,
.notification-editor-scoped
  .ck-widget_with-selection-handle:hover
  > .ck-widget__selection-handle,
.notification-editor-scoped
  .ck-widget_with-selection-handle.ck-widget_selected
  > .ck-widget__selection-handle,
.notification-editor-scoped .ck-widget__type-around,
.notification-editor-scoped
  .ck.ck-editor__editable_focused
  .ck-clipboard-drop-target-line {
  display: none !important;
  visibility: hidden !important;
  opacity: 0 !important;
  pointer-events: none !important;
}

/* Shimmer Loading Styles */
.shimmer {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 4px;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
