<!-- frontend/src/views/DataInput.vue -->
<template>
  <div class="data-input-container">
    <el-card class="main-card">
      <template #header>
        <div class="card-header">
          <h2>医疗数据资产价值评估表</h2>
          <p>请根据实际情况填写以下9大类成本指标数据（单位：元）</p>
        </div>
      </template>

      <el-form
        ref="dataFormRef"
        :model="formData"
        label-position="top"
        class="data-form"
      >
        <!-- 评估基本信息 -->
        <el-card class="section-card">
          <template #header>
            <div class="section-header">
              <span class="section-number">基本信息</span>
              <h3>评估基本信息</h3>
            </div>
          </template>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="评估名称" required>
                <el-input
                  v-model="formData.evaluationName"
                  placeholder="请输入本次评估的名称"
                  size="large"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="评估描述">
                <el-input
                  v-model="formData.description"
                  placeholder="请输入评估描述（可选）"
                  size="large"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </el-card>

        <!-- 9大类成本指标 -->
        <el-collapse v-model="activeCollapse" accordion>
          <!-- 第1类：数据战略与治理成本 -->
          <el-collapse-item name="1">
            <template #title>
              <div class="collapse-header">
                <span class="collapse-number">1</span>
                <h3>数据战略与治理成本</h3>
                <span class="collapse-total">{{ formatCurrency(calculateCategoryTotal(1)) }}</span>
              </div>
            </template>
            
            <div class="collapse-content">
              <el-row :gutter="20">
                <el-col 
                  :span="12" 
                  v-for="item in category1Items" 
                  :key="item.key"
                >
                  <el-form-item 
                    :label="item.label" 
                    class="indicator-item"
                  >
                    <el-input-number
                      v-model="formData.category1[item.key]"
                      :controls="false"
                      :min="0"
                      :precision="2"
                      :step="1000"
                      placeholder="0.00"
                      style="width: 100%"
                    >
                      <template #append>元</template>
                    </el-input-number>
                    <div class="item-description">{{ item.description }}</div>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-collapse-item>

          <!-- 第2类：数据获取与采集成本 -->
          <el-collapse-item name="2">
            <template #title>
              <div class="collapse-header">
                <span class="collapse-number">2</span>
                <h3>数据获取与采集成本</h3>
                <span class="collapse-total">{{ formatCurrency(calculateCategoryTotal(2)) }}</span>
              </div>
            </template>
            
            <div class="collapse-content">
              <el-row :gutter="20">
                <el-col 
                  :span="12" 
                  v-for="item in category2Items" 
                  :key="item.key"
                >
                  <el-form-item 
                    :label="item.label" 
                    class="indicator-item"
                  >
                    <el-input-number
                      v-model="formData.category2[item.key]"
                      :controls="false"
                      :min="0"
                      :precision="2"
                      :step="1000"
                      placeholder="0.00"
                      style="width: 100%"
                    >
                      <template #append>元</template>
                    </el-input-number>
                    <div class="item-description">{{ item.description }}</div>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-collapse-item>

          <!-- 第3类：数据存储与备份成本 -->
          <el-collapse-item name="3">
            <template #title>
              <div class="collapse-header">
                <span class="collapse-number">3</span>
                <h3>数据存储与备份成本</h3>
                <span class="collapse-total">{{ formatCurrency(calculateCategoryTotal(3)) }}</span>
              </div>
            </template>
            
            <div class="collapse-content">
              <el-row :gutter="20">
                <el-col 
                  :span="12" 
                  v-for="item in category3Items" 
                  :key="item.key"
                >
                  <el-form-item 
                    :label="item.label" 
                    class="indicator-item"
                  >
                    <el-input-number
                      v-model="formData.category3[item.key]"
                      :controls="false"
                      :min="0"
                      :precision="2"
                      :step="1000"
                      placeholder="0.00"
                      style="width: 100%"
                    >
                      <template #append>元</template>
                    </el-input-number>
                    <div class="item-description">{{ item.description }}</div>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-collapse-item>

          <!-- 第4类：数据处理与加工成本 -->
          <el-collapse-item name="4">
            <template #title>
              <div class="collapse-header">
                <span class="collapse-number">4</span>
                <h3>数据处理与加工成本</h3>
                <span class="collapse-total">{{ formatCurrency(calculateCategoryTotal(4)) }}</span>
              </div>
            </template>
            
            <div class="collapse-content">
              <el-row :gutter="20">
                <el-col 
                  :span="12" 
                  v-for="item in category4Items" 
                  :key="item.key"
                >
                  <el-form-item 
                    :label="item.label" 
                    class="indicator-item"
                  >
                    <el-input-number
                      v-model="formData.category4[item.key]"
                      :controls="false"
                      :min="0"
                      :precision="2"
                      :step="1000"
                      placeholder="0.00"
                      style="width: 100%"
                    >
                      <template #append>元</template>
                    </el-input-number>
                    <div class="item-description">{{ item.description }}</div>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-collapse-item>

          <!-- 第5类：数据应用与分析成本 -->
          <el-collapse-item name="5">
            <template #title>
              <div class="collapse-header">
                <span class="collapse-number">5</span>
                <h3>数据应用与分析成本</h3>
                <span class="collapse-total">{{ formatCurrency(calculateCategoryTotal(5)) }}</span>
              </div>
            </template>
            
            <div class="collapse-content">
              <el-row :gutter="20">
                <el-col 
                  :span="12" 
                  v-for="item in category5Items" 
                  :key="item.key"
                >
                  <el-form-item 
                    :label="item.label" 
                    class="indicator-item"
                  >
                    <el-input-number
                      v-model="formData.category5[item.key]"
                      :controls="false"
                      :min="0"
                      :precision="2"
                      :step="1000"
                      placeholder="0.00"
                      style="width: 100%"
                    >
                      <template #append>元</template>
                    </el-input-number>
                    <div class="item-description">{{ item.description }}</div>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-collapse-item>

          <!-- 第6类：数据流通与共享成本 -->
          <el-collapse-item name="6">
            <template #title>
              <div class="collapse-header">
                <span class="collapse-number">6</span>
                <h3>数据流通与共享成本</h3>
                <span class="collapse-total">{{ formatCurrency(calculateCategoryTotal(6)) }}</span>
              </div>
            </template>
            
            <div class="collapse-content">
              <el-row :gutter="20">
                <el-col 
                  :span="12" 
                  v-for="item in category6Items" 
                  :key="item.key"
                >
                  <el-form-item 
                    :label="item.label" 
                    class="indicator-item"
                  >
                    <el-input-number
                      v-model="formData.category6[item.key]"
                      :controls="false"
                      :min="0"
                      :precision="2"
                      :step="1000"
                      placeholder="0.00"
                      style="width: 100%"
                    >
                      <template #append>元</template>
                    </el-input-number>
                    <div class="item-description">{{ item.description }}</div>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-collapse-item>

          <!-- 第7类：数据安全、隐私与合规成本 -->
          <el-collapse-item name="7">
            <template #title>
              <div class="collapse-header">
                <span class="collapse-number">7</span>
                <h3>数据安全、隐私与合规成本</h3>
                <span class="collapse-total">{{ formatCurrency(calculateCategoryTotal(7)) }}</span>
              </div>
            </template>
            
            <div class="collapse-content">
              <el-row :gutter="20">
                <el-col 
                  :span="12" 
                  v-for="item in category7Items" 
                  :key="item.key"
                >
                  <el-form-item 
                    :label="item.label" 
                    class="indicator-item"
                  >
                    <el-input-number
                      v-model="formData.category7[item.key]"
                      :controls="false"
                      :min="0"
                      :precision="2"
                      :step="1000"
                      placeholder="0.00"
                      style="width: 100%"
                    >
                      <template #append>元</template>
                    </el-input-number>
                    <div class="item-description">{{ item.description }}</div>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-collapse-item>

          <!-- 第8类：数据归档与销毁成本 -->
          <el-collapse-item name="8">
            <template #title>
              <div class="collapse-header">
                <span class="collapse-number">8</span>
                <h3>数据归档与销毁成本</h3>
                <span class="collapse-total">{{ formatCurrency(calculateCategoryTotal(8)) }}</span>
              </div>
            </template>
            
            <div class="collapse-content">
              <el-row :gutter="20">
                <el-col 
                  :span="12" 
                  v-for="item in category8Items" 
                  :key="item.key"
                >
                  <el-form-item 
                    :label="item.label" 
                    class="indicator-item"
                  >
                    <el-input-number
                      v-model="formData.category8[item.key]"
                      :controls="false"
                      :min="0"
                      :precision="2"
                      :step="1000"
                      placeholder="0.00"
                      style="width: 100%"
                    >
                      <template #append>元</template>
                    </el-input-number>
                    <div class="item-description">{{ item.description }}</div>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-collapse-item>

          <!-- 第9类：数据全流程人力成本 -->
          <el-collapse-item name="9">
            <template #title>
              <div class="collapse-header">
                <span class="collapse-number">9</span>
                <h3>数据全流程人力成本</h3>
                <span class="collapse-total">{{ formatCurrency(calculateCategoryTotal(9)) }}</span>
              </div>
            </template>
            
            <div class="collapse-content">
              <el-row :gutter="20">
                <el-col 
                  :span="12" 
                  v-for="item in category9Items" 
                  :key="item.key"
                >
                  <el-form-item 
                    :label="item.label" 
                    class="indicator-item"
                  >
                    <el-input-number
                      v-model="formData.category9[item.key]"
                      :controls="false"
                      :min="0"
                      :precision="2"
                      :step="1000"
                      placeholder="0.00"
                      style="width: 100%"
                    >
                      <template #append>元</template>
                    </el-input-number>
                    <div class="item-description">{{ item.description }}</div>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-collapse-item>
        </el-collapse>

        <!-- 总计显示 -->
        <el-card class="total-card">
          <div class="total-content">
            <div class="total-item">
              <span class="total-label">总估值：</span>
              <span class="total-value">{{ formatCurrency(calculateTotal()) }}</span>
            </div>
            <div class="total-breakdown">
              <div 
                v-for="category in categories" 
                :key="category.id" 
                class="category-total"
              >
                <span>{{ category.name }}：</span>
                <span>{{ formatCurrency(calculateCategoryTotal(category.id)) }}</span>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 操作按钮 -->
        <div class="form-actions">
          <el-button 
            type="info" 
            :loading="savingDraft"
            @click="saveAsDraft"
            :disabled="!hasChanges"
          >
            {{ savingDraft ? '保存中...' : '保存草稿' }}
          </el-button>
          
          <el-button 
            type="primary" 
            :loading="submitting"
            @click="submitForm"
            :disabled="!isFormValid"
          >
            {{ submitting ? '提交中...' : '提交评估' }}
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { createEvaluationAPI } from '@/api/evaluation'
import { ElMessage } from 'element-plus'

