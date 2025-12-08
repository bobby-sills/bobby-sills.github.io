<script lang="ts">
  import Nav from "./lib/Nav.svelte";

  $effect(() => {
    document.title = "bobby sills";
  });
</script>

<main>
  <Nav />

  <div
    style:display="flex"
    style:margin="24px 0px"
    style:gap="24px"
    style:flex-wrap="wrap"
  >
    <img
      src="/profile-photo.jpg"
      alt="Portrait of a 9th grader"
      width="200"
      height="200"
    />
    <div
      style:display="flex"
      style:flex-direction="column"
      style:flex="1"
      style:min-width="300px"
    >
      <h3>bobby sills</h3>
      <span
        >9th grade developer working out of vientiane, laos. just released
        language learning app for lao. get it on
        <a href="https://apps.apple.com/us/app/read-lao/id6749076081">ios</a> and
        android (coming soon).
      </span>
      <span> </span>
    </div>
  </div>
</main>

<style>
  img {
    border-radius: 10px;
    width: 200px;
    height: 200px;
    display: block;
  }
  h3 {
    font-weight: normal;
    font-style: italic;
    color: var(--red);
  }
</style>
