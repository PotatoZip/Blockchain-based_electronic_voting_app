<template>
  <div class="mx-auto">
    <ul class="space-y-3">
      <li v-for="item in questions" :key="item.question">
        <details
          class="group rounded-xl border border-gray-200 bg-white p-4 shadow-md"
        >
          <summary
            class="flex cursor-pointer list-none items-center justify-between gap-4"
          >
            <span class="font-medium text-gray-900">{{ item.question }}</span>
            <Icon
              icon="mdi:chevron-down"
              class="h-5 w-5 text-gray-500 transition-transform group-open:rotate-180"
            />
          </summary>
          <div class="mt-2 text-gray-600 leading-relaxed">
            {{ item.answer }}
          </div>
        </details>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";

type Question = { question: string; answer: string };
const questions: Question[] = [
  { question: "How to enrol for voting?", answer: "fuebvowene" },
  { question: "How to enrol for voting?", answer: "fuebvowene" },
  { question: "How to enrol for voting?", answer: "fuebvowene" },
  { question: "How to enrol for voting?", answer: "fuebvowene" },
  { question: "How to enrol for voting?", answer: "fuebvowene" },
];
</script>
