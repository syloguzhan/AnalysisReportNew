<template>
  <div class="report-result">
    <div class="result-card" ref="pdfContent">
      <div class="pdf-btn-row">
        <button v-if="!pdfLoading" class="pdf-btn" @click="downloadPDF">
          <span>PDF Oluştur</span>
        </button>
        <div v-else class="pdf-loading-text">Yükleniyor...</div>
      </div>
      <h2>
        <span class="icon">📄</span> Analiz Sonuçları:
        <span class="domain">{{ domain }}</span>
      </h2>

      <!-- Şirket Bilgileri Bölümü -->
      <section class="company-info" v-if="company">
        <h3><span class="icon">🏢</span> Şirket Bilgileri</h3>
        <div class="info-box">
          <p><strong>Adı:</strong> {{ company.name }}</p>
          <p v-if="company.sector">
            <strong>Sektör:</strong> {{ company.sector }}
          </p>
          <p v-if="company.size">
            <strong>Çalışan:</strong> {{ company.size }}
          </p>
          <p v-if="company.founded">
            <strong>Kuruluş:</strong> {{ company.founded }}
          </p>
          <p v-if="company.description">
            <strong>Açıklama:</strong> {{ company.description }}
          </p>
        </div>
      </section>

      <!-- Sosyal Medya Varlıkları Bölümü -->
      <section class="social-media" v-if="socialMedia && socialMedia.length">
        <h3><span class="icon">🌐</span> Sosyal Medya Varlıkları</h3>
        <ul class="social-list">
          <li v-for="s in socialMedia" :key="s.platform">
            <strong>{{ s.platform }}:</strong>
            <a :href="s.url" target="_blank">{{ s.url }}</a>
            <span v-if="s.followers">- Takipçi: {{ s.followers }}</span>
          </li>
        </ul>
      </section>

      <!-- Yapay Zeka Analiz Tablosu -->
      <section class="ai-analysis-table" v-if="aiAnalysis && aiAnalysis.length">
        <h3><span class="icon">🤖</span> Yapay Zeka Analizleri</h3>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Kriter</th>
                <th>Değer</th>
                <th>Yorum</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in aiAnalysis" :key="row.criterion">
                <td>{{ row.criterion }}</td>
                <td>{{ row.value }}</td>
                <td>{{ row.comment }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- AI Özet Kutusu -->
      <section class="ai-summary">
        <h3><span class="icon">🧠</span> Özet Rapor</h3>
        <div class="summary-box">
          <p>{{ summary }}</p>
        </div>
      </section>

      <!-- Rakip Karşılaştırma Tablosu -->
      <section class="comparison-table" v-if="competitors.length">
        <h3><span class="icon">📊</span> Rakip Karşılaştırması</h3>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Firma</th>
                <th>İçerik</th>
                <th>AI Skoru</th>
                <th>Konular</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="c in competitors" :key="c.name">
                <td>{{ c.name }}</td>
                <td>{{ c.contentCount }}</td>
                <td>
                  <span class="score">{{ c.score }}</span>
                </td>
                <td>
                  <span v-for="t in c.topics" :key="t" class="topic-chip">{{
                    t
                  }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

export default {
  name: "ReportResult",
  props: {
    domain: { type: String, required: true },
    summary: { type: String, required: true },
    competitors: { type: Array, default: () => [] },
    company: { type: Object, default: null },
    socialMedia: { type: Array, default: () => [] },
    aiAnalysis: { type: Array, default: () => [] },
  },
  data() {
    return {
      pdfLoading: false,
    };
  },
  methods: {
    async downloadPDF() {
      this.pdfLoading = true;
      document.body.style.cursor = "wait";
      try {
        const el = this.$refs.pdfContent;
        // PDF için özel stil uygula
        el.classList.add("pdf-export");
        await this.$nextTick();
        const canvas = await html2canvas(el, { scale: 2 });
        const imgData = canvas.toDataURL("image/png");
        const pdf = new jsPDF({ orientation: "p", unit: "pt", format: "a4" });
        const pageWidth = pdf.internal.pageSize.getWidth();
        const pageHeight = pdf.internal.pageSize.getHeight();
        // Görüntüyü sayfaya sığdır
        const imgWidth = pageWidth - 40;
        const imgHeight = (canvas.height * imgWidth) / canvas.width;
        pdf.addImage(imgData, "PNG", 20, 20, imgWidth, imgHeight);
        pdf.save(`${this.domain}.rapor.pdf`);
      } finally {
        // PDF stili kaldır
        this.$refs.pdfContent.classList.remove("pdf-export");
        this.pdfLoading = false;
        document.body.style.cursor = "";
      }
    },
  },
};
</script>

<style scoped>
.pdf-btn-row {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}
.pdf-btn {
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 8px 18px;
  font-size: 1em;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  position: relative;
}
.pdf-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
.spinner {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 3px solid #fff;
  border-top: 3px solid #d76a2b;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  vertical-align: middle;
  margin-right: 8px;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.report-result {
  padding: 2rem;
}
.summary-box {
  padding: 1rem;
  border-left: 5px solid #4caf50;
  margin-bottom: 2rem;
}
.info-box {
  padding: 1rem;
  border-left: 5px solid #2196f3;
  margin-bottom: 2rem;
}
.social-list {
  list-style: none;
  padding: 0;
  margin: 0 0 2rem 0;
}
.social-list li {
  margin-bottom: 8px;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th,
td {
  padding: 0.75rem;
  border: 1px solid #ccc;
  text-align: left;
}
.topic-chip {
  background: #e3e3fa;
  color: #222;
  border-radius: 12px;
  padding: 2px 10px;
  margin-right: 4px;
  font-size: 0.95em;
}
.result-card.pdf-export {
  background: #fff !important;
  color: #111 !important;
  box-shadow: none !important;
}
.result-card.pdf-export h2,
.result-card.pdf-export h3,
.result-card.pdf-export th,
.result-card.pdf-export td,
.result-card.pdf-export p,
.result-card.pdf-export span,
.result-card.pdf-export strong,
.result-card.pdf-export a {
  color: #111 !important;
}
.result-card.pdf-export .topic-chip {
  background: #f0f0f0 !important;
  color: #111 !important;
}
.result-card.pdf-export .info-box,
.result-card.pdf-export .summary-box {
  border-left-color: #888 !important;
  background: #fafafa !important;
}
.pdf-loading-text {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1em;
  font-weight: 600;
  color: #ffffff;
  min-height: 40px;
  padding: 0 12px;
}
</style>
