import { mount } from 'svelte'
import './app.css'
import './styles/gruvbox-themes.css'
import { initTheme } from './theme'
import Blog from './Blog.svelte'

initTheme()

const app = mount(Blog, {
  target: document.getElementById('app')!,
})

export default app
