<script lang="ts">
  import Router from 'svelte-spa-router'
  import Home from './Home.svelte'
  import Blog from './Blog.svelte'
  import Books from './Books.svelte'

  const routes = {
    '/': Home,
    '/blog': Blog,
    '/books': Books,
  }
</script>

<Router {routes} />
