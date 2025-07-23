<template>
  <div class="history-view">
    <div class="history-header">
      <input
        class="history-search"
        v-model="search"
        placeholder="Geçmişte ara..."
      />
      <button class="clear-btn" @click="clearAll" v-if="history.length">
        Tümünü Temizle
      </button>
    </div>
    <div v-if="filteredHistory.length" class="history-list">
      <div
        v-for="(item, idx) in filteredHistory"
        :key="idx"
        class="history-card"
      >
        <div class="history-card-main">
          <div class="history-domain">{{ item.domain }}</div>
          <div class="history-date">{{ item.date }}</div>
        </div>
        <div class="history-card-actions">
          <span class="status-tag" :class="statusClass(item.status)">{{
            item.status || "Başarılı"
          }}</span>
          <button class="reanalyze-btn" @click="reanalyze(item.domain)">
            Tekrar Analiz Et
          </button>
          <button class="delete-btn" @click="deleteItem(idx)">Sil</button>
        </div>
      </div>
    </div>
    <div v-else class="empty-history">
      <div class="empty-icon">
        <svg width="64" height="64" fill="none" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10" stroke="#6ec1e4" stroke-width="2" />
          <path
            d="M8 12h8M8 16h8M8 8h8"
            stroke="#6ec1e4"
            stroke-width="2"
            stroke-linecap="round"
          />
        </svg>
      </div>
      <div class="empty-text">Henüz geçmiş yok</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HistoryView",
  data() {
    return {
      history: [],
      search: "",
    };
  },
  computed: {
    filteredHistory() {
      if (!this.search.trim()) return this.history;
      return this.history.filter((item) =>
        item.domain.toLowerCase().includes(this.search.trim().toLowerCase())
      );
    },
  },
  mounted() {
    this.loadHistory();
  },
  methods: {
    loadHistory() {
      const data = localStorage.getItem("domainHistory");
      this.history = data ? JSON.parse(data) : [];
    },
    deleteItem(idx) {
      this.history.splice(idx, 1);
      localStorage.setItem("domainHistory", JSON.stringify(this.history));
    },
    reanalyze(domain) {
      this.$router.push({ name: "Report", params: { domain } });
    },
    clearAll() {
      this.history = [];
      localStorage.removeItem("domainHistory");
    },
    statusClass(status) {
      if (!status || status === "Başarılı") return "status-success";
      if (status === "Hata") return "status-error";
      return "status-other";
    },
  },
};
</script>

<style scoped>
.history-view {
  min-height: 100vh;
  background: url("@/assets/radar-bg.jpg") center center/cover no-repeat,
    #0a1622;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 80px;
  overflow: hidden;
}
.history-header {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 500px;
  max-width: 95vw;
  margin-bottom: 32px;
  gap: 18px;
}
.history-search {
  flex: 1;
  background: rgba(10, 22, 34, 0.85);
  border: 2px solid #6ec1e4;
  border-radius: 10px;
  color: #e3e3fa;
  font-size: 1.1rem;
  padding: 12px 18px;
  font-family: "Share Tech Mono", "Consolas", "monospace";
  outline: none;
  box-shadow: 0 2px 12px #0006;
}
.clear-btn {
  background: #e74c3c;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 18px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  font-family: "Share Tech Mono", "Consolas", "monospace";
}
.clear-btn:hover {
  background: #c0392b;
}
.history-list {
  width: 500px;
  max-width: 95vw;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.history-card {
  background: rgba(10, 22, 34, 0.85);
  border: 2px solid #6ec1e4;
  border-radius: 14px;
  box-shadow: 0 2px 16px #000a;
  padding: 18px 22px 14px 22px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.history-card-main {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}
.history-domain {
  color: #6ec1e4;
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  font-family: "Share Tech Mono", "Consolas", "monospace";
}
.history-date {
  color: #e3e3fa;
  font-size: 1rem;
  opacity: 0.7;
  font-family: "Share Tech Mono", "Consolas", "monospace";
}
.history-card-actions {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
}
.status-tag {
  padding: 4px 14px;
  border-radius: 8px;
  font-size: 0.98rem;
  font-weight: 600;
  font-family: "Share Tech Mono", "Consolas", "monospace";
  letter-spacing: 0.06em;
  background: #1a2a2a;
  color: #6ec1e4;
  border: 1.5px solid #6ec1e4;
}
.status-success {
  background: #1a2a2a;
  color: #6ec1e4;
  border-color: #6ec1e4;
}
.status-error {
  background: #2a1a1a;
  color: #ff3c3c;
  border-color: #ff3c3c;
}
.status-other {
  background: #222a3a;
  color: #f7c873;
  border-color: #f7c873;
}
.reanalyze-btn {
  background: #6ec1e4;
  color: #0a1622;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  font-family: "Share Tech Mono", "Consolas", "monospace";
  transition: background 0.2s, color 0.2s;
}
.reanalyze-btn:hover {
  background: #ff3c3c;
  color: #fff;
}
.delete-btn {
  background: #e74c3c;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  font-family: "Share Tech Mono", "Consolas", "monospace";
  transition: background 0.2s;
}
.delete-btn:hover {
  background: #c0392b;
}
.empty-history {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
  width: 100vw;
  color: #6ec1e4;
  opacity: 0.7;
  font-size: 1.2rem;
  font-family: "Share Tech Mono", "Consolas", "monospace";
}
.empty-icon {
  margin-bottom: 18px;
  filter: drop-shadow(0 0 18px #6ec1e4aa);
}
.empty-text {
  font-size: 1.18rem;
  letter-spacing: 0.08em;
}
</style>
