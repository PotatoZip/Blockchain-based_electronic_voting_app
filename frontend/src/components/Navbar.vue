<template>
  <div class="pt-8 mx-auto max-w-7xl">
    <nav
      class="p-4 rounded-3xl border border-gray-200 dark:bg-gray-900 bg-white shadow-md"
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
            <li>
              <button
                @click="handleResetWallet"
                class="text-red-400 hover:text-red-500 text-sm py-1 px-3 border border-red-400 rounded-full hover:border-red-500"
              >
                Reset "Wallet"
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from "vue-router";
import { clearWallet } from "../utils/wallet";

const links = [
  { to: "/", label: "Home" },
  { to: "/elections", label: "Votings" },
  { to: "/about", label: "About" },
];

function handleResetWallet() {
  if (
    confirm(
      "Are you sure you want to reset your wallet? This will clear your stored keys and you will need to set up your wallet again during your next voting."
    )
  ) {
    clearWallet();
    window.location.reload();
  }
}
</script>
