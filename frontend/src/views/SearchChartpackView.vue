<template>
  <div>
    <v-row class="ma-2">
      <v-col cols="12" sm="9">
        <v-btn icon="mdi-arrow-left" size="large" @click="back" class="mr-2">
        </v-btn>
        <span
          class="text-20 fw-500"
          style="text-align: left; color: rgb(58, 65, 111)"
        >
          Hasil pencarian yang ditampilkan {{ resultSearch.length }} (total
          hasil relevan {{ resultSearch.length }})</span
        >
      </v-col>
      <v-col cols="12" sm="3">
        <v-text-field
          v-model="searchKeyword"
          clearable
          placeholder="Search"
          variant="solo"
          prepend-inner-icon="mdi-magnify"
          @keyup.enter="search()"
        ></v-text-field>
      </v-col>
    </v-row>
    <template v-if="resultSearch.length > 0">
      <v-card
        v-for="(item, index) in resultSearch"
        @click="openDetail(item)"
        :key="index"
        class="card-custom ma-5"
        style="cursor: pointer"
      >
        <v-row>
          <v-col md="10">
            <div
              class="pl-6 mt-2 text-blackTheme fw-700 text-18"
              v-html="highlightText(item.documentName)"
            ></div>
            <div
              class="pl-6 mt-2 text-blackTheme fw-400 text-14"
              v-html="
                highlightText(
                  'Area' +
                    item.area +
                    ', Sektor ' +
                    item.sektor +
                    ', Keywords : ' +
                    item.keyword
                )
              "
            ></div>
          </v-col>
          <v-col md="2">
            <div class="d-flex flex-column align-center mt-5">
              <v-img
                src="/images/graph.png"
                cover
                :width="90"
                :height="90"
              ></v-img>
            </div>
          </v-col>
        </v-row>
      </v-card>
    </template>
    <template v-else>
      <div class="row">
        <div class="col-lg-12">
          <div class="d-flex align-items-center justify-content-center">
            <v-img
              src="/images/chartpack/emptybox.png"
              :height="400"
              :width="400"
            ></v-img>
          </div>
          <div class="text-center" style="margin-top: -50px">
            <b><i>No Data Available</i></b>
          </div>
        </div>
      </div>
    </template>

    <detail-meeting ref="detailDialog"> </detail-meeting>
    <loading-dialog v-if="isLoading"></loading-dialog>
  </div>
</template>
<script lang="js">
import Client from "@/library/ApiClient";
import LoadingDialog from "@/components/LoadingDialog.vue";
import DetailMeeting from "@/components/meeting/DetailMeetingDialog";

export default {
  name: "SearchMeeting",
  components:{
    LoadingDialog,
    DetailMeeting
  },
  data: () => ({
    historySearch : "",
    isLoading : false,
    resultSearch : "",
    searchKeyword: "",
    idLevel: "",
  }),
  mounted(){
    this.searchKeyword = typeof this.$route.params.searchKeyword !== "undefined" ? this.$route.params.searchKeyword : "";
    this.search();
  },
  methods:{
    highlightText(text){
      const escapedSearch = this.historySearch.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      return text.replaceAll(RegExp("("+escapedSearch+")","ig"), `<span class="highlight">$1</span>`);
    },
    clearSearch(){
      this.searchKeyword="";
    },
    openDetail(item){
      this.$router.replace({
        name : "chartpack",
        params : {
          idChartpack : item.id,
          searchKeyword : this.searchKeyword,
          choosedPdf : item
        }
      })
    },
    search(){
      this.isLoading = true;
      Client.SearchChartpack({
        store: this.$store,
        data:{
          searchParam : this.searchKeyword
        }
      }).then((res)=>{
        this.resultSearch = res.plainData;
        this.historySearch = this.searchKeyword;
        this.isLoading = false;
      }).
      catch(() =>{
        this.isLoading = false;
      })
    },
    back(){
      this.$router.go(-1);
    }
  }
};
</script>
<style scoped>
.card-custom {
  margin-bottom: 30px;
  margin-top: 20px;
  background: #ffffff;
  /* block drop shadow */
  /* box-shadow: -2px -2px 9px 5px rgba(192, 192, 192, 0.25) !important; */
  box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
    0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
    0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12)) !important;
  border-radius: 23px !important;
}
:deep(.highlight) {
  background: orange;
}
</style>
