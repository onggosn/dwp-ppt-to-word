<template>
  <api-loader :apiMethod="getProfile" @loadingEnded="handleLoadingEnded">
    <template v-slot:default v-if="user">
      <div class="fontpoppins" style="padding: 50px">
        <v-sheet
          class="rounded-xl overflow-hidden d-none d-md-flex"
          elevation="2"
        >
          <v-img src="/images/bg-profile.png" />
        </v-sheet>
        <v-card
          class="mt-lg-n16 mt-sm-6 mx-auto d-flex flex-row pa-4 align-center rounded-lg shadow-blur blur"
          elevation="2"
          max-width="90%"
        >
          <v-list-item>
            <p
              class="text-h6 font-weight-bold text-blue-theme"
              style="font-size: 24px !important"
            >
              {{ user.name }}
            </p>
            <p class="font-weight-thin text-blue-theme" style="font-size: 14px">
              {{ user.gradeName }}
            </p>
            <template v-slot:prepend>
              <v-avatar>
                <v-icon size="45" color="dimgrey">mdi-account</v-icon>
              </v-avatar>
            </template>
          </v-list-item>
        </v-card>

        <v-card
          class="mt-8 rounded-xl pa-8 text-blueTheme"
          elevation="2"
          max-width="100%"
        >
          <v-row>
            <v-col class="font-weight-bold text-blue-theme" cols="12" md="3"
              >Informasi Pribadi</v-col
            >
            <v-col cols="12" md="9">
              <div class="font-weight-bold text-blue-theme">Jabatan</div>
              <div class="text-blue-theme">
                {{ user.jabatanName }}
              </div>
              <div class="mt-4 font-weight-bold text-blue-theme">NIP</div>
              <div class="text-blue-theme">
                {{ user.nip }}
              </div>
              <div class="mt-4 font-weight-bold text-blue-theme">
                Organisasi
              </div>
              <div class="text-blue-theme">
                {{ user.organizationName }}
              </div>
            </v-col>
          </v-row>

          <v-row>
            <v-col class="font-weight-bold text-blue-theme" cols="12" md="3"
              >Kontak</v-col
            >
            <v-col cols="12" md="9">
              <div class="font-weight-bold text-blue-theme">Email</div>
              <div class="text-blue-theme">
                {{ user.email }}
              </div>
            </v-col>
          </v-row>
          <v-row>
            <v-col
              class="font-weight-bold text-blue-theme"
              cols="12"
              md="3"
            ></v-col>
            <v-col cols="12" md="9">
              <div class="font-weight-bold text-blue-theme">Visual Sign</div>
              <div
                class="d-flex justify-start mb-6 bg-surface"
                v-if="$vuetify.display.lgAndUp"
              >
                <v-sheet style="margin-left: -0.6vw">
                  <v-checkbox
                    style="pointer-events: none"
                    v-model="ex4"
                    color="success"
                    value="success"
                    hide-details
                    class="pr-3 mt-1 align-self-center"
                  >
                    <template v-slot:label>
                      <span style="font-size: 16px; color: #3a416f"
                        >Available</span
                      >
                    </template></v-checkbox
                  >
                </v-sheet>
                <v-btn
                  class="ma-2 rounded-lg"
                  variant="outlined"
                  color="indigo"
                  style="letter-spacing: -0.2px; align-self: center"
                  @click="dialog = true"
                >
                  <v-icon left class="pr-4"> mdi-eye </v-icon>
                  Preview Visual Sign
                </v-btn>
                <v-sheet style="letter-spacing: -0.2px; align-self: center">
                  <edit-visual-sign ref="visualSignDialog" />
                </v-sheet>
              </div>
              <div v-else>
                <v-row no-gutters>
                  <v-col cols="12">
                    <v-sheet style="margin-left: -0.6vw">
                      <v-checkbox
                        style="pointer-events: none"
                        v-model="ex4"
                        color="success"
                        value="success"
                        hide-details
                        class="pr-3 mt-1 align-self-center"
                      >
                        <template v-slot:label>
                          <span style="font-size: 16px; color: #3a416f"
                            >Available</span
                          >
                        </template></v-checkbox
                      >
                    </v-sheet>
                  </v-col>
                  <v-col cols="12">
                    <v-btn
                      class="ma-2 rounded-lg"
                      variant="outlined"
                      color="indigo"
                      style="letter-spacing: -0.2px; align-self: center"
                      @click="dialog = true"
                    >
                      <v-icon left class="pr-4"> mdi-eye </v-icon>
                      Preview Visual Sign
                    </v-btn>
                  </v-col>
                  <v-col cols="12">
                    <v-sheet style="letter-spacing: -0.2px; align-self: left">
                      <edit-visual-sign
                        class="mt-2"
                        ref="visualSignDialog"
                        style="justify-content: left !important"
                      />
                    </v-sheet>
                  </v-col>
                </v-row>
              </div>
              <v-sheet class="d-flex mb-6 justify-start" flat tile>
                <div class="text-center">
                  <v-dialog v-model="dialog" max-width="700">
                    <v-card class="rounded-lg">
                      <v-sheet>
                        <div>
                          <div
                            class="pt-5 pb-5 text-center text-18 text-blueTheme"
                          >
                            Preview Visual Sign
                          </div>
                          <div
                            class="pt-5 text-center text-18"
                            style="position: absolute; right: 0px; top: -10px"
                          >
                            <v-btn
                              class="mx-2"
                              fab
                              small
                              variant="text"
                              @click="dialog = false"
                            >
                              <v-icon color="#C0C0C0"> mdi-close </v-icon>
                            </v-btn>
                          </div>
                        </div>
                        <v-btn
                          elevation="0"
                          class="d-block separatorHorizontal"
                          style="cursor: none"
                        />
                      </v-sheet>
                      <v-sheet class="pa-7">
                        <v-card
                          elevation="0"
                          style="
                            border-radius: 10px;
                            padding-top: 80px;
                            padding-bottom: 80px;
                            border: 1px dashed #065695;
                            text-align: -webkit-center;
                          "
                        >
                          <api-loader :apiMethod="getVisualSignByUsername">
                            <template v-slot:default="props">
                              <img
                                style="border-radius: 5px"
                                width="200"
                                height="100"
                                :src="
                                  'data:image/png;base64,' +
                                  props.response.plainData.responseData
                                    .visualImage
                                "
                              />
                            </template>
                            <template v-slot:loading>
                              <free-style-shimmer
                                height="15vh"
                                width="15vw"
                                border-radius="5px"
                                color="#DCDCDC"
                                class="ml-0 mt-0 mb-4"
                              />
                            </template>
                          </api-loader>
                        </v-card>
                      </v-sheet>
                    </v-card>
                  </v-dialog>
                </div>
              </v-sheet>
            </v-col>
          </v-row>
        </v-card>
      </div>
    </template>
    <template v-slot:loading>
      <custom-shimmer-profile />
    </template>
  </api-loader>
