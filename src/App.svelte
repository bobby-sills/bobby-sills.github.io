<script lang="ts">
  import Router from "svelte-spa-router";
  import Home from "./Home.svelte";
  import Blog from "./Blog.svelte";
  import BlogPost from "./BlogPost.svelte";
  import Books from "./Books.svelte";
  import TelephoneGame from "./projects/TelephoneGame.svelte";
  import NotFound from "./NotFound.svelte";

  const routes = {
    "/": Home,
    "/blog": Blog,
    "/blog/:slug": BlogPost,
    "/books": Books,
    "/telephone-game": TelephoneGame,
    "*": NotFound,
  };
</script>

<Router {routes} />
