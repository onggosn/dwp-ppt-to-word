<template>
  <Teleport to="body">
    <v-dialog
      v-model="dialog"
      width="800"
      persistent
      :class="[isShowDialog ? 'show' : 'hide']"
    >
      <v-card class="border-radius-dwp">
        <v-card-title class="text-center mt-3">
          <h3 class="text-h6 font-weight-regular">Create {{ currentTitle }}</h3>
          <v-btn
            density="default"
            icon="mdi-close"
            variant="text"
            class="btn-close"
            @click="onClose()"
          />
        </v-card-title>
        <hr class="line mt-3" />

        <Steppy
          v-model:step="step"
          nextText="Next"
          backText="Back"
          doneText="Create"
          :tabs="tabs"
        >
          <template #1>
            <v-form ref="form">
              <p class="ml-2 text-left text-darkBlue font-weight-bold">
                Event Type<span class="text-gradient-red">*</span>
              </p>
              <v-autocomplete
                :loading="isLoading"
                v-model="state._eventType"
                :items="listEventType"
                variant="solo"
                placeholder="Choose event type"
                class="px-2 mt-1"
                item-title="value"
                item-value="id"
                return-object
              ></v-autocomplete>

              <p class="ml-2 text-left text-darkBlue font-weight-bold">
                RDG Type<span class="text-gradient-red">*</span>
              </p>
              <v-autocomplete
                :loading="isLoading"
                v-model="state._rdgType"
                :items="listRDGType"
                variant="solo"
                placeholder="Choose RDG type"
                class="px-2 mt-1"
                item-title="value"
                item-value="id"
                return-object
              ></v-autocomplete>

              <!-- MONTH, YEAR -->
              <v-sheet class="d-flex flex-row">
                <div style="width: 50%">
                  <p class="ml-2 text-left text-darkBlue font-weight-bold">
                    Month<span class="text-gradient-red">*</span>
                  </p>
                  <v-autocomplete
                    :loading="isLoading"
                    v-model="state._month"
                    :items="listMonths"
                    variant="solo"
                    placeholder="Choose month"
                    class="px-2 mt-1"
                    item-title="name"
                    item-value="id"
                    return-object
                    ><template v-slot:append-inner>
                      <img
                        :src="require('@/v2/assets/icon/date.svg')"
                      /> </template
                  ></v-autocomplete>
                </div>
                <div style="width: 50%">
                  <p class="ml-2 text-left text-darkBlue font-weight-bold">
                    Year<span class="text-gradient-red">*</span>
                  </p>
                  <v-autocomplete
                    :loading="isLoading"
                    v-model="state._year"
                    :items="getYearPickerData()"
                    variant="solo"
                    placeholder="Choose year"
                    class="px-2 mt-1"
                    return-object
                    ><template v-slot:append-inner>
                      <img
                        :src="require('@/v2/assets/icon/date.svg')"
                      /> </template
                  ></v-autocomplete>
                </div>
              </v-sheet>
              <!-- END OF MONTH, YEAR -->
              <p class="ml-2 text-left text-darkBlue font-weight-bold">
                RDG<span class="text-gradient-red">*</span>
              </p>
              <v-autocomplete
                :loading="isLoading"
                v-model="state._rdg"
                :items="listRDG"
                variant="solo"
                placeholder="Choose RDG"
                class="px-2 mt-1"
                item-title="eventName"
                item-value="idEvent"
                return-object
              ></v-autocomplete>
            </v-form>
          </template>
          <template #2>
            <p class="ml-2 text-left text-darkBlue font-weight-bold">Sector</p>
            <v-autocomplete
              :loading="isLoading"
              v-model="formRequest.sector"
              :items="sectorList"
              variant="solo"
              placeholder="Choose Sector"
              class="px-2 mt-1 mb-4"
              item-title="value"
              item-value="id"
              return-object
            ></v-autocomplete>
            <div
              v-for="(form, i) in formRequest.forms"
              :key="i"
              class="rounded-lg px-2 py-4"
              :class="i != 0 ? 'mt-4' : ''"
              style="border: 2px #babcca solid"
            >
              <button
                v-if="i != 0"
                class="btn btn-delete-form"
                type="button"
                @click="deleteForm(i)"
              >
                <v-icon
                  icon="mdi-delete"
                  color="#D6212A"
                  size="x-small"
                ></v-icon>
              </button>
              <p class="text-left text-darkBlue font-weight-bold form-title">
                Form {{ i + 1 }}
              </p>
              <div class="px-2 py-2">
                <p class="text-darkBlue font-weight-bold my-3">Title</p>
                <v-text-field
                  variant="solo"
                  placeholder="Insert Title"
                  v-model="formRequest.forms[i].title"
                  :hide-details="
                    !hasNestedError(v$.forms.$each.$response.$errors[i].title)
                  "
                  :error-messages="
                    hasNestedError(v$.forms.$each.$response.$errors[i].title)
                      ? checkNestedError(
                          v$.forms.$each.$response.$errors[i].title,
                          {
                            unique: 'title tidak boleh ada yang sama',
                          }
                        )
                      : []
                  "
                ></v-text-field>
                <p class="text-darkBlue font-weight-bold my-4">Section</p>
                <template v-for="(section, y) in form.sections" :key="y">
                  <div class="d-flex" :class="y != 0 ? 'mt-2' : ''">
                    <v-autocomplete
                      variant="solo"
                      placeholder="Choose Section"
                      item-title="Value"
                      item-value="Id"
                      class="mr-3"
                      v-model="formRequest.forms[i].sections[y].id"
                      :items="listSection"
                      :hide-details="true"
                      :loading="isLoading"
                      :menu-props="{ maxHeight: 390 }"
                    ></v-autocomplete>
                    <button
                      type="button"
                      @click="addSection(i)"
                      class="btn btn-delete-section bg-blue-gradient"
                      :loading="isLoading"
                      v-if="
                        (y == form.sections.length - 1 && y < limitSection) ||
                        (y == form.sections.length - 1 && limitSection == -1)
                      "
                    >
                      <v-icon
                        icon="mdi-plus"
                        color="#fff"
                        size="large"
                      ></v-icon>
                    </button>
                    <button
                      type="button"
                      @click="deleteSection(i, y)"
                      class="btn btn-delete-section"
                      :loading="isLoading"
                      v-else
                    >
                      <v-icon
                        icon="mdi-delete"
                        color="#D6212A"
                        size="large"
                      ></v-icon>
                    </button>
                    <span
                      class="text-danger ml-5 text-12"
                      v-if="
                        hasNestedError(
                          v$.forms.$each.$response.$errors[i].sections[0]
                            ?.$response?.$errors[y].id ?? []
                        )
                      "
                    >
                      {{
                        checkNestedError(
                          v$.forms.$each.$response.$errors[i].sections[0]
                            ?.$response?.$errors[y].id ?? []
                        ).join(", ")
                      }}
                    </span>
                  </div>
                </template>
              </div>
            </div>
            <div class="text-left mt-4">
              <v-btn
                elevation="3"
                class="btn-create"
                @click="addForm"
                :loading="isLoading"
              >
                <v-icon icon="mdi-plus" color="#fff"></v-icon> Add Form
              </v-btn>
            </div>
          </template>
        </Steppy>
        <div class="text-right pb-5 pr-15 mt-n10">
          <v-btn
            class="btn-prev mr-3"
            @click="negativeClick"
            elevation="4"
            width="100"
            height="45"
            :loading="isLoading"
            >{{ step == 1 ? "Cancel" : "Back" }}</v-btn
          >
          <v-btn
            class="btn-next"
            @click="positiveClick"
            elevation="4"
            width="100"
            height="45"
            :loading="isLoading"
            :disabled="!buttonNext"
            >{{ step != 2 ? "Next" : "Create" }}</v-btn
          >
        </div>
      </v-card>
    </v-dialog>
  </Teleport>
