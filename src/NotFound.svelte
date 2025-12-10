<script lang="ts">
  import Nav from "./lib/Nav.svelte";

  $effect(() => {
    document.title = "bobby sills | 404";
  });
</script>

<main>
  <Nav />

  <div>
    <h1 style:color="var(--red)" style:font-size="4rem" style:margin="0">
      404
    </h1>
    <h2 style:color="var(--fg)" style:font-weight="normal">page not found</h2>
    <p style:color="var(--fg2)" style:margin-top="20px">
      sorry, you probably entered in a bad url.
    </p>
  </div>
</main>

<style>
  main {
    min-height: 50vh;
  }
</style>
