<template>
  <div class="input-view">
    <div
      v-if="showWelcome"
      :class="['welcome-message', { 'fade-out': fadeOut }]"
    >
      Welcome
    </div>

    <div class="home-center">
      <div class="home-slogan">Learn the Truth Behind Your Domain</div>
      <form class="modern-search-bar" @submit.prevent="fetchDomainInfo">
        <input
          class="modern-search-input"
          v-model="domain"
          placeholder="Enter domain name or IP address..."
          autocomplete="off"
        />
        <button class="modern-search-btn" type="submit">
          <span class="search-btn-text">Discover</span>
          <svg width="22" height="22" fill="none" viewBox="0 0 24 24">
            <path
              d="M5 12h14M13 6l6 6-6 6"
              stroke="#6ec1e4"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
      </form>
    </div>
    <button class="help-btn" title="Yardım">
      <svg width="22" height="22" fill="none" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" stroke="#6ec1e4" stroke-width="2" />
        <path
          d="M12 16v-2m0-4a2 2 0 1 1 2 2c0 1-2 1-2 2"
          stroke="#6ec1e4"
          stroke-width="2"
          stroke-linecap="round"
        />
      </svg>
    </button>
  </div>
</template>

<script>
import UICard from "@/components/ui/Card.vue";
import UIButton from "@/components/ui/Button.vue";
import CustomInput from "@/components/forms/CustomInput.vue";
import FormGroup from "@/components/forms/FormGroup.vue";

export default {
  name: "HomeView",
  components: { UICard, UIButton, CustomInput, FormGroup },
  data() {
    return {
      domain: "",
      showWelcome: true,
      fadeOut: false,
    };
  },
  mounted() {
    setTimeout(() => {
      this.fadeOut = true;
    }, 2500);

    setTimeout(() => {
      this.showWelcome = false;
    }, 4500);
  },
  methods: {
    fetchDomainInfo() {
      const d = this.domain.trim();
      if (!d) return;

      const sound = document.getElementById("clickSound");
      if (sound) sound.play();


      if ("vibrate" in navigator) {
        navigator.vibrate(100);
      }
      const hist = JSON.parse(localStorage.getItem("domainHistory") || "[]");
      hist.unshift({ domain: d, date: new Date().toLocaleString() });
      localStorage.setItem("domainHistory", JSON.stringify(hist.slice(0, 50)));
      this.$router.push({ name: "Report", params: { domain: d } });
    },
  },
};
</script>

<style scoped>
.input-view {
  min-height: 100vh;
  height: 100vh;
  background: url("@/assets/radar-bg.jpg") center center/cover no-repeat,
    #0a1622;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
  margin: 0;
  padding: 0;
}
.home-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100vw;
  margin-top: 40px;
}

.home-slogan {
  color: #6ec1e4;
  font-size: 1.45rem;
  font-family: "Share Tech Mono", "Consolas", "monospace";
  letter-spacing: 0.08em;
  margin-top: -55px;
  margin-bottom: 50px;
  text-shadow: 0 0 12px #6ec1e4aa;
  font-weight: 600;
}
.modern-search-bar {
  display: flex;
  flex-direction: row;
  align-items: center;
  height: 64px;
  width: 500px;
  max-width: 95vw;
  background: rgba(10, 22, 34, 0.85);
  border-radius: 18px;
  box-shadow: 0 4px 32px #000a, 0 0 0 2px #6ec1e433 inset;
  padding: 0 0 0 0;
  border: 2.5px solid #6ec1e4;
  overflow: hidden;
  position: relative;
}
.modern-search-input {
  flex: 1;
  background: transparent;
  border: none;
  color: #e3e3fa;
  font-size: 1.25rem;
  padding: 22px 5.5px;
  outline: none;
  letter-spacing: 0.005em;
  font-family: "Share Tech Mono", "Consolas", "monospace";
  box-shadow: none;
}
.modern-search-input::placeholder {
  color: #6ec1e4cc;
  font-size: 1.15rem;
  opacity: 1;
  font-family: "Share Tech Mono", "Consolas", "monospace";
}
.modern-search-btn {
  background: rgba(10, 22, 34, 0.85);
  color: #6ec1e4;
  border: none;
  border-left: 2.5px solid #6ec1e4;
  font-size: 1.18rem;
  font-family: "Share Tech Mono", "Consolas", "monospace";
  font-weight: 700;
  padding: 0 38px;
  cursor: pointer;
  border-radius: 0 18px 18px 0;
  transition: background 0.2s, color 0.2s, border 0.2s;
  box-shadow: none;
  height: 64px;
  display: flex;
  align-items: center;
  gap: 10px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
}
.modern-search-btn:hover {
  background: #6ec1e4;
  color: #0a1622;
}
.search-btn-text {
  font-size: 1.18rem;
  font-weight: 700;
  letter-spacing: 0.12em;
}
.help-btn {
  position: fixed;
  right: 38px;
  bottom: 38px;
  background: rgba(10, 22, 34, 0.85);
  border: 2px solid #6ec1e4;
  border-radius: 50%;
  width: 54px;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 16px #000a;
  cursor: pointer;
  transition: background 0.2s, border 0.2s;
  z-index: 200;
}
.help-btn:hover {
  background: #6ec1e4;
  border-color: #6ec1e4;
}
.help-btn svg {
  display: block;
}

.welcome-message {
  position: absolute;
  top: 30%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 2.8rem;
  color: #00ffff;
  font-family: "Courier New", monospace;
  z-index: 9999;
  text-shadow: 0 0 10px #00ffffaa;
  opacity: 1;
  transition: opacity 2s ease;
}

.fade-out {
  opacity: 0;
}
</style>

<style>
body,
html {
  height: 100vh;
  margin: 0;
  padding: 0;
  background: #0a1622;
  overflow-x: hidden;
}
</style>