const router = useRouter()
const dataFormRef = ref()

// 9大类指标定义（基于文档1）- 内联定义
const categories = [
  { id: 1, name: '数据战略与治理成本' },
  { id: 2, name: '数据获取与采集成本' },
  { id: 3, name: '数据存储与备份成本' },
  { id: 4, name: '数据处理与加工成本' },
  { id: 5, name: '数据应用与分析成本' },
  { id: 6, name: '数据流通与共享成本' },
  { id: 7, name: '数据安全、隐私与合规成本' },
  { id: 8, name: '数据归档与销毁成本' },
  { id: 9, name: '数据全流程人力成本' }
]

// 第1类指标项
const category1Items = [
  { 
    key: 'strategicPlanning', 
    label: '战略规划成本', 
    description: '制定数据战略、路线图的咨询费用' 
  },
  { 
    key: 'governanceSystem', 
    label: '治理体系建设成本', 
    description: '建立数据标准、管理规范、组织架构的成本；DCMM、DAMA等认证费用' 
  },
  { 
    key: 'metadataMaster', 
    label: '元数据与主数据管理成本', 
    description: '相关工具采购、开发及维护费用' 
  }
]

// 第2类指标项
const category2Items = [
  { 
    key: 'hardwareCollection', 
    label: '采集硬件成本', 
    description: '大型设备软件、生命支持类设备、爬虫服务器等采购成本' 
  },
  { 
    key: 'softwareCollection', 
    label: '采集软件/工具成本', 
    description: '数据抽取工具、录入系统、API接口等费用' 
  },
  { 
    key: 'dataPurchase', 
    label: '数据购买成本', 
    description: '向第三方采购数据集的费用、外部数据订阅费用' 
  }
]

