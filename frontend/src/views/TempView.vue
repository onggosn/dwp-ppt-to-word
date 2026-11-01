<template>
  <v-container>
    <v-row align="center" justify="center" style="display: none">
      <v-col cols="auto">
        <v-radio-group v-model="color" inline>
          <v-radio label="indigo" color="indigo" value="indigo"></v-radio>
          <v-radio
            label="indigo-darken-3"
            color="indigo-darken-3"
            value="indigo-darken-3"
          ></v-radio>
          <v-radio label="primary" color="primary" value="primary"></v-radio>
          <v-radio
            label="secondary"
            color="secondary"
            value="secondary"
          ></v-radio>
        </v-radio-group>
      </v-col>
    </v-row>
    <v-row align="center" justify="center" class="mt-15">
      <v-col v-for="(variant, i) in variants" :key="i" cols="auto">
        <v-card
          class="mx-auto"
          max-width="344"
          :color="color"
          :variant="variant"
        >
          <v-card-item>
            <div>
              <div class="text-overline mb-1"></div>
              <div class="text-h6 mb-1">Under Development</div>
              <div class="text-caption">this page is under development</div>
            </div>
          </v-card-item>

          <v-card-actions>
            <!-- <v-btn> Button </v-btn> -->
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script setup>
import { ref } from "vue";

const variants = ["elevated", "flat", "tonal", "outlined"];
const color = ref("indigo");
</script>
