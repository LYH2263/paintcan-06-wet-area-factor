<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const cur = ref(null)
onMounted(async () => { items.value = (await getJSON('/api/history')).items })
const open = async (id) => { cur.value = await getJSON(`/api/history/${id}`) }
</script>
<template><div class="page"><h1>估算记录</h1>
<table><tr v-for="h in items" :key="h.id"><td>#{{ h.id }}</td><td>{{ h.created_at }}</td>
<td><button @click="open(h.id)">查看</button></td></tr></table>
<div v-if="cur" class="run-detail"><h2>记录 #{{ cur.id }}</h2>
<p>潮湿区 {{ cur.result.damp ? '是' : '否' }} · 钉选系数 {{ cur.result.damp_factor ?? '—' }} · 折算净面积 {{ cur.result.adj_net_m2 ?? '—' }} m² · 升数 {{ cur.result.liters }} L</p>
</div></div></template>