// 第3类指标项
const category3Items = [
  { 
    key: 'storageHardware', 
    label: '存储硬件成本', 
    description: '服务器、磁盘阵列、磁带库的购置与运维费用' 
  },
  { 
    key: 'storageSoftware', 
    label: '存储软件成本', 
    description: '数据库、文件系统软件的授权与订阅费' 
  },
  { 
    key: 'cloudStorage', 
    label: '云存储服务费', 
    description: '对象存储、块存储的按量或包年费用' 
  },
  { 
    key: 'backupDisaster', 
    label: '备份与容灾成本', 
    description: '备份软件、异地灾备中心的建设与维护' 
  }
]

// 第4类指标项
const category4Items = [
  { 
    key: 'dataCleaning', 
    label: '数据清洗与标准化成本', 
    description: '数据质量检查、清洗、标准化处理的人工和工具费用' 
  },
  { 
    key: 'dataIntegration', 
    label: '数据集成与融合成本', 
    description: '多源异构数据集成、数据仓库/湖建设成本' 
  },
  { 
    key: 'dataModeling', 
    label: '数据建模成本', 
    description: '数据模型设计、开发、维护费用' 
  },
  { 
    key: 'dataProcessing', 
    label: '数据处理平台成本', 
    description: 'ETL/ELT工具、流处理平台的购置与开发费用' 
  }
]

