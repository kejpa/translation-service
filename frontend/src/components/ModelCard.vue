<script setup>
import {ref} from 'vue'
import {installModel} from "@/services/llmService.js";

const props = defineProps({
  model: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['installed',])

const installing = ref(false)
const message = ref('')

async function install() {
  installing.value = true
  message.value = ''

  try {
    const result = await installModel()

    if (result.success) {
      message.value = '✅ Model installed successfully'

      emit('installed')
    } else {
      if (result.message.includes('file does not exist',)) {
        message.value =
          `❌ The model "${result.model}" could not be found.`
      } else {
        message.value = result.message
      }

    }
  } catch {
    message.value = '❌ Unable to install model'
  } finally {
    installing.value = false
  }
}
</script>
<template>
  <section class="card">
    <h2>Model Setup</h2>

    <div class="row">
      <span>Configured Model</span>
      <span>{{ model }}</span>
    </div>
    <div class="row">
      <span>Status</span>
      <span>❌ Not Installed</span>
    </div>

    <p
      v-if="message"
      class="message"
    >
      {{ message }}
    </p>

    <button
      :disabled="installing"
      @click="install"
    >
      {{ installing ? `Installing ${model}...` : 'Install Model' }}
    </button>
    <p v-if="installing">Downloading model...<br>
      This may take up to 5 minutes depending on model size.
    </p>
  </section>
</template>


<style scoped>
h2 {
  margin-bottom: 1rem;
  font-size: 1rem;
}

.card {
  padding: 1rem;
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  background: var(--color-surface);
}

.card h2 {
  font-size: 1rem;
  font-weight: 600;

  padding-bottom: 0.5rem;
  margin-bottom: 0.5rem;

  border-bottom: 1px solid var(--color-border);
}

.row {
  display: grid;
  grid-template-columns: 250px 1fr;

  padding: 0.4rem 0.6rem;
}

.row:nth-child(even) {
  background: var(--color-surface-alternating);
}
</style>
