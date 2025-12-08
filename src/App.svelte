<script lang="ts">
  import Router from 'svelte-spa-router'
  import Home from './Home.svelte'
  import Blog from './Blog.svelte'
  import BlogPost from './BlogPost.svelte'
  import Books from './Books.svelte'

  const routes = {
    '/': Home,
    '/blog': Blog,
    '/blog/:slug': BlogPost,
    '/books': Books,
  }
</script>

<Router {routes} />
