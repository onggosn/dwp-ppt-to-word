<template>
  <v-dialog
    persistent
    v-model="dialog"
    content-class="overflowyhid"
    :max-width="600"
  >
    <v-card>
      <v-card-title class="d-flex justify-center align-center">
        <div class="text-18 text-blueTheme fw-500">Edit Role</div>
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
        <v-row class="my-1">
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">Nama User</div>
            <v-text-field
              disabled
              placeholder="Masukan Nama User"
              variant="solo"
              v-model="formData.nama"
              :error-messages="e(v$.formData.nama)"
              @blur="v$.formData.nama.$touch"
            />
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">Satker</div>
            <v-text-field
              disabled
              placeholder="Masukan Satker"
              variant="solo"
              v-model="formData.satker"
              :error-messages="e(v$.formData.satker)"
              @blur="v$.formData.satker.$touch"
            />
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">Jabatan</div>
            <v-text-field
              disabled
              placeholder="Masukan Jabatan"
              variant="solo"
              v-model="formData.jabatan"
              :error-messages="e(v$.formData.jabatan)"
              @blur="v$.formData.jabatan.$touch"
            />
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">Role</div>
            <v-autocomplete
              ref="selectRole"
              multiple
              chips
              single-line
              item-title="name"
              item-value="id"
              variant="solo"
              density="comfortable"
              placeholder="Choose Role"
              clearable
              hide-selected
              closable-chips
              v-model="formData.idRole"
              :items="itemsRole"
              :error-messages="e(v$.formData.idRole)"
              :menu-props="{ 'max-width': 200 }"
              :loading="loading[1]"
              @update:modelValue="counterRole"
            >
              <template v-slot:no-data>
                <span class="d-flex align-item-center ma-2 pa-1 select-empty">
                  <!-- <v-icon class="mr-2">mdi-reload</v-icon> -->
                  Data tidak ditemukan
                </span>
              </template>
            </v-autocomplete>
            <div
              class="v-messages"
              role="alert"
              v-if="errMessage"
              style="margin-top: -10px; color: red"
            >
              Maksimal 6 Role
            </div>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="justify-end pr-6 pt-0 pb-4">
        <v-btn class="btn-action btn-action-close" @click="hide()">
          Cancel
        </v-btn>
        <v-btn
          class="btn-action btn-action-create"
          @click="process()"
          :loading="loading"
          :disabled="loading"
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
import { mGetListRole } from "@/models/Administrator";

export default {
  name: "editRole",
  components: {},
  setup: () => ({ v$: useVuelidate() }),
  validations() {
    let formData = {
      nama: { required },
      satker: { required },
      jabatan: { required },
    };
    return { formData };
  },
  data() {
    return {
      dialog: false,
      loading: false,
      taskId: null,
      item: {},
      formData: {
        nama: null,
        satker: null,
        jabatan: null,
        idRole: null,
        username: null,
      },
      itemsRole: [],
      errMessage: false,
    };
  },
  created() {
    this.getMasterData();
  },
  methods: {
    e: getErrorMessages,
    isError: isError,
    show(item) {
      this.formData.nama = item.name != "" ? item.name : "-";
      this.formData.satker = item.satker ?? "-";
      this.formData.jabatan = item.jabatan ?? "-";
      this.formData.idRole = item.roleId;
      this.formData.username = item.username != "" ? item.username : "-";
      this.dialog = true;
    },
    hide() {
      this.dialog = false;
    },
    process() {
      this.v$.$validate().then((res) => {
        if (res) {
          this.loading = true;
          let data = {
            username: this.formData.username,
            roleId: this.formData.idRole,
          };
          client
            .updateUserRoleByUsername({
              store: this.$store,
              data: data,
            })
            .then((res) => {
              this.$root.toast.show({
                message: res.plainData.responseMessage,
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
              this.loading = false;
            });
        }
      });
    },
    getMasterData() {
      mGetListRole().then((res) => {
        this.itemsRole = res.plainData.responseData.data;
      });
    },
    counterRole() {
      this.$refs.selectRole.blur();
      if (this.formData.idRole.length > 6) {
        this.formData.idRole.pop();
        this.errMessage = true;
      } else {
        this.errMessage = false;
      }
    },
  },
  computed: {},
  watch: {},
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
