import { mount } from 'svelte'
import './app.css'
import './styles/gruvbox-themes.css'
import { initTheme } from './theme'
import Books from './Books.svelte'

initTheme()

const app = mount(Books, {
  target: document.getElementById('app')!,
})

export default app
