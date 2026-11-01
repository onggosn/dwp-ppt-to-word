<template>
  <v-app-bar :elevation="2">
    <div class="d-flex align-center">
      <router-link :to="{ name: 'home' }">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2 ml-4 logo-header"
          contain
          src="/images/logoNavbar.png"
          transition="scale-transition"
          width="220"
        />
      </router-link>
    </div>
  </v-app-bar>
  <section id="privacy">
    <v-container class="container-content">
      <p class="text-heading text-40 mb-6 pt-header">
        Privacy and Policy Digital Workplace Mobile
      </p>
      <p class="text-content text-16">
        This Privacy Policy describes how Central Bank of Indonesia collects,
        uses, and shares<br />
        information when you use our mobile application Digital Workplace
        Mobile. By downloading,<br />
        installing, and using the App, you agree to the terms of this Privacy
        Policy.
      </p>
      <br />
      <p class="text-heading text-30 mb-2">Information We Collect</p>
      <p class="text-content text-16">
        We do not collect any personal information from users of the App.
      </p>
      <br />
      <p class="text-heading text-30 mb-2">How We Use Information</p>
      <p class="text-content text-16">
        Since we do not collect any personal information, we do not use any
        information for <br />any purpose.
      </p>
      <br />
      <p class="text-heading text-30 mb-2">Information Sharing</p>
      <p class="text-content text-16">
        We do not share any information with third parties as we do not collect
        any information from <br />users.
      </p>
      <br />
      <p class="text-heading text-30 mb-2">Security</p>
      <p class="text-content text-16">
        We take reasonable measures to protect the information we do not collect
        from unauthorized <br />access or disclosure.
      </p>
      <br />
      <p class="text-heading text-30 mb-2">Changes to this Privacy Policy</p>
      <p class="text-content text-16">
        We reserve the right to update or change our Privacy Policy at any time.
        Any changes will be <br />effective immediately upon posting the updated
        Privacy Policy in the App.
      </p>
      <br />
      <p class="text-heading text-30 mb-2">Contact Us</p>
      <p class="text-content text-16">
        If you have any questions or concerns about this Privacy Policy, please
        contact us at<br />
        bicara@bi.go.id
      </p>
      <div class="d-flex flex-row-reverse pt-5">
        <v-btn
          class="text-redTheme-gradien text-15 fw-500"
          @click="$router.go(-1)"
          style="
            border-radius: 10px;
            box-shadow: 0px 3px 7px 0px rgba(133, 133, 133, 0.25);
          "
          >Back</v-btn
        >
      </div>
      <br />
    </v-container>
  </section>
</template>

<script>
export default {
  methods: {},
};
</script>

<style scoped>
@import "@/assets/styles/main.css";

.pt-header {
  padding-top: 80px;
}
.container-content {
  box-shadow: 0px -7px 18px 0px rgba(179, 179, 179, 0.25);
  padding-right: 160px;
  padding-left: 160px;
}
.v-app-bar.v-toolbar {
  box-shadow: 0px -7px 18px 0px rgba(179, 179, 179, 0.25) !important;
}

.text-heading {
  font-weight: 600;
  line-height: 52px;
  letter-spacing: 0em;
  color: rgba(75, 75, 75, 1);
}
.text-content {
  font-weight: 400;
  line-height: 27px;
  letter-spacing: 0em;
  text-align: left;
  color: rgba(75, 75, 75, 1);
  font-family: Poppins;
}
@media only screen and (max-width: 600px) {
  .logo-header {
    width: 150px !important;
  }

  .container-content {
    padding: 30px;
  }
  .pt-header {
    padding-top: 10px;
  }

  body {
    font-size: 12px;
  }
}
</style>
