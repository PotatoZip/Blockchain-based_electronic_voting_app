<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { RouterLink } from "vue-router";
import { Icon } from "@iconify/vue";

type Election = {
  id: number;
  name: string;
  description?: string;
  start_date: string;
  end_date: string;
  status: "active" | "archive" | "upcoming";
};

const API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

const elections = ref<Election[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

const filter = ref<"all" | "active" | "archive" | "upcoming">("all");

const dateFrom = ref<string>("");
const dateTo = ref<string>("");

async function fetchElections() {
  loading.value = true;
  error.value = null;
  try {
    const params = new URLSearchParams();
    if (filter.value !== "all") params.set("status", filter.value);
    if (dateFrom.value) params.set("date_from", dateFrom.value);
    if (dateTo.value) params.set("date_to", dateTo.value);

    const url = `${API}/api/elections/${
      params.toString() ? "?" + params.toString() : ""
    }`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();

    const items = Array.isArray(data)
      ? data
      : Array.isArray(data?.results)
      ? data.results
      : [];
    elections.value = (items || []).filter(Boolean);
  } catch (e: any) {
    error.value = e?.message ?? "Fetch error";
    elections.value = [];
  } finally {
    loading.value = false;
  }
}

onMounted(fetchElections);
watch([filter, dateFrom, dateTo], fetchElections);

function fmt(d: string) {
  return new Date(d).toLocaleString();
}
</script>

<template>
  <div class="mx-auto max-w-5xl">
    <div class="mt-20 grid gap-4">
      <!-- Filters -->
      <div class="flex flex-col md:flex-row gap-4">
        <div
          class="flex-1 bg-gray-100 rounded-3xl border border-gray-100 shadow-xl p-6"
        >
          <div class="flex flex-wrap items-center gap-6">
            <label class="inline-flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                class="size-4 text-indigo-600 focus:ring-2"
                value="all"
                v-model="filter"
                name="elections-filter"
              />
              <span class="text-sm font-medium text-gray-700">Show All</span>
            </label>

            <label class="inline-flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                class="size-4 text-indigo-600 focus:ring-2"
                value="active"
                v-model="filter"
                name="elections-filter"
              />
              <span class="text-sm font-medium text-gray-700">Active</span>
            </label>

            <label class="inline-flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                class="size-4 text-indigo-600 focus:ring-2"
                value="archive"
                v-model="filter"
                name="elections-filter"
              />
              <span class="text-sm font-medium text-gray-700">Archive</span>
            </label>

            <label class="inline-flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                class="size-4 text-indigo-600 focus:ring-2"
                value="upcoming"
                v-model="filter"
                name="elections-filter"
              />
              <span class="text-sm font-medium text-gray-700">Upcoming</span>
            </label>
          </div>
        </div>

        <div
          class="flex-1 bg-gray-100 rounded-3xl border border-gray-100 shadow-xl p-6"
        >
          <div class="flex flex-wrap items-center gap-6">
            <label for="from" class="text-sm text-gray-600">From</label>
            <input
              id="from"
              type="date"
              v-model="dateFrom"
              class="rounded-md border-gray-300 text-sm focus:border-indigo-500 focus:ring-indigo-500"
            />

            <label for="to" class="text-sm text-gray-600">To</label>
            <input
              id="to"
              type="date"
              v-model="dateTo"
              class="rounded-md border-gray-300 text-sm focus:border-indigo-500 focus:ring-indigo-500"
            />
          </div>
        </div>

        <button
          @click="
            dateFrom = '';
            dateTo = '';
            filter = 'all';
          "
          class="inline-flex items-center gap-2 bg-indigo-700 px-4 py-2 text-sm font-medium text-white rounded-3xl shadow-2xl p-6"
        >
          <Icon icon="mdi:close" class="w-4 h-4" />
          <span>Clear Filters</span>
        </button>
      </div>

      <!-- States -->
      <div v-if="loading" class="text-gray-600">Loading…</div>
      <div v-else-if="error" class="text-red-600">Error: {{ error }}</div>
      <div v-else-if="elections.length === 0" class="text-gray-500">
        No elections for this filter.
      </div>

      <!-- List of votings -->
      <div v-else class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 mb-4">
        <article
          v-for="el in elections"
          :key="el.id"
          class="bg-gray-100 rounded-3xl border border-gray-100 shadow-2xl p-6 hover:shadow-md hover:-translate-y-0.5 transition flex flex-col justify-between"
        >
          <div>
            <h2 class="text-xl font-semibold text-gray-900">{{ el.name }}</h2>
            <p class="text-gray-600 mt-2 line-clamp-3">{{ el.description }}</p>

            <div
              class="mt-4 flex flex-wrap items-center gap-3 text-sm text-gray-600"
            >
              <span
                class="inline-flex items-center gap-1 rounded-full bg-gray-50 px-2 py-1 ring-1 ring-inset ring-gray-200"
              >
                <Icon icon="mdi:calendar-start" class="w-4 h-4" />
                {{ fmt(el.start_date) }}
              </span>
              <span
                class="inline-flex items-center gap-1 rounded-full bg-gray-50 px-2 py-1 ring-1 ring-inset ring-gray-200"
              >
                <Icon icon="mdi:calendar-end" class="w-4 h-4" />
                {{ fmt(el.end_date) }}
              </span>

              <span
                class="ml-auto inline-flex items-center gap-1"
                :class="
                  el.status === 'active'
                    ? 'text-green-700'
                    : el.status === 'archive'
                    ? 'text-gray-600'
                    : 'text-indigo-700'
                "
              >
                <Icon
                  :icon="
                    el.status === 'active'
                      ? 'mdi:check-circle'
                      : el.status === 'archive'
                      ? 'mdi:archive'
                      : 'mdi:clock-outline'
                  "
                  class="w-4 h-4"
                />
                {{
                  el.status === "active"
                    ? "Active"
                    : el.status === "archive"
                    ? "Archive"
                    : "Upcoming"
                }}
              </span>
            </div>
          </div>

          <template v-if="el.status === 'upcoming'">
            <span
              class="mt-4 inline-flex items-center gap-2 text-gray-500 font-medium self-start"
            >
              Scheduled
              <Icon icon="mdi:calendar" class="w-4 h-4" />
            </span>
          </template>
          <RouterLink
            v-else
            :to="
              el.status === 'archive'
                ? `/elections/${el.id}/results`
                : `/elections/${el.id}/verify`
            "
            class="mt-4 inline-flex items-center gap-2 text-indigo-700 hover:text-indigo-800 font-medium self-start"
          >
            {{ el.status === "archive" ? "See results" : "Take part" }}
            <Icon icon="mdi:chevron-right" class="w-4 h-4" />
          </RouterLink>
        </article>
      </div>
    </div>
  </div>
</template>
