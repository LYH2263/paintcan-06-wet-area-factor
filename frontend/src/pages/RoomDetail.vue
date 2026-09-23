<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getJSON, postJSON, putJSON } from '../api'
const route = useRoute()
const detail = ref(null)
const est = ref(null)
const err = ref('')
const load = async () => {
  err.value = ''
  detail.value = await getJSON(`/api/rooms/${route.params.id}`)
  try {
    est.value = await postJSON('/api/estimate', { room_id: +route.params.id, persist: false })
  } catch (e) { est.value = null; err.value = `估算被拒绝：${e.message}` }
}
const toggleDamp = async () => {
  await putJSON(`/api/rooms/${route.params.id}/damp`, { damp: !detail.value.room.damp })
  await load()
}
onMounted(load); watch(() => route.params.id, load)
</script>
<template><div class="page" v-if="detail"><h1>{{ detail.room.name }} <span v-if="detail.room.damp" class="tag">潮湿区</span></h1>
<label><input type="checkbox" :checked="!!detail.room.damp" @change="toggleDamp" /> 潮湿区（净面积乘潮湿系数）</label>
<p v-if="est">净面积 {{ est.net_m2 }} m²<template v-if="est.damp"> · 折算 {{ est.adj_net_m2 }} m²（系数 {{ est.damp_factor }}）</template> · 需漆 <span class="hero-num">{{ est.liters }} L</span></p>
<p v-if="err" class="err">{{ err }}</p>
<ul><li v-for="o in detail.openings" :key="o.id">{{ o.kind }} {{ o.w }}×{{ o.h }}</li></ul>
</div></template>