// 第5类指标项
const category5Items = [
  { 
    key: 'businessApplication', 
    label: '业务应用开发成本', 
    description: '基于数据的业务应用系统开发费用' 
  },
  { 
    key: 'analyticsModeling', 
    label: '分析建模成本', 
    description: '统计分析、机器学习模型研发与训练成本' 
  },
  { 
    key: 'visualization', 
    label: '可视化与报表成本', 
    description: 'BI工具、报表系统、可视化大屏开发费用' 
  },
  { 
    key: 'applicationMaintenance', 
    label: '应用维护成本', 
    description: '现有数据应用的运维、更新、优化费用' 
  }
]

// 第6类指标项
const category6Items = [
  { 
    key: 'dataExchange', 
    label: '数据交换平台成本', 
    description: '院内/院间数据交换平台建设与维护' 
  },
  { 
    key: 'dataSharing', 
    label: '数据共享服务成本', 
    description: 'API网关、数据服务化平台建设费用' 
  },
  { 
    key: 'externalCooperation', 
    label: '外部合作成本', 
    description: '与外部机构数据合作的技术对接、管理费用' 
  },
  { 
    key: 'dataMarket', 
    label: '数据市场成本', 
    description: '参与数据要素市场的平台接入、运营费用' 
  }
]

// 第7类指标项
const category7Items = [
  { 
    key: 'securityHardware', 
    label: '安全硬件成本', 
    description: '防火墙、入侵检测、加密设备等安全硬件' 
  },
  { 
    key: 'securitySoftware', 
    label: '安全软件成本', 
    description: '防病毒、漏洞扫描、数据脱敏等安全软件' 
  },
  { 
    key: 'securityAudit', 
    label: '安全审计成本', 
    description: '等保测评、风险评估、合规审计费用' 
  },
  { 
    key: 'privacyProtection', 
    label: '隐私保护成本', 
    description: '匿名化、去标识化、知情同意管理成本' 
  },
  { 
    key: 'complianceCertification', 
    label: '合规认证成本', 
    description: 'ISO27001、GDPR、HIPAA等认证费用' 
  }
]

// 第8类指标项
const category8Items = [
  { 
    key: 'archivingSystem', 
    label: '归档系统成本', 
    description: '长期数据归档系统的软硬件投入' 
  },
  { 
    key: 'dataDestruction', 
    label: '数据销毁成本', 
    description: '安全数据擦除、介质销毁服务费用' 
  },
  { 
    key: 'lifecycleManagement', 
    label: '生命周期管理成本', 
    description: '数据生命周期管理工具、策略制定费用' 
  },
  { 
    key: 'complianceArchiving', 
    label: '合规归档成本', 
    description: '满足法规要求的长期数据保存成本' 
  }
]

