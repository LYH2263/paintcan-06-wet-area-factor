<script setup>
import { ref } from 'vue'
import { postJSON } from '../api'
const room_id = ref(1)
const out = ref(null)
const err = ref('')
const run = async () => {
  out.value = null; err.value = ''
  try { out.value = await postJSON('/api/estimate', { room_id: room_id.value, persist: true }) }
  catch (e) { err.value = `估算被拒绝：${e.message}` }
}
</script>
<template><div class="page"><h1>估漆工作台</h1>
<label>房间ID <input v-model.number="room_id" /></label>
<button @click="run">估算</button>
<template v-if="out">
<p>净 {{ out.net_m2 }} m² · 折算 {{ out.adj_net_m2 }} m² · <span class="hero-num">{{ out.liters }} 升</span> · {{ out.coats }} 遍</p>
<p v-if="out.damp">潮湿区 · 系数 {{ out.damp_factor }}<span v-if="out.run_id"> · 已钉入记录 #{{ out.run_id }}</span></p>
</template>
<p v-if="err" class="err">{{ err }}</p></div></template>