</template>
<script setup lang="ts">
import { Steppy } from "vue3-steppy";
import { useCreatePNIN } from "@/v2/composables/event/PNIN";

// Use the composable
const {
  // Form state
  state,
  formRequest,
  listMonths,

  // API state
  isLoading,
  listEventType,
  listRDGType,
  listRDG,
  sectorList,

  // Dialog state
  dialog,
  currentTitle,
  step,
  buttonNext,
  tabs,
  isShowDialog,
  listSection,
  limitSection,

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
} = useCreatePNIN();

defineExpose({
  showDialogEvent,
});
</script>

<style lang="scss" scoped>
.ellipsis-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 320px;
}

.error-border {
  border: 1px solid #b13737 !important;
}

.bg-blue-gradient {
  background: linear-gradient(#065695 -46.47%, #267dc2 157.9%);
}

:deep(.dp__overlay) {
  border-radius: 10px;
}
:deep(.dp__instance_calendar) {
  box-shadow: 1px 1px 7px 3px #7393b3;
  border-radius: 5px;
  padding: 10px;
}

:deep(.dp__overlay_cell_disabled) {
  display: none;
}

:deep(.dp__arrow_top) {
  display: none;
}
:deep(.dp__input_icon_pad) {
  background: white;
  border-radius: 12px;
  box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
    0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
    0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12));
  height: 5.5vh;
}

