<template>
  <div class="pt-8 mx-auto max-w-7xl">
    <nav
      class="p-4 rounded-3xl boder border-gray-200 dark:bg-gray-900 bg-white shadow-md"
    >
      <div class="px-4 py-3 flex items-center gap-4">
        <RouterLink to="/" class="flex items-center gap-4">
          <img src="/logo.png" class="h-12 w-12" alt="logo" />
          <span class="font-bold text-4xl text-indigo-300">EtherVote</span>
        </RouterLink>

        <nav class="ml-auto">
          <ul class="flex items-center gap-12 text-2xl px-4">
            <li v-for="link in links" :key="link.to">
              <RouterLink :to="link.to" v-slot="{ isActive }" class="block">
                <span
                  class="text-indigo-200 hover:text-indigo-300"
                  :class="isActive ? 'text-indigo-700' : 'text-indigo-300'"
                >
                  {{ link.label }}
                </span>
              </RouterLink>
            </li>
          </ul>
        </nav>
      </div>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from "vue-router";

const links = [
  { to: "/", label: "Home" },
  { to: "/elections", label: "Votings" },
  { to: "/about", label: "About" },
];
</script>
