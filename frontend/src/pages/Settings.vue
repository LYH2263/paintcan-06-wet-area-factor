<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'
const s = ref({})
const wetFactor = ref(1)
const msg = ref('')
const err = ref('')
onMounted(async () => {
  s.value = await getJSON('/api/settings')
  wetFactor.value = s.value.wet_factor ?? 1
})
const save = async () => {
  msg.value = ''; err.value = ''
  const v = Number(wetFactor.value)
  if (!Number.isFinite(v) || v <= 0) { err.value = '潮湿系数必须为正数'; return }
  try {
    await putJSON('/api/settings', { key: 'wet_factor', value: String(v) })
    s.value = await getJSON('/api/settings')
    msg.value = '已保存（仅影响新估算，历史记录不变）'
  } catch (e) { err.value = '保存失败：' + e.message }
}
</script>
<template><div class="page"><h1>设置</h1>
<div class="setting-row">
  <label>默认潮湿系数 <input v-model.number="wetFactor" type="number" step="0.01" min="0.01" /></label>
  <button @click="save">保存</button>
</div>
<p v-if="msg" class="ok">{{ msg }}</p>
<p v-if="err" class="err">{{ err }}</p>
<p class="hint">潮湿区房间按「净面积 × 系数」折算后再换算升数；系数 ≤ 0 的估算将被整单拒绝。</p>
<details><summary>全部设置</summary><pre>{{ s }}</pre></details>
</div></template>
