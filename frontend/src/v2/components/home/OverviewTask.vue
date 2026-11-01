<template>
  <div>
    <p class="mt-5 pt-0 ml-6 text-left font-weight-bold text-h6 text-darkBlue">
      Workspace Overview
    </p>
    <p class="pt-0 ml-6 text-left text-subtitle-2 text-darkBlue">
      See your overall Workspace overview
    </p>

    <v-sheet class="d-flex flex-wrap bg-transparent ml-4">
      <v-card
        height="17vh"
        class="border-radius-dwp mt-5 mr-5 flex-fill"
        elevation="4"
      >
        <p
          class="text-left text-gradient-red font-weight-bold text-36 pt-5 pl-5"
        >
          0
        </p>
        <p class="text-left text-darkBlue font-weight-bold pl-5">In Progress</p>
        <img
          :src="require('@/v2/assets/home/overview1.png')"
          height="120"
          width="120"
          style="
            position: absolute;
            right: 0;
            bottom: 0;
            margin-right: -15px;
            margin-bottom: -25px;
          "
        />
      </v-card>
      <v-card
        height="17vh"
        class="border-radius-dwp mt-5 mr-5 flex-fill"
        elevation="4"
      >
        <p
          class="text-left text-gradient-red font-weight-bold text-36 pt-5 pl-5"
        >
          0
        </p>
        <p class="text-left text-darkBlue font-weight-bold pl-5">
          Done <span class="text-white">------</span>
        </p>

        <img
          :src="require('@/v2/assets/home/overview2.png')"
          height="120"
          width="120"
          style="
            position: absolute;
            right: 0;
            bottom: 0;
            margin-right: -15px;
            margin-bottom: -25px;
          "
        />
      </v-card>
      <v-card
        height="17vh"
        class="border-radius-dwp mt-5 mr-5 flex-fill"
        elevation="4"
      >
        <p
          class="text-left text-gradient-red font-weight-bold text-36 pt-5 pl-5"
        >
          0
        </p>
        <p class="text-left text-darkBlue font-weight-bold pl-5">Not Started</p>
        <img
          :src="require('@/v2/assets/home/overview3.png')"
          height="120"
          width="120"
          style="
            position: absolute;
            right: 0;
            bottom: 0;
            margin-right: -25px;
            margin-bottom: -25px;
          "
        />
      </v-card>
    </v-sheet>
  </div>
</template>

<style scoped>
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
