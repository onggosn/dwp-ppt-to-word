<template>
  <v-dialog
    persistent
    v-model="dialog"
    content-class="overflowyhid"
    :max-width="600"
  >
    <v-card>
      <v-card-title class="d-flex justify-center align-center">
        <div class="text-18 text-blueTheme fw-500">Edit Metadata Task</div>
        <v-btn
          class="mr-2"
          style="position: absolute; right: 0"
          variant="text"
          icon="mdi-close"
          @click="hide()"
        ></v-btn>
      </v-card-title>
      <v-card-text class="pb-4">
        <div
          class="separatorHorizontalGradient"
          style="margin-top: -16px"
        ></div>
        <v-row class="my-3">
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">
              Task Name <span class="text-redTheme">*</span>
            </div>
            <v-text-field
              placeholder="Masukan task name"
              variant="solo"
              v-model="formData.taskName"
              :error-messages="e(v$.formData.taskName)"
              @blur="v$.formData.taskName.$touch"
            />
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">
              Description <span class="text-redTheme">*</span>
            </div>
            <v-textarea
              placeholder="Masukan deskripsi"
              variant="solo"
              v-model="formData.description"
              :error-messages="e(v$.formData.description)"
              @blur="v$.formData.description.$touch"
            />
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">
              PIC <span class="text-redTheme">*</span>
            </div>
            <v-autocomplete
              ref="autoCompletePic"
              multiple
              chips
              single-line
              item-title="name"
              return-object
              variant="solo"
              clearable
              density="comfortable"
              placeholder="Choose PIC"
              hide-selected
              closable-chips
              v-model="formData.pic"
              :items="itemsPic"
              :error-messages="e(v$.formData.pic)"
              :menu-props="{ 'max-width': 200 }"
              v-model:search="searchPic"
              @update:modelValue="selectedPic"
            >
              <template v-slot:no-data>
                <span class="d-flex align-item-center ma-2 pa-1 select-empty">
                  Search name...
                </span>
              </template>
              <template v-slot:item="{ props, item }">
                <v-list-item
                  v-bind="props"
                  :prepend-avatar="item?.raw?.avatar"
                  :title="item?.raw?.name"
                  :subtitle="item?.raw?.email"
                ></v-list-item>
              </template>
            </v-autocomplete>
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">
              Contributor <span class="text-redTheme">*</span>
            </div>
            <v-autocomplete
              ref="autoCompleteContributor"
              multiple
              clearable
              chips
              single-line
              item-title="name"
              return-object
              variant="solo"
              density="comfortable"
              placeholder="Choose Contributor"
              hide-selected
              closable-chips
              v-model="formData.contributor"
              :items="itemsContributor"
              :error-messages="e(v$.formData.contributor)"
              :menu-props="{ 'max-width': 200 }"
              v-model:search="searchContributor"
              @update:modelValue="selectedContributor"
            >
              <template v-slot:no-data>
                <span class="d-flex align-item-center ma-2 pa-1 select-empty">
                  Search name...
                </span>
              </template>
              <template v-slot:item="{ props, item }">
                <v-list-item
                  v-bind="props"
                  :prepend-avatar="item?.raw?.avatar"
                  :title="item?.raw?.name"
                  :subtitle="item?.raw?.email"
                ></v-list-item>
              </template>
            </v-autocomplete>
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">Participant</div>
            <v-autocomplete
              ref="autoCompleteParticipant"
              multiple
              clearable
              chips
              single-line
              return-object
              item-title="name"
              variant="solo"
              density="comfortable"
              placeholder="Choose Participant"
              hide-selected
              closable-chips
              v-model="formData.participant"
              :items="itemsParticipant"
              :error-messages="e(v$.formData.participant)"
              :menu-props="{ 'max-width': 200 }"
              v-model:search="searchParticipant"
              @update:modelValue="selectedParticipant"
            >
              <template v-slot:no-data>
                <span class="d-flex align-item-center ma-2 pa-1 select-empty">
                  Search name...
                </span>
              </template>
              <template v-slot:item="{ props, item }">
                <v-list-item
                  v-bind="props"
                  :prepend-avatar="item?.raw?.avatar"
                  :title="item?.raw?.name"
                  :subtitle="item?.raw?.email"
                ></v-list-item>
              </template>
            </v-autocomplete>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="justify-end pr-6 pt-0 pb-4">
        <v-btn class="btn-action btn-action-close" @click="hide()">
          Close
        </v-btn>
        <v-btn
          class="btn-action btn-action-create"
          @click="process()"
          :loading="loading[4]"
          :disabled="loading[4]"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";
import { getErrorMessages, isError } from "@/library/ValidationHelper";
import client from "@/library/ApiClient";

