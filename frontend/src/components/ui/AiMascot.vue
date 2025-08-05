<template>
  <div class="mascot-container">
    <div class="speech-bubble" v-if="showBubble">
      {{ bubbleMessage }}
    </div>
    <svg
      class="robot"
      width="200"
      height="200"
      viewBox="0 0 200 200"
      xmlns="http://www.w3.org/2000/svg"
    >
      <circle
        cx="100"
        cy="100"
        r="70"
        fill="#3498db"
        stroke="#2c3e50"
        stroke-width="4"
      />

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

      <path
        d="M75 120 Q100 140 125 120"
        stroke="#fff"
        stroke-width="4"
        fill="none"
        stroke-linecap="round"
      />

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
        { text: "Collecting data", icon: "🔍" },
        { text: "Analyzing competitors", icon: "📊" },
        { text: "Scanning social media", icon: "📱" },
        { text: "AI is creating content", icon: "🧠" },
        { text: "Preparing the report", icon: "📄" },
        { text: "Finalizing analysis", icon: "✅" },
        { text: "Formatting for output", icon: "📝" },
        { text: "Optimizing insights", icon: "📌" },
        { text: "Finishing touches", icon: "🎯" },
        { text: "Ready to display!", icon: "🚀" },
      ],
      currentStep: 0,
      eyeBlink: false,
      antenColor: "#e74c3c",
      showBubble: false,
      bubbleMessage: "",
      bubbleMessages: [
        "Hi! Starting the analysis...",
        "Hmm... This domain looks interesting!",
        "AI is processing content!",
        "Almost there 😄",
        "Hold tight, I’m checking the social profiles!",
        "Data detected, organizing it for clarity...",
        "This will only take a few more seconds ⏳",
        "Searching for recent activity 📰",
        "Finding hidden insights 🔍",
        "Evaluating trends and strategies...",
        "Finalizing visual summary 📊",
        "Writing up a smart summary ✍️",
        "One moment... cleaning up the report!",
        "Almost done! Loading final output ⚙️",
      ],
    };
  },
  mounted() {
    this.startAnimations();
  },
  methods: {
    startAnimations() {
      setInterval(() => {
        this.eyeBlink = true;
        setTimeout(() => {
          this.eyeBlink = false;
        }, 180);
      }, 3000);


      setInterval(() => {
        this.antenColor = this.antenColor === "#e74c3c" ? "#2ecc71" : "#e74c3c";
      }, 2000);


      setInterval(() => {
        this.bubbleMessage =
          this.bubbleMessages[
            Math.floor(Math.random() * this.bubbleMessages.length)
          ];
        this.showBubble = true;

        setTimeout(() => {
          this.showBubble = false;
        }, 10000);
      }, 10000);

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
  padding-top: 80px;
  animation: fadeIn 1s ease-in;
  position: relative;
}

.robot {
  animation: float 2s ease-in-out infinite;
}

.status-box {
  margin-top: -35px;
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
  margin-bottom: 4px;
}

.step-icon {
  margin-right: 10px;
  font-size: 20px;
}

.dots {
  display: flex;
  justify-content: center;
  margin-top: 4px;
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
  top: -40px;
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
  animation: fadeInOut 10s ease-in-out;
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
