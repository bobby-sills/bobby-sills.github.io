<script lang="ts">
  import Nav from "./lib/Nav.svelte";

  $effect(() => {
    document.title = "bobby sills | blog";
  });
</script>

<main>
  <Nav />

  <h1>blog</h1>
  <p>blog posts coming soon.</p>
</main>
