<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Icon } from "@iconify/vue";
import { signMessage } from "../utils/wallet";

const API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const route = useRoute();
const router = useRouter();
const electionId = Number(route.params.id);

type Choice = { id: number; name: string; description?: string };
type ElectionDetail = {
  id: number;
  name: string;
  description?: string;
  start_date: string;
  end_date: string;
  choices?: Choice[];
};

const loading = ref(true);
const error = ref<string | null>(null);
const election = ref<ElectionDetail | null>(null);
const selectedChoice = ref<number | null>(null);

const sessionToken = sessionStorage.getItem("evote_session_token");
const localNonce = ref<number>(
  Number(sessionStorage.getItem("evote_next_nonce") || "1")
);

if (!sessionToken) {
  router.replace(`/elections/${electionId}`);
}

async function fetchElection() {
  loading.value = true;
  error.value = null;
  try {
    const res = await fetch(`${API}/api/elections/${electionId}/`);
    const data = await res.json();
    if (!res.ok) throw new Error(data?.detail || `HTTP ${res.status}`);
    election.value = data;
  } catch (e: any) {
    error.value = e?.message ?? "Fetch error";
  } finally {
    loading.value = false;
  }
}

async function castVote() {
  if (!selectedChoice.value) {
    error.value = "Please pick an option.";
    return;
  }
  error.value = null;
  loading.value = true;
  try {
    const message = `vote:${electionId}:${selectedChoice.value}:${localNonce.value}`;
    const { signature } = await signMessage(message);

    const res = await fetch(`${API}/api/elections/${electionId}/vote/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_token: sessionToken,
        choice_id: selectedChoice.value,
        signature,
      }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data?.detail || `HTTP ${res.status}`);

    if (election.value) {
      sessionStorage.setItem(`has_voted_${election.value.id}`, "true");
    }

    alert(`Vote submitted.\nTx: ${data.txHash}`);

    if (typeof data.next_nonce === "number") {
      localNonce.value = data.next_nonce;
      sessionStorage.setItem("evote_next_nonce", String(data.next_nonce));
    } else {
      localNonce.value += 1;
      sessionStorage.setItem("evote_next_nonce", String(localNonce.value));
    }

    router.replace(`/`);
  } catch (e: any) {
    error.value = e?.message ?? "Vote failed";
  } finally {
    loading.value = false;
  }
}

const canSubmit = computed(
  () => !!selectedChoice.value && !!sessionToken && !loading.value
);

onMounted(fetchElection);
</script>

<template>
  <section
    class="mx-auto max-w-2xl mt-12 bg-white rounded-3xl border border-gray-100 shadow-2xl p-6"
  >
    <header class="mb-4">
      <h1 class="text-2xl font-bold text-gray-900">Cast your vote</h1>
    </header>

    <div v-if="loading" class="text-gray-600">Loading…</div>
    <div v-else-if="error" class="text-red-600">{{ error }}</div>

    <div v-else-if="election">
      <div class="mt-6 space-y-3">
        <label
          v-for="c in election.choices || []"
          :key="c.id"
          class="flex items-center gap-3 rounded-2xl border border-gray-200 bg-gray-50 p-4 cursor-pointer hover:bg-gray-100"
        >
          <input
            type="radio"
            name="choice"
            class="size-4 text-indigo-600 focus:ring-2"
            :value="c.id"
            v-model="selectedChoice"
          />
          <div>
            <div class="font-medium text-gray-900">{{ c.name }}</div>
            <div class="text-sm text-gray-600" v-if="c.description">
              {{ c.description }}
            </div>
          </div>
        </label>
      </div>

      <button
        class="mt-6 w-full inline-flex items-center justify-center gap-2 rounded-full bg-indigo-600 px-4 py-2 text-white font-medium hover:bg-indigo-700 transition disabled:opacity-60"
        :disabled="!canSubmit"
        @click="castVote"
      >
        <Icon
          v-if="loading"
          icon="line-md:loading-twotone-loop"
          class="w-5 h-5"
        />
        Submit vote
      </button>
    </div>
  </section>
</template>
