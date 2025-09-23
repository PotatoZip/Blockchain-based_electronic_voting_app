<template>
  <div>
    <div class="mx-auto max-w-5xl mt-20">
      <div class="grid gap-6 sm:grid-cols-2">
        <div
          class="bg-white rounded-3xl shadow border border-gray-100 shadow-sm p-6"
        >
          <div class="flex items-center gap-2 mb-2 text-indigo-600">
            <Icon icon="grommet-icons:contact" width="24" height="24" />
            <h1 class="text-2xl font-semibold">How to reach us?</h1>
          </div>
          <p>
            You can feel free to contact us via mail:
            <a
              href="mailto:ethervote@gmail.com"
              class="text-indigo-600 font-semibold underline hover:text-indigo-800"
              >ethervote@gmail.com</a
            >
          </p>
          <p>
            If you have any questions or you need our technical support feel
            free to reach us and we will make our best to satisfy your needs.
          </p>
        </div>
        <div
          class="bg-white rounded-3xl shadow border border-gray-100 shadow-sm p-6"
        >
          <div class="flex items-center gap-2 mb-2 text-indigo-600">
            <Icon icon="fluent:person-24-filled" width="24" height="24" />
            <h1 class="text-2xl font-semibold">Purpose & Author</h1>
          </div>
          <p>
            This application was developed by <b>Wiktor Zmiendak</b> as part of
            engineering thesis during Computer Science studies at the
            <b>Cracow University of Technology</b>. It solved my never-ending
            problem of organizing events for myself and my friends and it also
            helped me to understand blockchain fundaments.
          </p>
        </div>
      </div>
      <div class="mt-8 grid gap-4">
        <div class="bg-white rounded-3xl shadow border border-gray-100 p-6">
          <div class="flex items-center gap-2 mb-2 text-indigo-600">
            <Icon
              icon="streamline-ultimate:contact-us-faq"
              width="24"
              height="24"
            />
            <h1 class="text-2xl font-semibold">Most common questions</h1>
          </div>
          <QuestionsList />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";
import QuestionsList from "../components/QuestionsList.vue";
</script>
