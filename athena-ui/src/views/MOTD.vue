<template>
  <div class="motd">
    <div class="main">
      <h1 class="title">Message Of The Day</h1>
      <div class="content">
        <div class="card">
          <h2 class="subtitle">Something cool happened!</h2>
          <img class="image" src="https://images.pexels.com/photos/1148820/pexels-photo-1148820.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"/>
          <p class="message">
            Pokem ipsum dolor sit amet Exeggutor Kecleon Wing Attack Doduo Red Unown.
            Sunt in culpa Drilbur Calcium Hoenn Shieldon Wynaut Charizard.
            Growl Venonat Scolipede Espeon Charizard Barboach Hidden Machine.
            Duis aute irure dolor in reprehenderit in voluptate they're comfy
            and easy to wear Onix what kind of Pokemon are you Fog Badge Ampharos Noctowl.
            Pewter City Marill Slakoth Bronzong Rattata Treecko Cottonee.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "MOTD",
  components: {}
};
</script>

<style scoped lang="scss">
.card {
  background-color: #101018;
  flex-basis: 80%;
  min-height: 80vh;

  border-radius: 2em;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  border: 1px solid #2cb2ff;
}

.content {
  display: flex;
  justify-content: center;
}
.title {
  color: white;
}
.subtitle {
  color: rgba(255, 255, 255, 0.9);
  font-weight: bold;
}
.image {
    max-height: 15em;
    width: auto;
    background-size: cover;
    
}
.message {
  color: rgba(255, 255, 255, 0.8);
}
</style>
