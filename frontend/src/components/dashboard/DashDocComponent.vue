<template>
  <v-card
    class="pb-10 mt-5"
    style="
      border-left: 4px solid #267dc2;
      box-shadow: 0px 4px 18px rgba(192, 192, 192, 0.25);
      border-radius: 10px;
    "
  >
    <v-sheet class="pl-6 pt-6 font-weight-bold text-blueTheme-gradien">
      List Document
    </v-sheet>
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
          <tr style="color: red">
            <th class="text-center header font-weight-bold" style="width: 40px">
              No
            </th>
            <th class="text-center header font-weight-bold" style="width: 30%">
              Nama
            </th>
            <th class="text-center header font-weight-bold" style="width: 10%">
              Satker
            </th>
            <th class="text-center header font-weight-bold" style="width: 10%">
              PS
            </th>
            <th class="text-center header font-weight-bold" style="width: 17%">
              Penyusun
            </th>
            <th class="text-center header font-weight-bold" style="width: 15%">
              Pengaju
            </th>
            <th class="text-center header font-weight-bold" style="width: 15%">
              Penyetuju
            </th>
            <th class="text-center header font-weight-bold" style="width: 10%">
              Status
            </th>
            <th class="text-center header"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, idx) in items" :key="idx" style="font-size: 13px">
            <!-- <pre>{{ item }}</pre> -->
            <td class="text-center text-12">{{ getNumber(++idx) }}</td>
            <td class="text-left text-12">
              <span class="ellipsis"
                >{{ item.documentNameDisplay }}
                <v-tooltip activator="parent" location="top">{{
                  item.documentNameDisplay
                }}</v-tooltip></span
              >
            </td>
            <td class="text-center text-12">
              <p class="ellipsis">
                {{ item.satker ?? "-"
                }}<v-tooltip activator="parent" location="top">{{
                  item.satker
                }}</v-tooltip>
              </p>
            </td>
            <td class="text-center text-12">
              <p class="ellipsis">
                {{ item.programStrategisName ?? "-"
                }}<v-tooltip activator="parent" location="top">{{
                  item.programStrategisName
                }}</v-tooltip>
              </p>
            </td>
            <td class="text-center text-12">
              <p class="ellipsis">
                {{ item.listPenyusun ?? "-"
                }}<v-tooltip activator="parent" location="top">{{
                  item.listPenyusun
                }}</v-tooltip>
              </p>
            </td>
            <td class="text-center text-12">
              <p class="ellipsis">
                {{ item.pengaju ?? "-"
                }}<v-tooltip activator="parent" location="top">{{
                  item.pengaju
                }}</v-tooltip>
              </p>
            </td>
            <td class="text-center text-12">
              <p class="ellipsis">
                {{ item.penyetuju ?? "-"
                }}<v-tooltip activator="parent" location="top">{{
                  item.penyetuju
                }}</v-tooltip>
              </p>
            </td>
            <td class="text-center">
              <p
                class="text-12"
                :style="{ color: getColorStatus(item.statusDoc) }"
              >
                {{ item.statusDoc }}
              </p>
            </td>
            <td class="text-left">
              <v-btn
                variant="text"
                :to="{
                  name:
                    item.typeDocument == 'pendukung'
                      ? 'preview-document-support'
                      : 'preview-document',
                  params: {
                    documentId: item.id,
                    workspaceId: item.idWorkspace,
                    taskId: item.taskId,
                    pageId: 1,
                  },
                }"
              >
                <v-icon
                  class="table-content-center"
                  color="#267DC2"
                  small
                  style="
                    border: 1px solid;
                    border-radius: 4px;
                    padding: 13px;
                    cursor: pointer;
                  "
                  >mdi-file-document-outline</v-icon
                >
              </v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
    </div>
  </v-card>
</template>

<script>
export default {
  name: "dashDocComponent",
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
    },
  },
  data() {
    return {
      isLoading: this.loading,
    };
  },
  methods: {
    getColorStatus(status) {
      status = status.toLowerCase();
      if (status == "in progress") {
        return "#fe7411";
      } else if (status == "approved") {
        return "#02aa59";
      } else if (status == "rejected") {
        return "red";
      } else if (status == "need for approval") {
        return "#fe7411";
      }
      return "#fe7411";
    },
    getNumber(index) {
      let pageNo = parseInt(this.pagination.page);
      let entriesPerPage = parseInt(this.pagination.visible);
      let number = index + (pageNo - 1) * entriesPerPage;

      return number;
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
.header {
  text-align: center;
  font-weight: 900;
  color: #3a416f;
}

.text-blueTheme-gradien {
  background: -webkit-linear-gradient(#065695, #267dc2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
