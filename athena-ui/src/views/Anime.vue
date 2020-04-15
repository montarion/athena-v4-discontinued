<template>
  <div class="anime">
    <div class="main">
      <h1 class="title">Anime</h1>
      <div class="content">
        <div class="card"></div>
        <div class="card"></div>

        <div class="card"></div>
        <div class="card"></div>
        
        <div class="card"></div>
        <div class="card"></div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "Anime",
  components: {}
};
</script>

<style scoped lang="scss">
.card {
  background-image: url(https://tokyo.nl/wp-content/uploads/2014/10/manga-tekeningen.jpg);
  background-color: white;
  flex-basis: 40%;
  min-height: 15em;
  border-radius: 2em;
  margin-top: 2em;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.content {
  display: flex;
  flex-wrap: wrap;
  flex-grow: 1;
  justify-content: space-evenly;
}
.title {
  color: white;
}
</style>
