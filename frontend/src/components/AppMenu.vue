<script setup>
import {RouterLink} from 'vue-router'
</script>

<template>
  <aside class="menu">
    <div class="menu-title">
      Translation Service
    </div>

    <nav>
      <RouterLink to="/">Dashboard</RouterLink>
      <RouterLink to="/import">Import document pair</RouterLink>
      <RouterLink to="/translate">Translate document</RouterLink>
      <RouterLink to="/about">About</RouterLink>
    </nav>
  </aside>
</template>

<style scoped>
.menu {
  border-right: 1px solid var(--color-border);
  padding: 1rem;
}

.menu-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.menu nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.menu nav a {
  color: var(--color-text);
}
.menu nav a {
  position: relative;
  display: block;

  padding: 0.4rem 0.4rem 0.4rem 1rem;

  color: var(--color-text);
}

.menu nav a.router-link-active {
  font-weight: 600;
}

.menu nav a.router-link-active::before {
  content: "▶";

  position: absolute;
  left: 0;
  top: 50%;

  transform: translateY(-50%);
}
</style>
