<template>
  <v-card
    class="pb-10 mt-5"
    style="
      border-left: 4px solid #267dc2;
      box-shadow: 0px 4px 18px rgba(192, 192, 192, 0.25);
      border-radius: 10px;
    "
  >
    <div class="pl-6 pt-6 font-weight-bold text-blueTheme-gradien">
      List Template
    </div>
    <div v-if="isLoading" class="mx-6 mt-3">
      <v-row>
        <v-col cols="12" v-for="idx in 4" :key="idx">
          <paragraph-shimmer
            :is-loading="true"
            :lines="2"
            :random-size="false"
          />
        </v-col>
      </v-row>
    </div>
    <div class="mx-6 mt-3" v-else>
      <v-table>
        <thead>
          <tr>
            <th class="text-center header font-weight-bold" style="width: 40px">
              No
            </th>
            <th class="text-center header font-weight-bold">Nama File</th>
            <th class="text-center header font-weight-bold">Tipe Dokumen</th>
            <th class="text-center header font-weight-bold">Tipe Activity</th>
            <th class="text-center header font-weight-bold" style="width: 20%">
              Type Task
            </th>
            <th class="text-center header"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, idx) in items" :key="idx" style="font-size: 13px">
            <td class="text-center">
              {{ getNumber(++idx) }}
            </td>
            <td class="text-left">
              {{ item.namaFile != "" ? item.namaFile : "-" }}
            </td>
            <td class="text-center">{{ item.tipeDokumen ?? "-" }}</td>
            <td class="text-center">{{ item.tipeActivity ?? "-" }}</td>
            <td class="text-center">{{ item.tipeTask ?? "-" }}</td>
            <td class="text-center">
              <v-btn variant="text" @click="action(item)">
                <v-icon class="table-content-center" color="#267DC2" small
                  >mdi-pencil</v-icon
                >
                <v-tooltip activator="parent" location="top"
                  >Edit Template</v-tooltip
                >
              </v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
    </div>
  </v-card>
  <edit-template-dialog ref="modal_edit_template" @submit="reloadPage" />
</template>
<script>
import EditTemplateDialog from "@/components/administrator/EditTemplateDialog.vue";
export default {
  name: "adminTemplateComponent",
  emits: ["reloadPage"],
  components: {
    EditTemplateDialog,
  },
  props: {
    items: {
      type: Array,
      default: function () {
        return [];
      },
    },
    loading: {
      type: Boolean,
      default: false,
    },
    pagination: {
      page: null,
      total: null,
      visible: null,
      entriesPerPage: null,
    },
  },
  data() {
    return {
      isLoading: this.loading,
    };
  },
  methods: {
    action(item) {
      this.$refs.modal_edit_template.show(item);
    },
    getNumber(index) {
      let pageNo = parseInt(this.pagination.page);
      let entriesPerPage = parseInt(this.pagination.entriesPerPage);
      let number = index + (pageNo - 1) * entriesPerPage;

      return number;
    },
    reloadPage() {
      this.$emit("reloadPage");
    },
  },
  watch: {
    loading(val) {
      this.isLoading = val;
    },
  },
};
</script>
<style>
.text-blueTheme-gradien {
  background: -webkit-linear-gradient(#065695, #267dc2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-blueTheme-gradien {
  background: -webkit-linear-gradient(#065695, #267dc2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
:deep(
    v-table--density-default > .v-table__wrapper > table > tbody > tr > th,
    .v-table--density-default > .v-table__wrapper > table > thead > tr > th,
    .v-table--density-default > .v-table__wrapper > table > tfoot > tr > th
  ) {
  border-top: thin solid #e0e0e0 !important;
}
</style>
