<template>
  <v-container fluid class="pa-8">
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-2 font-weight-bold text-darkBlue">
          DWP UI Documentation
        </h1>
        <p class="text-subtitle-1 text-grey-darken1 mb-8">
          Panduan penggunaan class CSS global dan komponen UI di aplikasi.
        </p>

        <!-- Main Components Section -->
        <div id="core-components" class="item-card mb-6">
          <h2 class="text-h5 mb-4 text-gradient-blue">Core Components</h2>

          <!-- Banner Example -->
          <p class="text-caption text-grey mb-2">
            .home-banner (Banner Administrator)
          </p>
          <div class="home-banner-doc mb-6">
            <p class="pt-5 text-banner-doc">Banner Header Example</p>
            <p class="pt-1 text-sub-banner-doc">
              Subtitle banner description goes here.
            </p>
          </div>

          <!-- Custom Card Example -->
          <p class="text-caption text-grey mb-2">
            .item-card (Custom DWP Card Shadow)
          </p>
          <div
            class="pa-6 border border-radius-dwp mb-4 text-center"
            style="border: 1px dashed #ccc !important"
          >
            Contoh Inside Card
          </div>
        </div>

        <!-- Typography Section -->
        <div id="typography" class="item-card mb-6">
          <h2 class="text-h5 mb-4 text-gradient-blue">Typography & Sizes</h2>
          <v-row align="center" class="mb-4">
            <v-col cols="3"
              ><span class="text-caption text-grey">.text-36</span></v-col
            >
            <v-col cols="9"><div class="text-36">Contoh Text 36px</div></v-col>
          </v-row>
          <v-row align="center" class="mb-4">
            <v-col cols="3"
              ><span class="text-caption text-grey">.text-28</span></v-col
            >
            <v-col cols="9"><div class="text-28">Contoh Text 28px</div></v-col>
          </v-row>
          <v-row align="center" class="mb-4">
            <v-col cols="3"
              ><span class="text-caption text-grey">.text-24</span></v-col
            >
            <v-col cols="9"><div class="text-24">Contoh Text 24px</div></v-col>
          </v-row>
          <v-row align="center" class="mb-4">
            <v-col cols="3"
              ><span class="text-caption text-grey">.text-20</span></v-col
            >
            <v-col cols="9"><div class="text-20">Contoh Text 20px</div></v-col>
          </v-row>
          <v-row align="center">
            <v-col cols="3"
              ><span class="text-caption text-grey">.text-12</span></v-col
            >
            <v-col cols="9"><div class="text-12">Contoh Text 12px</div></v-col>
          </v-row>
        </div>

        <!-- Gradients Section -->
        <div id="gradients" class="item-card mb-6">
          <h2 class="text-h5 mb-4 text-gradient-blue">Gradients & Colors</h2>
          <v-row>
            <v-col cols="12" md="6">
              <div class="mb-4">
                <p class="text-caption text-grey mb-1">Background Gradients</p>
                <div class="d-flex flex-wrap gap-4">
                  <div
                    class="pa-4 bg-gradient-darkblue border-radius-dwp text-white"
                  >
                    .bg-gradient-darkblue
                  </div>
                  <div
                    class="pa-4 bg-gradient-darkred border-radius-dwp text-white"
                  >
                    .bg-gradient-darkred
                  </div>
                  <div
                    class="pa-4 primary-gradient border-radius-dwp text-white"
                  >
                    .primary-gradient
                  </div>
                </div>
              </div>
            </v-col>
            <v-col cols="12" md="6">
              <div class="mb-4">
                <p class="text-caption text-grey mb-1">Text Gradients</p>
                <div class="text-h6 text-gradient-blue">
                  .text-gradient-blue
                </div>
                <div class="text-h6 text-gradient-red">.text-gradient-red</div>
                <div class="text-h6 text-gradient-grey">
                  .text-gradient-grey
                </div>
                <div class="text-h6 text-gradient">
                  .text-gradient (Red Blue)
                </div>
              </div>
            </v-col>
          </v-row>
        </div>

        <!-- Buttons Section -->
        <div id="buttons" class="item-card mb-6">
          <h2 class="text-h5 mb-4 text-gradient-blue">Buttons Style</h2>
          <div class="d-flex flex-wrap gap-4 align-center mb-6">
            <div>
              <p class="text-caption text-grey mb-1">Theme Buttons</p>
              <v-btn class="button-blueTheme mr-2">.button-blueTheme</v-btn>
              <v-btn class="button-red">.button-red</v-btn>
            </div>
            <div>
              <p class="text-caption text-grey mb-1">Action Buttons</p>
              <v-btn class="btn-action btn-action-create mr-2"
                >.btn-action-create</v-btn
              >
              <v-btn class="btn-action btn-action-close"
                >.btn-action-close</v-btn
              >
            </div>
          </div>
          <div class="d-flex flex-wrap gap-4 align-center">
            <div>
              <p class="text-caption text-grey mb-1">Status Buttons</p>
              <v-btn class="btn-active mr-2">.btn-active</v-btn>
              <v-btn class="btn-danger mr-2">.btn-danger</v-btn>
              <v-btn class="btn-disable mr-2">.btn-disable</v-btn>
              <v-btn class="btn-cancel">.btn-cancel</v-btn>
            </div>
          </div>
        </div>

        <!-- Sections & Separators -->
        <div id="sections" class="item-card mb-6">
          <h2 class="text-h5 mb-4 text-gradient-blue">Sections & Separators</h2>
          <v-row>
            <v-col cols="12" md="6">
              <p class="text-caption text-grey mb-2">
                Section Headers (with gradient)
              </p>
              <div class="documentSection sectionBlue mb-2">.sectionBlue</div>
              <div class="documentSection sectionRed">.sectionRed</div>
            </v-col>
            <v-col cols="12" md="6">
              <p class="text-caption text-grey mb-4">Separators</p>
              <div class="mb-6">
                <span class="text-caption">.separator-gradient</span>
                <div class="separator-gradient"></div>
              </div>
              <div>
                <span class="text-caption"
                  >.separatorHorizontalGradient (Opacity 0.5)</span
                >
                <div class="separatorHorizontalGradient"></div>
              </div>
            </v-col>
          </v-row>
        </div>

        <!-- Common Form Components -->
        <div id="form-elements" class="item-card mb-6">
          <h2 class="text-h5 mb-4 text-gradient-blue">Common Form Elements</h2>
          <v-row>
            <v-col cols="12" md="6">
              <p class="text-caption text-grey mb-2">
                Standard Search Button (.btn-dropdown)
              </p>
              <v-btn class="btn-dropdown" variant="outlined">
                <v-icon icon="mdi-magnify" color="#065695" class="mr-2" />
                Search
              </v-btn>
            </v-col>
            <v-col cols="12" md="6">
              <p class="text-caption text-grey mb-2">
                Standard Filter Button (.btn-dropdown)
              </p>
              <v-btn class="btn-dropdown" variant="outlined">
                <v-icon icon="mdi-tune" color="#065695" class="mr-2" />
                Filter
              </v-btn>
            </v-col>
            <v-col cols="12" md="6" class="mt-4">
              <p class="text-caption text-grey mb-2">
                Custom Chips (.selected-chip)
              </p>
              <div class="d-flex flex-wrap">
                <v-chip class="selected-chip mr-2">
                  <span class="chip-text">Contoh Label</span>
                  <v-icon size="small" class="ml-2 chip-close-icon"
                    >mdi-close</v-icon
                  >
                </v-chip>
                <v-chip class="selected-chip">
                  <span class="chip-text">Active Filter</span>
                  <v-icon size="small" class="ml-2 chip-close-icon"
                    >mdi-close</v-icon
                  >
                </v-chip>
              </div>
            </v-col>
          </v-row>
        </div>

        <!-- Utilities Section -->
        <div id="utilities" class="item-card mb-6">
          <h2 class="text-h5 mb-4 text-gradient-blue">Utilities</h2>
          <v-table>
            <thead>
              <tr>
                <th class="text-left">Class Name</th>
                <th class="text-left">Preview / Usage</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>.btn-dropdown</code></td>
                <td>Gaya tombol outline biru dengan font semi-bold (600)</td>
              </tr>
              <tr>
                <td><code>.selected-chip</code></td>
                <td>
                  Gaya chip filter dengan border biru muda dan teks biru gelap
                </td>
              </tr>
              <tr>
                <td><code>.text-newBlack</code></td>
                <td>
                  <span class="text-newBlack"
                    >Warna hitam kustom (#4b4b4b)</span
                  >
                </td>
              </tr>
              <tr>
                <td><code>.text-darkBlue</code></td>
                <td>
                  <span class="text-darkBlue"
                    >Warna biru gelap kustom (#3a416f)</span
                  >
                </td>
              </tr>
              <tr>
                <td><code>.text-orange</code></td>
                <td>
                  <span class="text-orange">Warna orange kustom (#ff9900)</span>
                </td>
              </tr>
              <tr>
                <td><code>.border-radius-dwp</code></td>
                <td>
                  <div
                    class="pa-2 border border-radius-dwp text-center"
                    style="border: 1px solid #ccc !important"
                  >
                    Border Radius 12px
                  </div>
                </td>
              </tr>
              <tr>
                <td><code>.text-cammelCase</code></td>
                <td>
                  <span class="text-cammelCase">CONTOH TEKS CAPITALIZE</span>
                </td>
              </tr>
            </tbody>
          </v-table>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
// UI Documentation
</script>

<style scoped>
.gap-4 {
  gap: 16px;
}

.item-card {
  padding: 23px 30px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 16px;
  box-shadow: 0px 3px 10px 0px rgba(0, 0, 0, 0.12);
}

.home-banner-doc {
  max-width: 100%;
  background-image: linear-gradient(180deg, #065695 0%, #267dc2 100%);
  /* Menggunakan gradient sebagai fallback jika asset tidak ada di doc view */
  height: 125px;
  border-radius: 20px;
  border: 1px solid #f5f5f5;
  color: white;
}

.text-banner-doc {
  text-align: left;
  padding-left: 30px;
  font-size: 24px;
  color: white;
  font-weight: bold;
}
.text-sub-banner-doc {
  text-align: left;
  padding-left: 30px;
  font-size: 14px;
  color: white;
}

.btn-dropdown {
  color: #065695 !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  border-radius: 8px !important;
  text-transform: none !important;
}

.selected-chip {
  margin-right: 8px;
  margin-bottom: 8px;
  color: #6eb3ea !important;
  border: 1px solid #007bff !important;
  border-radius: 6px !important;
  background: white !important;
}

.chip-text {
  color: #065391;
  font-size: 12px;
  font-weight: 600;
}

.chip-close-icon {
  color: #065391 !important;
}
</style>