</template>

<script lang="js">
import { defineComponent } from "vue";
import client from "@/library/ApiClient";
import ApiLoader from "@/components/ApiLoader.vue";
import EditVisualSign from "@/components/profile/EditVisualSignDialog.vue";
import CustomShimmerProfile from "@/components/profile/CustomShimmerProfile.vue";

export default defineComponent({
  name: "LoginView",
  components: {
    ApiLoader,EditVisualSign,
    CustomShimmerProfile
  },
  data: function () {
    return {
      user: null,
      ex4: ["success"],
      signImage: null,
      loader: 0,
      dialog: false,
    };
  },
  methods: {
      getVisualSignByUsername() {
        return client.GetVisualSignByUsername({
        store: this.$store,
        data: {
          username: this.$store.state.username,
        },
      });
    },
    firstCharIsLetter(char) {
      if (typeof char !== "string") {
        return false;
      }

      return /^[a-z]+$/i.test(char);
    },
    getAbbreviation(name) {
      const segments = name.split(" ");
      let result = "";

      if (segments.length === 1) {
        result = segments[0][0];
      } else {
        let lastAbbreviation = "";

        for (let i = segments.length - 1; i > 0; i--) {
          if (this.firstCharIsLetter(segments[i])) {
            lastAbbreviation = segments[i][0];
            break;
          }
        }

        result = segments[0][0] + lastAbbreviation;
      }

      return result.toUpperCase();
    },
    getProfile() {
      return client.GetUserByUsername({
        store: this.$store,
        data: {
          username: this.$store.state.username,
        },
      });
    },
    handleLoadingEnded({ success, response }) {
      if (success) {
        this.user = response.plainData[0];
      }
    },
  },
});
</script>

<style scoped>
:deep(.v-img__img.v-img__img--contain) {
  width: 100%;
}
:deep(.v-img__img) {
  width: 100%;
}
.text-blue-theme {
  color: #3a416f;
}

.v-list-item__content .v-list-item-title :deep() {
  color: red;
}
.separatorHorizontal {
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
  height: 1.2px;
  width: 100%;
}
</style>