.chip-shadow {
  box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
    0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
    0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12));
  height: 56px;
  width: 94%;
  color: grey;
  font-size: 16px;
}

.red-color {
  color: red;
}

:deep(.v-chip__append) {
  position: absolute;
  right: 0;
  margin-right: 0.5vw;
}
.gradient-box {
  display: flex;
  align-items: center;
  margin: auto;

  position: relative;
  box-sizing: border-box;

  $border: 2px;
  background: #fff;
  background-clip: padding-box; /* !important */
  border: solid $border transparent; /* !important */
  border-radius: 15px;

  &:before {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: -1;
    margin: -$border; /* !important */
    border-radius: inherit; /* !important */
    background: linear-gradient(to right, #267dc2, #ff000d);
  }
}

.text-blueRedTheme-gradien {
  background: -webkit-linear-gradient(left, #267dc2, #ff000d);
  background: linear-gradient(to right, #267dc2, #ff000d);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.btn-close {
  position: absolute;
  right: 0;
  top: 0;
  margin-top: 10px;
  margin-right: 10px;
}

.line {
  border: none; /* Remove the default border */
  min-height: 2px; /* Set the height of the hr */
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}

:deep(.v-field.v-field--appended) {
  border-radius: 12px !important;
}

:deep(.steppy) {
  margin-top: 25px;
  margin-left: 25%;
  margin-right: 25%;
}
:deep(.number) {
  display: none !important;
}

:deep(.wrapper-steppy) {
  padding-left: 20px !important;
  padding-bottom: 0px !important;
  padding-right: 20px !important;
  padding-top: 25px;
}

:deep(.steppy-pane) {
  box-shadow: none !important;
  text-align: left !important;
}
:deep(.steppy-item.success .steppy-item-counter) {
  border: 8px solid #267dc2 !important;
}

:deep(.steppy-item-counter) {
  height: 20px !important;
  width: 20px !important;
  border: 5px solid grey !important;
  background-color: white !important;
}

:deep(.steppy-item.success .steppy-item-counter .icon-success) {
  width: 15px !important;
  height: 15px !important;
  fill: white !important;
  background-color: #267dc2 !important;
  border-radius: 50% !important;
}

:deep(.steppy-item-title) {
  font-size: 14px !important;
  font-weight: 900 !important;
  color: #3a416f !important;
  white-space: nowrap !important;
}

:deep(.steppy-progress) {
  background: #d9d9d9 !important;
  height: 3px !important;
}

:deep(.steppy-progress-bar) {
  background: #267dc2 !important;
  height: 3px !important;
}
:deep(.controls) {
  display: none !important;
}

:deep(.v-field--error) {
  border: 1px solid #b13737 !important;
}
:deep(.v-messages__message) {
  line-height: 12px;
  word-break: break-word;
  overflow-wrap: break-word;
  word-wrap: break-word;
  -webkit-hyphens: auto;
  hyphens: auto;
  transition-duration: 154ms;
  font-size: 13px;
  font-style: normal;
  font-weight: 600;
  font-family: Poppins;
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
  /* border-color: #267dc2 !important; */
  padding-left: 16px !important;
  padding-right: 16px !important;
  font-size: 14px !important;

  color: #267dc2;
  font-weight: 900;
}
.hide {
  display: none;
}

.show {
  display: show;
}

.btn-create {
  background: linear-gradient(#065695 -46.47%, #267dc2 157.9%);
  border-radius: 10px;
  padding-left: 15px;
  padding-right: 15px;
  font-weight: 800;
  width: 120px;
  color: white !important;
}

.form-title {
  margin-top: -28px;
  margin-left: 20px;
  background-color: white;
  width: fit-content;
}

.btn-delete-form {
  position: absolute;
  right: 0;
  margin-top: -16px;
  margin-right: 47px;
  padding: 1px 6px 2px 6px;
  border-radius: 0px 7px 0px 7px;
}

.btn-delete-section {
  padding: 10px;
  margin: 5px 0px 5px 5px;
  border-radius: 10px;
}
</style>
