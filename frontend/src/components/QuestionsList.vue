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
  {
    question: "How to enrol for voting?",
    answer:
      "You can't enrol for voting. If you should be able to participate in the vote, your organization will certainly ask us to register you.",
  },
  {
    question: "How will I know If I am enroled?",
    answer:
      "If the voting is visible on our website then you should have received an email with voting access codes",
  },
  {
    question: "What if I can't see mail message?",
    answer:
      "If you don't recieved mail for us or you just simply lost it then feel free to contact us via email message",
  },
  {
    question: "Can I propose next voting?",
    answer:
      "Of course! Let us know about it in mail message and will be glad to happy to prepare it for you",
  },
];
</script>
