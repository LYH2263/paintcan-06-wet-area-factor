<script setup>
import { ref } from 'vue'
import { postJSON } from '../api'
const room_id = ref(1)
const out = ref(null)
const err = ref('')
const run = async () => {
  err.value = ''
  try {
    out.value = await postJSON('/api/estimate', { room_id: room_id.value, persist: true })
  } catch (e) {
    out.value = null
    err.value = '估算被拒绝：' + e.message
  }
}
</script>
<template><div class="page"><h1>估漆工作台</h1>
<label>房间ID <input v-model.number="room_id" /></label>
<button @click="run">估算</button>
<p v-if="out">
  原净 {{ out.net_m2 }} m²
  <template v-if="out.wet">· 潮湿 ×{{ out.wet_factor }} · 折算净 {{ out.effective_m2 }} m²</template>
  · <span class="hero-num">{{ out.liters }} 升</span> · {{ out.coats }} 遍
  <span v-if="out.run_id"> · 记录 #{{ out.run_id }}</span>
</p>
<p v-if="err" class="err">{{ err }}</p>
</div></template>
