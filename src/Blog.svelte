<script lang="ts">
  import Nav from "./lib/Nav.svelte";

  $effect(() => {
    document.title = "blog | bobby sills";
  });
</script>

<main>
  <Nav />

  <h1>blog</h1>
  <p>blog posts coming soon.</p>
</main>
