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
        @click="detailMeeting(item)"
        :key="index"
        class="card-meeting ma-5"
        style="cursor: pointer"
      >
        <v-row>
          <v-col md="10">
            <div class="pl-6 mt-4 text-blackTheme fw-200 text-10">
              {{ $filters.formatTimeEngtoInd(item.startDate) }}
            </div>
            <div
              class="pl-6 mt-2 text-blackTheme fw-600 text-16"
              v-html="highlightText(item.meetingName)"
            ></div>
            <div class="pl-6 mt-2 text-blackTheme fw-300 text-13">
              {{ item.platform }}
            </div>
            <div class="pl-6 mt-2 mb-4 text-blackTheme fw-200 text-10">
              <v-icon x-small>mdi-clock-outline</v-icon>
              {{ $filters.formatTimeAmPm(item.startDate) }} -
              {{ $filters.formatTimeAmPm(item.endDate) }}
            </div>
          </v-col>
          <v-col md="2">
            <div class="d-flex flex-column align-center mt-5">
              <v-img
                src="/images/meeting/meeting-icon.svg"
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
    this.idLevel =  typeof this.$route.params.idLevel !== "undefined" ? this.$route.params.idLevel : "";
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
    detailMeeting(item){
      this.$refs.detailDialog.start({
        id:item.id
      })
    },
    search(){
      this.isLoading = true;
      Client.searchMeeting({
        store: this.$store,
        data:{
          username : this.$store.state.username,
          idWorkspaceLevel: this.idLevel,
          keyword : this.searchKeyword
        }
      }).then((res)=>{
        this.resultSearch = res.plainData.responseData;
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
.card-meeting {
  margin-bottom: 30px;
  margin-top: 20px;
  background: #ffffff;
  /* block drop shadow */
  box-shadow: 0px 4px 18px rgba(192, 192, 192, 0.25) !important;
  border-radius: 23px !important;
}
:deep(.highlight) {
  background: orange;
}
</style>
