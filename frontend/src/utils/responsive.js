// frontend/src/utils/responsive.js
import { ref, onMounted, onUnmounted } from 'vue'

// 屏幕尺寸定义
export const breakpoints = {
  xs: 0,
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  '2xl': 1536
}

// 响应式Hook
export function useResponsive() {
  const width = ref(window.innerWidth)
  const height = ref(window.innerHeight)
  
  const onResize = () => {
    width.value = window.innerWidth
    height.value = window.innerHeight
  }
  
  onMounted(() => {
    window.addEventListener('resize', onResize)
  })
  
  onUnmounted(() => {
    window.removeEventListener('resize', onResize)
  })
  
  const isMobile = computed(() => width.value < breakpoints.md)
  const isTablet = computed(() => width.value >= breakpoints.md && width.value < breakpoints.lg)
  const isDesktop = computed(() => width.value >= breakpoints.lg)
  
  return {
    width,
    height,
    isMobile,
    isTablet,
    isDesktop
  }
}

// 自适应字体大小
export function useFluidTypography(minSize, maxSize, minViewport = 375, maxViewport = 1920) {
  const { width } = useResponsive()
  
  return computed(() => {
    const viewportWidth = Math.min(Math.max(width.value, minViewport), maxViewport)
    const slope = (maxSize - minSize) / (maxViewport - minViewport)
    const base = minSize - slope * minViewport
    
    return `calc(${base}px + ${slope * 100}vw)`
  })
}