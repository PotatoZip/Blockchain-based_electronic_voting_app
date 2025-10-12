<script setup lang="ts">
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Icon } from "@iconify/vue";

const API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const route = useRoute();
const router = useRouter();
const electionId = route.params.id as string;

const pesel = ref("");
const code = ref("");
const loading = ref(false);
const error = ref<string | null>(null);

async function submit() {
  error.value = null;
  loading.value = true;
  try {
    const res = await fetch(`${API}/api/elections/${electionId}/verify/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pesel: pesel.value, code: code.value }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data?.detail || `HTTP ${res.status}`);

    sessionStorage.setItem("evote_session_id", data.session_id);
    sessionStorage.setItem("evote_eth_address", data.eth_address);

    router.push(`/elections/${electionId}/vote`);
  } catch (e: any) {
    error.value = e?.message ?? "Verification failed";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <section
    class="mx-auto max-w-md mt-16 bg-gray-100 border border-gray-100 shadow-2xl p-6 rounded-3xl p-6"
  >
    <h1 class="text-2xl font-bold text-gray-900 mb-1">Identity verification</h1>
    <p class="text-gray-600 mb-6">
      Enter your PESEL and code sent to your email.
    </p>

    <form @submit.prevent="submit" class="space-y-4">
      <div>
        <label class="block text-sm text-gray-700 mb-1">PESEL</label>
        <input
          v-model="pesel"
          inputmode="numeric"
          maxlength="11"
          minlength="11"
          class="w-full rounded-3xl border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
          required
        />
      </div>
      <div>
        <label class="block text-sm text-gray-700 mb-1"
          >Verification code</label
        >
        <input
          v-model="code"
          class="w-full rounded-3xl border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
          required
        />
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full inline-flex items-center justify-center gap-2 rounded-full bg-indigo-600 px-4 py-2 text-white font-medium hover:bg-indigo-700 transition disabled:opacity-60"
      >
        <Icon
          v-if="loading"
          icon="line-md:loading-twotone-loop"
          class="w-5 h-5"
        />
        Verify & Vote
      </button>

      <p v-if="error" class="text-red-600 text-sm">{{ error }}</p>
    </form>
  </section>
</template>
