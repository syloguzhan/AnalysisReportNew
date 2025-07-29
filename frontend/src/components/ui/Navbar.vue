<template>
  <nav class="navbar radar-navbar">
    <router-link to="/">Domain login</router-link> |
    <router-link to="/history">History</router-link>
  </nav>
</template>

<script>
export default {
  name: "Navbar"
};
</script>

<style scoped>
.radar-navbar {
  width: 100vw;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
  background: rgba(0,0,0,0);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 24px #000a, 0 1.5px 0 #ff3c3c44 inset;
  border-bottom: 2px solid #ff3c3c33;
  padding: 18px 0 18px 0;
  display: flex;
  justify-content: center;
  align-items: center;
}
.radar-navbar a {
  color: #6ec1e4;
  font-weight: 600;
  margin: 0 22px;
  text-decoration: none;
  font-size: 1.18rem;
  letter-spacing: 0.08em;
  transition: color 0.2s, border 0.2s;
  padding: 4px 0;
  border-bottom: 2px solid transparent;
}
.radar-navbar a.router-link-exact-active,
.radar-navbar a:hover {
  color: #ff3c3c;
  border-bottom: 2px solid #ff3c3c;
}
</style> 