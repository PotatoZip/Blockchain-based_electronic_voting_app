<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Icon } from "@iconify/vue";
import { getAddress, signMessage } from "../utils/wallet";

const API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const route = useRoute();
const router = useRouter();
const electionId = route.params.id as string;

const pesel = ref("");
const code = ref("");
const loading = ref(false);
const error = ref<string | null>(null);

const election = ref<any | null>(null);
const results = ref<Array<any>>([]);
const loadingResults = ref(false);

const isElectionStarted = computed(() => {
  if (!election.value) return false;
  return new Date(election.value.start_date) <= new Date();
});

const hasVoted = computed(() => {
  if (!election.value) return false;
  return sessionStorage.getItem(`has_voted_${election.value.id}`) === "true";
});

async function submit() {
  error.value = null;
  loading.value = true;
  try {
    const address = (await getAddress()).toLowerCase();

    const chRes = await fetch(`${API}/api/auth/challenge/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ address }),
    });
    const chData = await chRes.json();
    if (!chRes.ok) throw new Error(chData?.detail || `HTTP ${chRes.status}`);

    const { signature } = await signMessage(chData.nonce);

    const res = await fetch(`${API}/api/auth/verify/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        pesel: pesel.value,
        code: code.value,
        election_id: Number(electionId),
        address,
        signature,
      }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data?.detail || `HTTP ${res.status}`);

    sessionStorage.setItem("evote_session_token", data.session_token);
    sessionStorage.setItem("evote_public_address", data.public_address);
    sessionStorage.setItem("evote_next_nonce", String(data.next_nonce ?? 1));

    router.push(`/elections/${electionId}/vote`);
  } catch (e: any) {
    error.value = e?.message ?? "Verification failed";
  } finally {
    loading.value = false;
  }
}

async function fetchElectionAndMaybeResults() {
  try {
    const res = await fetch(`${API}/api/elections/${electionId}/`);
    const data = await res.json();
    if (!res.ok) throw new Error(data?.detail || `HTTP ${res.status}`);
    election.value = data;

    if (data.status === "archive") {
      loadingResults.value = true;
      const r = await fetch(`${API}/api/elections/${electionId}/results/`);
      const rd = await r.json();
      if (!r.ok) throw new Error(rd?.detail || `HTTP ${r.status}`);
      results.value = rd.results || [];
      loadingResults.value = false;
    }
  } catch (e: any) {
    console.error(e);
  }
}

onMounted(() => {
  fetchElectionAndMaybeResults();
});
</script>

<template>
  <section
    class="mx-auto max-w-md mt-16 bg-gray-100 border border-gray-100 shadow-2xl p-6 rounded-3xl"
  >
    <ResetWallet :election-started="isElectionStarted" :has-voted="hasVoted" />

    <h1 class="text-2xl font-bold text-gray-900 mb-1">Identity verification</h1>
    <p class="text-gray-600 mb-6">
      Enter your PESEL and code from mail message
    </p>

    <form @submit.prevent="submit" class="space-y-4">
      <div v-if="election && election.status === 'archive'" class="mb-4">
        <h3 class="text-lg font-semibold">Election results</h3>
        <div v-if="loadingResults" class="text-gray-600">Loading results…</div>
        <div v-else-if="results.length === 0" class="text-gray-600">
          No results available.
        </div>
        <ul v-else class="mt-2 space-y-2">
          <li
            v-for="r in results"
            :key="r.choice_id"
            class="flex justify-between"
          >
            <span>{{ r.name }}</span>
            <span class="font-mono">{{ r.votes }}</span>
          </li>
        </ul>
      </div>
      <div>
        <label class="block text-sm text-gray-700 mb-1">PESEL</label>
        <input
          v-model="pesel"
          inputmode="numeric"
          maxlength="11"
          minlength="11"
          class="w-full rounded-ml border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
          required
        />
      </div>
      <div>
        <label class="block text-sm text-gray-700 mb-1"
          >Verification code</label
        >
        <input
          v-model="code"
          class="w-full rounded-ml border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
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
