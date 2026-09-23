<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const detail = ref(null)
const err = ref('')
onMounted(async () => { items.value = (await getJSON('/api/history')).items })
const open = async (id) => {
  detail.value = null; err.value = ''
  try { detail.value = await getJSON(`/api/history/${id}`) }
  catch (e) { err.value = '读取失败：' + e.message }
}
</script>
<template><div class="page"><h1>估算记录</h1>
<table><tr v-for="h in items" :key="h.id">
  <td><a href="#" @click.prevent="open(h.id)">#{{ h.id }}</a></td>
  <td>{{ h.created_at }}</td>
</tr></table>
<p v-if="err" class="err">{{ err }}</p>
<div v-if="detail" class="run-detail">
  <h2>记录 #{{ detail.id }}</h2>
  <p>房间 {{ detail.input.room_id }} · {{ detail.result.coats }} 遍 · 涂布率 {{ detail.result.coverage }}</p>
  <p>潮湿区：{{ detail.input.wet ? '是' : '否' }}
     <template v-if="detail.input.wet"> · 钉选系数 ×{{ detail.input.wet_factor }}</template></p>
  <p>净面积 {{ detail.result.net_m2 }} m²
     <template v-if="detail.result.wet"> · 折算净面积 {{ detail.result.effective_m2 }} m²</template>
     · 升数 <span class="hero-num">{{ detail.result.liters }} L</span></p>
</div>
</div></template>