export default {
  name: "editParticipantDialog",
  emits: ["submit"],
  components: {},
  setup: () => ({ v$: useVuelidate() }),
  validations() {
    let formData = {
      taskName: { required },
      description: { required },
      pic: { required },
      contributor: { required },
    };
    return { formData };
  },
  data() {
    return {
      dialog: false,
      loading: [],
      taskId: null,
      item: {},
      formData: {
        taskName: null,
        description: null,
        pic: null,
        contributor: null,
        participant: null,
      },
      itemsPic: [],
      itemsContributor: [],
      itemsParticipant: [],
      searchPic: null,
      searchContributor: null,
      searchParticipant: null,
    };
  },
  watch: {
    searchPic(val) {
      if (val != "") this.searchUser(val, "pic");
    },
    searchContributor(val) {
      if (val != "") this.searchUser(val, "contributor");
    },
    searchParticipant(val) {
      if (val != "") this.searchUser(val, "participant");
    },
  },
  methods: {
    e: getErrorMessages,
    isError: isError,
    show(item) {
      this.item = item;
      this.formData.taskName = item.taskName;
      this.formData.description = item.descriptions;
      this.itemSelected(item);
      this.dialog = true;
    },
    itemSelected(item) {
      // debugger;
      if (item.pic) {
        this.itemsPic = item.pic.map((el) => {
          return {
            username: el.username,
            groupName: el.groupName,
            memberType: 1,
            name: el.name,
            email: el.email ?? "-",
          };
        });
      }
      if (item.contributor) {
        this.itemsContributor = item.contributor.map((el) => {
          return {
            username: el.username,
            groupName: el.groupName,
            memberType: 2,
            name: el.name,
            email: el.email ?? "-",
          };
        });
      }

      if (item.participant) {
        this.itemsParticipant = item.participant.map((el) => {
          return {
            username: el.username,
            groupName: el.groupName,
            memberType: 3,
            name: el.name,
            email: el.email ?? "-",
          };
        });
      }

      this.formData.pic = this.itemsPic;
      this.formData.contributor = this.itemsContributor;
      this.formData.participant = this.itemsParticipant;
    },
    hide() {
      this.dialog = false;
    },
    process() {
      this.v$.$validate().then((res) => {
        if (res) {
          // debugger;
          this.loading[4] = true;
          const members = [
            ...this.formData.pic,
            ...this.formData.contributor,
            ...this.formData.participant,
          ];

          let data = {
            idTaskTemplate: this.item.idTaskTemplate,
            idActivity: this.item.idActivity,
            taskName: this.formData.taskName,
            descriptions: this.formData.description,
            taskMemberTemplate: members,
          };

          client
            .updateTaskTemplate({
              store: this.$store,
              data: data,
            })
            .then((res) => {
              // debugger;
              this.$root.toast.show({
                message: res.plainData.responseData.descriptions,
                color:
                  res.plainData.responseCode == "011000" ? "success" : "error",
                timeout: 5000,
              });
              this.hide();
              this.$emit("submit");
            })
            .catch((err) => {
              this.$root.toast.show({
                message: err.message ?? "Maaf, terjadi kesalahan sistem",
                color: "error",
                timeout: 500000,
              });
            })
            .finally(() => {
              this.loading[4] = false;
            });
        }
      });
    },
    searchUser(query, type) {
      client
        .SearchUserByname({
          store: this.$store,
          data: {
            name: query,
          },
        })
        .then((res) => {
          // debugger;
          if (type === "pic") {
            this.itemsPic = res.plainData
              .filter((elm) => {
                const tmp = this.formData.contributor.filter((fil) => {
                  return [fil.groupName, fil.username].includes(elm.inputId);
                });
                return tmp.length == 0;
              })
              .filter((elm) => {
                const tmp = this.formData.participant.filter((fil) => {
                  return [fil.groupName, fil.username].includes(elm.inputId);
                });
                return tmp.length == 0;
              })
              .map((el) => {
                return {
                  username: el.isGrup == true ? "" : el.inputId,
                  name: el.inputName,
                  groupName: el.isGrup == true ? el.inputId : "",
                  memberType: 1,
                  email: el.inputEmail,
                };
              });
          } else if (type === "contributor") {
            this.itemsContributor = res.plainData
              .filter((elm) => {
                const tmp = this.formData.pic.filter((fil) => {
                  return [fil.groupName, fil.username].includes(elm.inputId);
                });
                return tmp.length == 0;
              })
              .filter((elm) => {
                const tmp = this.formData.participant.filter((fil) => {
                  return [fil.groupName, fil.username].includes(elm.inputId);
                });
                return tmp.length == 0;
              })
              .map((el) => {
                return {
                  username: el.isGrup == true ? "" : el.inputId,
                  name: el.inputName,
                  groupName: el.isGrup == true ? el.inputId : "",
                  memberType: 2,
                  email: el.inputEmail,
                };
              });
          } else {
            this.itemsParticipant = res.plainData
              .filter((elm) => {
                const tmp = this.formData.pic.filter((fil) => {
                  return [fil.groupName, fil.username].includes(elm.inputId);
                });
                return tmp.length == 0;
              })
              .filter((elm) => {
                const tmp = this.formData.contributor.filter((fil) => {
                  return [fil.groupName, fil.username].includes(elm.inputId);
                });
                return tmp.length == 0;
              })
              .map((el) => {
                return {
                  username: el.isGrup == true ? "" : el.inputId,
                  name: el.inputName,
                  groupName: el.isGrup == true ? el.inputId : "",
                  memberType: 3,
                  email: el.inputEmail,
                };
              });
          }
        })
        .finally(() => {
          this.loading[1] = false;
        });
    },
    selectedPic() {
      this.$refs.autoCompletePic.blur();
    },
    selectedContributor() {
      this.$refs.autoCompleteContributor.blur();
    },
    selectedParticipant() {
      this.$refs.autoCompleteParticipant.blur();
    },
  },
  computed: {},
};
</script>

<style scoped>
.overflowyhid {
  overflow-y: hidden;
  padding-bottom: 5px;
}

.select-empty {
  cursor: pointer;
}
:deep(.cursor-pointer input) {
  cursor: pointer !important;
}
:deep(.v-field--disabled) {
  background-color: rgb(168 160 160) !important;
}
:deep(.v-autocomplete__selection .v-chip) {
  background: #267dc2 !important;
  color: white !important;
}
</style>
