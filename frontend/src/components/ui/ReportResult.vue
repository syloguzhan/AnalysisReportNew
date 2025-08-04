<template>
  <div class="report-result">
    <div class="result-card" ref="pdfContent">
      <div class="pdf-btn-row">
        <button v-if="!pdfLoading" class="pdf-btn" @click="downloadPDF">
          <span>Create PDF</span>
        </button>
        <div v-else class="pdf-loading-text">Loading...</div>
      </div>

      <h2><span class="icon">📄</span> Analysis Results: <span class="domain">{{ domain }}</span></h2>

      <!-- ✅ Yeni Ana Rapor Bölümü -->
      <section class="main-report" v-if="mainReport">
        <h3><span class="icon">🧠</span> Company Analysis</h3>
        <div v-for="(content, title) in mainReport" :key="title" class="info-box">
          <h4>{{ title }}</h4>
          <p>{{ content }}</p>
        </div>
      </section>

      <!-- ✅ Yeni Rakip Firma Bölümü -->
      <section class="competitor-report" v-if="competitors && competitors.length">
        <h3><span class="icon">🏁</span> Competitor Company Analysis</h3>
        <div v-for="comp in competitors" :key="comp.competitor_domain" class="info-box">
          <h4>{{ comp.competitor_domain }}</h4>
          <div v-for="(content, title) in comp.sections" :key="title" style="margin-bottom: 1rem;">
            <strong>{{ title }}</strong>
            <p>{{ content }}</p>
          </div>
        </div>
      </section>

      <!-- 🔽 Mevcut Kodların Tamamı (dokunulmadı) -->
      <!-- Şirket Bilgileri Bölümü -->
      <section class="company-info" v-if="company">
        <h3><span class="icon">🏢</span> Company Information</h3>
        <div class="info-box">
          <p><strong>Name:</strong> {{ company.name }}</p>
          <p v-if="company.sector"><strong>Sector:</strong> {{ company.sector }}</p>
          <p v-if="company.size"><strong>Worker:</strong> {{ company.size }}</p>
          <p v-if="company.founded"><strong>Establishment:</strong> {{ company.founded }}</p>
          <p v-if="company.description"><strong>Explanation:</strong> {{ company.description }}</p>
        </div>
      </section>

      <!-- Sosyal Medya Varlıkları Bölümü -->
      <section class="social-media" v-if="socialMedia && socialMedia.length">
        <h3><span class="icon">🌐</span> Social Media Assets</h3>
        <ul class="social-list">
          <li v-for="s in socialMedia" :key="s.platform">
            <strong>{{ s.platform }}:</strong>
            <a :href="s.url" target="_blank">{{ s.url }}</a>
            <span v-if="s.followers">- Follower: {{ s.followers }}</span>
          </li>
        </ul>
      </section>

      <!-- Yapay Zeka Analiz Tablosu -->
      <section class="ai-analysis-table" v-if="aiAnalysis && aiAnalysis.length">
        <h3><span class="icon">🤖</span> Artificial Intelligence Analysis</h3>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Criterion</th>
                <th>Value</th>
                <th>Comment</th>
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



    </div>
  </div>
</template>

<script>
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'
import html2pdf from "html2pdf.js";

export default {
  name: 'ReportResult',
  props: {
    domain:        { type: String, required: true },
    mainReport:    { type: Object,  default: () => ({}) },     // ✅ eklendi
    competitors:   { type: Array,   default: () => [] },
    summary:       { type: String, default: "" },
    company:       { type: Object, default: null },
    socialMedia:   { type: Array,  default: () => [] },
    aiAnalysis:    { type: Array,  default: () => [] }
  },
  data() {
    return {
      pdfLoading: false
    }
  },

    methods: {
      async downloadPDF() {
        this.pdfLoading = true;
        document.body.style.cursor = 'wait';

        try {
          const el = this.$refs.pdfContent;

          const opt = {
            margin:       0.5,
            filename:     `${this.domain}.rapor.pdf`,
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  {
              scale: 2,
              useCORS: true,
              scrollY: 0,          // 🔥 Sayfa kaydırılsa da tüm içerik alınır
            },
            jsPDF:        { unit: 'in', format: 'a4', orientation: 'portrait' },
            pagebreak:    { mode: ['avoid-all', 'css', 'legacy'] }
          };

          await html2pdf().set(opt).from(el).save();
        } finally {
          this.pdfLoading = false;
          document.body.style.cursor = '';
        }
      }
    }
}
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
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.report-result { padding:2rem; }
.summary-box   { padding:1rem; border-left:5px solid #4CAF50; margin-bottom:2rem; }
.info-box      { padding:1rem; border-left:5px solid #2196F3; margin-bottom:2rem; }
.social-list   { list-style:none; padding:0; margin:0 0 2rem 0; }
.social-list li { margin-bottom: 8px; }
table          { width:100%; border-collapse:collapse; }
th,td          { padding:.75rem; border:1px solid #ccc; text-align:left; }
.topic-chip    { background:#e3e3fa; color:#222; border-radius:12px; padding:2px 10px; margin-right:4px; font-size:0.95em; }
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