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
      <p>
        9th grade developer working out of vientiane, laos. just released
        language learning app for lao. get it on
        <a href="https://apps.apple.com/us/app/read-lao/id6749076081">ios</a>
        and
        <a
          href="https://play.google.com/store/apps/details?id=com.readlao.app&pcampaignid=web_share"
        >
          android
        </a>.
      </p>
    </div>
  </div>

  <div
    style:display="grid"
    style:grid-template-columns="repeat(auto-fit, minmax(300px, 1fr))"
    style:margin="24px 0px"
    style:gap="24px"
  >
    <div>
      <h2>projects</h2>
      <ul>
        <li><a href="#/telephone-game">telephone game</a></li>
        <li>read lao app (see above)</li>
      </ul>
    </div>
    <div>
      <h2>profiles</h2>
      <ul>
        <li><a href="https://www.youtube.com/@itsmebobbysills">youtube</a></li>
        <li>
          <a href="https://monkeytype.com/profile/WriteThatDown">monkeytype</a>
        </li>
        <li>
          <a href="https://scratch.mit.edu/users/WriteThatDown">scratch</a> (not
          as active anymore)
        </li>
      </ul>
    </div>
    <div>
      <h2>work experience</h2>
      <p>I don't really have any</p>
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
