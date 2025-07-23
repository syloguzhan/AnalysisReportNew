<template>
  <div id="app">
    <Navbar />
    <router-view />
  </div>
</template>

<script>
import Navbar from "@/components/ui/Navbar.vue";
export default {
  name: "App",
  components: {
    Navbar,
  },
};
</script>

<style>
:root {
  --primary: #2d3a4b;
  --secondary: #4f5d75;
  --accent: #ef8354;
  --background: #f5f6fa;
  --surface: #ffffff;
  --text: #222f3e;
  --muted: #b0b7c3;
  --input-bg: #e9ecf3;
  --input-border: #b0b7c3;
  --input-focus: #ef8354;
}

body {
  background: var(--background);
  margin: 0;
  padding: 0;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: var(--text);
  background: var(--background);
  min-height: 100vh;
}

.navbar {
  background: var(--primary);
  padding: 24px 0;
  margin-bottom: 32px;
  box-shadow: 0 2px 8px rgba(45, 58, 75, 0.07);
}

.navbar a {
  color: var(--surface);
  font-weight: 600;
  margin: 0 18px;
  text-decoration: none;
  transition: color 0.2s;
}

.navbar a.router-link-exact-active {
  color: var(--accent);
}

.ui-card {
  background: var(--surface);
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(45, 58, 75, 0.08);
  padding: 24px;
  margin: 24px auto;
  max-width: 500px;
}

button,
.ui-button {
  background: var(--accent);
  color: var(--surface);
  border: none;
  border-radius: 6px;
  padding: 10px 22px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
button:hover,
.ui-button:hover {
  background: rgb(8, 0, 127);
}

input,
.custom-input input {
  background: var(--input-bg);
  border: 1.5px solid var(--input-border);
  border-radius: 6px;
  padding: 10px 14px;
  font-size: 1rem;
  outline: none;
  transition: border 0.2s, box-shadow 0.2s;
  margin-top: 6px;
  margin-bottom: 12px;
  width: 100%;
  box-sizing: border-box;
}
input:focus,
.custom-input input:focus {
  border-color: var(--input-focus);
  box-shadow: 0 0 0 2px #ef835455;
}

.form-group {
  margin-bottom: 18px;
}

.error-message {
  color: #e74c3c;
  font-size: 0.95rem;
  margin-top: 4px;
}

.ui-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(45, 58, 75, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.ui-modal-content {
  background: var(--surface);
  border-radius: 10px;
  padding: 32px 24px;
  min-width: 320px;
  box-shadow: 0 4px 24px rgba(45, 58, 75, 0.15);
}
</style>
