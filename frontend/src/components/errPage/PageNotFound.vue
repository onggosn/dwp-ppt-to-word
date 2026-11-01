<template>
  <v-app>
    <!-- <custom-stepper :itemNumber="10" :currentStep="8" /> -->
    <v-container>
      <v-row style="height: 90vh">
        <v-col align-self="center">
          <v-sheet class="bg-white text-center">
            <button>404 - Page Not Found</button>
            <p class="mt-5 text-12">
              The page you are looking for does not exist or has been moved.
              <br />
              Please check the URL for any typos, or go to our homepage to find
              the information you need.
            </p>
          </v-sheet>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<!-- <script setup lang="ts">
import CustomStepper from "@/components/stepper/CustomStepper.vue";
import { defineComponent } from "vue";

defineComponent({
  components: {
    CustomStepper,
  },
});
</script> -->

<style scoped>
button {
  --c: #fff;
  /* text color */
  background: linear-gradient(90deg, #0000 33%, #fff5, #0000 67%)
      var(--_p, 100%) / 300% no-repeat,
    linear-gradient(91deg, #d6212a 15.38%, #ff000d 81.89%);
  /* background color */
  color: #0000;
  border: none;
  transform: perspective(500px) rotateY(calc(20deg * var(--_i, -1)));
  text-shadow: calc(var(--_i, -1) * 0.08em) -0.01em 0 var(--c),
    calc(var(--_i, -1) * -0.08em) 0.01em 2px #0004;
  outline-offset: 0.1em;
  transition: 0.3s;
}

button:hover,
button:focus-visible {
  --_p: 0%;
  --_i: 1;
}

button:active {
  text-shadow: none;
  color: var(--c);
  box-shadow: inset 0 0 9e9Q #0005;
  transition: 0s;
}

button {
  font-family: system-ui, sans-serif;
  font-weight: bold;
  font-size: 2rem;
  margin: 0;
  cursor: pointer;
  padding: 0.1em 0.3em;
}
</style>
