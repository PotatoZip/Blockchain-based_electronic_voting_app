<template>
  <div>
    <div class="mx-auto max-w-5xl">
      <div
        class="mt-10 font-bold text-8xl text-indigo-600 text-center flex flex-col items-center gap-2"
      >
        <span>Welcome to</span>
        <span>EtherVote</span>
      </div>
      <div class="mt-10 grid gap-4">
        <div
          class="bg-gray-100 rounded-3xl border border-gray-100 shadow-2xl p-6"
        >
          <div class="text-indigo-600 flex items-center gap-2 mb-2">
            <Icon icon="fa-solid:vote-yea" width="24" height="24" />
            <h1 class="text-2xl font-semibold">Comfortable online voting</h1>
          </div>
          <p>
            Vote fast using our web application. It offers a wide range of
            voting options. Keep your vote secure with blockchain technology.
          </p>
        </div>
        <div
          class="bg-gray-100 rounded-3xl border border-gray-100 shadow-2xl p-6 mb-4"
        >
          <div class="text-indigo-600 flex items-center gap-2 mb-4">
            <Icon icon="fa:gears" width="24" height="24" />
            <h1 class="text-2xl font-semibold">How to use it</h1>
          </div>
          <p class="mb-4 text-gray-700">Just follow this simple instruction:</p>
          <ol class="list-decimal list-inside space-y-2 text-gray-700">
            <li>
              Check your email for the
              <span class="font-semibold text-indigo-600"
                >verification code</span
              >
            </li>
            <li>
              Go to
              <span class="font-semibold text-indigo-600">Votings</span> page
              and use filtering options to find your voting
            </li>
            <li>
              Choose it and verify your identity with your
              <span class="font-semibold text-indigo-600">PESEL</span> number
              and
              <span class="font-semibold text-indigo-600">code</span> provided
              in email message
            </li>
            <li>Take part in voting by casting your vote</li>
            <li>Wait for the results to be published after voting ends</li>
          </ol>
          <p class="mt-4 text-gray-700">
            In case of any problems or questions visit
            <span class="font-semibold text-indigo-600">About</span> page for
            more information. We will be happy to help you.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";
</script>
