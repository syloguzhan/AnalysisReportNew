<template>
  <div class="mascot-container">
    <!-- Konuşma Balonu -->
    <div class="speech-bubble" v-if="showBubble">
      {{ bubbleMessage }}
    </div>

    <!-- Robot ve Radar SVG -->
    <svg
      class="robot"
      width="200"
      height="200"
      viewBox="0 0 200 200"
      xmlns="http://www.w3.org/2000/svg"
    >
      <!-- Kafa -->
      <circle
        cx="100"
        cy="100"
        r="70"
        fill="#3498db"
        stroke="#2c3e50"
        stroke-width="4"
      />

      <!-- Gözler -->
      <circle
        class="eye left"
        :r="eyeBlink ? 2 : 6"
        cx="75"
        cy="90"
        fill="#fff"
      />
      <circle
        class="eye right"
        :r="eyeBlink ? 2 : 6"
        cx="125"
        cy="90"
        fill="#fff"
      />

      <!-- Ağız -->
      <path
        d="M75 120 Q100 140 125 120"
        stroke="#fff"
        stroke-width="4"
        fill="none"
        stroke-linecap="round"
      />

      <!-- Anten -->
      <line
        x1="100"
        y1="30"
        x2="100"
        y2="15"
        stroke="#2c3e50"
        stroke-width="4"
      />
      <circle cx="100" cy="10" r="6" :fill="antenColor" />
    </svg>

    <!-- Aşamalı Yazılar -->
    <div class="status-box">
      <p class="loading-text">
        <span class="step-icon">{{ steps[currentStep].icon }}</span>
        {{ steps[currentStep].text }}
      </p>
      <div class="dots">
        <span v-for="n in 3" :key="n" :class="'dot dot-' + n"></span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      steps: [
        { text: "Collecting data", icon: "🔍" }, // Veriler toplanıyor
        { text: "Analyzing competitors", icon: "📊" }, // Rakip firmalar analiz ediliyor
        { text: "Scanning social media", icon: "📱" }, // Sosyal medya taranıyor
        { text: "AI is creating content", icon: "🧠" }, // Yapay zeka içerik oluşturuyor
        { text: "Preparing the report", icon: "📄" }, // Rapor hazırlanıyor
        { text: "Finalizing analysis", icon: "✅" }, // Son analiz tamamlanıyor
        { text: "Formatting for output", icon: "📝" }, // Rapor çıktıya uygun hale getiriliyor
        { text: "Optimizing insights", icon: "📌" }, // İçgörüler optimize ediliyor
        { text: "Finishing touches", icon: "🎯" }, // Son rötuşlar yapılıyor
        { text: "Ready to display!", icon: "🚀" }, // Görüntülemeye hazır!
      ],
      currentStep: 0,
      eyeBlink: false,
      antenColor: "#e74c3c",
      showBubble: false,
      bubbleMessage: "",
      bubbleMessages: [
        "Hi! Starting the analysis...", // Merhaba! Analize başlıyorum...
        "Hmm... This domain looks interesting!", // Hmm... Bu domain ilginçmiş!
        "AI is processing content!", // AI içerikleri işliyor!
        "Almost there 😄", // Neredeyse hazır 😄
        "Hold tight, I’m checking the social profiles!", // Beklemede kal, sosyal profilleri kontrol ediyorum!
        "Data detected, organizing it for clarity...", // Veriler tespit edildi, düzenleniyor...
        "This will only take a few more seconds ⏳", // Sadece birkaç saniye daha sürecek ⏳
        "Searching for recent activity 📰", // Güncel etkinlikler araştırılıyor 📰
        "Finding hidden insights 🔍", // Gizli içgörüler bulunuyor 🔍
        "Evaluating trends and strategies...", // Trendler ve stratejiler değerlendiriliyor...
        "Finalizing visual summary 📊", // Görsel özet tamamlanıyor 📊
        "Writing up a smart summary ✍️", // Akıllı bir özet yazılıyor ✍️
        "One moment... cleaning up the report!", // Bir saniye... rapor düzenleniyor!
        "Almost done! Loading final output ⚙️", // Neredeyse bitti! Son çıktı yükleniyor ⚙️
      ],
    };
  },
  mounted() {
    this.startAnimations();
  },
  methods: {
    startAnimations() {
      // 👁 Göz kırpma animasyonu (3 saniyede bir)
      setInterval(() => {
        this.eyeBlink = true;
        setTimeout(() => {
          this.eyeBlink = false;
        }, 180);
      }, 3000);

      // 📡 Anten rengini değiştir (2 saniyede bir)
      setInterval(() => {
        this.antenColor = this.antenColor === "#e74c3c" ? "#2ecc71" : "#e74c3c";
      }, 2000);

      // 💬 10 saniyede bir konuşma balonu göster (balon 10 saniye boyunca açık kalır)
      setInterval(() => {
        this.bubbleMessage =
          this.bubbleMessages[
            Math.floor(Math.random() * this.bubbleMessages.length)
          ];
        this.showBubble = true;

        // 10 saniye sonra balonu kaldır
        setTimeout(() => {
          this.showBubble = false;
        }, 10000);
      }, 10000);

      // ⏱️ Her 10 saniyede bir adımı değiştir
      setInterval(() => {
        if (this.currentStep < this.steps.length - 1) {
          this.currentStep++;
        }
      }, 10000);
    },
  },
};
</script>

<style scoped>
.mascot-container {
  text-align: center;
  margin-top: 60px;
  padding-top: 80px; /* 💬 Balona yer bırakmak için */
  animation: fadeIn 1s ease-in;
  position: relative;
}

.robot {
  animation: float 2s ease-in-out infinite;
}

.status-box {
  margin-top: -35px; /* 🔼 Daha yukarı taşıdık (önceden 20px'ti) */
  animation: fadeIn 1s ease-in;
}

.loading-text {
  font-size: 18px;
  color: #eee;
  font-weight: 500;
  font-family: "Segoe UI", sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 4px; /* 🔽 Yazı ile noktalar arası boşluğu azalttık */
}

.step-icon {
  margin-right: 10px;
  font-size: 20px;
}

.dots {
  display: flex;
  justify-content: center;
  margin-top: 4px; /* 🔽 Önceden 8px'ti, azaltıldı */
}
.dot {
  width: 10px;
  height: 10px;
  background-color: #f1f1f1;
  border-radius: 50%;
  margin: 0 4px;
  animation: bounce 1.4s infinite ease-in-out both;
}
.dot-1 {
  animation-delay: -0.32s;
}
.dot-2 {
  animation-delay: -0.16s;
}
.dot-3 {
  animation-delay: 0;
}

.radar-line {
  animation: radar-spin 2s linear infinite;
}

.speech-bubble {
  position: absolute;
  top: -40px; /* 🧠 Robot kafasının üstüne yerleştirildi */
  left: 50%;
  transform: translateX(-50%);
  background: #fff;
  color: #333;
  padding: 8px 16px;
  border-radius: 16px;
  font-size: 14px;
  max-width: 240px;
  opacity: 1;
  transition: opacity 0.5s;
  animation: fadeInOut 10s ease-in-out; /* 💬 10 saniyelik görünme süresi */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

@keyframes fadeInOut {
  0% {
    opacity: 0;
  }
  5% {
    opacity: 1;
  }
  95% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

@keyframes float {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0);
  }
}

@keyframes radar-spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes bounce {
  0%,
  80%,
  100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