// 第9类指标项
const category9Items = [
  { 
    key: 'strategyGovernance', 
    label: '战略与治理人力成本', 
    description: 'CDO、数据治理专家、规划人员薪资福利' 
  },
  { 
    key: 'technicalOperations', 
    label: '技术运营人力成本', 
    description: '数据库管理员、数据分析师、开发工程师薪资' 
  },
  { 
    key: 'qualitySecurity', 
    label: '质量与安全人力成本', 
    description: '数据质量管理、安全运维、合规专员薪资' 
  },
  { 
    key: 'dataAnalysis', 
    label: '数据分析人力成本', 
    description: '数据科学家、业务分析师、可视化专家薪资' 
  },
  { 
    key: 'externalConsulting', 
    label: '外部咨询人力成本', 
    description: '第三方咨询、培训、技术支持费用' 
  }
]

// 状态
const activeCollapse = ref(['1'])
const savingDraft = ref(false)
const submitting = ref(false)

// 表单数据
const formData = reactive({
  evaluationName: '',
  description: '',
  
  // 第1类：数据战略与治理成本
  category1: {
    strategicPlanning: 0,
    governanceSystem: 0,
    metadataMaster: 0
  },
  
  // 第2类：数据获取与采集成本
  category2: {
    hardwareCollection: 0,
    softwareCollection: 0,
    dataPurchase: 0
  },
  
  // 第3类：数据存储与备份成本
  category3: {
    storageHardware: 0,
    storageSoftware: 0,
    cloudStorage: 0,
    backupDisaster: 0
  },
  
  // 第4类：数据处理与加工成本
  category4: {
    dataCleaning: 0,
    dataIntegration: 0,
    dataModeling: 0,
    dataProcessing: 0
  },
  
  // 第5类：数据应用与分析成本
  category5: {
    businessApplication: 0,
    analyticsModeling: 0,
    visualization: 0,
    applicationMaintenance: 0
  },
  
  // 第6类：数据流通与共享成本
  category6: {
    dataExchange: 0,
    dataSharing: 0,
    externalCooperation: 0,
    dataMarket: 0
  },
  
  // 第7类：数据安全、隐私与合规成本
  category7: {
    securityHardware: 0,
    securitySoftware: 0,
    securityAudit: 0,
    privacyProtection: 0,
    complianceCertification: 0
  },
  
  // 第8类：数据归档与销毁成本
  category8: {
    archivingSystem: 0,
    dataDestruction: 0,
    lifecycleManagement: 0,
    complianceArchiving: 0
  },
  
  // 第9类：数据全流程人力成本
  category9: {
    strategyGovernance: 0,
    technicalOperations: 0,
    qualitySecurity: 0,
    dataAnalysis: 0,
    externalConsulting: 0
  }
})

// 计算单类总计
const calculateCategoryTotal = (categoryId) => {
  const categoryKey = `category${categoryId}`
  const categoryData = formData[categoryKey]
  if (!categoryData) return 0
  
  return Object.values(categoryData).reduce((sum, value) => {
    const num = Number(value) || 0
    return sum + num
  }, 0)
}

// 计算所有类别总计
const calculateTotal = () => {
  let total = 0
  for (let i = 1; i <= 9; i++) {
    total += calculateCategoryTotal(i)
  }
  return total
}

// 获取类别名称
const getCategoryName = (categoryId) => {
  const category = categories.find(cat => cat.id === categoryId)
  return category ? category.name : `类别${categoryId}`
}

// 验证表单数据
const validateFormData = () => {
  const errors = []
  
  // 检查评估名称
  if (!formData.evaluationName.trim()) {
    errors.push('评估名称不能为空')
  }
  
  // 检查至少有一项有数据
  let hasData = false
  for (let i = 1; i <= 9; i++) {
    const categoryData = formData[`category${i}`]
    if (categoryData) {
      const hasValue = Object.values(categoryData).some(value => 
        Number(value) > 0
      )
      if (hasValue) {
        hasData = true
        break
      }
    }
  }
  
  if (!hasData) {
    errors.push('请至少填写一项成本数据')
  }
  
  return errors
}

