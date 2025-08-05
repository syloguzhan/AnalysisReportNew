<template>
  <div class="report-result">
    <div class="result-card" ref="pdfContent">
      <div class="header-row">
        <div class="saved-at" v-if="savedAt">Saved At: {{ formatDate(savedAt) }}</div>
        <button v-if="!pdfLoading" class="pdf-btn" @click="downloadPDF">
          <span>Create PDF</span>
        </button>
        <div v-else class="pdf-loading-text no-pdf">Loading...</div>
      </div>

      <h2><span class="icon"></span> Analysis Results: <span class="domain">{{ domain }}</span></h2>
      <section v-if="comparisonTable && comparisonTable.length" class="comparison-table">
        <h3><span class="icon"></span> Comparison Matrix</h3>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Section</th>
                <th v-for="company in companyNames" :key="company">{{ company }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="header in tableHeaders" :key="header">
                <td>{{ header }}</td>
                <td v-for="company in companyNames" :key="company">{{ getCell(company, header) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="main-report" v-if="mainReport">
        <h3><span class="icon"></span> Company Analysis</h3>
        <div v-for="(content, title) in mainReport" :key="title" class="info-box">
          <h4>{{ title }}</h4>
          <p>{{ content }}</p>
        </div>
      </section>

      <section class="competitor-report" v-if="competitors && competitors.length">
        <h3><span class="icon"></span> Competitor Company Analysis</h3>
        <div v-for="comp in competitors" :key="comp.competitor_domain" class="info-box">
          <h4>{{ comp.competitor_domain }}</h4>
          <div v-for="(content, title) in comp.sections" :key="title" style="margin-bottom: 1rem;">
            <strong>{{ title }}</strong>
            <p>{{ content }}</p>
          </div>
        </div>
      </section>
    </div>
    <div class="reanalyze-wrapper no-pdf">
      <button class="reanalyze-btn" @click="$emit('reanalyze')">Re-Analyze</button>
    </div>
  </div>
</template>

<script>
import html2pdf from "html2pdf.js";

export default {
  name: 'ReportResult',
  props: {
    domain: { type: String, required: true },
    mainReport: { type: Object, default: () => ({}) },
    competitors: { type: Array, default: () => [] },
    comparisonTable: { type: Array, default: () => [] },
    savedAt: { type: String, default: null }
  },
  data() {
    return { pdfLoading: false };
  },
  computed: {
    companyNames() {
      return this.comparisonTable.map(row => row.company);
    },
    tableHeaders() {
      if (this.comparisonTable.length > 0) {
        return Object.keys(this.comparisonTable[0]).filter(k => k !== 'company');
      }
      return [];
    }
  },
  methods: {
    getCell(company, header) {
      const row = this.comparisonTable.find(r => r.company === company);
      return row ? row[header] : '';
    },
    formatDate(dateStr) {
      const d = new Date(dateStr);
      return d.toLocaleString('tr-TR', {
        timeZone: 'Europe/Istanbul',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    },
    async downloadPDF() {
      this.pdfLoading = true;
      document.body.style.cursor = 'wait';
      try {
        const el = this.$refs.pdfContent;

        document.querySelectorAll('.no-pdf').forEach(el => (el.style.display = 'none'));

        const opt = {
          margin: 0.2,
          filename: `${this.domain}.report.pdf`,
          image: { type: 'jpeg', quality: 0.98 },
          html2canvas: {
            scale: 3,
            useCORS: true,
            scrollX: 0,
            scrollY: 0
          },
          jsPDF: {
            unit: 'in',
            format: 'a4',
            orientation: 'landscape' //
          },
          pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
        };

        await html2pdf().set(opt).from(el).save();

        // ✅ PDF tamamlanınca gizlenen elementleri geri göster
        document.querySelectorAll('.no-pdf').forEach(el => (el.style.display = ''));
      } finally {
        this.pdfLoading = false;
        document.body.style.cursor = '';
      }
    }
  }
};
</script>

<style scoped>
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.saved-at {
  font-size: 0.9em;
  color: #ccc;
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
}
.comparison-table {
  margin-bottom: 2rem;
}
.table-wrapper {
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
th, td {
  padding: .75rem;
  border: 1px solid #ccc;
  text-align: left;
}
th {
  background-color: #444;
  color: #fff;
}
.reanalyze-wrapper {
  text-align: center;
  margin-top: 20px;
}
.reanalyze-btn {
  background: #6ec1e4;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s;
}
.reanalyze-btn:hover {
  background: #4a9bbf;
}
</style>
