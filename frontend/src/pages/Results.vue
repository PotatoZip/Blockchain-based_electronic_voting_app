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
const results = ref<Array<{ choice_id: number; name: string; votes: number }>>(
  []
);
const total = ref(0);

async function fetchResults() {
  loading.value = true;
  error.value = null;
  try {
    const res = await fetch(`${API}/api/elections/${electionId}/results/`);
    const data = await res.json();
    if (!res.ok) throw new Error(data?.detail || `HTTP ${res.status}`);
    const sorted = (data.results || []).sort(
      (a: any, b: any) => b.votes - a.votes
    );
    results.value = sorted;
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
  <div class="min-h-screen bg-gray-50 py-12 px-4">
    <section class="mx-auto max-w-3xl">
      <!-- Back Button -->
      <div class="mb-4">
        <button
          @click="router.back()"
          class="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-medium px-5 py-2 rounded-lg shadow-md hover:shadow-lg transition-all duration-200"
        >
          <Icon icon="mdi:arrow-left" class="w-4 h-4" />
          <span>Back</span>
        </button>
      </div>

      <!-- Total Votes -->
      <div
        class="bg-white rounded-xl shadow-md p-8 mb-6 border border-gray-200"
      >
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Election Results</h1>
            <p class="text-gray-600 mt-1">Final vote count from blockchain</p>
          </div>
          <div class="text-right">
            <div class="text-4xl font-bold text-blue-600">{{ total }}</div>
            <div class="text-sm text-gray-500">Total Votes</div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div
        v-if="loading"
        class="bg-white rounded-xl shadow-md p-12 text-center border border-gray-200"
      >
        <Icon
          icon="line-md:loading-loop"
          class="w-12 h-12 text-blue-600 mx-auto"
        />
        <p class="mt-4 text-gray-600">Loading results...</p>
      </div>

      <!-- Error State -->
      <div
        v-else-if="error"
        class="bg-red-50 border border-red-200 rounded-xl shadow-md p-6"
      >
        <div class="flex items-center gap-3">
          <Icon icon="mdi:alert-circle" class="w-6 h-6 text-red-600" />
          <div>
            <p class="font-semibold text-red-900">Error loading results</p>
            <p class="text-sm text-red-700">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- Results -->
      <div v-else class="space-y-4">
        <div
          v-if="results.length === 0"
          class="bg-white rounded-xl shadow-md p-12 text-center border border-gray-200"
        >
          <Icon
            icon="mdi:file-document-outline"
            class="w-16 h-16 text-gray-300 mx-auto mb-4"
          />
          <p class="text-gray-600 text-lg">No results available yet</p>
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="(r, index) in results"
            :key="r.choice_id"
            class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-200 border border-gray-200"
          >
            <div class="p-6">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center gap-4">
                  <div
                    class="w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg"
                    :class="[
                      index === 0
                        ? 'bg-yellow-400 text-yellow-900'
                        : index === 1
                        ? 'bg-gray-300 text-gray-700'
                        : index === 2
                        ? 'bg-amber-600 text-amber-50'
                        : 'bg-blue-100 text-blue-700',
                    ]"
                  >
                    {{ index + 1 }}
                  </div>
                  <div>
                    <h3 class="text-xl font-semibold text-gray-900">
                      {{ r.name }}
                    </h3>
                    <p class="text-sm text-gray-500">{{ r.votes }} votes</p>
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-3xl font-bold text-blue-600">
                    {{ total ? Math.round((r.votes / total) * 100) : 0 }}%
                  </div>
                </div>
              </div>
              <div class="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                <div
                  class="h-full rounded-full transition-all duration-500"
                  :class="[
                    index === 0
                      ? 'bg-yellow-400'
                      : index === 1
                      ? 'bg-gray-400'
                      : index === 2
                      ? 'bg-amber-600'
                      : 'bg-blue-500',
                  ]"
                  :style="{ width: `${total ? (r.votes / total) * 100 : 0}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