// 格式化货币显示
const formatCurrency = (value) => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value)
}

// 检查表单是否有更改
const hasChanges = computed(() => {
  return formData.evaluationName.trim() !== '' || 
         Object.values(formData).some(value => {
           if (typeof value === 'object') {
             return Object.values(value).some(v => v !== 0)
           }
           return false
         })
})

// 检查表单是否有效
const isFormValid = computed(() => {
  return formData.evaluationName.trim() !== '' && 
         calculateTotal() > 0
})

// 保存草稿（仅存本地）
const saveAsDraft = async () => {
  savingDraft.value = true
  try {
    const toSave = { ...formData, __savedAt: Date.now() }
    localStorage.setItem('evaluationDraft', JSON.stringify(toSave))
    await new Promise(resolve => setTimeout(resolve, 300))
    ElMessage.success('草稿保存成功')
  } catch (error) {
    ElMessage.error('保存草稿失败')
  } finally {
    savingDraft.value = false
  }
}

// 提交表单
const submitForm = async () => {
  // 验证表单
  const errors = validateFormData()
  if (errors.length > 0) {
    errors.forEach(error => ElMessage.warning(error))
    return
  }

  submitting.value = true
  try {
    // 准备提交数据
    const submitData = {
      name: formData.evaluationName,
      description: formData.description,
      indicators: []
    }

    // 转换表单数据为后端需要的格式
    for (let i = 1; i <= 9; i++) {
      const categoryKey = `category${i}`
      const categoryData = formData[categoryKey]
      
      if (categoryData) {
        Object.entries(categoryData).forEach(([key, value]) => {
          if (value && Number(value) > 0) {
            submitData.indicators.push({
              category: i,
              item_name: key,
              amount: Number(value)
            })
          }
        })
      }
    }

    // 调用API
    const response = await createEvaluationAPI(submitData)
    
    if (response.data && response.data.id) {
      // 清除草稿
      localStorage.removeItem('evaluationDraft')
      
      ElMessage.success('评估提交成功！')
      
      // 跳转到结果页面
      router.push(`/result/${response.data.id}`)
    }
  } catch (error) {
    ElMessage.error('提交失败：' + (error.response?.data?.message || '网络错误'))
  } finally {
    submitting.value = false
  }
}

// 组件挂载时检查是否有草稿
onMounted(() => {
  const savedDraft = localStorage.getItem('evaluationDraft')
  if (savedDraft) {
    try {
      const draftData = JSON.parse(savedDraft)
      Object.assign(formData, draftData)
      ElMessage.info('已加载上次保存的草稿')
    } catch (error) {
      console.error('加载草稿失败:', error)
    }
  }
})

// 离开页面时提示保存
window.addEventListener('beforeunload', (e) => {
  if (hasChanges.value) {
    e.preventDefault()
    e.returnValue = '您有未保存的更改，确定要离开吗？'
  }
})
</script>

<style scoped>
.data-input-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.main-card {
  margin-bottom: 20px;
}

.card-header {
  text-align: center;
  padding: 20px 0;
}

.card-header h2 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 24px;
}

.card-header p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.section-card {
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  background-color: #409EFF;
  color: white;
  border-radius: 50%;
  font-weight: bold;
}

.collapse-header {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px 0;
}

.collapse-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  background-color: #67C23A;
  color: white;
  border-radius: 50%;
  font-weight: bold;
}

.collapse-header h3 {
  margin: 0;
  flex: 1;
  font-size: 18px;
  color: #333;
}

.collapse-total {
  font-weight: bold;
  color: #E6A23C;
  font-size: 16px;
}

.collapse-content {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 4px;
  margin: 10px 0;
}

.indicator-item {
  margin-bottom: 20px;
}

.item-description {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
  line-height: 1.4;
}

.total-card {
  margin: 20px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.total-content {
  padding: 20px;
}

.total-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.total-label {
  font-size: 20px;
  font-weight: bold;
}

.total-value {
  font-size: 28px;
  font-weight: bold;
}

.total-breakdown {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 10px;
  font-size: 14px;
}

.category-total {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e6e6e6;
}
</style>