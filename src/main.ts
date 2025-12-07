import { mount } from 'svelte'
import './app.css'
import './styles/gruvbox-themes.css'
import { initTheme } from './theme'
import Home from './Home.svelte'

initTheme()

const app = mount(Home, {
  target: document.getElementById('app')!,
})

export default app
