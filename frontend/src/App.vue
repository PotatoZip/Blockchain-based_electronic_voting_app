<template>
  <div class="px-32">
    <Navbar />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import Navbar from "./components/Navbar.vue";
</script>
