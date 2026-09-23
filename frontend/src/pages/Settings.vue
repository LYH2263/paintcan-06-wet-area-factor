<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'
const s = ref({})
const factor = ref('1')
const msg = ref('')
const err = ref('')
onMounted(async () => {
  s.value = await getJSON('/api/settings')
  factor.value = s.value.damp_factor ?? '1'
})
const save = async () => {
  msg.value = ''; err.value = ''
  const v = parseFloat(factor.value)
  if (Number.isNaN(v)) { err.value = '请输入数字'; return }
  try {
    s.value = await putJSON('/api/settings/damp_factor', { value: String(v) })
    factor.value = s.value.damp_factor
    msg.value = '已保存（历史记录中的钉选系数不受影响）'
  } catch (e) { err.value = e.message }
}
</script>
<template><div class="page"><h1>设置</h1>
<p><label>默认潮湿系数 <input v-model="factor" style="width:6rem" /></label>
<button @click="save">保存</button> <span>{{ msg }}</span></p>
<p v-if="err" class="err">{{ err }}</p>
<p class="hint">潮湿区房间的墙面净面积先乘该系数再按涂布率换升数；缺省为 1。系数 ≤ 0 时估漆整单拒绝且不写记录。</p>
<p class="hint">每升可刷 {{ s.coverage }} m² · 默认 {{ s.coats }} 遍</p>
</div></template>
