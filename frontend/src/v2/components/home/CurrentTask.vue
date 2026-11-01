<template>
  <div>
    <p class="mt-5 pt-0 ml-6 text-left font-weight-bold text-h6 text-darkBlue">
      Recently Assigned Task
    </p>
    <p class="pt-0 ml-6 text-left text-subtitle-2 text-darkBlue">
      See your newest/recently assigned task
    </p>

    <img
      :src="require('@/v2/assets/empty/no_available_state.svg')"
      class="img-no-available"
    />

    <!-- <v-card
      class="card-task mt-5 ml-5 mr-5 border-radius-dwp"
      v-for="i in 3"
      :key="i"
      elevation="4"
    >
      <v-row no-gutters class="align-center">
        <v-col cols="6">
          <v-sheet class="pa-2 ma-2 text-left font-weight-bold text-newBlack">
            Laporan Evaluasi Pelaksanaan Kebijakan Moneter, Makroprudensial, dan
            Sistem Pembayaran
          </v-sheet>
        </v-col>
        <v-col>
          <v-sheet class="pa-2 ma-2 text-orange font-weight-bold">
            In Progress
          </v-sheet>
        </v-col>
        <v-col cols="2">
          <v-sheet class="pa-2 ma-2">
            <v-btn
              class="bg-gradient-darkred text-white border-radius-dwp font-weight-bold text-cammelCase text-12"
            >
              See Details</v-btn
            >
          </v-sheet>
        </v-col>
      </v-row>
    </v-card> -->
  </div>
</template>

<style scoped>
.img-no-available {
  margin-top: 5vh;
  width: 100%;
  height: 20vh;
  margin-bottom: 5vh;
}
.card-task {
  background-color: white;
  border-radius: 25px;
  padding: 5px;
  margin-left: 17px;
  margin-right: 17px;
  transition: 0.3s;
  border-left: 5px solid #065695;
}
</style>
