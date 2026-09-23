<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getJSON, patchJSON, postJSON } from '../api'
const route = useRoute()
const detail = ref(null)
const est = ref(null)
const err = ref('')
const load = async () => {
  err.value = ''
  detail.value = await getJSON(`/api/rooms/${route.params.id}`)
  est.value = await postJSON('/api/estimate', { room_id: +route.params.id, persist: false })
}
const toggleWet = async () => {
  err.value = ''
  try {
    const next = !detail.value.room.wet
    const r = await patchJSON(`/api/rooms/${route.params.id}/wet`, { wet: next })
    detail.value.room = r.room
    est.value = await postJSON('/api/estimate', { room_id: +route.params.id, persist: false })
  } catch (e) { err.value = '切换失败：' + e.message }
}
onMounted(load); watch(() => route.params.id, load)
</script>
<template><div class="page" v-if="detail"><h1>{{ detail.room.name }}</h1>
<p>
  <label class="wet-toggle"><input type="checkbox" :checked="!!detail.room.wet" @change="toggleWet" /> 潮湿区</label>
</p>
<p v-if="est">
  原净面积 {{ est.net_m2 }} m²
  <template v-if="est.wet">· 潮湿系数 ×{{ est.wet_factor }} · 折算净面积 {{ est.effective_m2 }} m²</template>
  · 需漆 <span class="hero-num">{{ est.liters }} L</span>
</p>
<p v-if="err" class="err">{{ err }}</p>
<ul><li v-for="o in detail.openings" :key="o.id">{{ o.kind }} {{ o.w }}×{{ o.h }}</li></ul>
</div></template>
