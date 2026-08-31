<script setup lang="ts">
import { ref, onMounted } from 'vue'

const BACKEND = import.meta.env.VITE_BACKEND_URL ?? 'http://localhost:8000'

type Me = { logged_in: boolean; email?: string; calendar_url?: string }
const me = ref<Me>({ logged_in: false })
const loading = ref(true)

onMounted(async () => {
  const res = await fetch(`${BACKEND}/backend/me`, { credentials: 'include' })
  me.value = await res.json()
  loading.value = false
})

function login() {
  window.location.href = `${BACKEND}/backend/login`
}

function logout() {
  window.location.href = `${BACKEND}/backend/logout`
}
</script>

<template>
  <main>
    <h1>ÖBB Ticket Calendar</h1>
    <p v-if="loading">Loading...</p>
    <template v-else-if="me.logged_in">
      <p>Logged in as {{ me.email }}</p>
      <p>Your calendar feed (add this as a subscribed calendar):</p>
      <input readonly :value="me.calendar_url" onclick="this.select()" />
      <p><button @click="logout">Logout</button></p>
    </template>
    <template v-else>
      <button @click="login">Login with Google</button>
    </template>
  </main>
</template>

<style scoped>
main {
  max-width: 640px;
  margin: 4rem auto;
  font-family: system-ui, sans-serif;
  text-align: center;
}
input {
  width: 100%;
  padding: 0.5rem;
}
button {
  padding: 0.5rem 1rem;
  cursor: pointer;
}
</style>
