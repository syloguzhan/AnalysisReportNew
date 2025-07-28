<template>
  <div class="report-view">
    <div v-if="error" class="error-message">
      {{ error }}
      <button class="back-btn" @click="goHome">Geri Dön</button>
    </div>
    <div v-else-if="loaded" class="report-container">
      <ReportResult
        :domain="domain"
        :summary="summary"
        :competitors="competitors"
        :company="company"
        :socialMedia="socialMedia"
        :aiAnalysis="aiAnalysis"
      />
    </div>
    <div v-else class="loading">AI analiz hazırlanıyor…</div>
  </div>
</template>

<script>
import ReportResult from "@/components/ui/ReportResult.vue";
import axios from "axios";

export default {
  name: "ReportView",
  components: { ReportResult },

  props: {
    domain: { type: String, default: "" },
  },

  data() {
    return {
      summary: "",
      competitors: [],
      company: null,
      socialMedia: [],
      aiAnalysis: [],
      loaded: false,
      error: null,
    };
  },

  async created() {
    console.log("Gelen domain:", this.domain);
    await this.fetchReportData();
  },

  methods: {
    async fetchReportData() {
      this.loaded = false;
      this.error = null;
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/generate-reports",
          {
            domain: this.domain,
          }
        );
        const data = response.data;
        this.summary = data.report || "";
        this.loaded = true;
      } catch (err) {
        this.error = "Veri alınırken hata oluştu.";
        this.loaded = false;
      }
    },
    goHome() {
      this.$router.push({ name: "input" });
    },
  },
};
</script>

<style scoped>
.report-view {
  min-height: 100vh;
  background: url("@/assets/radar-bg.jpg") center center/cover no-repeat,
    #0a1622;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 60px 20px 40px;
  overflow-x: hidden;
}

.report-container {
  background-color: rgba(10, 22, 34, 0.85);
  padding: 30px;
  border-radius: 16px;
  max-width: 1000px;
  width: 100%;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.6);
  color: #f1f1f1;
  font-family: "Segoe UI", sans-serif;
}

.loading {
  padding: 2rem;
  font-size: 1.2rem;
  color: #f0f0f0;
}

.error-message {
  font-size: 1.5rem;
  color: #ff4d4f;
  margin-top: 250px;
  text-align: center;
  font-weight: bold;
}

.back-btn {
  margin-top: 32px;
  padding: 12px 32px;
  font-size: 1.1rem;
  background: #6ec1e4;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s;
}
.back-btn:hover {
  background: #ff4d4f;
}
</style>
