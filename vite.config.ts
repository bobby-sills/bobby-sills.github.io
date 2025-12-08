import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import { plugin as markdown, Mode } from 'vite-plugin-markdown'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    svelte(),
    markdown({ mode: [Mode.HTML] })
  ],
})
