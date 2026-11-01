<template>
  <v-app>
    <div v-if="isLoading" class="preloader">
      <div class="loading">
        <div class="spinner-border" role="status">
          <span class="sr-only"></span>
        </div>
      </div>
    </div>
    <main class="main-content mt-0">
      <section class="backgroundLogin" v-if="display.width > 450">
        <img
          src="/images/login/loginMotif1.png"
          class="fade-in-anim"
          style="
            height: 77vh;
            width: 36vw;
            top: 0px;
            left: 2px;
            position: absolute;
          "
        />
        <img
          src="/images/login/loginMotif2.png"
          class="fade-in-anim-delayed"
          style="
            height: 73vh;
            width: 73vw;
            position: absolute;
            top: 0px;
            right: 0px;
          "
        />

        <div class="logoDMP" style="position: absolute; top: 3vh; left: 3vw">
          <img src="/images/login/loginBI.png" style="height: 10vh" />
        </div>
        <div class="logoDMP" style="position: absolute; top: 5vh; right: 5vw">
          <img
            class="brandFull"
            src="/images/login/loginDMP_white_new.png"
            style="height: 8vh"
          />
          <img
            class="brandLogo"
            src="/images/login/logoDMP_white.png"
            style="height: 8vh"
          />
        </div>
        <img
          src="/images/login/loginBottomLine.png"
          class="nano-banana-wave"
          style="
            width: 100vw;
            height: 50vh;
            position: absolute;
            bottom: 0px;
            right: 0px;
          "
        />
        <img
          src="/images/new-asset/gambar.webp"
          style="
            height: 80vh;
            bottom: 0px;
            left: 5vw;
            position: absolute;
            width: 45vw;
          "
        />
        <div class="mr-3">
          <div
            style="display: block; position: absolute; right: 6vw; top: 22vh"
          >
            <div class="loginText">Very good works are waiting for you</div>
            <div class="loginText">Login Now</div>
          </div>
          <div
            style="display: block; position: absolute; right: 6vw; bottom: 30vh"
          >
            <v-sheet class="w-100 bg-transparent pa-5">
              <v-sheet width="400" class="bg-transparent">
                <login-form />
              </v-sheet>
            </v-sheet>
          </div>
        </div>
        <div class="privacy">
          <router-link :to="{ name: 'privacy.policy.data' }">
            <v-icon icon="mdi-lock"></v-icon> Privacy
          </router-link>
        </div>
      </section>
      <section v-else>
        <img
          src="/images/login/loginMotif1.png"
          class="fade-in-anim"
          style="height: 57vh; width: 100%; position: fixed"
        />
        <v-sheet
          style="
            padding-top: 20vh;
            display: block;
            justify-content: center;
            align-items: center;
            text-align: center;
          "
        >
          <img src="/images/login/logoDMP.png" style="height: 10vh" />
          <p class="heading mb-1 mt-2 text-blueTheme">
            <b>Hello Again !</b>
          </p>
          <p class="subheading darken-3 text-center text-blueTheme pb-5">
            Welcome back you've been missed !
          </p>
          <v-sheet class="ml-5 mr-5 bg-transparent">
            <login-form />
          </v-sheet>
        </v-sheet>
      </section>
    </main>
  </v-app>
</template>

<script>
import { defineComponent } from "vue";
import LoginForm from "../components/LoginForm.vue";
import { useDisplay } from "vuetify";
import { isNotNullorUndefined } from "@/helpers/utils.ts";

export default defineComponent({
  name: "LoginView",
  components: {
    LoginForm,
  },
  data: function () {
    return {
      isLoading: false,
      display: useDisplay(),
    };
  },
  created() {
    if (this.$store.getters.isLoggedIn) {
      this.$router.push({ name: "home" });
    }

    if (isNotNullorUndefined(localStorage.isLogout)) {
      this.isLogout();
    }
  },
  methods: {
    isLogout() {
      this.$root.toastAlert.warning(
        "Oops, you have been logged out from another device. Please log in again!",
        {
          timeout: 10000,
        }
      );
    },
  },
});
</script>

<style scoped>
a {
  color: inherit;
  text-decoration: none;
}
.privacy {
  position: absolute;
  right: 0;
  bottom: 0;
  padding: 15px;
  color: white;
  text-decoration: none !important;
}
.backgroundLogin {
  background: linear-gradient(92.72deg, #065695 0%, #267dc2 152.21%);
  min-height: 100vh !important;
}
.loginText {
  text-align: right;
  letter-spacing: 0.1vw;
  font-size: 3vw;
  font-weight: 700 !important;
  color: #fff !important;
}
.form-position {
  margin-top: 300px;
}
.v-input__slot {
  width: 30vw;
  height: 6vh;
}

@media screen and (max-width: 580px) {
  .brandFull {
    display: none;
  }
}

@media screen and (min-width: 581px) {
  .brandLogo {
    display: none;
  }
}

@keyframes nano-banana-float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-15px);
  }
  100% {
    transform: translateY(0px);
  }
}
@keyframes nano-banana-pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}
@keyframes nano-banana-wave {
  0% {
    transform: translateY(0px) scaleX(1);
  }
  50% {
    transform: translateY(5px) scaleX(1.02);
  }
  100% {
    transform: translateY(0px) scaleX(1);
  }
}
@keyframes nano-banana-wobble {
  0% {
    transform: translateY(0px) rotate(0deg);
  }
  25% {
    transform: translateY(-10px) rotate(2deg);
  }
  50% {
    transform: translateY(0px) rotate(-1deg);
  }
  75% {
    transform: translateY(10px) rotate(2deg);
  }
  100% {
    transform: translateY(0px) rotate(0deg);
  }
}

.nano-banana-float {
  animation: nano-banana-float 6s ease-in-out infinite;
}
.nano-banana-pulse {
  animation: nano-banana-pulse 4s ease-in-out infinite;
}
.nano-banana-wave {
  animation: nano-banana-wave 7s ease-in-out infinite;
}
.nano-banana-wobble {
  animation: nano-banana-wobble 8s ease-in-out infinite;
}

@keyframes fadeInAnim {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

.fade-in-anim {
  animation: fadeInAnim 1s ease-in forwards;
}

.fade-in-anim-delayed {
  animation: fadeInAnim 1s ease-in forwards;
  animation-delay: 0.3s;
  animation-fill-mode: backwards; /* Ensures opacity 0 before animation starts */
}
</style>
