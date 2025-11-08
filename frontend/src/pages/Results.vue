<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Icon } from "@iconify/vue";

const API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const route = useRoute();
const router = useRouter();
const electionId = Number(route.params.id);

const loading = ref(true);
const error = ref<string | null>(null);
const results = ref<Array<{ choice_id: number; name: string; votes: number }>>([]);
const total = ref(0);

async function fetchResults() {
  loading.value = true;
  error.value = null;
  try {
    const res = await fetch(`${API}/api/elections/${electionId}/results/`);
    const data = await res.json();
    if (!res.ok) throw new Error(data?.detail || `HTTP ${res.status}`);
    results.value = data.results || [];
    total.value = results.value.reduce((s, r) => s + (r.votes || 0), 0);
  } catch (e: any) {
    error.value = e?.message ?? "Fetch error";
  } finally {
    loading.value = false;
  }
}

onMounted(fetchResults);
</script>

<template>
  <section class="mx-auto max-w-2xl mt-12 bg-white rounded-3xl border border-gray-100 shadow-2xl p-6">
    <header class="mb-4">
      <h1 class="text-2xl font-bold text-gray-900">Election results</h1>
    </header>

    <div v-if="loading" class="text-gray-600">Loading…</div>
    <div v-else-if="error" class="text-red-600">Error: {{ error }}</div>

    <div v-else>
      <div v-if="results.length === 0" class="text-gray-600">No results available.</div>

      <ul v-else class="space-y-3">
        <li v-for="r in results" :key="r.choice_id" class="flex items-center justify-between p-3 rounded-lg border border-gray-100">
          <div>
            <div class="font-medium text-gray-900">{{ r.name }}</div>
            <div class="text-sm text-gray-500">{{ r.votes }} votes</div>
          </div>
          <div class="text-right">
            <div class="font-mono text-lg">{{ r.votes }}</div>
            <div class="text-sm text-gray-500">{{ total ? Math.round((r.votes/total)*100) : 0 }}%</div>
          </div>
        </li>
      </ul>

      <div class="mt-6 text-sm text-gray-600">Total votes: {{ total }}</div>

      <div class="mt-6">
        <button @click="router.back()" class="inline-flex items-center gap-2 bg-gray-100 px-4 py-2 rounded-full">Back</button>
      </div>
    </div>
  </section>
</template>
